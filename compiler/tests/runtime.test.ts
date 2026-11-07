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
    const r = cprog(`str-index-bad-${i}`, `dt_path = "x.ditto"; Value s = ${S('abc')}, o; ${call} return 0;`);
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
