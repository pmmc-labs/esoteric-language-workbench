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
