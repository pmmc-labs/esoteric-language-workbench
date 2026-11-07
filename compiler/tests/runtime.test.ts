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
  writeFileSync(c, `#include <stdint.h>\n#include <string.h>\n#include "ditto.h"\nint main(void) {\n${body}\n}\n`);
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
