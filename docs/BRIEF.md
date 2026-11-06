# Brief: step 1, arithmetic

For whoever builds step 1 of `PLAN.md`. The step's text is there; this is
the order to do it in, what to read, what to leave alone, and how to
report. Where the brief and the plan disagree, the decisions win, and the
brief is wrong: say so in your report.

## Before you start

- **The picks come first.** D20 to D28 are defaults. If the person has
  picked them, the log says so, with any change. If they haven't, or a
  default was turned down, stop: the step is rewritten before anything is
  built.
- **Size.** Step 1 is marked large in `PLAN.md`. Compare that with your own
  model, as `CLAUDE.md` and `docs/MODELS.md` ask. If you're smaller, say so
  before you start and stop at the first escalation signal below.

## Read, in this order

1. `CLAUDE.md`, all of it. The working rules matter most.
2. `docs/LANGUAGE.md`: the language as it is.
3. `docs/PLAN.md`: step 0 and step 1 only.
4. `docs/DECISIONS.md`: D1 to D7, then D20 to D28. Check the log before
   changing anything.
5. `docs/PROCESS.md`: "Golden tests from an independent source", and
   "Mechanical checks". `t/README.md` and `t/models/README.md`.
6. The code you'll change: `compiler/src/codegen.ts`, `reader.ts`,
   `sexp.ts`, `errors.ts`, `runtime/rt.h`, `runtime/rt.c`, `bin/langc.ts`
   (for how `cc` is run), `compiler/tests/codegen.test.ts` (for the style
   of unit tests), and `t/run.sh` (skim).

**Do not read `t/referee/`.** It is the second implementation the step's
model is checked against. A builder who has read it can't tell agreement
from copying.

## Do, in this order

1. `make -C /home/user/wtp-haiku hooks`, then `make -C /home/user/wtp-haiku test`.
   It should end with 2 golden tests passing and checks at 0 failed. If it
   doesn't, stop and report that before changing anything.
2. **The model.** Write `t/models/arith.py` from D20 to D28. Do not write
   it from `codegen.ts` or `rt.c`. It computes each expected output from
   the definition: Python's integers are unbounded, so compute the exact
   result and then apply the range of D23. Division truncates toward zero
   (D24); `//` floors, so don't use it. A fault's expected output is
   `fault: MESSAGE` and then `exit: 1`, on the same stream as the
   value. Its docstring lists one command per test, in the form
   `python3 t/models/arith.py --program NNN > t/NNN-name.lang` and
   `python3 t/models/arith.py NNN > t/NNN-name.expected`, as
   `t/models/README.md` shows.
3. **The tests.** These are the programs; the expected outputs come from
   the model, not from you.

   | Test | Program |
   |---|---|
   | `050-add` | `(+ 2 3)` |
   | `051-sub` | `(- 2 7)` |
   | `052-mul` | `(* -3 4)` |
   | `053-nested` | `(* (+ 1 2) (- 10 4))` |
   | `054-div-truncates` | `(/ -7 2)` |
   | `055-div-negative-divisor` | `(/ 7 -2)` |
   | `056-in-range-edge` | `(+ 4611686018427387902 1)` |
   | `057-add-overflow` | `(+ 4611686018427387903 1)` |
   | `058-sub-overflow` | `(- -4611686018427387904 1)` |
   | `059-mul-wraps` | `(* 4294967296 4294967296)` |
   | `060-mul-overflow` | `(* -1 -4611686018427387904)` |
   | `061-div-zero` | `(/ 1 0)` |
   | `062-div-overflow` | `(/ -4611686018427387904 -1)` |
   | `063-left-fault-first` | `(+ (/ 1 0) (+ 4611686018427387903 1))` |
   | `064-operand-fault-first` | `(+ 4611686018427387903 (/ 1 0))` |
   | `065-left-overflow-first` | `(+ (+ 4611686018427387903 1) (/ 1 0))` |

   Each `.lang` has a comment line that names `t/models/arith.py`. Run
   `make -C /home/user/wtp-haiku models`, which writes the `.lang` and
   `.expected` files. Then read each pair. Don't patch a file.
