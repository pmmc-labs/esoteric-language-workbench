// The runtime's own tests: C programs that call it directly, for what no
// compiled program can reach yet. Each is built with the C compiler the
// driver uses and run with stdout and stderr down one pipe, as t/run.sh
// reads a test's.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync } from 'node:fs';
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

test('a formatted string of 2^31 characters is too long, and is counted before it is made (step 16b)', () => {
    assert.deepEqual(run('format'), { status: 1, output: '11\nfault: formatted string too long at format.pl line 6.\n' });
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

// The limit on recursion (D68): the numbers by hand. A frame counts 1,024
// bytes and 16 a slot; 4 MB is 4,096 frames of no slots.
test('an open frame counts against the limit on recursion, and a closed one no longer does (D68)', () => {
    const head = 'one frame of no slots: 1024\nand one of forty: 2688\nboth closed: 0\n';
    assert.deepEqual(run('deep', '4096'), { status: 0, output: head + '4096 open: 4194304\nclosed: 0\n' });
    assert.deepEqual(run('deep', '4097'), { status: 1, output: head + 'fault: recursion too deep at deep.pl line 7.\n' });
});

// The count must run out before the C stack does, so a program that was
// given less stack than the count assumes is stopped before it starts.
test('a program given a stack of less than 8 MB does not start (D68)', () => {
    run('deep', '1');
    const r = spawnSync('sh', ['-c', 'ulimit -s 4096 && exec "$0" 1 2>&1', join(build, 'deep')], { encoding: 'utf8' });
    assert.deepEqual({ status: r.status, output: r.stdout },
        { status: 2, output: 'curly: the stack is limited to 4194304 bytes, and a program needs 8388608 (ulimit -s)\n' });
});

// Arrays under the collector (step 9; D80). The numbers by hand: a block's
// header is 24 bytes and an array 64 after it (40 until step 12, when it
// gained the three words a hash's index needs), so an empty array holds 88;
// its first storage is for 8 values, 128 bytes; the string `ab1` is 24 of
// header, 32 of rt_str, 3 bytes and a NUL, 60.
test('an array in a slot keeps what it holds, and one a slot lets go is freed with its storage', () => {
    assert.deepEqual(run('arrays', 'kept-through'), { status: 0, output: [
        'made: 3 on the heap, 3 made, 0 collections, 336 bytes held',
        'collected: 2 on the heap, 3 made, 1 collections, 276 bytes held',
        'ab1',
        'and again: 0 on the heap, 3 made, 2 collections, 0 bytes held', ''].join('\n') });
});

test('an array in no slot is collected, and one used after that is an internal error', () => {
    assert.deepEqual(run('arrays', 'dropped', { CURLY_GC_POISON: '1' }), { status: 2, output:
        'collected: 0 on the heap, 1 made, 1 collections, 88 bytes held\ninternal: an array was used after it was collected at arrays.pl line 1.\n' });
});

test("an array's values count against the cap, and an array holds no array", () => {
    // 4,096 values are 65,536 bytes; the next needs as much again.
    assert.deepEqual(run('arrays', 'storage', { CURLY_HEAP_CAP: '100000' }), { status: 1, output: 'pushing\nfault: out of memory at arrays.pl line 1.\n' });
    assert.deepEqual(run('arrays', 'storage', { CURLY_HEAP_CAP: '200000' }), { status: 1, output: 'pushing\nfault: out of memory at arrays.pl line 1.\n' });
    assert.deepEqual(run('arrays', 'storage', { CURLY_HEAP_CAP: '300000' }), { status: 0, output: 'pushing\nnot reached\n' });
    assert.deepEqual(run('arrays', 'no-array-in-an-array'), { status: 1, output: 'fault: not a value at arrays.pl line 1.\n' });
});

test('every way an array is changed, and read at the edges of the integers', () => {
    // (1,2,3) pushed onto itself is 6; unshifted, 9; the last off, 3; the
    // first off, 1; seven are left. A store at 9 makes it ten long. The
    // last two out, and three in.
    assert.deepEqual(run('arrays', 'every-way'), { status: 0, output: '6\n9\n3\n1\n2312312\n5\n9\n\n5\n\n\n2\n11\n' });
});

// The freeze (step 9b; D17, D80): a count, and while it is not 0 every way
// of changing the array faults, and every way of reading it works.
test('a frozen array is read and not changed, until it is given back as often as it was frozen', () => {
    const frozen = 'fault: an array was changed while a foreach is over it at arrays.pl line 1.\n';
    // Read while frozen twice: 3, 2, 3, 1, 2, and a list of it, 123. Given
    // back once, it is frozen still.
    for (const way of ['push', 'unshift', 'pop', 'shift', 'splice', 'store', 'make', 'assign', 'rest']) {
        assert.deepEqual(run('arrays', `frozen-${way}`), { status: 1, output: '3\n2\n3\n1\n2\n123\n' + frozen }, way);
    }
    // Given back twice, everything works again: four values after a push.
    assert.deepEqual(run('arrays', 'frozen-none'), { status: 0, output: '3\n2\n3\n1\n2\n123\n4\n' });
    assert.deepEqual(run('arrays', 'thaw-unfrozen'), { status: 2, output: 'internal: an array that no foreach is over was given back at arrays.pl line 1.\n' });
});

test("a foreach's own: an element that must be there, and the ends of a range", () => {
    // The last element by either index; 1 to 3 has values, 3 to 1 none, and
    // the ends are cut toward zero; the smallest end perl takes.
    assert.deepEqual(run('arrays', 'strict'), { status: 0, output: '3\n3\n1 1 3\n0 3 1\n1 -1 1\n1 -9223372036854775295 0\n' });
    const past = 'fault: an element past the end of the array in a foreach, where perl would make it at arrays.pl line 1.\n';
    assert.deepEqual(run('arrays', 'strict-past'), { status: 1, output: past });
    assert.deepEqual(run('arrays', 'strict-before'), { status: 1, output: past });
    const low = 'fault: a foreach over a range that begins or ends this near the smallest integer: perl refuses it at arrays.pl line 1.\n';
    assert.deepEqual(run('arrays', 'range-low'), { status: 1, output: low });
    assert.deepEqual(run('arrays', 'range-low-end'), { status: 1, output: low });
    assert.deepEqual(run('arrays', 'range-string'), { status: 1, output: 'fault: a string as the end of a range at arrays.pl line 1.\n' });
    assert.deepEqual(run('arrays', 'range-string-from'), { status: 1, output: 'fault: a string as the end of a range at arrays.pl line 1.\n' });
});

// Step 10a. By hand: true and (1, ab, 2.5) are four values; reversed after
// them, 2.5 ab 1; joined by `ab` (1, ab, ab, ab, 2.5), and by 0; a join of nothing is the empty
// string; a list of none has no one value, and a list of one has it; the
// slurpy array is 7, then 5 and 6, then ab and 2.5, and nothing for a
// start past the last argument.
test('a list added to a list, reversed, joined, and taken by a slurpy parameter', () => {
    const out = '4\n11ab2.52.5ab1\n1ababab2.5\n1010ab02.502.50ab01\n0\n1\n7\n7\n756ab2.5\n';
    assert.deepEqual(run('arrays', 'handed-'), { status: 0, output: out });
    assert.deepEqual(run('arrays', 'handed-join-undef'), { status: 1, output: out + 'fault: undef where a string is wanted at arrays.pl line 1.\n' });
    assert.deepEqual(run('arrays', 'handed-separator-undef'), { status: 1, output: out + 'fault: undef where a string is wanted at arrays.pl line 1.\n' });
    assert.deepEqual(run('arrays', 'handed-only-two'), { status: 2, output: out + 'internal: a sub that gives no list gave one at arrays.pl line 1.\n' });
});

// The sort machine (step 10c; D82, D83), held to perl: for the 4,200 lists
// of t/models/merge.py, under four ways of comparing (one of them no order
// at all), the pairs it asks for are the pairs perl's sort hands a block,
// in perl's order, and the values come out as perl has them. With a sort
// begun and ended in the middle of every fifth comparison of a fourth of
// them, which leaves the outer one where it was.
test("the sort machine asks for perl's pairs, in perl's order", () => {
    // (The model is found from wherever this file is: a copy of the tree
    // made to be broken has the runtime and not the models.)
    let root = here;
    while (!existsSync(join(root, 't', 'models', 'merge.py')) && dirname(root) !== root) root = dirname(root);
    const cases = spawnSync('python3', [join(root, 't', 'models', 'merge.py'), '--cases'], { encoding: 'utf8', maxBuffer: 1 << 28 }).stdout;
    assert.equal(cases.split('\n').length, 4201);
    const perl = `use v5.42;
        while (my $line = <STDIN>) {
            chomp $line;
            my ($how, @v) = split / /, $line;
            my (@log, @s);
            if ($how eq 'n') { @s = sort { push @log, "$a,$b"; $a <=> $b } @v; }
            elsif ($how eq 'r') { @s = sort { push @log, "$a,$b"; $b <=> $a } @v; }
            elsif ($how eq 'm') { @s = sort { push @log, "$a,$b"; ($a * 7 + $b * 13) % 3 - 1 } @v; }
            else { @s = sort { push @log, "$a,$b"; ($a % 10) <=> ($b % 10) } @v; }
            say "|", join(" ", @log);
            say join(" ", @s);
        }`;
    const said = spawnSync(process.env.CURLY_PERL ?? 'perl', ['-e', perl], { input: cases, encoding: 'utf8', maxBuffer: 1 << 28 });
    assert.equal(said.status, 0, said.stderr);
    run('sortm', '');
    const ours = spawnSync(join(build, 'sortm'), [], { input: cases, encoding: 'utf8', maxBuffer: 1 << 28 });
    assert.equal(ours.status, 0, ours.stderr);
    const [theirs, mine] = [said.stdout.split('\n'), ours.stdout.split('\n')];
    assert.equal(mine.length, theirs.length);
    const differ = mine.findIndex((line, n) => line !== theirs[n]);
    assert.equal(differ, -1, `line ${differ + 1}: ${mine[differ]?.slice(0, 200)} where perl has ${theirs[differ]?.slice(0, 200)}`);
    // A fault in the middle of a sort stops the program as any does.
    const stopped = spawnSync(join(build, 'sortm'), ['stop'], { input: 'n 3 1 2 5 4 9 8 7\n', encoding: 'utf8' });
    assert.deepEqual([stopped.status, stopped.stderr], [1, 'fault: undef where a number is wanted at sortm.pl line 1.\n']);
});

// Hashes (step 12a; D27). The numbers by hand: an empty hash is the 88
// bytes an empty array is; its first storage is for 8 values, 128 bytes,
// and its first index 8 slots of 4 bytes, 32; `ab1` is 60, as above.
test('a hash in a slot keeps its keys and values, and one a slot lets go is freed with its storage and its index', () => {
    assert.deepEqual(run('hash', 'kept-through'), { status: 0, output: [
        'made: 4 on the heap, 4 made, 0 collections, 428 bytes held',
        'collected: 3 on the heap, 4 made, 1 collections, 368 bytes held',
        'ab2',
        'and again: 0 on the heap, 4 made, 2 collections, 0 bytes held', ''].join('\n') });
    assert.deepEqual(run('hash', 'dropped', { CURLY_GC_POISON: '1' }), { status: 2, output:
        'collected: 0 on the heap, 1 made, 1 collections, 88 bytes held\ninternal: a hash was used after it was collected at hash.pl line 1.\n' });
});

test('a key is a string, however it was given, and is made one once, as it is stored', () => {
    assert.deepEqual(run('hash', 'number-key'), { status: 0, output: '2 made\nab\nab\n5 made\n3\n4\n\n1\n7,1,,1.5|2,3,4,5|4\n' });
});

test("a hash keeps the order its keys were first stored in (D27)", () => {
    assert.deepEqual(run('hash', 'order'), { status: 0, output: [
        'a,b,c,d|1,2,3,4|4',
        '', 'a,b,c,d|1,22,3,4|4',
        '22', '', 'a,c,d|1,3,4|3',
        'a,c,d,b|1,3,4,5|4',
        '', 'a,c,d,b,k|1,3,4,5,6|5',
        '12', 'a,c,d,b,k|9,3,4,5,6|5',
        'c,d,b,k,a|3,4,5,6,9|5',
        '||0', ''].join('\n') });
});

test('ten thousand keys are each found, the deleted ones alone are gone, and the order holds', () => {
    const output = '10000\n50005000\n5000\n5000 found, 5000 missing\nk9991,k9995,k9997,k9999,a,k9993|9991,9995,9997,9999,0,1|6\n';
    assert.deepEqual(run('hash', 'grow'), { status: 0, output });
    // And with a collection at every allocation, nothing it needs is lost.
    assert.deepEqual(run('hash', 'grow', { CURLY_GC_STRESS: '1', CURLY_GC_POISON: '1' }), { status: 0, output });
});

// 5,000 keys: storage for 16,384 values, 262,144 bytes; an index of 16,384
// slots, 65,536; the hash, 88; and the keys, 56 bytes and their digits and
// a NUL each, 303,890: 631,658 in all.
test("a hash's pairs and its index count against the cap", () => {
    assert.deepEqual(run('hash', 'storage', { CURLY_HEAP_CAP: '631657' }), { status: 1, output: 'storing\nfault: out of memory at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'storage', { CURLY_HEAP_CAP: '631658' }), { status: 0, output: 'storing\nstored\n' });
    // Without the index it would fit in 566,122.
    assert.deepEqual(run('hash', 'storage', { CURLY_HEAP_CAP: '600000' }), { status: 1, output: 'storing\nfault: out of memory at hash.pl line 1.\n' });
});

test("a hash's faults", () => {
    assert.deepEqual(run('hash', 'odd'), { status: 1, output: '1|2|1\nfault: an odd number of values for a hash at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'undef-key'), { status: 1, output: 'fault: undef where a string is wanted at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'whole-num-key'), { status: 1, output: 'fault: a whole float this size prints two ways in perl (add 0 to print the integer) at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'no-array-in-a-hash'), { status: 1, output: 'fault: not a value at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'no-hash-in-an-array'), { status: 1, output: 'fault: not a value at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'not-a-hash'), { status: 1, output: 'fault: not a hash at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'not-an-array'), { status: 1, output: 'fault: not an array at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'put-nowhere'), { status: 2, output: 'internal: a key that was made is not there at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'put-in-a-hole'), { status: 2, output: 'internal: a key that was made is not there at hash.pl line 1.\n' });
});

test('a frozen hash is read, and every change to it is a fault', () => {
    const read = '1\n\n\na,b,c,d|1,2,3,4|4\n';
    for (const way of ['store', 'new', 'make', 'delete', 'assign']) {
        assert.deepEqual(run('hash', `frozen-${way}`), { status: 1, output: read + 'fault: a hash was changed while a foreach is over it at hash.pl line 1.\n' }, way);
    }
    assert.deepEqual(run('hash', 'frozen-none'), { status: 0, output: read + '5\n' });
});

// Step 12b: what stands on a hash. The hash is a, b, c, d with 1 to 4; the
// keys asked for are a, k and d, and k is not there.
test('an element and a slice of a hash where perl would make a key (T216)', () => {
    assert.deepEqual(run('hash', 'on-strict'), { status: 1, output: '4\nfault: a key that is not there in a foreach, where perl would make it at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'on-slice'), { status: 0, output: '3\n1\n\n4\n4\n' });
    assert.deepEqual(run('hash', 'on-slice-strict'), { status: 1, output: '3\n1\n\n4\n4\nfault: a slice with a key that is not there, where perl would make it at hash.pl line 1.\n' });
});

test('a slice of a hash stored to and deleted, and of an array stored to (T228)', () => {
    assert.deepEqual(run('hash', 'on-store'), { status: 0, output: '5\n10\n20\n\n1\na,b,c,d,k\n' });
    assert.deepEqual(run('hash', 'on-store-frozen'), { status: 1, output: 'fault: a hash was changed while a foreach is over it at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'on-delete'), { status: 0, output: '3\n1\n\n4\nb,c|2,3|2\n' });
    assert.deepEqual(run('hash', 'on-delete-frozen'), { status: 1, output: 'fault: a hash was changed while a foreach is over it at hash.pl line 1.\n' });
    assert.deepEqual(run('hash', 'on-array'), { status: 0, output: '5\n9\n\n' });
    assert.deepEqual(run('hash', 'on-array-before'), { status: 1, output: 'fault: an element before the start of the array at hash.pl line 1.\n' });
});

test('a hash as a last parameter is filled from the arguments left, and an odd number is a fault (T226)', () => {
    assert.deepEqual(run('hash', 'on-parameter'), { status: 1, output: "k,a|1,2|2\na|2|1\nfault: an odd number of arguments for f's hash at hash.pl line 1.\n" });
});
