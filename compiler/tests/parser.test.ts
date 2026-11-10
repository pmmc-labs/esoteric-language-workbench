import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parse } from '../src/parser.ts';
import { Failure } from '../src/errors.ts';

// A syntax error with this message, at this position.
const at = (message: string, line: number, col: number) => (e: unknown) =>
    e instanceof Failure && e.message === message && e.pos?.line === line && e.pos?.col === col;

test('statements are separated by ;, and the last may end with one', () => {
    assert.equal(parse('1; 2;').length, 2);
    assert.equal(parse('1; 2').length, 2);
    assert.equal(parse('').length, 0);
    assert.equal(parse('// nothing but a comment').length, 0);
});

test('a method call takes its receiver, and a name keeps its sigil', () => {
    assert.deepEqual(parse('$a.size(1, "x")'), [{ kind: 'expr', expr: {
        kind: 'method', recv: { kind: 'name', name: '$a' }, name: 'size',
        args: [{ kind: 'int', value: 1n }, { kind: 'str', value: 'x' }] } }]);
});

test('a let names the binding it makes', () => {
    assert.deepEqual(parse('let @xs = nil'), [{ kind: 'let', name: '@xs', expr: { kind: 'const', name: 'nil' } }]);
});

test('a minus directly before a digit is part of the integer', () => {
    assert.deepEqual(parse('-5'), [{ kind: 'expr', expr: { kind: 'int', value: -5n } }]);
});

test("a missing '=' is reported where it is", () => {
    assert.throws(() => parse('let $x 42'), at("expected '=' after $x, found 42", 1, 8));
});

test('two statements need a ; between them', () => {
    assert.throws(() => parse('42 42'), at("expected ';' or the end of the program, found 42", 1, 4));
});

test('a string that never ends is reported where it starts', () => {
    assert.throws(() => parse('"abc'), at('unterminated string', 1, 1));
});

test('a sigil needs a name after it', () => {
    assert.throws(() => parse('$ = 1'), at("expected a name after '$'", 1, 1));
});

test('a plain name is not an expression statement on its own', () => {
    assert.throws(() => parse('x = 1'), at("expected ';' or the end of the program, found '='", 1, 3));
});
