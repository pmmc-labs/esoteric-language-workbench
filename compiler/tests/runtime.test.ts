import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The runtime on its own, from a hand-written C main: what a golden test
// can't reach at step 0 (no Ditto program faults yet) and the allocator.
const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const dir = join(root, 'build', 'unit-runtime');
mkdirSync(dir, { recursive: true });

function cprog(name: string, body: string) {
  const c = join(dir, name + '.c');
  const exe = join(dir, name);
  writeFileSync(c, `#include <stdint.h>\n#include <stdio.h>\n#include <string.h>\n#include "ditto.h"\nint main(void) {\n${body}\n}\n`);
  const cc = process.env.LANG_CC || 'cc';
  const b = spawnSync(cc, ['-std=c11', '-Wall', '-Wextra', '-Werror', '-I', join(root, 'runtime'),
    c, join(root, 'runtime', 'ditto.c'), '-o', exe], { encoding: 'utf8' });
  assert.equal(b.status, 0, b.stderr);
  // One pipe for both streams, as a golden test sees them.
  const r = spawnSync('sh', ['-c', `${exe} 2>&1`], { encoding: 'utf8' });
  return { out: r.stdout, status: r.status };
}

test('print writes values separated by spaces, then a newline', () => {
  const r = cprog('print', `
    Value a[] = {dt_int(1), dt_int(-2), dt_int(INT64_MIN), dt_int(INT64_MAX), dt_int(0)};
    Value n = dt_b_print(1, 1, 5, a);
    dt_b_print(1, 1, 0, NULL);
    Value b[] = {dt_bool(true), dt_nil(), dt_bool(false)};
    dt_b_print(1, 1, 3, b);
    if (n.tag != T_NIL) return 9;
    return 0;`);
  assert.equal(r.out, '1 -2 -9223372036854775808 9223372036854775807 0\n\ntrue nil false\n');
  assert.equal(r.status, 0);
});

test('a fault flushes standard output first, then prints one line and exits 1', () => {
  const r = cprog('fault', `
    dt_path = "x.ditto";
    Value a[] = {dt_int(1)};
    dt_b_print(1, 1, 1, a);
    dt_fault(3, 4, "boom %d", 7);
    return 0;`);
  assert.equal(r.out, '1\nx.ditto:3:4: fault: boom 7\n');
  assert.equal(r.status, 1);
});

test('the allocator hands out aligned, distinct, lasting memory', () => {
  const r = cprog('alloc', `
    dt_path = "x.ditto";
    enum { N = 50000 };
    static char *p[N];
    for (int i = 0; i < N; i++) {
      p[i] = dt_alloc(1 + (size_t)(i % 100));
      if ((uintptr_t)p[i] % 16 != 0) dt_fault(1, 1, "misaligned %d", i);
      memset(p[i], i % 251, 1 + (size_t)(i % 100));
      if (i % 5000 == 0) {
        char *big = dt_alloc((size_t)3 << 20);   // bigger than a chunk
        memset(big, 7, (size_t)3 << 20);
      }
    }
    for (int i = 0; i < N; i++)
      for (int j = 0; j < 1 + i % 100; j++)
        if ((unsigned char)p[i][j] != i % 251) dt_fault(1, 1, "clobbered %d", i);
    char *z = dt_alloc(0);
    if (z == NULL) dt_fault(1, 1, "alloc(0) is NULL");
    dt_b_print(1, 1, 0, NULL);
    return 0;`);
  assert.equal(r.out, '\n');
  assert.equal(r.status, 0);
});

