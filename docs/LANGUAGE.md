# SMOL

The language as it is, for someone writing programs in it. Each form is
added here in the same commit that adds it.
Each code block here is run by `make checks`, and the output block after it is what
it must print (D44).

## Values

An integer, of any size, written in decimal with a `-` directly before the
digits for a negative. A string, in double quotes; it can't contain a `"`,
and it has no escapes (D43). The constants `nil`, `true` and `false`. A
function, which prints as `<function>`.

```smol
print(42);
print(-7);
print(99999999999999999999.times(99999999999999999999));
print("hello");
print(nil);
print(true);
function (x) { x }
```

```output
42
-7
9999999999999999999800000000000000000001
"hello"
nil
true
<function>
```

An array is a list of values, written `Array.new(a, b, ...)`. A hash maps
strings to values, written `Hash.new(k, v, ...)`, with its key and value
pairs in turn. Arrays and hashes change in place, through their methods. A
name holds a reference to one: a `let` copies the reference, not the
contents, so a change made through one name is seen through every other.

```smol
let a = Array.new(1, 2);
let b = a;
b.push(3);
print(a);
let h = Hash.new("x", 1);
let g = h;
g.set("y", 2);
h
```

```output
[1, 2, 3]
{"x": 1, "y": 2}
```

The classes `Array` and `Hash` are made by the bootstrap, and each has the
method `new`, so `Array.new(...)` and `Hash.new(...)` are the ways to write
them. An array or a hash is not an instance, but it has a class: `Array` or
`Hash`, whose methods it answers (see Methods and Bootstrap). An integer and a
string have the classes `Integer` and `String` in the same way.

```smol
Array.new(7.class().name(), "s".class().name(), Array.new().class().name(), Hash.new().class().name())
```

```output
["Integer", "String", "Array", "Hash"]
```

An instance is an id, a class and attrs. The id is an integer, and each
instance made takes the next one. A program's own instances start at 100: the
bootstrap makes its objects first, and keeps the ids below 100 (see Bootstrap). The class is any value; it may be
`nil`. The attrs are a hash, which the instance holds by reference. A class
is an instance too, one whose attrs hold a method table under `"%methods"`
and a superclass under `"$superclass"`. The built-in functions under
Instances, below, make instances and read them.

## Names

A name is a letter or `_`, then letters, digits and `_`. It may begin with
a sigil, `$`, `@` or `%`, which is part of the name: `$a` and `@a` are two
different names. `let`, `function`, `nil`, `true` and `false` are keywords
and aren't names.

```smol
let $a = 1;
let @a = 2;
let %a = 3;
let a_1 = 4;
Array.new($a, @a, %a, a_1)
```

```output
[1, 2, 3, 4]
```

## Programs

A program is statements separated by `;`, and the last may end with one.
An empty program does nothing. `//` starts a comment, which runs to the end
of the line.

```smol
// A comment runs to the end of the line.
let x = 1; // so this one ends here
x.plus(1);
```

```output
2
```

## Statements

`let NAME = EXPR` binds the name for the statements after it. A later
`let` of the same name hides the earlier binding.

Any other statement is an expression.

```smol
let x = 1;
let f = function () { x };
let x = 2;
Array.new(x, f())
```

```output
[2, 1]
```

## Expressions

A name is its value. A constant is its value.

`function (PARAMS) { BODY }` is a function. PARAMS is a list of names,
separated by commas, that are distinct; it may be empty. BODY is statements,
as in a program, and it may be empty. The function's value is the value of
the last statement of its body, if that statement is an expression. A body
with no such statement gives `nil`. A function sees the names bound where it
is written, and not the names bound after it. A parameter is an ordinary
name, and so is `self`: a method is a function whose first parameter takes
the receiver, and `self` is the name used for it.

```smol
let add = function (a, b) { a.plus(b) };
let nothing = function () { };
let onlyLet = function () { let y = 1 };
let adder = function (n) { function (x) { x.plus(n) } };
let add10 = adder(10);
Array.new(add(2, 3), nothing(), onlyLet(), add10(5))
```

```output
[5, nil, nil, 15]
```

The last parameter may be `%name`, which takes the rest of the arguments as
a hash, in pairs of key and value as for `Hash.new`. Those arguments must
come in pairs. With none left for it, it is an empty hash. A `%name`
parameter must be the last one.

