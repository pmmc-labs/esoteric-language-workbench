// What to emit. A program is one expression: an integer, or an operator
// applied to expressions. The output is C that computes it with the
// runtime's checked operations (overflow and division by zero fault,
// D4, D5). Later steps emit assembly through a target interface; C is
// the quickest way to a binary on any machine and is enough to start.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

// Each operator's runtime function and how many arguments it takes (D3:
// two, no variadic arithmetic, so (- 1) is an error rather than a guess).
// The comparisons give a boolean (D12); the runtime checks the types.
const OPS: Record<string, string> = {
    '+': 'rt_add', '-': 'rt_sub', '*': 'rt_mul', '/': 'rt_div', '%': 'rt_mod',
    '<': 'rt_lt', '<=': 'rt_le', '>': 'rt_gt', '>=': 'rt_ge', '==': 'rt_eq', '!=': 'rt_ne',
};

// The two booleans are names the reader gives as symbols (D11).
const CONSTANTS: Record<string, string> = { '#true': 'RT_TRUE', '#false': 'RT_FALSE' };

const fail = (f: Form, message: string): never => { throw new CompileError(message, f.pos.line, f.pos.col); };

const compileExpr = (f: Form): string => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) fail(f, 'integer out of range');
        return `rt_int(${f.value}LL)`;
    }
    if (f.kind === 'symbol') {
        if (f.name in CONSTANTS) return CONSTANTS[f.name]!;
        return fail(f, `unknown name ${f.name}`);
    }
    const [head, ...args] = f.items;
    if (head === undefined) return fail(f, 'empty call');
    // `if` is a special form, not an operator: only the taken branch runs (D13).
    if (head.kind === 'symbol' && head.name === 'if') {
        if (args.length !== 3) fail(f, `if takes 3 arguments, not ${args.length}`);
        return `(rt_truth(${compileExpr(args[0]!)}) ? (${compileExpr(args[1]!)}) : (${compileExpr(args[2]!)}))`;
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
