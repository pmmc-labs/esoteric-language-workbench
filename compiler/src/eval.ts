// Statements to a value, and values to text. Integers are unbounded (BigInt
// on the host). Bindings are an association list: a let puts a new head on
// it, so a later binding hides an earlier one. A function keeps the list as
// it was where the function was written. Lists are never changed, so keeping
// one is only keeping a pointer, and a later let is invisible to it. The
// built-ins are the first bindings of the list every program starts with.
//
// Arrays and hashes are the one kind of value that changes. A method on one
// changes it, and a let copies the reference, so every name for it sees the
// change. Their methods are host builtins, but they live in the method tables
// of the SMOL classes Array and Hash, which the prelude makes (D31).
//
// An opaque instance is an id, a class and attrs (D10). Its methods are not
// on the host: a method call on one walks its class's chain, below. So does a
// method call on a primitive whose class is registered (D29, D31).
import type { Expr, Stmt } from './ast.ts';
import { Failure } from './errors.ts';

type Env = { readonly name: string; readonly value: Value; readonly next: Env } | null;

export type Value =
    | { kind: 'int'; value: bigint }
    | { kind: 'str'; value: string }
    | { kind: 'nil' }
    | { kind: 'bool'; value: boolean }
    | { kind: 'fn'; params: readonly string[]; body: readonly Stmt[]; env: Env }
    | { kind: 'builtin'; arity: number | null; call: (args: Value[]) => Value }
    | { kind: 'arr'; items: Value[] }
    | { kind: 'hash'; entries: Map<string, Value> }
    | { kind: 'obj'; id: bigint; cls: Value; attrs: HashV };

