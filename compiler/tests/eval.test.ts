import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parse } from '../src/parser.ts';
import { evaluate, show } from '../src/eval.ts';
import { Failure } from '../src/errors.ts';

const run = (src: string): string => {
    const v = evaluate(parse(src));
    return v === undefined ? '' : show(v);
};

// A fault raised with this message.
const faults = (src: string, message: string) => assert.throws(() => run(src), (e: unknown) =>
    e instanceof Failure && e.message === message);

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
    faults('let $f = function ($a) { $a }; $f()', 'wrong number of arguments: want 1, got 0');
});

test('catch gives nil when the function raises no fault', () => {
    assert.equal(run('catch(function () { 1 })'), 'nil');
});

test('catch gives the message of a fault raised by the function, as a string', () => {
    assert.equal(run('catch(function () { $nope })'), '"unbound name: $nope"');
});

test('a fault in the call catch makes is caught too', () => {
    assert.equal(run('catch(function ($a) { $a })'), '"wrong number of arguments: want 1, got 0"');
});

test('a fault in the argument to catch is not caught', () => {
    faults('catch(42)', 'not a function: 42');
});

test('catch itself takes exactly one argument', () => {
    faults('catch()', 'wrong number of arguments: want 1, got 0');
});

test('a nested catch catches its own fault, and the outer one sees no fault', () => {
    assert.equal(run('catch(function () { catch(function () { $nope }) })'), 'nil');
});

test('catch is an ordinary name, so a let can shadow it', () => {
    assert.equal(run('let catch = 5; catch'), '5');
});

test('an array shows its items, and push returns the array so calls chain', () => {
    assert.equal(run('let @a = Array.new(); @a.push(1).push(2); @a'), '[1, 2]');
});

test('a missing index gives nil, and setting past the end is a fault', () => {
    assert.equal(run('Array.new(10).get(5)'), 'nil');
    faults('Array.new(1).set(1, 2)', 'index 1 is out of range for an array of 1');
});

test('a hash keeps its keys in insertion order, and a missing key gives nil', () => {
    assert.equal(run('Hash.new("b", 1, "a", 2).keys()'), '["b", "a"]');
    assert.equal(run('Hash.new().get("nope")'), 'nil');
});

test('a hash key must be a string', () => {
    faults('Hash.new(42, 1)', 'a hash key must be a string: 42');
});

test('arrays are references: a let copies the reference, not the contents', () => {
    assert.equal(run('let @a = Array.new(); let @b = @a; @b.push(1); @a.size()'), '1');
});

test('an array can hold itself, and the printed form stops at the cycle', () => {
    assert.equal(run('let @a = Array.new(); @a.push(@a); @a'), '[[...]]');
});

test('a class shows as <class NAME>', () => {
    assert.equal(run('Array'), '<class Array>');
});

test('a scalar has no methods yet', () => {
    faults('42.size()', 'no method found for size on 42');
});

test('a %name parameter collects the rest as a Hash', () => {
    assert.equal(run('function ($a, %rest) { %rest }(1, "k", 2)'), '{"k": 2}');
    assert.equal(run('function (%rest) { %rest }()'), '{}');
});

test('a %name parameter needs its arguments in pairs', () => {
    faults('function (%rest) { %rest }("a")', '%rest needs key and value pairs: an even number of arguments');
});

test('with a %name parameter, the fixed parameters still need their arguments', () => {
    faults('function ($a, %rest) { $a }()', 'wrong number of arguments: want at least 1, got 0');
});
