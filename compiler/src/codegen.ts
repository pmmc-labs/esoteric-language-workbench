// The tree to C: straight-line, one statement per operation (D31), every
// runtime call taking the context first (D28). The C is linked with
// runtime/rt.c by the driver.
import { NAMES } from './names.ts';
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

// The checker has seen every literal: it is 0 to 2^63 - 1.
const genExpr = (e: Expr): string => `rt_int(INT64_C(${e.value}))`;

const genStmt = (s: Stmt): string[] => {
    // `use v5.42;` says which language this is; it does nothing at run time.
    if (s.kind === 'use') return [];
    const name = NAMES.get(s.name);
    if (name === undefined || name.kind !== 'builtin') throw new Error(`no runtime function for ${s.name}`);
    return [`    ${name.rt}(cx, ${s.args.map(genExpr).join(', ')});`];
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
