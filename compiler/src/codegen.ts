// The tree to C: straight-line, one statement per operation, each result
// in a temporary (D31), every runtime call taking the context first (D28).
// The C is linked with runtime/rt.c by the driver.
//
// A variable is never copied into a temporary: an operand that is the
// variable itself is read when its operator runs (D14). So an
// expression's C is either a value fixed when it was made (a temporary, a
// literal) or a place, and where an operator gives one of two operands
// (`||`, `? :`) its C is a pointer to whichever it gave.
//
// Every variable and every temporary is a slot of its function's frame,
// `f[n]`, where the collector can see it (D66): the variables first, each
// at its depth among those in scope, and then the temporaries, which every
// statement numbers from the first again. Nothing a program can still use
// is anywhere else when a runtime call is made, and that is the whole of
// what the collector asks of this file.
//
// A loop is C's `for (;;)` with its test inside it, and `last` and `next`
// are each a `goto`, to a label after the loop or at the end of its block:
// C's own `break` and `continue` reach only the nearest loop. They are the
// only jumps there are (D31), but for `return`, below.
//
// A sub is a C function (D72). It is handed its context, perl's three, and
// **where each argument is**, a pointer to a slot of its caller's frame or
// of the file's, or NULL for one that wasn't given: it copies each into a
// slot of its own as that parameter's turn comes, a default running in
// between, which is the order perl has (T144, D73), and what makes an
// argument that is a variable be read late (T1). Until it is copied an
// argument is in a slot of the caller's, where the collector sees it. A
// `return` puts the value in a C local and jumps to the one place the
// frame is closed; nothing can allocate between there and the caller's
// slot. A sub reaches the file's variables through the context, `g[n]`
// (D28: nothing is global). After every call the caller's line is stored
// again (D34).
import { NAMES, PRAGMAS, infixOp, prefixOp, stepOp } from './names.ts';
import type { ArrayOp, Binder, Expr, If, Invoke, Program, Sort, Stmt, Sub } from './ast.ts';
import { behind } from './shapes.ts';
import type { Resolution } from './resolver.ts';
import { handsOn, shaped } from './shapes.ts';
import type { Gives } from './shapes.ts';

// The context an expression is worked out in (D18): one of perl's three,
// or the one its own sub was called in, which a `return` and a last
// statement hand on.
type Want = 'void' | 'scalar' | 'list' | 'pass';
const WANT: Readonly<Record<Want, string>> = { void: 'RT_VOID', scalar: 'RT_SCALAR', list: 'RT_LIST', pass: 'want' };

// A C string literal of `text`'s UTF-8 bytes. Octal, three digits, for
// whatever isn't plain: a shorter escape would swallow a digit after it.
// `?` is escaped so that no two of them begin a trigraph.
export const cString = (text: string): string => {
    let out = '"';
    for (const byte of new TextEncoder().encode(text)) {
        const c = String.fromCharCode(byte);
        const plain = byte >= 0x20 && byte < 0x7f && c !== '"' && c !== '\\' && c !== '?';
        out += plain ? c : '\\' + byte.toString(8).padStart(3, '0');
    }
    return out + '"';
};

// The C of one expression statement or test, as it is made: `vars`, the
// variables it declares, which outlive it; `decls`, its temporaries, all
// declared before its first statement so that a pointer to one set in a
// branch is good after the branch; `lines`, its statements. `strings` is
// the whole program's: the string literals, each a constant at the top
// of the C file, in the order met.
// `fn` is the function it is in, 0 for the file, and `line` the line a
// fault in it names.
// `out` is what the statement is being generated into, for the block of
// a `map` or a `grep`, whose statements are generated in the middle of it.
// `inPlace` is a sort that perl would do in place (T187).
type Code = { vars: string[]; decls: string[]; lines: string[]; temps: number; values: number; out: Out; inPlace?: Expr; strings: string[]; names: Resolution; frame: Frame; fn: number; line: number };

// What the function being generated needs of its frame: the most
// temporaries any one statement of it has.
type Frame = { temporaries: number };

// An expression's C, and whether it has an address: a variable, a
// temporary, or what a pointer points at.
type C = { c: string; place: boolean };

const temp = (b: Code, call: string): C => {
    const t = `f[${b.names.frames[b.fn]! + b.values}]`;
    b.values += 1;
    b.frame.temporaries = Math.max(b.frame.temporaries, b.values);
    b.lines.push(`${t} = ${call};`);
    return { c: t, place: true };
};

// A pointer to an expression's value, which is put in a temporary first
// if it has no address.
const pointTo = (b: Code, v: C): string => `&${v.place ? v.c : temp(b, v.c).c}`;

// The slot of the variable or the array a node names (D80: an element, a
// slice and a builtin name their array).
const variable = (b: Code, e: Expr): string => {
    const id = b.names.of.get(e);
    const slot = id === undefined ? undefined : b.names.slots[id];
    if (id === undefined || slot === undefined) throw new Error(`a ${e.kind} was not resolved`);
    // Its own function's, or the file's, which a sub reaches through `g`.
    return b.names.owner[id] === b.fn ? `f[${slot}]` : `g[${slot}]`;
};

// Whether a declaration is a file variable: undef as the program starts,
// and nothing is stored by its `my` (T134).
const isFile = (b: Code, e: Expr): boolean => {
    const id = b.names.of.get(e);
    return id !== undefined && b.names.owner[id] === 0 && b.names.slots[id]! < b.names.file;
};

// ---- lists (D76, D80)

// An expression behind any unary plus, which hands on where it stands.
const through = (e: Expr): Expr => (e.kind === 'unary' && prefixOp(e.op)?.rt === undefined ? through(e.operand) : e);
const isRange = (e: Expr): boolean => e.kind === 'binary' && infixOp(e.op)?.range === true;
const isRepeat = (e: Expr): boolean => e.kind === 'binary' && infixOp(e.op)?.list === true && (e.left.kind === 'list' || e.left.bracketed === true);
// What is more values than one, or fewer, where a list is wanted.
const listy = (in_: Expr): boolean => {
    const e = through(in_);
    return e.kind === 'array' || e.kind === 'list' || isRange(e) || isRepeat(e)
        || e.kind === 'slice'
        || (e.kind === 'arrayop' && e.op === 'splice')
        || (e.kind === 'listop' && e.op === 'reverse')
        || e.kind === 'binder' || e.kind === 'sort'
        || (e.kind === 'ternary' && (listy(e.then) || listy(e.else)))
        || (e.kind === 'binary' && infixOp(e.op)?.when !== undefined && listy(e.right));
};

