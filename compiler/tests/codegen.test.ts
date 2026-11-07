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
  const c = compile('print("a\\n\\"?\xc3\xa9")', 'a.ditto');
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
  assert.match(c, /dt_index\(2, 8, /);
  assert.match(c, /dt_bool\(dt_in\(2, 15, /);
  assert.match(c, /dt_bool\(!dt_in\(2, 23, /);
});

test('a lookup is a runtime call that returns whether it hit, so step 7 can branch on a miss', () => {
  const h = readFileSync(new URL('../../runtime/ditto.h', import.meta.url), 'utf8');
  assert.match(h, /bool dt_try_index\(int line, int col, Value c, Value i, Value \*out\);/);
  assert.match(h, /bool dt_try_int\(int line, int col, Value s, Value \*out\);/);
});

test('a list literal computes its items in order, then builds the list once', () => {
  const c = compile('print([1, [2], []])', 'a.ditto');
  assert.match(c, /Value a\d+\[\] = \{t\d+, t\d+, t\d+\};\n\s*Value t\d+ = dt_list_new\(3, a\d+\);/);
  assert.match(c, /dt_list_new\(0, NULL\)/);
  assert.ok(c.indexOf('dt_int(INT64_C(1))') < c.indexOf('dt_int(INT64_C(2))'));
});

test('an indexed assignment evaluates its indexes, then the value, then rebuilds the spine from the inside out', () => {
  const c = compile('let g = [[1]]\nlet i = 0\ng[i][0] = 5', 'a.ditto');
  // The path is looked up (all steps but the last) at each step's own `[`, then set, innermost first.
  const look = c.indexOf('dt_index(3, 2, ');
  const rhs = c.indexOf('INT64_C(5)');
  const inner = c.indexOf('dt_set_index(3, 5, ');
  const outer = c.indexOf('dt_set_index(3, 2, ');
  assert.ok(rhs > 0 && look > rhs && inner > look && outer > inner, `${rhs} ${look} ${inner} ${outer}`);
  assert.match(c, /v_g = t\d+;/);
  assert.doesNotMatch(c, /dt_index\(3, 5, /);
});

test('a compound assignment on a path reads the current value, evaluates the value, then applies the operator at the operator', () => {
  const c = compile('let g = [[1]]\ng[0][0] += 2', 'a.ditto');
  const read = c.indexOf('dt_index(2, 5, ');
  const rhs = c.indexOf('INT64_C(2)');
  const add = c.indexOf('dt_add(2, 9, ');
  const set = c.indexOf('dt_set_index(2, 5, ');
  assert.ok(read > 0 && rhs > read && add > rhs && set > add, `${read} ${rhs} ${add} ${set}`);
});

test('a lookup on a list is the same runtime call as on a string, so step 7 can branch on its result', () => {
  const h = readFileSync(new URL('../../runtime/ditto.h', import.meta.url), 'utf8');
  assert.match(h, /Value dt_set_index\(int line, int col, Value c, Value i, Value v\);/);
  assert.match(h, /Value dt_list_new\(int64_t n, const Value \*items\);/);
  assert.match(h, /Value dt_b_sort\(/);
});

test('a map literal computes its keys and values in order, then builds the map once', () => {
  const c = compile('print({a: f(1), "b": f(2), 3: 4})\nfn f(x) {\n}', 'a.ditto');
  const main = c.indexOf('int main');
  assert.match(c, /Value a\d+\[\] = \{t\d+, t\d+, t\d+\};\n\s*Value b\d+\[\] = \{t\d+, t\d+, t\d+\};\n\s*Value t\d+ = dt_map_new\(3, a\d+, b\d+\);/);
  assert.match(compile('print({})', 'a.ditto'), /dt_map_new\(0, NULL, NULL\)/);
  const at = ['f_f(', 'f_f(', 'dt_map_new('].map((s, k) => c.indexOf(s, k === 1 ? c.indexOf('f_f(', main) + 1 : main));
  assert.ok(at.every((n) => n > 0) && at[0] < at[1] && at[1] < at[2], String(at));
  assert.match(c, /dt_str_new\("a", 1\)/);
  assert.match(c, /dt_int\(INT64_C\(3\)\)/);
});

test('a field is a runtime call at its dot, with the name as a string key', () => {
  const c = compile('let m = {}\nprint(m.name, m["x"])', 'a.ditto');
  assert.match(c, /dt_str_new\("name", 4\)/);
  assert.match(c, /dt_field\(2, 8, t\d+, t\d+\)/);
  assert.match(c, /dt_index\(2, 16, /);
});

test('a path of fields and indexes looks up each step at its own position, then sets from the inside out', () => {
  const c = compile('let m = {a: [{b: 1}]}\nm.a[0].b = 5', 'a.ditto');
  const rhs = c.indexOf('INT64_C(5)');
  const look1 = c.indexOf('dt_field(2, 2, ');
  const look2 = c.indexOf('dt_index(2, 4, ');
  const set1 = c.indexOf('dt_set_field(2, 7, ');
  const set2 = c.indexOf('dt_set_index(2, 4, ');
  const set3 = c.indexOf('dt_set_field(2, 2, ');
  assert.ok(rhs > 0 && look1 > rhs && look2 > look1 && set1 > look2 && set2 > set1 && set3 > set2, [rhs, look1, look2, set1, set2, set3].join(' '));
  assert.doesNotMatch(c, /dt_field\(2, 7, /);
  // The compound form reads the whole path first, with the last step's own lookup.
  const d = compile('let m = {a: {b: 1}}\nm.a.b += 2', 'a.ditto');
  assert.ok(d.indexOf('dt_field(2, 4, ') < d.indexOf('INT64_C(2)') && d.indexOf('INT64_C(2)') < d.indexOf('dt_add(2, 7, '));
});

test('the runtime header declares the map lookups in their try form, for step 7', () => {
  const h = readFileSync(new URL('../../runtime/ditto.h', import.meta.url), 'utf8');
  assert.match(h, /bool dt_try_field\(int line, int col, Value c, Value name, Value \*out\);/);
  assert.match(h, /Value dt_field\(int line, int col, Value c, Value name\);/);
  assert.match(h, /Value dt_set_field\(int line, int col, Value c, Value name, Value v\);/);
  assert.match(h, /Value dt_map_new\(int64_t n, const Value \*keys, const Value \*vals\);/);
  assert.match(h, /Value dt_b_keys\(/);
  assert.match(h, /Value dt_b_remove\(/);
});

test('an else compiles to if and goto: the try form inside its left operand, the fault form elsewhere', () => {
  const c = compile('let xs = [1]\nprint(xs[5] else 0, xs[0], int("x") else 1, xs.a else 2)', 'a.ditto');
  assert.match(c, /if \(!dt_try_index\(2, 9, t\d+, t\d+, &t\d+\)\) goto miss\d+;/);
  assert.match(c, /dt_index\(2, 23, t\d+, /);
  assert.match(c, /if \(!dt_try_int\(2, 28, t\d+, &t\d+\)\) goto miss\d+;/);
  assert.match(c, /if \(!dt_try_field\(2, 47, t\d+, t\d+, &t\d+\)\) goto miss\d+;/);
  assert.doesNotMatch(c, /dt_b_int|dt_field\(|&&|\?/);
  // The right operand sits after the label, outside the left operand's catcher.
  const d = compile('let xs = [1]\nprint(xs[5] else xs[6])', 'a.ditto');
  assert.ok(d.indexOf('miss') < d.indexOf('dt_index(2, 20, '), d);
  assert.match(d, /dt_try_index\(2, 9, /);
  // A function's body is compiled with no catcher, whatever calls it.
  const e = compile('fn f(xs) { return xs[0] }\nprint((f([]) + [1][5]) else 0)', 'a.ditto');
  assert.match(e, /return t\d+;/);
  assert.match(e, /dt_index\(1, 21, t\d+, /);
});

test('a miss label is written only when a lookup jumps to it', () => {
  // The inner else catches the only lookup, so the outer one has no label.
  const c = compile('let xs = [1]\nprint((xs[5] else 0) else 1)', 'a.ditto');
  assert.equal(c.match(/^\s*miss\d+: ;/gm)?.length, 1);
  assert.equal(c.match(/^\s*done\d+: ;/gm)?.length, 2);
});
