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
import type { Expr, If, Program, Stmt, Sub } from './ast.ts';
import type { Resolution } from './resolver.ts';

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
type Code = { vars: string[]; decls: string[]; lines: string[]; temps: number; values: number; strings: string[]; names: Resolution; frame: Frame; fn: number; line: number };

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

const variable = (b: Code, e: Expr): string => {
    if (e.kind !== 'var' && e.kind !== 'my') throw new Error('not a variable');
    const id = b.names.of.get(e);
    const slot = id === undefined ? undefined : b.names.slots[id];
    if (id === undefined || slot === undefined) throw new Error(`$${e.name} was not resolved`);
    // Its own function's, or the file's, which a sub reaches through `g`.
    return b.names.owner[id] === b.fn ? `f[${slot}]` : `g[${slot}]`;
};

// Whether a declaration is a file variable: undef as the program starts,
// and nothing is stored by its `my` (T134).
const isFile = (b: Code, e: Expr): boolean => {
    const id = e.kind === 'var' || e.kind === 'my' ? b.names.of.get(e) : undefined;
    return id !== undefined && b.names.owner[id] === 0 && b.names.slots[id]! < b.names.file;
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
    // The right side first, and then the variable is read, if the
    // operator reads it, and set. The value is the variable.
    case 'assign': {
        const op = infixOp(e.op);
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
        const args = e.args.map(a => genExpr(a, b, 'list'));
        const least = called.params.filter(p => p.op === undefined).length;
        const most = called.params.length;
        if (args.length < least || args.length > most) {
            b.lines.push(`rt_fault_arguments(cx, ${cString(e.name)}, ${args.length}, ${least}, ${most});`);
            return { c: 'rt_undef()', place: false };
        }
        const where = called.params.map((_, n) => (args[n] === undefined ? 'NULL' : pointTo(b, args[n])));
        const result = temp(b, `sub_${e.name}(${['cx', WANT[want], ...where].join(', ')})`);
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
type Out = { strings: string[]; names: Resolution; frame: Frame; fn: number; sub?: Sub };

// The C of an expression that is a statement's or a test's, and what it
// is worth. A fault names the line its statement starts on (D34), a test's
// the line of its `if` or `elsif`: so the line is stored first.
// `vars` are the variables it declares, which belong to the C block the
// statement stands in.
const genWhole = (e: Expr, line: number, out: Out, use: (c: string) => string[], want: Want = 'scalar'): { vars: string[]; code: string[] } => {
    const b: Code = { vars: [], decls: [], lines: [], temps: 0, values: 0, strings: out.strings, names: out.names, frame: out.frame, fn: out.fn, line };
    const c = genExpr(e, b, want).c;
    return { vars: b.vars, code: [`cx->line = ${line};`, ...b.decls, ...b.lines, ...use(c)] };
};

const indent = (lines: string[]): string[] => lines.map(l => `    ${l}`);

// The expressions of one part of a `for`, left to right, in a C block of
// their own for their temporaries; nothing, for an empty part.
const genParts = (es: readonly Expr[], line: number, out: Out): { vars: string[]; code: string[] } => {
    const b: Code = { vars: [], decls: [], lines: [], temps: 0, values: 0, strings: out.strings, names: out.names, frame: out.frame, fn: out.fn, line };
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
        return ['{', ...indent(genWhole(s.args[0]!, s.pos.line, out, c => [`${name.rt}(cx, ${c});`], 'list').code), '}'];
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
            ...indent([...test.vars, ...test.code, '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', `next_${id}: RT_UNUSED;`]),
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
                ...indent([...(test.length ? ['{', ...indent(test), '}'] : []), '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', `next_${id}: RT_UNUSED;`, ...each.code]),
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
        return [`goto ${name.leaves ? 'last' : 'next'}_${id};`];
    }
    // A sub is a function of its own, written by `genSub`.
    case 'sub': return [];
    // The value into the C local that is returned, and out by the one
    // way there is. `return;` is undef to a scalar, and to a list it is
    // nothing at all, which the language can't yet say (D71).
    case 'return': {
        const name = cString(out.sub!.name);
        if (s.value === undefined) {
            return ['{', ...indent([`cx->line = ${s.pos.line};`, `if (want == RT_LIST) rt_fault_sub(cx, ${name}, RT_NOTHING);`, 'r = rt_undef();', 'goto done;']), '}'];
        }
        return ['{', ...indent(genWhole(s.value, s.pos.line, out, c => [`r = ${c};`, 'goto done;'], 'pass').code), '}'];
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
    const out: Out = { strings, names, frame: { temporaries: 0 }, fn, sub: s };
    const name = cString(s.name);
    const lines: string[] = [];
    for (const [n, p] of s.params.entries()) {
        const slot = p.my === undefined ? undefined : `f[${names.slots[names.of.get(p.my)!]}]`;
        const given = p.op === '//=' ? `a${n} != NULL && !rt_is_undef(cx, *a${n})`
            : p.op === '||=' ? `a${n} != NULL && rt_is_true(cx, *a${n})`
            : `a${n} != NULL`;
        const copy = slot === undefined ? [] : [`${slot} = *a${n}; // $${p.my!.name}`];
        if (p.op === undefined) {
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
        lines.push(`if (want == RT_LIST) {`, `    cx->line = ${s.pos.line};`, `    rt_fault_sub(cx, ${name}, RT_NOTHING);`, '}');
    } else if (last.kind === 'do') {
        const whole = genWhole(last.expr, last.pos.line, out, c => [`r = ${c};`], 'pass');
        lines.push(...whole.vars, '{', ...indent(whole.code), '}');
    } else if (last.kind === 'call') {
        lines.push('r = rt_bool(1);');
    } else if (last.kind !== 'return') {
        lines.push(`if (want != RT_VOID) {`, `    cx->line = ${last.pos.line};`, `    rt_fault_sub(cx, ${name}, RT_NO_VALUE);`, '}');
    }
    const slots = Math.max(1, names.frames[fn]! + out.frame.temporaries);
    return [
        `${prototype(s)} {`,
        `    rt_value f[${slots}];`,
        '    rt_frame frame;',
        '    rt_value r = rt_undef();',
        '    rt_value *g RT_UNUSED = cx->shared;',
        `    rt_enter(cx, &frame, f, ${slots});`,
        ...indent(lines),
        'done: RT_UNUSED;',
        '    rt_leave(cx, &frame);',
        '    return r;',
        '}',
        '',
    ];
};

const prototype = (s: Sub): string =>
    `static rt_value sub_${s.name}(${['rt_ctx *cx', 'int want RT_UNUSED', ...s.params.map((_, n) => `rt_value *a${n} RT_UNUSED`)].join(', ')})`;

// `file` is the program's path as the driver was given it, which is the
// path perl is given too (D10): a fault names it.
export const generate = (program: Program, names: Resolution, file: string): string => {
    const out: Out = { strings: [], names, frame: { temporaries: 0 }, fn: 0 };
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
        ...(names.file ? [`    for (int k = 0; k < ${names.file}; k++) f[k] = rt_undef();`] : []),
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
