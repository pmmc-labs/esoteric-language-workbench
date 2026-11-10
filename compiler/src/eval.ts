// Statements to a value, and values to text. Integers are unbounded (BigInt
// on the host). Bindings are an association list: a let puts a new head on
// it, so a later binding hides an earlier one. A function keeps the list as
// it was where the function was written. Lists are never changed, so keeping
// one is only keeping a pointer, and a later let is invisible to it. The
// built-ins are the first bindings of the list every program starts with.
//
// Arrays and hashes are the one kind of value that changes. A method on one
// changes it, and a let copies the reference, so every name for it sees the
// change. Each kind's methods are a table on the host, which a method call
// consults; step 5 moves them into class method tables, when Array and Hash
// become SMOL classes.
//
// An opaque instance is an id, a class and attrs (D10). Its methods are not
// on the host: a method call on one walks its class's chain, below.
import type { Expr, Stmt } from './ast.ts';
import { Failure } from './errors.ts';

type Env = { readonly name: string; readonly value: Value; readonly next: Env } | null;

export type Value =
    | { kind: 'int'; value: bigint }
    | { kind: 'str'; value: string }
    | { kind: 'nil' }
    | { kind: 'bool'; value: boolean }
    | { kind: 'fn'; params: readonly string[]; body: readonly Stmt[]; env: Env }
    | { kind: 'builtin'; arity: number; call: (args: Value[]) => Value }
    | { kind: 'arr'; items: Value[] }
    | { kind: 'hash'; entries: Map<string, Value> }
    | { kind: 'class'; name: string; make: (args: Value[]) => Value }
    | { kind: 'obj'; id: bigint; cls: Value; attrs: HashV };

type ArrV = Extract<Value, { kind: 'arr' }>;
type HashV = Extract<Value, { kind: 'hash' }>;
type ClassV = Extract<Value, { kind: 'class' }>;
type ObjV = Extract<Value, { kind: 'obj' }>;

// A method: how many arguments it takes (null for any number), and what it
// does with its receiver.
type Method<S> = { arity: number | null; call: (self: S, args: Value[]) => Value };

const NIL: Value = { kind: 'nil' };

const fault = (message: string): never => {
    throw new Failure(message);
};

const NO_SELF = 'a method needs a first parameter for self';

const lookup = (env: Env, name: string): Value | undefined =>
    env === null ? undefined : env.name === name ? env.value : lookup(env.next, name);

// An array or hash can hold itself, so the ones being printed are kept on a
// list, and a cycle prints as [...] or {...}.
const render = (v: Value, open: Value[]): string => {
    switch (v.kind) {
        case 'int': return v.value.toString();
        case 'str': return `"${v.value}"`;
        case 'nil': return 'nil';
        case 'bool': return String(v.value);
        case 'fn': case 'builtin': return '<function>';
        case 'class': return `<class ${v.name}>`;
        case 'obj': return `<object ${v.id}>`;
        case 'arr': return open.includes(v) ? '[...]'
            : `[${v.items.map(x => render(x, [...open, v])).join(', ')}]`;
        case 'hash': return open.includes(v) ? '{...}'
            : `{${[...v.entries].map(([k, x]) => `"${k}": ${render(x, [...open, v])}`).join(', ')}}`;
    }
};

export const show = (v: Value): string => render(v, []);

const constant = (name: 'nil' | 'true' | 'false'): Value =>
    name === 'nil' ? NIL : { kind: 'bool', value: name === 'true' };

const values = (es: readonly Expr[], env: Env): Value[] => es.map(e => evalExpr(e, env));

// A hash key is a string, so a key that isn't one is a fault.
const keyOf = (v: Value): string => {
    if (v.kind !== 'str') return fault(`a hash key must be a string: ${show(v)}`);
    return v.value;
};

// Key and value pairs, as a Hash. `who` names the source, for the message.
const hashOf = (args: Value[], who: string): Value => {
    if (args.length % 2 !== 0) return fault(`${who} needs key and value pairs: an even number of arguments`);
    const entries = new Map<string, Value>();
    for (let i = 0; i < args.length; i += 2) entries.set(keyOf(args[i]!), args[i + 1]!);
    return { kind: 'hash', entries };
};