4. **The compile errors, as unit tests.** `compiler/tests/arith.test.ts`
   checks each D21 message and its position, using `read` and
   `compileProgram` as `codegen.test.ts` does:
   - `(+ 1)` and `(+ 1 2 3)`: `+ takes two operands`, at the `(`.
   - `(foo 1 2)`: `unknown operator: foo`, at the `(`.
   - `()` and `(1 2)`: `a form must start with an operator`, at the `(`.
   - `x` and `+5`: `a symbol is not a value: x` and `a symbol is not a value: +5`,
     at the symbol.
   - `(+ (/ 1 0) 4611686018427387904)`: `integer out of range`, at the
     literal. This is a compile error, so the division never runs.
5. **The compiler, `codegen.ts`.** Validate the whole tree first (D21),
   then generate. A form becomes C statements. Each operand is generated
   left to right into its own named temporary (D27), and the operator is
   a call on the temporaries. Nothing is evaluated at compile time (D28).
   Keep the functions pure, as the style in `CLAUDE.md` asks: the
   temporary counter goes through as a value. Don't use GNU statement
   expressions; they aren't standard C.
6. **The runtime, `rt.h` and `rt.c`.** Add `rt_add`, `rt_sub`, `rt_mul`
   and `rt_div`. Each decodes its operands (`v >> RT_INT_SHIFT`), computes
   with `__builtin_add_overflow`, `__builtin_sub_overflow` or
   `__builtin_mul_overflow` (D26), range-checks the result against
   `[-2^62, 2^62 - 1]`, and encodes with `rt_int` only after that check.
   `rt_div` truncates toward zero, checks for zero first (`division by
   zero`), and range-checks the quotient (D25). A fault goes through
   `rt_fault`, with the message exactly as D21 and D23 to D24 give it.
7. **Run it.** `make -C /home/user/wtp-haiku test`. Then
   `LANG_CC=clang make -C /home/user/wtp-haiku golden-clang`. Then
   `make -C /home/user/wtp-haiku sanitize`, if clang's sanitizer runtime is
   installed; if it isn't, say so rather than skip it silently.
8. **Docs.** `docs/LANGUAGE.md`: the operators, the faults and the form
   rules, in prose with examples, no tables. `docs/DECISIONS.md`: where
   the person changed a default, record it as their pick (*(User)*) with
   the reason. `docs/PLAN.md`: step 1's heading becomes `(done)`, with a
   note on anything that differs from the text; the progress line moves
   on. `CLAUDE.md`'s Status: one paragraph for step 1, with its tests
   (050 to 065) and its decisions (D20 to D28), and what is next.
9. **Commit** on the worktree's branch, with a subject that names the step
   and its decisions, for example `Step 1: arithmetic, with its faults and
   tests 050 to 065 green (D20 to D28)`. The `make hooks` check needs that.
   Trailers as the session asks. Do not push.

## Do not touch

- `t/referee/`: don't read it or edit it.
- Tests `000` and `001`, and their `.expected` files.
- Any model but `t/models/arith.py`, which is new.
- `DESIGN.md`. Its open questions are the person's.
- `reader.ts`. `+` is not a literal (D22), and nothing else in the reader
  changes.
- `t/run.sh`, `t/checks.py` and the Makefile. Don't weaken a check to get
  green.
- Anything that is not in D20 to D28, which includes: a remainder
  operator, n-ary or unary operators, bignums, constant folding,
  comparisons, booleans, `if`, bindings, and a flag, an environment
  variable or a knob.

## Stop and say so when

- A `.expected` would have to be patched to pass. Rerun the model. If its
  output looks wrong to you, stop: either the model or the compiler is
  wrong, and the decisions say which.
- `make checks` reports that the referee and an `.expected` disagree.
  Stop, and report the test and both outputs. Don't read `t/referee/` to
  settle it; the decisions settle it, and the person reads both.
- A test is still red after two attempts at a fix.
- You're tempted to add a decision, a builtin, a flag or a knob to make a
  test pass. The example bends to the language, not the reverse (D6).
- The diff has grown past what this brief describes.

## Report

Your final message says: which tests landed; the last lines of `make test`;
the result of the clang run and of `make sanitize`, or why it wasn't run;
every point where D20 to D28 didn't say what to do, and what you chose; and
whether the step's Size matched your model. Don't call the step done unless
`make test` is green.
