// What to emit. A program is one expression: an integer, a boolean, an
// operator applied to expressions, an `if`, or a `within`. The output is C that
// computes it with the runtime's checked operations (overflow and division
// by zero fault, D4, D5; a spent budget faults, D22; a bad shift count or exponent faults, D16, D19; a non-integer or
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

// The temporaries a program's C declares at the top of lang_main (D26):
// `rt_value` for the operands of an operator whose two operands are both
// lists, `int64_t` for the limit a `within` saves (D27). Numbered per
// program, one name per use, from a counter made by compileProgram and
// passed down; module state would leak between the unit tests' programs.
type Temps = { values: number; limits: number };

// `if` is a special form, not an operator: only the taken branch runs
// (D13), which the C conditional gives, test first.
const compileIf = (f: Form, args: readonly Form[], temps: Temps): string => {
    if (args.length !== 3) fail(f, `if takes 3 arguments, not ${args.length}`);
    const [test, then, otherwise] = args as [Form, Form, Form];
    return `(rt_test(${compileExpr(test, temps)}) ? ${compileExpr(then, temps)} : ${compileExpr(otherwise, temps)})`;
};

// `within` is a special form too: its budget must be in force before its
// body runs (D24), which an operator's operands, evaluated before the
// operator is applied, can't do. The comma operator sequences them (D26).
const compileWithin = (f: Form, args: readonly Form[], temps: Temps): string => {
    if (args.length !== 2) fail(f, `within takes 2 arguments, not ${args.length}`);
    const b = `b${temps.limits++}`;
    const budget = compileExpr(args[0]!, temps);
    return `(${b} = rt_within(${budget}), rt_within_end(${b}, ${compileExpr(args[1]!, temps)}))`;
};

// C doesn't order a call's arguments, so two operands that can fault or
// charge are never two arguments of one call (D25, D26). With an atom on
// either side there is nothing to order: an integer or a boolean has no
// effect and can't fault.
const compileOperator = (op: string, left: Form, right: Form, temps: Temps): string => {
    if (left.kind !== 'list' || right.kind !== 'list') return `${op}(${compileExpr(left, temps)}, ${compileExpr(right, temps)})`;
    const l = `t${temps.values++}`;
    const r = `t${temps.values++}`;
    return `(${l} = ${compileExpr(left, temps)}, ${r} = ${compileExpr(right, temps)}, ${op}(${l}, ${r}))`;
};

const compileExpr = (f: Form, temps: Temps): string => {
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
    if (head.kind === 'symbol' && head.name === 'if') return compileIf(f, args, temps);
    if (head.kind === 'symbol' && head.name === 'within') return compileWithin(f, args, temps);
    const name = head.kind === 'symbol' ? head.name : undefined;
    const op = name === undefined ? undefined : OPS.get(name);
    if (name === undefined || op === undefined) return fail(head, `not an operator: ${name ?? head.kind}`);
    if (args.length !== 2) return fail(f, `${name} takes 2 arguments, not ${args.length}`);
    return compileOperator(op, args[0]!, args[1]!, temps);
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    const temps: Temps = { values: 0, limits: 0 };
    const body = compileExpr(forms[0]!, temps);
    const names = (prefix: string, n: number) => Array.from({ length: n }, (_, i) => `${prefix}${i}`).join(', ');
    const declarations = [
        ...(temps.values > 0 ? [`    rt_value ${names('t', temps.values)};`] : []),
        ...(temps.limits > 0 ? [`    int64_t ${names('b', temps.limits)};`] : []),
    ];
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        ...declarations,
        `    return ${body};`,
        '}',
        '',
    ].join('\n');
};