// A call, with the callee and the arguments already values. The arguments
// bind to the parameters in order, on top of the list the function kept. A
// trailing %name parameter takes the rest of them as a Hash.
//
// A method call passes its receiver as the first argument (D15), and says so
// with `hidden` = 1. The caller didn't write that argument, so an arity fault
// leaves it out of both counts, and a function with no parameter to take it
// can't be a method.
const apply = (f: Value, args: Value[], hidden: number = 0): Value => {
    if (f.kind !== 'fn' && f.kind !== 'builtin') return fault(`not a function: ${show(f)}`);
    if (f.kind === 'builtin') {
        if (f.arity < hidden) return fault(NO_SELF);
        if (args.length !== f.arity)
            return fault(`wrong number of arguments: want ${f.arity - hidden}, got ${args.length - hidden}`);
        return f.call(args);
    }
    const last = f.params[f.params.length - 1];
    const rest = last !== undefined && last.startsWith('%') ? last : null;
    const fixed = rest === null ? f.params : f.params.slice(0, -1);
    if (fixed.length < hidden) return fault(NO_SELF);
    const wrong = rest === null ? args.length !== fixed.length : args.length < fixed.length;
    if (wrong) return fault(`wrong number of arguments: want ${rest === null ? '' : 'at least '}${fixed.length - hidden}, got ${args.length - hidden}`);
    const bound = fixed.reduce<Env>((acc, name, i) => ({ name, value: args[i]!, next: acc }), f.env);
    const env = rest === null ? bound : { name: rest, value: hashOf(args.slice(fixed.length), rest), next: bound };
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

// An index is an integer. Anything else is a fault.
const indexOf = (v: Value): number => {
    if (v.kind !== 'int') return fault(`index must be an integer: ${show(v)}`);
    return Number(v.value);
};

// The methods of each kind of value. Array and Hash are the only ones with
// any, and they change their receiver in place: push, set. Each returns the
// receiver, so calls chain.
const ARRAY = new Map<string, Method<ArrV>>([
    ['push', { arity: null, call: (self, args) => { self.items.push(...args); return self; } }],
    ['get', { arity: 1, call: (self, args) => {
        const n = indexOf(args[0]!);
        return n >= 0 && n < self.items.length ? self.items[n]! : NIL;
    } }],
    ['set', { arity: 2, call: (self, args) => {
        const n = indexOf(args[0]!);
        if (n < 0 || n >= self.items.length)
            return fault(`index ${n} is out of range for an array of ${self.items.length}`);
        self.items[n] = args[1]!;
        return self;
    } }],
    ['size', { arity: 0, call: self => ({ kind: 'int', value: BigInt(self.items.length) }) }],
]);

const HASH = new Map<string, Method<HashV>>([
    ['get', { arity: 1, call: (self, args) => self.entries.get(keyOf(args[0]!)) ?? NIL }],
    ['set', { arity: 2, call: (self, args) => { self.entries.set(keyOf(args[0]!), args[1]!); return self; } }],
    ['keys', { arity: 0, call: self => ({ kind: 'arr', items: [...self.entries.keys()].map((k): Value => ({ kind: 'str', value: k })) }) }],
    ['size', { arity: 0, call: self => ({ kind: 'int', value: BigInt(self.entries.size) }) }],
]);

// A class value's one method is new, which makes an instance of the class.
const CLASS = new Map<string, Method<ClassV>>([
    ['new', { arity: null, call: (self, args) => self.make(args) }],
]);

const NONE = new Map<string, Method<Value>>();

// Array and Hash, as values bound before the program starts. Array.new(a, b)
// is an array of its arguments; Hash.new takes key and value pairs.
const ARRAY_CLASS: Value = { kind: 'class', name: 'Array', make: args => ({ kind: 'arr', items: [...args] }) };
const HASH_CLASS: Value = { kind: 'class', name: 'Hash', make: args => hashOf(args, 'Hash.new') };

// A method call: the receiver's kind picks the table, and the method in it
// checks its arity and runs.
const invoke = <S extends Value>(table: ReadonlyMap<string, Method<S>>, self: S, name: string, args: Value[]): Value => {
    const m = table.get(name);
    if (m === undefined) return fault(`no method found for ${name} on ${show(self)}`);
    if (m.arity !== null && args.length !== m.arity)
        return fault(`wrong number of arguments: want ${m.arity}, got ${args.length}`);
    return m.call(self, args);
};

// The core rule (DESIGN.md). The method is looked for in the class's
// "%methods", then in its "$superclass", along the one chain (D16), until
// the chain ends at nil. A class that isn't an instance, or has no Hash under
// "%methods", has no methods; one that isn't an instance has no superclass
// either, so the chain ends there.
// A chain that loops back to a class already searched is a fault, not a
// crash: the walk would otherwise never end.
const findMethod = (cls: Value, name: string, seen: Value[] = []): Value | undefined => {
    if (cls.kind !== 'obj') return undefined;
    if (seen.includes(cls)) return fault(`superclass chain loops back to ${show(cls)}`);
    const table = cls.attrs.entries.get('%methods');
    const found = table !== undefined && table.kind === 'hash' ? table.entries.get(name) : undefined;
    return found ?? findMethod(cls.attrs.entries.get('$superclass') ?? NIL, name, [...seen, cls]);
};

// A method call on an instance: the search starts at the instance's class,
// and the method found is called with the instance first, as self (D15).
const send = (self: ObjV, name: string, args: Value[]): Value => {
    const m = findMethod(self.cls, name);
    if (m === undefined) return fault(`no method found for ${name} on ${show(self)}`);
    return apply(m, [self, ...args], 1);
};

const attrsOf = (v: Value): HashV => {
    if (v.kind !== 'hash') return fault(`attrs must be a Hash: ${show(v)}`);
    return v;
};

const objOf = (v: Value): ObjV => {
    if (v.kind !== 'obj') return fault(`not an opaque instance: ${show(v)}`);
    return v;
};

const builtin = (arity: number, call: (args: Value[]) => Value): Value => ({ kind: 'builtin', arity, call });

// The names every program starts with. The two built-ins that make an
// instance share one id counter, and it belongs to the list made here, so
// each run of a program counts from 1.
const root = (): Env => {
    let ids = 0n;
    const create = (cls: Value, attrs: HashV): Value => ({ kind: 'obj', id: ++ids, cls, attrs });
    // create_class: the defaults, then the given attrs over them, in a Hash
    // of the class's own. Its class is nil: a class made this way isn't an
    // instance of Class. Class.new makes one that is (LANGUAGE.md, Bootstrap).
    const createClass = (given: HashV): Value => create(NIL, { kind: 'hash', entries: new Map<string, Value>([
        ['$name', { kind: 'str', value: '' }],
        ['$superclass', NIL],
        ['%methods', { kind: 'hash', entries: new Map() }],
        ...given.entries,
    ]) });
    const bindings: [string, Value][] = [
        ['catch', CATCH],
        ['Array', ARRAY_CLASS],
        ['Hash', HASH_CLASS],
        ['create_opaque_instance', builtin(2, args => create(args[0]!, attrsOf(args[1]!)))],
        ['opaque_instance_id', builtin(1, args => ({ kind: 'int', value: objOf(args[0]!).id }))],
        ['opaque_instance_class', builtin(1, args => objOf(args[0]!).cls)],
        ['opaque_instance_attrs', builtin(1, args => objOf(args[0]!).attrs)],
        ['create_class', builtin(1, args => createClass(attrsOf(args[0]!)))],
        // D19: the one place an instance's class is set after it is made, so a
        // class can be made an instance of itself once it exists.
        ['opaque_instance_set_class', builtin(2, args => {
            const o = objOf(args[0]!);
            o.cls = args[1]!;
            return o;
        })],
    ];
    return bindings.reduceRight<Env>((next, [name, value]) => ({ name, value, next }), null);
};

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
            const recv = evalExpr(e.recv, env);
            const args = values(e.args, env);
            switch (recv.kind) {
                case 'arr': return invoke(ARRAY, recv, e.name, args);
                case 'hash': return invoke(HASH, recv, e.name, args);
                case 'class': return invoke(CLASS, recv, e.name, args);
                case 'obj': return send(recv, e.name, args);
                default: return invoke(NONE, recv, e.name, args);
            }
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

export const evaluate = (stmts: readonly Stmt[]): Value | undefined => run(stmts, root());
