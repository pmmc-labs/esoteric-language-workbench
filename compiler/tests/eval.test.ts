import { test } from 'node:test';
import assert from 'node:assert/strict';
import { parse } from '../src/parser.ts';
import { program } from '../src/program.ts';
import { evaluate, show } from '../src/eval.ts';
import { Failure } from '../src/errors.ts';

// A program runs after the prelude, as the driver runs it, since arrays and
// hashes take their methods from the classes the prelude makes (D31). So a
// program's own objects start at 100 (D32).
const run = (src: string): string => {
    const v = evaluate(program(src));
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

test('a class is an object, and shows as one', () => {
    assert.equal(run('Array'), '<object 7>');
    assert.equal(run('Hash'), '<object 8>');
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

test('ids come from one counter, which starts again for each run', () => {
    const src = 'let $a = create_opaque_instance(nil, Hash.new()); opaque_instance_id(create_class(Hash.new()))';
    assert.equal(run(src), '101');
    assert.equal(run(src), '101');
});

test('only instances take ids: arrays, hashes and functions do not', () => {
    assert.equal(run('let @a = Array.new(); let $f = function () { 1 }; opaque_instance_id(create_opaque_instance(nil, Hash.new()))'), '100');
});

test('an instance shows as <object ID>, and its class may be nil', () => {
    assert.equal(run('create_opaque_instance(nil, Hash.new())'), '<object 100>');
    assert.equal(run('opaque_instance_class(create_opaque_instance(nil, Hash.new()))'), 'nil');
});

test('attrs that are not a Hash are a fault', () => {
    faults('create_opaque_instance(nil, 42)', 'attrs must be a Hash: 42');
    faults('create_opaque_instance(nil, Array.new())', 'attrs must be a Hash: []');
    faults('create_class(nil)', 'attrs must be a Hash: nil');
});

test('the readers fault on a value that is not an instance', () => {
    faults('opaque_instance_id(1)', 'not an opaque instance: 1');
    faults('opaque_instance_class(function () { 1 })', 'not an opaque instance: <function>');
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
    faults(`${FOO} create_opaque_instance($Foo, Hash.new()).nope()`, 'no method found for nope on <object 101>');
    faults('create_opaque_instance(create_opaque_instance(nil, Hash.new()), Hash.new()).m()', 'no method found for m on <object 101>');
    faults('create_opaque_instance("Foo", Hash.new()).m()', 'no method found for m on <object 100>');
    faults(`${FOO} let $Bar = create_opaque_instance(nil, Hash.new("$superclass", 42));
        create_opaque_instance($Bar, Hash.new()).foo()`, 'no method found for foo on <object 102>');
});

test('the receiver is self, and an arity fault counts only the arguments after it', () => {
    const cls = 'let $C = create_class(Hash.new("%methods", Hash.new("m", function (self, $x) { self }, "r", function (self, $x, %rest) { %rest })));';
    assert.equal(run(`${cls} create_opaque_instance($C, Hash.new()).m(1)`), '<object 101>');
    faults(`${cls} create_opaque_instance($C, Hash.new()).m(1, 2)`, 'wrong number of arguments: want 1, got 2');
    faults(`${cls} create_opaque_instance($C, Hash.new()).r()`, 'wrong number of arguments: want at least 1, got 0');
});

test('a method with no parameter for self is a fault, and so is a built-in that takes none', () => {
    faults('let $C = create_class(Hash.new("%methods", Hash.new("m", function (%rest) { 1 }))); create_opaque_instance($C, Hash.new()).m()',
        'a method needs a first parameter for self');
    assert.equal(run('let $C = create_class(Hash.new("%methods", Hash.new("id", opaque_instance_id))); create_opaque_instance($C, Hash.new()).id()'), '101');
    faults('let $C = create_class(Hash.new("%methods", Hash.new("id", opaque_instance_id))); create_opaque_instance($C, Hash.new()).id(1)',
        'wrong number of arguments: want 0, got 1');
});

test('arrays and hashes have their classes\' methods, and an instance of no class has none of them', () => {
    faults('create_opaque_instance(nil, Hash.new()).size()', 'no method found for size on <object 100>');
    assert.equal(run('Hash.new("a", 1).size()'), '1');
});

test("opaque_instance_set_class changes an instance's class, and only an instance's", () => {
    assert.equal(run('let $c = create_opaque_instance(nil, Hash.new()); opaque_instance_set_class($c, $c); opaque_instance_class($c)'), '<object 100>');
    faults('opaque_instance_set_class(1, nil)', 'not an opaque instance: 1');
});

test('set_primitive_class takes a class for true, false, nil, integers, strings, arrays and hashes only, and the class must be an instance', () => {
    faults('set_primitive_class(function () { 1 }, create_opaque_instance(nil, Hash.new()))', 'only true, false, nil, integers, strings, arrays and hashes take a class: <function>');
    faults('set_primitive_class(nil, 1)', 'not an opaque instance: 1');
});

test('without a class, a method on nil or a boolean is a fault', () => {
    // Without the prelude, nothing has registered a class.
    const bare = (src: string, message: string) => assert.throws(() => evaluate(parse(src)), (e: unknown) =>
        e instanceof Failure && e.message === message);
    bare('nil.foo()', 'no method found for foo on nil');
    bare('true.foo()', 'no method found for foo on true');
});

test('a method that a constant\'s class chain lacks is a fault', () => {
    faults('nil.foo()', 'no method found for foo on nil');
    faults('true.foo()', 'no method found for foo on true');
});

test('opaque_instance_class gives a registered primitive its class', () => {
    assert.equal(run('opaque_instance_class(Array.new())'), '<object 7>');
    assert.equal(run('opaque_instance_class(nil)'), '<object 6>');
    assert.equal(run('opaque_instance_class("a").name()'), '"String"');
    faults('opaque_instance_class(function () { 1 })', 'not an opaque instance: <function>');
});

test('host_method gives a builtin that takes the receiver first, and checks it', () => {
    assert.equal(run('host_method("Array", "push")(Array.new(1), 2, 3)'), '[1, 2, 3]');
    assert.equal(run('host_method("Hash", "new")(nil, "a", 1)'), '{"a": 1}');
    faults('host_method("Hash", "get")(Array.new(), "a")', 'get needs a hash as its receiver: []');
    faults('host_method("Array", "push")()', 'wrong number of arguments: want at least 1, got 0');
    faults('host_method("Array", 1)', 'no host method 1 for Array');
});

test('reserve_ids moves the next id forward only, and gives nil', () => {
    assert.equal(run('reserve_ids(200); opaque_instance_id(create_opaque_instance(nil, Hash.new()))'), '200');
    assert.equal(run('reserve_ids(5); opaque_instance_id(create_opaque_instance(nil, Hash.new()))'), '100');
    assert.equal(run('reserve_ids(5)'), 'nil');
    faults('reserve_ids(nil)', 'reserve_ids needs an integer: nil');
});

test('includes compares scalars by value and objects only as themselves', () => {
    assert.equal(run('Array.new(1, "a").includes("a")'), 'true');
    assert.equal(run('Array.new(1).includes(2)'), 'false');
    assert.equal(run('let $o = create_opaque_instance(nil, Hash.new()); Array.new($o).includes(create_opaque_instance(nil, Hash.new()))'), 'false');
});

test('fault raises its message, then the value shown, and needs a string message', () => {
    faults('fault("boom", 1)', 'boom 1');
    faults('fault(1, 2)', 'fault needs a string message: 1');
});

test('isa and can answer false for a value with no class, and can wants a string name', () => {
    assert.equal(run('host_method("Object", "can")(create_opaque_instance(nil, Hash.new()), "id")'), 'false');
    assert.equal(run('host_method("Object", "isa")(function () { 1 }, Object)'), 'false');
    faults('host_method("Object", "can")(1, 2)', 'can needs a method name as a string: 2');
});

test('integers and strings take the classes Integer and String (D36)', () => {
    assert.equal(run('host_method("Object", "isa")(42, Integer)'), 'true');
    assert.equal(run('host_method("Integer", "equals")(42, 42)'), 'true');
    assert.equal(run('host_method("String", "size")("a😀")'), '2');
});
