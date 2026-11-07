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
