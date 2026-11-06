// What to emit. A program is one expression: an integer, a boolean, an
// operator applied to expressions, or an `if`. The output is C that
// computes it with the runtime's checked operations (overflow and division
// by zero fault, D4, D5; a bad shift count or exponent faults, D16, D19; a non-integer or
// non-boolean faults, D11, D13, D14, D15). Later steps emit assembly
// through a target interface; C is the quickest way to a binary on any
// machine and is enough to start.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

// Each operator's runtime function (D3: two arguments each, no variadic
// arithmetic, so (- 1) is an error rather than a guess). The orderings
// and == and != are D12, the bit operations D15 and D16, `**` D18 and D19. A Map, not an
// object: a name like `toString` would be found on an object's prototype.
const OPS = new Map<string, string>([
    ['+', 'rt_add'], ['-', 'rt_sub'], ['*', 'rt_mul'], ['/', 'rt_div'], ['%', 'rt_mod'],
    ['<', 'rt_lt'], ['<=', 'rt_le'], ['>', 'rt_gt'], ['>=', 'rt_ge'], ['==', 'rt_eq'], ['!=', 'rt_ne'],
    ['bit/and', 'rt_bit_and'], ['bit/or', 'rt_bit_or'], ['bit/xor', 'rt_bit_xor'],
    ['bit/shl', 'rt_bit_shl'], ['bit/shr', 'rt_bit_shr'], ['**', 'rt_pow'],
]);

// The booleans, read as the symbols the reader makes of them (D11).
const BOOLS = new Map<string, string>([['#true', 'RT_TRUE'], ['#false', 'RT_FALSE']]);

const fail = (f: Form, message: string): never => { throw new CompileError(message, f.pos.line, f.pos.col); };

// `if` is a special form, not an operator: only the taken branch runs
// (D13), which the C conditional gives.
const compileIf = (f: Form, args: readonly Form[]): string => {
    if (args.length !== 3) fail(f, `if takes 3 arguments, not ${args.length}`);
    const [test, then, otherwise] = args as [Form, Form, Form];
    return `(rt_test(${compileExpr(test)}) ? ${compileExpr(then)} : ${compileExpr(otherwise)})`;
};

const compileExpr = (f: Form): string => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) fail(f, 'integer out of range');
        return `rt_int(${f.value}LL)`;
    }
    if (f.kind === 'symbol') {
        const bool = BOOLS.get(f.name);
        return bool ?? fail(f, `unknown name ${f.name}`);
    }
    const [head, ...args] = f.items;
    if (head === undefined) return fail(f, 'empty call');
    if (head.kind === 'symbol' && head.name === 'if') return compileIf(f, args);
    const name = head.kind === 'symbol' ? head.name : undefined;
    const op = name === undefined ? undefined : OPS.get(name);
    if (name === undefined || op === undefined) return fail(head, `not an operator: ${name ?? head.kind}`);
    if (args.length !== 2) return fail(f, `${name} takes 2 arguments, not ${args.length}`);
    return `${op}(${compileExpr(args[0]!)}, ${compileExpr(args[1]!)})`;
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
