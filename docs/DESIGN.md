# SMOL design

This is the design as agreed. [`DECISIONS.md`](DECISIONS.md) has the
reasons and the alternatives that were turned down, and
[`PLAN.md`](PLAN.md) has the build order. **(default)** marks something
the agent took without discussion, which is fair to change. What is built
so far is in [`LANGUAGE.md`](LANGUAGE.md).

## Goals

- **A bootstrapped object meta-model.** Classes are objects, `Class` is
  an instance of itself, and `Object` is the root. It borrows from
  Smalltalk and CLOS, and it is written in SMOL itself (D8, D9, D19).
- **Personal experimentation.** A theoretical exercise, not a tool (D8).
- **Aggressively simple.** The meta-model and the runtime it needs,
  nothing else (D8, D13).

## Non-goals

- General-purpose programming, and performance (D8).
- Regular expressions, Perl compatibility, and Perl's context-dependent
  sigils (D9, D11, D13).

## The language

- **Values**: integers, unbounded (BigInt on the host) (default); strings,
  with no escapes yet (default); `nil`, `true` and `false` (default). These
  are the Scalar values: a name is bound to one, and there is no box type
  (D20). The primitives Hash and Array (D11) are references, and they change
  in place (default). Closures (D11), opaque instances (D10), and the
  classes `Array` and `Hash` (default) are values too. Methods that change
  their receiver return it, so calls chain (default). A missing key or
  index gives `nil`, and `set` won't grow an array (default). An array or
  hash that holds itself prints its cycle as `[...]` or `{...}` (default).
- **Names**: a sigil is part of the name and never changes with context:
  `$a` and `@a` are different names (D11). There is no element syntax;
  reading an element is a method call, `@a.get(0)` (default).
- **Literals**: `[a, b]` is `Array.new(a, b)` and `{k => v}` is
  `Hash.new(...)` (D12). `Hash.new` takes flat alternating keys and values,
  as the sketch's `%attrs` does (default). Keys are strings, sigils
  included (D21).
- **Statements and comments**: statements are separated by `;`, and the
  last may omit it (default). `//` runs a comment to the end of the line
  (default): the plan's `;` comments couldn't coexist with `;` separators.
- **Calls and methods**: `f(a, b)`, `obj.m(a)`, `@a.push(x)` (D12).
- **Bindings**: `let x = e` binds for the statements after it (default).
- **Closures**: `function (params) { body }`, an expression (default).
  Parameters are names, distinct, with no prototypes or signatures
  (default). A function keeps the names bound where it is written, so a
  later let is invisible to it (default; the association list makes that a
  pointer). A body's value is its last statement if that is an expression,
  and `nil` otherwise (default). A call must give as many arguments as there
  are parameters (default). A method's first parameter is its receiver,
  `self` (D15). `self` is an ordinary name, and dispatch passes the receiver
  as the first argument (step 4). A method's arity counts only the
  arguments after the receiver, and a function with no parameter to take
  the receiver can't be called as a method (default).
  A trailing `%name` parameter collects the remaining arguments as a Hash,
  in pairs, and must be the last parameter (default; step 3). A let binds
  after its value is computed,
  so a function can't call itself by name (default); methods recurse
  through dispatch (step 4).
- **Truthiness**: `nil` and `false` are false; everything else is true
  (default).
- **Output**: a program prints the value of its last statement, if that
  statement is an expression, and then a newline. A let prints nothing
  (default).
- **Faults**: a fault is printed as `fault: MESSAGE` on stderr, and the
  program exits 1 (default). A syntax error is printed as
  `FILE:LINE:COLUMN: MESSAGE` and also exits 1 (default). The faults so far
  are an unbound name, a call of a non-function, a call with the wrong
  number of arguments, a method that isn't found, an index that isn't an
  integer, a `set` index out of range, a hash key that isn't a string, and
  a key with no value (default). Step 4 adds attrs that aren't a Hash, a
  value that isn't an instance given to one of the `opaque_instance_`
  readers, and a method with no parameter for `self` (default).

## The core rule

