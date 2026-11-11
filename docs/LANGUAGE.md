# SMOL

The language as it is, for someone writing programs in it. Each form is
added here in the same commit that adds it.

## Values

An integer, of any size, written in decimal with a `-` directly before the
digits for a negative. A string, in double quotes; it can't contain a `"`,
and it has no escapes yet. The constants `nil`, `true` and `false`. A
function, which prints as `<function>`.

An array is a list of values, written `Array.new(a, b, ...)`. A hash maps
strings to values, written `Hash.new(k, v, ...)`, with its key and value
pairs in turn. Arrays and hashes change in place, through their methods. A
name holds a reference to one: a `let` copies the reference, not the
contents, so a change made through one name is seen through every other.

The classes `Array` and `Hash` are made by the bootstrap, and each has the
method `new`, so `Array.new(...)` and `Hash.new(...)` are the ways to write
them. An array or a hash is not an instance, but it has a class: `Array` or
`Hash`, whose methods it answers (see Methods and Bootstrap).

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

## Programs

A program is statements separated by `;`, and the last may end with one.
An empty program does nothing. `//` starts a comment, which runs to the end
of the line.

## Statements

`let NAME = EXPR` binds the name for the statements after it. A later
`let` of the same name hides the earlier binding.

Any other statement is an expression.

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

The last parameter may be `%name`, which takes the rest of the arguments as
a hash, in pairs of key and value as for `Hash.new`. Those arguments must
come in pairs. With none left for it, it is an empty hash. A `%name`
parameter must be the last one.

`f(a, b)` calls `f`. The arguments are evaluated first, from left to right.
`f` must be a function, and the call must give as many arguments as `f` has
parameters. If its last parameter is `%name`, it needs at least as many as
it has before that.

`x.name(a, b)` calls the method `name` on `x`. An instance has the methods of
its class, as Instances says. An array, a hash, `true`, `false` and `nil` have
the methods of their classes in the same way (see Bootstrap). Every other value
has none, so a method call on it is a fault.

`catch(f)` is a built-in function, bound before the program starts, so a
`let` can shadow it. It calls `f` with no arguments. If that call raises a
fault, `catch` returns the fault's message as a string; otherwise it returns
`nil`. A fault in the argument itself, such as a value that isn't a function,
is not caught. `catch` takes exactly one argument.

## Methods

The methods below are the host's, in the method tables of the classes `Array`
and `Hash`. A method call on an array or a hash finds them there as it finds any
method, so it also finds the methods of `Object`, which `Array` and `Hash`
inherit from, and a method added to `Array`'s table is one every array answers.

An array has five methods. `push(x, ...)` adds its arguments to the end. It
returns the array, so calls chain. `get(i)` gives the item at index `i`,
counting from 0, or `nil` if `i` is past the end or negative. `set(i, x)`
replaces the item at `i`, which must be within the array, and returns the
array. `size()` gives the number of items. `includes(x)` is true if `x` is in the
array: scalars are equal by value, and anything else only as the same object.

A hash has four methods. `get(k)` gives the value for the key `k`, or `nil`
if there is none. `set(k, v)` stores a value under `k`, and returns the hash.
`keys()` gives an array of the keys, in the order they were first added.
`size()` gives the number of entries. A key is always a string.

`Array.new(a, b, ...)` and `Hash.new(k, v, ...)` are methods of the classes
`Array` and `Hash`, and they make an array or a hash. The other methods check
that their receiver is an array, or a hash: one called on anything else, such as
an instance whose class is `Array`, is the fault `NAME needs an array as its
receiver: VALUE`, or `a hash`.

## Instances

Five built-in functions, bound before the program starts as `catch` is.
Under Bootstrap are a sixth, `opaque_instance_set_class`, and
`set_primitive_class`, `host_method` and `reserve_ids`.
`fault(message, value)` raises a fault, whose message is the string and then
the value shown, separated by a space.

`create_opaque_instance(class, attrs)` makes an instance with that class
and those attrs, and gives it the next id. `attrs` must be a hash. It isn't
copied, so a later change to the hash is a change to the instance's attrs.

