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

const run = (name: string, arg = '', env: Record<string, string> = {}): { status: number | null; output: string } => {
    mkdirSync(build, { recursive: true });
    const bin = join(build, name);
    const cc = (process.env.CURLY_CC ?? 'cc').split(' ');
    const built = spawnSync(cc[0]!, [...cc.slice(1), '-O1', '-Wall', `-I${runtime}`, '-o', bin, join(here, `${name}.c`), join(runtime, 'rt.c'), '-lm'], { encoding: 'utf8' });
    assert.equal(built.status, 0, built.stderr);
    // The knobs are the test's own to set: none comes in from outside.
    const clean = Object.fromEntries(Object.entries(process.env).filter(([name]) => !name.startsWith('CURLY_GC_') && name !== 'CURLY_HEAP_CAP'));
    const r = spawnSync('sh', ['-c', 'exec "$0" "$1" 2>&1', bin, arg], { encoding: 'utf8', env: { ...clean, ...env } });
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

test('and so do the comparisons and the tests of truth (step 4)', () => {
    const numbers = ['num_eq-left', 'num_eq-right', 'num_ne-left', 'num_ne-right', 'num_lt-left', 'num_lt-right', 'num_gt-left', 'num_gt-right', 'num_le-left', 'num_le-right', 'num_ge-left', 'num_ge-right', 'num_cmp-left', 'num_cmp-right'];
    const values = ['str_eq-left', 'str_eq-right', 'str_ne-left', 'str_ne-right', 'str_lt-left', 'str_lt-right', 'str_gt-left', 'str_gt-right', 'str_le-left', 'str_le-right', 'str_ge-left', 'str_ge-right', 'str_cmp-left', 'str_cmp-right'].concat(['xor-left', 'xor-right', 'not', 'defined', 'is-true', 'is-false', 'is-undef']);
    for (const [cases, what] of [[numbers, 'not a numeric value'], [values, 'not a value']] as const) {
        for (const which of cases) {
            const r = run('tags', which);
            assert.equal(r.output, `2\nfault: ${what} at tags.pl line 3.\n`, which);
            assert.equal(r.status, 1, which);
        }
    }
});

test('and so do the steps and the assigning operators (step 5)', () => {
    const numbers = ['inc', 'dec', 'add_to-left', 'add_to-right', 'sub_from-left', 'sub_from-right'];
    const values = ['before-inc', 'concat_to-left', 'concat_to-right'];
    for (const [cases, what] of [[numbers, 'not a numeric value'], [values, 'not a value'],
        [['add_to-undef', 'sub_from-undef'], 'undef where a number is wanted'], [['concat_to-undef'], 'undef where a string is wanted']] as const) {
        for (const which of cases) {
            const r = run('tags', which);
            assert.equal(r.output, `2\nfault: ${what} at tags.pl line 3.\n`, which);
            assert.equal(r.status, 1, which);
        }
    }
});

test('a repeated string of 2^31 characters is too long', () => {
    assert.deepEqual(run('limit'), { status: 1, output: '2000\nfault: repeated string too long at limit.pl line 5.\n' });
});

// ---- the collector (step 7; D26, D63 to D66). Each count below is worked
// out from the case in collect.c, which says how.

test('a string in a slot is kept, and one in no slot is freed', () => {
    assert.deepEqual(run('collect', 'kept-and-freed'), { status: 0, output: [
        'made: 2 on the heap, 2 made, 0 collections', 'collected: 1 on the heap, 2 made, 1 collections', 'ab1',
        'and again: 0 on the heap, 2 made, 2 collections', '',
    ].join('\n') });
    assert.deepEqual(run('collect', 'every-slot'), { status: 0, output: 'four held: 4 on the heap, 4 made, 1 collections\nab0\nab1\nab2\nab3\n' });
});

test('a constant is not on the heap, and a number as a string is on no heap either', () => {
    assert.deepEqual(run('collect', 'constant'), { status: 0, output: 'ab\ncollected: 0 on the heap, 0 made, 2 collections\n' });
    // Under stress the one allocation of the join is a collection too.
    const ways: Record<string, string>[] = [{}, { CURLY_GC_STRESS: '1', CURLY_GC_POISON: '1' }];
    for (const env of ways) {
        assert.deepEqual(run('collect', 'numbers', env), { status: 0, output: [
            `joined: 1 on the heap, 1 made, ${'CURLY_GC_STRESS' in env ? 1 : 0} collections`,
            `read: 1 on the heap, 1 made, ${'CURLY_GC_STRESS' in env ? 1 : 0} collections`, '121.5', '20', '1', '2', '',
        ].join('\n') });
    }
});

test('every frame is walked, the older as the newest', () => {
    assert.deepEqual(run('collect', 'two-frames'), { status: 0, output: [
        'both open: 2 on the heap, 2 made, 1 collections', 'ab1', 'ab2', 'the newer closed: 1 on the heap, 2 made, 2 collections', 'ab1', '',
    ].join('\n') });
});

test('a string used after it was collected is an internal error, every way one is read', () => {
    const dead = 'ab1\ninternal: a string was used after it was collected at collect.pl line 1.\n';
    for (const which of ['used-after', 'number-after', 'truth-after']) {
        assert.deepEqual(run('collect', which, { CURLY_GC_POISON: '1' }), { status: 2, output: dead }, which);
    }
    // In the operation that reads it, when the collection is that operation's own.
    for (const which of ['operand-after', 'repeat-after', 'case-after', 'substr-after']) {
        assert.deepEqual(run('collect', which, { CURLY_GC_STRESS: '1', CURLY_GC_POISON: '1' }), { status: 2, output: dead }, which);
    }
    // (And with no collection in the way each is the operation it is.)
    assert.deepEqual(run('collect', 'repeat-after'), { status: 0, output: 'ab1\nab1ab1\n' });
    assert.deepEqual(run('collect', 'case-after'), { status: 0, output: 'ab1\nAB1\n' });
    assert.deepEqual(run('collect', 'substr-after'), { status: 0, output: 'ab1\nb1\n' });
    assert.deepEqual(run('collect', 'slot-after', { CURLY_GC_POISON: '1' }),
        { status: 2, output: 'ab1\ninternal: a slot holds a string that was collected at collect.pl line 1.\n' });
});

test('a frame opens with no value in any slot, whatever the C stack held', () => {
    assert.deepEqual(run('collect', 'opens-empty'), { status: 0, output: 'collected: 0 on the heap, 0 made, 1 collections\n' });
});

test('a frame left open, or closed out of turn, is an internal error', () => {
    assert.deepEqual(run('collect', 'left-open'), { status: 2, output: 'internal: a frame was left open at collect.pl line 1.\n' });
    assert.deepEqual(run('collect', 'closed-out-of-turn'), { status: 2, output: 'internal: a frame was closed that is not the newest at collect.pl line 1.\n' });
});

// A block is 24 bytes of header, 32 of rt_str, the string and its NUL:
// 1057 for a kilobyte. 993 of them are the megabyte that brings a
// collection, so the 994th allocation collects, and every 993rd after:
// 100 times in 100,000. The last was before allocation 99,301, and left
// the one string a slot held: 701 are on the heap at the end.
test('with no knob, a collection comes when a megabyte has been allocated since the last (D66)', () => {
    assert.deepEqual(run('collect', 'policy'), { status: 0, output: '100000 made, 100 collections, 701 on the heap, 740957 bytes held\n' });
    // And waits for as much again as was live: 6 MB held, and 4 MB more is no collection.
    assert.deepEqual(run('collect', 'policy-grows'), { status: 0, output: '0 collections for two more\n' });
});

test('the cap is on what is held: garbage passes under it, and what is kept does not (D65)', () => {
    assert.deepEqual(run('collect', 'cap', { CURLY_HEAP_CAP: '4096' }), { status: 1, output: [
        'garbage: 2 on the heap, 1000 made, 499 collections', 'held 1', 'held 2', 'held 3', 'fault: out of memory at collect.pl line 1.', '',
    ].join('\n') });
    // Under poison the dead are held too: the same garbage is too much.
    assert.deepEqual(run('collect', 'cap', { CURLY_HEAP_CAP: '4096', CURLY_GC_POISON: '1' }),
        { status: 1, output: 'fault: out of memory at collect.pl line 1.\n' });
    assert.equal(run('collect', 'cap').status, 0);
});

test('a knob is a whole number in digits, and anything else stops the program before it starts (D63)', () => {
    const bad = (name: string, value: string, most: string) =>
        assert.deepEqual(run('collect', 'constant', { [name]: value }),
            { status: 2, output: `curly: ${name} is '${value}': it is a whole number from 0 to ${most}, in digits\n` }, `${name}=${value}`);
    for (const value of ['abc', '-1', '1.5', ' 1', '0x10', '4294967296']) bad('CURLY_GC_STRESS', value, '4294967295');
    for (const value of ['2', 'yes', 'true']) bad('CURLY_GC_POISON', value, '1');
    for (const value of ['16M', '4611686018427387905', '99999999999999999999999']) bad('CURLY_HEAP_CAP', value, '4611686018427387904');
    // Unset, empty and 0 are off, and the largest of each is taken.
    const fine = 'ab\ncollected: 0 on the heap, 0 made, 2 collections\n';
    const off: Record<string, string>[] = [{ CURLY_GC_STRESS: '' }, { CURLY_GC_STRESS: '0', CURLY_GC_POISON: '0', CURLY_HEAP_CAP: '0' }, { CURLY_GC_STRESS: '00012' },
        { CURLY_GC_STRESS: '4294967295', CURLY_GC_POISON: '1', CURLY_HEAP_CAP: '4611686018427387904' }];
    for (const env of off) {
        assert.deepEqual(run('collect', 'constant', env), { status: 0, output: fine }, JSON.stringify(env));
    }
});
