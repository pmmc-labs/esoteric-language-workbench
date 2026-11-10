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

test('a function literal has its parameters and its body', () => {
    assert.deepEqual(parse('function ($a, $b) { $a }'), [{ kind: 'expr', expr: {
        kind: 'function', params: ['$a', '$b'], body: [{ kind: 'expr', expr: { kind: 'name', name: '$a' } }] } }]);
});

test('a function body may be empty, and a function can be called where it is written', () => {
    assert.deepEqual(parse('function () {}()'), [{ kind: 'expr', expr: {
        kind: 'call', fn: { kind: 'function', params: [], body: [] }, args: [] } }]);
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

test('a parameter is listed once', () => {
    assert.throws(() => parse('function ($a, $a) {}'), at('duplicate parameter $a', 1, 15));
});

test('a parameter is a name', () => {
    assert.throws(() => parse('function (1) { 1 }'), at('expected a parameter name, found 1', 1, 11));
});

test("a function body ends with a '}'", () => {
    assert.throws(() => parse('function () { 1'), at("expected ';' or '}', found the end of the program", 1, 16));
});

test('function is a keyword, so it is not a name', () => {
    assert.throws(() => parse('let function = 1'), at("expected a name after 'let', found 'function'", 1, 5));
});
