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

test('and so does everything that wants a string, or a whole number', () => {
    const strings = ['say', 'print', 'concat-left', 'concat-right', 'repeat-left', 'length', 'uc', 'lc', 'ord',
        'substr2-1', 'substr3-1', 'index2-1', 'index2-2', 'index3-1', 'index3-2'];
    const numbers = ['repeat-right', 'chr', 'substr2-2', 'substr3-2', 'substr3-3', 'index3-3'];
    for (const [cases, what] of [[strings, 'not a value'], [numbers, 'not a numeric value']] as const) {
        for (const which of cases) {
            const r = run('tags', which);
            assert.equal(r.output, `2\nfault: ${what} at tags.pl line 3.\n`, which);
            assert.equal(r.status, 1, which);
        }
    }
});

// The second and third characters of the four are three bytes and four.
test('strings are counted in characters, whatever their bytes', () => {
    assert.deepEqual(run('strings'), { status: 0, output: [
        'chr 233: 2 bytes, 1 character', 'chr 9786: 3 bytes, 1 character', 'chr 128512: 4 bytes, 1 character',
        'joined: 10 bytes, 4 characters', 'repeated: 30 bytes, 12 characters', 'substr 1, 2: 7 bytes, 2 characters',
        'index of the last: 3', 'a NUL in the middle: 3 bytes, 3 characters', '12 as a string: 2 bytes, 2 characters',
        'a literal ends with a NUL that is not its own: 0', '',
    ].join('\n') });
});

// What perl makes of each is in docs/briefs/claims.py (T79), by sprintf.
test('the sign of a zero', () => {
    assert.deepEqual(run('zero'), { status: 0, output: [
        '-(0.0): negative Num', '-(-(0.0)): Num', '0 * -1.5: negative Num', '0.0 * -1: Int', '0 / -5: negative Num',
        '-(0.0) + 0: Int', '-(0): Int', '0', '',
    ].join('\n') });
});

test('a repeated string of 2^31 characters is too long', () => {
    assert.deepEqual(run('limit'), { status: 1, output: '2000\nfault: repeated string too long at limit.pl line 5.\n' });
});
