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
that prints the value.** (Run by an interpreter on the `interpreter`
branch: D28.) *(User: "let's make a small calculator language
to work out these steps.")* The language exists to exercise the
process: steps, models, checks. It grows only as far as that needs.

**D2. The compiler is TypeScript run by Node as it is, and emits C.**
*(Default)* C so step 0 runs wherever there's a C compiler; a native
target through a target interface when something needs one. Node's
type stripping, so there's no build step; the compiler uses only
erasable syntax (no parameter properties, no enums). (On the
`interpreter` branch there's no compiler: D28, D29.)

**D28. An interpreter, not a compiler: on the `interpreter` branch the
calculator is built again as one, from its decisions and its tests.**
*(User, Nov 2026: "How applicable would the process be for an
interpreter rather than a compiler?", then "Let's make a branch of
esoteric language workbench with those changes." The rule for errors
before running, and its exit 2, are a default, Claude's, fair to
revisit.)* The language is
the calculator's as it stands on main after step 5, D3 to D25, and its
46 golden tests, its models and its referee are the spec: what a
program prints doesn't change. The compiler, the runtime and the C they
make are main's, and the decisions about them, D2, D14's encoding, D26
and D27, don't bind the interpreter, which keeps their observable part
(D11's booleans, D25's order, D21 to D24's budgets) its own way. What
the compiler reported before a program ran (D3's arity, an unknown
name, a literal past the range, the forms of D13 and D24) the
interpreter reports before it evaluates anything, so `(if #false (+ 1
2 3) 0)` is an error and not `0`: `FILE:LINE:COL: message` on stderr
and exit 2, kept apart from a fault (D6, exit 1), since one process now
does both. Such an error is a unit test, as before (D7). Rejected:
checking a form only when it's evaluated (a program's errors would
depend on which branches it takes, which no program on main's compiler
could show); exit 1 for both (a test couldn't tell a program that
faults from one that never ran).

**D29. The interpreter is TypeScript, run by Node as it is: a
tree-walker over the reader's forms.** *(Default)* The workbench's
tooling is TypeScript already, and the referee is Python, so the two
implementations of the language stay in different hosts
(`docs/PROCESS.md`, "An interpreter instead of a compiler"). Node's
type stripping and erasable syntax only, as D2 had it. Where Node's
behaviour and the decisions could differ, `DESIGN.md`'s "What the host
gives" says what the interpreter inherits, what it overrides and how,
answered at step 0, before the code. Rejected: a bytecode VM in C (a
compiler and a runtime in all but name, which main has); Python (the
referee's host, and two implementations in one host share its blind
spots); a bytecode VM in TypeScript (a step of its own, if speed is
ever wanted).

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

**D21. For a budget, an operation is one application of an operator:
any of the seventeen, `+` to `**`, each counting one.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)*
D20 says "a budget of n operations", and the language's operations are
its operators (`LANGUAGE.md`: arithmetic, the comparisons, the bit
operations, `**`). `(** 1 4611686018427387903)` is one operation,
however the runtime computes it. A literal, an `if` and a `within`
are not operations: they compute no value of their own, they choose or
limit what does. So what a program costs is the number of operator
applications it evaluates, at run time, which can be read off the
program and the values of its `if` tests: a branch not taken isn't
evaluated (D13) and costs nothing, and a test and a taken branch cost
what their operators cost. The compiler doesn't fold constants, so
`(+ 1 2)` is charged at run time like any other. A form added later
says in its own decision whether it's an operation; a call, when calls
come, will need to be one, or a recursive program would run outside
every budget. Rejected: counting every form evaluated, literals
included (the cost would depend on how a value is written, not on the
work done); counting `if` too (the other consistent choice, turned
down because a choice computes nothing and D20's word is operations;
the one most worth the person's look); weighting `**` by its
multiplications (the count would be the runtime's squaring loop, which
D19 doesn't specify, and a model would have to mirror `rt_pow` to
compute it); counting `within` (it limits operations rather than doing
one).

**D22. `(within n expr)` lets `expr` perform `n` operations; the one
that would be the n+1th faults `budget spent` instead of running. An
operation is charged when it's applied: after its operands have been
evaluated, before it checks or computes anything.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)*
So `(within 3 (+ (* 2 3) (- 10 4)))` is 12, with a budget of 2 it
faults, and `(within 0 42)` is 42. After the operands, because that's
when an operation happens: in `(within 1 (+ (/ 1 0) 2))` the division
is the first operation, the budget allows it, and it faults `division
by zero`. Before the operator's own checks, because the budget decides
whether the operation happens at all, and one that doesn't happen
can't fault some other way: `(within 0 (/ 1 0))` faults `budget
spent`. The value of `(within n expr)` is the value of `expr`, of
whatever type: `(within 1 (< 1 2))` is `#true`. `budget spent` is a
fault like the others (D6): the program ends, the message on stderr,
exit 1, nothing on stdout. `within` doesn't catch it, and nothing in
the language does. Rejected: "spent" as the moment the count reaches
`n`, so that a budget of `n` allows `n - 1` (D20 says a budget of n
operations); charging an operation when its form is entered, before its
operands (then `(within 1 (+ (/ 1 0) 2))` faults `budget spent` for an
addition that never happens); checking before charging (then an
operation the budget refuses still reports its own fault, and which
fault a spent budget gives depends on what the refused operation would
have done); a value instead of a fault when the budget runs out,
`#false` or a default (D20 says it faults, and a value would need a way
to tell it from `expr`'s own).

**D23. Budgets nest, and every budget in force applies: an operation
is charged to all of them, and faults if any is spent.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)* So an
inner `within` can't give more than the outer has left: `(within 1
(within 5 (+ (+ 1 2) 3)))` faults, as does `(within 5 (within 1 (+ (+
1 2) 3)))`. When an inner `within` ends, what it didn't use is dropped,
and the outer has paid for what it did: `(within 3 (+ (within 5 (+ (+
1 2) 3)) 4))` is 10, and with a budget of 2 outside it faults. Asking
for more than the outer has left isn't a fault in itself; the fault
comes only from an operation that finds a budget spent. A program
starts with no budget in force: outside every `within` nothing is
counted against anything, so every program written before this runs
as it did. Rejected: an inner budget replacing the outer while it's in
force (a budget that any expression inside can escape, by asking for
more, isn't a budget); reserving all of an inner `n` from the outer
when the inner starts (it charges for work not done, and faults a
`within` that would never have used what it asked for); a fault on
entry when `n` is more than the outer has left (a second rule for the
same limit, which would fault programs that fit).

**D24. `within` is a special form of two parts. Its budget is any
expression, evaluated first, under the budgets already in force, and
must be an integer that isn't negative.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)* A special form and not
an operator, since the budget has to be in force before `expr` is
evaluated, and an operator's operands are evaluated before it's applied
(D25). `(within)`, `(within 5)` and `(within 1 2 3)` are compile
errors, `within takes 2 arguments, not N` at the form, as `if`'s are
(D7, D13), and `within` on its own is an unknown name, as `if` is. The
budget is evaluated before `expr` and isn't under the new budget: its
operations are charged to the budgets around the `within`, so `(within
1 (within (+ 1 1) (* 3 4)))` faults (the `+` spent the outer's one)
where `(within 2 (within (+ 1 1) (* 3 4)))` is 12. Then it's checked:
a boolean faults `not an integer` (D14), a negative integer faults `bad
budget`, both before `expr` is evaluated, so `(within -1 (/ 1 0))`
faults `bad budget`. At run time, even for a literal, as `(** 1 -1)`
is (D19). 0 is a budget: under it only an expression with no
operations runs. Any integer from 0 to the largest is one. `budget
spent` (D22) and `bad budget` join D17's and D19's fault names.
Rejected: a negative budget taken as 0 (a silent answer to what is
nearly always a mistake, as D16 and D19 rejected); a budget that must
be a literal, checked by the compiler (every other operand in the
language is an expression, and a budget computed from the program's
own values is the natural use); a compile error for a negative literal
on top of the run-time fault (two places for one rule); a one-part
`within` with a default budget (a number nobody chose).

**D25. Evaluation is left to right: an operator's left operand
completely, then its right, then the operator; an `if`'s test, then one
branch; a `within`'s budget, then its body. Where a program could fault
in more than one place, the first fault in that order is the one
reported.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)* Until now nothing said, and a program's output depended on
the C compiler: each operation is a C call with its operands as
arguments, C doesn't order a call's arguments, and `(+ (/ 1 0) (+ #true
1))` faults `not an integer` under gcc, which happens to evaluate the
right operand first, and `division by zero` under clang. No test had a
program like that, so the suite passed under both. A budget makes it
every program that runs out: `(within 1 (+ (* 2 3) (/ 1 0)))` faults
`budget spent` left to right and `division by zero` right to left, and
D22's charge point can't be tested without an order. What stays open is
the order of one operator's own checks, where a single application
could fault two ways (`(bit/shl #true 99)`, which `CLAUDE.md`'s Status
lists as not agreed): D22 puts the budget's charge before all of them,
and nothing else about them is decided here. Rejected: leaving it to
the C compiler (a program's output would differ between the cloud
machine's gcc and the person's clang); right to left (nothing for it,
and the referee and the models already read left to right).

