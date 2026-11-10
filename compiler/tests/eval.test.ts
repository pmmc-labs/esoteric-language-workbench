import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parse } from '../src/parser.ts';
import { evaluate, show } from '../src/eval.ts';
import { Failure } from '../src/errors.ts';

const run = (src: string): string => {
    const v = evaluate(parse(src));
    return v === undefined ? '' : show(v);
};

test('integers are exact at any size', () => {
    assert.equal(run('123456789012345678901234567890'), '123456789012345678901234567890');
});

test('a later let hides an earlier one, and sigils make different names', () => {
    assert.equal(run('let $x = 1; let $x = 2; $x'), '2');
    assert.equal(run('let $a = 1; let @a = 2; $a'), '1');
});

test('a fault has no position, since the program has run', () => {
    assert.throws(() => run('$nope'), (e: unknown) =>
        e instanceof Failure && e.pos === undefined && e.message === 'unbound name: $nope');
});

test('a program that ends in a let has no value', () => {
    assert.equal(run('let $x = 1'), '');
});

test('strings show in double quotes', () => {
    assert.equal(run('"hi"'), '"hi"');
});

test('a function captures the names bound where it is written, not later ones', () => {
    assert.equal(run('let $x = 1; let $f = function () { $x }; let $x = 2; $f()'), '1');
});

test('a call binds its arguments to the parameters in order', () => {
    assert.equal(run('function ($a, $b) { $b }(1, "two")'), '"two"');
});

test('a body with no value gives nil, and so does an empty body', () => {
    assert.equal(run('function () {}()'), 'nil');
    assert.equal(run('function () { let $y = 1 }()'), 'nil');
});

test('a function shows as <function>', () => {
    assert.equal(run('function () { 1 }'), '<function>');
});

test('a wrong number of arguments is a fault', () => {
    assert.throws(() => run('let $f = function ($a) { $a }; $f()'), (e: unknown) =>
        e instanceof Failure && e.message === 'wrong number of arguments: want 1, got 0');
});
