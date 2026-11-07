import { test } from 'node:test';
import assert from 'node:assert/strict';
import { compile } from '../src/main.ts';

test('the program includes the runtime header and sets the path', () => {
  const c = compile('print(1)', 'dir/a "b".ditto');
  assert.match(c, /#include "ditto\.h"/);
  assert.match(c, /dt_path = "dir\/a \\"b\\"\.ditto";/);
  assert.match(c, /int main\(void\)/);
});

test('an int argument becomes a Value temporary; print gets its position', () => {
  const c = compile('\n  print(9223372036854775807, 0)', 'a.ditto');
  assert.match(c, /dt_int\(INT64_C\(9223372036854775807\)\)/);
  assert.match(c, /dt_b_print\(2, 3, 2, /);
});

test('print with no arguments passes a null array', () => {
  assert.match(compile('print()', 'a.ditto'), /dt_b_print\(1, 1, 0, NULL\)/);
});

test('statements come out in source order', () => {
  const c = compile('print(1)\nprint(2)\nprint(3)', 'a.ditto');
  const at = [1, 2, 3].map((n) => c.indexOf(`INT64_C(${n})`));
  assert.ok(at[0] > 0 && at[0] < at[1] && at[1] < at[2], String(at));
});

test('compile errors carry position and message', () => {
  assert.throws(() => compile('foo(1)', 'a.ditto'), (e: any) => e.message === 'unknown function foo');
});

test('operators call the runtime with their own position, operands first', () => {
  const c = compile('print(1 +\n  -2 * 3)', 'a.ditto');
  const at = ['dt_neg(2, 3,', 'dt_mul(2, 6,', 'dt_add(1, 9,', 'dt_b_print('].map((s) => c.indexOf(s));
  assert.ok(at.every((n) => n > 0), String(at));
  assert.deepEqual([...at].sort((a, b) => a - b), at);
});

test('== and != take no position; comparisons do', () => {
  const c = compile('print(1 == 2, 1 != 2, 1 <= 2)', 'a.ditto');
  assert.match(c, /dt_bool\(dt_equal\(t\d+, t\d+\)\)/);
  assert.match(c, /dt_bool\(!dt_equal\(/);
  assert.match(c, /dt_le\(1, 25,/);
});

test('and / or evaluate the right operand only inside an if', () => {
  const c = compile('print(true and 1 / 0 == 0)', 'a.ditto');
  const iff = c.indexOf('if (');
  assert.ok(iff > 0 && c.indexOf('dt_div') > iff && c.indexOf('dt_int') < iff + 400);
  assert.ok(c.indexOf('dt_bool(true)') < iff);
  assert.match(compile('print(true or false)', 'a.ditto'), /if \(!t\d+\.b\)/);
  assert.match(c, /dt_need_bool\(1, 12, "and", /);
});
