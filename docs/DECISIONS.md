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

**D8. A call is `(op a b)`: five binary operators, `+ - * / %`, each
with exactly two operands.** *(Default)* Prefix and parenthesised
because that is what the reader already reads (lists, symbols and
integers, each with its position), so the step adds no syntax. `/` is integer division and `%`
the remainder (D11). Exactly two operands: no operator has a one-operand
or many-operand form, so there is no arity rule to remember and no fold
order to get wrong (`(- 1 2 3)`, left or right?), and an operand count
other than two is a compile error (D15). A program is still one form
(step 0), so a program is a literal or a call. Rejected: infix with
precedence (a parser with a precedence table, for a language whose
reader is three kinds of form); variadic `+ - *` (a fold direction and
a place for the overflow to be checked, per D10, that a test must pin);
a one-operand `-` for negation (an arity case for one operator; `(- 0
x)` does it, and faults on the minimum like any subtraction, D10);
names (`add`, `rem`) over symbols (longer, and nothing needs them);
`%` as modulo (D11).

**D9. An integer is an optional `-` and then one or more of the digits
`0` to `9`, and nothing else.** *(Default)* This is what the reader does
now, written down because the operators make a nearby mistake easy:
`+5`, `1_0`, `1.5`, `0x10`, `--1` and `-` alone are symbols, not
integers, and so, as a program or an operand, a compile error (D15).
`007` is 7 and `-0` is 0. Whitespace is space, newline, tab and carriage
return only; anything else, a no-break space say, is part of the atom. A
second implementation must not use its own language's `int()`, which
takes `+5`, `1_0` and the digits of other scripts. Rejected: a `+`
sign on a literal (it would make `+5` and `(+ 5 ...)` a lookahead
problem for a reader that has none); underscores and radix prefixes
(nothing needs them; D6).

**D11. `/` truncates toward zero, and `%` takes the sign of the
dividend, so `a = (a / b) * b + a % b` always holds.** *(Default)*
`(/ -7 2)` is -3 and `(% -7 2)` is -1; `(/ 7 -2)` is -3 and `(% 7 -2)`
is 1. A zero divisor, for either, is the fault `division by zero`
(D3). The minimum integer divided by -1 is 2^62, out of range, so it
is the fault `integer overflow` (D10); the minimum `%` -1 is 0 and
faults nowhere. Truncation is what the hardware's divide does and what
C does, so a native target later (D2) does it with no fix-up, and it
makes `%` the remainder that C programmers expect. Python's `//` and
`%` floor: a model or referee written with them gets -4 and 1 for
`(/ -7 2)` and `(% -7 2)`, and passes every positive test. Rejected:
floor division (the natural answer in the language models are written
in, and a fix-up on every divide on the hardware); Euclidean division
(a non-negative remainder is nice and agrees with neither C nor the
hardware); a fault for a negative operand (a calculator that refuses
`-7 / 2`).