```smol
let tag = function (name, %opts) { Array.new(name, %opts) };
print(tag("a"));
tag("b", "size", 2, "color", "red")
```

```output
["a", {}]
["b", {"size": 2, "color": "red"}]
```

`f(a, b)` calls `f`. The arguments are evaluated first, from left to right.
`f` must be a function, and the call must give as many arguments as `f` has
parameters. If its last parameter is `%name`, it needs at least as many as
it has before that.

Here `add(1)` gives too few, and `catch` (below) takes the fault:

```smol
let add = function (a, b) { a.plus(b) };
let err = catch(function () { add(1) });
Array.new(add(1, 2), err.isNil(), err.class().name())
```

```output
[3, false, "String"]
```

`x.name(a, b)` calls the method `name` on `x`. An instance has the methods of
its class, as Instances says. An array, a hash, an integer, a string, `true`,
`false` and `nil` have the methods of their classes in the same way (see
Bootstrap). A function has none, so a method call on it is a fault.

The receiver `x` is any expression that is a name, a literal, a call or a method
call, so `42.size()` and `f(1).plus(2)` are both calls. There is no parenthesised
expression, and `(1).plus(2)` is a syntax error.

```smol
let double = function (n) { n.times(2) };
print(1.plus(2));
print("ab".concat("cd"));
print(double(1).plus(2));
print(Array.new(1, 2).size());
catch(function () { double.size() })
```

```output
3
"abcd"
4
2
"no method found for size on <function>"
```

`catch(f)` is a built-in function, bound before the program starts, so a
`let` can shadow it. It calls `f` with no arguments. If that call raises a
fault, `catch` returns the fault's message as a string; otherwise it returns
`nil`. A fault in the argument itself, such as a value that isn't a function,
is not caught. `catch` takes exactly one argument.

```smol
print(catch(function () { 1.divBy(0) }));
print(catch(function () { 1.divBy(1) }));
"carried on"
```

```output
"divBy by zero"
nil
"carried on"
```

`print(x)` is a built-in function too. It writes `x` and a newline, as Output
says the last value is written, and gives `x` back, so it can sit inside an
expression: `print(3).plus(4)` writes `3` and is 7 (D38).

```smol
print("first");
print(3).plus(4)
```

```output
"first"
3
7
```

## Methods

The methods below are the host's, in the method tables of the classes `Array`,
`Hash`, `Integer` and `String`. A method call on one of their values finds them
there as it finds any method, so it also finds the methods of `Object`, which
these classes inherit from, and a method added to `Array`'s table is one every
array answers.

An array has nine methods. `push(x, ...)` adds its arguments to the end. It
returns the array, so calls chain. `get(i)` gives the item at index `i`,
counting from 0, or `nil` if `i` is past the end or negative. `set(i, x)`
replaces the item at `i`, which must be within the array, and returns the
array. `size()` gives the number of items. `includes(x)` is true if `x` is in the
array: scalars are equal by value, and anything else only as the same object.
`pop()` removes the last item and gives it, or `nil` if the array is empty.
`indexOf(x)` gives the index of the first item equal to `x`, as `includes`
compares them, or -1 if there is none.

```smol
let xs = Array.new(10, 20).push(30, 40);
print(xs);
print(Array.new(xs.get(0), xs.get(9), xs.get(-1)));
xs.set(1, 25);
print(Array.new(xs.size(), xs.includes(25), xs.indexOf(40), xs.indexOf(99)));
print(xs.pop());
xs
```

```output
[10, 20, 30, 40]
[10, nil, nil]
[4, true, 3, -1]
40
[10, 25, 30]
```

SMOL has no loop: two of an array's methods take a block, which is a function,
and call it for each item in order (D40). `each(block)` calls `block(item)`,
and gives the array. `inject(acc, block)` calls `block(acc, item)` with `acc`
for the first item and with the last call's value for each one after, and gives
the value of the last call, or `acc` itself for an empty array. Both walk the
items the array had when the method was called, so a block may change the
array. A block is called as any function is: it must be a function that takes
that many arguments, and a fault inside it is a fault of the call.

```smol
let xs = Array.new(1, 2, 3, 4);
let squares = Array.new();
xs.each(function (x) { squares.push(x.times(x)) });
print(squares);
print(xs.inject(0, function (acc, x) { acc.plus(x) }));
Array.new().inject("empty", function (acc, x) { x })
```

