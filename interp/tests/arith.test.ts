import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { check } from '../src/check.ts';
import { evaluate } from '../src/evaluate.ts';
import { CheckError, Fault } from '../src/errors.ts';

// Read, check and evaluate a text the way the driver does.
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

test('the five operators, with D5\'s rounding and sign', () => {
  assert.equal(run('(+ 6 7)'), 13n);
  assert.equal(run('(- 1 2)'), -1n);
  assert.equal(run('(* -3 4)'), -12n);
  assert.equal(run('(/ -7 2)'), -3n);
  assert.equal(run('(% -7 2)'), -1n);
  assert.equal(run('(/ 7 -2)'), -3n);
  assert.equal(run('(% 7 -2)'), 1n);
  assert.equal(run('(+ (* 6 7) (- 10 (/ 7 2)))'), 49n);
});

test('the range is 63 bits at both ends: an edge value is fine, one past it faults (D4)', () => {
  assert.equal(run('(- 4611686018427387903 0)'), 4611686018427387903n);
  assert.equal(run('(+ -4611686018427387904 0)'), -4611686018427387904n);
  assert.equal(faultOf('(+ 4611686018427387903 1)'), 'overflow');
  assert.equal(faultOf('(- -4611686018427387904 1)'), 'overflow');
  assert.equal(faultOf('(* 3037000500 3037000500)'), 'overflow');
  assert.equal(faultOf('(/ -4611686018427387904 -1)'), 'overflow');
});

test('a zero divisor faults, for / and %', () => {
  assert.equal(faultOf('(/ 1 0)'), 'division by zero');
  assert.equal(faultOf('(% 5 0)'), 'division by zero');
});

test('an arithmetic operator on a boolean faults, and the left operand goes first (D25, D32)', () => {
  assert.equal(faultOf('(+ #true 1)'), 'not an integer');
  assert.equal(faultOf('(/ #true 0)'), 'not an integer');
  assert.equal(faultOf('(+ (/ 1 0) (+ #true 1))'), 'division by zero');
});

test('a wrong number of operands is an error before running, at the form (D3, D33)', () => {
  assert.equal(errorOf('(+ 1 2 3)'), '+ takes 2 arguments, not 3');
  assert.equal(errorOf('(- 1)'), '- takes 2 arguments, not 1');
  assert.equal(errorOf('(+ 1 (* 2))'), '* takes 2 arguments, not 1');
});

test('an unknown name or an unknown operator is an error before running', () => {
  assert.equal(errorOf('(+ x 1)'), 'unknown name x');
  assert.equal(errorOf('(foo 1 2)'), 'unknown operator foo');
  // A Map, not an object: the names on Object.prototype aren't operators.
  assert.equal(errorOf('(constructor 1 2)'), 'unknown operator constructor');
});

test('nesting to the limit evaluates: 1000 levels of (+ _ 1) over 0 is 1000 (D30)', () => {
  const text = '(+ '.repeat(1000) + '0' + ' 1)'.repeat(1000);
  assert.equal(run(text), 1000n);
});
