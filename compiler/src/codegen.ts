// What to emit. A program is checked as a whole (D15), then written as
// straight-line C: one statement per node, each result in a fresh
// temporary numbered in the order evaluated (D14). Later steps emit
// assembly through a target interface; C is the quickest way to a binary
// on any machine and is enough to start.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

const OPERATORS: readonly string[] = ['+', '-', '*', '/', '%'];

// The runtime function for each operator the code generator handles.
const RT_FUNCTION: Readonly<Record<string, string>> = { '+': 'rt_add', '-': 'rt_sub', '*': 'rt_mul' };

const err = (message: string, f: Form): CompileError => new CompileError(message, f.pos.line, f.pos.col);

// The checks of D15, over every form before any C is written, so that a
// malformed form after one that would fault at run time is still a
// compile error. Text order: a call's own errors (head, then operand
// count) before its operands', operands left to right.
const check = (f: Form): void => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) throw err('integer out of range', f);
        return;
    }
    if (f.kind === 'symbol') throw err(`can't compile ${f.kind} yet`, f);
    if (f.items.length === 0) throw err('empty form', f);
    const head = f.items[0]!;
    if (head.kind !== 'symbol') throw err('expected an operator', head);
    if (!OPERATORS.includes(head.name)) throw err(`unknown operator '${head.name}'`, head);
    const operands = f.items.slice(1);
    if (operands.length !== 2) throw err(`'${head.name}' takes 2 arguments, got ${operands.length}`, f);
    operands.forEach(check);
};

// C statements for a form, the name of the temporary holding its value,
// and the next free temporary number.
type Emitted = { code: string[]; result: string; next: number };

const emit = (f: Form, n: number): Emitted => {
    if (f.kind === 'int') return { code: [`rt_value t${n} = rt_int(${f.value}LL);`], result: `t${n}`, next: n + 1 };
    if (f.kind !== 'list') throw err(`can't compile ${f.kind} yet`, f);
    const head = f.items[0]!;
    const fn = head.kind === 'symbol' ? RT_FUNCTION[head.name] : undefined;
    if (fn === undefined) throw err(`can't compile ${f.kind} yet`, f);
    // Left operand's statements, then the right's, then the operation:
    // the order the temporaries are numbered in is the order of evaluation
    // (D12, D14).
    const left = emit(f.items[1]!, n);
    const right = emit(f.items[2]!, left.next);
    const t = `t${right.next}`;
    return {
        code: [...left.code, ...right.code, `rt_value ${t} = ${fn}(${left.result}, ${right.result});`],
        result: t,
        next: right.next + 1,
    };
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    check(forms[0]!);
    const { code, result } = emit(forms[0]!, 0);
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        ...code.map((s) => `    ${s}`),
        `    return ${result};`,
        '}',
        '',
    ].join('\n');
};
