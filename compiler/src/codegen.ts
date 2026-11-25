// The tree to C: straight-line, one statement per operation, each result
// in a temporary (D31), every runtime call taking the context first (D28).
// The C is linked with runtime/rt.c by the driver.
//
// A variable is a C local, and is never copied into a temporary: an
// operand that is the variable itself is read when its operator runs
// (D14). So an expression's C is either a value fixed when it was made (a
// temporary, a literal) or a place, and where an operator gives one of
// two operands (`||`, `? :`) its C is a pointer to whichever it gave.
import { NAMES, PRAGMAS, infixOp, prefixOp, stepOp } from './names.ts';
import type { Expr, If, Program, Stmt } from './ast.ts';
import type { Resolution } from './resolver.ts';

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
type Code = { vars: string[]; decls: string[]; lines: string[]; temps: number; strings: string[]; names: Resolution };

// An expression's C, and whether it has an address: a variable, a
// temporary, or what a pointer points at.
type C = { c: string; place: boolean };

const temp = (b: Code, call: string): C => {
    const t = `t${++b.temps}`;
    b.decls.push(`rt_value ${t} RT_UNUSED;`);
    b.lines.push(`${t} = ${call};`);
    return { c: t, place: true };
};

// A pointer to an expression's value, which is put in a temporary first
// if it has no address.
const pointTo = (b: Code, v: C): string => `&${v.place ? v.c : temp(b, v.c).c}`;

const variable = (b: Code, e: Expr): string => {
    if (e.kind !== 'var' && e.kind !== 'my') throw new Error('not a variable');
    const id = b.names.of.get(e);
    if (id === undefined) throw new Error(`$${e.name} was not resolved`);
    return `v${id}_${e.name}`;
};

// The C for an expression's value, once the statements appended to `b`
// have run. Operands are generated left before right, so that is the
// order they run in, and the first of two faults is the left one. Nothing
// that can fault is ever an argument of a call: C doesn't say which
// argument it would evaluate first.
const genExpr = (e: Expr, b: Code): C => {
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
    // `my $x`: an undef, in the C block the statement stands in.
    case 'my':
        b.vars.push(`rt_value ${variable(b, e)} RT_UNUSED = rt_undef();`);
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
        const operand = genExpr(e.operand, b);
        const rt = prefixOp(e.op)?.rt;
        // Unary plus is in the language and does nothing: what it is
        // given is what it gives, the variable itself included.
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
        b.lines.push(`${p} = ${pointTo(b, genExpr(e.then, b))};`, '} else {');
        b.lines.push(`${p} = ${pointTo(b, genExpr(e.else, b))};`, '}');
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
    case 'binary': {
        const op = infixOp(e.op);
        const left = genExpr(e.left, b);
        // `&&`, `||`, `//`: the value is the left operand, unless the test
        // says the right one is wanted, and only then is it worked out.
        if (op?.when !== undefined) {
            const p = `p${++b.temps}`;
            b.decls.push(`rt_value *${p} RT_UNUSED;`);
            b.lines.push(`${p} = ${pointTo(b, left)};`, `if (${op.when}(cx, *${p})) {`);
            b.lines.push(`${p} = ${pointTo(b, genExpr(e.right, b))};`, '}');
            return { c: `(*${p})`, place: true };
        }
        const right = genExpr(e.right, b);
        if (op?.rt === undefined) throw new Error(`no runtime function for ${e.op}`);
        return temp(b, `${op.rt}(cx, ${left.c}, ${right.c})`);
    }
    }
};

type Out = { strings: string[]; names: Resolution };

// The C of an expression that is a statement's or a test's, and what it
// is worth. A fault names the line its statement starts on (D34), a test's
// the line of its `if` or `elsif`: so the line is stored first.
// `vars` are the variables it declares, which belong to the C block the
// statement stands in.
const genWhole = (e: Expr, line: number, out: Out, use: (c: string) => string[]): { vars: string[]; code: string[] } => {
    const b: Code = { vars: [], decls: [], lines: [], temps: 0, strings: out.strings, names: out.names };
    const c = genExpr(e, b).c;
    return { vars: b.vars, code: [`cx->line = ${line};`, ...b.decls, ...b.lines, ...use(c)] };
};

const indent = (lines: string[]): string[] => lines.map(l => `    ${l}`);

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
        return ['{', ...indent(genWhole(s.args[0]!, s.pos.line, out, c => [`${name.rt}(cx, ${c});`]).code), '}'];
    }
    // The variables an expression statement declares are the enclosing
    // block's, and come before the C block its temporaries are in.
    case 'do': {
        const whole = genWhole(s.expr, s.pos.line, out, () => []);
        return [...whole.vars, '{', ...indent(whole.code), '}'];
    }
    case 'block': return ['{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}'];
    case 'if': return ['{', ...indent(genArms(s, 0, out)), '}'];
    }
};

// `file` is the program's path as the driver was given it, which is the
// path perl is given too (D10): a fault names it.
export const generate = (program: Program, names: Resolution, file: string): string => {
    const out: Out = { strings: [], names };
    const body = program.body.flatMap(s => genStmt(s, out));
    return [
        '#include "rt.h"',
        '',
        ...out.strings,
        ...(out.strings.length ? [''] : []),
        'static void curly_main(rt_ctx *cx) {',
        '    (void)cx;',
        ...indent(body),
        '}',
        '',
        'int main(void) {',
        `    return rt_run(curly_main, ${cString(file)});`,
        '}',
        '',
    ].join('\n');
};
