// Tokens to statements, by recursive descent. Statements are separated by
// `;`, and the last may end with one. After an expression, `(` makes a call,
// and `.name(` makes a method call. Nothing else follows an expression.
import type { Expr, Stmt } from './ast.ts';
import { Failure } from './errors.ts';
import { lex, type Token } from './lexer.ts';

const KEYWORDS = ['let', 'nil', 'true', 'false'];

const isPunct = (t: Token, text: string): boolean => t.kind === 'punct' && t.text === text;

const describe = (t: Token): string =>
    t.kind === 'eof' ? 'the end of the program'
    : t.kind === 'punct' ? `'${t.text}'`
    : t.kind === 'name' ? `'${t.name}'`
    : t.kind === 'int' ? String(t.value)
    : 'a string';

const fail = (message: string, t: Token): Failure => new Failure(message, t.pos);

// The arguments of a call, after its `(`, up to and including the `)`.
const args = (toks: readonly Token[], i: number): [Expr[], number] => {
    if (isPunct(toks[i]!, ')')) return [[], i + 1];
    const [first, j] = expr(toks, i);
    return moreArgs([first], toks, j);
};

const moreArgs = (acc: Expr[], toks: readonly Token[], i: number): [Expr[], number] => {
    const t = toks[i]!;
    if (isPunct(t, ')')) return [acc, i + 1];
    if (!isPunct(t, ',')) throw fail(`expected ',' or ')', found ${describe(t)}`, t);
    const [e, j] = expr(toks, i + 1);
    return moreArgs([...acc, e], toks, j);
};

const primary = (toks: readonly Token[], i: number): [Expr, number] => {
    const t = toks[i]!;
    if (t.kind === 'int') return [{ kind: 'int', value: t.value }, i + 1];
    if (t.kind === 'str') return [{ kind: 'str', value: t.value }, i + 1];
    if (t.kind === 'name' && (t.name === 'nil' || t.name === 'true' || t.name === 'false'))
        return [{ kind: 'const', name: t.name }, i + 1];
    if (t.kind === 'name' && !KEYWORDS.includes(t.name)) return [{ kind: 'name', name: t.name }, i + 1];
    throw fail(`expected an expression, found ${describe(t)}`, t);
};

const postfix = (e: Expr, toks: readonly Token[], i: number): [Expr, number] => {
    if (isPunct(toks[i]!, '(')) {
        const [as, j] = args(toks, i + 1);
        return postfix({ kind: 'call', fn: e, args: as }, toks, j);
    }
    if (isPunct(toks[i]!, '.')) {
        const n = toks[i + 1]!;
        if (n.kind !== 'name' || KEYWORDS.includes(n.name))
            throw fail(`expected a method name after '.', found ${describe(n)}`, n);
        const open = toks[i + 2]!;
        if (!isPunct(open, '(')) throw fail(`expected '(' after ${n.name}, found ${describe(open)}`, open);
        const [as, j] = args(toks, i + 3);
        return postfix({ kind: 'method', recv: e, name: n.name, args: as }, toks, j);
    }
    return [e, i];
};

const expr = (toks: readonly Token[], i: number): [Expr, number] => {
    const [e, j] = primary(toks, i);
    return postfix(e, toks, j);
};

const stmt = (toks: readonly Token[], i: number): [Stmt, number] => {
    const t = toks[i]!;
    if (t.kind === 'name' && t.name === 'let') {
        const n = toks[i + 1]!;
        if (n.kind !== 'name' || KEYWORDS.includes(n.name))
            throw fail(`expected a name after 'let', found ${describe(n)}`, n);
        const eq = toks[i + 2]!;
        if (!isPunct(eq, '=')) throw fail(`expected '=' after ${n.name}, found ${describe(eq)}`, eq);
        const [e, j] = expr(toks, i + 3);
        return [{ kind: 'let', name: n.name, expr: e }, j];
    }
    const [e, j] = expr(toks, i);
    return [{ kind: 'expr', expr: e }, j];
};

const program = (acc: Stmt[], toks: readonly Token[], i: number): Stmt[] => {
    const [s, j] = stmt(toks, i);
    const all = [...acc, s];
    const t = toks[j]!;
    if (t.kind === 'eof') return all;
    if (!isPunct(t, ';')) throw fail(`expected ';' or the end of the program, found ${describe(t)}`, t);
    return toks[j + 1]!.kind === 'eof' ? all : program(all, toks, j + 1);
};

export const parse = (src: string): Stmt[] => {
    const toks = lex(src);
    return toks[0]!.kind === 'eof' ? [] : program([], toks, 0);
};
