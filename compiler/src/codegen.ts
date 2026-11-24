// The tree to C: straight-line, one statement per operation, each result
// in a temporary (D31), every runtime call taking the context first (D28).
// The C is linked with runtime/rt.c by the driver.
import { NAMES, infixOp, prefixOp } from './names.ts';
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
// they have declared.
type Block = { lines: string[]; temps: number };

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
    if (e.kind === 'unary') {
        const operand = genExpr(e.operand, b);
        const rt = prefixOp(e.op)?.rt;
        // Unary plus is in the language and does nothing.
        return rt === undefined ? operand : temp(b, `${rt}(cx, ${operand})`);
    }
    const left = genExpr(e.left, b);
    const right = genExpr(e.right, b);
    const rt = infixOp(e.op)?.rt;
    if (rt === undefined) throw new Error(`no runtime function for ${e.op}`);
    return temp(b, `${rt}(cx, ${left}, ${right})`);
};

const genStmt = (s: Stmt): string[] => {
    // `use v5.42;` says which language this is; it does nothing at run time.
    if (s.kind === 'use') return [];
    const name = NAMES.get(s.name);
    if (name === undefined || name.kind !== 'builtin') throw new Error(`no runtime function for ${s.name}`);
    const b: Block = { lines: [], temps: 0 };
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
export const generate = (program: Program, file: string): string => [
    '#include "rt.h"',
    '',
    'static void curly_main(rt_ctx *cx) {',
    '    (void)cx;',
    ...program.body.flatMap(genStmt),
    '}',
    '',
    'int main(void) {',
    `    return rt_run(curly_main, ${cString(file)});`,
    '}',
    '',
].join('\n');
