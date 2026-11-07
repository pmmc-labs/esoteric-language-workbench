import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read, MAX_DEPTH } from '../src/reader.ts';
import { CheckError } from '../src/errors.ts';

// The error a text gives before running, or a failure if it reads.
function errorOf(text: string): CheckError {
  try {
    read(text);
  } catch (e) {
    if (e instanceof CheckError) return e;
    throw e;
  }
  assert.fail(`no error for ${JSON.stringify(text)}`);
}

test('an integer reads with its position, after comments and blank lines', () => {
  assert.deepEqual(read('  42'), { kind: 'int', value: 42n, line: 1, col: 3 });
  assert.deepEqual(read('; c\n\n  -7 ; x'), { kind: 'int', value: -7n, line: 3, col: 3 });
});

test('leading zeros and -0 read as the integer they name', () => {
  assert.deepEqual(read('007'), { kind: 'int', value: 7n, line: 1, col: 1 });
  assert.deepEqual(read('-0'), { kind: 'int', value: 0n, line: 1, col: 1 });
});

test('the 63-bit range is accepted at both ends and refused past them (D4)', () => {
  assert.equal(read('4611686018427387903').kind, 'int');
  assert.equal(read('-4611686018427387904').kind, 'int');
  for (const text of ['4611686018427387904', '-4611686018427387905']) {
    const e = errorOf(text);
    assert.equal(e.message, 'integer out of range');
    assert.deepEqual([e.line, e.col], [1, 1]);
  }
});

test('the booleans read, and any other # word is an unknown name', () => {
  assert.deepEqual(read('#true'), { kind: 'bool', value: true, line: 1, col: 1 });
  assert.equal(read('#false').kind, 'bool');
  assert.equal(errorOf('#foo').message, 'unknown name #foo');
});

test('a program with no expression, or two, is an error before running', () => {
  assert.equal(errorOf('').message, 'expected an expression');
  assert.deepEqual([errorOf('; only\n').line, errorOf('; only\n').col], [2, 1]);
  const e = errorOf('1 2');
  assert.equal(e.message, 'expected end of file after the expression');
  assert.deepEqual([e.line, e.col], [1, 3]);
});

test('unbalanced parentheses are reported at the paren at fault', () => {
  const open = errorOf('(1');
  assert.equal(open.message, 'unclosed (');
  assert.deepEqual([open.line, open.col], [1, 1]);
  const close = errorOf('1)');
  assert.equal(close.message, 'expected end of file after the expression');
  assert.deepEqual([close.line, close.col], [1, 2]);
  assert.equal(errorOf(')').message, 'unexpected )');
});

test('nesting to MAX_DEPTH reads; one level more is an error at that paren (D30)', () => {
  const ok = '('.repeat(MAX_DEPTH) + ')'.repeat(MAX_DEPTH);
  assert.equal(read(ok).kind, 'list');
  const over = '('.repeat(MAX_DEPTH + 1) + ')'.repeat(MAX_DEPTH + 1);
  const e = errorOf(over);
  assert.equal(e.message, `nested more than ${MAX_DEPTH} deep`);
  assert.deepEqual([e.line, e.col], [1, MAX_DEPTH + 1]);
});
