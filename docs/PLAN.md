# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** step 0 is done, and so are the mechanical checks. Next: step 1, proposed below
(D8 to D13, defaults until the person agrees), its referee written.

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

### 1. Arithmetic (proposed)

- The form: an operation, `(op a b)`, `op` one of `+ - * / %` and each
  operand an integer literal or an operation (D8). A program is one
  form, a literal or an operation, and its value is printed as before.
  The reader doesn't change.
- The codegen (`compiler/src/codegen.ts`): the whole program checked
  first, then a list compiled to the runtime's operation for its
  operator, with the operands sequenced left to right in the C it
  emits (D11), never as two operations in one call's arguments. A
  malformed expression is a compile error at the form at fault, one of
  D13's six messages, the first in D13's order. Nothing is computed at
  compile time (D12).
- The runtime (`runtime/rt.h`, `runtime/rt.c`): five checked operations
  on 63-bit integers, faulting through `rt_fault` with `integer
  overflow` (D9) or `division by zero` (D10). The check is at 63 bits,
  not 64, and catches a product that int64 wraps back into range
  (D9). Before it's called done: `make golden-clang` and `make
  sanitize` as well as `make test` (CLAUDE.md, code style).
- Unit tests in `compiler/tests/codegen.test.ts`: each of D13's six
  messages with its line and column; a literal out of range inside an
  operation; the order (`(+ 99999999999999999999)` is the arity
  error; an error in the second operand is reported though the first
  would fault when run).
- Golden tests 010 to 026, each a program of one line under a comment
  that says what it checks and cites its decision:
  - 010-add `(+ 1 2)` and 011-arith `(- (* 6 7) (+ (/ 9 2) (% 9 2)))`:
    expected output by hand, worked from the program.
  - 012-div-signs `(+ (* 1000 (/ -7 2)) (+ (* 100 (/ 7 -2)) (+ (* 10
    (/ -7 -2)) (/ 7 2))))` and 013-rem-signs, the same with `%`:
    truncation in all four sign cases, weighted so a floored one shows
    (D10).
  - 014-max-result `(+ 4611686018427387902 1)`, 015-min-result
    `(* -2305843009213693952 2)`, 016-rem-min
    `(% -4611686018427387904 -1)`: results at the range's ends, and
    the remainder that doesn't fault (D9, D10).
  - 017-add-overflow `(+ 4611686018427387903 1)`, 018-sub-overflow
    `(- -4611686018427387904 1)`, 019-mul-overflow
    `(* 2147483648 2147483648)` (2^62, which int64 holds),
    020-mul-wrap `(* 4294967296 4294967296)` (2^64, which int64 wraps
    to 0), 021-div-overflow `(/ -4611686018427387904 -1)` (D9).
  - 022-div-zero `(/ 1 0)`, 023-rem-zero `(% 1 0)` (D10).
  - 024-order-left `(+ (/ 1 0) (+ 4611686018427387903 1))` and
    025-order-right, its operands swapped: the first fault in left to
    right order is the one reported, so an order that's right under
    one C compiler by chance fails one of the two (D11).
  - 026-intermediate `(* (+ 4611686018427387903 1) 0)`: an
    intermediate result faults though the whole would be 0 (D9).

  012 to 026, programs and expected outputs both, come from a new
  model, `t/models/arith.py`, written from D8 to D12: each result in
  Python's unbounded integers, truncation worked on the magnitudes
  (not Python's `//` and `%`, which floor), the range checked after
  every operation, operands left to right. It writes the `.lang` too,
  with a comment naming it, since `t/checks.py` fails a test that
  names a model which doesn't list it; its docstring lists the thirty
  commands. 010 and 011 don't name it.
- Documents: `LANGUAGE.md` gains the operations, in prose with
  examples, and the two faults, and loses "nothing faults yet";
  `DESIGN.md`'s "The language" says what D8 to D12 say, in a
  paragraph; this step is marked (done) with the progress line;
  `CLAUDE.md`'s Status gains step 1, with the tests and the `Dn`s.
- Leaves out: variadic operators and a unary minus (D8); comparisons
  and any other operator; constant folding, and a position in a
  fault's message (D12); integers past 63 bits (D9); a program nested
  deeper than a C compiler's bracket limit (clang stops at 256,
  CLAUDE.md), which isn't tested; more than one top-level form;
  any new runtime knob or environment variable.

**Referee:** write `t/referee/calc.py` to cover this, done with the
proposal and agreeing with tests 000 and 001 under `make checks`. It's
wanted on all three counts: the model is delegated to the builder; the
semantics have traps a model shaped like the implementation would
copy (overflow at 64 bits rather than 63, Python's floor for C's
truncation, the C compiler's argument order for left to right); and a
19-digit boundary isn't checkable by eye. Checked, besides, against
C99's own `/` and `%` and an exact `__int128` range check on 51,005
operand pairs, the boundaries among them.

**Size:** medium, **Effort:** high. The design is D8 to D13, every
test and the source of its expected output is named, no existing
output moves, nothing (open) is in reach, and the model, which
`MODELS.md` keeps for large, is checked under `make checks` by the
referee, which is what the referee is for. What fails `MODELS.md`'s
five is precedent: this is the first step to compile an expression,
so there's no pattern to read, and that risk is carried by the named
tests and the referee. Effort high, because the model is where the
builder's own checking is the check. Escalate, rather than press on,
when the referee and the model disagree and the decisions don't say
which is wrong, or say the referee is; when a test needs a decision
D8 to D13 don't make; or when the diff reaches beyond the files above.

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
