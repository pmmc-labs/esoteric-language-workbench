# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. **User** means the person decided it; **default** means the agent
proposed it and it wasn't explicitly discussed. Defaults are fair to
revisit. The open questions are settled; the record of each is below.

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics (quote the person where the words matter),
the reason, and `Rejected:` with each alternative and why it lost. A
decision that's later changed stays, with a note pointing to the entry
that changed it; the new entry says what it retires.

Sections group entries by subject, not by time; a new entry goes in the
section it belongs to. Number by time.

D1 to D4 were the calculator this template started as. They are removed
now that the language is SMOL, and their numbers aren't reused. D5 to D7
are the process and stay.

## Scope

**D8. SMOL is a small language for personal experimentation, to explore
bootstrapping object meta-models.** *(User: "a small language called SMOL,
which is just for personal experimentation ... a theoretical exercise to
explore bootstrapping object meta models.")* The language grows only as
far as the meta-model and the runtime it needs. Rejected: general-purpose
use and high performance, both of which the user ruled out.

**D9. The object model borrows from Smalltalk and CLOS, and the Perl
sketch is the guide, not the spec.** *(User: the sketch "was one of the
first properly bootstrapped versions", and "I do not want to replicate
the Perl, but I do want to use it as somewhat of a guide.")* The sketch is
`docs/prior-art/MiniMetaModel.pl`. Rejected: replicating Perl.

## Implementation

**D14. The implementation is a tree-walking interpreter in TypeScript,
run by Node.** *(User: "Let's go with your recommendations.")* The reader,
parser and evaluator are pure functions over immutable data. Each step
runs end to end, and `t/run.sh` runs the interpreter on each `.smol` file.
Rejected: a bytecode VM, which needs an instruction set and frames the
experiment doesn't need; compiling to JavaScript, which gains nothing over
the interpreter but an output file; compiling to C, the calculator's
route, which needs a heap, a collector and a value encoding before the
first bootstrap test can pass. Retires the calculator's C runtime and its
`langc` pipeline, when step 0 lands.

## Object model

**D10. Every object is one opaque instance, and it dispatches its own
methods.** *(User: "The `opaque_instance` structure, and the `Dispatchable`
package should be one thing ... We do not need this promotion if the
opaque_instance type can dispatch the method itself.")* An instance holds
an id, a class and attributes. A method call looks the method up in the
class's method table, then in each superclass in turn, and calls the
closure it finds. Nothing is installed anywhere else, so the sketch's
promotion of methods from meta space into user space goes. The sketch's
`::` functions become built-ins of the runtime. Rejected: the promotion,
which the user called an implementation detail of Perl packages.

**D11. The primitive types are Scalar, Hash and Array, and methods are
closures.** *(User: "The primitive data types are like Perl, ... Scalar,
Hash and Array, ... along with closures for the methods.")* Sigils are
part of a name and don't change with context, as in Perl 6, so `@a` and
`$a` are different names. Rejected: Perl 5's context-dependent sigils.

**D15. A method's receiver is its first parameter, `self`, which the
dispatch binds.** *(User: "Let's go with your recommendations.")* A method
is `function (self, ...) { ... }`, and a call passes the receiver in.
Rejected: `this`, which brings JavaScript's binding rules (detached calls,
arrow functions) that the design doesn't need.

**D16. Inheritance is single. A class has one superclass, and its
precedence list is its superclass chain.** *(User: "Let's go with your
recommendations.")* Rejected: multiple inheritance with a CLOS-style
precedence list. It is parked until a proposal wants it.

**D18. `isa` and `can` are built-in methods on `Object`.** *(User: "Let's go
with your recommendations.")* Rejected: dropping them. The sketch names
them; its stubs that die (they route to AUTOLOAD) are a gap, not a
decision.

**D19. Bootstrapping is done in SMOL. A built-in setter gives an instance
its class, so `Class` can be made an instance of itself after it exists.**
*(User: "Let's go with your recommendations.")* The setter is
`opaque_instance_set_class` (the name is a default). Rejected: the runtime
building `Class` natively, which would move the bootstrap out of the
language being explored. The sketch's reference to a variable that is
assigned later is replaced by this setter.

**D20. Scalar is a value bound to a name, with no box type.** *(User:
"Let's go with your recommendations.")* Rejected: a Scalar box. Its one
use in the sketch, `\$Class`, is replaced by D19.

## Runtime

**D17. A fault can be caught by a built-in `catch(closure)`, which returns
the fault's message, or `nil`.** *(User: "Let's go with your
recommendations.")* Rejected: a `try`/`catch` form. It is one more form to
parse, and its only use is the meta-model's tests.

## Syntax

**D12. The syntax is JavaScript-like, and collection literals are
constructor calls.** *(User: "something cleaner and more javascript like
... converted into explicit `Array.new(...)` and `Hash.new(...)` calls, to
make parsing less complicated ... `@array.push(...)`.")* So `[a, b]` is
`Array.new(a, b)`, `{k => v}` is `Hash.new(...)`, and `push @array, x` is
`@array.push(x)`. Rejected: Perl's bracket and `=>` literals and its
list-operator calls, which the user wanted out of the parser.

**D13. No regular expressions, and no Perl features beyond what the
meta-model needs.** *(User: "There is no need to support regular
expressions or any other Perl features like that. We are just interested
in the meta-model and the minimum features in the runtime needed to
support it.")* Rejected: regular expressions and everything else the
meta-model doesn't use.

**D21. Hash keys keep their sigils as part of the name.** *(User: "Let's go
with your recommendations.")* The keys are `"$name"` and `"%methods"`, not
the sketch's `"$:name"` and `"%:methods"`: in SMOL the colon has no job.
Rejected: keeping the sketch's prefixes.

**D22. The sketch's `%:attributes` and `lock_keys` are dropped.** *(User:
"Let's go with your recommendations.")* `create_class` sets
`%:attributes` and nothing reads it. `lock_keys` seals each instance, and
instances don't need sealing. Rejected: keeping either.

## Dispatch

**D23. The edges of the core rule: a method is found by key presence, a
function with no first parameter can't be a method, and a superclass chain
that loops is a fault.** *(default: the step 4 builder's choices, reviewed
by the lead.)* A key present under a method name is found, even when its value
isn't a function, and calling that value is the fault `not a function`. The
sketch tests the value for truth instead, which would make a stored `false`
or `nil` look like no method at all. A method with no fixed first parameter
for `self` faults, rather than leaving the receiver to land in the arguments
or in a `%name`. A chain that loops back to a class already searched is the
fault `superclass chain loops back to VALUE`. The sketch would never end on
one, and the first version of step 4 overflowed the stack, an internal error
that `catch` couldn't take. Rejected: each of those three as the sketch has
it.

## Bootstrap

**D24. The Array and Hash methods move to class method tables in step 5, and
step 5 is split into three parts.** *(default)* A class method table needs a
class that is an instance, and step 4 had none. So step 5 is split: 5a, the
prelude with `Class` and `Object` (landed); 5b, `Array` and `Hash` as classes,
which needs a builtin that takes any number of arguments and a class for array
and hash values; 5c, `class_precedence_list`, which ends its walk at `nil` and
needs a conditional that SMOL doesn't have. Rejected: moving the tables in
step 4, when there was no class to hold them; doing 5b and 5c in one step,
since each needs a decision of its own.

**D25. Every program runs a prelude first, so `Class` is object 1, `Object` is
object 2, and a program's own objects start at 3.** *(User: "D25 is fine". D28 revises its numbers.)*
The sketch
numbers its objects this way, and the layout puts the prelude in every
program. The consequence is that the id expectations of golden tests 050 to
084 each moved by two, re-derived by hand. Rejected: running the prelude only
for programs that ask for it, since no way of asking exists, and an id would
depend on the program's text; and starting a program's objects at 1, which
puts the sketch's numbers out of step with its Foo, the third object.

**D26. `create_class` makes an instance of `Class`.** *(User: "create_class
should return instances of Class".)* The built-in makes an instance with
class `nil`; the prelude wraps it, so a class made by `create_class` is an
instance of `Class`, as the sketch's is. The wrapper is bound inside the
function that builds it, so the built-in's name is not visible to programs.
Rejected: giving the built-in the metaclass as a second argument, which
changes the signature the sketch gives and every test that calls it.

**D27. Conditionals are methods of booleans, as in Smalltalk, with a Boolean
class.** *(User: "lets follow smalltalk and make conditionals be a method of
booleans. This probably means adding a Boolean class too.")* The shape is
decided. Its classes, and how they are numbered, are open (PLAN, 5c).
Rejected: a conditional special form, which would add grammar the Smalltalk
shape doesn't need; and a builtin that picks between two functions, which
would make the branch a host operation, not a method.

**D28. The bootstrap also makes Boolean, True, False and UndefinedObject, so a
program's own objects start at 7.** *(User: "go with option A".)* Boolean is
the abstract parent of True and False, and UndefinedObject is nil's class, as
Smalltalk has them. The sketch's numbers are a guide, not the spec (D9), so
they move: the sketch's Foo is 7, not 3. Rejected: option B, one Boolean class
with the branch done by a host primitive (user objects at 4), which moves the
numbers too; and option C, the boolean methods on Object with no new class
(user objects at 3), which gives no Boolean class, and the person asked for one.

**D29. A boolean or nil takes its methods from its class, through a registry
that `set_primitive_class` fills.** *(default: the step 5c builder's choice;
the shape is the person's, D27, and this is the mechanism it needs.)* The host
keeps a registry from `true`, `false` and `nil` to a class. A method call on
one of them walks that class's chain, as for an instance (D10). Only those
three take a class so far; the other primitives come with 5b, which is still
open. Rejected: a host table of boolean methods, which would keep the
conditionals off the Boolean class; and a class held on each value, which the
constants can't carry. A program can call `set_primitive_class` too, so it can
change a constant's class for the rest of its run. That is the same open
question as `opaque_instance_set_class` (D19), and it is not settled here.

**D30. A loop in the superclass chain stops `class_precedence_list` with the
lookup's fault, through two small additions.** *(default: the review of step
5c found the loop crashed the interpreter, and the fix needed a way to stop a
walk.)* `includes(x)` on an array tests membership, with scalars equal by value
and anything else only by identity. `fault(message, value)` raises a fault, the
message and then the value shown. Rejected: a loop check in the host for this
walk alone, which would move the object model's behaviour out of SMOL (D10);
and a walk that quietly stops at a repeat, which would hide a loop the lookup
reports.

**D31. Array and Hash are classes, and their methods are host builtins in the class's method table, reached through the registry.** *(User: "I agree with all recommendations".)* Array and Hash are made by the prelude, as Boolean is. Their methods are builtins in their `"%methods"`, and an array or hash finds its class through the registry (D29), which now covers arrays and hashes. The host method tables and the host `class` value go. `opaque_instance_class` answers the registered class for a primitive, so `[1].class()` is `Array`; `id()` still needs an instance. Classes print as objects, so `Array` prints as `<object 7>`. The one exception to "methods in the class's own table" is `new`, which lives in a metaclass (D34). Rejected: keeping the host tables and pointing the classes at them, which is two dispatch routes (D10); and a class field on each array and hash value, which keeps the class in two places.

**D32. The bootstrap reserves ids, so a program's own objects start at 100.** *(User: "I agree with all recommendations".)* The bootstrap's objects are numbered 1 to 10 (Class 1, Object 2, Boolean 3, True 4, False 5, UndefinedObject 6, Array 7, Hash 8, and the metaclasses of Array and Hash, 9 and 10, D34), and the prelude then reserves the ids up to 99 with `reserve_ids(n)`, which only ever moves the next id forward. So adding a bootstrap class no longer moves a program's numbers. This revises D25 and D28 again. Rejected: accepting the moves, which would repeat with every class added; and tests that avoid absolute ids, which would lose the `<object N>` output.

**D33. The prelude reaches the host methods through `host_method(class, method)`, and each host method takes its receiver as its first argument.** *(default: the mechanism D31 needs, chosen by the lead.)* `host_method` returns the builtin for a method of Array or Hash, and faults for any other name. A builtin's arity counts its receiver, so the existing hidden-argument rule still applies. A builtin checks that its receiver is the kind it expects. Rejected: names for the host methods in the starting environment, which would put more names in front of programs.

**D34. Array and Hash each have a metaclass, because `new` is found through the receiver's class.** *(default: the builder's choice in step 5b, reviewed and accepted by the lead. It refines D31's wording; the reason in D31 stands.)* Under the core rule, `Array.new(...)` looks in Array's class, not in Array's own `"%methods"`. So `new` lives in a class of Array's, a metaclass named "Array class" under Class, and Hash has one too. The other bootstrap classes have no class-side methods, so they have none. Rejected: a metaclass for every class now, which adds objects with no behaviour behind them; and a `new` in Object that checks the receiver's name, which special-cases the object model.

**D35. `isa` and `can` are host builtins in Object's table, reached through
`host_method`, and `can` is the lookup dispatch uses.** *(default: the lead's
choice in step 6. D18 fixes that they are built-in methods of Object.)*
`isa(cls)` walks the value's class and the superclasses above it, and it stops
with the lookup's loop fault (D23). `can(name)` is the lookup itself, so the
two can't disagree. A value with no class is an instance of nothing, and it
answers false to both. Rejected: SMOL definitions, since they need a loop over
the chain, and SMOL has no loop, while Array has no test for membership; and a
`can` that looks only at the class's own table, which would disagree with
dispatch for an inherited method.

## Project

**D5. Golden tests' expected output comes from an independent source,
never from the compiler.** *(User)* See `t/README.md`. `t/checks.py`
enforces the half it can: a file a model writes is what the model
writes now.

**D6. Examples bend to the language.** *(User)* When a port needs a
feature, the example changes or is left out. Rejected: adding to the
language to make a port pass.

**D7. A commit that touches the implementation names a decision or a
plan step in its subject.** *(User)* So a change is found from the log
and the log from a change. `make commits` checks a range and `make
hooks` installs the check as a commit-msg hook. A commit that touches
only docs or tests is exempt; the models' files count as tests.