Every object is an opaque instance: an id, a class and attributes (D10).
A method call looks the method up in the class's method table, then in
each superclass in turn, along the single chain (D16), and calls the
closure it finds, passing the receiver as `self` (D15). Nothing is
installed anywhere else, so there is no promotion step. A proposal that
changes how lookup works is a proposal about this rule.

The primitives are opaque instances too, and their methods, such as
`push`, are built-in closures in their class's method table, so they
dispatch by the same rule (default). That is step 5: until then arrays,
hashes and the class values `Array` and `Hash` keep the host tables of
step 3, and take no ids.

As built in step 4:

- The method table is the Hash under `"%methods"` in the class's attrs,
  keyed by plain method names, and the superclass is the value under
  `"$superclass"` (D21). The chain ends at `nil`.
- A class that isn't an instance, or has no Hash under `"%methods"`, has no
  methods. One that isn't an instance has no superclass either, so the
  chain ends there, as it does at a class with no `"$superclass"` key
  (default).
- A method is found when its name is a key of the table. A value there that
  isn't a function is found, and calling it is the fault `not a function`
  (default). The sketch tests the value for truth instead.
- A superclass chain that loops back to a class already searched is the
  fault `superclass chain loops back to VALUE` (default). The sketch would
  never end on one.
- A missing method is `no method found for NAME on VALUE`, and an instance
  is shown as `<object ID>`.

## Values and memory

Each new instance takes the next id from one counter. The prelude runs
first, so `Class` is 1 and `Object` is 2, and a program's own objects start
at 3, as in the sketch (D25). Only `create_opaque_instance` and
`create_class` take ids. The counter belongs to one run of a program, so
each run starts again at 1 before its prelude. An
instance holds its attrs Hash by reference; `create_class` builds a new
Hash, the defaults and then the given attrs, so it doesn't share the one it
was given (default). An overridden default keeps its place in that Hash,
and a new key follows the three defaults (default). Memory is Node's: the collector and the closures of the
interpreter's host (D14).

## The runtime

Built in:

- From the sketch's `::` functions (D10): `create_opaque_instance`,
  `opaque_instance_id`, `opaque_instance_class`, `opaque_instance_attrs`,
  and `create_class` (step 4). They are plain names in the starting
  environment. `attrs` is one Hash value, not flat arguments. Attrs that
  aren't a Hash are the fault `attrs must be a Hash: VALUE`, and a reader
  given something else is `not an opaque instance: VALUE` (default: the
  wording). The built-in `create_class` gives the class `nil`. The prelude's
  `create_class` wraps it, so a class made by `create_class` is an instance of
  `Class`, as the sketch's is (D26). `Class` gets its own class from the prelude
  (D19). One difference from the sketch remains: the lookup reads
  `"$superclass"` directly where the sketch calls the `superclass` method,
  which gives the same answer while `Class` keeps its `superclass` method.
- `opaque_instance_set_class(instance, class)`: sets an instance's class
  slot, so SMOL source can make `Class` an instance of itself (D19). The
  name is a default.
- `catch(closure)`: calls the closure with no arguments, and returns the
  fault's message as a string, or `nil` if the call raised no fault (D17).
  A fault in the argument itself, such as a value that isn't a function, is
  not caught (default). `catch` is bound in the starting environment, so a
  let can shadow it (default). Built-ins print as `<function>`, as closures
  do (default).
- `isa` and `can`, as methods on `Object` (D18).

- Array and Hash methods, one table of host functions per kind of value,
  which a method call consults (step 3). Step 4 leaves the tables as they
  are. Step 5 replaces them with class method tables (D10, D16), when it
  makes `Array` and `Hash` SMOL classes that hold them.

Everything else is SMOL source (D19).

## The implementation

A tree-walking interpreter in TypeScript, run by Node (D14). In
`compiler/src/`: `lexer.ts` turns text into tokens, `parser.ts` turns
tokens into statements, `eval.ts` runs them, and `ast.ts` and `errors.ts`
hold the shapes and the one error class. `bin/smol.ts` is the driver. The
object model is SMOL source running on that interpreter.

## Open questions

None. The ten questions from the first draft are settled in D14 to D22.
The defaults marked above are fair to revisit.