```output
[1, 4, 9, 16]
10
"empty"
```

A hash has five methods. `get(k)` gives the value for the key `k`, or `nil`
if there is none. `set(k, v)` stores a value under `k`, and returns the hash.
`keys()` gives an array of the keys, in the order they were first added.
`size()` gives the number of entries. `has(k)` is true if there is an entry
under `k`, even one whose value is `nil`, which `get` can't tell from a missing
key. A key is always a string.

```smol
let h = Hash.new("a", 1).set("b", nil);
print(h.keys());
print(Array.new(h.get("b"), h.has("b"), h.get("c"), h.has("c")));
h.size()
```

```output
["a", "b"]
[nil, true, nil, false]
2
```

An integer has seven methods. `plus(n)`, `minus(n)` and `times(n)` give the sum,
the difference and the product of the integer and `n`. `n` must be an integer:
otherwise the fault is `plus needs an integer as its argument: VALUE`, with the
name of the method that was called. `divBy(n)` gives the quotient of the integer
by `n`, truncated toward zero, so `-7.divBy(2)` is -3 (D41). `n` must be an
integer, and if it is zero the fault is `divBy by zero`. There is no remainder.
`lessThan(n)` is true if the integer is less
than `n`, which must be an integer. `equals(n)` is true if `n` is the same
integer, and false for any other value, which is not a fault. `toString()` gives
the integer as a string of its decimal digits.

```smol
print(Array.new(7.plus(3), 7.minus(10), 7.times(6), 7.divBy(2), -7.divBy(2)));
print(Array.new(3.lessThan(4), 3.equals(3), 3.equals("3")));
print(12.toString().concat("!"));
catch(function () { 1.plus(nil) })
```

```output
[10, -3, 42, 3, -3]
[true, true, false]
"12!"
"plus needs an integer as its argument: nil"
```

A string has three methods. `size()` gives the number of characters, which are
Unicode code points, so an emoji counts as one. `concat(s)` gives the string
followed by `s`, which must be a string. `equals(s)` is true if `s` is the same
string, and false for any other value.

```smol
let s = "smol";
print(Array.new(s.size(), "🍎".size()));
print(s.concat(" talk"));
Array.new(s.equals("smol"), s.equals(4))
```

```output
[4, 1]
"smol talk"
[true, false]
```

`Array.new(a, b, ...)` and `Hash.new(k, v, ...)` are methods of the classes
`Array` and `Hash`, and they make an array or a hash. The other methods check
that their receiver is of their class's kind: one called on anything else, such
as an instance whose class is `Array`, is the fault `NAME needs an array as its
receiver: VALUE`. The others say `a hash`, `an integer` or `a string`.

## Instances

Five built-in functions make and read instances: `create_opaque_instance`,
`opaque_instance_id`, `opaque_instance_class`, `opaque_instance_attrs` and
`create_class`, described below. Like `catch`, they are bound before the program
starts. The bootstrap adds `opaque_instance_set_class`, `set_primitive_class`,
`host_method` and `reserve_ids`, which Bootstrap describes.

`fault(message, value)` is a separate built-in. It raises a fault, whose message
is the string and then the value shown, separated by a space. The value is shown
as Output shows it, so a string value is in quotes.

```smol
catch(function () { fault("too small:", 3) })
```

```output
"too small: 3"
```

`create_opaque_instance(class, attrs)` makes an instance with that class
and those attrs, and gives it the next id. `attrs` must be a hash. It isn't
copied, so a later change to the hash is a change to the instance's attrs.

`opaque_instance_id(o)` gives the id of the instance `o`,
`opaque_instance_class(o)` its class, and `opaque_instance_attrs(o)` its
attrs, the hash itself. Each takes an instance and nothing else, except that
`opaque_instance_class` also gives the class of a value that has one without
being an instance: an integer, a string, an array, a hash, `true`, `false` or
`nil`. So
`Array.new(1).class()` is `Array`, but `Array.new(1).id()` is the fault
`not an opaque instance: [1]`.

```smol
let attrs = Hash.new("x", 1);
let o = create_opaque_instance(nil, attrs);
let p = create_opaque_instance(nil, Hash.new());
attrs.set("y", 2);
print(opaque_instance_attrs(o));
print(opaque_instance_class(o));
print(opaque_instance_id(p).minus(opaque_instance_id(o)));
print(opaque_instance_class(5).name());
catch(function () { Array.new(1).id() })
```

