# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** steps 0 and 1 are done, and so are the mechanical checks. Step 1 (D8 to D15, all defaults, none confirmed) landed with golden tests 000 to 030 and `t/referee/calc.py` agreeing with all 31. Step 2 is to be proposed.

Read [`DESIGN.md`](DESIGN.md) first. Where a step meets an **(open)**
item, propose options to the user before building (see `CLAUDE.md`).

## Proposed layout

[The tree as planned. `CLAUDE.md` has the layout as built; when they
differ, this stays as a record of the plan.]

## Steps

Each step says what it adds, what it touches, what tests it adds, and
what it leaves out on purpose. A step marked **(done)** keeps its text,
with a note where what landed differs.

### 0. Scaffold (done)

- The build: `bin/langc.ts` reads a file, compiles it to C next to the
  output, and links it with `runtime/rt.c` by `cc` (`LANG_CC` overrides);
  `make test` runs the unit tests then the golden tests. C rather than
  assembly, so step 0 runs on any machine with a C compiler; a native
  target comes when the language needs one, through a target interface.
- The reader (`compiler/src/reader.ts`): integers, symbols and lists,
  each form with its line and column; `;` comments. Unit tests in
  `compiler/tests/`.
- A compiler for one kind of literal (`codegen.ts`): a program that is
  `42` compiles to a binary that prints `42`. Integers are 63 bits,
  shifted left one, tag 0 (`runtime/rt.h`); one past the range is a
  compile error, checked by a unit test since the golden runner calls a
  failed compile a failure.
- `t/run.sh`: compile each golden test, run it with the environment the
  tests assume (none yet; the knobs go there as the runtime gains them),
  compare stdout and stderr together with the `.expected` file, plus
  `exit: N` when the status isn't 0, `JOBS` at a time, with a watchdog.
- Golden tests 000 and 001, their outputs by hand.

Each step carries a **Referee** line, set when the step is proposed:
`extend t/referee/NAME.py to cover this`, or `none`, with the reason
(`docs/PROCESS.md`, "The referee"), and a **Size** line, the capability
the step needs of the agent that builds it, by `docs/MODELS.md`'s tiers: *large* where
there's a decision to propose, a runtime mechanism to design, or a
model to write; *medium* where the design is agreed and the step
describes its tests; *small* where the step is a pattern to repeat.
A session's first move is to compare its own model with the step's size.

### 1. Arithmetic (done)

- The five operators `+ - * / %`, each a call `(op a b)` with two
  operands (D8). A program is still one form, now a literal or a call,
  nested to any depth the tests reach (1000).
- Overflow of the 63-bit range is the fault `integer overflow`, a zero
  divisor `division by zero`; `/` truncates toward zero and `%` takes
  the dividend's sign (D10, D11). Operands are evaluated left to right,
  and nothing is folded: a fault is a run-time event, the first to
  happen is the one printed (D12).
- The runtime (`runtime/rt.c`, `rt.h`): `rt_add`, `rt_sub`, `rt_mul`,
  `rt_div`, `rt_rem` and the range as `RT_INT_MIN`/`RT_INT_MAX`, by the
  one recipe of D13. `rt_fault` is as it is.
- The compiler (`codegen.ts`): straight-line C, a temporary per node in
  evaluation order (D14); the malformed-call errors with their messages
  and positions, all found before any C is written (D15). The reader
  doesn't change; D9 is what it does already, and a unit test pins it.
- Unit tests, in `compiler/tests/`, expected by hand from D9 and D15:
  `reader.test.ts` reads `+5`, `1_0`, `1.5`, `0x10`, `--1` and `-` as
  symbols and `007` and `-0` as the integers 7 and 0;
  `codegen.test.ts` has one test per message of D15 (`()`, `(1 2)`,
  `(foo 1 2)`, `(+ 1)`, `(+ 1 2 3)`, a bare `x`, a bare `+`), each with its
  line and column, one that the outer form's error comes before the inner
  one's, and one that a malformed form after an operand that would
  fault is still a compile error.
