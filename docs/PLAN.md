# Plan

Ghuloum's incremental approach: the interpreter works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** this is the `interpreter` branch (D28, D29): the
calculator of main after step 5, to be built again as an interpreter.
Steps 0 to 5 are built: the calculator of main, all 46 golden tests
passing on Node 22 and 24. Steps 6 onward are still placeholders, to be
proposed first.

Read [`DESIGN.md`](DESIGN.md) first. Where a step meets an **(open)**
item, propose options to the user before building (see `CLAUDE.md`).

## Proposed layout

`bin/lang.ts`, the driver; `interp/src/`, a file per pass (reader,
checker, evaluator, errors); `interp/tests/`, their unit tests; `t/`,
the golden tests, models and referee, as on main.

## Steps

Each step says what it adds, what it touches, what tests it adds, and
what it leaves out on purpose. A step marked **(done)** keeps its text,
with a note where what landed differs.

Steps 0 to 5 build the language main has, in main's order, and every
one of their golden tests already exists: written on main, from the
models and by hand, and agreeing with the referee. So a step here adds
no golden test and changes none: it makes its own pass, and the
earlier steps' still pass. A step's tests are the ones numbered in its
decade, so `./t/run.sh t/0[0-2]*.lang` runs steps 0 to 2's, and step 5
ends with all 46 and `make test` green. main's `PLAN.md` has the steps
as the compiler built them, and what each found.

A step is **done** when its tests and every earlier step's pass under
`./t/run.sh` and `LANG_NODE=/opt/node24/bin/node ./t/run.sh` (the
second Node, `make golden-node` once every test passes), `make unit`,
`make checks` and `make check` pass (`make check` if `npm install`
works where it's built), no file under `t/` is changed, the documents
it names are moved, and its commits name the step (`make commits`).

Each step carries a **Referee** line, set when the step is proposed:
`extend t/referee/NAME.py to cover this`, or `none`, with the reason
(`docs/PROCESS.md`, "The referee"), and a **Size** line, the capability
the step needs of the agent that builds it, by `docs/MODELS.md`'s tiers: *large* where
there's a decision to propose, a runtime mechanism to design, or a
model to write; *medium* where the design is agreed and the step
describes its tests; *small* where the step is a pattern to repeat.
A session's first move is to compare its own model with the step's size.

### 0. One literal, evaluated and printed (done)

Size: medium. The decisions are made; the step's design work is the
host's answers, and they come first. Referee: none new;
`t/referee/calc.py` covers every test already.

- First, `DESIGN.md`'s "What the host gives": every item answered,
  each as inherits (with the test that shows it), overrides (and how)
  or asks; committed before any code. Later steps may correct an
  answer, saying so.
- `bin/lang.ts FILE`: reads the file, checks it, evaluates it, prints
  the value and a newline, exits 0. A fault ends it as D6 says; an
  error before running is `FILE:LINE:COL: message` on stderr, exit 2
  (D28), as is a usage error; a fault in the interpreter itself is
  `lang: internal error: ...` with Node's stack.
- The reader (`interp/src/reader.ts`): integers, symbols and lists, each
  form with its line and column; `;` comments. Unit tests in
  `interp/tests/`.
- Integers are 63 bits (D4): a literal past the range is an error
  before running, a unit test.
- Tests 000 and 001.
- Documents: `DESIGN.md`'s answers, Values and memory and The
  interpreter; this heading and the progress line; `CLAUDE.md`'s
  Status.

### 1. Arithmetic (done)

Size: medium. Referee: none new.

- `(+ a b)`, `-`, `*`, `/`, `%`, nested, on 63-bit integers (D3, D4,
  D5); overflow and division by zero fault (D6).
- Errors before running (D7, D28), each a unit test: an operator with
  other than two operands, an unknown name, a list whose head isn't an
  operator.
- Tests 010 to 015.
- Documents: this heading, the progress line, the Status; `DESIGN.md`
  where an answer moved.

### 2. Booleans, comparisons and `if` (done)

Size: medium. Referee: none new.

- `#true` and `#false` (D11), printed as written; the arithmetic faults
  `not an integer` on anything else (D11). D14's tags are main's: the
  representation is the interpreter's (D28).
- The six comparisons (D12): the orderings on integers, `==` and `!=`
  on any two values.
- `(if test then else)` (D13): the test a boolean at run time or `not a
  boolean`, only the taken branch evaluated; an `if` with other than
  three parts is an error before running, in a branch that's never
  taken too (D28), a unit test.
- Tests 020 to 024.
- Leave out: `and`, `or`, `not`, `cond`, truthiness.

### 3. Bit operations (done)

Size: medium. Referee: none new.

- `bit/and`, `bit/or`, `bit/xor`, `bit/shl` and `bit/shr` (D15, D16),
  their faults named as D17 says.
- Where one application could fault two ways (a boolean and a bad
  count), which fault reports is open (`CLAUDE.md`'s Status). No test
  has one; don't add one, and say what the interpreter does.
- Tests 030 to 036.
- Leave out: `bit/not`, a count masked rather than checked, anything
  unsigned.

### 4. Exponentiation (done)

Size: medium. Referee: none new.

- `(** a b)` (D18, D19): a negative exponent faults `bad exponent`,
  `a ** 0` is 1. An exponent as large as the range must be quick: test
  056, at step 5, raises 1 to 4611686018427387903.
- Tests 040 to 045.

### 5. A budget: `(within n expr)` (done)

Size: medium. Referee: none new; it holds D21 to D25 as main's step 5
proposed them.

- `within` (D20 to D24): its parts checked before running (D24, D28);
  the charge, nesting and the budget's own evaluation as the decisions
  say. D27's two counts are main's runtime's: any mechanism that keeps
  D21 to D24 will do (D28).
- Left to right (D25), the first fault the one reported.
- Tests 050 to 069; then `make test` and `make golden-node` pass whole.
- Documents: `LANGUAGE.md` is already right; this heading, the
  progress line, the Status.
- Leave out: a way to catch `budget spent` or ask what's left, budgets
  of anything but operator applications.

### 6. [Local bindings.] Referee: [decide]. Size: medium.

### 7. [Heap values.]

### 8. [Procedures, calls and tail calls.]

### 9. [Closures.]

### 10. [Whatever the language is really about: its core rule.]

### 11. [The prelude, in the language.]

### 12. [Examples: ports of existing programs, each a golden test.]

### 13. [Tooling: the runtime cached, tests in parallel, the guide's
code checked.]

## Proposals

[Agreed proposals become steps above. Proposals not yet agreed go here,
each with its options and the agent's recommendation, marked
**proposed** until the person picks, and the pick recorded as a `Dn`.]

## Example-port table

| Example | Needs | Status |
|---|---|---|
| [name] | [the features it needs, by step] | [waits on step n / ported / dropped (Dn)] |