```output
{"x": 1, "y": 2}
nil
1
"Integer"
"not an opaque instance: [1]"
```

`create_class(attrs)` makes a class: an instance of `Class`, as the sketch's
is (D26). Its attrs are a new hash with `"$name"` as `""`, `"$superclass"` as
`nil` and `"%methods"` as an empty hash, and then each entry of `attrs`,
which must be a hash, set over those.

```smol
let Point = create_class(Hash.new("$name", "Point"));
let attrs = opaque_instance_attrs(Point);
Array.new(opaque_instance_class(Point).name(), attrs.get("$name"), attrs.get("$superclass"), attrs.get("%methods"))
```

```output
["Class", "Point", nil, {}]
```

`o.name(a, b)` on an instance looks for the method, starting at the
instance's class. It takes the hash under `"%methods"` in that class's
attrs, and looks up `name` there; the keys of a method table are plain
method names. If the name isn't there, it goes on to the class under
`"$superclass"`, and so on up until that is `nil`, where the method isn't
found. A class that has no hash under `"%methods"` has no methods of its
own. A class that isn't an instance has no methods and no superclass.

The method found is called with `o` as its first argument, then `a` and
`b`. So a method is written `function (self, $a, $b) { ... }`, and it must
have a first parameter to take the receiver. The check on the number of
arguments, and its message, count only the arguments after the receiver.
The method's value is the value of the call.

A class's `"%methods"` are for its instances. A method call on the class
itself starts at the class's own class, as for any instance.

```smol
let Base = create_class(Hash.new(
  "$name", "Base",
  "%methods", Hash.new("hello", function (self, who) { "hello ".concat(who) })));
let Sub = create_class(Hash.new("$name", "Sub", "$superclass", Base));
let s = create_opaque_instance(Sub, Hash.new());
print(s.hello("there"));
Sub.name()
```

```output
"hello there"
"Sub"
```

## Bootstrap

Before every program, a prelude in `lib/prelude.smol` runs. It makes the
classes below the way a program makes any class, so they are the first
objects, numbered in this order: `Class` 1, `Object` 2, `Boolean` 3, `True` 4,
`False` 5, `UndefinedObject` 6, `Array` 7 and `Hash` 8, then the classes of
`Array` and `Hash`, 9 and 10, and then `Integer` 11 and `String` 12. It then
calls `reserve_ids(100)`, so a program's own objects start at 100, however many
objects the bootstrap makes below that. The prelude binds the names of these
classes, and a program can use them.

`Class` is an instance of itself, and its superclass is `Object`. Its methods
are `name()`, which gives its name; `superclass()`, which gives its superclass;
`get_method(label)`, which gives the method under that label in its own
`"%methods"`, or `nil`; `find_method(label)`, which gives the method under that
label in its own `"%methods"` or, if it has none there, in its superclass's and
so on up the chain, or `nil` if no class on the chain has it; `define(label,
fn)`, which puts `fn` under that label in its own `"%methods"`, and gives the
class back; and `class_precedence_list()`, which gives an array of
the class, then its superclass, and so on up the chain until a superclass is
`nil`. If the chain loops back to a class it has already listed, that is the
fault `superclass chain loops back to VALUE`, which `catch` can take. Its
helper `cpl_into(acc)` adds the class to `acc` and walks on from there.
`find_method` gives the same fault when its walk comes back to a class it has
searched, and its helper is `find_method_from(label, seen)`.

```smol
let Shape = create_class(Hash.new("$name", "Shape", "$superclass", Object));
Shape.define("area", function (self) { 0 }).define("describe", function (self) {
  self.class().name().concat(" of area ").concat(self.area().toString())
});
let Square = create_class(Hash.new("$name", "Square", "$superclass", Shape));
Square.define("area", function (self) { self.attr("side").times(self.attr("side")) });
print(Square.superclass().name());
print(Array.new(Square.get_method("describe"), Square.find_method("describe")));
print(Square.class_precedence_list().size());
Square.new("side", 3).describe()
```

```output
"Shape"
[nil, <function>]
3
"Square of area 9"
```