test('integer operators: truncating division, checked arithmetic', () => {
  const r = cprog('ops', `
    Value mn = dt_int(INT64_MIN), mx = dt_int(INT64_MAX);
    int64_t got[] = {
      dt_div(1, 1, dt_int(-7), dt_int(2)).i, dt_mod(1, 1, dt_int(-7), dt_int(2)).i,
      dt_div(1, 1, dt_int(7), dt_int(-2)).i, dt_mod(1, 1, dt_int(7), dt_int(-2)).i,
      dt_mod(1, 1, mn, dt_int(-1)).i, dt_add(1, 1, mx, mn).i, dt_sub(1, 1, mn, mn).i,
      dt_mul(1, 1, mx, dt_int(-1)).i, dt_mul(1, 1, mn, dt_int(1)).i, dt_mul(1, 1, dt_int(-3037000499), dt_int(3037000499)).i,
      dt_neg(1, 1, mx).i, dt_sub(1, 1, dt_int(-1), mx).i, dt_sub(1, 1, dt_int(0), mx).i,
    };
    for (size_t i = 0; i < sizeof got / sizeof got[0]; i++) printf("%lld\\n", (long long)got[i]);
    return 0;`);
  assert.equal(r.out, ['-3', '-1', '-3', '1', '0', '-1', '0', '-9223372036854775807', '-9223372036854775808',
    '-9223372030926249001', '-9223372036854775807', '-9223372036854775808', '-9223372036854775807', ''].join('\n'));
  assert.equal(r.status, 0);
});

test('the call depth: 1000 nested calls are allowed, the 1001st faults at its call', () => {
  const ok = cprog('depth-ok', `
    dt_path = "x.ditto";
    for (int i = 0; i < 1000; i++) dt_enter(1, 1);
    for (int i = 0; i < 1000; i++) dt_leave();
    for (int i = 0; i < 1000; i++) dt_enter(1, 1);
    printf("deep\\n");
    return 0;`);
  assert.equal(ok.out, 'deep\n');
  assert.equal(ok.status, 0);
  const over = cprog('depth-over', `
    dt_path = "x.ditto";
    for (int i = 0; i < 1000; i++) dt_enter(1, 1);
    dt_enter(5, 6);
    return 0;`);
  assert.equal(over.out, 'x.ditto:5:6: fault: stack overflow (more than 1000 nested calls)\n');
  assert.equal(over.status, 1);
});

test('equality is structural across types and never faults', () => {
  const r = cprog('eq', `
    Value v[] = {dt_nil(), dt_bool(true), dt_bool(false), dt_int(0), dt_int(1)};
    for (int i = 0; i < 5; i++) { for (int j = 0; j < 5; j++) putchar(dt_equal(v[i], v[j]) ? '1' : '0'); putchar('\\n'); }
    return 0;`);
  assert.equal(r.out, '10000\n01000\n00100\n00010\n00001\n');
});

test('conditions and range bounds must be what they are', () => {
  const ok = cprog('cond-ok', `
    dt_path = "x.ditto";
    dt_need_cond(1, 1, dt_bool(false));
    dt_need_range_bound(1, 1, dt_int(INT64_MIN));
    dt_b_print(1, 1, 0, NULL);
    return 0;`);
  assert.equal(ok.out, '\n');
  const cases: [string, string][] = [
    ['dt_need_cond(4, 5, dt_int(1));', 'x.ditto:4:5: fault: condition must be a bool, got int\n'],
    ['dt_need_cond(4, 5, dt_nil());', 'x.ditto:4:5: fault: condition must be a bool, got nil\n'],
    ['dt_need_range_bound(2, 3, dt_bool(true));', 'x.ditto:2:3: fault: range bounds must be ints, got bool\n'],
    ['dt_iter_len(7, 8, dt_int(5));', 'x.ditto:7:8: fault: cannot iterate over int\n'],
    ['dt_iter_len(7, 8, dt_nil());', 'x.ditto:7:8: fault: cannot iterate over nil\n'],
  ];
  for (const [i, [call, out]] of cases.entries()) {
    const r = cprog(`cond-${i}`, `dt_path = "x.ditto"; ${call} return 0;`);
    assert.equal(r.out, out);
    assert.equal(r.status, 1);
  }
});

// Strings are bytes with a length: a NUL inside one is an ordinary byte.
const S = (text: string) =>
  `dt_str_new("${[...text].map((c) => '\\' + c.charCodeAt(0).toString(8).padStart(3, '0')).join('')}", ${text.length})`;

