# Brief: step 1, arithmetic

For the session that builds step 1 of `docs/PLAN.md`. The step is
medium: the design is decided and the tests are named. Compare that
with your own model first (`CLAUDE.md`, `docs/MODELS.md`) and say if
they don't match; if you are smaller than medium, stop and say so.

## Read

In `CLAUDE.md`'s order: `docs/LANGUAGE.md`, `docs/DESIGN.md`, step 1 of
`docs/PLAN.md`, then `docs/DECISIONS.md` D1 to D15, all of which the
step rests on (D8 to D15 are new; read them closely, since they decide
the traps), then `docs/MODELS.md` for the size and escalation rules and
`t/README.md`, `t/models/README.md` for how tests and models are kept. The code is
small: `compiler/src/`, `runtime/`, `compiler/tests/`, `t/run.sh`.

Do not open anything under `t/referee/`, its README included. It is the
second implementation your model is judged against. You may run `make
checks` and read what it prints.

## Do, in this order, `make test` green after each

1. `make hooks`. Then read `make test` once as the baseline: 2 golden
   tests, 0 failed.
2. The compiler's shape (D14), with nothing new in the language: codegen
   emits a temporary per node and returns the last one. 000 and 001 still
   pass, unchanged. Add D15's checks, as a pass over the forms before
   any C is written, with their unit tests in
   `compiler/tests/codegen.test.ts`, and the reader's unit tests (D9) in
   `reader.test.ts`. Write each test's expected message and position from
   D15, not from running the compiler.
3. `+ - *` (D8, D10, D12, D13): `rt_add`, `rt_sub`, `rt_mul` and the
   range in `rt.h`; the codegen case for them; golden tests 002 to 004,
   010 to 013 and 015 to 021 (the rest need `/` or `%`). Write each
   `.lang` and `.expected` by hand from the plan's list before running
   it.
4. `/ %` (D11): `rt_div`, `rt_rem`; tests 005 to 009, 014 and 022 to 027.
5. The model `t/models/arith.py` and tests 028 to 030, as the step
   describes. The model computes the answer from D10 and D11 as
   written, not by calling the compiler and not by copying the
   runtime's code. Its docstring lists its six commands, one a line;
   `make models` writes the files. Then `make test`: the `referee` line
   of `make checks` must say 31 tests agree and none are outside it.
6. Update `docs/LANGUAGE.md` (no tables; every operator, the integer
   rule, both faults, an example of each), `docs/DESIGN.md` as the step
   says, `docs/PLAN.md` (mark step 1 done, with a note where what landed
   differs), and `CLAUDE.md`'s Status: one sentence for step 1 with its
   `Dn` and test numbers, **Next:** to be proposed, and the model you
   were.
7. `LANG_CC=clang make golden`, and `make sanitize`. A runtime change is
   not done until all three pass.

Commit at the end of each item, with `step 1` or a `Dn` in the subject
(`make hooks` checks it). Do not push.

## Do not

- Touch `t/referee/`, `t/run.sh`, `t/checks.py`, `Makefile`, `bin/`, the
  reader (`compiler/src/reader.ts`), or step 0's tests, `000` and `001`.
- Fold constants, nest calls in the generated C, evaluate in any order but
  left to right, or add an environment variable, a flag or a knob (D12,
  D14).
- Add a form, an operator or a message the step doesn't name. If a test
  seems to want one, the test changes (D6).
- Edit an `.expected` to turn a test green, or patch a file a model writes.
  If the compiler and an expected output disagree, redo the arithmetic
  from the decisions by hand; if you still can't say which is wrong,
  stop.
- Decide anything. If D8 to D15 don't settle a question, stop and report
  it as a question; don't pick.

## Stop and report if

The two attempts rule fires (`docs/MODELS.md`); `make checks` says the
referee and a test disagree, and D8 to D15 don't tell you which is wrong
(they usually do: say what you derived); the diff is growing past what the
step names; or anything in "Do not" is the only way forward.

## Report

What landed, by item, with the test numbers; the last lines of `make
test`, `LANG_CC=clang make golden` and `make sanitize`; the `referee:`
line of `make checks`; for the model, what it does for each of the
traps (floor division, the range checked at every node, the integer rule)
in a line each; every place you were unsure or the step's text was
unclear; and the size you built it at, against the step's.