`opaque_instance_id(o)` gives the id of the instance `o`,
`opaque_instance_class(o)` its class, and `opaque_instance_attrs(o)` its
attrs, the hash itself. Each takes an instance and nothing else, except that
`opaque_instance_class` also gives the class of a value that has one without
being an instance: an array, a hash, `true`, `false` or `nil`. So
`Array.new(1).class()` is `Array`, but `Array.new(1).id()` is the fault
`not an opaque instance: [1]`.

`create_class(attrs)` makes a class: an instance of `Class`, as the sketch's
is (D26). Its attrs are a new hash with `"$name"` as `""`, `"$superclass"` as
`nil` and `"%methods"` as an empty hash, and then each entry of `attrs`,
which must be a hash, set over those.

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

## Bootstrap

Before every program, a prelude in `lib/prelude.smol` runs. It makes the
classes below the way a program makes any class, so they are the first
objects, numbered in this order: `Class` 1, `Object` 2, `Boolean` 3, `True` 4,
`False` 5, `UndefinedObject` 6, `Array` 7 and `Hash` 8, and then the classes of
`Array` and `Hash`, 9 and 10. It then calls `reserve_ids(100)`, so a program's
own objects start at 100, however many objects the bootstrap makes below that.
The prelude binds the names of the eight classes, and a program can use them.

`Class` is an instance of itself, and its superclass is `Object`. Its methods
are `name()`, which gives its name; `superclass()`, which gives its superclass;
`get_method(label)`, which gives the method under that label in its own
`"%methods"`, or `nil`; and `class_precedence_list()`, which gives an array of
the class, then its superclass, and so on up the chain until a superclass is
`nil`. If the chain loops back to a class it has already listed, that is the
fault `superclass chain loops back to VALUE`, which `catch` can take. Its
helper `cpl_into(acc)` adds the class to `acc` and walks on from there.

`Object` is an instance of `Class`, and it has no superclass. Its methods are
`new(key, value, ...)`, which makes an instance of the class it is called on,
with those pairs as its attrs; `id()`; `class()`; `isNil()`, which is false;
`isa(cls)`, which is true if `cls` is the value's class or a class above it on
its superclass chain; and `can(name)`, which is true if a method of that name
is found for the value, by the same lookup dispatch uses. A value with no class
answers false to both.

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
only that one. `not()` is on `Boolean`.

Because `Boolean` and `UndefinedObject` inherit from `Object`, they also answer
Object's methods: `true.class()` is `True`, `true.id()` is a fault, since `id`
needs an instance, and `nil.new()` makes an instance whose class is `nil`.

`Array` and `Hash` inherit from `Object`. Their `"%methods"` hold the methods
under Methods: `push`, `get`, `set`, `size` and `includes` for `Array`, and
`get`, `set`, `keys` and `size` for `Hash`. `new` is not a method of an array
but of the class, so it is in the table of the class's own class: `Array`'s
class is a class named `"Array class"`, whose superclass is `Class` and whose
one method is `new`, and the same for `Hash`. So `Array.name()` is `"Array"`,
and `Array.get_method("push")` is a function.

A constant, an array or a hash gets its class from `set_primitive_class(v, c)`,
which makes the instance `c` the class of `v`: of `true`, `false` or `nil`
itself, or of every array or every hash, by its kind. It gives back `c`. Any
other `v` is the fault `only true, false, nil, arrays and hashes take a class:
VALUE`, and a `c` that isn't an instance is `not an opaque instance: VALUE`.

`host_method(class, method)` gives the host's built-in function for a method of
`Array` or `Hash`, both named by strings: `host_method("Array", "push")`.
Anything else is the fault `no host method METHOD for CLASS`. The function takes
the receiver as its first argument, so it takes one more argument than the
method: `host_method("Array", "size")(Array.new(1, 2))` is 2. Called as a
method, the receiver is passed for it, and a wrong number of arguments counts
only the ones after it. `push` and `new` take any number.

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
`set_primitive_class` given a value other than `true`, `false`, `nil`, an array
or a hash, or a class that isn't an instance; a host method given a receiver
of the wrong kind; `host_method` given anything but a method of `Array` or
`Hash`; and `reserve_ids` given something other than an integer. A
method that isn't found is `no method found for NAME on VALUE`, for an
instance as for any other value. `can` given a name that isn't a string is a fault. A fault that `catch` takes
is not a fault of the program: the program carries on after the call to
`catch`.
