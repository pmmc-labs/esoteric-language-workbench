import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { compileProgram } from '../src/codegen.ts';
import { CompileError } from '../src/errors.ts';

// D21's compile errors, each with its message and where it's reported.
// Each program puts the culprit somewhere other than 1:1, so a position
// that defaulted to the program's start would fail.
const refuses = (src: string, message: string, line: number, col: number) =>
    assert.throws(() => compileProgram(read(src)), (e: unknown) => {
        assert.ok(e instanceof CompileError, `not a CompileError: ${e}`);
        assert.deepEqual([e.message, e.line, e.col], [message, line, col]);
        return true;
    });

test('an operator takes exactly two operands, reported at the form', () => {
    refuses('\n  (+ 1)', '+ takes two operands', 2, 3);
    refuses('(+ 1 2 3)', '+ takes two operands', 1, 1);
    refuses('(* 2 (+ 1 2 3))', '+ takes two operands', 1, 6);
    refuses('(/ 1)', '/ takes two operands', 1, 1);
});

test('an unknown operator is reported at the form', () => {
    refuses('(foo 1 2)', 'unknown operator: foo', 1, 1);
    refuses('(+ 1 (foo 1 2))', 'unknown operator: foo', 1, 6);
});

test('a form must start with an operator', () => {
    refuses('()', 'a form must start with an operator', 1, 1);
    refuses('(- 1 ())', 'a form must start with an operator', 1, 6);
    refuses('\n(1 2)', 'a form must start with an operator', 2, 1);
});

test('a bare symbol is not a value, reported where it is', () => {
    refuses('(+ 1 x)', 'a symbol is not a value: x', 1, 6);
    refuses('  x', 'a symbol is not a value: x', 1, 3);
    // D22: a leading + isn't part of a literal.
    refuses('+5', 'a symbol is not a value: +5', 1, 1);
    refuses('(- +5 1)', 'a symbol is not a value: +5', 1, 4);
});

// D21: the whole tree is checked before anything runs, so the division
// by zero never gets the chance to fault.
test('a literal out of range is a compile error even after a fault', () => {
    refuses('(+ (/ 1 0) 4611686018427387904)', 'integer out of range', 1, 12);
});

// D21's left-to-right order: the first error in the text is the one
// reported.
test('the first error from the left is reported', () => {
    refuses('(+ x (foo 1 2))', 'a symbol is not a value: x', 1, 4);
    refuses('(+ (foo 1 2) x)', 'unknown operator: foo', 1, 4);
});
