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

const run = (name: string, arg = ''): { status: number | null; output: string } => {
    mkdirSync(build, { recursive: true });
    const bin = join(build, name);
    const cc = (process.env.CURLY_CC ?? 'cc').split(' ');
    const built = spawnSync(cc[0]!, [...cc.slice(1), '-O1', '-Wall', `-I${runtime}`, '-o', bin, join(here, `${name}.c`), join(runtime, 'rt.c'), '-lm'], { encoding: 'utf8' });
    assert.equal(built.status, 0, built.stderr);
    const r = spawnSync('sh', ['-c', 'exec "$0" "$1" 2>&1', bin, arg], { encoding: 'utf8' });
    return { status: r.status, output: r.stdout };
};

test('a fault: stdout first, then the line on stderr, then exit 1', () => {
    const r = run('fault');
    assert.equal(r.output, '1\n9223372036854775807\nfault: not a value at some dir/a "file".pl line 7.\n');
    assert.equal(r.status, 1);
});

test('every operator faults on an operand that is no number', () => {
    const cases = ['add-left', 'add-right', 'sub-left', 'sub-right', 'mul-left', 'mul-right', 'div-left', 'div-right',
        'mod-left', 'mod-right', 'pow-left', 'pow-right', 'neg'];
    for (const which of cases) {
        const r = run('tags', which);
        assert.equal(r.output, '2\nfault: not a numeric value at tags.pl line 3.\n', which);
        assert.equal(r.status, 1, which);
    }
    // And with nothing wrong, nothing faults.
    assert.deepEqual(run('tags'), { status: 0, output: '2\n2\n' });
});

// What perl makes of each is in docs/briefs/claims.py (T79), by sprintf.
test('the sign of a zero', () => {
    assert.deepEqual(run('zero'), { status: 0, output: [
        '-(0.0): negative Num', '-(-(0.0)): Num', '0 * -1.5: negative Num', '0.0 * -1: Int', '0 / -5: negative Num',
        '-(0.0) + 0: Int', '-(0): Int', '0', '',
    ].join('\n') });
});
