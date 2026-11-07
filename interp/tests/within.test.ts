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

test('a budget of n allows n operations; the next faults budget spent (D20, D22)', () => {
  assert.equal(run('(within 3 (+ (* 2 3) (- 10 4)))'), 12n);
  assert.equal(faultOf('(within 2 (+ (* 2 3) (- 10 4)))'), 'budget spent');
  assert.equal(run('(within 0 42)'), 42n);
  assert.equal(run('(within 1 (< 1 2))'), true);
});

test('an operation is charged after its operands, before its own checks (D22)', () => {
  assert.equal(faultOf('(within 1 (+ (/ 1 0) 2))'), 'division by zero');
  assert.equal(faultOf('(within 0 (/ 1 0))'), 'budget spent');
  assert.equal(faultOf('(within 1 (+ (* 2 3) (/ 1 0)))'), 'budget spent');
});

test('if, within and literals cost nothing, and an untaken branch is not charged (D21)', () => {
  assert.equal(run('(within 0 (if #true (within 0 7) (/ 1 0)))'), 7n);
  assert.equal(run('(within 2 (if (< 1 2) (+ 40 2) (+ (+ 1 1) (+ 1 1))))'), 42n);
});

test('** is one operation whatever its exponent (D21)', () => {
  assert.equal(run('(within 1 (** 1 4611686018427387903))'), 1n);
});

test('every operator is charged: seventeen operations in a budget of seventeen (D21)', () => {
  const body = `(bit/xor (** (bit/shr (bit/shl 3 4) 2) 2)
    (if (== (< 1 2) (>= 3 3))
        (if (!= (<= 5 4) (> 5 4))
            (+ (bit/and 12 10) (bit/or (- 7 (* 2 3)) (% (/ 17 2) 5)))
            0)
        0))`;
  assert.equal(run(`(within 17 ${body})`), 155n);
  assert.equal(faultOf(`(within 16 ${body})`), 'budget spent');
});

test('nested budgets: an inner one cannot give more than the outer has left (D23)', () => {
  assert.equal(faultOf('(within 1 (within 5 (+ (+ 1 2) 3)))'), 'budget spent');
  assert.equal(faultOf('(within 5 (within 1 (+ (+ 1 2) 3)))'), 'budget spent');
  assert.equal(run('(within 3 (+ (within 5 (+ (+ 1 2) 3)) 4))'), 10n);
  assert.equal(faultOf('(within 2 (+ (within 5 (+ (+ 1 2) 3)) 4))'), 'budget spent');
});

test('a budget is any expression, evaluated under the budgets around it (D24)', () => {
  assert.equal(run('(within 2 (within (+ 1 1) (* 3 4)))'), 12n);
  assert.equal(faultOf('(within 1 (within (+ 1 1) (* 3 4)))'), 'budget spent');
  assert.equal(faultOf('(within #true 1)'), 'not an integer');
  assert.equal(faultOf('(within -1 (/ 1 0))'), 'bad budget');
});

test('a within of the wrong number of parts is an error before running (D24)', () => {
  assert.throws(() => check(read('(within 5)')), (e: unknown) =>
    e instanceof CheckError && e.message === 'within takes 2 arguments, not 1');
});

test('outside every within nothing is counted, so a program with none runs as it did (D23)', () => {
  assert.equal(run('(+ (+ 1 2) (+ 3 4))'), 10n);
});