// Where perl would make an element that is not there, and so the language
// faults for one past either end (T161): nowhere; a slice among a call's
// arguments; a slice or an element in a `foreach`'s list, through what
// hands a list on.
type Strict = 0 | 1 | 2;

// Whether a call is of a sub that gives a list back (D18).
const gives = (names: Resolution): Gives => (call: Invoke) => names.lists[names.calls.get(call)!] === true;

// A list, built in a temporary: made empty, and each item added to it in
// turn, a value or the values of what is itself a list.
const genList = (items: readonly Expr[], b: Code, strict: Strict = 0): C => {
    const list = temp(b, 'rt_array_new(cx)');
    items.forEach(item => addItem(item, list.c, b, strict));
    return list;
};

const addItem = (in_: Expr, list: string, b: Code, strict: Strict): void => {
    const e = through(in_);
    if (e.kind === 'array') {
        b.lines.push(`rt_list_add_all(cx, ${list}, ${variable(b, e)});`);
    } else if (e.kind === 'list') {
        e.items.forEach(item => addItem(item, list, b, strict));
    } else if (e.kind === 'binary' && isRange(e)) {
        const from = genExpr(e.left, b);
        const to = genExpr(e.right, b);
        b.lines.push(`rt_list_add_range(cx, ${list}, ${from.c}, ${to.c});`);
    } else if (e.kind === 'slice') {
        // The indexes first, and then what they are indexes into (T163).
        const indexes = genList(e.indexes, b);
        if (e.name !== undefined) {
            b.lines.push(`rt_list_add_slice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, ${strict ? 2 : 0});`);
        } else {
            const from = genList(e.items!, b);
            b.lines.push(`rt_list_add_slice(cx, ${list}, ${from.c}, ${indexes.c}, 1);`);
        }
    } else if (e.kind === 'binary' && isRepeat(e)) {
        const values = genList([e.left], b, strict === 2 ? 2 : 0);
        const count = genExpr(e.right, b);
        b.lines.push(`rt_list_add_repeat(cx, ${list}, ${values.c}, ${count.c});`);
    } else if (e.kind === 'arrayop' && e.op === 'splice') {
        genSplice(e, b, list);
    } else if (e.kind === 'binder') {
        genBinder(e, b, list);
    } else if (e.kind === 'sort') {
        genSort(e, b, list);
    } else if (e.kind === 'listop' && e.op === 'reverse') {
        // perl's `reverse` makes no element that is not there (T177).
        const values = genList(e.args, b);
        b.lines.push(`rt_list_add_reversed(cx, ${list}, ${values.c});`);
    } else if (e.kind === 'ternary' && (listy(e) || strict === 2)) {
        const test = genExpr(e.test, b);
        b.lines.push(`if (rt_is_true(cx, ${test.c})) {`);
        addItem(e.then, list, b, strict);
        b.lines.push('} else {');
        addItem(e.else, list, b, strict);
        b.lines.push('}');
    } else if (e.kind === 'binary' && infixOp(e.op)?.when !== undefined && (listy(e) || strict === 2)) {
        // The left side is one value, an array's count too (T150); the
        // right, if it is wanted, is the list.
        const left = genExpr(e.left, b);
        const kept = left.place ? left : temp(b, left.c);
        b.lines.push(`if (${infixOp(e.op)!.when}(cx, ${kept.c})) {`);
        addItem(e.right, list, b, strict);
        b.lines.push('} else {', `rt_list_add(cx, ${list}, ${kept.c});`, '}');
    } else if (e.kind === 'elem' && strict === 2) {
        const at = genExpr(e.index, b);
        const value = temp(b, `rt_elem_strict(cx, ${variable(b, e)}, ${at.c})`);
        b.lines.push(`rt_list_add(cx, ${list}, ${value.c});`);
    } else {
        // One value, or none: a sub that returned nothing (D79).
        b.lines.push(`rt_list_add(cx, ${list}, ${genExpr(in_, b, 'list').c});`);
    }
};

