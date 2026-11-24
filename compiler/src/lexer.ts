// Text to tokens: the whole file at once, a line and column on each (D29).
// White space and comments are dropped. Character tests, not regexes.
//
// The parser doesn't steer the lexer yet. It will have to once `/` can be
// a division or the start of a pattern (D29); nothing here is ambiguous.
import { refuse } from './errors.ts';
import type { Pos } from './ast.ts';

export type Token =
    | { kind: 'word'; text: string; pos: Pos }
    | { kind: 'int'; text: string; pos: Pos }
    | { kind: 'version'; text: string; pos: Pos }
    | { kind: ';'; text: string; pos: Pos }
    | { kind: 'eof'; text: string; pos: Pos };

const isDigit = (c: string) => c >= '0' && c <= '9';
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

    while (i < src.length) {
        const c = at();
        const start = pos();
        if (isBlank(c)) {
            take();
        } else if (c === '#') {
            // perl reads switches from a first line that starts `#!`,
            // after any blanks: `-n` wraps the program in a loop over
            // stdin, and a line that doesn't say `perl` names another
            // program to run in perl's place (T72, D33).
            if (line === 1 && tokens.length === 0 && src[i + 1] === '!') {
                refuse("a first line that starts '#!' is not in the language: perl takes switches from it", start);
            }
            run(ch => ch !== '\n');
        } else if (isDigit(c)) {
            const digits = run(isDigit);
            // `1_000`, `0x10`, `1e3` are numbers in perl, and `42x3` is
            // `42 x 3`: each is a later step's, and none is two tokens.
            if (isWordStart(at())) refuse(`${digits + run(isWord)}: the only numbers so far are decimal integers`, start);
            tokens.push({ kind: 'int', text: digits, pos: start });
        } else if (isWordStart(c)) {
            let text = run(isWord);
            // A `v` and digits is a version literal, and takes the groups
            // of `.digits` that follow.
            const isVersion = text.length > 1 && text[0] === 'v' && [...text.slice(1)].every(isDigit);
            while (isVersion && at() === '.' && isDigit(src[i + 1] ?? '')) text += take() + run(isDigit);
            tokens.push({ kind: isVersion ? 'version' : 'word', text, pos: start });
        } else if (c === ';') {
            tokens.push({ kind: ';', text: take(), pos: start });
        } else {
            take();
            refuse(`'${c}' is not in the language yet`, start);
        }
    }
    tokens.push({ kind: 'eof', text: '', pos: pos() });
    return tokens;
};