**D30. Nesting is limited to 1000 deep, an error before running; and a
fault in the interpreter itself exits 3.** *(Default, written by the
builder of the interpreter's step 0, which could not ask; fair to
revisit.)* The evaluator recurses on Node's stack, which gives out at a
depth that varies with the Node version and the machine, in words of its
own. A fixed limit checked by the reader makes the same program behave
the same under every Node (`make golden-node`) and keeps the evaluator
far inside the stack: `FILE:LINE:COL: nested too deeply (limit 1000)` at
the form that opens the 1001st level, exit 2. The golden tests nest at
most 147. D28 names `lang: internal error: ...` for a fault in the
interpreter but no status; 3 keeps it apart from a program's fault (1)
and an error before running (2). Rejected: no limit, catching the host's
`RangeError` (the depth would differ between Nodes and the failure
would come mid-run, perhaps after a `within` had charged); a trampoline
or an explicit evaluation stack (machinery for a depth no program has,
though the calculator has no calls, so nesting is all the depth there
is; overtaken by D34, which gives programs calls 10,000 deep); exit 1 for an internal error (indistinguishable from a fault).

**D31. Functions: a program is any number of definitions, `(def (name
param ...) body)`, and then one expression; a call is `(name arg
...)`.** *(Default, Claude's, written for the interpreter experiments
the person asked for, to check what is particular to an interpreter;
fair to revisit.)* A definition names a function, its parameters (none
or more, each a name: a symbol, never an integer or a boolean) and its
body, one expression. The definitions
come first and the expression last, and every definition sees every
other whatever their order, so functions may call themselves and each
other. A parameter is visible in its own function's body and nowhere
else, and evaluates to the value the call gave it. A call applies a
defined function to as many arguments as it has parameters. Functions
are not values: a function's name is only ever a call's head, and a
parameter only ever a value, so the language stays first order. Each of
these is an error before running (D28): a definition after the
expression, or anywhere but the top; a program of definitions with no
expression; two definitions of one name; a definition whose name is an
operator, `if`, `within` or `def`; a `def` of other than two parts, or
whose first part isn't a list of names; two parameters with one name,
or a parameter with the name of a function, an operator, `if`, `within`
or `def`; a call with the wrong number of arguments (`f takes 2
arguments, not 3`, as an operator's); a name that is neither a
parameter in scope nor a call's head; a function's name used as a
value; a parameter used as a call's head. Rejected: functions as values,
and `lambda` (closures are a step of their own, and not what this one
is for); definitions of values; definitions inside a body.

**D32. A call evaluates its arguments left to right, then is charged
as one operation, then is checked for depth (D34), then evaluates the
body with the parameters bound to the arguments.** *(Default, Claude's,
as D31.)* D21 said a call would need to be an operation when calls
came, or a recursive program would run outside every budget: so `(within
1 (f (+ 1 2)))` faults `budget spent` whatever `f`'s body is, the `+`
and the call being two. Charged after the arguments and before the
body, as D22 charges an operator after its operands and before its own
checks. The arguments' order is D25's: the first fault in it is the
one reported. A function's body runs under every budget in force where
it's called (D23), whichever function's `within` set it. Rejected: calls free (D21's reason); charging when the
call's form is entered, before the arguments (D22's reason); charging
when the body returns (a call that never returns would never be
charged).

**D33. A call in tail position replaces its caller, so any number of
tail calls run in constant space.** *(Default, Claude's, as D31.)* A
function's body is in tail position, and so are both branches of an
`if` in tail position; nothing else is: not an operator's operand, an
`if`'s test, a call's argument, a `within`'s budget or body (when the
body ends the outer budget is put back, so the `within` is still in
progress), nor the program's own expression (a call from it makes
depth 1, D34). The language has no loop but a function that calls itself,
so this is what makes a loop: `(def (count n acc) (if (== n 0) acc
(count (- n 1) (+ acc 1))))` and `(count 1000000 0)` is `1000000`. A
tail call is still charged (D32), and adds nothing to the depth, so it
never faults `stack`. Rejected: no tail calls (every loop would be
bounded by D34's depth); a `within`'s body in tail position (the budget
is put back after it, which is work the caller still has to do).

**D34. Calls not in tail position may nest 10,000 deep; the call that
would make it 10,001 faults `stack`.** *(Default, Claude's, as D31.)*
The depth is the number of calls in progress, a tail call replacing its
caller rather than adding to it (D33); the program's expression is at
depth 0, and a call from it makes depth 1. So `(def (sum n) (if (== n
0) 0 (+ n (sum (- n 1)))))` gives `(sum 9999)` as `49995000`, ten
thousand calls from `(sum 9999)` down to `(sum 0)`, and `(sum 10000)`
faults `stack`: `fault: stack` on stderr, exit 1, as
every fault (D6). The check comes after the call's charge (D32) and
before its body, so a call refused for depth has been charged, and one
refused by its budget never reaches the check. A fixed number, so a
program behaves the same under every Node and on every machine, which
the host's own stack doesn't (`make golden-node`), and one past what a
tree-walker reaches if it recurses on the host's stack for every call,
so the interpreter decides its depth and the host doesn't. That
overtakes D30's reason for keeping the evaluator on the host's stack
(no program was deep enough to need a stack of its own): one now is.
D30's limit on nesting in the source is another thing and stays. Rejected: no limit
(the failure would come when memory ran out, in the host's words); the
host's stack as the limit (it differs between Node versions and
machines, and a golden test at the edge would pass on one and fail on
another); a limit as low as a naive tree-walker reaches (the language's
depth would be the host's accident).

**D35. The messages and positions of D31's errors, and where a
program's reading and its checking divide.** *(Default, written by the
builder of the interpreter's step 6, which could not ask; fair to
revisit.)* D31 says which errors come before running, not what they
say. Each is `FILE:LINE:COL: message` (D28), at the form D31 names: a
definition after the expression, or a second expression, at the form
that breaks the shape (the first form after the expression); a program
of definitions with no expression, at the last definition; `def takes 2
arguments, not N` as an operator's arity is worded; a definition whose
first part isn't a list with a name first, at the name or, if there is
none, at that part; a name that is
an operator or `if`, `within` or `def`, at the name; two definitions of
one name, at the second; a parameter that isn't a name, at it; two
parameters named alike, or a parameter named as a function, at the
second; a call's arity as `f takes 2 arguments, not 3`, at the call; a
function's name used as a value, or a parameter as a call's head, at
that name. The reader reads any number of top-level forms and only
their nesting and literals are its errors (D30, D31), so a shape error
is the checker's; an error the reader finds in a later form comes before
a shape error the checker would find in an earlier one, since the reader
runs first. Rejected: the shape errors in the reader (it would have to
know which forms are definitions, and the reader's job is text to forms,
D29); a single message for every shape error (a program's author then
can't tell which shape is wrong, the one thing D31's list is for).

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
that the compiler can't know what an `if` gives. (The compiler's
encoding: the interpreter represents a value its own way, D28.)

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

**D27. The runtime keeps the budget as two counts: `spent`, the
operations done since the program started, and `limit`, the count at
which the next one is refused, at first the largest `int64_t`, which is
no budget.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)* Each of the seventeen operators' runtime functions charges
first, before `need_ints` or any other check (`rt_eq` and `rt_ne`
too, which have none): if `spent` equals `limit`, fault `budget spent`,
otherwise add one to `spent`. `rt_within(n)` checks `n` (`not an
integer`, then `bad budget`), saves `limit`, lowers it to `spent + n`
if that's lower, and returns the saved limit; `rt_within_end(saved, v)`
puts the saved limit back and returns `v`. Because the limits are
counts from the start of the program, the innermost is the lowest, so
checking one count against it checks every budget in force (D23), and
an inner `within`'s end has only to restore the outer's limit, the
outer having seen every operation through `spent`. `spent + n` is
computed only when `n < limit - spent`, so it can't overflow; `spent`
itself would take centuries to reach 2^63. `rt_test` and `rt_print`
are not operations and don't charge. Rejected: a stack of what each
budget has left, all decremented on every operation (D23's own
wording, and the referee's, but a cost per operation that grows with
the nesting, and a stack to size); the charge emitted by the compiler
around each call (the charge must come after the operands and before
the checks, which is a runtime function's entry, and the runtime is
where the checks are). (The compiler's runtime: on the `interpreter`
branch, any mechanism that keeps D21 to D24, D28.)