test('strings: construction, length, printing and str with embedded NULs', () => {
  const r = cprog('str-basic', `
    Value s = ${S('ab\0cd')};
    Value e = dt_str_new("", 0);
    Value a[] = {s, e, dt_int(5), dt_bool(true), dt_nil()};
    dt_b_print(1, 1, 5, a);
    Value l = dt_b_len(1, 1, 1, &s);
    Value t = dt_b_str(1, 1, 1, &a[2]);
    printf("%lld %lld %d\\n", (long long)l.i, (long long)t.s->len, t.s->bytes[0]);
    return 0;`);
  assert.equal(r.out, 'ab\0cd  5 true nil\n5 1 53\n');
});

test('strings: + joins, == and the ordering are byte by byte with the length', () => {
  const r = cprog('str-ops', `
    Value a = ${S('a\0b')}, b = ${S('a\0')}, c = ${S('a\xff')}, e = dt_str_new("", 0);
    Value j = dt_add(1, 1, a, b);
    printf("%lld %d\\n", (long long)j.s->len, memcmp(j.s->bytes, "a\\0ba\\0", 5));
    printf("%d%d%d%d\\n", dt_equal(a, a), dt_equal(a, b), dt_equal(e, e), dt_equal(e, dt_nil()));
    printf("%d%d%d\\n", dt_lt(1, 1, b, a).b, dt_lt(1, 1, a, c).b, dt_lt(1, 1, c, a).b);
    printf("%d%d%d\\n", dt_lt(1, 1, e, b).b, dt_le(1, 1, a, a).b, dt_ge(1, 1, b, a).b);
    return 0;`);
  assert.equal(r.out, '5 0\n1010\n110\n110\n');
});

test('strings: index hits and misses are reported by dt_try_index, faults by dt_index', () => {
  const ok = cprog('str-index', `
    dt_path = "x.ditto";
    Value s = ${S('a\0b')}, out = dt_nil();
    bool hit = dt_try_index(1, 1, s, dt_int(1), &out);
    printf("%d %lld %d\\n", hit, (long long)out.s->len, out.s->bytes[0]);
    bool m1 = dt_try_index(1, 1, s, dt_int(3), &out);
    bool m2 = dt_try_index(1, 1, s, dt_int(-1), &out);
    printf("%d %d\\n", m1, m2);
    Value c = dt_index(1, 1, s, dt_int(2));
    printf("%c\\n", c.s->bytes[0]);
    dt_index(4, 5, s, dt_int(3));
    return 0;`);
  assert.equal(ok.out, '1 1 0\n0 0\nb\nx.ditto:4:5: fault: index 3 out of range (length 3)\n');
  assert.equal(ok.status, 1);
  const bad: [string, string][] = [
    ['dt_try_index(2, 3, s, dt_nil(), &o);', 'x.ditto:2:3: fault: string index must be an int, got nil\n'],
    ['dt_try_index(2, 3, dt_int(1), dt_int(0), &o);', 'x.ditto:2:3: fault: cannot index int\n'],
  ];
  for (const [i, [call, out]] of bad.entries()) {
    const r = cprog(`str-index-bad-${i}`, `dt_path = "x.ditto"; Value s = ${S('abc')}, o; (void)s; ${call} return 0;`);
    assert.equal(r.out, out);
    assert.equal(r.status, 1);
  }
});

test('strings: int parses the whole spelling, and reports a miss rather than faulting', () => {
  const r = cprog('str-int', `
    dt_path = "x.ditto";
    const char *good[] = {"0", "-0", "007", "-12", "9223372036854775807", "-9223372036854775808"};
    for (int i = 0; i < 6; i++) {
      Value s = dt_str_new(good[i], (int64_t)strlen(good[i])), o = dt_nil();
      bool hit = dt_try_int(1, 1, s, &o);
      printf("%d %lld\\n", hit, (long long)o.i);
    }
    const char *bad[] = {"", "-", "+1", " 1", "1 ", "1_0", "12x", "9223372036854775808", "-9223372036854775809", "--1"};
    for (int i = 0; i < 10; i++) {
      Value s = dt_str_new(bad[i], (int64_t)strlen(bad[i])), o = dt_nil();
      printf("%d", dt_try_int(1, 1, s, &o));
    }
    printf("\\n");
    Value n = ${S('1\0')}, o;
    printf("%d\\n", dt_try_int(1, 1, n, &o));
    dt_try_int(3, 4, dt_int(5), &o);
    return 0;`);
  assert.equal(r.out, ['1 0', '1 0', '1 7', '1 -12', '1 9223372036854775807', '1 -9223372036854775808',
    '0000000000', '0', 'x.ditto:3:4: fault: int: expected a string, got int', ''].join('\n'));
});

