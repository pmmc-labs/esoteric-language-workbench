// The runtime's own tests: C programs that call it directly, for what no
// compiled program can reach yet. Each is built with the C compiler the
// driver uses and run with stdout and stderr down one pipe, as t/run.sh
// reads a test's.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const runtime = join(here, '..');
const build = join(runtime, '..', 'build', 'unit');

const run = (name: string): { status: number | null; output: string } => {
    mkdirSync(build, { recursive: true });
    const bin = join(build, name);
    const cc = (process.env.CURLY_CC ?? 'cc').split(' ');
    const built = spawnSync(cc[0]!, [...cc.slice(1), '-O1', '-Wall', `-I${runtime}`, '-o', bin, join(here, `${name}.c`), join(runtime, 'rt.c')], { encoding: 'utf8' });
    assert.equal(built.status, 0, built.stderr);
    const r = spawnSync('sh', ['-c', 'exec "$0" 2>&1', bin], { encoding: 'utf8' });
    return { status: r.status, output: r.stdout };
};

test('a fault: stdout first, then the line on stderr, then exit 1', () => {
    const r = run('fault');
    assert.equal(r.output, '1\n9223372036854775807\nfault: not a value at some dir/a "file".pl line 7.\n');
    assert.equal(r.status, 1);
});
