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
import type { Binder, Expr, Foreach, Invoke, Jump, Loop, My, MyArray, Pos, Program, Stmt, Sub } from './ast.ts';
import { listSubs } from './shapes.ts';

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
//
// An array is a declaration like any other, with a name of its own: `@x`
// and `$x` are two (D80). `isArray` says which a declaration is, and `of`
// has every node that names one: an array, an element, a slice, `$#x`, a
// builtin that takes one.
export type Resolution = {
    of: ReadonlyMap<Expr, number>;
    names: readonly string[];
    isArray: readonly boolean[];
    slots: readonly number[];
    owner: readonly number[];
    frames: readonly number[];
    file: number;
    fileIds: ReadonlySet<number>;
    subs: readonly Sub[];
    calls: ReadonlyMap<Invoke, number>;
    // Which functions give a list back (D18), by number.
    lists: readonly boolean[];
    loops: ReadonlyMap<Loop, number>;
    jumps: ReadonlyMap<Jump, number>;
    each: ReadonlyMap<Foreach | Binder, Each>;
    // The declarations that are a loop's variable or `$_`: read-only (D17).
    readonly: ReadonlySet<number>;
};

// What a `foreach` has beside its variable: `list`, a declaration no
// program can name, whose slot holds the loop's list while it runs; and
// `arrays`, every array named anywhere in the list, which the loop
// freezes (D80, T162).
export type Each = { list: number; arrays: readonly number[] };

// What is round a statement that perl counts as a loop: a loop, or a
// bare block, which runs once (T32).
// And the block of a `map` or a `grep`, which no `last` or `next` may leave
// (T59).
type Round = { loop: Loop } | { bare: Pos } | { wall: string };

