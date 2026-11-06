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
them, keeping D5 to D7, which are the process.

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

Not numbered D8 to D19: those numbers were used by an earlier build of
these steps, in this branch's history, and aren't reused.

**D20. Arithmetic is four binary operators in prefix form: `(+ a b)`,
`(- a b)`, `(* a b)`, `(/ a b)`.** *(default)* The reader already reads
lists, so the forms need no reader change, and prefix is the form every
later operator will take. Each operator takes exactly two operands, and
a nested form is an operand, so `(* (+ 1 2) (- 10 4))` is 18. Rejected:
infix `1 + 2` (a precedence table and a second reader rule, against
aggressive simplicity); n-ary `(+ 1 2 3)` (its meaning turns on whether
an intermediate sum overflows, a second semantics to decide and test,
which can come when it's asked for); unary `(- x)` (negation is
`(- 0 x)`, and a literal already takes a sign).

**D21. A malformed form is a compile error, found over the whole program
before anything runs, with fixed messages.** *(default)* A form is an
operator with two operands. Anything else is a compile error, unit-tested
with its position (D4): `+ takes two operands` (wrong count, at the
list's `(`, naming the operator); `unknown operator: foo` (a list headed
by a symbol that isn't one of the four, at the `(`); `a form must start
with an operator` (an empty list, or a list whose head isn't a symbol,
at the `(`); `a symbol is not a value: x` (a bare symbol, at its own
position); `integer out of range` (a literal past 63 bits, at the
literal, as step 0 has it). The whole tree is checked, left to right,
before the first operation runs, so a literal out of range in the second
operand of a division by zero is a compile error, not a fault. Rejected:
reporting these at run time (a program that can't compile would fault
instead, and the golden runner would see a fault, not a refusal);
checking as the code runs (a fault in an earlier operand would then hide
a later compile error).

**D22. A leading `+` is not part of a literal: `+5` is a symbol, and so
a compile error.** *(default)* The reader keeps its rule, an integer is an
optional `-` and digits. Rejected: reading `+5` as 5 (a second spelling
of one value, and it would make the operator's own name start a
literal, so a reader would have to know which `+` is which).

**D24. Division truncates toward zero, and a zero divisor is
`fault: division by zero`.** *(default)* `(/ -7 2)` and `(/ 7 -2)` are
both -3, as C's `/` and most languages' give. A zero divisor has no
value to give, so it is a fault (D3), not 0. The remainder is left out
(see step 1's text): it would need its own rule for negative operands.
Rejected: floor division, Python's `//` (a second rule for the operator
the calculator already has); 0 as the result (a silent wrong answer);
a compile error for a literal zero divisor (it would move a run-time
fault to compile time, see D28).

## Values and memory

**D23. A result outside the 63-bit range is a fault: `fault: integer
overflow`.** *(default)* The range is the one the literals have (step 0).
A calculator that wraps gives plausible wrong answers, and a fault is
what D3 gives when the program can't go on. The fault is for an
operator's result only; operands are always in range. Rejected:
wrapping (silent wrong answers, and the machine's width is 64 bits, not
63); bignums (a heap value, which is step 5's business, and machinery
this calculator doesn't need); saturating at the limits (silent wrong
answers again).

**D25. The one quotient out of range, `-2^62 / -1`, is an overflow.**
*(default)* Its true value, 2^62, is past the 63-bit range, so it is
`fault: integer overflow` by D23. The divisor isn't zero, so it isn't a
division fault. Rejected: a division fault (the divisor is not zero);
wrapping to -2^62 (D23 rejects wrapping).

## Runtime

**D3. A fault ends the program: its message on stderr, exit 1, after
whatever stdout had.** *(Default)* So a golden test checks a fault as
two lines, the message and `exit: 1`.

**D26. The runtime checks each operation's own result, on the operands'
values, before the range check.** *(default)* A 64-bit product of two
63-bit numbers can exceed 64 bits and wrap: `(* 4294967296 4294967296)`
is 2^64, which wraps to 0, and a range check on the wrapped result alone
finds 0, in range. So `rt_add`, `rt_sub` and `rt_mul` decode their
operands, compute with `__builtin_add_overflow`, `__builtin_sub_overflow`
and `__builtin_mul_overflow`, range-check the result, and encode it with
`rt_int`. `rt_div` range-checks its quotient (D25). Rejected: checking the
wrapped result (the case above); a 128-bit type (`__int128` isn't
standard C; the builtins are supported by gcc and clang, which the suite
runs under).

**D27. Operands are evaluated left to right, and the first fault in that
order is the one reported; an operator's own fault comes after both of
its operands'.** *(default)* C doesn't order a call's arguments
(CLAUDE.md's code style), so the codegen binds each operand to a C
temporary, in order, before the operator's call. In
`(+ 4611686018427387903 (/ 1 0))` the answer is `division by zero`: the
right operand faults before the add overflows. In
`(+ (+ 4611686018427387903 1) (/ 1 0))` it is `integer overflow`, since
the left operand is evaluated, and faults, first. Rejected: leaving the
order to C (the answer would depend on the compiler, and gcc and clang
have already disagreed); the operator's fault before its operands' (an
overflow would hide a division by zero in the right operand, which a
reader would not expect).

## Compiler

**D28. The compiler doesn't evaluate: every fault is a run-time event.**
*(default)* A fault is what happens while the program runs (D3: output
before it, then exit 1). Folding `(/ 1 0)` at compile time would make it
a compile error, which the golden tests can't hold (D4), and so hide
it from them. Rejected: constant folding now (an optimization, and its
own step if it's ever wanted; folding would also have to follow D27's
order at compile time).

**D4. A compile error can't be a golden test; it's a unit test.**
*(Default)* `t/run.sh` calls a failed compile a failure, which is what
it should be for a test that's meant to run. Messages and positions
are checked in `compiler/tests/`. Rejected: a `; compile-error:` header
line in a golden test; it would come when a language has enough
compile errors to want it.

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