// `map` and `grep` (step 10b): a `foreach` in the middle of a statement.
// The list is built, once, into a slot of the binder's own; every array it
// names is frozen while the block runs (D80); `$_` is a copy, stored anew
// each time round. The block's statements are generated where they stand,
// as a loop's are, their temporaries numbered after this statement's own
// so far; then the block's value, which is this statement's to work out:
// `map` adds its values to `list`, and `grep` adds `$_` if it is true.
// Nothing leaves a block but by its end: no `return`, and no `last` or
// `next` to a loop outside it (T59, T174).
const genBinder = (e: Binder, b: Code, list: string): void => {
    const each = b.names.each.get(e);
    const last = e.body.at(-1);
    if (each === undefined || last === undefined) throw new Error(`a ${e.op} was not resolved`);
    const slot = (decl: number): string => `${b.names.owner[decl] === b.fn ? 'f' : 'g'}[${b.names.slots[decl]}]`;
    const it = slot(b.names.of.get(e.var)!);
    const held = slot(each.list);
    const at = `bn${++b.temps}`;
    b.decls.push(`int64_t ${at} RT_UNUSED;`);
    // (An element or a slice past the end in the list is a fault, as in a
    // `foreach`: perl would make it, T177.)
    const source = genList(e.items, b, 2);
    b.lines.push(`${held} = ${source.c};`, ...each.arrays.map(a => `rt_freeze(cx, ${slot(a)});`));
    b.lines.push(`for (${at} = 0; ${at} < rt_list_length(cx, ${held}); ${at}++) {`, `${it} = rt_list_item(cx, ${held}, ${at}); // $_`);
    const base = b.out.base;
    b.out.base = b.values;
    const statements = e.body.slice(0, -1).flatMap(t => genStmt(t, b.out));
    b.out.base = base;
    b.lines.push(...statements, `cx->line = ${last.pos.line};`);
    if (last.kind !== 'do') {
        // A block that ends in a `say`: `true` (D70).
        b.out.base = b.values;
        b.lines.push(...genStmt(last, b.out), `rt_list_add(cx, ${list}, ${e.op === 'grep' ? it : 'rt_bool(1)'});`);
        b.out.base = base;
    } else if (e.op === 'grep') {
        const kept = genExpr(last.expr, b);
        b.lines.push(`if (rt_is_true(cx, ${kept.c})) rt_list_add(cx, ${list}, ${it});`);
    } else {
        addItem(last.expr, list, b, 0);
    }
    b.lines.push('}', ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`), `cx->line = ${b.line};`);
};

// `sort` (step 10c; D82, D83). The list is built and held as a `map`'s
// is, its arrays frozen; an element or a slice past the end in it is a
// fault (T188). With no block the runtime sorts it, by string. With one,
// **this code drives the sort**: the runtime's merge runs as far as its
// next comparison and hands back the two values, which are `$a` and `$b`;
// the block is generated here, where it stands, and its value handed
// back; and so on until the merge has no more to ask. The runtime calls
// nothing. The values, in order, are added to `list`.
const genSort = (e: Sort, b: Code, list: string): void => {
    const source = genList(e.items, b, 2);
    if (e.body === undefined) {
        b.lines.push(`rt_sort_strings(cx, ${source.c}, ${list});`);
        return;
    }
    const each = b.names.each.get(e);
    const last = e.body.at(-1);
    if (each === undefined || last?.kind !== 'do') throw new Error('a sort was not resolved');
    const slot = (decl: number): string => `${b.names.owner[decl] === b.fn ? 'f' : 'g'}[${b.names.slots[decl]}]`;
    const held = slot(each.list);
    const so = `so${++b.temps}`;
    b.decls.push(`rt_sort *${so} RT_UNUSED;`);
    b.lines.push(`${held} = ${source.c};`, ...each.arrays.map(a => `rt_freeze(cx, ${slot(a)});`));
    if (b.inPlace === e) b.lines.push(`rt_sort_in_place(cx, ${held});`);
    b.lines.push(`${so} = rt_sort_begin(cx, ${held}, ${thrownAway(e) ? 1 : 0});`,
        `while (rt_sort_next(cx, ${so}, &${slot(b.names.of.get(e.a!)!)}, &${slot(b.names.of.get(e.b!)!)})) {`);
    const base = b.out.base;
    b.out.base = b.values;
    const statements = e.body.slice(0, -1).flatMap(t => genStmt(t, b.out));
    b.out.base = base;
    b.lines.push(...statements, `cx->line = ${last.pos.line};`);
    const answer = genExpr(last.expr, b);
    b.lines.push(`rt_sort_answer(cx, ${so}, ${answer.c});`, '}', `rt_sort_end(cx, ${so}, ${list});`,
        ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`), `cx->line = ${b.line};`);
};

// The four blocks perl compares without running (`$a <=> $b`, `$b <=> $a`,
// `$a cmp $b`, `$b cmp $a`): for those it turns every value to a number or
// a string before it sorts, and so looks at a lone one (T190).
const thrownAway = (e: Sort): boolean => {
    const only = e.body?.length === 1 ? e.body[0] : undefined;
    const test = only?.kind === 'do' ? behind(only.expr) : undefined;
    if (test?.kind !== 'binary' || (test.op !== '<=>' && test.op !== 'cmp')) return false;
    const [left, right] = [behind(test.left), behind(test.right)];
    return left.kind === 'var' && right.kind === 'var' && [left.name, right.name].sort().join('') === 'ab';
};

// `@a = sort { ... } @a`, through brackets on either side: perl sorts in
// place, and drops what was never stored (T187).
const sortedInPlace = (b: Code, target: Expr, value: Expr): Expr | undefined => {
    const sort = behind(value);
    if (target.kind !== 'array' || sort.kind !== 'sort' || sort.body === undefined || sort.items.length !== 1) return undefined;
    const from = behind(sort.items[0]!);
    return from.kind === 'array' && b.names.of.get(from) === b.names.of.get(target) ? sort : undefined;
};

// `splice(@a, OFFSET, LENGTH, LIST)`: the numbers, then the list, then
// the splice, what it removed added to `removed`.
const genSplice = (e: ArrayOp, b: Code, removed: string): void => {
    const [offset, length] = [e.args[0], e.args[1]].map(a => (a === undefined ? undefined : genExpr(a, b)));
    const put = genList(e.args.slice(2), b);
    b.lines.push(`rt_splice(cx, ${removed}, ${variable(b, e)}, ${Math.min(e.args.length, 2)}, ${offset?.c ?? 'rt_undef()'}, ${length?.c ?? 'rt_undef()'}, ${put.c});`);
};

// A C local for where an element is, once it has been made.
const index = (b: Code, e: Expr): string => {
    if (e.kind !== 'elem') throw new Error('not an element');
    const at = `i${++b.temps}`;
    b.decls.push(`int64_t ${at} RT_UNUSED;`);
    b.lines.push(`${at} = rt_elem_make(cx, ${variable(b, e)}, ${genExpr(e.index, b).c});`);
    return at;
};

