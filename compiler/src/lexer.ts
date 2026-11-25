// Text to tokens: the whole file at once, a line and column on each (D29).
// White space and comments are dropped. Character tests, not regexes.
//
// The lexer knows whether a value or an operator may come next, by the
// token before: after a value a dot joins and `x` repeats, and before one
// a dot begins `.5` and `x` is a word (T90). D29 has the parser tell it;
// the last token says as much, and will until `/` can begin a pattern.
import { refuse } from './errors.ts';
import { NAMES, NAME_MAX_LENGTH, OPERATORS, RESERVED, infixOp, isScalarValue, prefixOp, stepOp } from './names.ts';
import type { Pos } from './ast.ts';

export type Token =
    // `asFunction`: the word is `say` or `print`, one blank and a bracket
    // follow it, and perl's look along the line for the end of the call
    // fails, so that it warns `say (...) interpreted as function` (T76).
    | { kind: 'word'; text: string; pos: Pos; asFunction?: true }
    | { kind: 'int' | 'num'; text: string; pos: Pos }
    // `text` is the literal as written, quotes and all; `value` is the
    // string it stands for.
    | { kind: 'str'; text: string; value: string; pos: Pos }
    | { kind: 'version'; text: string; pos: Pos }
    // A variable: `text` is `$name`.
    | { kind: 'var'; text: string; name: string; pos: Pos }
    | { kind: ';' | '(' | ')' | ',' | '?' | ':' | '{' | '}'; text: string; pos: Pos }
    | { kind: 'op'; text: string; pos: Pos }
    | { kind: 'eof'; text: string; pos: Pos };

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
        if (isWord(at()) || at() === '.') {
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

    // A string literal. In single quotes a backslash is itself, except
    // before a backslash or the quote. In double quotes it begins an
    // escape, and a `$` or an `@` begins a variable to perl, which is
    // refused until there is interpolation (T34): perl takes some of them
    // as they stand (`"a @ b"`) and stops at others (`"a$"`).
    const string = (start: Pos): Token => {
        const from = i;
        const quote = take();
        let value = '';
        for (;;) {
            if (i >= src.length) refuse(`a string that never ends: it begins with ${quote} here`, start);
            const where = pos();
            const c = take(true);
            if (c === quote) break;
            if (c !== '\\') {
                if (quote === '"' && (c === '$' || c === '@')) {
                    refuse(`'${c}' in a double-quoted string is a variable to perl: write \\${c} (interpolation is not in the language yet)`, where);
                }
                value += c;
            } else if (quote === '"') {
                value += escape(where);
            } else {
                value += at() === '\\' || at() === "'" ? take() : '\\';
            }
        }
        return { kind: 'str', text: src.slice(from, i), value, pos: start };
    };

    // Whether the last token ends a value, so that an operator comes next.
    // `true`, `false` and `undef` are values too, and so is a `++` or `--`
    // that came after a variable.
    const afterValue = (): boolean => {
        const last = tokens.at(-1);
        if (last?.kind === 'op' && stepOp(last.text)) return tokens.at(-2)?.kind === 'var';
        return last?.kind === 'int' || last?.kind === 'num' || last?.kind === 'str' || last?.kind === ')' || last?.kind === 'var'
            || (last?.kind === 'word' && NAMES.get(last.text)?.kind === 'constant');
    };

    while (i < src.length) {
        const c = at();
        const start = pos();
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
            if (!isWordStart(at())) refuse("after '$' comes a name: a letter or '_', then letters, digits and '_'", start);
            const name = run(isWord);
            if (RESERVED.has(name)) refuse(`$${name} is not a name a variable may have`, start);
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
        } else if (c === ';' || c === '(' || c === ')' || c === ',' || c === '?' || c === ':' || c === '{' || c === '}') {
            // `sub NAME (` opens a signature, and its own `)` closes it.
            const [word, name] = [tokens.at(-2), tokens.at(-1)];
            if (c === '(' && (signature > 0 || (word?.kind === 'word' && NAMES.get(word.text)?.kind === 'sub' && name?.kind === 'word'))) signature += 1;
            if (c === ')' && signature > 0) signature -= 1;
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
