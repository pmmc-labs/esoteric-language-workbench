import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { check } from '../src/check.ts';
import { evaluate, show } from '../src/evaluate.ts';
import { CheckError } from '../src/errors.ts';

test('step 0: literals check and evaluate, and print as the language writes them', () => {
  check(read('42'));
  assert.equal(show(evaluate(read('42'))), '42');
  assert.equal(show(evaluate(read('-4611686018427387904'))), '-4611686018427387904');
  assert.equal(show(evaluate(read('#false'))), '#false');
});

test('a name or a list with no operator to name is an error before running', () => {
  assert.throws(() => check(read('foo')), (e: unknown) => e instanceof CheckError && e.message === 'unknown name foo');
  assert.throws(() => check(read('(foo 1 2)')), (e: unknown) =>
    e instanceof CheckError && e.message === 'unknown operator foo' && e.line === 1 && e.col === 2);
  assert.throws(() => check(read('()')), (e: unknown) => e instanceof CheckError && e.message === 'expected an operator');
  assert.throws(() => check(read('((1) 2)')), (e: unknown) =>
    e instanceof CheckError && e.message === 'expected an operator, not a list');
});
