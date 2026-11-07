import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { check } from '../src/check.ts';
import { evaluate } from '../src/evaluate.ts';
import { CheckError, Fault } from '../src/errors.ts';

const run = (text: string) => {
  const f = read(text);
  check(f);
  return evaluate(f);
};
const faultOf = (text: string) => {
  try {
    run(text);
  } catch (e) {
    if (e instanceof Fault) return e.message;
    throw e;
  }
  assert.fail(`no fault for ${text}`);
};
const errorOf = (text: string) => {
  try {
    run(text);
  } catch (e) {
    if (e instanceof CheckError) return e.message;
    throw e;
  }
  assert.fail(`no error for ${text}`);
};

test('the bit operations are two\'s complement of any width (D15)', () => {
  assert.equal(run('(bit/and -1 7)'), 7n);
  assert.equal(run('(bit/or -8 1)'), -7n);
  assert.equal(run('(bit/xor -1 0)'), -1n);
});

test('shifts: a times 2^n, and the right shift floors (D16)', () => {
  assert.equal(run('(bit/shl -1 62)'), -(2n ** 62n));
  assert.equal(run('(bit/shl 3 4)'), 48n);
  assert.equal(run('(bit/shr -7 1)'), -4n);
  assert.equal(run('(bit/shr 7 1)'), 3n);
  assert.equal(faultOf('(bit/shl 1 62)'), 'overflow');
});

test('a count outside 0 to 62 faults bad shift, before the range is looked at (D16, D32)', () => {
  assert.equal(faultOf('(bit/shl 1 63)'), 'bad shift');
  assert.equal(faultOf('(bit/shr 7 -1)'), 'bad shift');
});

test('an operand that is not an integer faults first, whatever the count (D32)', () => {
  assert.equal(faultOf('(bit/shl #true 1)'), 'not an integer');
  assert.equal(faultOf('(bit/shl #true 99)'), 'not an integer');
});

test('the arity of a bit operation is checked before running (D3)', () => {
  assert.equal(errorOf('(bit/and 1)'), 'bit/and takes 2 arguments, not 1');
});
