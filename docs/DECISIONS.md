# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. **User** means the person decided it; **default** means the agent
proposed it and it wasn't explicitly discussed. Defaults are fair to
revisit. Open questions are listed at the end of [`DESIGN.md`](DESIGN.md).

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
