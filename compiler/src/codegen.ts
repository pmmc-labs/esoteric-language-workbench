// What to emit. Step 0: a program is one integer, and the output is C that
// prints it. Later steps emit assembly through a target interface; C is
// the quickest way to a binary on any machine and is enough to start.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

const compileExpr = (f: Form): string => {
    if (f.kind !== 'int') throw new CompileError(`can't compile ${f.kind} yet`, f.pos.line, f.pos.col);
    if (f.value < INT_MIN || f.value > INT_MAX) throw new CompileError('integer out of range', f.pos.line, f.pos.col);
    return `rt_int(${f.value}LL)`;
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        `    return ${compileExpr(forms[0])};`,
        '}',
        '',
    ].join('\n');
};