test('strings: not a number prints the string as a list would, NULs included', () => {
  const r = cprog('str-int-fault', `
    dt_path = "x.ditto";
    Value s = ${S('a"\\\n\0z')};
    dt_b_int(2, 3, 1, &s);
    return 0;`);
  assert.equal(r.out, 'x.ditto:2:3: fault: not a number: "a\\"\\\\\\n\0z"\n');
  assert.equal(r.status, 1);
});

test('strings: in is substring search, the empty string is in every string', () => {
  const r = cprog('str-in', `
    Value h = ${S('ab\0cab')}, e = dt_str_new("", 0);
    printf("%d%d%d%d%d%d%d\\n", dt_in(1, 1, e, h), dt_in(1, 1, e, e), dt_in(1, 1, ${S('b\0c')}, h),
      dt_in(1, 1, ${S('b\0d')}, h), dt_in(1, 1, ${S('abx')}, h), dt_in(1, 1, h, h), dt_in(1, 1, ${S('cab\0')}, h));
    return 0;`);
  assert.equal(r.out, '1110010\n');
});

test('strings: iteration yields one-byte strings; lower, upper and slice', () => {
  const r = cprog('str-misc', `
    dt_path = "x.ditto";
    Value s = ${S('aB\0\xc9z')};
    printf("%lld\\n", (long long)dt_iter_len(1, 1, s));
    for (int i = 0; i < 5; i++) { Value c = dt_iter_item(s, i); printf("%lld:%d ", (long long)c.s->len, (unsigned char)c.s->bytes[0]); }
    Value lo = dt_b_lower(1, 1, 1, &s), up = dt_b_upper(1, 1, 1, &s);
    printf("\\n%d %d\\n", memcmp(lo.s->bytes, "ab\\0\\xc9z", 5), memcmp(up.s->bytes, "AB\\0\\xc9Z", 5));
    Value a[] = {s, dt_int(1), dt_int(4)};
    Value sl = dt_b_slice(1, 1, 3, a);
    printf("%lld %d\\n", (long long)sl.s->len, memcmp(sl.s->bytes, "B\\0\\xc9", 3));
    Value b[] = {s, dt_int(2), dt_int(9)};
    dt_b_slice(6, 7, 3, b);
    return 0;`);
  assert.equal(r.out, '5\n1:97 1:66 1:0 1:201 1:122 \n0 0\n3 0\nx.ditto:6:7: fault: slice 2..9 out of range (length 5)\n');
});

test('read returns the rest of standard input, NULs included, then the empty string', () => {
  const c = join(dir, 'read.c');
  const exe = join(dir, 'read');
  writeFileSync(c, `#include <stdio.h>\n#include "ditto.h"\nint main(void) {
    Value a = dt_b_read(1, 1, 0, NULL), b = dt_b_read(1, 1, 0, NULL);
    printf("%lld %lld\\n", (long long)a.s->len, (long long)b.s->len);
    return 0;\n}\n`);
  const cc = process.env.LANG_CC || 'cc';
  const bld = spawnSync(cc, ['-std=c11', '-Wall', '-Wextra', '-Werror', '-I', join(root, 'runtime'),
    c, join(root, 'runtime', 'ditto.c'), '-o', exe], { encoding: 'utf8' });
  assert.equal(bld.status, 0, bld.stderr);
  const big = Buffer.concat([Buffer.from('x\0y'), Buffer.alloc(200000, 65)]);
  const r = spawnSync(exe, [], { input: big, encoding: 'utf8' });
  assert.equal(r.stdout, '200003 0\n');
});

