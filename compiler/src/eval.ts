// Statements to a value, and values to text. Integers are unbounded (BigInt
// on the host). Bindings are an association list: a let puts a new head on
// it, so a later binding of the same name hides an earlier one, and the rest
// of the program sees the newest.
import type { Expr, Stmt } from './ast.ts';
import { Failure } from './errors.ts';

export type Value =
    | { kind: 'int'; value: bigint }
    | { kind: 'str'; value: string }
    | { kind: 'nil' }
    | { kind: 'bool'; value: boolean };

type Env = { readonly name: string; readonly value: Value; readonly next: Env } | null;

const fault = (message: string): never => {
    throw new Failure(message);
};

const lookup = (env: Env, name: string): Value | undefined =>
    env === null ? undefined : env.name === name ? env.value : lookup(env.next, name);

export const show = (v: Value): string =>
    v.kind === 'int' ? v.value.toString()
    : v.kind === 'str' ? `"${v.value}"`
    : v.kind === 'nil' ? 'nil'
    : String(v.value);

const constant = (name: 'nil' | 'true' | 'false'): Value =>
    name === 'nil' ? { kind: 'nil' } : { kind: 'bool', value: name === 'true' };

const values = (es: readonly Expr[], env: Env): Value[] => es.map(e => evalExpr(e, env));

const evalExpr = (e: Expr, env: Env): Value => {
    switch (e.kind) {
        case 'int': return { kind: 'int', value: e.value };
        case 'str': return { kind: 'str', value: e.value };
        case 'const': return constant(e.name);
        case 'name': return lookup(env, e.name) ?? fault(`unbound name: ${e.name}`);
        case 'call': {
            // The arguments are evaluated before the fault, as a call would
            // evaluate them. Nothing is callable yet: closures are step 1.
            const fn = evalExpr(e.fn, env);
            values(e.args, env);
            return fault(`not a function: ${show(fn)}`);
        }
        case 'method': {
            // No value has methods yet: dispatch is step 4.
            const recv = evalExpr(e.recv, env);
            values(e.args, env);
            return fault(`no method found for ${e.name} on ${show(recv)}`);
        }
    }
};

// The value of the last statement, if it is an expression. A let has none.
const run = (stmts: readonly Stmt[], env: Env): Value | undefined => {
    if (stmts.length === 0) return undefined;
    const [s, ...rest] = stmts;
    if (s.kind === 'let') return run(rest, { name: s.name, value: evalExpr(s.expr, env), next: env });
    const v = evalExpr(s.expr, env);
    return rest.length === 0 ? v : run(rest, env);
};

export const evaluate = (stmts: readonly Stmt[]): Value | undefined => run(stmts, null);