**D12. Operands are evaluated left to right, both always, before the
operation; the first fault to happen is the fault reported; nothing is
folded at compile time.** *(Default)* `(+ (/ 1 0) (* big big))` is
`division by zero` and `(+ (* big big) (/ 1 0))` is `integer overflow`.
`(* 0 (/ 1 0))` is `division by zero`: no operator short-circuits, and
the compiler may not notice that the product is 0. A call whose operands
are literals, `(+ 4611686018427387903 1)`, faults when the program
runs, not when it is compiled, because a golden test can only test a
running program (D4) and because a folding compiler would need its own
copy of D10 and D11 to be wrong in. Which fault shows matters because
the fault message is the test's whole output. Rejected: unspecified
order (C's is, and gcc and clang differ: see CLAUDE.md, code style);
right to left; short-circuiting `*` by 0; constant folding (a second
implementation of the arithmetic inside the compiler, with nothing to
check it).

## Values and memory

**D10. An operation whose exact result is outside the 63-bit range is
the fault `integer overflow`; nothing wraps, saturates or grows.**
*(Default)* The range is -4611686018427387904 to 4611686018427387903
(LANGUAGE.md); `+ - * /` can leave it, `%` cannot. Each operation is
checked on its own result, as it happens, so `(- (+ max 1) 1)` faults
though the final value would fit. The fault is D3's: `fault: integer
overflow` on stderr, exit 1, after whatever stdout had (nothing yet).
The edges are the tests: a result of exactly the maximum or the minimum
is fine, one past is a fault, and `(* -2147483648 2147483648)`, which is
exactly -2^62, is fine. Rejected: wraparound (a program's value would
depend on how many bits a value has, which no test could then tell
from a bug); saturation (the same, and quietly); promoting to a bignum
(a heap, a tag, a collector, for a calculator whose literals are
63 bits; D1); a fault only when the final value is out of range (the
checked step is then not a step); a different message for each operator
(the message is the test's output; the operator is in the source).

## Runtime

**D3. A fault ends the program: its message on stderr, exit 1, after
whatever stdout had.** *(Default)* So a golden test checks a fault as
two lines, the message and `exit: 1`.

**D13. The runtime does the arithmetic: `rt_add`, `rt_sub`, `rt_mul`,
`rt_div`, `rt_rem` in `runtime/rt.c`, each taking two values and
returning one, or faulting through `rt_fault`.** *(Default)* Each
decodes both to `int64_t`, computes in `int64_t`, checks the result
against `RT_INT_MIN` and `RT_INT_MAX` (new in `rt.h`), and encodes it.
For `+` and `-` two 63-bit operands cannot overflow 64 bits, so the
plain operation is defined and only the range check is needed. For `*`
the product can pass 64 bits, so it is
`__builtin_mul_overflow` into an `int64_t` and then the same range
check; a signed multiply that overflows is undefined C, and UBSan
(`make sanitize`) says so. For `/` and `%` the zero divisor is checked
first; the minimum is only 2^62 in magnitude, so `INT64_MIN / -1`, the
one divide that traps, cannot occur. The builtin's result is written to
a variable in a statement of its own, and the check reads it in the next
(CLAUDE.md, code style: never a variable and the call that sets it in
one argument list). Decoding is an arithmetic right shift, as
`rt_print` already does. Plain functions in `rt.c`, not inlined from
`rt.h`: speed is not a goal yet. Rejected: arithmetic on the tagged
words (`+` and `-` work on them, `*` needs one operand decoded and `/`
both, so three recipes for five operators, where one recipe works for
all); `__int128` for the product (not every C compiler has it; the
builtin is checked); the compiler emitting the arithmetic inline
(the fault logic would be in the generator, where a unit test can't
reach it and every call site repeats it).

## Compiler

**D4. A compile error can't be a golden test; it's a unit test.**
*(Default)* `t/run.sh` calls a failed compile a failure, which is what
it should be for a test that's meant to run. Messages and positions
are checked in `compiler/tests/`. Rejected: a `; compile-error:` header
line in a golden test; it would come when a language has enough
compile errors to want it.

**D14. The generated C is straight-line: one statement per node, each
result in a fresh temporary, numbered in the order evaluated.**
*(Default)* `(+ (* 2 3) 4)` becomes `t0 = rt_int(2)`, `t1 = rt_int(3)`,
`t2 = rt_mul(t0, t1)`, `t3 = rt_int(4)`, `t4 = rt_add(t2, t3)`, `return
t4`. It is what makes D12 true: C leaves the order of a call's
arguments unspecified, so `rt_add(rt_div(...), rt_mul(...))` would pick
the fault by compiler, and does (CLAUDE.md, code style). It also keeps
the C flat: clang stops at 256 levels of brackets, and a program that
nests a call per level, which a calculator's long expression does, would
not compile. The tests nest 1000 deep. The compiler's own recursion
(Node's stack) runs out near 5000 levels as `langc: internal error`;
no depth beyond the tests' is promised. Rejected: nested C calls (both
reasons above); the comma operator or GNU statement expressions to force
an order inside one expression (still deep, and not C everywhere); an
explicit stack machine in the output (a second evaluator to be wrong).

**D15. A malformed call is a compile error with a message and a
position, found before anything runs.** *(Default)* All of a program's
forms are checked before any C is written, so a bad form after a
faulting one still gives no output but the error. In order of the
program's text, outer form before inner, left before right, the first
found is the one reported:

- `()`: `empty form`, at the `(`.
- a head that is not a symbol, `(1 2)`: `expected an operator`, at the
  head.
- a head that is a symbol but not one of the five, `(foo 1 2)`:
  `unknown operator 'foo'`, at the head.
- an operand count other than two: `'+' takes 2 arguments, got 1`, at
  the `(` of the call.
- a symbol as a program or an operand, `x` or `+` alone: the existing
  `can't compile symbol yet`, at the symbol. An operator is not a value.
- the existing `integer out of range` and `a program is one form`.

They are unit tests in `compiler/tests/` (D4), the messages and the
positions both. Rejected: a golden test for a compile error (D4); a
message that says what the operator is for; collecting every error
(the compiler stops at the first, as it does).

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
