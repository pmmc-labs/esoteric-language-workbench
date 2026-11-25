// Names to their declarations (D29): every `$x` is tied to the `my` it
// means before any code is made, and the three ways that can fail are
// refused here, as perl refuses or warns of each (D56):
//   a variable with no `my` in sight (perl: `Global symbol requires
//   explicit package name`);
//   a second `my` of a name in one scope (perl warns that it masks the
//   first);
//   `my $x = $x` with no outer `$x`, which is the first again: a `my` is
//   seen from the statement after its own (T58).
// A scope is a block, and an `if` with its tests: a `my` in a test is
// seen in the blocks of that `if`, in its later tests, and no further. A
// loop is one too, for its test or its first part.
//
// And each `last` and `next` to its loop (D59, D61, D62), refused when
// there is none: perl looks for the loop as the program runs, and dies
// there.
//
// And each call to its sub (D72), wherever in the file the sub is; one
// the program doesn't have is refused, where perl dies when it gets
// there. A sub is a function of its own: its parameters and its
// variables are its frame's, it may name the file's variables that were
// declared before it, and no `last` or `next` in it reaches a loop
// outside it (T60).
import { refuse } from './errors.ts';
import type { Expr, Invoke, Jump, Loop, My, Pos, Program, Stmt, Sub, Var } from './ast.ts';

// A declaration is a number, in the order the `my`s are met; `of` says
// which one each variable in the tree means, and `names` what each is
// called. A loop is a number too: `loops` gives each its own, and `jumps`
// says which loop each `last` and `next` is for.
//
// `slots` says where each declaration's value is kept as the program runs
// (D66): the slot of its function's frame that is its depth among the
// variables in scope, so that the variables of a block that has ended
// leave their slots to the next one.
//
// A function is the file, 0, or a sub, numbered from 1 in the order they
// are written: `owner` says whose frame a declaration is in, `frames` how
// many slots each function's variables take at most, `subs` the subs, and
// `calls` which one each call is of. **A file variable**, a `my` at the
// top level, has a slot that nothing else is ever given, the first `file`
// slots of the file's frame: a sub may be called before the `my` runs, and
// what it put there is still there after (T134).
export type Resolution = {
    of: ReadonlyMap<Var | My, number>;
    names: readonly string[];
    slots: readonly number[];
    owner: readonly number[];
    frames: readonly number[];
    file: number;
    subs: readonly Sub[];
    calls: ReadonlyMap<Invoke, number>;
    loops: ReadonlyMap<Loop, number>;
    jumps: ReadonlyMap<Jump, number>;
};

// What is round a statement that perl counts as a loop: a loop, or a
// bare block, which runs once (T32).
type Round = { loop: Loop } | { bare: Pos };

