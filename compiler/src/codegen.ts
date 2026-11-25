// The tree to C: straight-line, one statement per operation, each result
// in a temporary (D31), every runtime call taking the context first (D28).
// The C is linked with runtime/rt.c by the driver.
import { NAMES, PRAGMAS, infixOp, prefixOp } from './names.ts';
import type { Expr, Program, Stmt } from './ast.ts';

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

// The C statements of one source statement, and how many temporaries
// they have declared. `strings` is the whole program's: the string
// literals, each a constant at the top of the C file, in the order met.
type Block = { lines: string[]; temps: number; strings: string[] };

const temp = (b: Block, call: string): string => {
    const t = `t${++b.temps}`;
    b.lines.push(`rt_value ${t} = ${call};`);
    return t;
};

// The C for an expression's value: a literal, or the temporary that holds
// it once the statements appended to `b` have run. Operands are generated
// left before right, so that is the order they run in, and the first of
// two faults is the left one. Nothing that can fault is ever an argument
// of a call: C doesn't say which argument it would evaluate first.
const genExpr = (e: Expr, b: Block): string => {
    // The checker has seen every literal: it is 0 to 2^63 - 1.
    if (e.kind === 'int') return `rt_int(INT64_C(${e.value}))`;
    // A Num goes over as its 64 bits: no decimal is read twice.
    if (e.kind === 'num') return `rt_num_bits(UINT64_C(0x${new BigUint64Array(new Float64Array([e.value]).buffer)[0]!.toString(16)}))`;
    // A string literal is a constant the program never allocates: its
    // bytes as UTF-8, how many there are, and how many characters.
    if (e.kind === 'str') {
        const bytes = new TextEncoder().encode(e.value).length;
        b.strings.push(`static const rt_str s${b.strings.length + 1} = { ${bytes}, ${[...e.value].length}, ${cString(e.value)} };`);
        return `rt_string(&s${b.strings.length})`;
    }
    if (e.kind === 'constant') {
        const name = NAMES.get(e.name);
        if (name?.kind !== 'constant') throw new Error(`no value for ${e.name}`);
        return name.c;
    }
    // One branch is worked out, and the other is C that doesn't run: so
    // a fault in it doesn't happen (D49). The value is a temporary set in
    // whichever block runs.
    if (e.kind === 'ternary') {
        const test = genExpr(e.test, b);
        const result = temp(b, 'rt_undef()');
        b.lines.push(`if (rt_is_true(cx, ${test})) {`);
        b.lines.push(`${result} = ${genExpr(e.then, b)};`, '} else {');
        b.lines.push(`${result} = ${genExpr(e.else, b)};`, '}');
        return result;
    }
    if (e.kind === 'apply') {
        // Arguments left before right, each in a temporary or a literal
        // by the time the call is made.
        const args = e.args.map(a => genExpr(a, b));
        const name = NAMES.get(e.name);
        const rt = name?.kind === 'unary' ? name.rt : name?.kind === 'function' ? name.rt[e.args.length - name.min] : undefined;
        if (rt === undefined) throw new Error(`no runtime function for ${e.name}`);
        return temp(b, `${rt}(${['cx', ...args].join(', ')})`);
    }
    if (e.kind === 'unary') {
        const operand = genExpr(e.operand, b);
        const rt = prefixOp(e.op)?.rt;
        // Unary plus is in the language and does nothing.
        return rt === undefined ? operand : temp(b, `${rt}(cx, ${operand})`);
    }
    const left = genExpr(e.left, b);
    // `&&`, `||`, `//`: the value is the left operand, unless the test
    // says the right one is wanted, and only then is it worked out.
    const when = infixOp(e.op)?.when;
    if (when !== undefined) {
        const result = temp(b, left);
        b.lines.push(`if (${when}(cx, ${result})) {`);
        b.lines.push(`${result} = ${genExpr(e.right, b)};`, '}');
        return result;
    }
    const right = genExpr(e.right, b);
    const rt = infixOp(e.op)?.rt;
    if (rt === undefined) throw new Error(`no runtime function for ${e.op}`);
    return temp(b, `${rt}(cx, ${left}, ${right})`);
};

const genStmt = (s: Stmt, strings: string[]): string[] => {
    // `use v5.42;` says which language this is; it does nothing at run time.
    if (s.kind === 'use') return [];
    // A pragma is the compiler's business, unless the table gives it
    // something to do as the program starts.
    if (s.kind === 'pragma') {
        const rt = PRAGMAS.get(s.name)?.rt;
        return rt === undefined ? [] : [`    ${rt}(cx);`];
    }
    const name = NAMES.get(s.name);
    if (name === undefined || name.kind !== 'statement') throw new Error(`no runtime function for ${s.name}`);
    const b: Block = { lines: [], temps: 0, strings };
    const args = s.args.map(a => genExpr(a, b));
    b.lines.push(`${name.rt}(cx, ${args.join(', ')});`);
    // A fault names the line its statement starts on (D34). A block of
    // its own keeps each statement's temporaries out of the next one's
    // way: a C compiler is slow over ten thousand locals in one scope.
    return [
        `    cx->line = ${s.pos.line};`,
        ...(b.temps === 0 ? b.lines.map(l => `    ${l}`) : ['    {', ...b.lines.map(l => `        ${l}`), '    }']),
    ];
};

// `file` is the program's path as the driver was given it, which is the
// path perl is given too (D10): a fault names it.
export const generate = (program: Program, file: string): string => {
    const strings: string[] = [];
    const body = program.body.flatMap(s => genStmt(s, strings));
    return [
        '#include "rt.h"',
        '',
        ...strings,
        ...(strings.length ? [''] : []),
        'static void curly_main(rt_ctx *cx) {',
        '    (void)cx;',
        ...body,
        '}',
        '',
        'int main(void) {',
        `    return rt_run(curly_main, ${cString(file)});`,
        '}',
        '',
    ].join('\n');
};