test('fail faults with the string itself, or the printed form of anything else', () => {
  const s = cprog('fail-str', `dt_path = "x.ditto"; Value s = ${S('a\0b"')}; dt_b_fail(2, 3, 1, &s); return 0;`);
  assert.equal(s.out, 'x.ditto:2:3: fault: a\0b"\n');
  const n = cprog('fail-int', `dt_path = "x.ditto"; Value s = dt_int(-4); dt_b_fail(2, 3, 1, &s); return 0;`);
  assert.equal(n.out, 'x.ditto:2:3: fault: -4\n');
  assert.equal(n.status, 1);
});

// Lists (step 5). A list is built once and never written (D7): every update
// returns a new list and the old one is as it was. `L` builds a list in C
// source from the C source of its items; `I` is an int.
const L = (...items: string[]) =>
  `dt_list_new(${items.length}, (Value[]){${items.length > 0 ? items.join(', ') : 'dt_nil()'}})`;
const I = (n: number) => `dt_int(${n})`;

test('lists: construction copies the items, printing quotes strings inside, nesting', () => {
  const r = cprog('list-basic', `
    Value items[] = {dt_int(1), ${S('a"b\n')}, dt_nil()};
    Value l = dt_list_new(3, items);
    items[0] = dt_int(99);
    Value e = ${L()}, e0 = dt_list_new(0, NULL);
    Value n = ${L(I(1), L(S('x'), L()), 'dt_bool(true)')};
    Value a[] = {l, e0, n, ${S('top')}};
    dt_b_print(1, 1, 4, a);
    Value s = dt_b_str(1, 1, 1, &n);
    Value len = dt_b_len(1, 1, 1, &n), len0 = dt_b_len(1, 1, 1, &e0);
    printf("%s %lld %lld %lld %d %lld\\n", s.s->bytes, (long long)len.i, (long long)len0.i, (long long)l.l->len, (int)e.tag, (long long)l.l->items[0].i);
    Value parts[] = {${S('<')}, n, ${S('>')}};
    printf("%s\\n", dt_interp(3, parts).s->bytes);
    return 0;`);
  assert.equal(r.out, '[1, "a\\"b\\n", nil] [] [1, ["x", []], true] top\n[1, ["x", []], true] 3 0 3 4 1\n<[1, ["x", []], true]>\n');
});

test('lists: lookups report a miss, fault on a wrong type, and name the length', () => {
  const r = cprog('list-index', `
    dt_path = "x.ditto";
    Value l = ${L(I(10), I(20), L(I(30)))}, out = dt_nil();
    bool hit = dt_try_index(1, 1, l, dt_int(1), &out);
    printf("%d %lld\\n", hit, (long long)out.i);
    bool m1 = dt_try_index(1, 1, l, dt_int(3), &out), m2 = dt_try_index(1, 1, l, dt_int(-1), &out);
    printf("%d %d\\n", m1, m2);
    Value in = dt_index(1, 1, dt_index(1, 1, l, dt_int(2)), dt_int(0));
    printf("%lld\\n", (long long)in.i);
    dt_index(4, 5, l, dt_int(-1));
    return 0;`);
  assert.equal(r.out, '1 20\n0 0\n30\nx.ditto:4:5: fault: index -1 out of range (length 3)\n');
  assert.equal(r.status, 1);
  const bad: [string, string][] = [
    ['dt_try_index(2, 3, l, dt_str_new("a", 1), &o);', 'x.ditto:2:3: fault: list index must be an int, got string\n'],
    ['dt_try_index(2, 3, l, dt_bool(true), &o);', 'x.ditto:2:3: fault: list index must be an int, got bool\n'],
    ['dt_try_index(2, 3, l, dt_nil(), &o);', 'x.ditto:2:3: fault: list index must be an int, got nil\n'],
    ['dt_index(2, 3, dt_nil(), dt_int(0));', 'x.ditto:2:3: fault: cannot index nil\n'],
  ];
  for (const [i, [call, out]] of bad.entries()) {
    const c = cprog(`list-index-bad-${i}`, `dt_path = "x.ditto"; Value l = ${L(I(1))}, o; (void)l; (void)o; ${call} return 0;`);
    assert.equal(c.out, out);
    assert.equal(c.status, 1);
  }
});

