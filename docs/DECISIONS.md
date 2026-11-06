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

**D15. Bit operations on two integers: `bit/and`, `bit/or`, `bit/xor`,
`bit/shl` and `bit/shr`.** *(User, as the step to test model-writing
on; the shape default.)* Each takes two integers (D3) and gives one;
a boolean faults `not an integer`. The integers are the mathematical
ones in two's complement, so `bit/and`, `bit/or` and `bit/xor` are on
the sign-extended value, as every width agrees: `(bit/and -1 7)` is
7, `(bit/or -8 1)` is -7, `(bit/xor -1 0)` is -1. A result of these
three is always in range. Rejected: `bit/not` (D3 says two arguments;
`(bit/xor x -1)` is it); unsigned views; a width other than the
integers' own.

**D16. Shifts: `(bit/shl a n)` is `a` times 2^n, faulting `overflow`
when that doesn't fit (D4); `(bit/shr a n)` is `a` divided by 2^n
rounded toward negative infinity, so the sign is kept and `(bit/shr -7
1)` is -4 where `(/ -7 2)` is -3 (D5).** *(Default)* The count `n` is
from 0 to 62; any other count faults `bad shift`, since 63 or more
shifts every bit of a 63-bit integer out, and a negative count is a
mistake, not the other shift. Rejected: wrapping on `bit/shl` (D4
rejected wrapping); a count masked to its low bits, C's and Java's
way, which hides the mistake; `bit/shr` as division (it rounds the
other way, and that's the point of having both).

**D17. The faults' names: `not an integer`, `overflow` and `bad
shift`.** *(Default)* The first two are the arithmetic's (D4, D14);
the third is new and only the shifts give it.

**D18. Exponentiation: `(** a b)`, a to the power b, on two integers.**
*(User)*

**D19. What D18 left open: `a ** 0` is 1 for every `a`, `0 ** 0`
included; a negative exponent faults `bad exponent`, whatever the base;
a result past the range faults `overflow` (D4).** *(Default, written by
the agent that built step 4, which could not ask; fair to revisit.)* A
boolean as either argument faults `not an integer` (D11, D14). The
negative-exponent rule is on the exponent, so `(** 1 -1)` faults though
1 would fit, and one rule needs no list of bases. `bad exponent` is a
fourth fault name beside D17's. Rejected: a negative exponent giving 0
or the truncated reciprocal (a silent answer for what is nearly always a
mistake, as D16 rejected masking a count); reusing `bad shift` (the
wrong word); `0 ** 0` faulting (the empty product is 1, and a rule with
fewer exceptions is easier to check); a bignum intermediate (D4).

**D20. A budget: `(within n expr)` evaluates `expr` with a budget of
`n` operations, and faults when it's spent.** *(User)*

D21 to D27 are what D20 left open, proposed with step 5 and not yet
confirmed by the person (all *default*): what counts as an operation,
where the edge of the budget is, what `n` may be, how budgets nest,
which fault reports first, what kind of form it is, and how it runs.

**D21. An operation is one application of an operator, and nothing
else is.** *(Default, proposed with step 5; fair to revisit.)* The
seventeen operators of the table (`+ - * / %`, the six comparisons,
the five `bit/` operations, `**`) cost one each, `==` and `!=` too,
however large their arguments are: `(** 1 4611686018427387903)` is one
operation, whatever the exponent. Integers, booleans,
`if` and `within` cost nothing: an `if` costs its test and the branch it
takes, as those are operations, and the branch it doesn't take is not
run (D13). The cost of a program is therefore a count of operators
applied, and is the same however the arguments are ordered. A form a later
step adds (a binding, a call) says what it costs when it arrives; this
entry is only about what exists. Rejected: counting every node, literals
included (the size of the program, not its work: `(within 0 5)` would
fault); counting `if` (it is a form, not an operator, D13, and cannot
repeat, so it does no work of its own to bound); the work an operation does
(`**`'s squarings, a division's steps): that is the runtime's loop, and
the definition of the language is not to be the number of times a loop
in `rt.c` turns; a weight per operator (a table to remember and to
get wrong, for no use the calculator has).

**D22. A budget of `n` allows `n` operations; the next one faults `out
of budget`, and nothing catches it.** *(Default, proposed with step 5;
fair to revisit. D20 says "faults when it's spent", which reads two
ways; this is the first.)* A program whose body applies exactly `n`
operators gives its value, and one that would apply the `n+1`th ends
there with `fault: out of budget`, exit 1, nothing on stdout (D6). So
`(within 0 e)` allows `e` no operator, and `(within 3 e)` is `e`'s
value when `e` costs 3 or fewer. A `within` that completes is its body's
value, whatever type. Rejected: faulting when the `n`th operation
completes (it throws away a result the budget paid for, so `n` would have to
be written one more than the operations wanted, and a budget of 0 and a
budget of 1 would both allow none); a `within` that gives a
value, `#false` or a pair, when spent (D6 has no handlers and no
catching, and the value would need a type to be told from the body's);
a message that carries `n` or the count (D6's messages are a name).

**D23. `n` is an expression, evaluated first and outside the budget it
sets; it must be an integer, and not negative.** *(Default, proposed
with step 5; fair to revisit.)* `(within (+ 1 1) e)` is allowed. The
operators in `n` are charged to the budgets that surround the `within`,
not to the one it makes, which does not exist yet. A boolean as `n`
faults `not an integer` (D11, D14); a negative `n` faults `bad budget`,
a fifth fault name beside D17's and D19's, and is checked after the
type, so `n` of `#true` is `not an integer` and never `bad budget`.
Zero is a budget, and the largest integer, 4611686018427387903, is one
(it is far past what any program can spend). The check is at run
time, for a literal too: `(within -1 5)` compiles. Rejected: `n` a
literal only (a restriction the next step, with a name to bind, would
have to undo, and a second rule for what may stand in the place);
`n` evaluated inside the budget it sets (circular: its cost would be the
first operations of a budget whose size it decides); a negative `n`
treated as 0 (D16 and D19 rejected the same silence for a bad shift and
a bad exponent) or as no limit (the opposite of what a budget is for);
a compile error for a negative literal (the run-time fault is needed for
the expression anyway, and two rules for one mistake is what D3 chose against).

**D24. Budgets nest by the smallest: an operation is charged to every
`within` around it.** *(Default, proposed with step 5; fair to revisit.)*
In `(within 2 (within 100 e))` the inner budget does not extend the
outer: `e` may apply 2 operations. In `(within 100 (+ (within 2 a) b))`
the operations of `a` count against the outer budget too, and still
count when the inner `within` has ended, so `b` has what the outer one has
left. Two `within`s one after the other, or one in each argument, have
a budget each and do not share: the operations of the first are not taken
from the second. Where an operation finds two budgets spent the fault is
`out of budget` for both, so there is no choice of which to report.
Rejected: an inner budget that replaces the outer for its body (a limit
that a nested `within 1000000` undoes is no limit, and the point of a
budget is to be a guard around code you did not write); an inner budget
whose unspent part is returned to the outer, or is thrown away (what was
spent is spent, and what is not has no owner after the `within`); a
fault name for each level (nothing to tell the program, and the
single name is what makes the order of two budgets not matter).

**D25. When it is charged, and which fault reports first.** *(Default,
proposed with step 5; fair to revisit.)* An operation is charged when it
is applied: after its arguments have been evaluated and before it looks
at them. So `(within 0 (/ 1 0))` is `out of budget`, the budget having
refused the operation before it could fault, and `(within 1 (/ 1 0))`
is `division by zero`, the operation having been paid for. Likewise
`(within 0 (+ #true 1))` is `out of budget` and `(within 1 (+ #true 1))`
`not an integer`. The `n` of a `within` is evaluated before its body; the
test of an `if` before its branch. What stays as it was, unspecified
and untested (the Status says so): the order a call's two arguments are
evaluated in, and so which fault reports when each argument could fault
differently. The budget adds one more such pair (a spent budget in one
argument and another fault in the other); no test has one, and the total
number of operations a program that completes applies does not depend on
the order. Rejected: charging after the operation (a budget that stops
work would report an operation it had already let run, and the
operation's own fault would win over the budget); charging an
application before its arguments are evaluated (the same total for a
program that completes, but `(within 1 (+ (/ 1 0) 2))` would be `out of
budget` and not `division by zero`: the `+` would be paid for before
the division that has to happen first); deciding the order of arguments now
(left to right: the generated C would have to sequence them, by
temporaries, which rewrites the compiler's output and moves unit tests
that match its text, and that is a step of its own that would also give
clang's bracket limit its fix; not this one).

**D26. `within` is a special form with exactly two parts, like `if`.**
*(Default, proposed with step 5; fair to revisit.)* Not an operator:
its body must run after the budget is set, which an operator, whose
arguments are all evaluated before the operator is called, cannot do.
Another number of parts is a compile error at the form's start,
`within takes 2 arguments, not N` (D7, D13's wording), and a unit test.
`within` alone, not in head position, is `unknown name within` as any
other name. The form costs nothing (D21). Rejected: an operator of two
arguments (D3), which would run the body outside the budget it sets; a
third part for what to do when spent (D22: nothing catches).

**D27. The runtime keeps a count of operations and a limit, and a
`within` is a C function the runtime calls.** *(Default, proposed with
step 5; fair to revisit.)* `rt.c` counts every operation applied, in or
out of any `within`, and faults `out of budget` when the count passes
the limit, which starts at the largest 64-bit integer. Each of the
seventeen operator functions charges first, as its first statement
(D25). `(within n e)` compiles to a call `rt_within(N, lang_within_L_C)`
where `lang_within_L_C` is a static C function returning `e`, named by the
form's line and column; the functions are emitted before `lang_main`,
inner ones first. `rt_within` checks `n` (D23), saves the limit, lowers
it to the count plus `n` if that is lower, calls the body, puts the saved
limit back, and returns the value; a fault ends the program (D6) so
nothing needs undoing on that way out. That is D24 as arithmetic: the
limit in force is the smallest of the surrounding ones. The count plus
`n` cannot pass 2^63: `n` is below 2^62, and a count that high takes
longer than a machine runs. The known cost: the body's function sees no
variables, so a step that binds names has to give it an environment or
change this (D2 leaves C as the target; step 6 decides). Rejected: GNU
statement expressions, `({ ... })`, in place (not ISO C; and the arguments of a call are unsequenced against each
other, so two that are statement expressions may in principle
interleave, where two calls never do: the function is right by the
standard and not only by what gcc and clang do); the comma operator with `rt_enter` and `rt_leave`
(the saved limits would need a stack of unbounded depth in the runtime,
or a fixed one that is a limit on nesting); a remaining count
decremented at every level (a stack again, and an unwind to write);
counting only inside a `within` (a test in each operator for no
difference in what a program computes).

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
