// What to emit. A program is one expression: an integer, a boolean, or an
// operator applied to expressions. The output is C that computes it with
// the runtime's checked operations (overflow and division by zero fault,
// D4, D5). Later steps emit assembly through a target interface; C is
// the quickest way to a binary on any machine and is enough to start.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

// Each operator's runtime function and how many arguments it takes (D3:
// two, no variadic arithmetic, so (- 1) is an error rather than a guess).
// The comparisons (D12) give a boolean; the orderings take two integers,
// == and != take any two values.
const OPS: Record<string, string> = {
    '+': 'rt_add', '-': 'rt_sub', '*': 'rt_mul', '/': 'rt_div', '%': 'rt_mod',
    '<': 'rt_lt', '<=': 'rt_le', '>': 'rt_gt', '>=': 'rt_ge', '==': 'rt_eq', '!=': 'rt_ne',
};

const fail = (f: Form, message: string): never => { throw new CompileError(message, f.pos.line, f.pos.col); };

const compileExpr = (f: Form): string => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) fail(f, 'integer out of range');
        return `rt_int(${f.value}LL)`;
    }
    if (f.kind === 'symbol') {
        // #true and #false are booleans (D11, D14); the reader makes them
        // symbols, and the meaning is here, so (+ #true 1) compiles and
        // faults at run time, not at compile.
        if (f.name === '#true') return 'rt_bool(1)';
        if (f.name === '#false') return 'rt_bool(0)';
        return fail(f, `unknown name ${f.name}`);
    }
    const [head, ...args] = f.items;
    if (head === undefined) return fail(f, 'empty call');
    // if is a special form, not an operator (D13): only the taken branch
    // runs, so C's ?: does the selection and the test is checked at run
    // time. The branches are parenthesised, since each may itself be a ?:
    if (head.kind === 'symbol' && head.name === 'if') {
        if (args.length !== 3) return fail(f, `if takes 3 arguments, not ${args.length}`);
        return `rt_if_test(${compileExpr(args[0]!)}) ? (${compileExpr(args[1]!)}) : (${compileExpr(args[2]!)})`;
    }
    if (head.kind !== 'symbol' || !(head.name in OPS)) return fail(head, `not an operator: ${head.kind === 'symbol' ? head.name : head.kind}`);
    if (args.length !== 2) return fail(f, `${head.name} takes 2 arguments, not ${args.length}`);
    return `${OPS[head.name]}(${compileExpr(args[0]!)}, ${compileExpr(args[1]!)})`;
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        `    return ${compileExpr(forms[0]!)};`,
        '}',
        '',
    ].join('\n');
};
