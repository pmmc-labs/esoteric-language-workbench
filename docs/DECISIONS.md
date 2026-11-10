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