// The C for an expression's value, once the statements appended to `b`
// have run. Operands are generated left before right, so that is the
// order they run in, and the first of two faults is the left one. Nothing
// that can fault is ever an argument of a call: C doesn't say which
// argument it would evaluate first.
const genExpr = (e: Expr, b: Code, want: Want = 'scalar'): C => {
    switch (e.kind) {
    // The checker has seen every literal: it is 0 to 2^63 - 1.
    case 'int': return { c: `rt_int(INT64_C(${e.value}))`, place: false };
    // A Num goes over as its 64 bits: no decimal is read twice.
    case 'num': return { c: `rt_num_bits(UINT64_C(0x${new BigUint64Array(new Float64Array([e.value]).buffer)[0]!.toString(16)}))`, place: false };
    // A string literal is a constant the program never allocates: its
    // bytes as UTF-8, how many there are, and how many characters.
    case 'str': {
        const bytes = new TextEncoder().encode(e.value).length;
        b.strings.push(`static const rt_str s${b.strings.length + 1} = { ${bytes}, ${[...e.value].length}, ${cString(e.value)} };`);
        return { c: `rt_string(&s${b.strings.length})`, place: false };
    }
    case 'constant': {
        const name = NAMES.get(e.name);
        if (name?.kind !== 'constant') throw new Error(`no value for ${e.name}`);
        return { c: name.c, place: false };
    }
    case 'var': return { c: variable(b, e), place: true };
    // `my $x`: an undef, each time the `my` is reached, whatever the slot
    // held for a variable before it.
    case 'my':
        if (!isFile(b, e)) b.vars.push(`${variable(b, e)} = rt_undef(); // my $${e.name}`);
        return { c: variable(b, e), place: true };
    // `my @a`: a new array each time the `my` is reached; the file's are
    // made as the program starts (T156).
    case 'myarray':
        if (!isFile(b, e)) b.vars.push(`${variable(b, e)} = rt_array_new(cx); // my @${e.name}`);
        return { c: variable(b, e), place: true };
    // Where one value is wanted, an array is its count, at once (T21).
    case 'array': return temp(b, `rt_count(cx, ${variable(b, e)})`);
    case 'lastindex': return temp(b, `rt_last_index(cx, ${variable(b, e)})`);
    // An element is read where it stands (D76).
    case 'elem': {
        const at = genExpr(e.index, b);
        return temp(b, `rt_elem(cx, ${variable(b, e)}, ${at.c})`);
    }
    // `(LIST)[N]`, where one value is wanted: that one, or undef.
    case 'slice': return temp(b, `rt_first(cx, ${genList([e], b).c})`);
    case 'sort': throw new Error('sort where one value is wanted');
    // Where one value is wanted, how many values it gives (D84).
    case 'binder': {
        const values = temp(b, 'rt_array_new(cx)');
        genBinder(e, b, values.c);
        return temp(b, `rt_count(cx, ${values.c})`);
    }
    // `join`: the separator, which is read when the list has been built
    // (T186), and the list.
    case 'listop': {
        if (e.op !== 'join') throw new Error(`${e.op} where one value is wanted`);
        const sep = genExpr(e.args[0]!, b);
        const kept = sep.place ? sep : temp(b, sep.c);
        const values = genList(e.args.slice(1), b);
        return temp(b, `rt_join(cx, ${kept.c}, ${values.c})`);
    }
    // Declarations alone, `my ($x, @a);`; and brackets round one value
    // with a comma after it, where one value is wanted.
    case 'list':
        if (e.items.length === 1 && !e.my) return genExpr(e.items[0]!, b, want);
        e.items.forEach(item => genExpr(item, b));
        return { c: 'rt_undef()', place: false };
    case 'arrayop': {
        const name = NAMES.get(e.op);
        if (name?.kind !== 'arrayop') throw new Error(`no runtime function for ${e.op}`);
        if (name.shape === 'push') {
            const values = genList(e.args, b);
            return temp(b, `${name.rt}(cx, ${variable(b, e)}, ${values.c})`);
        }
        if (name.shape === 'splice') {
            // As a statement: what it removed is not wanted.
            const removed = temp(b, 'rt_array_new(cx)');
            genSplice(e, b, removed.c);
            return { c: 'rt_undef()', place: false };
        }
        return temp(b, `${name.rt}(cx, ${variable(b, e)})`);
    }
    // The right side, then each target's index, then the stores, a value
    // for each target in turn, undef when they run out; an array takes
    // what is left (D80, T158).
    case 'listassign': {
        const values = genList([e.value], b);
        e.targets.forEach(t => { if (t.kind === 'my' || t.kind === 'myarray') genExpr(t, b); });
        // An index is a value before anything is stored: one that is a
        // variable is copied now, since a target before it may be that
        // variable (`($i, $a[$i]) = (1, 5)` stores at the old `$i`).
        const kept = (v: C): C => (v.place ? temp(b, v.c) : v);
        const indexes = e.targets.map(t => (t.kind === 'elem' ? kept(genExpr(t.index, b)) : undefined));
        e.targets.forEach((t, n) => {
            if (t.kind === 'constant') return;
            if (t.kind === 'array' || t.kind === 'myarray') b.lines.push(`rt_array_rest(cx, ${variable(b, t)}, ${values.c}, ${n});`);
            else if (t.kind === 'elem') b.lines.push(`rt_elem_store(cx, ${variable(b, t)}, ${indexes[n]!.c}, rt_list_item(cx, ${values.c}, ${n}));`);
            else b.lines.push(`${variable(b, t)} = rt_list_item(cx, ${values.c}, ${n});`);
        });
        return { c: 'rt_undef()', place: false };
    }
    // The right side first, and then the variable is read, if the
    // operator reads it, and set. The value is the variable.
    case 'assign': {
        const op = infixOp(e.op);
        // `@a = LIST`: the list, and then the array's values are its.
        if (e.target.kind === 'array' || e.target.kind === 'myarray') {
            const before = b.inPlace;
            b.inPlace = sortedInPlace(b, e.target, e.value);
            const values = genList([e.value], b);
            b.inPlace = before;
            if (e.target.kind === 'myarray') genExpr(e.target, b);
            b.lines.push(`rt_array_assign(cx, ${variable(b, e.target)}, ${values.c});`);
            return { c: 'rt_undef()', place: false };
        }
        if (e.target.kind === 'elem') {
            const array = variable(b, e.target);
            // `=`: the right side, then the index, then the store, the
            // right side read then if it is a variable (T158).
            if (op?.rt === undefined && op?.when === undefined) {
                const value = genExpr(e.value, b);
                const at = genExpr(e.target.index, b);
                return temp(b, `rt_elem_store(cx, ${array}, ${at.c}, ${value.c})`);
            }
            // The others: the index, the target made, then the right
            // side, then the element read, worked on and stored (T159).
            const at = index(b, e.target);
            if (op.when !== undefined) {
                const was = temp(b, `rt_elem_get(cx, ${array}, ${at})`);
                b.lines.push(`if (${op.when}(cx, ${was.c})) {`);
                b.lines.push(`rt_elem_put(cx, ${array}, ${at}, ${genExpr(e.value, b).c});`, '}');
                return temp(b, `rt_elem_get(cx, ${array}, ${at})`);
            }
            const value = genExpr(e.value, b);
            const was = temp(b, `rt_elem_get(cx, ${array}, ${at})`);
            const now = temp(b, `${op.rt}(cx, ${was.c}, ${value.c})`);
            b.lines.push(`rt_elem_put(cx, ${array}, ${at}, ${now.c});`);
            return now;
        }
        if (e.target.kind === 'my') genExpr(e.target, b);
        const v = variable(b, e.target);
        if (op?.when !== undefined) {
            b.lines.push(`if (${op.when}(cx, ${v})) {`);
            b.lines.push(`${v} = ${genExpr(e.value, b).c};`, '}');
        } else {
            const value = genExpr(e.value, b);
            b.lines.push(op?.rt === undefined ? `${v} = ${value.c};` : `${v} = ${op.rt}(cx, ${v}, ${value.c});`);
        }
        return { c: v, place: true };
    }
    // `++$x` is the variable; `$x++` is what it held, kept in a temporary.
    case 'step': {
        const op = stepOp(e.op);
        if (op === undefined) throw new Error(`no runtime function for ${e.op}`);
        if (e.target.kind === 'elem') {
            const array = variable(b, e.target);
            const at = index(b, e.target);
            const held = temp(b, `rt_elem_get(cx, ${array}, ${at})`);
            const was = e.before || op.before === undefined ? held : temp(b, `${op.before}(cx, ${held.c})`);
            const now = temp(b, `${op.rt}(cx, ${held.c})`);
            b.lines.push(`rt_elem_put(cx, ${array}, ${at}, ${now.c});`);
            return e.before ? now : was;
        }
        const v = variable(b, e.target);
        const was = e.before ? undefined : temp(b, op.before === undefined ? v : `${op.before}(cx, ${v})`);
        b.lines.push(`${v} = ${op.rt}(cx, ${v});`);
        return was ?? { c: v, place: true };
    }
    case 'unary': {
        const rt = prefixOp(e.op)?.rt;
        // Unary plus is in the language and does nothing: what it is
        // given is what it gives, the variable itself included, and its
        // context is its operand's (T146).
        const operand = genExpr(e.operand, b, rt === undefined ? want : 'scalar');
        return rt === undefined ? operand : temp(b, `${rt}(cx, ${operand.c})`);
    }
    // One branch is worked out, and the other is C that doesn't run: so
    // a fault in it doesn't happen (D49). The value is whichever branch's,
    // itself.
    case 'ternary': {
        const test = genExpr(e.test, b);
        const p = `p${++b.temps}`;
        b.decls.push(`rt_value *${p} RT_UNUSED;`);
        b.lines.push(`if (rt_is_true(cx, ${test.c})) {`);
        b.lines.push(`${p} = ${pointTo(b, genExpr(e.then, b, want))};`, '} else {');
        b.lines.push(`${p} = ${pointTo(b, genExpr(e.else, b, want))};`, '}');
        return { c: `(*${p})`, place: true };
    }
    case 'apply': {
        // Arguments left before right, each in a temporary, a variable or
        // a literal by the time the call is made.
        const args = e.args.map(a => genExpr(a, b).c);
        const name = NAMES.get(e.name);
        const rt = name?.kind === 'unary' ? name.rt : name?.kind === 'function' ? name.rt[e.args.length - name.min] : undefined;
        if (rt === undefined) throw new Error(`no runtime function for ${e.name}`);
        return temp(b, `${rt}(${['cx', ...args].join(', ')})`);
    }
    // A call of a sub. Every argument is worked out, left to right, each
    // a list to perl; then the count is looked at, as perl does it; then
    // the sub is handed where they are. What it returns is kept in a
    // temporary, void or not, and the line is the caller's again.
    case 'invoke': {
        const called = b.names.subs[b.names.calls.get(e)! - 1]!;
        const most = called.params.length;
        const n = ++b.temps;
        b.decls.push(`rt_value *av${n}[${Math.max(1, most, e.args.length)}] RT_UNUSED;`, `int64_t ac${n} RT_UNUSED;`, `rt_value *fl${n} RT_UNUSED = NULL;`);
        if (e.args.some(a => listy(a) || handsOn(a, gives(b.names)))) {
            // A list among them, or a call that gives one: all of them
            // are built as one list, copied, and the sub is handed where
            // its values are, which is one after another.
            const values = genList(e.args, b, 1);
            b.lines.push(`ac${n} = rt_list_length(cx, ${values.c});`, `fl${n} = rt_list_items(cx, ${values.c});`);
        } else {
            // Each a place, or a temporary: a variable is read when the
            // sub takes it (D73). A call that gave nothing is no argument.
            const where = e.args.map(a => pointTo(b, genExpr(a, b, 'list')));
            b.lines.push(`ac${n} = 0;`);
            where.forEach(p => b.lines.push(`if ((${p})->tag != RT_TAG_ABSENT) av${n}[ac${n}++] = ${p};`));
        }
        const result = temp(b, `sub_${e.name}(cx, ${WANT[want]}, ac${n}, av${n}, fl${n})`);
        b.lines.push(`cx->line = ${b.line};`);
        return result;
    }
    case 'binary': {
        const op = infixOp(e.op);
        const left = genExpr(e.left, b);
        // `&&`, `||`, `//`: the value is the left operand, unless the test
        // says the right one is wanted, and only then is it worked out.
        if (op?.when !== undefined) {
            const p = `p${++b.temps}`;
            b.decls.push(`rt_value *${p} RT_UNUSED;`);
            b.lines.push(`${p} = ${pointTo(b, left)};`, `if (${op.when}(cx, *${p})) {`);
            b.lines.push(`${p} = ${pointTo(b, genExpr(e.right, b, want))};`, '}');
            return { c: `(*${p})`, place: true };
        }
        const right = genExpr(e.right, b);
        if (op?.rt === undefined) throw new Error(`no runtime function for ${e.op}`);
        return temp(b, `${op.rt}(cx, ${left.c}, ${right.c})`);
    }
    }
};

