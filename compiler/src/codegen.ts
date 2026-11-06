// What to emit. A program is one expression: an integer, or (op a b) with
// op one of + - * / % (D8). The output is C: the whole program is checked
// first (D13), then compiled to straight-line code, one statement per
// operation, so the operands run left to right whatever the C compiler
// does with a call's arguments (D11). Later steps emit assembly through a
// target interface; C is the quickest way to a binary on any machine.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

// The five operators and the runtime function each calls.
const OPERATIONS: Readonly<Record<string, string>> = {
    '+': 'rt_add', '-': 'rt_sub', '*': 'rt_mul', '/': 'rt_div', '%': 'rt_rem',
};
const isOperator = (name: string) => Object.hasOwn(OPERATIONS, name);

const fail = (message: string, f: Form): never => {
    throw new CompileError(message, f.pos.line, f.pos.col);
};

// D13: a list's shape and operator before its operands, the operands left
// to right, and the first error is the one reported.
const check = (f: Form): void => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) fail('integer out of range', f);
    } else if (f.kind === 'symbol') {
        fail(`unexpected symbol ${f.name}`, f);
    } else {
        const op = f.items[0];
        if (op === undefined) fail('empty list', f);
        else if (op.kind !== 'symbol') fail('expected an operator', op);
        else if (!isOperator(op.name)) fail(`unknown operator ${op.name}`, op);
        else if (f.items.length !== 3) fail(`${op.name} takes 2 operands`, f);
        f.items.slice(1).forEach(check);
    }
};

// What compiling an expression gives: the statements to run first, the C
// expression for its value (a temporary, or for an integer the literal,
// neither of which has an effect), and the next unused temporary's number.
type Compiled = { stmts: readonly string[]; value: string; next: number };

// Assumes `check` passed, so a symbol or a malformed list can't be here.
const compileExpr = (f: Form, next: number): Compiled => {
    if (f.kind === 'int') return { stmts: [], value: `rt_int(${f.value}LL)`, next };
    const op = f.kind === 'list' ? f.items[0] : undefined;
    if (op?.kind !== 'symbol' || f.kind !== 'list') throw new Error('compileExpr: not checked');
    const left = compileExpr(f.items[1]!, next);
    const right = compileExpr(f.items[2]!, left.next);
    const t = `t${right.next}`;
    return {
        stmts: [...left.stmts, ...right.stmts, `rt_value ${t} = ${OPERATIONS[op.name]}(${left.value}, ${right.value});`],
        value: t,
        next: right.next + 1,
    };
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    check(forms[0]!);
    const body = compileExpr(forms[0]!, 0);
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        ...body.stmts.map(s => `    ${s}`),
        `    return ${body.value};`,
        '}',
        '',
    ].join('\n');
};
