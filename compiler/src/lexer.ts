// Text to tokens: the whole file at once, a line and column on each (D29).
// White space and comments are dropped. Character tests, not regexes.
//
// The parser doesn't steer the lexer yet. It will have to once `/` can be
// a division or the start of a pattern (D29); nothing here is ambiguous.
import { refuse } from './errors.ts';
import { OPERATORS, infixOp, prefixOp } from './names.ts';
import type { Pos } from './ast.ts';

export type Token =
    | { kind: 'word'; text: string; pos: Pos }
    | { kind: 'int' | 'num'; text: string; pos: Pos }
    | { kind: 'version'; text: string; pos: Pos }
    | { kind: ';' | '(' | ')'; text: string; pos: Pos }
    | { kind: 'op'; text: string; pos: Pos }
    | { kind: 'eof'; text: string; pos: Pos };

const isDigit = (c: string) => c >= '0' && c <= '9';
const isHexDigit = (c: string) => isDigit(c) || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
const isWordStart = (c: string) => (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_';
const isWord = (c: string) => isWordStart(c) || isDigit(c);
const isBlank = (c: string) => c === ' ' || c === '\t' || c === '\n';

const codePoint = (c: number) => 'U+' + c.toString(16).toUpperCase().padStart(4, '0');

export const lex = (src: string): Token[] => {
    const tokens: Token[] = [];
    // `i` counts UTF-16 units and `col` code points. They move together
    // because the first character past ASCII is refused: step 3, which
    // brings `use utf8`, has to count a pair of surrogates as one column.
    let i = 0;
    let line = 1;
    let col = 1;
    const at = (): string => src[i] ?? '';
    const pos = (): Pos => ({ line, col });

    // Every character of the file passes through here, a comment's too,
    // so this is the one place that says which characters a program may
    // hold: tab, newline and printable ASCII (D16). perl 5.42 refuses a
    // byte past ASCII without `use utf8` even in a comment (T73), ends
    // the program at a ^D or ^Z outside one, and takes a lone carriage
    // return for white space that doesn't end a line. None is worth
    // having.
    const take = (): string => {
        const c = src[i]!;
        const n = src.codePointAt(i)!;
        if (n > 0x7f) refuse(`a character past ASCII (${codePoint(n)}) is not in the language yet`, pos());
        if ((n < 0x20 && c !== '\t' && c !== '\n') || n === 0x7f) refuse(`a control character (${codePoint(n)}) is not in the language`, pos());
        i += 1;
        if (c === '\n') { line += 1; col = 1; } else col += 1;
        return c;
    };
    const run = (more: (c: string) => boolean): string => {
        let text = '';
        while (i < src.length && more(at())) text += take();
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
            parts.push(digitsOf(letter === 'x' ? isHexDigit : letter === 'b' ? ch => ch === '0' || ch === '1' : ch => ch >= '0' && ch <= '7'));
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
            if (src[i + 1] === '!' && tokens.at(-1)?.pos.line !== line) {
                refuse("a line that starts '#!' is not in the language: perl can take switches from it", start);
            }
            run(ch => ch !== '\n');
        } else if (isDigit(c) || (c === '.' && isDigit(src[i + 1] ?? ''))) {
            tokens.push(number(start));
        } else if (isWordStart(c)) {
            let text = run(isWord);
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
            tokens.push({ kind: isVersion ? 'version' : 'word', text, pos: start });
        } else if (c === ';' || c === '(' || c === ')') {
            tokens.push({ kind: c, text: take(), pos: start });
        } else {
            // The longest of perl's operators that starts here: `--` is a
            // decrement and never two minus signs, `**` never two stars
            // (T27). One the language doesn't have yet is refused as the
            // whole operator it is to perl.
            const op = [3, 2, 1].map(n => src.slice(i, i + n)).find(s => OPERATORS.has(s)) ?? c;
            for (const _ of op) take();
            if (!prefixOp(op) && !infixOp(op)) refuse(`'${op}' is not in the language yet`, start);
            tokens.push({ kind: 'op', text: op, pos: start });
        }
    }
    tokens.push({ kind: 'eof', text: '', pos: pos() });
    return tokens;
};