// What is being generated: the whole program's strings and names, and the
// function in hand, its frame, and its sub if it is one.
// `open` is the loops round the statement in hand, the nearest last, each
// with the C that gives back what it froze: a `last` or `next` to a loop
// further out, and a `return`, leave by a `goto`, and run it first.
// `base` is the temporaries a statement begins after: none, unless it is
// in the block of a `map` or a `grep`, where it is those the statement the
// block stands in has in use.
type Out = { strings: string[]; names: Resolution; frame: Frame; fn: number; sub?: Sub; open: { id: number; thaws: readonly string[] }[]; base: number };

const inLoop = (out: Out, id: number | undefined, thaws: readonly string[], body: readonly Stmt[]): string[] => {
    if (id === undefined) throw new Error('a loop was not resolved');
    out.open.push({ id, thaws });
    const lines = body.flatMap(t => genStmt(t, out));
    out.open.pop();
    return lines;
};

// The C of an expression that is a statement's or a test's, and what it
// is worth. A fault names the line its statement starts on (D34), a test's
// the line of its `if` or `elsif`: so the line is stored first.
// `vars` are the variables it declares, which belong to the C block the
// statement stands in.
const genWhole = (e: Expr, line: number, out: Out, use: (c: string) => string[], want: Want = 'scalar'): { vars: string[]; code: string[] } => {
    const b: Code = { vars: [], decls: [], lines: [], temps: 0, values: out.base, out, strings: out.strings, names: out.names, frame: out.frame, fn: out.fn, line };
    const c = genExpr(e, b, want).c;
    return { vars: b.vars, code: [`cx->line = ${line};`, ...b.decls, ...b.lines, ...use(c)] };
};

