// Text to forms: integers, symbols and lists, `;` to the end of a line a
// comment. Character tests rather than regexes, since the language this
// becomes won't have them.
import { CompileError } from './errors.ts';
import type { Form, Pos } from './sexp.ts';

type State = { src: string; i: number; line: number; col: number };

const isSpace = (c: string) => c === ' ' || c === '\n' || c === '\t' || c === '\r';
const isDigit = (c: string) => c >= '0' && c <= '9';
const isDelim = (c: string) => c === '' || isSpace(c) || c === '(' || c === ')' || c === ';';

const at = (s: State): string => s.src[s.i] ?? '';
const pos = (s: State): Pos => ({ line: s.line, col: s.col });
const step = (s: State): State =>
    at(s) === '\n' ? { ...s, i: s.i + 1, line: s.line + 1, col: 1 } : { ...s, i: s.i + 1, col: s.col + 1 };

const skip = (s: State): State => {
    while (true) {
        if (isSpace(at(s))) s = step(s);
        else if (at(s) === ';') { while (at(s) !== '' && at(s) !== '\n') s = step(s); }
        else return s;
    }
};

const readAtom = (s: State): [Form, State] => {
    const p = pos(s);
    let text = '';
    while (!isDelim(at(s))) { text += at(s); s = step(s); }
    const digits = text[0] === '-' ? text.slice(1) : text;
    const isInt = digits.length > 0 && [...digits].every(isDigit);
    return [isInt ? { kind: 'int', value: BigInt(text), pos: p } : { kind: 'symbol', name: text, pos: p }, s];
};

const readForm = (s: State): [Form, State] => {
    s = skip(s);
    const c = at(s);
    if (c === '') throw new CompileError('unexpected end of input', s.line, s.col);
    if (c === ')') throw new CompileError("unexpected ')'", s.line, s.col);
    if (c !== '(') return readAtom(s);
    const p = pos(s);
    const items: Form[] = [];
    s = step(s);
    while (true) {
        s = skip(s);
        if (at(s) === '') throw new CompileError("missing ')'", p.line, p.col);
        if (at(s) === ')') return [{ kind: 'list', items, pos: p }, step(s)];
        const [item, next] = readForm(s);
        items.push(item);
        s = next;
    }
};

// Every top-level form in the text, in order.
export const read = (src: string): Form[] => {
    const forms: Form[] = [];
    let s: State = { src, i: 0, line: 1, col: 1 };
    while (true) {
        s = skip(s);
        if (at(s) === '') return forms;
        const [form, next] = readForm(s);
        forms.push(form);
        s = next;
    }
};
