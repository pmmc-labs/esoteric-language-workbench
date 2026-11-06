# Brief: write the model for step 3, then build it

You are in a repository: a small calculator language, `lang`, with a
compiler in TypeScript (`compiler/src/`, run by Node as it is) that
emits C, a runtime in C (`runtime/rt.c`, `runtime/rt.h`), and golden
tests (`t/NNN-name.lang` with `t/NNN-name.expected`). Steps 0 to 2 are
built: integers of 63 bits, the operators `+ - * / %`, booleans `#true`
and `#false`, the comparisons `< <= > >= == !=`, and `(if test then
else)`. Step 3 adds bit operations. Its decisions are made. **No tests
and no model exist yet: writing them is the first and larger part of
this job.** This brief is everything you need; it stands in for the
repository's longer documents.

## What a model is, and the one rule about tests

A golden test's expected output is **never taken from the compiler**:
running the compiler and saving what it prints would freeze a bug as
the specification. Expected output comes from a *model*: a small
Python program in `t/models/` that computes what the output must be
from the language's definition, with Python's own unbounded integers,
and writes both the test program and its expected output.
`t/models/arith.py` and `t/models/compare.py` are the shape to copy:
read one before you write yours. The rules a model follows:

- It computes the answer from the decisions below, not from `rt.c` or
  `codegen.ts`. Do not read the runtime's code for the bit operations
  to decide what the model should say; the model is the second opinion,
  and it's worth nothing if it copies the first.
- Its docstring says which tests it writes and lists **every command
  that regenerates a file, one a line**, in exactly this form, with no
  "and so on":

      python3 t/models/bits.py --program 030 > t/030-bit-logic.lang
      python3 t/models/bits.py 030 > t/030-bit-logic.expected

  `make models` runs those lines to write the files, and `make checks`
  (part of `make test`) reruns them and fails if any file differs. Never
  write or patch a `.lang` or `.expected` by hand.
- Each test program's first line is a comment naming the model, for
  example `; From t/models/bits.py.`
- A fault ends the program, so a test that faults is a program of its
  own: its expected output is two lines, `fault: MESSAGE` then `exit: 1`.
- Many values can go in one test by folding them into one expression.
  Reduce each term modulo a prime before adding, so the fold never
  overflows, and fold as a balanced tree, not a chain: clang refuses an
  expression nested more than 256 brackets deep.

## The decisions for step 3 (build to them; do not change them)

- **D15.** Bit operations on two integers: `bit/and`, `bit/or`,
  `bit/xor`, `bit/shl` and `bit/shr`. Each takes exactly two integers
  and gives one; a boolean faults `not an integer`. The integers are the
  mathematical ones in two's complement, so `bit/and`, `bit/or` and
  `bit/xor` are on the sign-extended value, as every width agrees:
  `(bit/and -1 7)` is 7, `(bit/or -8 1)` is -7, `(bit/xor -1 0)` is -1.
  A result of these three is always in range. There is no `bit/not`.
- **D16.** `(bit/shl a n)` is `a` times 2^n, faulting `overflow` when
  that doesn't fit 63 bits. `(bit/shr a n)` is `a` divided by 2^n
  rounded toward negative infinity, so the sign is kept and
  `(bit/shr -7 1)` is -4, where `(/ -7 2)` is -3. The count `n` is from
  0 to 62; any other count faults `bad shift`, whatever `a` is.
- **D17.** The faults' names: `not an integer`, `overflow` and `bad
  shift`. The first two exist already; the third is new.

The integer range is -4611686018427387904 to 4611686018427387903. A
boolean is a tagged word the runtime already checks with `check_int`.

## Rules for the build

- Build only what the decisions say. No `bit/not`, no masked shift
  count, nothing unsigned. If something seems to need more, report it.
- Keep the compiler's shape (pure functions over the forms) and the
  runtime's style. Two C lessons the runtime already follows: never pass
  a variable and a call that sets it in one argument list (C doesn't
  order arguments); and a left shift of a negative value is undefined C,
  so multiply instead, and don't use `>>` on a negative value either,
  since that is implementation-defined; compute the floor another way.
- `make test` is the unit tests, the golden tests and the checks; then
  `make golden-clang` and `make sanitize`. Done means all three pass,
  the model's files are exactly what it writes now, and no existing test
  or model changed.
- If you are stuck on the same failing test after two attempts, stop
  and report rather than trying a third thing.

## Order of work

1. `make test` once, for the baseline: 13 golden tests, all green.
2. Read `t/models/arith.py`, `compiler/src/codegen.ts` and
   `runtime/rt.h`.
3. Write `t/models/bits.py` and run `make models`. Read every file it
   wrote. Then `make test`: the new golden tests must fail (the operators
   are unknown), and `make checks` must still say `0 failed`. Commit this
   state, red, with a subject like `Step 3 written: the bit operations'
   model and tests, red (D15 to D17)`.
4. The runtime, then the compiler (five entries in the operator table).
   Unit tests only if there's a new compile error, which there needn't be.
5. `make test`, `make golden-clang`, `make sanitize`; fix until green.
6. `git add -A` and commit, subject like `Step 3: bit operations (D15 to
   D17)`. Do not push.
7. Call `done` with your report.

## Report

Say, in this order: how the model computes each operation, and from
what; which tests it writes and what each checks; what you changed in
the compiler and runtime; the last lines of the three checks; every
point where you were unsure or the brief was silent, and what you
chose; and whether any file that existed before changed under `t/`.