// The same for a list: `say`'s.
const genListWhole = (items: readonly Expr[], line: number, out: Out, use: (c: string) => string[]): { code: string[] } => {
    const b: Code = { vars: [], decls: [], lines: [], temps: 0, values: out.base, out, strings: out.strings, names: out.names, frame: out.frame, fn: out.fn, line };
    const c = genList(items, b).c;
    return { code: [`cx->line = ${line};`, ...b.decls, ...b.lines, ...use(c)] };
};

const indent = (lines: string[]): string[] => lines.map(l => `    ${l}`);

// The expressions of one part of a `for`, left to right, in a C block of
// their own for their temporaries; nothing, for an empty part.
const genParts = (es: readonly Expr[], line: number, out: Out): { vars: string[]; code: string[] } => {
    const b: Code = { vars: [], decls: [], lines: [], temps: 0, values: out.base, out, strings: out.strings, names: out.names, frame: out.frame, fn: out.fn, line };
    es.forEach(e => genExpr(e, b, 'void'));
    return { vars: b.vars, code: es.length ? ['{', ...indent([`cx->line = ${line};`, ...b.decls, ...b.lines]), '}'] : [] };
};

// An `if` chain from arm `n` on: this arm's test, its block, and the rest
// of the chain as its `else`. A test's variables and temporaries are in
// the C block the chain opens, or the `else` it is in, so they are seen
// by this arm's block and the arms after it, and no further.
const genArms = (s: If, n: number, out: Out): string[] => {
    const arm = s.arms[n];
    if (arm === undefined) return (s.otherwise ?? []).flatMap(t => genStmt(t, out));
    const rest = genArms(s, n + 1, out);
    // A test's fault names the line of its `if` or `elsif`; under a
    // modifier, the line the statement before it starts on, as perl has
    // it for both.
    const test = genWhole(arm.test, s.modifier ? s.pos.line : arm.pos.line, out, c => [
        `if (${arm.negate ? 'rt_is_false' : 'rt_is_true'}(cx, ${c})) {`,
        ...indent(arm.body.flatMap(t => genStmt(t, out))),
        ...(rest.length ? ['} else {', ...indent(rest), '}'] : ['}']),
    ]);
    return [...test.vars, ...test.code];
};

// What a `return`'s value, or a last statement's, is worth to the call
// (D18). List-shaped: a fault for a call that wants one value, before
// anything of it is worked out, and otherwise a list. What may be a list
// and is not list-shaped (`()`, `(LIST)[N]`, brackets round one value) is
// a list to a call that wants one and a value to any other. Anything else
// is one value, or what a call it hands on gave.
const genGiven = (e: Expr, line: number, out: Out, after: readonly string[]): string[] => {
    const asList = (): string[] => genListWhole([e], line, out, c => [`r = ${c};`, ...after]).code;
    const asValue = (): string[] => genWhole(e, line, out, c => [`r = ${c};`, ...after], 'pass').code;
    if (shaped(e, gives(out.names))) {
        return ['if (want == RT_SCALAR) {', `    cx->line = ${line};`, `    rt_fault_sub(cx, ${cString(out.sub!.name)}, RT_LISTED);`, '}', ...asList()];
    }
    if (!listy(e)) return asValue();
    // A sub with nothing list-shaped in it is called as one that gives a
    // value or none (its caller hands on a pointer to what it gave): so
    // that is what it gives, and the list here holds no more than one.
    const few = out.names.lists[out.fn] === true ? asList()
        : genListWhole([e], line, out, c => [`r = rt_only(cx, ${c});`, ...after]).code;
    return ['if (want == RT_LIST) {', ...indent(few), '} else {', ...indent(asValue()), '}'];
};

// What a `return` gives back on its way out: everything the loops it is
// in have frozen.
const leaving = (out: Out): string[] => [...out.open].reverse().flatMap(l => l.thaws);

