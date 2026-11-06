import { test } from 'node:test';
import assert from 'node:assert/strict';
import { read } from '../src/reader.ts';
import { show } from '../src/sexp.ts';
import { CompileError } from '../src/errors.ts';

test('integers, symbols and lists, with positions', () => {
    const forms = read('42 ; a comment\n(f -1 (g))');
    assert.deepEqual(forms.map(show), ['42', '(f -1 (g))']);
    assert.deepEqual(forms[1]!.pos, { line: 2, col: 1 });
    const inner = forms[1]!.kind === 'list' ? forms[1]!.items[2]! : forms[1]!;
    assert.deepEqual(inner.pos, { line: 2, col: 7 });
});

test('a lone minus is a symbol', () => {
    assert.equal(read('-')[0]!.kind, 'symbol');
});

test("a missing ')' is reported at the list's start", () => {
    assert.throws(() => read('\n  (1 2'), (e: unknown) =>
        e instanceof CompileError && e.line === 2 && e.col === 3);
});

// D9: an integer is an optional `-` and then digits, and nothing else.
test('what looks like a number but is not one is a symbol', () => {
    for (const text of ['+5', '1_0', '1.5', '0x10', '--1', '-']) {
        const forms = read(text);
        assert.equal(forms.length, 1, text);
        assert.deepEqual(forms[0]!.kind === 'symbol' ? forms[0]!.name : null, text);
    }
});

test('leading zeros and a negative zero are integers', () => {
    assert.deepEqual(read('007 -0').map(show), ['7', '0']);
    assert.deepEqual(read('007 -0').map((f) => f.kind), ['int', 'int']);
});

test('only space, newline, tab and carriage return separate atoms', () => {
    assert.deepEqual(read('1 2').map(show), ['1 2']);
    assert.equal(read('1 2')[0]!.kind, 'symbol');
    assert.deepEqual(read('1\t2\r3\n4 5').map(show), ['1', '2', '3', '4', '5']);
});