test('lists: dt_set_index builds a new list and leaves the old one and its elements alone', () => {
  const r = cprog('list-set', `
    dt_path = "x.ditto";
    Value inner = ${L(I(1), I(2))};
    Value l = dt_list_new(2, (Value[]){inner, dt_int(7)});
    Value m = dt_set_index(1, 1, l, dt_int(1), dt_int(8));
    Value deep = dt_set_index(1, 1, l, dt_int(0), dt_set_index(1, 1, inner, dt_int(0), dt_int(9)));
    Value a[] = {l, m, deep, inner};
    dt_b_print(1, 1, 4, a);
    printf("%d %d %d\\n", m.l != l.l, m.l->items[0].l == inner.l, deep.l->items[1].i == 7);
    dt_set_index(5, 6, l, dt_int(2), dt_int(0));
    return 0;`);
  assert.equal(r.out, '[[1, 2], 7] [[1, 2], 8] [[9, 2], 7] [1, 2]\n1 1 1\nx.ditto:5:6: fault: index 2 out of range (length 2)\n');
  assert.equal(r.status, 1);
  const bad: [string, string][] = [
    ['dt_set_index(2, 3, l, dt_int(-1), dt_int(0));', 'x.ditto:2:3: fault: index -1 out of range (length 1)\n'],
    ['dt_set_index(2, 3, l, dt_str_new("a", 1), dt_int(0));', 'x.ditto:2:3: fault: list index must be an int, got string\n'],
    ['dt_set_index(2, 3, dt_str_new("abc", 3), dt_int(0), dt_int(0));', 'x.ditto:2:3: fault: cannot assign into string\n'],
    ['dt_set_index(2, 3, dt_int(5), dt_int(0), dt_int(0));', 'x.ditto:2:3: fault: cannot assign into int\n'],
    ['dt_set_index(2, 3, dt_nil(), dt_str_new("a", 1), dt_int(0));', 'x.ditto:2:3: fault: cannot assign into nil\n'],
  ];
  for (const [i, [call, out]] of bad.entries()) {
    const c = cprog(`list-set-bad-${i}`, `dt_path = "x.ditto"; Value l = ${L(I(1))}; (void)l; ${call} return 0;`);
    assert.equal(c.out, out);
    assert.equal(c.status, 1);
  }
});

test('lists: + joins into a new list; == is structural, and true is not 1', () => {
  const r = cprog('list-ops', `
    dt_path = "x.ditto";
    Value a = ${L(I(1), L(I(2)))}, b = ${L(I(3))}, e = ${L()};
    Value j = dt_add(1, 1, a, b), k = dt_add(1, 1, e, e);
    Value p[] = {j, k, a, b};
    dt_b_print(1, 1, 4, p);
    printf("%d%d%d%d\\n", dt_equal(a, a), dt_equal(a, ${L(I(1), L(I(2)))}), dt_equal(a, b), dt_equal(e, e));
    printf("%d%d%d\\n", dt_equal(${L('dt_bool(true)')}, ${L(I(1))}), dt_equal(${L('dt_nil()')}, ${L('dt_nil()')}), dt_equal(e, dt_nil()));
    printf("%d%d\\n", dt_equal(${L(S('a'))}, ${L(S('a'))}), dt_equal(${L(L())}, ${L()}));
    dt_add(3, 4, a, dt_int(1));`);
  assert.equal(r.out, '[1, [2], 3] [] [1, [2]] [3]\n1101\n010\n10\nx.ditto:3:4: fault: cannot use + on list and int\n');
});