const genStmt = (s: Stmt, out: Out): string[] => {
    switch (s.kind) {
    // `use v5.42;` says which language this is; it does nothing at run time.
    case 'use': return [];
    // A pragma is the compiler's business, unless the table gives it
    // something to do as the program starts.
    case 'pragma': {
        const rt = PRAGMAS.get(s.name)?.rt;
        return rt === undefined ? [] : [`${rt}(cx);`];
    }
    case 'call': {
        const name = NAMES.get(s.name);
        if (name?.kind !== 'statement') throw new Error(`no runtime function for ${s.name}`);
        // A block of its own keeps each statement's temporaries out of the
        // next one's way: a C compiler is slow over ten thousand locals in
        // one scope.
        return ['{', ...indent(genListWhole(s.args, s.pos.line, out, c => [`${name.rt}(cx, ${c});`]).code), '}'];
    }
    // The variables an expression statement declares are the enclosing
    // block's, and come before the C block its temporaries are in.
    case 'do': {
        const whole = genWhole(s.expr, s.pos.line, out, () => [], 'void');
        return [...whole.vars, '{', ...indent(whole.code), '}'];
    }
    case 'block': return ['{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}'];
    case 'if': return ['{', ...indent(genArms(s, 0, out)), '}'];
    // The test is worked out in the loop's own C block, each time round:
    // so what it declares is new each time, and the block of the loop,
    // inside it, sees it (T119). The block's own variables are in a C
    // block of their own for the same reason. A fault in the test names
    // the loop's line, and under a modifier the statement's, which is
    // where the node is (D62).
    case 'while': {
        const test = genWhole(s.test, s.pos.line, out, c => [`if (${s.negate ? 'rt_is_true' : 'rt_is_false'}(cx, ${c})) break;`]);
        const id = out.names.loops.get(s);
        return [
            'for (;;) {',
            ...indent([...test.vars, ...test.code, '{', ...indent(inLoop(out, id, [], s.body)), '}', `next_${id}: RT_UNUSED;`]),
            '}',
            `last_${id}: RT_UNUSED;`,
        ];
    }
    // What the first part declares is one variable for the whole loop, in
    // the C block the loop stands in. `next` comes out before the third
    // part, which runs; `last` after the loop, where it doesn't.
    case 'for': {
        const first = genParts(s.first, s.pos.line, out);
        const test = s.test === undefined ? [] : genWhole(s.test, s.pos.line, out, c => [`if (rt_is_false(cx, ${c})) break;`]).code;
        const each = genParts(s.each, s.pos.line, out);
        const id = out.names.loops.get(s);
        return [
            '{',
            ...indent([
                ...first.vars, ...first.code,
                'for (;;) {',
                ...indent([...(test.length ? ['{', ...indent(test), '}'] : []), '{', ...indent(inLoop(out, id, [], s.body)), '}', `next_${id}: RT_UNUSED;`, ...each.code]),
                '}',
                `last_${id}: RT_UNUSED;`,
            ]),
            '}',
        ];
    }
    case 'jump': {
        const name = NAMES.get(s.name);
        const id = out.names.jumps.get(s);
        if (name?.kind !== 'jump' || id === undefined) throw new Error(`${s.name} was not resolved`);
        // What the loops inside the one it is for have frozen is given
        // back on the way; its own loop's is given back after `last_`.
        const at = out.open.map(l => l.id).lastIndexOf(id);
        if (at < 0) throw new Error(`${s.name} is in no loop`);
        return [...out.open.slice(at + 1).reverse().flatMap(l => l.thaws), `goto ${name.leaves ? 'last' : 'next'}_${id};`];
    }
    // The list is built once, into a slot the loop keeps (a statement's
    // temporaries are the next statement's too), and every array it names
    // is frozen from then until the loop is left, by any way out (D80,
    // T162). The variable is a copy, stored anew each time round. A loop
    // over one range counts in C and builds nothing.
    case 'foreach': {
        const id = out.names.loops.get(s);
        const each = out.names.each.get(s);
        if (id === undefined || each === undefined) throw new Error('a foreach was not resolved');
        const b: Code = { vars: [], decls: [], lines: [], temps: 0, values: out.base, out, strings: out.strings, names: out.names, frame: out.frame, fn: out.fn, line: s.pos.line };
        const slot = (decl: number): string => `${out.names.owner[decl] === out.fn ? 'f' : 'g'}[${out.names.slots[decl]}]`;
        const x = slot(out.names.of.get(s.var)!);
        const one = s.items.length === 1 ? through(s.items[0]!) : undefined;
        const range = one !== undefined && one.kind === 'binary' && isRange(one) ? one : undefined;
        let loop: string[];
        if (range) {
            const from = genExpr(range.left, b);
            const to = genExpr(range.right, b);
            b.lines.push(`go_${id} = rt_range_ends(cx, ${from.c}, ${to.c}, &at_${id}, &end_${id});`);
            loop = [`if (go_${id}) for (;; at_${id}++) {`, `    ${x} = rt_int(at_${id}); // $${s.var.name}`];
        } else {
            const list = genList(s.items, b, 2);
            b.lines.push(`${slot(each.list)} = ${list.c};`);
            loop = [`for (; at_${id} < rt_list_length(cx, ${slot(each.list)}); at_${id}++) {`, `    ${x} = rt_list_item(cx, ${slot(each.list)}, at_${id}); // $${s.var.name}`];
        }
        const thaws = each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`);
        return [
            '{',
            ...indent([
                `cx->line = ${s.pos.line};`,
                `int64_t at_${id} = 0, end_${id} RT_UNUSED = 0;`,
                `int go_${id} RT_UNUSED = 0;`,
                ...b.decls, ...b.lines,
                ...each.arrays.map(a => `rt_freeze(cx, ${slot(a)});`),
                ...loop,
                ...indent(['{', ...indent(inLoop(out, id, thaws, s.body)), '}', `next_${id}: RT_UNUSED;`, ...(range ? [`if (at_${id} == end_${id}) break;`] : [])]),
                '}',
                `last_${id}: RT_UNUSED;`,
                ...thaws,
            ]),
            '}',
        ];
    }
    // A sub is a function of its own, written by `genSub`.
    case 'sub': return [];
    // The value into the C local that is returned, and out by the one
    // way there is. `return;` is undef to a scalar, and to a list it is
    // nothing at all, which the language can't yet say (D71).
    case 'return': {
        if (s.value === undefined) {
            return ['{', ...indent([`cx->line = ${s.pos.line};`, 'r = want == RT_LIST ? rt_absent() : rt_undef();', ...leaving(out), 'goto done;']), '}'];
        }
        return ['{', ...indent(genGiven(s.value, s.pos.line, out, [...leaving(out), 'goto done;'])), '}'];
    }
    }
};

// A sub as a C function. Its parameters are the first of its variables,
// each copied from where the caller said its argument is when its turn
// comes, or given its default; then the body; then what the sub is worth
// if it ends with no `return` (D72): its last statement's value if that is
// an expression, `true` after a `say` (D70), and otherwise nothing, which
// is a fault unless the call was void (D18).
const genSub = (s: Sub, fn: number, strings: string[], names: Resolution): string[] => {
    const out: Out = { strings, names, frame: { temporaries: 0 }, fn, sub: s, open: [], base: 0 };
    const name = cString(s.name);
    const lines: string[] = [];
    for (const [n, p] of s.params.entries()) {
        const slot = p.my === undefined ? undefined : `f[${names.slots[names.of.get(p.my)!]}]`;
        const given = p.op === '//=' ? `a${n} != NULL && !rt_is_undef(cx, *a${n})`
            : p.op === '||=' ? `a${n} != NULL && rt_is_true(cx, *a${n})`
            : `a${n} != NULL`;
        const copy = slot === undefined ? [] : [`${slot} = *a${n}; // $${p.my!.name}`];
        if (p.slurpy) {
            // Filled now, at its turn, from where the arguments are (T191).
            if (p.rest !== undefined) {
                const rest = `f[${names.slots[names.of.get(p.rest)!]}]`;
                lines.push(`${rest} = rt_array_new(cx); // @${p.rest.name}`, `rt_slurp(cx, ${rest}, argc, argv, flat, ${n});`);
            }
        } else if (p.op === undefined) {
            lines.push(...copy);
        } else if (p.default === undefined) {
            // `$=`: an argument that may be left out, and names nothing.
        } else {
            const fallback = genWhole(p.default, p.pos.line, out, c => (slot === undefined ? [] : [`${slot} = ${c};`])).code;
            lines.push(`if (${given}) {`, ...indent(copy), '} else {', ...indent(fallback), '}');
        }
    }
    const last = s.body.at(-1);
    const before = last?.kind === 'do' ? s.body.slice(0, -1) : s.body;
    lines.push(...before.flatMap(t => genStmt(t, out)));
    if (last === undefined) {
        lines.push('if (want == RT_LIST) r = rt_absent();');
    } else if (last.kind === 'do' && listy(last.expr)) {
        lines.push('{', ...indent(genGiven(last.expr, last.pos.line, out, [])), '}');
    } else if (last.kind === 'do') {
        const whole = genWhole(last.expr, last.pos.line, out, c => [`r = ${c};`], 'pass');
        lines.push(...whole.vars, '{', ...indent(whole.code), '}');
    } else if (last.kind === 'call') {
        lines.push('r = rt_bool(1);');
    } else if (last.kind !== 'return') {
        lines.push(`if (want != RT_VOID) {`, `    cx->line = ${last.pos.line};`, `    rt_fault_sub(cx, ${name}, RT_NO_VALUE);`, '}');
    }
    const slots = Math.max(1, names.frames[fn]! + out.frame.temporaries);
    const slurpy = s.params.at(-1)?.slurpy === true;
    const least = s.params.filter(p => p.op === undefined && !p.slurpy).length;
    return [
        `${prototype(s)} {`,
        `    rt_value f[${slots}];`,
        '    rt_frame frame;',
        '    rt_value r = rt_undef();',
        '    rt_value *g RT_UNUSED = cx->shared;',
        // The count first, while the line is still the caller's.
        slurpy ? `    if (argc < ${least}) rt_fault_arguments(cx, ${name}, argc, ${least}, INT64_MAX);`
            : `    if (argc < ${least} || argc > ${s.params.length}) rt_fault_arguments(cx, ${name}, argc, ${least}, ${s.params.length});`,
        ...s.params.map((_, n) => `    rt_value *a${n} RT_UNUSED = argc > ${n} ? (flat != NULL ? &flat[${n}] : argv[${n}]) : NULL;`),
        `    rt_enter(cx, &frame, f, ${slots});`,
        ...indent(lines),
        'done: RT_UNUSED;',
        '    rt_leave(cx, &frame);',
        '    return r;',
        '}',
        '',
    ];
};

// Whether a declaration is one of the file's: a block's and a sub's have
// slots that are numbered after them.
const isFileSlot = (names: Resolution, id: number): boolean => names.fileIds.has(id);

const prototype = (s: Sub): string =>
    `static rt_value sub_${s.name}(rt_ctx *cx, int want RT_UNUSED, int64_t argc, rt_value **argv RT_UNUSED, rt_value *flat RT_UNUSED)`;

// `file` is the program's path as the driver was given it, which is the
// path perl is given too (D10): a fault names it.
export const generate = (program: Program, names: Resolution, file: string): string => {
    const out: Out = { strings: [], names, frame: { temporaries: 0 }, fn: 0, open: [], base: 0 };
    const subs = names.subs.flatMap((s, n) => genSub(s, n + 1, out.strings, names));
    const body = program.body.flatMap(s => genStmt(s, out));
    // A frame has a slot at least: C has no array of none.
    const slots = Math.max(1, names.frames[0]! + out.frame.temporaries);
    return [
        '#include "rt.h"',
        '',
        ...out.strings,
        ...(out.strings.length ? [''] : []),
        ...names.subs.map(s => `${prototype(s)};`),
        ...(names.subs.length ? [''] : []),
        ...subs,
        'static void curly_main(rt_ctx *cx) {',
        `    rt_value f[${slots}];`,
        '    rt_frame frame;',
        `    rt_enter(cx, &frame, f, ${slots});`,
        // The file's variables: undef before anything runs, a sub
        // included, and reached by the subs through the context (T134).
        ...names.names.flatMap((_, id) => (names.owner[id] === 0 && names.slots[id]! < names.file && isFileSlot(names, id)
            ? [`    f[${names.slots[id]}] = ${names.isArray[id] ? 'rt_array_new(cx)' : 'rt_undef()'};`] : [])),
        '    cx->shared = f;',
        ...indent(body),
        '    rt_leave(cx, &frame);',
        '}',
        '',
        'int main(void) {',
        `    return rt_run(curly_main, ${cString(file)});`,
        '}',
        '',
    ].join('\n');
};