export const resolve = (program: Program): Resolution => {
    const of = new Map<Var | My, number>();
    const names: string[] = [];
    const slots: number[] = [];
    const owner: number[] = [];
    const frames: number[] = [0];
    // The function being read, and of its variables that share slots, how
    // many are in scope and how many there have been at once.
    let fn = 0;
    let inScope = 0;
    let variables = 0;
    let file = 0;
    const fileSlots = new Set<number>();
    const fileScope = new Map<string, number>();
    let scopes: Map<string, number>[] = [fileScope];
    const close = (): void => {
        inScope -= scopes.pop()!.size;
    };
    const loops = new Map<Loop, number>();
    const jumps = new Map<Jump, number>();
    let round: Round[] = [];

    // The subs, before anything is read: a call may come before its sub.
    const subs = program.body.filter(s => s.kind === 'sub');
    const called = new Map<string, number>();
    for (const [n, s] of subs.entries()) {
        if (called.has(s.name)) refuse(`a second sub called ${s.name}: perl warns that it is redefined, and takes this one`, s.named);
        called.set(s.name, n + 1);
    }
    const calls = new Map<Invoke, number>();

    // A declaration comes into scope: a file variable in a slot of its
    // own, any other at its depth among those in scope.
    const declare = (d: My): void => {
        const id = of.get(d)!;
        scopes.at(-1)!.set(d.name, id);
        owner[id] = fn;
        if (scopes.at(-1) === fileScope) {
            fileSlots.add(id);
            slots[id] = file;
            file += 1;
            return;
        }
        slots[id] = inScope;
        inScope += 1;
        variables = Math.max(variables, inScope);
    };

    // The variables an expression uses, each looked up as it is met; and
    // the ones it declares, which are returned and not yet seen.
    const walk = (e: Expr, declared: My[]): void => {
        switch (e.kind) {
        case 'var': {
            const found = [...scopes].reverse().find(s => s.has(e.name));
            if (found === undefined) return refuse(`$${e.name} is not declared: my $${e.name}`, e.pos);
            of.set(e, found.get(e.name)!);
            return;
        }
        case 'my':
            of.set(e, names.length);
            names.push(e.name);
            declared.push(e);
            return;
        case 'assign':
            // The right side first: it is worked out first, and in `my $x
            // = $x` its `$x` is the outer one.
            walk(e.value, declared);
            return walk(e.target, declared);
        case 'step': return walk(e.target, declared);
        case 'unary': return walk(e.operand, declared);
        case 'binary':
            walk(e.left, declared);
            return walk(e.right, declared);
        case 'ternary':
            walk(e.test, declared);
            walk(e.then, declared);
            return walk(e.else, declared);
        case 'apply': return e.args.forEach(a => walk(a, declared));
        case 'invoke': {
            e.args.forEach(a => walk(a, declared));
            const found = called.get(e.name);
            if (found === undefined) return refuse(`the program has no sub called ${e.name}`, e.pos);
            calls.set(e, found);
            return;
        }
        default: return;
        }
    };

    // An expression of a statement, or a test, or the expressions of one
    // part of a `for`: what it declares is seen once the whole of it has
    // been read.
    const whole = (...es: Expr[]): void => {
        const declared: My[] = [];
        es.forEach(e => walk(e, declared));
        // In the order they are written: the second of two is the one at
        // fault.
        declared.sort((a, b) => a.pos.line - b.pos.line || a.pos.col - b.pos.col);
        for (const d of declared) {
            const scope = scopes.at(-1)!;
            if (scope.has(d.name)) refuse(`my $${d.name} again in one scope: perl warns that it masks the first`, d.pos);
            declare(d);
        }
    };

    const inner = (body: readonly Stmt[]): void => {
        scopes.push(new Map());
        body.forEach(statement);
        close();
    };

    // A sub: a function of its own, which sees the file's variables as
    // far as they have been declared. A default is read before its own
    // parameter exists, so `sub f($x = $x)` means the file's `$x` (T138);
    // the body is in the parameters' scope, so a `my` of a parameter's
    // name there is a second one (T141).
    const function_ = (s: Sub): void => {
        const outer = { fn, inScope, variables, scopes, round };
        fn = called.get(s.name)!;
        inScope = 0;
        variables = 0;
        scopes = [fileScope, new Map()];
        round = [];
        for (const p of s.params) {
            if (p.default) whole(p.default);
            if (p.my === undefined) continue;
            if (scopes.at(-1)!.has(p.my.name)) refuse(`two parameters called $${p.my.name}: perl warns that the second masks the first`, p.my.pos);
            of.set(p.my, names.length);
            names.push(p.my.name);
            declare(p.my);
        }
        s.body.forEach(statement);
        frames[fn] = variables;
        ({ fn, inScope, variables, scopes, round } = outer);
    };

    const statement = (s: Stmt): void => {
        switch (s.kind) {
        case 'sub': return function_(s);
        case 'return': return s.value === undefined ? undefined : whole(s.value);
        case 'call': return s.args.forEach(a => whole(a));
        case 'do': return whole(s.expr);
        case 'block':
            round.push({ bare: s.pos });
            inner(s.body);
            round.pop();
            return;
        case 'while':
            loops.set(s, loops.size);
            // As under `if`: the statement is written before its test.
            if (s.modifier) {
                s.body.forEach(statement);
                return whole(s.test);
            }
            scopes.push(new Map());
            whole(s.test);
            round.push({ loop: s });
            inner(s.body);
            round.pop();
            close();
            return;
        case 'for':
            loops.set(s, loops.size);
            scopes.push(new Map());
            whole(...s.first);
            if (s.test) whole(s.test);
            whole(...s.each);
            round.push({ loop: s });
            inner(s.body);
            round.pop();
            close();
            return;
        case 'jump': {
            if (s.label !== undefined) {
                const name = s.label.name;
                const found = [...round].reverse().find(r => 'loop' in r && r.loop.label?.name === name);
                if (found === undefined || !('loop' in found)) return refuse(`no loop called ${name} is round this ${s.name}`, s.label.pos);
                jumps.set(s, loops.get(found.loop)!);
                return;
            }
            const nearest = round.at(-1);
            if (nearest === undefined) return refuse(`${s.name} outside a loop`, s.pos);
            // To perl a bare block is a loop that runs once, and this
            // would leave it and nothing more (D59).
            if ('bare' in nearest) {
                return refuse(`${s.name} with no label would leave only the bare block that begins on line ${nearest.bare.line}, to perl: label the loop it is for, and say ${s.name} NAME`, s.pos);
            }
            jumps.set(s, loops.get(nearest.loop)!);
            return;
        }
        case 'if':
            // A modifier's statement is in the scope it stands in, and is
            // written before its test; an `if` with blocks is a scope of
            // its own, for its tests.
            if (s.modifier) {
                s.arms[0]!.body.forEach(statement);
                return whole(s.arms[0]!.test);
            }
            scopes.push(new Map());
            for (const arm of s.arms) {
                whole(arm.test);
                inner(arm.body);
            }
            if (s.otherwise) inner(s.otherwise);
            close();
            return;
        default: return;
        }
    };

    program.body.forEach(statement);
    // The file's own frame: its file variables first, and then the rest,
    // which were numbered from 0 before anyone knew how many those were.
    for (const id of names.keys()) {
        if (owner[id] === 0 && !fileSlots.has(id)) slots[id]! += file;
    }
    frames[0] = file + variables;
    return { of, names, slots, owner, frames, file, subs, calls, loops, jumps };
};
