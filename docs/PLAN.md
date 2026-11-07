# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** [which steps are done, in a sentence, updated as they land;
what's next.]

Read [`DESIGN.md`](DESIGN.md) first. Where a step meets an **(open)**
item, propose options to the user before building (see `CLAUDE.md`).

## Proposed layout

[The tree as planned. `CLAUDE.md` has the layout as built; when they
differ, this stays as a record of the plan.]

## Steps

Each step says what it adds, what it touches, what tests it adds, and
what it leaves out on purpose. A step marked **(done)** keeps its text,
with a note where what landed differs.

### 0. Scaffold

- The build: the driver, the runtime compiled and linked, `make test`.
- The reader, with source positions, and its unit tests.
- A compiler for one kind of literal: a program that is `42` compiles
  to a binary that prints `42`.
- `t/run.sh`: compile a golden test, run it with the environment the
  tests assume, compare stdout and stderr together with the `.expected`
  file, plus `exit: N` when the status isn't 0.
- Golden test 000.

### 1. [Immediates: the rest of the literals.]

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