- Golden tests 002 to 030. Each program is the one line shown and its
  expected output is worked out by hand from the decisions, not run;
  `fault` tests expect the two lines `fault: MESSAGE` and `exit: 1`.
  Write the `.expected` files from this list, then check them against
  the arithmetic once more before running anything.
  - 002 `(+ 40 2)` is 42; 003 `(- 3 10)` is -7; 004 `(* -6 7)` is -42;
    005 `(- (* 3 (+ 4 5)) (/ 100 (% 17 5)))` is -23.
  - Truncation (D11): 006 `(/ -7 2)` is -3; 007 `(/ 7 -2)` is -3; 008
    `(% -7 2)` is -1; 009 `(% 7 -2)` is 1.
  - The edges of the range, which are fine (D10): 010
    `(+ 4611686018427387902 1)` is 4611686018427387903; 011
    `(- -4611686018427387903 1)` is -4611686018427387904; 012
    `(* 2147483648 2147483647)` is 4611686016279904256 (2^62 - 2^31);
    013 `(* -2147483648 2147483648)` is -4611686018427387904; 014
    `(% -4611686018427387904 -1)` is 0.
  - One past the edges, `fault: integer overflow` (D10): 015
    `(+ 4611686018427387903 1)`; 016 `(+ -4611686018427387904 -1)`; 017
    `(- -4611686018427387904 1)`; 018 `(- 4611686018427387903 -1)`; 019
    `(* 2147483648 2147483648)`; 020
    `(* 4611686018427387903 4611686018427387903)`, whose product passes
    64 bits; 021 `(- 0 -4611686018427387904)`; 022
    `(/ -4611686018427387904 -1)`.
  - `fault: division by zero` (D11): 023 `(/ 1 0)`; 024 `(% 1 0)`.
  - Order (D12): 025
    `(+ (/ 1 0) (* 4611686018427387903 4611686018427387903))` is
    `division by zero`; 026
    `(+ (* 4611686018427387903 4611686018427387903) (/ 1 0))` is
    `integer overflow`; 027 `(* 0 (/ 1 0))` is `division by zero`.
  - From a model, `t/models/arith.py`, which the builder writes (the
    docstring lists the six commands, `--program` for the test and
    none for its output; see `t/models/README.md`): 028 `deep-left`,
    `(+ (+ (+ 0 1) 2) 3)` carried to 1000, so 999 more lists around the
    first: 500500; 029 `deep-right`, `(- 1 (- 2 (- 3 ... (- 999
    1000))))`: -500; 030 `mixed`, a tree of about 300 operations over
    all five operators and all four sign pairs of `/` and `%`, with
    operands from -50 to 50, drawn by a linear congruential generator
    written out in the model (not Python's `random`, whose stream is
    not part of the definition), each operation redrawn if it would
    fault, so that the program has a value, which the model computes by
    D10 and D11 written out (not Python's `//` and `%`: they floor) and
    asserts in range at every node, and that some intermediate passes
    2^40 so multiplications past 32 bits are used. The generated
    programs begin with a comment naming the model.
- Moves: `docs/LANGUAGE.md` (Values keeps its range; Forms gains the
  five operators and the integer rule; Programs gains the two faults,
  with examples), `docs/DESIGN.md` (The language: a few lines, D8 to D12
  marked **(open)** as defaults, and Open questions), this file's
  progress line and the step marked done, and `CLAUDE.md`'s Status. The
  Layout, Commands and Toolchain of `CLAUDE.md` don't change.
- Leaves out: a one-operand `-` (D8), operators with more or fewer
  operands, comparison, bit operations, bindings, conditionals,
  anything but integers, bignums, constant folding, a limit on nesting or
  an error for exceeding Node's stack, a new environment variable or
  knob for `t/run.sh`, any change to the reader, a native target.

**What landed differs in small ways.** Each golden test's `.lang` has a
comment line above the program (the plan said the one line). `codegen.ts`
has the D15 checks as one pass (`check`) and the C as another (`emit`),
which returns the statements, the temporary holding the value and the
next free number. `reader.test.ts` has a third test beyond the plan's
list, for D9's whitespace; `codegen.test.ts` has more than one test per
ordering rule (outer before inner, left before right) and one for D14's
shape. `t/models/arith.py` draws `mixed` with half its left operands
being the newest call, so that values compound (drawing both operands
uniformly from the pool, the largest value in the first dozen seeds tried
was about 2^36), and its seed is the first of those tried that satisfies the
assertions at the end of `mixed`, which say what the test must exercise
(300 operations, every operator, every sign pair of `/` and `%`, a
product past 2^40, a program value past 2^32).

**Referee:** `t/referee/calc.py`, written with this proposal, from D1 to
D4 and D8 to D15; `make checks` runs it over every golden test and it
agrees with 000 and 001. Wanted because the model for 028 to 030 is
written by a builder smaller than the one that proposed it, and the
arithmetic has traps a model copies from its language: floor division and
unbounded integers in Python, `int()` taking `+5` and `1_0`, a range
check made once at the end and not at each node. The builder runs `make
checks` and reads its verdicts but not `t/referee/calc.py`; a model that
disagrees with it is judged by D8 to D15, and where they don't say, the
builder stops and reports. A later step that adds a form extends the
referee in the same way, before its builder starts.

**Size:** medium. The design is decided (D8 to D15), the tests are named
with their expected output, and the referee checks the one thing a medium
model can't be trusted to judge for itself, the model in
`t/models/arith.py`. Read that model as if it were the implementation
(`docs/MODELS.md`); raise effort for it. Escalate on the signals in
`docs/MODELS.md`: in particular, a model and the referee disagreeing that
D8 to D15 don't settle, or a test wanting a special case in the compiler.
`docs/BRIEF.md` is what the builder is given.

### 2. [Primitives on them.]

### 3. [Conditionals.]

### 4. [Local bindings.]

### 5. [Heap values.]

### 6. [Procedures, calls and tail calls.]

### 7. [Closures.]

### 8. [Whatever the language is really about: its core rule.]

### 9. [The prelude, in the language.]

### 10. [Examples: ports of existing programs, each a golden test.]

### 11. [Tooling: the runtime cached, tests in parallel, the guide's
code checked.]

## Proposals

[Agreed proposals become steps above. Proposals not yet agreed go here,
each with its options and the agent's recommendation, marked
**proposed** until the person picks, and the pick recorded as a `Dn`.]

## Example-port table

| Example | Needs | Status |
|---|---|---|
| [name] | [the features it needs, by step] | [waits on step n / ported / dropped (Dn)] |
