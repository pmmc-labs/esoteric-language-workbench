# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. **User** means [the person] decided it; **default** means the
agent proposed it and it wasn't explicitly discussed. Defaults are fair to
revisit. Open questions are listed at the end of [`DESIGN.md`](DESIGN.md).

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics (quote the person where the words matter),
the reason, and `Rejected:` with each alternative and why it lost. A
decision that's later changed stays, with a note pointing to the entry
that changed it; the new entry says what it retires.

Sections group entries by subject, not by time; a new entry goes in the
section it belongs to. Number by time.

The entries below are the workbench's own: a calculator, built to work
the process out on. A language started from this template replaces
them, keeping D8 to D10, which are the process.

## Scope

**D1. A calculator: integer expressions, compiled to a native binary
that prints the value.** *(User: "let's make a small calculator language
to work out these steps.")* The language exists to exercise the
process: steps, models, checks. It grows only as far as that needs.

**D2. The compiler is TypeScript run by Node as it is, and emits C.**
*(Default)* C so step 0 runs wherever there's a C compiler; a native
target through a target interface when something needs one. Node's
type stripping, so there's no build step; the compiler uses only
erasable syntax (no parameter properties, no enums).

## Language

**D3. Operators take exactly two arguments.** *(Default)* `(+ 1 2 3)`
and `(- 1)` are compile errors. Rejected: variadic `+` and `*` and
unary `-`, which a Lisp usually has, because the calculator doesn't
need them and a rule with no exceptions is easier to check.

**D11. Booleans, `#true` and `#false`, a type of their own.** *(User,
as the step to test the process on; the shape default.)* They print as
written. Neither is an integer: arithmetic on one faults `not an
integer`. Rejected: 0 and 1 as the booleans (no way to fault a
`(+ #true 1)`, and the calculator is here to have faults to test).

**D12. Comparisons: `<`, `<=`, `>`, `>=` on two integers, `==` and
`!=` on any two values, each giving a boolean.** *(Default)* An
ordering given a boolean faults `not an integer`. `==` on two values of
different types is `#false`, not a fault, as `eq?` is in a Lisp.

**D13. `(if test then else)`: three parts, the test a boolean at run
time or the program faults `not a boolean`, and only the taken branch
evaluated.** *(Default)* So `(if #true 1 (/ 1 0))` is 1. Rejected:
truthiness (anything but `#false` is true), which hides the mistake
`(if 0 ...)`; and a two-part `if`, which would need a value for the
missing branch.

## Values and memory

**D4. Integers are 63 bits, and a result that doesn't fit faults.**
*(Default)* One bit for a tag, so other values can come later without
changing the integers. Overflow is a fault, `fault: overflow`, exit 1.
Rejected: wrapping (silent, and no model of it is the definition);
bignums (machinery the calculator doesn't need; a step later, if ever).

**D14. A boolean is an immediate with its own tag: the low two bits
`11`, the value in bit 2.** *(Default)* An integer's low bit stays 0
(D4), so integers are untouched, and `01` is left for what comes next.
The runtime checks a value's tag before arithmetic and comparison now
that the compiler can't know what an `if` gives.

**D5. Division truncates toward zero and the remainder takes the
dividend's sign.** *(Default)* C's rule, so the runtime is `/` and `%`
with a zero check. `(/ -7 2)` is `-3` and `(% -7 2)` is `-1`. Dividing
by zero faults, `fault: division by zero`. Rejected: floored division,
Python's, which would be a model-side convenience and a runtime-side
cost; both are defensible, and the model (`t/models/arith.py`) says
which this is, in its own functions.

## Runtime

**D6. A fault ends the program: its message on stderr, exit 1, after
whatever stdout had.** *(Default)* So a golden test checks a fault as
two lines, the message and `exit: 1`.

## Compiler

**D7. A compile error can't be a golden test; it's a unit test.**
*(Default)* `t/run.sh` calls a failed compile a failure, which is what
it should be for a test that's meant to run. Messages and positions
are checked in `compiler/tests/`. Rejected: a `; compile-error:` header
line in a golden test; it would come when a language has enough
compile errors to want it.

## Project

**D8. Golden tests' expected output comes from an independent source,
never from the compiler.** *(User)* See `t/README.md`. `t/checks.py`
enforces the half it can: a file a model writes is what the model
writes now.

**D9. Examples bend to the language.** *(User)* When a port needs a
feature, the example changes or is left out. Rejected: adding to the
language to make a port pass.

**D10. A commit that touches the implementation names a decision or a
plan step in its subject.** *(User)* So a change is found from the log
and the log from a change. `make commits` checks a range and `make
hooks` installs the check as a commit-msg hook. A commit that touches
only docs or tests is exempt; the models' files count as tests.
