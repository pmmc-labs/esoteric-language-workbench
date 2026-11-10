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

test('ids come from one counter, which starts again at 1 for each run', () => {
    const src = 'let $a = create_opaque_instance(nil, Hash.new()); opaque_instance_id(create_class(Hash.new()))';
    assert.equal(run(src), '2');
    assert.equal(run(src), '2');
});

test('only instances take ids: arrays, hashes and functions do not', () => {
    assert.equal(run('let @a = Array.new(); let $f = function () { 1 }; opaque_instance_id(create_opaque_instance(nil, Hash.new()))'), '1');
});

test('an instance shows as <object ID>, and its class may be nil', () => {
    assert.equal(run('create_opaque_instance(nil, Hash.new())'), '<object 1>');
    assert.equal(run('opaque_instance_class(create_opaque_instance(nil, Hash.new()))'), 'nil');
});

test('attrs that are not a Hash are a fault', () => {
    faults('create_opaque_instance(nil, 42)', 'attrs must be a Hash: 42');
    faults('create_opaque_instance(nil, Array.new())', 'attrs must be a Hash: []');
    faults('create_class(nil)', 'attrs must be a Hash: nil');
});

test('the readers fault on a value that is not an instance', () => {
    faults('opaque_instance_id(1)', 'not an opaque instance: 1');
    faults('opaque_instance_class(nil)', 'not an opaque instance: nil');
    faults('opaque_instance_attrs("a")', 'not an opaque instance: "a"');
});

test('an instance holds its attrs by reference', () => {
    assert.equal(run('let %a = Hash.new(); let $i = create_opaque_instance(nil, %a); %a.set("$x", 1); opaque_instance_attrs($i)'), '{"$x": 1}');
});

test('create_class copies the given attrs over the defaults', () => {
    assert.equal(run('let %a = Hash.new("$name", "Foo"); let $c = create_class(%a); %a.set("$late", 1); opaque_instance_attrs($c)'),
        '{"$name": "Foo", "$superclass": nil, "%methods": {}}');
});

const FOO = 'let $Foo = create_class(Hash.new("%methods", Hash.new("foo", function (self) { "Foo->foo" })));';

test('the chain walk finds a method in the class, then in each superclass', () => {
    assert.equal(run(`${FOO} create_opaque_instance($Foo, Hash.new()).foo()`), '"Foo->foo"');
    assert.equal(run(`${FOO} let $Bar = create_class(Hash.new("$superclass", $Foo));
        let $Baz = create_class(Hash.new("$superclass", $Bar)); create_opaque_instance($Baz, Hash.new()).foo()`), '"Foo->foo"');
});

test('a class with no "%methods", or one that is not a Hash, has no methods and the walk goes on', () => {
    assert.equal(run(`${FOO} let $Bar = create_opaque_instance(nil, Hash.new("$superclass", $Foo));
        create_opaque_instance($Bar, Hash.new()).foo()`), '"Foo->foo"');
    assert.equal(run(`${FOO} let $Bar = create_opaque_instance(nil, Hash.new("$superclass", $Foo, "%methods", 42));
        create_opaque_instance($Bar, Hash.new()).foo()`), '"Foo->foo"');
});

test('the walk ends at nil, at a class with no "$superclass", and at a class that is not an instance', () => {
    faults(`${FOO} create_opaque_instance($Foo, Hash.new()).nope()`, 'no method found for nope on <object 2>');
    faults('create_opaque_instance(create_opaque_instance(nil, Hash.new()), Hash.new()).m()', 'no method found for m on <object 2>');
    faults('create_opaque_instance("Foo", Hash.new()).m()', 'no method found for m on <object 1>');
    faults(`${FOO} let $Bar = create_opaque_instance(nil, Hash.new("$superclass", 42));
        create_opaque_instance($Bar, Hash.new()).foo()`, 'no method found for foo on <object 3>');
});

test('the receiver is self, and an arity fault counts only the arguments after it', () => {
    const cls = 'let $C = create_class(Hash.new("%methods", Hash.new("m", function (self, $x) { self }, "r", function (self, $x, %rest) { %rest })));';
    assert.equal(run(`${cls} create_opaque_instance($C, Hash.new()).m(1)`), '<object 2>');
    faults(`${cls} create_opaque_instance($C, Hash.new()).m(1, 2)`, 'wrong number of arguments: want 1, got 2');
    faults(`${cls} create_opaque_instance($C, Hash.new()).r()`, 'wrong number of arguments: want at least 1, got 0');
});

test('a method with no parameter for self is a fault, and so is a built-in that takes none', () => {
    faults('let $C = create_class(Hash.new("%methods", Hash.new("m", function (%rest) { 1 }))); create_opaque_instance($C, Hash.new()).m()',
        'a method needs a first parameter for self');
    assert.equal(run('let $C = create_class(Hash.new("%methods", Hash.new("id", opaque_instance_id))); create_opaque_instance($C, Hash.new()).id()'), '2');
    faults('let $C = create_class(Hash.new("%methods", Hash.new("id", opaque_instance_id))); create_opaque_instance($C, Hash.new()).id(1)',
        'wrong number of arguments: want 0, got 1');
});

test('arrays and hashes keep their own methods, and an instance has none of them', () => {
    faults('create_opaque_instance(nil, Hash.new()).size()', 'no method found for size on <object 1>');
    assert.equal(run('Hash.new("a", 1).size()'), '1');
});

test("opaque_instance_set_class changes an instance's class, and only an instance's", () => {
    assert.equal(run('let $c = create_opaque_instance(nil, Hash.new()); opaque_instance_set_class($c, $c); opaque_instance_class($c)'), '<object 1>');
    faults('opaque_instance_set_class(1, nil)', 'not an opaque instance: 1');
});
