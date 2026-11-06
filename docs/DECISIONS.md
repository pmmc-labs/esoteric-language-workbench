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

**D8. Five operators, `+ - * / %`, each written `(op a b)` with exactly
two operands.** *(Default)* An operand is an integer literal or another
operation, so a program is a tree of them, and its value is the root's.
Exactly two operands, so there's no fold to put in an order, no identity
for `(+)`, and no meaning to choose for one operand; negation is
`(- 0 x)`, and a negative number is already a literal. A list of any
other length is a compile error (D13). Rejected: variadic `(+ 1 2 3)`,
as Lisps have it: it needs a fold order, a ruling on whether an
intermediate sum that overflows faults when the whole wouldn't, an
identity for no operands, and a meaning for one that differs by
operator (`(- x)` negates; `(/ x)` would be a reciprocal, which has no
integer), four decisions for a shorthand, and a long chain nests one
level of C per term (CLAUDE.md, code style). A unary `(- x)` beside the
binary one: `(- 0 x)` says it. The names `quot` and `rem`, or `div` and
`mod`: `/` and `%` are what someone writing a calculation writes, and
D10 says which division they are.

**D9. An operation's result is the exact integer result, and one
outside 63 bits is a fault, `integer overflow`.** *(Default)* The range
is step 0's, -4611686018427387904 to 4611686018427387903. The rule is
on each operation's mathematical result, an intermediate one included:
`(* (+ 4611686018427387903 1) 0)` faults, though the whole would be 0.
So a model's rule is one line: compute in unbounded integers, and fault
on a result out of range. What follows from it, written down so it's
decided before it's met: the check is at 63 bits, not the machine's 64,
so `(* 2147483648 2147483648)`, which is 2^62, faults though an int64
holds it, and `(* 4294967296 4294967296)`, 2^64, faults though int64
arithmetic wraps it to 0, which is in range; `(/ -4611686018427387904
-1)` is 2^62 and faults; `(% -4611686018427387904 -1)` is 0 and
doesn't (D10). Rejected: wrapping at 63 bits, as the hardware wraps at
64: a calculator that prints a wrong answer without a word is worse
than one that stops, and a model of wrapping has to mirror the
encoding. Saturating at the range's ends: a wrong answer too. Integers
of any size: a heap and a bignum library, which D1 doesn't need.

**D10. `/` truncates toward zero and `%` takes the dividend's sign; a
divisor of zero is a fault, `division by zero`.** *(Default)* So
`(/ -7 2)` is -3 and `(% -7 2)` is -1, `(/ 7 -2)` is -3 and `(% 7 -2)`
is 1, `(/ -7 -2)` is 3 and `(% -7 -2)` is -1, and `a` is always
`b * (a / b) + a % b`. It's C's division (since C99) and the
hardware's, so the runtime divides directly once it has checked the
divisor, and `%`'s result is never out of range. Both `/` and `%`
fault on zero. The trap, for a model in Python: Python's `//` and `%`
floor, and give -4 and 1 for -7 and 2, so a model works truncation out
itself (on the magnitudes, with the sign put back) rather than using
them. Rejected: floored division (Python's, Haskell's `div` and `mod`):
a remainder by a positive divisor is then never negative, which is
nicer for clocks and indexes, but every C compiler and CPU truncates,
so the runtime would correct every division whose operands differ in
sign, and a calculator's user reads `-7 / 2` as -3.5 cut to -3.
Euclidean division (a remainder never negative): least expected of
`%`. `(% x 0)` as `x`, as some languages have it: a wrong answer
again, where D9 chose a fault.

**D11. Operands are evaluated left to right, and the first fault ends
the program.** *(Default)* Which fault is reported depends on the
order: `(+ (/ 1 0) (+ 4611686018427387903 1))` is `division by zero`,
and with its operands swapped, `integer overflow`. C doesn't order a
call's arguments, and gcc and clang differ (CLAUDE.md, code style), so
C that passes two operations as one call's arguments would report
either, by the C compiler; the codegen sequences the operands itself,
the left one's value computed in a statement, or a comma expression,
before the right one's. Rejected: order unspecified, as C and Scheme
leave it: a faulting program's output would then depend on the C
compiler, and its golden test would pass under gcc and fail under
clang, which is the bug the person's machine has found once already.
Right to left: nothing recommends it.

## Values and memory

## Runtime

**D3. A fault ends the program: its message on stderr, exit 1, after
whatever stdout had.** *(Default)* So a golden test checks a fault as
two lines, the message and `exit: 1`.

**D12. A fault happens when the program runs, even in an expression of
constants, and its message says what went wrong, not where.**
*(Default)* Every operation runs at run time: the compiler doesn't fold
`(/ 1 0)` or `(+ 4611686018427387903 1)` into a compile error or a
warning, so a faulting program compiles, and its golden test is the
fault (D3): `fault: division by zero` on stderr and `exit: 1`, with
stdout empty, since the value is printed only at the end. The message
is the bare text D9 or D10 gives, with no line or column: the runtime
doesn't know where an operation came from, and telling it means a
position passed to every operation. Rejected: constant folding: an
optimisation a calculator doesn't need, and it would turn every
faulting program into a compile error, so into a unit test (D4), since
in this language every program is constants. Positions in a fault's
message: worth having once programs are long; machinery now.

## Compiler

**D4. A compile error can't be a golden test; it's a unit test.**
*(Default)* `t/run.sh` calls a failed compile a failure, which is what
it should be for a test that's meant to run. Messages and positions
are checked in `compiler/tests/`. Rejected: a `; compile-error:` header
line in a golden test; it would come when a language has enough
compile errors to want it.

**D13. A malformed expression is a compile error, at the form at
fault, with one of six messages.** *(Default)* Checked by unit tests
(D4). The whole program is checked before anything runs, so a program
with an error anywhere in it is a compile error, never a fault (D12).
A list's shape and operator are checked before its operands, and its
operands left to right; the first error found is the one reported, and
the compiler stops there. The messages, exactly:

- `()`: `empty list`, at its `(`.
- A list whose first item isn't a symbol, `(1 2 3)` or `((+ 1 2) 3)`:
  `expected an operator`, at that item.
- A symbol other than D8's five where an operator goes, `(max 1 2)`:
  `unknown operator max`, at the symbol.
- One of the five with other than two operands, `(- 5)`:
  `- takes 2 operands`, at the list's `(`.
- A symbol where an operand or the program goes, `x`, `(+ 1 +)` or
  `+5` (which isn't a literal: a literal is an optional `-` and
  decimal digits): `unexpected symbol x`, at the symbol.
- An integer literal out of range, anywhere in the program:
  `integer out of range`, at the literal, as step 0 has it.

So `(+ 99999999999999999999)` is `+ takes 2 operands`, the list before
its operand, and `(max 99999999999999999999 1)` is `unknown operator
max`. Step 0's `a program is one form` stays as it is. Rejected:
reporting every error found: a program here is a line or two, and one
is enough. Messages that spell out the shape wanted (`expected (op a
b)`): longer and no clearer.

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