There is no `super` form (D39). A method calls the one above it by asking the
superclass of the class it is written for: `Puppy.superclass().find_method("speak")(self)`.
The method found is a function, and it is called with `self` as its first
argument, as a method call would call it. The name `Puppy` must be bound where
the method is written, so such a method is added with `Puppy.define(...)`,
after the `let` that binds the class.

```smol
let Dog = create_class(Hash.new("$name", "Dog", "$superclass", Object));
Dog.define("speak", function (self) { "Woof" });
let Puppy = create_class(Hash.new("$name", "Puppy", "$superclass", Dog));
Puppy.define("speak", function (self) {
  Puppy.superclass().find_method("speak")(self).concat("!")
});
Puppy.new().speak()
```

```output
"Woof!"
```

`Object` is an instance of `Class`, and it has no superclass. Its methods are
`new(key, value, ...)`, which makes an instance of the class it is called on,
with those pairs as its attrs; `id()`; `class()`; `isNil()`, which is false;
`attr(name)`, which gives the value under `name` in the instance's attrs, or
`nil` if there is none; `setAttr(name, value)`, which stores the value there
and gives the instance back, so calls chain (D42);
`isa(cls)`, which is true if `cls` is the value's class or a class above it on
its superclass chain; and `can(name)`, which is true if a method of that name
is found for the value, by the same lookup dispatch uses. A value with no class
answers false to both when `host_method` gives the method. A method call on such
a value finds nothing, so it is a fault. Such a value is a function, or an
instance whose class is `nil`.

```smol
let Box = create_class(Hash.new("$name", "Box", "$superclass", Object));
let b = Box.new("size", 1);
b.setAttr("size", 2).setAttr("color", "red");
print(Array.new(b.attr("size"), b.attr("color"), b.attr("weight")));
print(Array.new(b.class().name(), b.isNil(), nil.isNil()));
Array.new(b.isa(Box), b.isa(Object), 5.isa(Box), b.can("attr"), b.can("fly"))
```

```output
[2, "red", nil]
["Box", false, true]
[true, true, false, true, false]
```

`Class.new("$name", "Foo", "$superclass", Object, "%methods", Hash.new(...))`
makes a class. `create_class(attrs)` also makes a class, an instance of `Class`,
as the sketch's is (D26). `opaque_instance_set_class(o, c)` sets an instance's
class, and gives back `o`.

Conditionals are methods of booleans (D27). `Boolean` is the parent of `True`
and `False`, and both inherit from `Object`. `true` belongs to `True`, `false`
to `False`, and `nil` to `UndefinedObject`, which also inherits from `Object`
and answers `isNil()` with true (D29). Each conditional takes blocks, which are
functions of no arguments. `ifTrue(block)` on `true` runs the block, and on
`false` gives `nil` without running anything; `ifFalse(block)` is the other
way round; `ifTrueFalse(whenTrue, whenFalse)` runs one of its two blocks, and
only that one. Each conditional's value is the value of the block it runs, or
`nil` when `ifTrue` or `ifFalse` runs no block. `not()` is on `Boolean`.

```smol
let sign = function (n) {
  n.lessThan(0).ifTrueFalse(function () { "negative" }, function () { "not negative" })
};
print(sign(-3));
print(sign(4));
print(true.ifTrue(function () { "ran" }));
print(true.ifFalse(function () { "ran" }));
print(false.not());
true.class().name()
```

```output
"negative"
"not negative"
"ran"
nil
true
"True"
```

Because `Boolean` and `UndefinedObject` inherit from `Object`, they also answer
Object's methods: `true.class()` is `True`, `true.id()` is a fault, since `id`
needs an instance, and `nil.new()` makes an instance whose class is `nil`.

`Array` and `Hash` inherit from `Object`. Their `"%methods"` hold the methods
under Methods: `push`, `get`, `set`, `size`, `includes`, `pop`, `each`, `inject`
and `indexOf` for `Array`, and `get`, `set`, `keys`, `size` and `has` for `Hash`. `new` is not a method of an array
but of the class, so it is in the table of the class's own class: `Array`'s
class is a class named `"Array class"`, whose superclass is `Class` and whose
one method is `new`, and the same for `Hash`. So `Array.name()` is `"Array"`,
and `Array.get_method("push")` is a function.