test('lists: ordering is lexicographic, a prefix first; an uncomparable pair faults at the operator', () => {
  const r = cprog('list-order', `
    dt_path = "x.ditto";
    Value e = ${L()}, a = ${L(I(1), I(2))}, b = ${L(I(1), I(3))}, c = ${L(I(1))};
    printf("%d%d%d%d\\n", dt_lt(1, 1, a, b).b, dt_lt(1, 1, b, a).b, dt_lt(1, 1, a, a).b, dt_le(1, 1, a, a).b);
    printf("%d%d%d%d\\n", dt_lt(1, 1, c, a).b, dt_gt(1, 1, a, c).b, dt_lt(1, 1, e, c).b, dt_ge(1, 1, e, e).b);
    Value s1 = ${L(S('a'), S('b'))}, s2 = ${L(S('a'), S('c'))}, n1 = ${L(L(I(1)), I(5))}, n2 = ${L(L(I(1), I(0)), I(0))};
    printf("%d%d\\n", dt_lt(1, 1, s1, s2).b, dt_lt(1, 1, n1, n2).b);
    Value x = ${L(I(1), S('a'))}, y = ${L(I(2), I(3))};
    printf("%d\\n", dt_lt(1, 1, x, y).b);
    dt_lt(7, 8, x, ${L(I(1), I(2))});`);
  assert.equal(r.out, '1001\n1111\n11\n1\nx.ditto:7:8: fault: cannot use < on string and int\n');
  const ops: [string, string][] = [
    ['dt_le(2, 3, a, a);', 'x.ditto:2:3: fault: cannot use <= on nil and nil\n'],
    ['dt_gt(2, 3, a, dt_int(1));', 'x.ditto:2:3: fault: cannot use > on list and int\n'],
  ];
  for (const [i, [call, out]] of ops.entries()) {
    const c = cprog(`list-order-bad-${i}`, `dt_path = "x.ditto"; Value a = ${L('dt_nil()')}; ${call} return 0;`);
    assert.equal(c.out, out);
    assert.equal(c.status, 1);
  }
});

test('lists: in is == on an element; a for walks the items by index', () => {
  const r = cprog('list-in-iter', `
    dt_path = "x.ditto";
    Value l = ${L(I(1), L(I(2)), S('a'))};
    printf("%d%d%d%d%d\\n", dt_in(1, 1, dt_int(1), l), dt_in(1, 1, ${L(I(2))}, l), dt_in(1, 1, ${S('a')}, l), dt_in(1, 1, dt_int(2), l), dt_in(1, 1, dt_bool(true), l));
    printf("%d\\n", dt_in(1, 1, dt_nil(), ${L()}));
    printf("%lld\\n", (long long)dt_iter_len(1, 1, l));
    Value a[] = {dt_iter_item(l, 0), dt_iter_item(l, 1), dt_iter_item(l, 2)};
    dt_b_print(1, 1, 3, a);
    dt_in(6, 7, l, dt_int(3));`);
  assert.equal(r.out, '11100\n0\n3\n1 [2] a\nx.ditto:6:7: fault: cannot use in on list and int\n');
});

