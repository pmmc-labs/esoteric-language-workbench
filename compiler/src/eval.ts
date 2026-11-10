// Statements to a value, and values to text. Integers are unbounded (BigInt
// on the host). Bindings are an association list: a let puts a new head on
// it, so a later binding hides an earlier one. A function keeps the list as
// it was where the function was written. Lists are never changed, so keeping
// one is only keeping a pointer, and a later let is invisible to it. The
// built-ins are the first bindings of the list every program starts with.
import type { Expr, Stmt } from './ast.ts';
import { Failure } from './errors.ts';

type Env = { readonly name: string; readonly value: Value; readonly next: Env } | null;

export type Value =
    | { kind: 'int'; value: bigint }
    | { kind: 'str'; value: string }
    | { kind: 'nil' }
    | { kind: 'bool'; value: boolean }
    | { kind: 'fn'; params: readonly string[]; body: readonly Stmt[]; env: Env }
    | { kind: 'builtin'; arity: number; call: (args: Value[]) => Value };

const NIL: Value = { kind: 'nil' };

const fault = (message: string): never => {
    throw new Failure(message);
};

const lookup = (env: Env, name: string): Value | undefined =>
    env === null ? undefined : env.name === name ? env.value : lookup(env.next, name);

export const show = (v: Value): string =>
    v.kind === 'int' ? v.value.toString()
    : v.kind === 'str' ? `"${v.value}"`
    : v.kind === 'nil' ? 'nil'
    : v.kind === 'fn' || v.kind === 'builtin' ? '<function>'
    : String(v.value);

const constant = (name: 'nil' | 'true' | 'false'): Value =>
    name === 'nil' ? NIL : { kind: 'bool', value: name === 'true' };

const values = (es: readonly Expr[], env: Env): Value[] => es.map(e => evalExpr(e, env));

// A call, with the callee and the arguments already values. The arguments
// bind to the parameters in order, on top of the list the function kept.
const apply = (f: Value, args: Value[]): Value => {
    if (f.kind !== 'fn' && f.kind !== 'builtin') return fault(`not a function: ${show(f)}`);
    const want = f.kind === 'fn' ? f.params.length : f.arity;
    if (args.length !== want) return fault(`wrong number of arguments: want ${want}, got ${args.length}`);
    if (f.kind === 'builtin') return f.call(args);
    const env = f.params.reduce<Env>((acc, name, i) => ({ name, value: args[i]!, next: acc }), f.env);
    return run(f.body, env) ?? NIL;
};

// catch(f): calls f with no arguments. A fault raised by that call comes back
// as its message, a string; otherwise the result is nil. A fault in the
// argument itself, such as a value that isn't a function, is not caught: it
// happens before anything could fail inside f.
const catchFault = (args: Value[]): Value => {
    const f = args[0]!;
    if (f.kind !== 'fn' && f.kind !== 'builtin') return fault(`not a function: ${show(f)}`);
    try {
        apply(f, []);
        return NIL;
    } catch (e) {
        if (e instanceof Failure) return { kind: 'str', value: e.message };
        throw e;
    }
};

const CATCH: Value = { kind: 'builtin', arity: 1, call: catchFault };

const ROOT: Env = { name: 'catch', value: CATCH, next: null };

const evalExpr = (e: Expr, env: Env): Value => {
    switch (e.kind) {
        case 'int': return { kind: 'int', value: e.value };
        case 'str': return { kind: 'str', value: e.value };
        case 'const': return constant(e.name);
        case 'name': return lookup(env, e.name) ?? fault(`unbound name: ${e.name}`);
        case 'function': return { kind: 'fn', params: e.params, body: e.body, env };
        case 'call': {
            const fn = evalExpr(e.fn, env);
            return apply(fn, values(e.args, env));
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

export const evaluate = (stmts: readonly Stmt[]): Value | undefined => run(stmts, ROOT);
