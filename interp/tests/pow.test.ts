import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { check } from '../src/check.ts';
import { evaluate } from '../src/evaluate.ts';
import { Fault } from '../src/errors.ts';

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

test('a to the power b, and a ** 0 is 1 for every a, 0 ** 0 too (D18, D19)', () => {
  assert.equal(run('(** 2 10)'), 1024n);
  assert.equal(run('(** -3 3)'), -27n);
  assert.equal(run('(** 0 0)'), 1n);
  assert.equal(run('(** -5 0)'), 1n);
  assert.equal(run('(** 0 5)'), 0n);
});

test('a negative exponent faults bad exponent, even where the answer would fit (D19)', () => {
  assert.equal(faultOf('(** 2 -1)'), 'bad exponent');
  assert.equal(faultOf('(** 1 -1)'), 'bad exponent');
  assert.equal(faultOf('(** 0 -1)'), 'bad exponent');
});

test('a result past the range faults overflow, and a huge exponent is quick (D4, D19)', () => {
  assert.equal(faultOf('(** 2 62)'), 'overflow');
  assert.equal(faultOf('(** 2 4611686018427387903)'), 'overflow');
  assert.equal(run('(** 1 4611686018427387903)'), 1n);
  assert.equal(run('(** -1 4611686018427387903)'), -1n);
  assert.equal(run('(** -1 4611686018427387902)'), 1n);
  assert.equal(run('(** 0 4611686018427387903)'), 0n);
});

test('a boolean as either argument is not an integer (D11)', () => {
  assert.equal(faultOf('(** #true 2)'), 'not an integer');
});
