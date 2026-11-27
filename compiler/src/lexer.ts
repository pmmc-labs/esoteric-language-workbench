// Text to tokens: the whole file at once, a line and column on each (D29).
// White space and comments are dropped. Character tests, not regexes.
//
// The lexer knows whether a value or an operator may come next, by the
// token before: after a value a dot joins and `x` repeats, and before one
// a dot begins `.5` and `x` is a word (T90). D29 has the parser tell it;
// the last token says as much, and will until `/` can begin a pattern.
import { refuse } from './errors.ts';
import { NAMES, NAME_MAX_LENGTH, OPERATORS, infixOp, isScalarValue, prefixOp, stepOp } from './names.ts';
import type { Pos } from './ast.ts';

export type Token =
    // `asFunction`: the word is `say` or `print`, one blank and a bracket
    // follow it, and perl's look along the line for the end of the call
    // fails, so that it warns `say (...) interpreted as function` (T76).
    | { kind: 'word'; text: string; pos: Pos; asFunction?: true }
    | { kind: 'int' | 'num'; text: string; pos: Pos }
    // `text` is the literal as written, quotes and all; `value` is the
    // string it stands for. `pieces`: it has a variable in it (step 11a),
    // and is these from left to right; `value` is then nothing.
    // `bare`: a word that perl makes a string of, alone in a hash's
    // braces or before `=>` (step 12; T214, T215).
    | { kind: 'str'; text: string; value: string; pos: Pos; pieces?: readonly Piece[]; bare?: true }
    | { kind: 'version'; text: string; pos: Pos }
    // `qw(...)`, its words (step 16a, D122): a bracketed list of strings.
    | { kind: 'qw'; text: string; words: readonly string[]; pos: Pos }
    // A variable: `text` is `$name`.
    | { kind: 'var'; text: string; name: string; pos: Pos }
    // An array, `@name`, and its last index, `$#name`.
    | { kind: 'array' | 'lastindex'; text: string; name: string; pos: Pos }
    // A hash, `%name` (step 12).
    | { kind: 'hash'; text: string; name: string; pos: Pos }
    // `subscript`: the brace opens or closes the key of a hash's element,
    // `$h{...}`. A `,` whose text is `=>` is the fat comma.
    | { kind: ';' | '(' | ')' | ',' | '?' | ':' | '{' | '}' | '[' | ']'; text: string; pos: Pos; subscript?: true }
    | { kind: 'op'; text: string; pos: Pos }
    | { kind: 'eof'; text: string; pos: Pos };

// An index in a string (D91): a whole number, with a minus or without, or
// a scalar variable; and in a slice a range between two of them.
export type Index =
    | { kind: 'int'; text: string; negative: boolean; pos: Pos }
    | { kind: 'var'; name: string; pos: Pos }
    | { kind: 'range'; from: Index; to: Index; pos: Pos };

// A piece of a string that has a variable in it (D92): text, or one of
// the shapes that interpolate. `pos` is the `$`'s or the `@`'s.
export type Piece =
    | { kind: 'text'; value: string }
    | { kind: 'var' | 'array' | 'lastindex'; name: string; pos: Pos }
    | { kind: 'elem'; name: string; index: Index; pos: Pos }
    // `$name{key}` (step 12b; D99): the key a word or a scalar variable.
    | { kind: 'helem'; name: string; key: { kind: 'word'; text: string } | { kind: 'var'; name: string; pos: Pos }; pos: Pos }
    | { kind: 'slice'; name: string; indexes: readonly Index[]; pos: Pos };

const INDEX = 'in a string an index is a whole number or a scalar variable (D91): take the index into a my first';
const INDEX_MAX = 9223372036854775807n;
const KEY = 'in a string a key is a word or a scalar variable, hard against its braces (D99): take the key into a my first';

