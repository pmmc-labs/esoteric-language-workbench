import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const dir = join(root, 'build', 'unit-main');
mkdirSync(dir, { recursive: true });
const ditto = (args: string[], env: Record<string, string> = {}) =>
  spawnSync(join(root, 'bin', 'ditto'), args, {
    cwd: root,
    encoding: 'utf8',
    env: { ...process.env, ...env },
  });
const src = (name: string, text: string) => {
  const p = join('build', 'unit-main', name);
  writeFileSync(join(root, p), text);
  return p;
};

test('c prints the generated C', () => {
  const r = ditto(['c', src('c.ditto', 'print(1)\n')]);
  assert.equal(r.status, 0);
  assert.match(r.stdout, /dt_b_print/);
  assert.equal(r.stderr, '');
});

test('build writes EXE and EXE.c; the executable runs', () => {
  const p = src('b.ditto', 'print(1, 2)\n');
  const exe = join('build', 'unit-main', 'b');
  const r = ditto(['build', p, '-o', exe]);
  assert.equal(r.status, 0, r.stderr);
  const out = spawnSync(join(root, exe), { encoding: 'utf8' });
  assert.equal(out.stdout, '1 2\n');
  assert.equal(out.status, 0);
  assert.equal(spawnSync('test', ['-f', join(root, exe + '.c')]).status, 0);
});

test('run runs the program and passes its output through', () => {
  const r = ditto(['run', src('r.ditto', 'print(7)\nprint()\n')]);
  assert.equal(r.status, 0, r.stderr);
  assert.equal(r.stdout, '7\n\n');
});

test('a compile error is path:line:col: error: message, exit 2', () => {
  const p = src('e.ditto', 'print(1)\nfoo(2)\n');
  for (const args of [['c', p], ['run', p], ['build', p, '-o', join('build', 'unit-main', 'e')]]) {
    const r = ditto(args);
    assert.equal(r.status, 2, args[0]);
    assert.equal(r.stderr, `${p}:2:1: error: unknown function foo\n`);
    assert.equal(r.stdout, '');
  }
});

test('bad usage is exit 2 with a usage line on stderr', () => {
  for (const args of [[], ['frob'], ['build'], ['build', 'x.ditto'], ['build', 'x.ditto', '-o'], ['run'], ['c']]) {
    const r = ditto(args);
    assert.equal(r.status, 2, JSON.stringify(args));
    assert.match(r.stderr, /^usage: /);
  }
});

test('a missing source file is exit 2', () => {
  const r = ditto(['c', 'build/unit-main/nope.ditto']);
  assert.equal(r.status, 2);
  assert.match(r.stderr, /cannot read build\/unit-main\/nope\.ditto/);
});

test('a failing C compiler is exit 3', () => {
  const p = src('f.ditto', 'print(1)\n');
  const r = ditto(['build', p, '-o', join('build', 'unit-main', 'f')], { LANG_CC: 'false' });
  assert.equal(r.status, 3);
});

test('LANG_CFLAGS reaches the C compiler', () => {
  const p = src('g.ditto', 'print(1)\n');
  const r = ditto(['build', p, '-o', join('build', 'unit-main', 'g')], { LANG_CFLAGS: '-DDITTO_TEST=1 -nonsense-flag' });
  assert.equal(r.status, 3);
});
