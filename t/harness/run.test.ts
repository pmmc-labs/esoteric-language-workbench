// t/run.sh's two watchdogs, each made to bite: from step 6 a program can
// run for ever, and one that prints as it goes fills a disk in the time
// the first watchdog allows it.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const run = (name: string, env: Record<string, string>) =>
    spawnSync('sh', ['t/run.sh', `t/harness/${name}.pl`], { cwd: root, encoding: 'utf8', env: { ...process.env, ...env }, maxBuffer: 1 << 28 });

test('a program that never ends is killed, and its test fails', () => {
    const r = run('never-ends', { TIMEOUT: '1' });
    assert.equal(r.status, 1, r.stdout);
    assert.match(r.stdout, /^FAIL never-ends$/m);
    assert.match(r.stdout, /^\+killed after 1s$/m);
    assert.match(r.stdout, /^1 tests, 1 failed$/m);
});

test('a program that prints without end is stopped at the limit, and its test fails', () => {
    const r = run('prints-for-ever', { TIMEOUT: '30' });
    assert.equal(r.status, 1, r.stdout.slice(0, 2000));
    assert.match(r.stdout, /^FAIL prints-for-ever$/m);
    assert.match(r.stdout, /^\+stopped: it printed more than 16384 blocks of 512 bytes$/m);
    assert.doesNotMatch(r.stdout, /killed after/);
    // What it printed is not in the report.
    assert.ok(r.stdout.length < 2000, String(r.stdout.length));
});

test('and a loop that ends, having printed a megabyte, passes', () => {
    const r = run('ends', { TIMEOUT: '30' });
    assert.equal(r.status, 0, r.stdout.slice(0, 2000));
    assert.match(r.stdout, /^ok   ends$/m);
});
