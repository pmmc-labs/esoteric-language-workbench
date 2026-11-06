// What to emit. A program is one expression: an integer, a boolean, an
// operator applied to expressions, an `if`, or a `within`. The output is C, a
// statement per operation in evaluation order (D21, D27), that computes it with the runtime's checked operations (overflow and division
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

// What compiling an expression gives: the C statements that compute it,
// and the C expression that is its value once they have run. `atom` is
// true when that expression is a literal or a temporary, so a parent can
// use it where it stands; otherwise it is a call, which the parent binds to
// a temporary of its own, in order (D27). `next` is the next free
// temporary's number, threaded through rather than kept in a variable.
type Out = { lines: string[]; expr: string; atom: boolean; next: number };

const indent = (lines: readonly string[]): string[] => lines.map((l) => `    ${l}`);

// Compile an operation's operands in order, each non-literal one into a
// temporary as soon as it is computed, so that a later operand's statements
// run after it (D21, D27). C would leave the order of a call's arguments to
// the compiler.
const compileOperands = (forms: readonly Form[], next: number): { lines: string[]; atoms: string[]; next: number } => {
    const lines: string[] = [];
    const atoms: string[] = [];
    for (const form of forms) {
        const out = compileExpr(form, next);
        lines.push(...out.lines);
        next = out.next;
        if (out.atom) atoms.push(out.expr);
        else {
            lines.push(`rt_value t${next} = ${out.expr};`);
            atoms.push(`t${next}`);
            next += 1;
        }
    }
    return { lines, atoms, next };
};

// `if` is a special form, not an operator: only the taken branch runs
// (D13), so the branches are statements of their own, and the value is
// whichever of them set the result's temporary.
const compileIf = (f: Form, args: readonly Form[], next: number): Out => {
    if (args.length !== 3) fail(f, `if takes 3 arguments, not ${args.length}`);
    const [test, then, otherwise] = args as [Form, Form, Form];
    const t = compileOperands([test], next);
    const result = `t${t.next}`;
    const a = compileBranch(then, result, t.next + 1);
    const b = compileBranch(otherwise, result, a.next);
    const lines = [
        ...t.lines,
        `rt_value ${result};`,
        'rt_charge();',
        `if (rt_test(${t.atoms[0]})) {`,
        ...indent(a.lines),
        '} else {',
        ...indent(b.lines),
        '}',
    ];
    return { lines, expr: result, atom: true, next: b.next };
};

// A branch: its statements, then its value stored in the result.
const compileBranch = (f: Form, result: string, next: number): { lines: string[]; next: number } => {
    const out = compileExpr(f, next);
    return { lines: [...out.lines, `${result} = ${out.expr};`], next: out.next };
};

// `(within n expr)` is a special form beside `if` (D22): the budget has to
// be set before `expr` runs. `n` is an integer literal of 0 or more, read
// from the source; the checks are in this order: the arity, the budget,
// then `expr`, whose errors are its own. The limit is restored after `expr`
// has been computed into a temporary, since the value must exist before the
// budget around it ends.
const compileWithin = (f: Form, args: readonly Form[], next: number): Out => {
    if (args.length !== 2) fail(f, `within takes 2 arguments, not ${args.length}`);
    const [budget, body] = args as [Form, Form];
    if (budget.kind !== 'int' || budget.value < 0n) return fail(budget, "within's budget must be a non-negative integer literal");
    if (budget.value > INT_MAX) return fail(budget, 'integer out of range');
    const saved = `t${next}`;
    const out = compileExpr(body, next + 1);
    const lines = [`uint64_t ${saved} = rt_within_enter(${budget.value}ULL);`, ...out.lines];
    let expr = out.expr;
    let n = out.next;
    if (!out.atom) {
        lines.push(`rt_value t${n} = ${out.expr};`);
        expr = `t${n}`;
        n += 1;
    }
    lines.push(`rt_within_leave(${saved});`);
    return { lines, expr, atom: true, next: n };
};

const compileExpr = (f: Form, next: number): Out => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) fail(f, 'integer out of range');
        return { lines: [], expr: `rt_int(${f.value}LL)`, atom: true, next };
    }
    if (f.kind === 'symbol') {
        const bool = BOOLS.get(f.name);
        return { lines: [], expr: bool ?? fail(f, `unknown name ${f.name}`), atom: true, next };
    }
    const [head, ...args] = f.items;
    if (head === undefined) return fail(f, 'empty call');
    if (head.kind === 'symbol' && head.name === 'if') return compileIf(f, args, next);
    if (head.kind === 'symbol' && head.name === 'within') return compileWithin(f, args, next);
    const name = head.kind === 'symbol' ? head.name : undefined;
    const op = name === undefined ? undefined : OPS.get(name);
    if (name === undefined || op === undefined) return fail(head, `not an operator: ${name ?? head.kind}`);
    if (args.length !== 2) return fail(f, `${name} takes 2 arguments, not ${args.length}`);
    const operands = compileOperands(args, next);
    return { lines: operands.lines, expr: `${op}(${operands.atoms[0]}, ${operands.atoms[1]})`, atom: false, next: operands.next };
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    const out = compileExpr(forms[0]!, 0);
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        ...indent(out.lines),
        `    return ${out.expr};`,
        '}',
        '',
    ].join('\n');
};
