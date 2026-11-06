# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** steps 0 to 4 are done; the mechanical checks came with 1. Step 2 was the experiment of `docs/MODELS.md`: written with its tests red, then built by a small model (Haiku 5.5) on a step marked medium. Step 3 was the second experiment: written with its decisions and no model or tests, so the builder wrote the model (`t/models/bits.py`) and its tests, red, before the code. Step 4 is the third: the same, on one line of decision.

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

Each step carries a **Size** line, the capability the step needs of
the agent that builds it, by `docs/MODELS.md`'s tiers: *large* where
there's a decision to propose, a runtime mechanism to design, or a
model to write; *medium* where the design is agreed and the step
describes its tests; *small* where the step is a pattern to repeat.
A session's first move is to compare its own model with the step's size.

### 1. Arithmetic (done)

Size: large, for the model and the decisions; medium once they're
written.

- `(+ a b)`, `-`, `*`, `/`, `%`, nested, on 63-bit integers (D3, D4,
  D5); the runtime's checked operations in `runtime/rt.c`, the
  operator table in `codegen.ts`.
- Faults: overflow and division by zero end the program with a message
  and exit 1 (D6).
- `t/models/arith.py`: the operators over the edge values, Python's
  integers with the range and the division rule applied after. It
  writes tests 010 (every pair that gives a value, folded into one
  expression) and 011 to 015 (each a fault). The first version of the
  model folded a term before reducing it and overflowed: the compiler
  found the model's bug, which is the other half of why a model is
  worth having.
- The mechanical checks, `t/checks.py` (D8, D10): `models`, `tests`,
  `commits`, and the hook.
- Compile errors (arity, an unknown name, not an operator) as unit
  tests (D7).

### 2. Booleans, comparisons and `if` (done)

Size: medium. The decisions were made (D11 to D14), the model is
`t/models/compare.py`, and the tests 020 to 024 were red until the step. It
is done: `make test`, `make sanitize` and `make golden-clang` pass with no
test or model changed. One thing landed differently from the text: the
reader still makes `#true` and `#false` symbols, and `codegen.ts` gives them
their meaning.

The experiment's record is in `docs/MODELS.md`. Two models built this
step cold from the same commit: Sonnet's build is the branch
`step2-sonnet`, Haiku's `step2-haiku`, which is what main took; Haiku
again at low and at high effort are `step2-haiku-low` and
`step2-haiku-high`. What the
step's text lacked, found by both: it named only code and tests, so
neither was told to move `LANGUAGE.md`, the plan's heading or the
Status; Sonnet left them, Haiku moved them. A step says which documents
it moves, and "done when" includes them.

- `#true` and `#false` (D11): read as themselves (today the reader
  makes them symbols; either the reader or `codegen.ts` may give them
  their meaning, but `(+ #true 1)` must fault at run time, not fail to
  compile, since D11 says what it does). An immediate with its own tag
  (D14), in `runtime/rt.h`; `rt_print` prints them as written.
- The six comparisons (D12), as runtime functions beside the arithmetic
  in `rt.c`, through the operator table in `codegen.ts`. The orderings
  check both arguments are integers; `==` and `!=` compare any two
  values.
- The arithmetic checks its arguments are integers (D14), faulting
  `not an integer`; before this step nothing but an integer could reach
  it.
- `(if test then else)` (D13): a special form in `codegen.ts`, not an
  operator, since only the taken branch runs. The test is checked to be
  a boolean at run time, faulting `not a boolean`. C's `?:` does this;
  a form with other than three parts is a compile error, as a unit test.
- Tests: 020 (every comparison over the edge values, counted with `if`,
  from the model), 021 to 024 (by hand: a boolean printed; only the
  taken branch runs; `not an integer`; `not a boolean`). Unit tests for
  the compile errors (`if` with two parts; `(if)`).
- Leave out: `and`, `or`, `not`, `cond`, truthiness, anything else.
  Report, don't add, if something seems to need them.

### 3. Bit operations (done)

Size: large, for the model; the build is medium once the model and its
tests exist. The decisions are made (D15 to D17). No model and no tests
existed: this step's first work was `t/models/bits.py`, and the tests it
writes, 030 and up, before any code changed. The step is done when
`make test`, `make golden-clang` and `make sanitize` pass, the model
lists every file it writes (`make checks` holds it to that), and
`LANGUAGE.md`, this heading and `CLAUDE.md`'s Status are moved.

What landed differently from the text: the model folds its terms as a
balanced tree, not a chain, since clang stops at 256 levels of brackets
and the chain's 500 nested terms didn't compile under it. The shape of
the program is the only thing the model chooses; every value is computed
from the definition. The
step didn't name the compile-error unit tests for the bit operations'
arity and `bit/not`; they were added to `compiler/tests/codegen.test.ts`.

- `t/models/bits.py` first: the five operations over values that find
  the edges, from the definition in D15 and D16 and nothing else. The
  model's job is to compute what the decisions say, not what the
  runtime does; `t/models/README.md` says how, and `arith.py` and
  `compare.py` are the shape. Expected outputs for every value and
  every fault the decisions name, 030 and up, each fault in a test of
  its own since a fault ends the program (as 011 to 015).
- Then the operations, as runtime functions beside the arithmetic in
  `rt.c`, through the operator table in `codegen.ts`. `bit/shl` checks
  its result's range (D4, D16); both shifts check the count (D16).
  Note the clang lesson in CLAUDE.md, and that a left shift of a
  negative value is undefined C (`rt.h`'s comment).
- A fault's name as D17 says.
- Unit tests for what a golden test can't see (D7), if anything new.
- Leave out: `bit/not`, a count masked rather than checked, unsigned
  anything. Report, don't add.


Both trials' branches are kept: `step3-sonnet` and `step3-haiku`,
which is what main took. The record is in `docs/MODELS.md`. Open, from
Haiku's run: the compiler emits one nested C expression per program, so
a user's program about 250 operators deep fails under clang's bracket
limit. A decision when a program that deep is wanted: statements with
temporaries, or `-fbracket-depth`, or a documented limit.

### 4. Exponentiation (done)

Size: large, for the model. D18 (and D19, which the build had to add:
D18 gave only the operator). The model first, `t/models/pow.py`
and its tests, 040 and up, then the code; done when `make test`,
`make golden-clang` and `make sanitize` pass, the model lists what it
writes, and `LANGUAGE.md`, this heading and `CLAUDE.md`'s Status are
moved.

What landed: `t/models/pow.py` and tests 040 to 045, committed red, then
`rt_pow` (squaring, so an exponent of 2^62 - 1 on a base of 1 is quick)
and the table entry. The model's one shortcut, overflow without computing
when |a| >= 2 and b >= 63, is asserted against the real power up to 200.

### 5. [Local bindings.] Size: medium.

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
