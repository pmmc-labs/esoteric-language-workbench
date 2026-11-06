# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** step 0 is done, and so are the mechanical checks. Step 1 (arithmetic) is proposed on D20 to D28, which the person accepted as proposed; next: its build.

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

### 1. Arithmetic (proposed; not agreed)

Adds `+`, `-`, `*` and `/` as binary prefix forms, `(op a b)`, with their
faults. Every choice in it (D20 to D28) was proposed as a default and
accepted by the person as proposed, so the build can go ahead.

- **The forms** (D20, D21, D22): exactly two operands, and a nested form
  is an operand. A malformed form and a bare symbol are compile errors,
  with the messages in D21, found over the whole program before anything
  runs. A leading `+` is not part of a literal, so `+5` is a symbol.
- **The faults** (D23 to D25): a result outside the 63-bit range is
  `fault: integer overflow`. `/` truncates toward zero, so `(/ -7 2)` is
  -3. A zero divisor is `fault: division by zero`. `-2^62 / -1` is an
  overflow, not a division fault.
- **The runtime** (D26, D27): `rt_add`, `rt_sub`, `rt_mul` and `rt_div`
  in `runtime/rt.c`, declared in `rt.h`. Each decodes its operands,
  checks the operation with `__builtin_*_overflow` before the range check
  (so `(* 4294967296 4294967296)` faults, though 2^64 wraps to 0), and
  encodes with `rt_int`. Faults go through `rt_fault`.
- **The compiler** (D27, D28): a form is flattened into C statements, its
  operands first, left to right, each into a named temporary, and then the
  operator's call. Nothing is evaluated at compile time.

**Touches:** `compiler/src/codegen.ts` (lists and the four operators, and
the D21 messages); `runtime/rt.h` and `runtime/rt.c`; `compiler/tests/`,
a new `arith.test.ts` for the compile errors, their messages and their
positions; `docs/LANGUAGE.md` (the operators, the faults, and the rules
for forms, in prose); `docs/DECISIONS.md`, with the picks; this progress
line; and `CLAUDE.md`'s Status, by the builder as the step lands.
`reader.ts` doesn't change: it already reads what this step needs.

**Tests added:** `t/050` to `t/065`, sixteen golden tests, listed in
`t/models/arith.py`. Their expected output comes from that model, which
the builder writes from D20 to D28 and not from `codegen.ts` or `rt.c`.
Its docstring lists a `--program` line and an expected-output line for
each test, and `make models` writes the files; nothing is patched. The
numbers 010 to 045 were used by an earlier build of these steps, in this
branch's history, so they aren't reused. Each `.lang` names the model in
a comment, so `make checks` ties it to the model. The unit tests cover
what a golden test can't: the D21 compile errors, with messages and
positions.

**Documents moved:** `LANGUAGE.md`, `DECISIONS.md` and `PLAN.md`, by the
builder; `CLAUDE.md`'s Status, by the builder when it lands. `DESIGN.md`
doesn't change in this step, and its open questions stay the person's.

**Leaves out, on purpose:** the remainder (`%`), which would need its own
rule for negative operands; n-ary and unary operators (D20); bignums and
wrapping (D23); constant folding (D28); comparisons, booleans and `if`;
bindings; any flag, environment variable or knob.

**Referee:** wanted. `t/referee/calc.py` is written with this proposal,
from D20 to D28, and checked against `t/000` and `t/001`. It's wanted
because the builder writes the model, and the expected outputs at the
edges of the 63-bit range, the order of the faults and the truncation of
division can't be checked by eye. Each is where a model that mirrors the
implementation would copy its mistake. The builder doesn't read
`t/referee/`.

**Size:** large. The step has decisions to propose (D20 to D28 are
defaults for the person to pick), a runtime mechanism to design (the
checked operations and the temporaries), and a model to write, and
`docs/MODELS.md` puts each of those at large. The one way to take it at
medium is to split it: a step that writes the model and makes the referee
agree with it, done large, then the build, done medium against that
model.

**Brief:** `docs/BRIEF.md`, for the builder: what to read, the order, what
not to touch, and how to report.


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