A constant, an integer, a string, an array or a hash gets its class from
`set_primitive_class(v, c)`, which makes the instance `c` the class of `v`: of
`true`, `false` or `nil` itself, or of every integer, string, array or hash, by
its kind. It gives back `c`. A program may call it at any time, so it can change
a class for the rest of its run (D37). Any other `v` is the fault `only true,
false, nil, integers, strings, arrays and hashes take a class: VALUE`, and a `c`
that isn't an instance is `not an opaque instance: VALUE`.

`host_method(class, method)` gives the host's built-in function for a method of
`Array`, `Hash`, `Integer`, `String` or `Object`, both named by strings: `host_method("Array", "push")`.
Anything else is the fault `no host method METHOD for CLASS`. The function takes
the receiver as its first argument, so it takes one more argument than the
method: `host_method("Array", "size")(Array.new(1, 2))` is 2. Called as a
method, the receiver is passed for it, and a wrong number of arguments counts
only the ones after it. `push` and `new` take any number.

```smol
let size = host_method("Array", "size");
print(size(Array.new(1, 2)));
catch(function () { size(5) })
```

```output
2
"size needs an array as its receiver: 5"
```

`reserve_ids(n)` makes the next id at least `n`. It never moves the next id
back, and it gives `nil`. An `n` that isn't an integer is the fault
`reserve_ids needs an integer: VALUE`.

## Output

The program prints the value of its last statement, if that statement is an
expression, and then a newline. Integers print in decimal, strings in double
quotes, functions as `<function>`, and the constants as `nil`, `true` and
`false`. An array prints as `[1, "two"]` and a hash as `{"a": 1}`, with keys
in the order they were added. An array or hash that holds itself prints as
`[...]` or `{...}` where the cycle starts. An instance prints as
`<object ID>`, where ID is its id: `<object 1>`. A class is an instance, so
`Array` prints as `<object 7>`.
A program whose last statement is a `let` prints nothing. The program then
exits 0.

```smol
let xs = Array.new(1);
xs.push(xs);
print(Hash.new("a", 1, "b", Array.new(true, false)));
print(xs);
Array.new(1, "two", nil, Array.name())
```

```output
{"a": 1, "b": [true, false]}
[1, [...]]
[1, "two", nil, "Array"]
```

`print(x)` writes `x` in the same way, and a newline, when it is called. So a
program's output is a line for each call of `print`, in the order of the calls,
and then the last value. A string is written in its quotes by `print` too.

Here the last statement is a `let`, so the one line is the one `print` wrote:

```smol
print("only this");
let x = 1
```

```output
"only this"
```

A string literal can't contain a `"`, and no method makes one, so a printed
string needs no escaping. A fault's message can contain one, since it shows a
string value in quotes, as Output does, and `catch` gives the message back. A
string can't hold a newline either: `print` is the way to start a new line.

## Faults

A syntax error is reported as `FILE:LINE:COLUMN: MESSAGE` on stderr, and the
program exits 1. A fault is `fault: MESSAGE` on stderr, and the program exits
1; anything printed before it is kept. The faults so far are: an unbound
name; a call of something that isn't a function; a call with the wrong number
of arguments; a method that isn't found, including any method on a value
that has none; an index that isn't an integer; a `set` index that is out of
range; a hash key that isn't a string; key-value arguments with a key
and no value; attrs that aren't a hash; a value that isn't an instance where
one is needed; and a method with no first parameter for the receiver; a superclass
chain that loops back to a class it has already searched;
`set_primitive_class` given a value other than `true`, `false`, `nil`, an
integer, a string, an array or a hash, or a class that isn't an instance; a host
method given a receiver of the wrong kind; an integer or string method given an
argument of the wrong kind; `divBy` given zero, which is `divBy by zero`; `host_method` given anything but a method of
`Array`, `Hash`, `Integer`, `String` or `Object`; and `reserve_ids` given
something other than an integer. A
method that isn't found is `no method found for NAME on VALUE`, for an
instance as for any other value. `can` given a name that isn't a string is a fault. A fault that `catch` takes
is not a fault of the program: the program carries on after the call to
`catch`.

A fault that nothing catches ends the program, after what it printed:

```smol
print("start");
fault("bad value:", 42);
print("never")
```

```output
"start"
fault: bad value: 42
exit: 1
```

A fault that `catch` takes lets the program carry on:

```smol
print(catch(function () { 5.fly() }));
"carried on"
```

```output
"no method found for fly on 5"
"carried on"
```

## A larger example