export const resolve = (program: Program): Resolution => {
    const of = new Map<Expr, number>();
    const names: string[] = [];
    const isArray: boolean[] = [];
    // An array's name in a scope: with its sigil, so that it is its own.
    const key = (d: My | MyArray): string => (d.kind === 'myarray' ? '@' : '') + d.name;
    // The array a node names, looked up as it is met.
    const array = (e: Expr, name: string): void => {
        const found = [...scopes].reverse().find(scope => scope.has('@' + name));
        if (found === undefined) return refuse(`@${name} is not declared: my @${name}`, e.pos);
        of.set(e, found.get('@' + name)!);
        naming.forEach(set => set.add(found.get('@' + name)!));
    };
    // The arrays named while the list of a `foreach`, a `map` or a `grep`
    // is read: one set for each list that is being read.
    const naming: Set<number>[] = [];
    const each = new Map<Foreach | Binder, Each>();
    const readonly = new Set<number>();
    // The most slots in use since the statement in hand began: a `map`
    // in it has slots of its own while it runs.
    let peak = 0;
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
    const declare = (d: My | MyArray): void => {
        const id = of.get(d)!;
        scopes.at(-1)!.set(key(d), id);
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
        peak = Math.max(peak, inScope);
    };

    // The variables an expression uses, each looked up as it is met; and
    // the ones it declares, which are returned and not yet seen.
    const walk = (e: Expr, declared: (My | MyArray)[]): void => {
        switch (e.kind) {
        case 'var': {
            const found = [...scopes].reverse().find(s => s.has(e.name));
            if (found === undefined && e.name === '_') return refuse('$_ outside the block of a for, a map or a grep: it is the value they give their block, and is seen there alone (D17)', e.pos);
            if (found === undefined) return refuse(`$${e.name} is not declared: my $${e.name}`, e.pos);
            of.set(e, found.get(e.name)!);
            return;
        }
        case 'my':
        case 'myarray':
            of.set(e, names.length);
            isArray.push(e.kind === 'myarray');
            names.push(e.name);
            declared.push(e);
            return;
        case 'array':
        case 'lastindex':
            return array(e, e.name);
        case 'elem':
            walk(e.index, declared);
            return array(e, e.name);
        case 'slice':
            // Its indexes are worked out first (T163).
            e.indexes.forEach(x => walk(x, declared));
            e.items?.forEach(x => walk(x, declared));
            return e.name === undefined ? undefined : array(e, e.name);
        case 'list': return e.items.forEach(x => walk(x, declared));
        case 'arrayop':
            e.args.forEach(x => walk(x, declared));
            return array(e, e.name);
        case 'listop': return e.args.forEach(x => walk(x, declared));
        case 'binder': {
            // The list is read where the binder stands, so a `$_` in it is
            // the one outside; then the block, in a scope of its own.
            const arrays = new Set<number>();
            naming.push(arrays);
            e.items.forEach(x => walk(x, declared));
            naming.pop();
            scopes.push(new Map());
            bind(e, e.var, arrays);
            round.push({ wall: e.op });
            inner(e.body);
            round.pop();
            close();
            return;
        }
        case 'listassign':
            walk(e.value, declared);
            return e.targets.forEach(x => walk(x, declared));
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
        const declared: (My | MyArray)[] = [];
        const before = peak;
        peak = inScope;
        es.forEach(e => walk(e, declared));
        // What this declares is stored to as the statement begins, and a
        // `map` in the statement had slots of its own while it was read:
        // so these come after them (the slots between are let go with
        // the scope).
        if (declared.length > 0 && scopes.at(-1) !== fileScope) {
            for (; inScope < peak; inScope += 1) scopes.at(-1)!.set(` ${inScope}`, -1);
        }
        peak = Math.max(before, peak);
        // In the order they are written: the second of two is the one at
        // fault.
        declared.sort((a, b) => a.pos.line - b.pos.line || a.pos.col - b.pos.col);
        for (const d of declared) {
            const scope = scopes.at(-1)!;
            if (scope.has(key(d))) refuse(`my ${d.kind === 'myarray' ? '@' : '$'}${d.name} again in one scope: perl warns that it masks the first`, d.pos);
            declare(d);
        }
    };

    // What a `foreach`, a `map` or a `grep` has in its scope: its list,
    // a declaration no program can name (no name has a blank in it), and
    // its variable.
    const bind = (binder: Foreach | Binder, variable: My, arrays: ReadonlySet<number>): void => {
        const list: MyArray = { kind: 'myarray', name: 'the list', pos: binder.pos };
        for (const d of [list, variable]) {
            of.set(d, names.length);
            isArray.push(d.kind === 'myarray');
            names.push(d.name);
            declare(d);
        }
        readonly.add(of.get(variable)!);
        each.set(binder, { list: of.get(list)!, arrays: [...arrays] });
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
            if (p.rest !== undefined) {
                of.set(p.rest, names.length);
                isArray.push(true);
                names.push(p.rest.name);
                declare(p.rest);
            }
            if (p.my === undefined) continue;
            if (scopes.at(-1)!.has(p.my.name)) refuse(`two parameters called $${p.my.name}: perl warns that the second masks the first`, p.my.pos);
            of.set(p.my, names.length);
            isArray.push(false);
            names.push(p.my.name);
            declare(p.my);
        }
        s.body.forEach(statement);
        frames[fn] = variables;
        ({ fn, inScope, variables, scopes, round } = outer);
    };

    // perl's `last` in a `map` block leaves the loop round the `map`, and
    // warns (T59).
    const walled = (word: string, op: string): string => `${word} out of the block of a ${op}: a loop says it`;

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
        case 'foreach': {
            loops.set(s, loops.size);
            // The list is read where the loop stands: the loop's variable
            // is not in it.
            const arrays = new Set<number>();
            naming.push(arrays);
            whole(...s.items);
            naming.pop();
            scopes.push(new Map());
            bind(s, s.var, arrays);
            round.push({ loop: s });
            inner(s.body);
            round.pop();
            close();
            return;
        }
        case 'jump': {
            if (s.label !== undefined) {
                const name = s.label.name;
                const found = [...round].reverse().find(r => 'wall' in r || ('loop' in r && r.loop.label?.name === name));
                if (found !== undefined && 'wall' in found) return refuse(walled(s.name, found.wall), s.pos);
                if (found === undefined || !('loop' in found)) return refuse(`no loop called ${name} is round this ${s.name}`, s.label.pos);
                jumps.set(s, loops.get(found.loop)!);
                return;
            }
            const nearest = round.at(-1);
            if (nearest === undefined) return refuse(`${s.name} outside a loop`, s.pos);
            if ('wall' in nearest) return refuse(walled(s.name, nearest.wall), s.pos);
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
    return { of, names, isArray, slots, owner, frames, file, fileIds: fileSlots, subs, calls, lists: listSubs(subs, calls), loops, jumps, each, readonly };
};
