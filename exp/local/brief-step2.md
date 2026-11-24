# Brief: build step 2 of the plan

You are in a repository: a small calculator language, `lang`, with a
compiler in TypeScript (`compiler/src/`, run by Node as it is) that
emits C, a runtime in C (`runtime/rt.c`, `runtime/rt.h`), and golden
tests (`t/NNN-name.lang` with `t/NNN-name.expected`). Steps 0 and 1 are
built: integers of 63 bits and the operators `+ - * / %`. Step 2 is
written and its tests exist and fail. Your job is to build step 2 so
that they pass. This brief is everything you need; it stands in for the
repository's longer documents, which you need not read.

## Rules

- **Never edit a test or its expected output.** Tests 020 to 024 and
  `t/models/compare.py` are the specification. If the compiler and an
  expected file disagree, the compiler is wrong. If you believe a test
  is wrong, stop and say so in your report instead of changing it.
- **Build only what the step says.** No `and`, `or`, `not`, `cond`, no
  truthiness, no flag or environment variable. If something seems to
  need more, report it, don't add it.
- **Keep the compiler's shape:** pure functions over the forms, no
  classes, no module-level mutable state. Keep the runtime's style, and
  its two lessons: C doesn't order a call's arguments, so never pass a
  variable and a call that sets it in one argument list; and a left
  shift of a negative value is undefined C, so the integer tag
  multiplies rather than shifts (`rt_int` in `rt.h` already does).
- **Run the checks, and report what they print.** `make test` is the
  unit tests, the golden tests and the mechanical checks. Then `make
  golden-clang` (the golden tests under clang) and `make sanitize` (under
  clang's UBSan and ASan). The step is done when all three pass with no
  file under `t/` changed.
- If you are stuck on the same failing test after two attempts, stop
  and report rather than trying a third thing.

## The language today

A program is one expression. An expression is an integer literal or an
operator applied to two expressions, `(+ 1 2)`. The runtime prints the
program's value and a newline and exits 0. A fault ends the program:
`fault: MESSAGE` on stderr and exit 1, with nothing on stdout. Values
are tagged words (`rt_value`): an integer is shifted left one bit, low
bit 0. `codegen.ts` has an operator table from names to runtime
functions, and compiles each form to a C expression; `rt.c` has
`rt_add` and the rest, each checking its result. Read `compiler/src/
codegen.ts`, `runtime/rt.h` and `runtime/rt.c` first; they are short.

## Step 2: booleans, comparisons and `if`

The decisions, which you build to and do not change:

- **D11.** Booleans, `#true` and `#false`, a type of their own. They
  print as written. Neither is an integer: arithmetic on one faults
  `not an integer`.
- **D12.** Comparisons `<`, `<=`, `>`, `>=` on two integers, and `==`
  and `!=` on any two values, each giving a boolean. An ordering given
  a boolean faults `not an integer`. `==` on two values of different
  types is `#false`, not a fault.
- **D13.** `(if test then else)`: three parts; the test must be a
  boolean at run time or the program faults `not a boolean`; only the
  taken branch is evaluated, so `(if #true 1 (/ 1 0))` is 1. No
  truthiness. A two-part or four-part `if` is a compile error.
- **D14.** A boolean is an immediate with its own tag: the low two bits
  `11`, the value in bit 2. An integer's low bit stays 0, so integers
  are untouched. The runtime checks a value's tag before arithmetic and
  comparison, now that the compiler can't know what an `if` gives.

What to build:

- `#true` and `#false`: the reader makes them symbols today; either the
  reader or `codegen.ts` may give them their meaning, but `(+ #true 1)`
  must fault at run time, not fail to compile. Encode them in `rt.h` as
  D14 says; `rt_print` prints them as written.
- The six comparisons as runtime functions beside the arithmetic in
  `rt.c`, through the operator table in `codegen.ts`. The orderings
  check both arguments are integers; `==` and `!=` compare any two
  values.
- The arithmetic checks its arguments are integers, faulting `not an
  integer`.
- `(if test then else)` as a special form in `codegen.ts`, not an
  operator, since only the taken branch runs. The test is checked at run
  time, faulting `not a boolean`; C's `?:` does the rest. A form with
  other than three parts is a compile error: add a unit test for it in
  `compiler/tests/codegen.test.ts`, in the style of the tests there,
  since the golden runner treats a failed compile as a failure.
- The tests: 020 (every comparison over edge values, counted with `if`,
  written by `t/models/compare.py`) and 021 to 024 (a boolean printed;
  only the taken branch runs; `not an integer`; `not a boolean`). They
  fail now because `#true`, the comparisons and `if` are unknown.

## Order of work

1. `make test` once, to see the baseline: 8 golden tests, 5 failing at
   compile.
2. Read the three source files named above and the failing tests.
3. The runtime, then the compiler, then the unit test.
4. `make test`, `make golden-clang`, `make sanitize`; fix until green.
5. `git add -A` and `git commit` with a subject that names the step and
   the decisions, for example `Step 2: booleans, comparisons and if
   (D11 to D14)`. Do not push.
6. Call `done` with your report.

## Report

Say, in this order: what you changed, file by file; the last lines
`make test`, `make golden-clang` and `make sanitize` printed; every
point where you were unsure or the brief was silent, and what you
chose; and whether you changed any file under `t/` (you should not
have).
