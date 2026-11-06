import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { compileProgram } from '../src/codegen.ts';
import { CompileError } from '../src/errors.ts';

// A compile error can't be a golden test (t/run.sh calls a failed
// compile a failure, D7), so the messages are checked here.
const fails = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => compileProgram(read(src)), (e: unknown) =>
        e instanceof CompileError && e.message === message && e.line === line && e.col === col, `${src}: ${message} at ${line}:${col}`);

test('an integer past 63 bits is refused where it is', () => {
    fails('\n 4611686018427387904', 'integer out of range', 2, 2);
});

test('a program is one form', () => {
    fails('1 2', 'a program is one form', 1, 1);
});

test('operators take two arguments (D3)', () => {
    fails('(+ 1 2 3)', '+ takes 2 arguments, not 3', 1, 1);
    fails('(- 1)', '- takes 2 arguments, not 1', 1, 1);
});

test('what is not an operator is refused at its position', () => {
    fails('(+ 1 (f 2 3))', 'not an operator: f', 1, 7);
    fails('x', 'unknown name x', 1, 1);
    fails('()', 'empty call', 1, 1);
    fails('((+ 1 2) 3 4)', 'not an operator: list', 1, 2);
});

test('if takes three parts (D13)', () => {
    fails('(if #true 1)', 'if takes 3 arguments, not 2', 1, 1);
    fails('(if)', 'if takes 3 arguments, not 0', 1, 1);
});

test('the comparisons take two arguments (D12)', () => {
    fails('(< 1)', '< takes 2 arguments, not 1', 1, 1);
    fails('(== 1 2 3)', '== takes 2 arguments, not 3', 1, 1);
});

test('the C for an if is a conditional, so only the taken branch runs', () => {
    assert.match(compileProgram(read('(if #true 1 (/ 1 0))')), /rt_truth\(rt_bool\(1\)\) \? rt_int\(1LL\) : rt_div\(rt_int\(1LL\), rt_int\(0LL\)\)/);
});

test('the C for a nested expression', () => {
    assert.match(compileProgram(read('(* (+ 1 2) -3)')), /rt_mul\(rt_add\(rt_int\(1LL\), rt_int\(2LL\)\), rt_int\(-3LL\)\)/);
});
