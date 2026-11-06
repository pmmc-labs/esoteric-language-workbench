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

test('the C for a nested expression', () => {
    assert.match(compileProgram(read('(* (+ 1 2) -3)')), /rt_mul\(rt_add\(rt_int\(1LL\), rt_int\(2LL\)\), rt_int\(-3LL\)\)/);
});

test('a comparison takes two arguments (D12)', () => {
    fails('(< 1 2 3)', '< takes 2 arguments, not 3', 1, 1);
    fails('(== 1)', '== takes 2 arguments, not 1', 1, 1);
});

test('a bit operation takes two arguments, and bit/not is not one (D15)', () => {
    fails('(bit/shl 1)', 'bit/shl takes 2 arguments, not 1', 1, 1);
    fails('(bit/and 1 2 3)', 'bit/and takes 2 arguments, not 3', 1, 1);
    fails('(bit/not 1)', 'not an operator: bit/not', 1, 2);
});

test('a shift is its runtime function (D16)', () => {
    assert.match(compileProgram(read('(bit/shr -7 1)')), /rt_bit_shr\(rt_int\(-7LL\), rt_int\(1LL\)\)/);
});

test('** takes two arguments, its base first (D18)', () => {
    fails('(** 2)', '** takes 2 arguments, not 1', 1, 1);
    fails('(** 2 3 4)', '** takes 2 arguments, not 3', 1, 1);
    assert.match(compileProgram(read('(** 2 -1)')), /rt_pow\(rt_int\(2LL\), rt_int\(-1LL\)\)/);
});

test('if takes three parts, its test first (D13)', () => {
    fails('(if 1 2)', 'if takes 3 arguments, not 2', 1, 1);
    fails('(if)', 'if takes 3 arguments, not 0', 1, 1);
    fails('(+ 1 (if #true 2 3 4))', 'if takes 3 arguments, not 4', 1, 6);
    assert.match(compileProgram(read('(if (< 1 2) #true 0)')), /rt_test\(rt_lt\(rt_int\(1LL\), rt_int\(2LL\)\)\) \? RT_TRUE : rt_int\(0LL\)/);
});

test('the booleans are their own names, and nothing else is', () => {
    fails('#maybe', 'unknown name #maybe', 1, 1);
    assert.match(compileProgram(read('#false')), /return RT_FALSE;/);
});

test('a name the prototype of an object has is not an operator', () => {
    fails('(toString 1 2)', 'not an operator: toString', 1, 2);
});

// Step 5: budgets (D20 to D27).
test('within takes two parts, its budget first (D24)', () => {
    fails('(within)', 'within takes 2 arguments, not 0', 1, 1);
    fails('(within 5)', 'within takes 2 arguments, not 1', 1, 1);
    fails('(+ 1 (within 1 2 3))', 'within takes 2 arguments, not 3', 1, 6);
    fails('within', 'unknown name within', 1, 1);
});

test('two list operands go through temporaries, left first (D25, D26)', () => {
    assert.match(compileProgram(read('(+ (/ 1 0) (+ #true 1))')),
        /\((t\d+) = rt_div\(rt_int\(1LL\), rt_int\(0LL\)\), (t\d+) = rt_add\(RT_TRUE, rt_int\(1LL\)\), rt_add\(\1, \2\)\)/);
});

test('a within saves the limit and restores it around its body (D26)', () => {
    assert.match(compileProgram(read('(within 5 (+ 1 2))')),
        /\((b\d+) = rt_within\(rt_int\(5LL\)\), rt_within_end\(\1, rt_add\(rt_int\(1LL\), rt_int\(2LL\)\)\)\)/);
});
