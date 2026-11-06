// What to emit. Step 1: a program is one expression, an integer or a form
// `(op a b)` over the four operators (D20), and the output is C that
// prints its value. The whole tree is checked before any C is written
// (D21), then flattened into statements: each operand into a temporary of
// its own, left to right, and then the operator's call on them, since C
// doesn't order a call's arguments (D27). Nothing is evaluated here; every
// fault is the runtime's (D28). Later steps emit assembly through a target
// interface; C is the quickest way to a binary on any machine.
import { CompileError } from './errors.ts';
import type { Form } from './sexp.ts';

const INT_MIN = -(2n ** 62n);
const INT_MAX = 2n ** 62n - 1n;

// Each operator and the runtime function that does it, checked.
const OPERATORS: readonly (readonly [string, string])[] = [
    ['+', 'rt_add'], ['-', 'rt_sub'], ['*', 'rt_mul'], ['/', 'rt_div'],
];
const runtimeName = (op: string): string | undefined => OPERATORS.find(([o]) => o === op)?.[1];

const refuse = (message: string, f: Form): CompileError => new CompileError(message, f.pos.line, f.pos.col);

// D21: the first error from the left, a form's own before its operands'.
const check = (f: Form): void => {
    if (f.kind === 'int') {
        if (f.value < INT_MIN || f.value > INT_MAX) throw refuse('integer out of range', f);
        return;
    }
    if (f.kind === 'symbol') throw refuse(`a symbol is not a value: ${f.name}`, f);
    const head = f.items[0];
    if (head === undefined || head.kind !== 'symbol') throw refuse('a form must start with an operator', f);
    if (runtimeName(head.name) === undefined) throw refuse(`unknown operator: ${head.name}`, f);
    if (f.items.length !== 3) throw refuse(`${head.name} takes two operands`, f);
    check(f.items[1]!);
    check(f.items[2]!);
};

// The statements that compute a form, and the temporary that holds its
// value. `next` numbers the next temporary, passed along rather than kept.
type Code = { stmts: readonly string[]; result: string; next: number };

const bind = (stmts: readonly string[], expr: string, next: number): Code =>
    ({ stmts: [...stmts, `rt_value t${next} = ${expr};`], result: `t${next}`, next: next + 1 });

// Only for a tree `check` has passed.
const generate = (f: Form, next: number): Code => {
    if (f.kind === 'int') return bind([], `rt_int(${f.value}LL)`, next);
    const [head, a, b] = f.kind === 'list' ? f.items : [];
    const fn = head?.kind === 'symbol' ? runtimeName(head.name) : undefined;
    if (fn === undefined || a === undefined || b === undefined) throw new Error(`generate: unchecked form at ${f.pos.line}:${f.pos.col}`);
    const left = generate(a, next);
    const right = generate(b, left.next);
    return bind([...left.stmts, ...right.stmts], `${fn}(${left.result}, ${right.result})`, right.next);
};

export const compileProgram = (forms: readonly Form[]): string => {
    if (forms.length !== 1) throw new CompileError('a program is one form', forms[0]?.pos.line ?? 1, forms[0]?.pos.col ?? 1);
    check(forms[0]!);
    const code = generate(forms[0]!, 0);
    return [
        '#include "rt.h"',
        'rt_value lang_main(void) {',
        ...code.stmts.map(s => `    ${s}`),
        `    return ${code.result};`,
        '}',
        '',
    ].join('\n');
};
