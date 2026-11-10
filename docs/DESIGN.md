# SMOL design

This is the design as agreed so far. [`DECISIONS.md`](DECISIONS.md) has
the reasons and the alternatives that were turned down, and
[`PLAN.md`](PLAN.md) has the build order. **(open)** marks a proposal
that hasn't been confirmed. **(default)** marks something the agent took
without discussion, which is fair to change. Nothing here is built yet.

## Goals

- **A bootstrapped object meta-model.** Classes are objects, `Class` is
  an instance of itself, and `Object` is the root. It borrows from
  Smalltalk and CLOS, and it is written in SMOL itself (D8, D9).
- **Personal experimentation.** A theoretical exercise, not a tool (D8).
- **Aggressively simple.** The meta-model and the runtime it needs,
  nothing else (D8, D13).

## Non-goals

- General-purpose programming, and performance (D8).
- Regular expressions, Perl compatibility, and Perl's context-dependent
  sigils (D9, D11, D13).

## The language

- **Values**: integers, strings, `nil`, `true` and `false` (default); the
  primitives Scalar, Hash and Array (D11); closures (D11); opaque
  instances (D10).
- **Names**: a sigil is part of the name and never changes with context:
  `$a` and `@a` are different names (D11). There is no element syntax;
  reading an element is a method call, `@a.get(0)` (default).
- **Literals**: `[a, b]` is `Array.new(a, b)` and `{k => v}` is
  `Hash.new(...)` (D12). `Hash.new` takes flat alternating keys and values,
  as the sketch's `%attrs` does (default). Keys are strings (default).
- **Calls and methods**: `f(a, b)`, `obj.m(a)`, `@a.push(x)` (D12).
- **Bindings**: `let x = e` (default).
- **Closures**: `function (params) { ... }`. A trailing `%name` parameter
  collects the remaining arguments into a Hash (default). A function's
  value is its last expression (default). Parameters are names only: no
  prototypes or signatures (default). The receiver is open, below.
- **Truthiness**: `nil` and `false` are false; everything else is true
  (default).

## The core rule (candidate)

Every object is an opaque instance: an id, a class and attributes. A
method call looks the method up in the class's method table, then in each
superclass in turn, and calls the closure it finds. Nothing is installed
anywhere else, so there is no promotion step (D10). A proposal that
changes how lookup works is a proposal about this rule.

The primitives are opaque instances too, and their methods, such as
`push`, are built-in closures in their class's method table, so they
dispatch by the same rule (default).

## Values and memory

Each new instance takes the next id from one counter, starting at 1, so
in the bootstrap `Class` is 1 and `Object` is 2, as in the sketch
(default). Memory is the host's until the implementation is picked
(open 1).

## The runtime

Built in, from the sketch's `::` functions (D10): `create_opaque_instance`,
`opaque_instance_id`, `opaque_instance_class`, `opaque_instance_attrs`,
and `create_class`. Everything else is SMOL source, or one of the
built-ins settled by the open questions below.

## The implementation (open)

Not chosen. The options are a tree-walking interpreter in TypeScript
(recommended), a bytecode VM, a compiler that emits JavaScript, and a
compiler that emits C as the calculator did. The reasons are in the
proposal at the top of [`PLAN.md`](PLAN.md).

## Open questions

1. **Implementation**: an interpreter in TypeScript (recommended), or one
   of the alternatives in `PLAN.md`.
2. **Receiver**: a method's first parameter is `self`, bound by the
   dispatch (recommended), or `this`, which brings in JavaScript's rules
   for it.
3. **Inheritance**: single (recommended), or multiple with a CLOS-style
   precedence list. The sketch is single: its precedence list is the
   superclass chain.
4. **Faults**: a built-in `catch(closure)` that returns the fault's
   message, or `nil` (recommended), or a `try`/`catch` form. The sketch's
   `fails_ok` needs one of them.
5. **`isa` and `can`**: built-in methods on `Object` (recommended). The
   sketch names them, but they route to AUTOLOAD and die with "No method
   found", so they're stubs.
6. **Bootstrapping the class slot**: a built-in setter for an instance's
   class, so SMOL source can make `Class` an instance of itself
   (recommended). The alternative is that the runtime builds `Class`
   natively. The sketch does this with a reference to a variable that is
   assigned later.
7. **Scalar**: a value bound to a name, with no box type (recommended).
   The sketch's `\$Class` is the only use of a box, and 6 replaces it.
8. **Keys**: the sketch's `$:name` and `%:methods` keys drop their colon
   and keep the sigil as part of the name: `$name`, `%methods`
   (recommended).
9. **`%:attributes`**: `create_class` sets it, and nothing reads it. Drop
   it (recommended).
10. **Sealed instances**: the sketch locks each instance's three fields
    with `lock_keys`. Drop it unless sealed instances are wanted
    (recommended: drop, since it's Perl's).