A shelf in a shop holds a few items, each with a price in whole units. The
program tries to shelve eight items, prints a line for each, and refuses four
of them. Then it prints where each item went, the total, and the cheapest
item, and ends with a value.

```smol
let Item = create_class(Hash.new(
  "$name", "Item",
  "$superclass", Object,
  "%methods", Hash.new(
    "price", function (self) { self.attr("price") },
    "label", function (self) {
      self.attr("name").concat(" at ").concat(self.price().toString())
    })));
let SaleItem = create_class(Hash.new("$name", "SaleItem", "$superclass", Item));
SaleItem.define("price", function (self) { self.attr("price").minus(self.attr("off")) });
SaleItem.define("label", function (self) {
  SaleItem.superclass().find_method("label")(self).concat(" (sale)")
});

let Shelf = create_class(Hash.new(
  "$name", "Shelf",
  "$superclass", Object,
  "%methods", Hash.new(
    "add", function (self, item) {
      let items = self.attr("items");
      let slots = self.attr("slots");
      let name = item.attr("name");
      item.price().lessThan(1).ifTrue(function () { fault("price must be positive, got", item.price()) });
      slots.has(name).ifTrue(function () { fault("already on the shelf in slot", slots.get(name)) });
      items.size().lessThan(self.attr("capacity")).ifFalse(function () { fault("shelf is full at", items.size()) });
      slots.set(name, items.size());
      items.push(item);
      self
    },
    "total", function (self) {
      self.attr("items").inject(0, function (sum, item) { sum.plus(item.price()) })
    })));
Shelf.define("cheapest", function (self) {
  let items = self.attr("items");
  items.inject(items.get(0), function (best, item) {
    item.price().lessThan(best.price()).ifTrueFalse(function () { item }, function () { best })
  })
});

let shelf = Shelf.new("items", Array.new(), "slots", Hash.new(), "capacity", 4);
let tries = Array.new(
  Item.new("name", "tea", "price", 4),
  SaleItem.new("name", "jam", "price", 6, "off", 3),
  Item.new("name", "bread", "price", 0),
  Item.new("name", "honey", "price", 9),
  Item.new("name", "tea", "price", 5),
  Item.new("name", "rice", "price", 2),
  Item.new("name", "salt", "price", 1),
  Item.new("name", "air", "price", nil));
let refused = Array.new();
tries.each(function (item) {
  let err = catch(function () { shelf.add(item) });
  err.isNil().ifTrueFalse(
    function () { print("added ".concat(item.label())) },
    function () { refused.push(err); print("refused ".concat(item.attr("name")).concat(": ").concat(err)) })
});
print(shelf.attr("slots"));
print("total ".concat(shelf.total().toString()));
print("cheapest ".concat(shelf.cheapest().label()));
Array.new(shelf.attr("items").size(), refused.size(), tries.get(1).isa(Item), tries.get(0).isa(SaleItem))
```

```output
"added tea at 4"
"added jam at 3 (sale)"
"refused bread: price must be positive, got 0"
"added honey at 9"
"refused tea: already on the shelf in slot 0"
"added rice at 2"
"refused salt: shelf is full at 4"
"refused air: no method found for lessThan on nil"
{"tea": 0, "jam": 1, "honey": 2, "rice": 3}
"total 18"
"cheapest rice at 2"
[4, 4, true, false]
```

The classes are made as Instances says, with `create_class` and `Hash.new`, and
`"$superclass"` set to `Object`, so that items and the shelf answer `new`,
`attr`, `setAttr`, `isa` and the rest of Object's methods (Bootstrap). The state
of each object is its attrs, read with `attr`. `SaleItem` adds its methods with
`define` once its name is bound, and its `label` is a super call:
`SaleItem.superclass().find_method("label")(self)` runs Item's `label` with the
sale item as `self`, so the `price()` inside it is the sale price.

`add` refuses three ways, each with `fault` and an integer value (Instances),
and a fourth refusal is a fault the program didn't raise itself: `nil` has no
`lessThan` (Faults). The loop over the items is `each`, and each call of `add`
is under `catch`, so a refused item is printed and the loop goes on
(Expressions). The duplicate check is `has` on the `slots` hash, and the total
and the cheapest item are folds with `inject` (Methods). The choice in
`cheapest` and the refusals are conditionals, which are methods of booleans that
take blocks (Bootstrap). Each line is written by `print`, and the last value is
the array at the end (Output).
