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

// D13's six messages, each with where it is reported. A program is read
// from text, so the positions are the reader's.
const refused = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => compileProgram(read(src)), (e: unknown) =>
        e instanceof CompileError && e.message === message && e.line === line && e.col === col);

test('an empty list is refused at its (', () => {
    refused('\n  (+ 1 ())', 'empty list', 2, 8);
});

test('a list that does not start with a symbol is refused at its first item', () => {
    refused('(1 2 3)', 'expected an operator', 1, 2);
    refused('((+ 1 2) 3)', 'expected an operator', 1, 2);
});

test('an unknown operator is refused at the symbol', () => {
    refused('\n(max 1 2)', 'unknown operator max', 2, 2);
});

test('an operator with other than two operands is refused at the list', () => {
    refused('(- 5)', '- takes 2 operands', 1, 1);
    refused('(+ 1\n  (* 1 2 3))', '* takes 2 operands', 2, 3);
    refused('(/)', '/ takes 2 operands', 1, 1);
});

test('a symbol where an operand or the program goes is refused at the symbol', () => {
    refused('x', 'unexpected symbol x', 1, 1);
    refused('(+ 1 +)', 'unexpected symbol +', 1, 6);
    refused('+5', 'unexpected symbol +5', 1, 1);
});

test('an integer out of range is refused wherever it is', () => {
    refused('(+ 1 (* 2 4611686018427387904))', 'integer out of range', 1, 11);
    refused('(+ -4611686018427387905 1)', 'integer out of range', 1, 4);
});

test('the shape and operator are checked before the operands', () => {
    refused('(+ 99999999999999999999)', '+ takes 2 operands', 1, 1);
    refused('(max 99999999999999999999 1)', 'unknown operator max', 1, 2);
    refused('(99999999999999999999 1)', 'expected an operator', 1, 2);
});

test('operands are checked left to right, and the first error is the one reported', () => {
    refused('(+ x 99999999999999999999)', 'unexpected symbol x', 1, 4);
    refused('(+ 99999999999999999999 x)', 'integer out of range', 1, 4);
    // an error in the second operand is reported though the first would
    // fault when run (D13, D12)
    refused('(+ (/ 1 0) (max 1 2))', 'unknown operator max', 1, 13);
});

test('operations at the ends of the range compile, and so do ones that fault when run', () => {
    // nothing is folded (D12): (/ 1 0) and an overflow are the runtime's
    for (const src of ['(+ 4611686018427387902 1)', '(/ 1 0)', '(+ 4611686018427387903 1)'])
        assert.match(compileProgram(read(src)), /lang_main/);
});

test('each operator calls its runtime function', () => {
    const c = compileProgram(read('(- (+ 1 2) (* (/ 3 4) (% 5 6)))'));
    for (const fn of ['rt_add', 'rt_sub', 'rt_mul', 'rt_div', 'rt_rem']) assert.ok(c.includes(`${fn}(`), fn);
});

test('operands run left to right: no call has another operation in its arguments', () => {
    const c = compileProgram(read('(+ (/ 1 0) (+ 4611686018427387903 1))'));
    assert.ok(!/rt_(add|sub|mul|div|rem)\([^;]*rt_(add|sub|mul|div|rem)\(/.test(c), c);
    // the left operation's statement comes before the right one's
    assert.ok(c.indexOf('rt_div(') < c.indexOf('rt_add(rt_int(4611686018427387903LL)'), c);
});
