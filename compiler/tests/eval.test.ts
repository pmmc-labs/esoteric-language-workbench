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