test('lists: sort is stable, by <, returns a new list; slice, split, join, words', () => {
  const r = cprog('list-builtins', `
    dt_path = "x.ditto";
    Value l = ${L(I(3), I(1), I(2), I(1))};
    Value s = dt_b_sort(1, 1, 1, &l);
    Value pairs = ${L(L(I(2), S('b')), L(I(1), S('z')), L(I(2), S('a')), L(I(1), S('a')))};
    Value sp = dt_b_sort(1, 1, 1, &pairs);
    Value p1[] = {l, s, sp, dt_b_sort(1, 1, 1, (Value[]){${L()}})};
    dt_b_print(1, 1, 4, p1);
    Value sl[] = {l, dt_int(1), dt_int(3)};
    Value part = dt_b_slice(1, 1, 3, sl);
    Value sl2[] = {l, dt_int(4), dt_int(4)};
    Value none = dt_b_slice(1, 1, 3, sl2);
    Value p2[] = {part, none};
    dt_b_print(1, 1, 2, p2);
    Value st[] = {${S('a,,b,')}, ${S(',')}};
    Value parts = dt_b_split(1, 1, 2, st);
    Value st2[] = {${S('aaa')}, ${S('aa')}};
    Value parts2 = dt_b_split(1, 1, 2, st2);
    Value st3[] = {${S('')}, ${S(',')}};
    Value parts3 = dt_b_split(1, 1, 2, st3);
    Value p3[] = {parts, parts2, parts3};
    dt_b_print(1, 1, 3, p3);
    Value jn[] = {parts, ${S('-')}};
    Value jn2[] = {${L()}, ${S('-')}};
    Value jn3[] = {${L(S('x'), S('y'))}, ${S('')}};
    Value j[] = {dt_b_join(1, 1, 2, jn), dt_b_join(1, 1, 2, jn2), dt_b_join(1, 1, 2, jn3)};
    dt_b_print(1, 1, 3, j);
    Value w1 = ${S(' \ta\0b \r\n c  ')};
    Value w = dt_b_words(1, 1, 1, &w1);
    printf("%lld %lld %lld\\n", (long long)w.l->len, (long long)w.l->items[0].s->len, (long long)w.l->items[1].s->len);
    return 0;`);
  assert.equal(r.out,
    '[3, 1, 2, 1] [1, 1, 2, 3] [[1, "a"], [1, "z"], [2, "a"], [2, "b"]] []\n[1, 2] []\n' +
    '["a", "", "b", ""] ["", "a"] [""]\na--b-  xy\n2 3 1\n');
});

test('lists: builtin faults', () => {
  const cases: [string, string][] = [
    ['Value a[] = {dt_int(1)}; dt_b_sort(2, 3, 1, a);', 'x.ditto:2:3: fault: sort: expected a list, got int\n'],
    [`Value a[] = {${L(I(1))}}; dt_b_words(2, 3, 1, a);`, 'x.ditto:2:3: fault: words: expected a string, got list\n'],
    ['Value a[] = {dt_str_new("abc", 3), dt_str_new("", 0)}; dt_b_split(2, 3, 2, a);', 'x.ditto:2:3: fault: split: empty separator\n'],
    ['Value a[] = {dt_int(1), dt_str_new(",", 1)}; dt_b_split(2, 3, 2, a);', 'x.ditto:2:3: fault: split: expected a string, got int\n'],
    ['Value a[] = {dt_str_new(",", 1), dt_int(1)}; dt_b_split(2, 3, 2, a);', 'x.ditto:2:3: fault: split: expected a string, got int\n'],
    [`Value a[] = {${L(S('a'), I(1))}, dt_str_new(",", 1)}; dt_b_join(2, 3, 2, a);`, 'x.ditto:2:3: fault: join: expected a list of strings, got int\n'],
    ['Value a[] = {dt_str_new("ab", 2), dt_str_new(",", 1)}; dt_b_join(2, 3, 2, a);', 'x.ditto:2:3: fault: join: expected a list of strings, got string\n'],
    [`Value a[] = {${L(S('a'))}, dt_int(1)}; dt_b_join(2, 3, 2, a);`, 'x.ditto:2:3: fault: join: expected a string, got int\n'],
    [`Value a[] = {${L(I(1), I(2), I(3))}, dt_int(1), dt_int(4)}; dt_b_slice(2, 3, 3, a);`, 'x.ditto:2:3: fault: slice 1..4 out of range (length 3)\n'],
    [`Value a[] = {${L(I(1))}, dt_int(1), dt_str_new("a", 1)}; dt_b_slice(2, 3, 3, a);`, 'x.ditto:2:3: fault: slice: expected an int, got string\n'],
    [`Value a[] = {${L(I(3), S('a'))}}; dt_b_sort(2, 3, 1, a);`, 'x.ditto:2:3: fault: cannot use < on string and int\n'],
  ];
  for (const [i, [code, out]] of cases.entries()) {
    const c = cprog(`list-fault-${i}`, `dt_path = "x.ditto"; ${code} return 0;`);
    assert.equal(c.out, out);
    assert.equal(c.status, 1);
  }
});