type ArrV = Extract<Value, { kind: 'arr' }>;
type HashV = Extract<Value, { kind: 'hash' }>;
type ObjV = Extract<Value, { kind: 'obj' }>;

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
// can't be a method. A builtin whose arity is null takes any number.
const apply = (f: Value, args: Value[], hidden: number = 0): Value => {
    if (f.kind !== 'fn' && f.kind !== 'builtin') return fault(`not a function: ${show(f)}`);
    if (f.kind === 'builtin') {
        if (f.arity === null) return f.call(args);
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

// Equality for includes (D30): scalars are equal by value, and anything else
// only by identity, so an object is in a list only as itself.
const sameValue = (a: Value, b: Value): boolean => {
    if (a.kind === 'int' && b.kind === 'int') return a.value === b.value;
    if (a.kind === 'str' && b.kind === 'str') return a.value === b.value;
    if (a.kind === 'bool' && b.kind === 'bool') return a.value === b.value;
    return a === b || (a.kind === 'nil' && b.kind === 'nil');
};

// The methods of Array and Hash, as builtins that host_method hands to the
// prelude, which puts them in the classes' "%methods" (D33). A builtin's
// arity counts its receiver, which comes first, and is null for a method that
// takes any number of arguments. Each checks that its receiver is the kind
// the class expects, since a method table can be reached from anything whose
// class inherits from it. push and set change their receiver in place, and
// return it, so calls chain.
const receiver = <K extends Value['kind']>(kind: K, what: string, name: string, args: Value[]): Extract<Value, { kind: K }> => {
    const self = args[0];
    if (self === undefined) return fault('wrong number of arguments: want at least 1, got 0');
    if (self.kind !== kind) return fault(`${name} needs ${what} as its receiver: ${show(self)}`);
    return self as Extract<Value, { kind: K }>;
};

const arrayMethod = (name: string, arity: number | null, call: (self: ArrV, args: Value[]) => Value): [string, Value] =>
    [name, { kind: 'builtin', arity, call: args => call(receiver('arr', 'an array', name, args), args.slice(1)) }];

const hashMethod = (name: string, arity: number | null, call: (self: HashV, args: Value[]) => Value): [string, Value] =>
    [name, { kind: 'builtin', arity, call: args => call(receiver('hash', 'a hash', name, args), args.slice(1)) }];

// new is a method of the class, and its receiver is the class, which it
// ignores. Array.new(a, b) is an array of its arguments; Hash.new takes key
// and value pairs.
const classMethod = (call: (args: Value[]) => Value): [string, Value] =>
    ['new', { kind: 'builtin', arity: null, call: args => call(args.slice(1)) }];

const HOST_METHODS = new Map<string, Map<string, Value>>([
    ['Array', new Map([
        classMethod(args => ({ kind: 'arr', items: [...args] })),
        arrayMethod('push', null, (self, args) => { self.items.push(...args); return self; }),
        arrayMethod('get', 2, (self, args) => {
            const n = indexOf(args[0]!);
            return n >= 0 && n < self.items.length ? self.items[n]! : NIL;
        }),
        arrayMethod('set', 3, (self, args) => {
            const n = indexOf(args[0]!);
            if (n < 0 || n >= self.items.length)
                return fault(`index ${n} is out of range for an array of ${self.items.length}`);
            self.items[n] = args[1]!;
            return self;
        }),
        arrayMethod('size', 1, self => ({ kind: 'int', value: BigInt(self.items.length) })),
        arrayMethod('includes', 2, (self, args) => ({ kind: 'bool', value: self.items.some(x => sameValue(x, args[0]!)) })),
    ])],
    ['Hash', new Map([
        classMethod(args => hashOf(args, 'Hash.new')),
        hashMethod('get', 2, (self, args) => self.entries.get(keyOf(args[0]!)) ?? NIL),
        hashMethod('set', 3, (self, args) => { self.entries.set(keyOf(args[0]!), args[1]!); return self; }),
        hashMethod('keys', 1, self => ({ kind: 'arr', items: [...self.entries.keys()].map((k): Value => ({ kind: 'str', value: k })) })),
        hashMethod('size', 1, self => ({ kind: 'int', value: BigInt(self.entries.size) })),
    ])],
]);

// host_method(class, method): the builtin for a method of one of the host's
// classes, from the table the starting environment builds (D33, D35).
const hostMethod = (table: ReadonlyMap<string, Map<string, Value>>, args: Value[]): Value => {
    const [cls, name] = [args[0]!, args[1]!];
    const text = (v: Value): string => v.kind === 'str' ? v.value : show(v);
    const found = cls.kind === 'str' && name.kind === 'str' ? table.get(cls.value)?.get(name.value) : undefined;
    return found ?? fault(`no host method ${text(name)} for ${text(cls)}`);
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

// A method call on a value whose class is cls: the search starts at cls, and
// the method found is called with the value first, as self (D15).
const dispatch = (cls: Value, self: Value, name: string, args: Value[]): Value => {
    const m = findMethod(cls, name);
    if (m === undefined) return fault(`no method found for ${name} on ${show(self)}`);
    return apply(m, [self, ...args], 1);
};

// The hidden binding that holds the classes of true, false, nil, arrays and
// hashes (D29, D31). A space in its name means no program can write it.
const PRIMITIVES = ' primitive classes';

// The key a value's class is registered under: the constant itself for true,
// false and nil, and the kind for an array or a hash.
const primitiveKey = (v: Value): string | undefined =>
    v.kind === 'nil' ? 'nil' : v.kind === 'bool' ? (v.value ? 'true' : 'false')
    : v.kind === 'arr' || v.kind === 'hash' ? v.kind : undefined;

const registered = (table: HashV, v: Value): Value | undefined => {
    const key = primitiveKey(v);
    return key === undefined ? undefined : table.entries.get(key);
};

const primitiveClass = (env: Env, v: Value): Value | undefined => {
    const table = lookup(env, PRIMITIVES);
    return table !== undefined && table.kind === 'hash' ? registered(table, v) : undefined;
};

// A value with no class (an integer, a string, a function, or a primitive
// before the prelude registers its class) has no methods.
const noMethod = (self: Value, name: string): never => fault(`no method found for ${name} on ${show(self)}`);

// A method call on an instance: the search starts at the instance's class,
// and the method found is called with the instance first, as self (D15).
const send = (self: ObjV, name: string, args: Value[]): Value => dispatch(self.cls, self, name, args);

const attrsOf = (v: Value): HashV => {
    if (v.kind !== 'hash') return fault(`attrs must be a Hash: ${show(v)}`);
    return v;
};

const objOf = (v: Value): ObjV => {
    if (v.kind !== 'obj') return fault(`not an opaque instance: ${show(v)}`);
    return v;
};

const builtin = (arity: number, call: (args: Value[]) => Value): Value => ({ kind: 'builtin', arity, call });

// isa(target): the value's class, or a class above it on the superclass chain,
// is target (D18). A value with no class is an instance of nothing. The chain
// is walked the way the lookup walks it, so a loop is the same fault (D23).
const isaClass = (cls: Value | undefined, target: Value): boolean => {
    const seen: Value[] = [];
    let c = cls;
    while (c !== undefined && c.kind === 'obj') {
        if (sameValue(c, target)) return true;
        if (seen.includes(c)) return fault(`superclass chain loops back to ${show(c)}`);
        seen.push(c);
        c = c.attrs.entries.get('$superclass');
    }
    return false;
};

// can(name): a method of that name is found for the value, by the same lookup
// dispatch uses, so the two can't disagree (D18). A name that isn't a string
// is a fault.
const canName = (cls: Value | undefined, name: Value): boolean => {
    if (name.kind !== 'str') return fault(`can needs a method name as a string: ${show(name)}`);
    return cls !== undefined && findMethod(cls, name.value) !== undefined;
};

// The names every program starts with. The two built-ins that make an
// instance share one id counter, and it belongs to the list made here, so
// each run of a program counts from 1.
const root = (): Env => {
    let ids = 0n;  // the last id given; the next is one more
    const create = (cls: Value, attrs: HashV): Value => ({ kind: 'obj', id: ++ids, cls, attrs });
    // create_class: the defaults, then the given attrs over them, in a Hash
    // of the class's own. Its class is nil. The prelude's create_class wraps
    // this to give Class (D26).
    const createClass = (given: HashV): Value => create(NIL, { kind: 'hash', entries: new Map<string, Value>([
        ['$name', { kind: 'str', value: '' }],
        ['$superclass', NIL],
        ['%methods', { kind: 'hash', entries: new Map() }],
        ...given.entries,
    ]) });
    const primitives: HashV = { kind: 'hash', entries: new Map<string, Value>() };
    // The class of a value: an instance's, or the one registered for a primitive.
    const classOf = (v: Value): Value | undefined => v.kind === 'obj' ? v.cls : registered(primitives, v);
    // Object's built-in methods (D18), which every value with a class answers.
    const objectMethods = new Map<string, Value>([
        ['isa', builtin(2, args => ({ kind: 'bool', value: isaClass(classOf(args[0]!), args[1]!) }))],
        ['can', builtin(2, args => ({ kind: 'bool', value: canName(classOf(args[0]!), args[1]!) }))],
    ]);
    const hostMethods = new Map<string, Map<string, Value>>([...HOST_METHODS, ['Object', objectMethods]]);
    const bindings: [string, Value][] = [
        ['catch', CATCH],
        ['create_opaque_instance', builtin(2, args => create(args[0]!, attrsOf(args[1]!)))],
        ['opaque_instance_id', builtin(1, args => ({ kind: 'int', value: objOf(args[0]!).id }))],
        // A primitive with a registered class answers that class (D31), so
        // [1].class() is Array.
        ['opaque_instance_class', builtin(1, args => {
            const v = args[0]!;
            return v.kind === 'obj' ? v.cls : registered(primitives, v) ?? fault(`not an opaque instance: ${show(v)}`);
        })],
        ['opaque_instance_attrs', builtin(1, args => objOf(args[0]!).attrs)],
        ['create_class', builtin(1, args => createClass(attrsOf(args[0]!)))],
        // D19: the one place an instance's class is set after it is made, so a
        // class can be made an instance of itself once it exists.
        ['opaque_instance_set_class', builtin(2, args => {
            const o = objOf(args[0]!);
            o.cls = args[1]!;
            return o;
        })],
        [PRIMITIVES, primitives],
        // fault(message, value): raises a fault, whose message is the string and
        // then the value shown, separated by a space (D30). The prelude uses it
        // where a loop in the superclass chain has to stop the walk.
        ['fault', builtin(2, args => {
            const m = args[0]!;
            if (m.kind !== 'str') return fault(`fault needs a string message: ${show(m)}`);
            return fault(`${m.value} ${show(args[1]!)}`);
        })],
        // D29, D31: makes an instance the class of true, false or nil, or of
        // every array or every hash, which then answer its methods. The class
        // is returned.
        ['set_primitive_class', builtin(2, args => {
            const cls = args[1]!;
            if (cls.kind !== 'obj') return fault(`not an opaque instance: ${show(cls)}`);
            const key = primitiveKey(args[0]!);
            if (key === undefined) return fault(`only true, false, nil, arrays and hashes take a class: ${show(args[0]!)}`);
            primitives.entries.set(key, cls);
            return cls;
        })],
        // D33: the prelude takes the methods of Array and Hash from here.
        ['host_method', builtin(2, args => hostMethod(hostMethods, args))],
        // D32: makes the next id at least n, and never lower, so the
        // bootstrap can keep the ids below n for itself.
        ['reserve_ids', builtin(1, args => {
            const n = args[0]!;
            if (n.kind !== 'int') return fault(`reserve_ids needs an integer: ${show(n)}`);
            if (n.value - 1n > ids) ids = n.value - 1n;
            return NIL;
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
            if (recv.kind === 'obj') return send(recv, e.name, args);
            const cls = primitiveClass(env, recv);
            return cls === undefined ? noMethod(recv, e.name) : dispatch(cls, recv, e.name, args);
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
