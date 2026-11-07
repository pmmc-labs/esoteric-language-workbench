import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
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

test('functions are prototyped, defined before main, and called between enter and leave', () => {
  const c = compile('print(f(1))\nfn f(a) {\n  return a\n}', 'a.ditto');
  assert.match(c, /Value f_f\(Value v_a\);/);
  const proto = c.indexOf('Value f_f(Value v_a);');
  const def = c.indexOf('Value f_f(Value v_a) {');
  const main = c.indexOf('int main(void)');
  assert.ok(proto > 0 && proto < def && def < main, String([proto, def, main]));
  // The body returns its value, and falls off the end with nil.
  assert.match(c.slice(def, main), /return t\d+;/);
  assert.match(c.slice(def, main), /return dt_nil\(\);\n}/);
  // The call: arguments first, then enter (at the name), the call, leave.
  const at = ['dt_int(', 'dt_enter(1, 7)', 'f_f(', 'dt_leave()', 'dt_b_print('].map((s) => c.indexOf(s, main));
  assert.ok(at.every((n) => n > 0), String(at));
  assert.deepEqual([...at].sort((a, b) => a - b), at);
});

test('a function called before its definition is prototyped first', () => {
  const c = compile('fn a() { return b() }\nfn b() { return a() }', 'a.ditto');
  assert.ok(c.indexOf('Value f_b(void);') < c.indexOf('Value f_a(void) {'));
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

// Step 2.
test('a variable is a C Value named v_NAME, declared where its let is', () => {
  const c = compile('let x = 1\nx = x + 2\nprint(x)', 'a.ditto');
  assert.match(c, /Value v_x = t\d+;/);
  assert.match(c, /v_x = t\d+;/);
  assert.ok(c.indexOf('Value v_x') < c.indexOf('dt_add'));
});

test('compound assignment reads the variable first, applies the operator at its own position', () => {
  const c = compile('let x = 1\nx -= 2', 'a.ditto');
  assert.match(c, /dt_sub\(2, 3, t\d+, t\d+\)/);
  const read = c.search(/Value t\d+ = v_x;/);
  assert.ok(read > 0 && read < c.indexOf('dt_sub'));
});

test('if tests its condition with the condition\'s first-token position', () => {
  const c = compile('if 1 + 2 < 4 {\n}', 'a.ditto');
  assert.match(c, /dt_need_cond\(1, 4, t\d+\);/);
  assert.match(c, /if \(t\d+\.b\) \{/);
});

test('while is a C loop that tests at the top; break and continue are C ones', () => {
  const c = compile('while true {\n  break\n  continue\n}', 'a.ditto');
  assert.match(c, /for \(;;\) \{/);
  assert.match(c, /dt_need_cond\(1, 7, /);
  assert.match(c, /if \(!t\d+\.b\) break;/);
  assert.match(c, /\n\s+break;\n\s+continue;/);
});

test('a range loop checks both bounds after evaluating both, and cannot overflow', () => {
  const c = compile('for i in 1..=2 + 3 {\n}', 'a.ditto');
  const at = ['dt_add(', 'dt_need_range_bound(1, 10, ', 'dt_need_range_bound(1, 14, '].map((s) => c.indexOf(s));
  assert.ok(at.every((n) => n > 0) && at[0] < at[1] && at[1] < at[2], String(at));
  assert.match(c, /Value v_i = dt_int\(/);
  assert.doesNotMatch(c, /\+\+/);
});

test('a for over a value asks the runtime for its length, at the expression', () => {
  assert.match(compile('for x in 5 {\n}', 'a.ditto'), /dt_iter_len\(1, 10, t\d+\)/);
});

test('a string literal is built once and cached; its bytes are escaped for C', () => {
  const c = compile('print("a\\n\\"?\\xc3\\xa9")'.replace('\\xc3\\xa9', 'é'), 'a.ditto');
  assert.match(c, /static Value s\d+;/);
  assert.match(c, /dt_str_new\("a\\012\\"\\\?\\303\\251", 6\)/);
  assert.match(compile('print("")', 'a.ditto'), /dt_str_new\("", 0\)/);
});

test('interpolation evaluates its parts in order, then joins them', () => {
  const c = compile('print("<{f(1)}{g(2)}>")\nfn f(a) {\n}\nfn g(a) {\n}', 'a.ditto');
  const main = c.indexOf('int main');
  const at = ['f_f(', 'f_g(', 'dt_interp(4, '].map((s) => c.indexOf(s, main));
  assert.ok(at.every((n) => n > 0) && at[0] < at[1] && at[1] < at[2], String(at));
});

test('indexing and in call the runtime at the operator', () => {
  const c = compile('let s = "abc"\nprint(s[1], 1 in s, 2 not in s)', 'a.ditto');
  assert.match(c, /dt_index\(2, 9, /);
  assert.match(c, /dt_bool\(dt_in\(2, 17, /);
  assert.match(c, /dt_bool\(!dt_in\(2, 24, /);
});

test('a lookup is a runtime call that returns whether it hit, so step 7 can branch on a miss', () => {
  const h = readFileSync(new URL('../../runtime/ditto.h', import.meta.url), 'utf8');
  assert.match(h, /bool dt_try_index\(int line, int col, Value c, Value i, Value \*out\);/);
  assert.match(h, /bool dt_try_int\(int line, int col, Value s, Value \*out\);/);
});
