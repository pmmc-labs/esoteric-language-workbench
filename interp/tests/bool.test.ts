import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { check } from '../src/check.ts';
import { evaluate, show } from '../src/evaluate.ts';
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

test('a boolean prints as written (D11)', () => {
  assert.equal(show(run('#true')), '#true');
  assert.equal(show(run('(== (+ 1 2) 3)')), '#true');
});

test('the orderings are on integers; == and != are on any two values (D12)', () => {
  assert.equal(run('(< 1 2)'), true);
  assert.equal(run('(<= 2 2)'), true);
  assert.equal(run('(> 2 2)'), false);
  assert.equal(run('(>= -1 0)'), false);
  assert.equal(run('(== 1 #true)'), false);
  assert.equal(run('(!= 1 #true)'), true);
  assert.equal(run('(== #false #false)'), true);
  assert.equal(faultOf('(< #true 1)'), 'not an integer');
});

test('if gives the branch its test picks, and evaluates only that one (D13)', () => {
  assert.equal(run('(if #true 1 (/ 1 0))'), 1n);
  assert.equal(run('(if (< 1 2) (if #false (/ 1 0) 42) (/ 1 0))'), 42n);
});

test('a test that is not a boolean faults, and an arithmetic operator on a boolean faults', () => {
  assert.equal(faultOf('(if (- 1 1) 1 2)'), 'not a boolean');
  assert.equal(faultOf('(+ 1 (if #true #false 0))'), 'not an integer');
});

test('an if with the wrong number of parts is an error before running, even in a branch never taken (D13, D28)', () => {
  assert.equal(errorOf('(if #true 1)'), 'if takes 3 arguments, not 2');
  assert.equal(errorOf('(if #false (+ 1 2 3) 0)'), '+ takes 2 arguments, not 3');
});
