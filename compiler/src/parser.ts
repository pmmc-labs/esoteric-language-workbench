// Tokens to statements, by recursive descent. Statements are separated by
// `;`, and the last may end with one. A program is statements to the end of
// the text; a function body is statements between braces. After an
// expression, `(` makes a call, and `.name(` makes a method call. Nothing
// else follows an expression.
import type { Expr, Stmt } from './ast.ts';
import { Failure } from './errors.ts';
import { lex, type Token } from './lexer.ts';

const KEYWORDS = ['let', 'function', 'nil', 'true', 'false'];

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

// The parameter names of a function, after its `(`, up to and including the `)`.
const params = (toks: readonly Token[], i: number): [string[], number] => {
    if (isPunct(toks[i]!, ')')) return [[], i + 1];
    return moreParams([], toks, i);
};

const moreParams = (acc: string[], toks: readonly Token[], i: number): [string[], number] => {
    const t = toks[i]!;
    if (t.kind !== 'name' || KEYWORDS.includes(t.name)) throw fail(`expected a parameter name, found ${describe(t)}`, t);
    if (acc.includes(t.name)) throw fail(`duplicate parameter ${t.name}`, t);
    const all = [...acc, t.name];
    const n = toks[i + 1]!;
    if (isPunct(n, ')')) return [all, i + 2];
    if (!isPunct(n, ',')) throw fail(`expected ',' or ')' after a parameter, found ${describe(n)}`, n);
    return moreParams(all, toks, i + 2);
};

// A function literal, from the token after `function`.
const func = (toks: readonly Token[], i: number): [Expr, number] => {
    const open = toks[i]!;
    if (!isPunct(open, '(')) throw fail(`expected '(' after 'function', found ${describe(open)}`, open);
    const [ps, j] = params(toks, i + 1);
    const brace = toks[j]!;
    if (!isPunct(brace, '{')) throw fail(`expected '{' after the parameters, found ${describe(brace)}`, brace);
    const [body, k] = stmts([], toks, j + 1, '}');
    return [{ kind: 'function', params: ps, body }, k + 1];
};

const primary = (toks: readonly Token[], i: number): [Expr, number] => {
    const t = toks[i]!;
    if (t.kind === 'int') return [{ kind: 'int', value: t.value }, i + 1];
    if (t.kind === 'str') return [{ kind: 'str', value: t.value }, i + 1];
    if (t.kind === 'name' && t.name === 'function') return func(toks, i + 1);
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

// Whether a token closes the statements: the end of the program, or a `}`.
const atEnd = (t: Token, closer: '}' | null): boolean =>
    closer === null ? t.kind === 'eof' : isPunct(t, '}');

// Statements up to the closer, which is not consumed: the end of the program
// when the closer is null, else a `}`. Returns them with the closer's index.
const stmts = (acc: Stmt[], toks: readonly Token[], i: number, closer: '}' | null): [Stmt[], number] => {
    if (atEnd(toks[i]!, closer)) return [acc, i];
    const [s, j] = stmt(toks, i);
    const all = [...acc, s];
    const t = toks[j]!;
    if (atEnd(t, closer)) return [all, j];
    const endName = closer === null ? 'the end of the program' : "'}'";
    if (!isPunct(t, ';')) throw fail(`expected ';' or ${endName}, found ${describe(t)}`, t);
    return stmts(all, toks, j + 1, closer);
};

export const parse = (src: string): Stmt[] => stmts([], lex(src), 0, null)[0];