## Compiler

**D7. A compile error can't be a golden test; it's a unit test.**
*(Default)* `t/run.sh` calls a failed compile a failure, which is what
it should be for a test that's meant to run. Messages and positions
are checked in `compiler/tests/` (`interp/tests/` on the `interpreter`
branch, where such an error comes before evaluation, D28). Rejected: a `; compile-error:` header
line in a golden test; it would come when a language has enough
compile errors to want it.

**D26. The generated C sequences what C's argument order doesn't. An
operator whose operands are both lists evaluates them into two
temporaries first, with C's comma operator: `(+ (/ 1 0) (+ #true 1))`
is `(t0 = rt_div(...), t1 = rt_add(...), rt_add(t0, t1))`. A `within`
is `(b0 = rt_within(N), rt_within_end(b0, E))`.** *(User: accepted as proposed, 2026-11-06, from three proposals; `docs/MODELS.md`, "The untested case, run".)* The comma
operator is sequenced, so the left operand is finished before the right
starts (D25), and a `within`'s budget is in force before its body
starts (D24); C's `?:` already evaluates an `if`'s test first, and
stays. An atom operand, an integer or a boolean, has no effect and
can't fault, so where either operand is an atom the call is emitted as
it is now, `rt_mul(rt_add(rt_int(1LL), rt_int(2LL)), rt_int(-3LL))`,
and the C the existing unit tests read is unchanged. Two temporaries
and not one: `(t0 = L, rt_add(t0, R))` puts `R` two brackets deeper
than now, and a program nested to the right then hits clang's limit of
256 at about 125 levels instead of about 250; with both operands in
temporaries the depth is what it was (checked while proposing: 250
levels compile under clang and 255 don't, before and after). The
temporaries are numbered by the compiler, one name per use, and
declared at the top of `lang_main`: `rt_value` for operands, `int64_t`
for a `within`'s saved limit (D27). Rejected: relying on C's argument
order (the gcc and clang difference D25 records); straight-line C, one
statement per operation (also right, and it would retire the bracket
limit for operators, but it rewrites the code generator and the
unit tests that read its C, and the bracket limit is a decision of its
own, still waiting); GNU statement expressions, `({ ... })` (two
brackets a level, so the limit halves); a temporary for every operand,
atoms too (it changes the C of every program for nothing an atom
needs). (The compiler's: on the `interpreter` branch D25's order is the
interpreter's to keep, D28.)

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
