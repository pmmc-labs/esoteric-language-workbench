# SMOL design

This is the design as agreed. [`DECISIONS.md`](DECISIONS.md) has the
reasons and the alternatives that were turned down, and
[`PLAN.md`](PLAN.md) has the build order. **(default)** marks something
the agent took without discussion, which is fair to change. Nothing here
is built yet.

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

- **Values**: integers, strings, `nil`, `true` and `false` (default); the
  primitives Hash and Array (D11); Scalar, a value bound to a name (D20);
  closures (D11); opaque instances (D10).
- **Names**: a sigil is part of the name and never changes with context:
  `$a` and `@a` are different names (D11). There is no element syntax;
  reading an element is a method call, `@a.get(0)` (default).
- **Literals**: `[a, b]` is `Array.new(a, b)` and `{k => v}` is
  `Hash.new(...)` (D12). `Hash.new` takes flat alternating keys and values,
  as the sketch's `%attrs` does (default). Keys are strings, sigils
  included (D21).
- **Calls and methods**: `f(a, b)`, `obj.m(a)`, `@a.push(x)` (D12).
- **Bindings**: `let x = e` (default).
- **Closures**: `function (params) { ... }`. A method's first parameter is
  its receiver, `self` (D15). A trailing `%name` parameter collects the
  remaining arguments into a Hash (default). A function's value is its
  last expression (default). Parameters are names only: no prototypes or
  signatures (default).
- **Truthiness**: `nil` and `false` are false; everything else is true
  (default).

## The core rule

Every object is an opaque instance: an id, a class and attributes (D10).
A method call looks the method up in the class's method table, then in
each superclass in turn, along the single chain (D16), and calls the
closure it finds, passing the receiver as `self` (D15). Nothing is
installed anywhere else, so there is no promotion step. A proposal that
changes how lookup works is a proposal about this rule.

The primitives are opaque instances too, and their methods, such as
`push`, are built-in closures in their class's method table, so they
dispatch by the same rule (default).

## Values and memory

Each new instance takes the next id from one counter, starting at 1, so
in the bootstrap `Class` is 1 and `Object` is 2, as in the sketch
(default). Memory is Node's: the collector and the closures of the
interpreter's host, since the implementation is a TypeScript interpreter
(D14).

## The runtime

Built in:

- From the sketch's `::` functions (D10): `create_opaque_instance`,
  `opaque_instance_id`, `opaque_instance_class`, `opaque_instance_attrs`,
  and `create_class`.
- `opaque_instance_set_class(instance, class)`: sets an instance's class
  slot, so SMOL source can make `Class` an instance of itself (D19). The
  name is a default.
- `catch(closure)`: runs the closure, and returns the fault's message, or
  `nil` (D17).
- `isa` and `can`, as methods on `Object` (D18).

Everything else is SMOL source (D19).

## The implementation

A tree-walking interpreter in TypeScript, run by Node (D14). The reader,
parser and evaluator are pure functions over immutable data. The object
model is SMOL source running on that interpreter.

## Open questions

None. The ten questions from the first draft are settled in D14 to D22,
and the defaults marked above are fair to revisit.
