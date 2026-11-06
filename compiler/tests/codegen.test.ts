import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { compileProgram } from '../src/codegen.ts';
import { CompileError } from '../src/errors.ts';

// A compile error can't be a golden test (t/run.sh calls a failed
// compile a failure), so the messages are checked here.
test('an integer past 63 bits is refused where it is', () => {
    assert.throws(() => compileProgram(read('\n 4611686018427387904')), (e: unknown) =>
        e instanceof CompileError && e.message === 'integer out of range' && e.line === 2 && e.col === 2);
});

test('a program is one form', () => {
    assert.throws(() => compileProgram(read('1 2')), /one form/);
});

// D15: each malformed form, with its message and where it is reported.
// The expected values come from the decision, not from running the
// compiler.
const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => compileProgram(read(src)), (e: unknown) =>
        e instanceof CompileError && e.message === message && e.line === line && e.col === col);

test('an empty form is reported at its (', () => refused('\n  ()', 'empty form', 2, 3));

test('a head that is not a symbol is reported at the head', () => {
    refused('(1 2)', 'expected an operator', 1, 2);
    refused('( (+ 1 2) 3)', 'expected an operator', 1, 3);
});

test('an unknown operator is reported at the head', () => refused('\n (foo 1 2)', "unknown operator 'foo'", 2, 3));

test('an operand count other than two is reported at the call', () => {
    refused('(+ 1)', "'+' takes 2 arguments, got 1", 1, 1);
    refused(' (+ 1 2 3)', "'+' takes 2 arguments, got 3", 1, 2);
    refused('(%)', "'%' takes 2 arguments, got 0", 1, 1);
});

test('a symbol as a program or an operand is reported at the symbol', () => {
    refused('\n  x', "can't compile symbol yet", 2, 3);
    refused('+', "can't compile symbol yet", 1, 1);
    refused('(+ 1 +)', "can't compile symbol yet", 1, 6);
});

test('an integer past 63 bits as an operand is reported at the integer', () =>
    refused('(- 1 -4611686018427387905)', 'integer out of range', 1, 6));

test('the outer form\'s error comes before the inner one\'s', () => {
    refused('(foo (bar 1 2))', "unknown operator 'foo'", 1, 2);
    refused('(+ (bar 1 2))', "'+' takes 2 arguments, got 1", 1, 1);
    refused('(+ x (bar 1 2) 3)', "'+' takes 2 arguments, got 3", 1, 1);
});

test('left comes before right', () => {
    refused('(+ (foo) (bar))', "unknown operator 'foo'", 1, 5);
    refused('(+ x (foo))', "can't compile symbol yet", 1, 4);
});

test('a malformed form after an operand that would fault is still a compile error', () => {
    refused('(+ (/ 1 0) (foo))', "unknown operator 'foo'", 1, 13);
    refused('(+ (* 4611686018427387903 4611686018427387903) x)', "can't compile symbol yet", 1, 48);
});

// D14: one statement per node, a temporary each, numbered in the order
// evaluated; the last one is returned. The statements are written out
// from the decision's own example.
test('the C is straight-line, a temporary per node in evaluation order', () => {
    const c = compileProgram(read('(+ (* 2 3) 4)'));
    const lines = c.split('\n').map((l) => l.trim());
    const at = (s: string) => lines.findIndex((l) => l.endsWith(s));
    const order = ['t0 = rt_int(2LL);', 't1 = rt_int(3LL);', 't2 = rt_mul(t0, t1);', 't3 = rt_int(4LL);', 't4 = rt_add(t2, t3);', 'return t4;'].map(at);
    assert.ok(order.every((i) => i >= 0), c);
    assert.deepEqual(order, [...order].sort((a, b) => a - b));
    assert.ok(!/rt_\w+\([^)]*rt_\w+\(/.test(c.replace(/rt_int\(/g, 'i(')), 'no nested calls');
});
