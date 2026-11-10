// Text to tokens. A name is a letter or `_`, then letters, digits and `_`,
// with an optional sigil in front that is part of the name. `//` runs a
// comment to the end of the line. A `-` directly before a digit is part of
// the integer, since there is no subtraction yet. Character tests rather than
// regular expressions, as the language has none.
import type { Pos } from './ast.ts';
import { Failure } from './errors.ts';

export type Token =
    | { kind: 'int'; value: bigint; pos: Pos }
    | { kind: 'str'; value: string; pos: Pos }
    | { kind: 'name'; name: string; pos: Pos }
    | { kind: 'punct'; text: string; pos: Pos }
    | { kind: 'eof'; pos: Pos };

type State = { readonly src: string; readonly i: number; readonly line: number; readonly col: number };

const isDigit = (c: string): boolean => c >= '0' && c <= '9';
const isLetter = (c: string): boolean => (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c === '_';
const isSpace = (c: string): boolean => c === ' ' || c === '\t' || c === '\r' || c === '\n';
const isSigil = (c: string): boolean => c === '$' || c === '@' || c === '%';
const PUNCT = '(),.;={}';

const at = (s: State): string => s.src[s.i] ?? '';
const pos = (s: State): Pos => ({ line: s.line, col: s.col });
const advance = (s: State): State =>
    at(s) === '\n' ? { ...s, i: s.i + 1, line: s.line + 1, col: 1 } : { ...s, i: s.i + 1, col: s.col + 1 };

const takeWhile = (s: State, ok: (c: string) => boolean): [string, State] => {
    let text = '';
    let t = s;
    while (ok(at(t))) { text += at(t); t = advance(t); }
    return [text, t];
};

// Blanks and comments, up to the next token.
const skip = (s0: State): State => {
    let s = s0;
    while (true) {
        if (isSpace(at(s))) s = advance(s);
        else if (at(s) === '/' && s.src[s.i + 1] === '/') { while (at(s) !== '' && at(s) !== '\n') s = advance(s); }
        else return s;
    }
};

const str = (s: State, p: Pos): [Token, State] => {
    let t = advance(s);
    let text = '';
    while (at(t) !== '"') {
        if (at(t) === '') throw new Failure('unterminated string', p);
        text += at(t);
        t = advance(t);
    }
    return [{ kind: 'str', value: text, pos: p }, advance(t)];
};

const token = (s0: State): [Token, State] => {
    const s = skip(s0);
    const p = pos(s);
    const c = at(s);
    const after = s.src[s.i + 1] ?? '';
    if (c === '') return [{ kind: 'eof', pos: p }, s];
    if (c === '"') return str(s, p);
    const negative = c === '-' && isDigit(after);
    if (negative || isDigit(c)) {
        const [digits, t] = takeWhile(negative ? advance(s) : s, isDigit);
        return [{ kind: 'int', value: BigInt(negative ? `-${digits}` : digits), pos: p }, t];
    }
    if (isSigil(c) || isLetter(c)) {
        const start = isSigil(c) ? advance(s) : s;
        if (isSigil(c) && !isLetter(at(start))) throw new Failure(`expected a name after '${c}'`, p);
        const [word, t] = takeWhile(start, x => isLetter(x) || isDigit(x));
        return [{ kind: 'name', name: (isSigil(c) ? c : '') + word, pos: p }, t];
    }
    if (PUNCT.includes(c)) return [{ kind: 'punct', text: c, pos: p }, advance(s)];
    throw new Failure(`unexpected character '${c}'`, p);
};

// The whole text as tokens, ending with one eof token.
export const lex = (src: string): Token[] => {
    const out: Token[] = [];
    let s: State = { src, i: 0, line: 1, col: 1 };
    while (true) {
        const [t, next] = token(s);
        out.push(t);
        if (t.kind === 'eof') return out;
        s = next;
    }
};