const isDigit = (c: string) => c >= '0' && c <= '9';
const isOctalDigit = (c: string) => c >= '0' && c <= '7';
const isHexDigit = (c: string) => isDigit(c) || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
const isWordStart = (c: string) => (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_';
const isWord = (c: string) => isWordStart(c) || isDigit(c);
const isBlank = (c: string) => c === ' ' || c === '\t' || c === '\n';

const codePoint = (c: number) => 'U+' + c.toString(16).toUpperCase().padStart(4, '0');

// The escapes of a double-quoted string that are one letter (D43).
const ESCAPES: Readonly<Record<string, string>> = {
    n: '\n', t: '\t', r: '\r', f: '\f', b: '\b', a: '\x07', e: '\x1b',
};

export const lex = (src: string): Token[] => {
    const tokens: Token[] = [];
    // `i` counts UTF-16 units and `col` code points: a character past
    // U+FFFF is two of the first and one of the second.
    let i = 0;
    let line = 1;
    let col = 1;
    // The first line on which a character past ASCII may stand: the one
    // after `use utf8;` (T73).
    let utf8From = Infinity;
    // The line the last token ended on (a string may end lines after it
    // began), and where in the source it ended.
    let lastLine = 0;
    let lastEnd = 0;
    // How many brackets of a sub's signature are open: there, and nowhere
    // else, a `$` may stand alone, a parameter with no name (D72).
    let signature = 0;
    // For each brace that is open, whether it opened a hash's key.
    const braces: boolean[] = [];
    const at = (): string => src[i] ?? '';
    const pos = (): Pos => ({ line, col });
    const push = (t: Token): void => {
        tokens.push(t);
        lastLine = line;
        lastEnd = i;
    };

    // Every character of the file passes through here, a comment's too,
    // so this is the one place that says which characters a program may
    // hold: tab, newline and printable ASCII (D16); and, in a string or a
    // comment (`inText`) on a line after `use utf8;`, any other character
    // but a control. perl 5.42 refuses a byte past ASCII without `use
    // utf8` even in a comment, and on the line that says `use utf8;`
    // itself (T73); it ends the program at a ^D or ^Z outside a string,
    // and takes a lone carriage return for white space that doesn't end a
    // line. None is worth having.
    const take = (inText = false): string => {
        const n = src.codePointAt(i)!;
        const c = String.fromCodePoint(n);
        if (n > 0x7f) {
            if (line < utf8From) refuse(`a character past ASCII (${codePoint(n)}) needs 'use utf8;' on a line before it`, pos());
            if (!inText) refuse(`a character past ASCII (${codePoint(n)}) outside a string or a comment is not in the language`, pos());
            // Half of a pair: the driver refuses a file that isn't UTF-8,
            // and this is for a caller that isn't the driver.
            if (!isScalarValue(n)) refuse(`${codePoint(n)} is not a character`, pos());
        }
        if ((n < 0x20 && c !== '\t' && c !== '\n') || n === 0x7f) refuse(`a control character (${codePoint(n)}) is not in the language`, pos());
        i += c.length;
        if (c === '\n') { line += 1; col = 1; } else col += 1;
        return c;
    };
    const run = (more: (c: string) => boolean, inText = false): string => {
        let text = '';
        while (i < src.length && more(at())) text += take(inText);
        return text;
    };

    // A numeric literal (D38). The token is the literal as written; what
    // it is worth, and whether it is too large, are the parser's and the
    // checker's. What is refused here is a shape perl warns about or reads
    // as something else: an underscore that isn't between two digits
    // (T82); a point with no digit after it; and a number that runs into
    // a letter, a digit or a dot, which to perl is a hex float, a version
    // string, or a number joined to the next as a string (T62, T78).
    const number = (start: Pos): Token => {
        const from = i;
        const digitsOf = (ok: (c: string) => boolean): string => run(ch => ok(ch) || ch === '_');
        let kind: 'int' | 'num' = 'int';
        const parts: string[] = [];
        const based = at() === '0' && 'xXbBoO'.includes(src[i + 1] ?? ' ');
        if (based) {
            const letter = src[i + 1]!.toLowerCase();
            take(); take();
            parts.push(digitsOf(letter === 'x' ? isHexDigit : letter === 'b' ? ch => ch === '0' || ch === '1' : isOctalDigit));
        } else {
            if (isDigit(at())) parts.push(digitsOf(isDigit));
            if (at() === '.' && src[i + 1] !== '.') {
                if (!isDigit(src[i + 1] ?? '') && !isWord(src[i + 1] ?? '')) {
                    refuse(`${src.slice(from, i)}. ends with a point: write ${src.slice(from, i)}.0`, start);
                }
                if (isDigit(src[i + 1] ?? '')) {
                    take();
                    kind = 'num';
                    parts.push(digitsOf(isDigit));
                }
            }
            const sign = src[i + 1] === '+' || src[i + 1] === '-' ? 1 : 0;
            if ((at() === 'e' || at() === 'E') && isDigit(src[i + 1 + sign] ?? '')) {
                take();
                if (sign) take();
                kind = 'num';
                parts.push(digitsOf(isDigit));
            }
        }
        // (`1..3` is a range: two dots are an operator, and no part of
        // either number.)
        if (isWord(at()) || (at() === '.' && src[i + 1] !== '.')) {
            refuse(`${src.slice(from, i) + run(ch => isWord(ch) || ch === '.')} is not a number in the language`, start);
        }
        const text = src.slice(from, i);
        // Each run of digits: digits, and single underscores between them.
        const wellFormed = (part: string) => part !== '' && part.split('_').every(group => group !== '');
        if (!parts.every(wellFormed)) {
            refuse(text.includes('_') ? `${text}: an underscore goes between two digits` : `${text} is not a number in the language`, start);
        }
        return { kind, text, pos: start };
    };

    // `\x{...}`, `\o{...}` and `\N{U+...}`: digits of one base between
    // braces, and nothing else, which is less than perl takes (it allows
    // blanks and underscores in some) and none of what it warns about.
    // The opening brace is next.
    const braced = (where: Pos, shown: string, ok: (c: string) => boolean, base: number): string => {
        take();
        const digits = run(ok);
        if (digits === '' || at() !== '}') {
            refuse(`${shown}...}: ${base === 16 ? 'hex' : 'octal'} digits between the braces, and nothing else`, where);
        }
        take();
        const n = parseInt(digits, base);
        if (!isScalarValue(n)) refuse(`${shown}${digits}} is not a character: a surrogate, or past U+10FFFF`, where);
        return String.fromCodePoint(n);
    };

    // What a backslash and the characters after it stand for in a
    // double-quoted string (D43); the backslash, at `where`, is taken.
    // Refused: what perl warns about (a letter or a digit that is no
    // escape; one hex digit, or an octal escape, that a character which
    // isn't a digit of its base cuts short), what it reads in silence as
    // a NUL (`\x` alone, T86), and what belongs to interpolation or needs
    // every character's name (`\U`, `\Q`, `\N{NAME}`, `\c`).
    const escape = (where: Pos): string => {
        if (i >= src.length) return '';     // the caller says the string never ends
        const c = take(true);
        if (ESCAPES[c] !== undefined) return ESCAPES[c];
        if (isOctalDigit(c)) {
            let digits = c;
            while (digits.length < 3 && isOctalDigit(at())) digits += take();
            if (digits.length < 3 && isDigit(at())) {
                refuse(`\\${digits}${at()}: an octal escape that ${at()} cuts short, and perl warns: write \\${digits.padStart(3, '0')}`, where);
            }
            return String.fromCodePoint(parseInt(digits, 8));
        }
        if (c === 'x' && at() === '{') return braced(where, '\\x{', isHexDigit, 16);
        if (c === 'x') {
            const digits = (isHexDigit(at()) ? take() : '') + (isHexDigit(at()) ? take() : '');
            if (digits.length !== 2) refuse(`\\x${digits}: \\x takes two hex digits, or any number in braces: \\x0A, \\x{263A}`, where);
            return String.fromCodePoint(parseInt(digits, 16));
        }
        if (c === 'o' && at() === '{') return braced(where, '\\o{', isOctalDigit, 8);
        if (c === 'N' && src.startsWith('{U+', i)) {
            take(); take();
            // `braced` takes the third character, as it does a brace.
            return braced(where, '\\N{U+', isHexDigit, 16);
        }
        if (isWord(c) && c !== '_') {
            refuse(`\\${c}${c === 'N' ? '{...}' : ''} is not an escape in the language`, where);
        }
        if (c >= ' ' && c <= '~') return c;
        return refuse(`a backslash before ${c === '\n' ? 'the end of a line' : c === '\t' ? 'a tab' : codePoint(c.codePointAt(0)!)} is not in the language`, where);
    };

    // One index in a string, the next character its first (D91). A number
    // is the language's own whole-number literal: with a leading zero it
    // is octal to perl, in silence, and from 2^63 perl wraps it round to
    // the other end of the array (T211). `open` is the bracket's place,
    // for an index that the end of the string cuts short.
    const index = (open: Pos): Index => {
        const where = pos();
        const cut = (): never => (i >= src.length || at() === '"'
            ? refuse('an index in a string that does not close: write \\[ for the character', open)
            : refuse(INDEX, pos()));
        if (at() === '$') {
            take();
            if (!isWordStart(at())) refuse(INDEX, where);
            const name = run(isWord);
            if (name.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, where);
            return { kind: 'var', name, pos: where };
        }
        const negative = at() === '-';
        if (negative) {
            if (!isDigit(src[i + 1] ?? '')) refuse(INDEX, where);
            take();
        }
        if (!isDigit(at())) cut();
        const digitsAt = pos();
        const digits = run(isDigit);
        if (digits.length > 1 && digits[0] === '0') refuse(`${digits} in an index in a string: a leading zero makes it octal, to perl; write the number without it`, digitsAt);
        if (BigInt(digits) > INDEX_MAX) refuse(`an index of ${INDEX_MAX + 1n} or more in a string: perl wraps it round to the other end of the array`, digitsAt);
        return { kind: 'int', text: digits, negative, pos: where };
    };

    // The indexes between square brackets in a string, the bracket next:
    // one for an element; for a slice, any number with commas between,
    // each an index or a range between two, and a comma after the last
    // if wanted. Blanks where perl takes them, and all of it on one line:
    // to perl this is code, with comments, quotes and calls (T202).
    const indexes = (slice: boolean): Index[] => {
        const open = pos();
        take();
        const blanks = (): void => { while (at() === ' ') take(); };
        const cut = (): never => (i >= src.length || at() === '"'
            ? refuse('an index in a string that does not close: write \\[ for the character', open)
            : refuse(INDEX, pos()));
        const found: Index[] = [];
        for (;;) {
            blanks();
            let one = index(open);
            blanks();
            if (slice && src.startsWith('..', i)) {
                const dots = pos();
                take(); take();
                blanks();
                const to = index(open);
                blanks();
                one = { kind: 'range', from: one, to, pos: dots };
            }
            found.push(one);
            if (slice && at() === ',') {
                take();
                blanks();
                if (at() === ']') break;
                continue;
            }
            if (at() === ']') break;
            cut();
        }
        take();
        return found;
    };

    // A variable in a double-quoted string, its `$` or `@` just taken at
    // `where` (D92). It is one of a short list of shapes, each hard
    // against its `$` or `@`, or the string is refused: perl takes blanks
    // and a new line before a name (T200), and has thirty variables of
    // its own that are punctuation, some printing nothing in silence
    // (T204). What stands hard after a shape and perl would take into the
    // variable is refused too: `::` (T199), `{`, another `[`, an arrow
    // before `[ { @ $` (T203), and after a bare name a character past
    // ASCII, which goes on with the name if it is a letter, a digit or a
    // mark by perl's tables (T205). After a name in braces nothing is.
    const variable = (sigil: string, where: Pos): Piece => {
        const from = i - 1;
        let open = sigil;
        if (sigil === '$' && at() === '#') {
            if (!isWordStart(src[i + 1] ?? '') && src[i + 1] !== '{') {
                refuse("after '$#' in a string comes an array's name, or one in braces: write \\$ for the character", where);
            }
            take();
            open = '$#';
        }
        const kind = open === '$' ? 'var' : open === '@' ? 'array' : 'lastindex';
        const reference = (what: string): never => refuse(`${what} in a string takes a reference, and references are not in the language yet (step 13)`, where);
        if (at() === '$' && (isWordStart(src[i + 1] ?? '') || src[i + 1] === '{')) reference(open + '$');
        const tooLong = (name: string): void => {
            if (name.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, where);
        };
        if (at() === '{') {
            const inside = src[i + 1] ?? '';
            if (inside === '\\' || inside === '[' || inside === '$') reference(open + '{' + inside);
            const hard = (): never => refuse(`in a string a name in braces is hard against both of them: ${open}{name}`, where);
            take();
            if (!isWordStart(at())) hard();
            const name = run(isWord);
            if (at() === '[') refuse(`${open}{${name}[...]} in a string: perl warns that it is ambiguous; write ${open}${name}[...]`, where);
            if (at() !== '}') hard();
            take();
            if (kind === 'array' && name === '_') refuse('@_ is not in the language: a sub has a signature (D17)', where);
            tooLong(name);
            return { kind, name, pos: where };
        }
        if (!isWordStart(at())) {
            refuse(sigil === '$'
                ? "'$' in a double-quoted string begins a variable, and no name is hard against it: write \\$ for the character"
                : "'@' in a double-quoted string begins an array, and no name is hard against it: write \\@ for the character", where);
        }
        const name = run(isWord);
        if (kind === 'array' && name === '_') refuse('@_ is not in the language: a sub has a signature (D17)', where);
        if (kind === 'var' && name === '_' && (at() === '[' || at() === '{')) refuse(`$_${at()} is an element of perl's own @_ or %_, which are not in the language`, where);
        tooLong(name);
        const braced = `${open}{${name}}`;
        let piece: Piece = { kind, name, pos: where };
        if (at() === '{' && kind === 'var') {
            // An element of a hash (D99). To perl what stands in the braces
            // is code, as an index is: blanks, quotes, calls, arithmetic.
            take();
            const keyAt = pos();
            let key: (Piece & { kind: 'helem' })['key'];
            if (at() === '$') {
                take();
                if (!isWordStart(at())) refuse(KEY, keyAt);
                key = { kind: 'var', name: run(isWord), pos: keyAt };
            } else {
                if (!isWordStart(at())) refuse(KEY, keyAt);
                key = { kind: 'word', text: run(isWord) };
            }
            if (at() !== '}') refuse(KEY, i >= src.length || at() === '"' ? keyAt : pos());
            take();
            tooLong(key.kind === 'var' ? key.name : key.text);
            piece = { kind: 'helem', name, key, pos: where };
        } else if (at() === '[' && kind !== 'lastindex') {
            piece = kind === 'var' ? { kind: 'elem', name, index: indexes(false)[0]!, pos: where } : { kind: 'slice', name, indexes: indexes(true), pos: where };
        }
        const shown = src.slice(from, i);
        const named = piece.kind !== 'elem' && piece.kind !== 'slice' && piece.kind !== 'helem';
        const or = (after: string): string => (named ? `${braced}${after} or ` : '');
        // (After a hash's element `::` is text, to perl: T227.)
        if (src.startsWith('::', i) && piece.kind !== 'helem') refuse(`'::' hard after ${shown} in a string: perl reads a variable of another package; write ${or('::')}${shown}\\::`, pos());
        if (at() === '{') {
            refuse(piece.kind === 'array'
                ? `'{' hard after ${shown} in a string: a slice of a hash, to perl, which is not in a string (D99): join it first; or write ${or('{')}${shown}\\{`
                : `'{' hard after ${shown} in a string: an element of what that holds, to perl, and references are not in the language yet (step 13); write ${shown}\\{`, pos());
        }
        if (at() === '[') refuse(`'[' hard after ${shown} in a string: another index, to perl; write ${shown}\\[`, pos());
        const then = src[i + 2] ?? '';
        if (src.startsWith('->', i) && then !== '' && '[{@$'.includes(then)) {
            refuse(`'->${then}' hard after ${shown} in a string: a dereference, to perl, and references are not in the language yet (step 13); write ${shown}\\->${then}`, pos());
        }
        const next = src.codePointAt(i) ?? 0;
        if (named && next > 0x7f && line >= utf8From) {
            refuse(`a character past ASCII (${codePoint(next)}) hard after ${shown} in a string: perl takes a letter, a digit or a mark there into the name; write ${braced}`, pos());
        }
        return piece;
    };

    // A string literal. In single quotes a backslash is itself, except
    // before a backslash or the quote. In double quotes it begins an
    // escape, and a `$` or an `@` begins a variable (step 11a).
    const string = (start: Pos): Token => {
        const from = i;
        const quote = take();
        let value = '';
        const pieces: Piece[] = [];
        for (;;) {
            if (i >= src.length) refuse(`a string that never ends: it begins with ${quote} here`, start);
            const where = pos();
            const c = take(true);
            if (c === quote) break;
            if (c !== '\\') {
                if (quote === '"' && (c === '$' || c === '@')) {
                    if (value !== '') pieces.push({ kind: 'text', value });
                    value = '';
                    pieces.push(variable(c, where));
                    continue;
                }
                value += c;
            } else if (quote === '"') {
                value += escape(where);
            } else {
                value += at() === '\\' || at() === "'" ? take() : '\\';
            }
        }
        if (pieces.length === 0) return { kind: 'str', text: src.slice(from, i), value, pos: start };
        if (value !== '') pieces.push({ kind: 'text', value });
        return { kind: 'str', text: src.slice(from, i), value: '', pos: start, pieces };
    };

    // Whether the last token ends a value, so that an operator comes next.
    // `true`, `false` and `undef` are values too, and so is a `++` or `--`
    // that came after a variable.
    const afterValue = (): boolean => {
        const last = tokens.at(-1);
        if (last?.kind === 'op' && stepOp(last.text)) {
            const target = tokens.at(-2);
            return target?.kind === 'var' || target?.kind === ']' || (target?.kind === '}' && target.subscript === true);
        }
        return last?.kind === 'int' || last?.kind === 'num' || last?.kind === 'str' || last?.kind === 'qw' || last?.kind === ')' || last?.kind === 'var'
            || last?.kind === ']' || last?.kind === 'array' || last?.kind === 'lastindex' || last?.kind === 'hash'
            || (last?.kind === '}' && last.subscript === true)
            || (last?.kind === 'word' && NAMES.get(last.text)?.kind === 'constant');
    };

    // Where the blanks from `k` on end: spaces and tabs, and with `lines`
    // the ends of lines and comments too.
    const past = (k: number, lines: boolean): number => {
        for (;;) {
            const ch = src[k] ?? '';
            if (ch === ' ' || ch === '\t' || (lines && ch === '\n')) k += 1;
            else if (lines && ch === '#') k = src.indexOf('\n', k) < 0 ? src.length : src.indexOf('\n', k);
            else return k;
        }
    };
    // Where the word that starts at `k` ends.
    const wordEnd = (k: number): number => {
        while (k < src.length && isWord(src[k]!)) k += 1;
        return k;
    };
    // A word that is a string: the next characters, taken.
    const bare = (): void => {
        const start = pos();
        const text = run(isWord);
        if (text.length > NAME_MAX_LENGTH) refuse(`a word of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, start);
        push({ kind: 'str', text, value: text, pos: start, bare: true });
    };

    // ---- step 16a: `q`, `qq`, `qw` and heredocs (D121 to D123)

    // Where perl's string ends, the opening bracket just before `from`:
    // brackets of its kind nest, and a backslash takes the character
    // after it with it. perl finds the end first and reads what is
    // between after, so this does too.
    const closing = (from: number, open: string, close: string, start: Pos, shown: string): number => {
        let depth = 1;
        for (let k = from; k < src.length; k++) {
            const ch = src[k]!;
            if (ch === '\\') k += 1;
            else if (ch === open) depth += 1;
            else if (ch === close && --depth === 0) return k;
        }
        return refuse(`${shown} that never ends: it begins here`, start);
    };

    // The characters from here to `end`, as a string. With `interpolate`
    // they are a double-quoted string's, its escapes and its variables
    // exactly (D43, D91 to D99); otherwise each is itself, but that a
    // backslash before one of `backslashed` is taken away. `indent` is
    // what a `<<~` heredoc takes off the start of each line. `brackets`:
    // a `qq`'s own, before which perl takes a backslash away before it
    // interpolates, so that `qq[$x\[0\]]` is an element (T278).
    const body = (end: number, interpolate: boolean, backslashed: string, indent: string, brackets = ''): { value: string; pieces?: Piece[] } => {
        let value = '';
        const pieces: Piece[] = [];
        let lineStart = true;
        const inside = (): void => {
            if (i > end) refuse('what stands in this string runs past its end: perl ends the string first, and does not compile the rest', pos());
        };
        while (i < end) {
            if (lineStart && indent !== '') {
                lineStart = false;
                if (src.startsWith(indent, i)) {
                    for (let n = 0; n < indent.length; n++) take();
                    continue;
                }
                if (at() !== '\n') refuse("a line of a <<~ heredoc that does not begin with the blanks before its terminator: perl dies (T263)", pos());
            }
            const where = pos();
            const c = take(true);
            lineStart = c === '\n';
            if (interpolate && (c === '$' || c === '@')) {
                if (value !== '') pieces.push({ kind: 'text', value });
                value = '';
                pieces.push(variable(c, where));
                inside();
            } else if (c === '\\' && interpolate) {
                if (brackets.includes(at())) refuse(`a backslash before '${at()}' in a qq with that bracket: perl takes it away before it reads the variables, so that what follows can go on with one (T278); write the string with other brackets`, where);
                value += escape(where);
                inside();
            } else if (c === '\\' && i < end && backslashed.includes(at())) {
                value += take(true);
            } else {
                value += c;
            }
        }
        if (pieces.length === 0) return { value };
        if (value !== '') pieces.push({ kind: 'text', value });
        return { value: '', pieces };
    };

    // `q(...)`, `qq(...)` and `qw(...)`, with any of the four brackets
    // hard against the word (D121); the word is next.
    const BRACKETS: Readonly<Record<string, string>> = { '(': ')', '[': ']', '{': '}', '<': '>' };
    const quoteLike = (start: Pos): void => {
        const from = i;
        const word = run(isWord);
        const open = at();
        const close = BRACKETS[open];
        if (close === undefined) {
            refuse(`${word} takes a bracket hard against it, and no other delimiter: ${word}(...), ${word}[...], ${word}{...} or ${word}<...> (D121)`, start);
        }
        const end = closing(i + 1, open, close, start, `${word}${open}...${close}`);
        take();
        if (word === 'qw') {
            // The words between blanks (D122). perl warns of a comma and
            // a `#` in one, and a backslash there is taken away before a
            // bracket and kept anywhere else (T261).
            const words: string[] = [];
            let w = '';
            while (i < end) {
                const where = pos();
                const ch = take(true);
                if (isBlank(ch)) {
                    if (w !== '') words.push(w);
                    w = '';
                    continue;
                }
                if (ch === ',') refuse('a comma in qw(...): perl warns that it may be meant to separate the words, and keeps it in one', where);
                if (ch === '#') refuse("a '#' in qw(...): perl warns that it may be meant for a comment, and keeps it in a word", where);
                if (ch === '\\') refuse('a backslash in qw(...): perl keeps it, or takes it away before a bracket (T261); write the list in quotes', where);
                w += ch;
            }
            if (w !== '') words.push(w);
            take();
            push({ kind: 'qw', text: src.slice(from, i), words, pos: start });
            return;
        }
        const read = body(end, word === 'qq', word === 'q' ? '\\' + open + close : '', '', word === 'qq' ? open + close : '');
        take();
        push(read.pieces === undefined
            ? { kind: 'str', text: src.slice(from, i), value: read.value, pos: start }
            : { kind: 'str', text: src.slice(from, i), value: '', pos: start, pieces: read.pieces });
    };

    // A heredoc waiting for the end of its line, and where the lexer goes
    // on from when it gets there: past the body and its terminator.
    let heredoc: { line: number; resume: number; resumeLine: number; at: Pos } | undefined;

    // `<<"END"`, `<<END`, `<<'END'`, each with `~` or without (D123); the
    // `<<` is next. The body is read now, and skipped when the line ends.
    const hereDoc = (start: Pos): void => {
        const from = i;
        take();
        take();
        const squiggle = at() === '~';
        if (squiggle) take();
        const lead = `<<${squiggle ? '~' : ''}`;
        let quote = '';
        if (at() === '"' || at() === "'") quote = take();
        if (!isWordStart(at())) {
            refuse(isBlank(at()) || at() === ''
                ? `a blank after '${lead}${quote}': a heredoc's terminator is a word hard against it, ${lead}"END"`
                : `a heredoc's terminator is a word, a letter or '_' first: ${lead}"END"`, start);
        }
        const word = run(isWord);
        if (quote !== '') {
            if (at() !== quote) refuse(`a heredoc's terminator is a word between its quotes: ${lead}${quote}END${quote}`, start);
            take();
        }
        if (heredoc !== undefined) refuse('a second heredoc on one line: write each on a line of its own', start);
        const newline = src.indexOf('\n', i);
        const never = (): never => refuse(`a heredoc that never ends: no line is ${word} alone${squiggle ? ', after blanks' : ''}`, start);
        if (newline < 0) never();
        // The terminator's line: the word alone, or with `~` after blanks.
        let k = newline + 1;
        let indent = '';
        let bodyEnd = -1;
        let lineEnd = 0;
        while (k < src.length) {
            const e = src.indexOf('\n', k);
            lineEnd = e < 0 ? src.length : e;
            const text = src.slice(k, lineEnd);
            const blanks = squiggle ? text.length - text.replace(/^[ \t]*/, '').length : 0;
            if (text.slice(blanks) === word) {
                indent = text.slice(0, blanks);
                bodyEnd = k;
                break;
            }
            k = lineEnd + 1;
        }
        if (bodyEnd < 0) never();
        const text = src.slice(from, i);
        const [atI, atLine, atCol] = [i, line, col];
        i = newline + 1;
        line = atLine + 1;
        col = 1;
        const read = body(bodyEnd, quote !== "'", '', indent);
        const resumeLine = line + 1;
        [i, line, col] = [atI, atLine, atCol];
        heredoc = { line, resume: Math.min(lineEnd + 1, src.length), resumeLine, at: start };
        push(read.pieces === undefined
            ? { kind: 'str', text, value: read.value, pos: start }
            : { kind: 'str', text, value: '', pos: start, pieces: read.pieces });
    };

    while (i < src.length) {
        const c = at();
        const start = pos();
        // A heredoc's line ends here, and the lexer goes on past its body
        // (D123); what went on past the end of the line hid the body from
        // perl, or moved it (T264).
        if (heredoc !== undefined && line !== heredoc.line) {
            refuse('this goes on past the end of the line a heredoc stands on: perl reads the body after it, or does not find it (T264)', heredoc.at);
        }
        if (heredoc !== undefined && c === '\n') {
            [i, line, col] = [heredoc.resume, heredoc.resumeLine, 1];
            heredoc = undefined;
            continue;
        }
        if (isBlank(c)) {
            take();
        } else if (c === '#') {
            // perl reads switches from a line that starts `#!`, after any
            // blanks, if it is line 1: `-n` wraps the program in a loop
            // over stdin, and a line that doesn't say `perl` names another
            // program to run in perl's place. And line 1 is whichever line
            // perl calls 1: a `# line 1` comment above it will do. So no
            // line may start that way (T72, D33).
            if (src[i + 1] === '!' && lastLine !== line) {
                refuse("a line that starts '#!' is not in the language: perl can take switches from it", start);
            }
            run(ch => ch !== '\n', true);
        } else if (c === '"' || c === "'") {
            push(string(start));
        } else if (isDigit(c) || (c === '.' && isDigit(src[i + 1] ?? '') && !afterValue())) {
            push(number(start));
        } else if (isWordStart(c) && !afterValue() && src.startsWith('=>', past(wordEnd(i), true))) {
            // A word before `=>` is a string, whatever the word (T214):
            // on one line. Across the end of a line perl makes a string
            // of every word but a `v` and digits, which is a version
            // string there, the character of that number (T224).
            if (!src.startsWith('=>', past(wordEnd(i), false))) {
                refuse(`${src.slice(i, wordEnd(i))} and its '=>' are on one line: across the end of a line perl does not make a string of every word; write the word in quotes`, start);
            }
            bare();
        } else if (c === '=' && src[i + 1] === '>') {
            // The fat comma: a comma, the word before it a string already.
            take(); take();
            push({ kind: ',', text: '=>', pos: start });
        } else if (c === '%' && !afterValue()) {
            // A hash, `%name` (step 12). After a value the same character
            // is the modulus, as it is to perl.
            take();
            // In a signature a `%` alone is a parameter with no name.
            if (signature > 0 && !isWordStart(at()) && at() !== '$' && at() !== '{') {
                push({ kind: 'hash', text: '%', name: '', pos: start });
                continue;
            }
            if (at() === '$' || at() === '{') refuse("'%' before a reference: references are not in the language yet (step 13)", start);
            if (!isWordStart(at())) refuse("after '%' comes a name: a letter or '_', then letters, digits and '_'", start);
            const name = run(isWord);
            if (name === '_') refuse("%_ is perl's own, and not in the language", start);
            if (name.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, start);
            if (at() === '{') refuse(`%${name}{...} is a slice of keys and values, and not in the language`, start);
            if (at() === '[') refuse(`%${name}[...] is a slice of indexes and values, and not in the language`, start);
            push({ kind: 'hash', text: '%' + name, name, pos: start });
        } else if (isWordStart(c) && !afterValue() && ['q', 'qq', 'qw'].includes(src.slice(i, wordEnd(i)))
            && !(tokens.at(-1)?.kind === 'word' && NAMES.get(tokens.at(-1)!.text)?.kind === 'sub')) {
            // (`sub q(...)` names a sub, which the parser refuses: T28.)
            quoteLike(start);
        } else if (c === '<' && src[i + 1] === '<' && !afterValue()) {
            hereDoc(start);
        } else if (isWordStart(c)) {
            const operator = afterValue();
            let text = run(isWord);
            // After a value, `x` is the repetition operator. perl takes
            // it hard against a number too, `"ab" x3`, and stops at `$s
            // x3`, where `x3` is a word to it (T57): here it is a word of
            // its own. `x=` is the assignment.
            // The other operators that are words (`lt`, `and`) are
            // operators after a value too, and `not` is one before one.
            // Each is a word of its own: `1 lt2` is no operator to perl.
            if (operator ? infixOp(text) : prefixOp(text)) {
                // `x=` is one operator to perl, the assignment.
                if (operator && at() === '=' && infixOp(text + '=')) text += take();
                push({ kind: 'op', text, pos: start });
                continue;
            }
            if (operator && text[0] === 'x' && [...text.slice(1)].every(isDigit)) {
                refuse(`${text}: the repetition operator is a word of its own: write x ${text.slice(1)}`, start);
            }
            // A `v` and digits is a version literal, and takes the groups
            // of `.digits` that follow.
            const isVersion = text.length > 1 && text[0] === 'v' && [...text.slice(1)].every(isDigit);
            while (isVersion && at() === '.' && isDigit(src[i + 1] ?? '')) text += take() + run(isDigit);
            // perl looks at the one character after it to decide that this
            // is a version, and a `#` there isn't good enough: `use
            // v5.42#c` asks for a module called v5 (T75).
            // (`take` first, so that a character no program may hold is
            // refused as that.)
            if (isVersion && i < src.length && !isBlank(at()) && at() !== ';') {
                refuse(`${text} runs into '${take()}': perl reads a version only before a blank or ';'`, start);
            }
            // `say (` with exactly one space: perl looks along the rest
            // of the line, as text, for the bracket that closes this one
            // and then for what may follow a call, and warns `say (...)
            // interpreted as function` when it doesn't find them (T76).
            // It counts every bracket it passes, one in a string or a
            // comment too, so `say ("(");` warns (T100). The characters
            // it is content to find are its own list, begun with `;`.
            // The parser refuses it, after what it has to say itself.
            let asFunction = false;
            if (NAMES.get(text)?.kind === 'statement' && at() === ' ' && src[i + 1] === '(') {
                const newline = src.indexOf('\n', i);
                const end = newline < 0 ? src.length : newline;
                let w = i + 2;
                let level = 1;
                for (; w < end && level > 0; w++) level += src[w] === '(' ? 1 : src[w] === ')' ? -1 : 0;
                while (w < end && (src[w] === ' ' || src[w] === '\t')) w++;
                asFunction = level > 0 || w >= end || !';&/|})]oaiuwef!='.includes(src[w]!);
            }
            push(isVersion ? { kind: 'version', text, pos: start } : asFunction ? { kind: 'word', text, pos: start, asFunction } : { kind: 'word', text, pos: start });
        } else if (c === '$') {
            // A variable is `$name`, and nothing else (D55): perl also
            // takes `$ name` and `${name}`, and warns of the second.
            take();
            if (signature > 0 && !isWordStart(at())) {
                push({ kind: 'var', text: '$', name: '', pos: start });
                continue;
            }
            // `$#name`, the last index of `@name`. perl takes `$#{name}`
            // and warns, and `$# name` not at all.
            if (at() === '#') {
                take();
                if (!isWordStart(at())) refuse("after '$#' comes an array's name: $#a is the last index of @a", start);
                const array = run(isWord);
                if (array.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, start);
                push({ kind: 'lastindex', text: '$#' + array, name: array, pos: start });
                continue;
            }
            if (!isWordStart(at())) refuse("after '$' comes a name: a letter or '_', then letters, digits and '_'", start);
            const name = run(isWord);
            // `$a[0]` is an element of `@a`, which is a name an array may
            // have; `$a` alone is `sort`'s (D55).
            // `$_` is what a `for`, a `map` or a `grep` gives its block
            // (step 10b); `$_[0]` is an element of `@_`, to perl.
            if (name === '_' && (at() === '[' || at() === '{')) refuse(`$_${at()} is an element of perl's own @_ or %_, which are not in the language`, start);
            // (`$a` and `$b` are a `sort` block's, step 10c: the resolver
            // refuses them anywhere else.)
            // perl stops the compile at a longer one: `Identifier too long`.
            if (name.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, start);
            // perl takes a variable that comes first after `say` or
            // `print`, brackets between or not, for a file handle when
            // what follows the blank after it could begin a value, and
            // dies or doesn't compile (T26, T111). The same after
            // `substr(` and `index(`, which are list operators to perl
            // too: `substr($x -1, 0)` doesn't compile (T125). The list is perl's own
            // (toke.c), less what is no program here either way: a sign
            // hard against what follows it, a dot and a digit, a star, a
            // percent, a less-than or an ampersand hard against a name, a
            // slash hard against anything but an equals or a slash.
            let before = tokens.length - 1;
            while (tokens[before]?.kind === '(') before -= 1;
            const lop = tokens[before];
            const lopKind = lop?.kind === 'word' ? NAMES.get(lop.text)?.kind : undefined;
            if (lop !== undefined && (lopKind === 'statement' || lopKind === 'function') && isBlank(at())) {
                let w = i;
                while (w < src.length && (isBlank(src[w]!) || src[w] === '#')) {
                    w = src[w] === '#' ? Math.max(src.indexOf('\n', w), w + 1) : w + 1;
                }
                const a = src[w] ?? '';
                const b = src[w + 1] ?? '';
                const hard = b !== '' && !isBlank(b);
                const handle = ((a === '-' || a === '+') && hard && b !== '=')
                    || (a === '.' && isDigit(b))
                    || ((a === '*' || a === '%' || a === '<' || a === '&') && isWordStart(b))
                    || (a === '/' && hard && b !== '=' && b !== '/');
                if (handle) {
                    refuse(`${lop.text} $${name} ${a}${b}: perl takes $${name} for a file handle here; put a blank after the '${a}', or none before it`, start);
                }
            }
            push({ kind: 'var', text: '$' + name, name, pos: start });
        } else if (c === '@') {
            // An array, `@name`: perl takes `@ name` and `@{name}` too.
            take();
            if (signature > 0 && !isWordStart(at())) {
                push({ kind: 'array', text: '@', name: '', pos: start });
                continue;
            }
            if (!isWordStart(at())) refuse("after '@' comes a name: a letter or '_', then letters, digits and '_'", start);
            const name = run(isWord);
            if (name === '_') refuse('@_ is not in the language: a sub has a signature (D17)', start);
            if (name.length > NAME_MAX_LENGTH) refuse(`a name of more than ${NAME_MAX_LENGTH} characters: perl refuses it as too long`, start);
            push({ kind: 'array', text: '@' + name, name, pos: start });
        } else if (c === ';' || c === '(' || c === ')' || c === ',' || c === '?' || c === ':' || c === '{' || c === '}' || c === '[' || c === ']') {
            // `sub NAME (` opens a signature, and its own `)` closes it.
            const [word, name] = [tokens.at(-2), tokens.at(-1)];
            if (c === '(' && (signature > 0 || (word?.kind === 'word' && NAMES.get(word.text)?.kind === 'sub' && name?.kind === 'word'))) signature += 1;
            if (c === ')' && signature > 0) signature -= 1;
            // A brace hard after a variable opens a hash's key, `$h{...}`.
            // (perl takes a blank between the two, and the parser refuses
            // it: nothing else a brace could be stands after a variable.)
            if (c === '{' && (name?.kind === 'var' || name?.kind === 'array') && lastEnd === i) {
                braces.push(true);
                push({ kind: '{', text: take(), pos: start, subscript: true });
                // One word alone in the braces is that string, whatever
                // the word (T215): on one line with its braces. Across the
                // end of a line `true` is the key 1 to perl, and `v65` is
                // `A`, in silence (T223).
                // And `-word` alone there is the string `-word`.
                const sign = past(i, false);
                if (src[sign] === '-' && isWordStart(src[sign + 1] ?? '') && src[past(wordEnd(sign + 1), false)] === '}') {
                    const text = src.slice(sign, wordEnd(sign + 1));
                    refuse(`${text} alone in a hash's braces is the string ${text}, to perl: write it in quotes`, { line, col: col + sign - i });
                }
                const from = past(i, true);
                if (isWordStart(src[from] ?? '') && src[past(wordEnd(from), true)] === '}') {
                    const near = past(i, false);
                    if (near !== from || src[past(wordEnd(near), false)] !== '}') {
                        refuse(`a word alone in a hash's braces is on one line with them: across the end of a line perl does not make a string of every word; write the word in quotes`, start);
                    }
                    run(ch => ch === ' ' || ch === '\t');
                    bare();
                }
                continue;
            }
            if (c === '{') braces.push(false);
            if (c === '}' && braces.pop() === true) {
                push({ kind: '}', text: take(), pos: start, subscript: true });
                continue;
            }
            push({ kind: c, text: take(), pos: start });
            // `use utf8;` is in force from the next line (T73). Whether it
            // may stand where it does is the checker's to say.
            const [use, utf8] = [tokens.at(-3), tokens.at(-2)];
            if (c === ';' && use?.kind === 'word' && use.text === 'use' && utf8?.kind === 'word' && utf8.text === 'utf8') {
                utf8From = Math.min(utf8From, line + 1);
            }
        } else {
            // The longest of perl's operators that starts here: `--` is a
            // decrement and never two minus signs, `**` never two stars
            // (T27). One the language doesn't have yet is refused as the
            // whole operator it is to perl.
            const op = [3, 2, 1].map(n => src.slice(i, i + n)).find(s => OPERATORS.has(s)) ?? c;
            const last = tokens.at(-1);
            const between = src.slice(lastEnd, i);
            for (const _ of op) take();
            if (!prefixOp(op) && !infixOp(op) && !stepOp(op)) refuse(`'${op}' is not in the language yet`, start);
            // `$x =- $y`: perl warns `Reversed -= operator` when a sign is
            // hard after a `=` and a blank follows the sign (T127).
            if (infixOp(op)?.assign && op.length === 1 && prefixOp(at())?.sign && isBlank(src[i + 1] ?? '')) {
                refuse(`'${op}${at()}' with a blank after it: perl warns that it reads as '${at()}${op}' reversed; put a blank after the '${op}'`, start);
            }
            // A sign after a named unary operator is the sign of its
            // argument, `length -5`, and perl warns that the rest are
            // ambiguous: `length - 5` and `length-5`, which read as a
            // subtraction and aren't one. It goes by the characters: a
            // blank before the sign and none after (T94). On a line
            // below the name perl looks at how that line begins; here
            // the sign is on the name's own line.
            if (prefixOp(op)?.sign && last?.kind === 'word' && NAMES.get(last.text)?.kind === 'unary'
                && (between === '' || [...between].some(ch => ch !== ' ' && ch !== '\t') || isBlank(at()))) {
                refuse(`${last.text} ${op}: perl warns that this is ambiguous: write ${last.text}(${op}...)`, start);
            }
            push({ kind: 'op', text: op, pos: start });
        }
    }
    tokens.push({ kind: 'eof', text: '', pos: pos() });
    return tokens;
};
