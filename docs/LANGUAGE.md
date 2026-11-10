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

The classes `Array` and `Hash` are bound before the program starts. Each
has the one method `new`, which makes an instance, so `Array.new(...)` and
`Hash.new(...)` are the ways to write them.

An instance is an id, a class and attrs. The id is an integer, and each
instance made takes the next one. A program's own instances start at 3, after
the two the bootstrap makes (see Bootstrap). The class is any value; it may be
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

`x.name(a, b)` calls the method `name` on `x`. Arrays, hashes and the
classes `Array` and `Hash` have methods, listed below. An instance has the
methods of its class, as Instances says. Every other value has none, so a
method call on it is a fault.

`catch(f)` is a built-in function, bound before the program starts, so a
`let` can shadow it. It calls `f` with no arguments. If that call raises a
fault, `catch` returns the fault's message as a string; otherwise it returns
`nil`. A fault in the argument itself, such as a value that isn't a function,
is not caught. `catch` takes exactly one argument.

## Methods

An array has four methods. `push(x, ...)` adds its arguments to the end. It
returns the array, so calls chain. `get(i)` gives the item at index `i`,
counting from 0, or `nil` if `i` is past the end or negative. `set(i, x)`
replaces the item at `i`, which must be within the array, and returns the
array. `size()` gives the number of items.

A hash has four methods. `get(k)` gives the value for the key `k`, or `nil`
if there is none. `set(k, v)` stores a value under `k`, and returns the hash.
`keys()` gives an array of the keys, in the order they were first added.
`size()` gives the number of entries. A key is always a string.

The class `new` method works as `Array.new` and `Hash.new` do.

## Instances

Five built-in functions, bound before the program starts as `catch` is.
A sixth, `opaque_instance_set_class`, is under Bootstrap.

`create_opaque_instance(class, attrs)` makes an instance with that class
and those attrs, and gives it the next id. `attrs` must be a hash. It isn't
copied, so a later change to the hash is a change to the instance's attrs.

`opaque_instance_id(o)` gives the id of the instance `o`,
`opaque_instance_class(o)` its class, and `opaque_instance_attrs(o)` its
attrs, the hash itself. Each takes an instance and nothing else.

`create_class(attrs)` makes an instance to use as a class. Its class is
`nil`, so a class made this way isn't an instance of `Class`, unlike the
sketch's; `Class.new` makes one that is. Its attrs are a new hash with `"$name"` as `""`, `"$superclass"` as
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

Before every program, a prelude in `lib/prelude.smol` runs. It makes two
classes the way a program makes any class, so they are the first two
objects. The names `Class` and `Object` are bound by it, and a program can
use them.

`Class` is object 1. It is an instance of itself, and its superclass is
`Object`. Its methods are `name()`, which gives its name; `superclass()`,
which gives its superclass; and `get_method(label)`, which gives the method
under that label in its own `"%methods"`, or `nil`.

`Object` is object 2. It is an instance of `Class`, and it has no superclass.
Its methods are `new(key, value, ...)`, which makes an instance of the class
it is called on, with those pairs as its attrs; `id()`; and `class()`.

So `Class.new("$name", "Foo", "$superclass", Object, "%methods", Hash.new(...))`
makes a class. The built-in `opaque_instance_set_class(o, c)` sets an
instance's class, and gives back `o`; the prelude uses it to make `Class` an
instance of itself (D19). The prelude binds no name of its own, and its last
statement is an expression whose value is never printed: a program with no
statements prints nothing.

The methods of `Array` and `Hash` are not in this section: they are still
the host's, and move to class method tables with the rest of the bootstrap.

## Output

The program prints the value of its last statement, if that statement is an
expression, and then a newline. Integers print in decimal, strings in double
quotes, functions as `<function>`, and the constants as `nil`, `true` and
`false`. An array prints as `[1, "two"]` and a hash as `{"a": 1}`, with keys
in the order they were added. An array or hash that holds itself prints as
`[...]` or `{...}` where the cycle starts. A class prints as `<class Array>`.
An instance prints as `<object ID>`, where ID is its id: `<object 1>`.
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
chain that loops back to a class it has already searched. A
method that isn't found is `no method found for NAME on VALUE`, for an
instance as for any other value. A fault that `catch` takes is not a fault of the program: the
program carries on after the call to `catch`.
