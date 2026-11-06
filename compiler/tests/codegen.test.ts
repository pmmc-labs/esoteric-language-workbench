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
