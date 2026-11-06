# Brief: propose the next step of the plan

You are in a repository: a small calculator language, `lang`, with a
compiler in TypeScript (`compiler/src/`, run by Node as it is) that
emits C, a runtime in C (`runtime/rt.c`, `runtime/rt.h`), golden tests
(`t/NNN-name.lang` with `t/NNN-name.expected`), and documents under
`docs/`. Only step 0 is built: a program is one integer literal, and
the compiled binary prints it. The language is to be a calculator:
integer expressions, compiled to a native binary that prints the value
(decision D1 in `docs/DECISIONS.md`). Nothing beyond that is decided.

**Your job is to propose step 1, and not to build it.** A proposal is
what a builder, working alone later, is handed cold. It is complete
when it has four parts, below. Do not change the compiler, the runtime,
`docs/LANGUAGE.md`, the Status in `CLAUDE.md`, or any test.

## How this repository works, in brief

- Every change to the language's meaning is **decided before it's
  built**, in `docs/DECISIONS.md`: numbered entries, `**D8. Title.**`,
  each saying what was decided, why, and under `Rejected:` what
  alternatives were turned down and why. An entry you write is marked
  `*(Default)*`, since the person hasn't confirmed it. Decisions should
  settle the questions a builder would otherwise have to guess at: the
  edge cases are where a design is made, and a builder meeting one
  undecided will decide it alone. Read D1 to D7 first; they are short.
- A golden test's expected output **never comes from the compiler**. It
  is worked out by hand from the decisions, or written by a *model*, a
  small Python program in `t/models/` that computes the output from the
  definition; `t/models/README.md` says how.
- A **referee** is a second implementation of the language in Python,
  an evaluator written from the decisions that prints what any
  program's expected output must be. `make checks` runs every file in
  `t/referee/` over every golden test and fails where they disagree. It
  exists so that a model written by someone else can be checked. Write
  it as a loop over the program's structure, not as recursive calls,
  since a test program can nest thousands deep. A program it doesn't
  cover exits 3, and the check skips it.
- A step in `docs/PLAN.md` carries a **Referee** line (`extend
  t/referee/NAME.py to cover this`, or `none`, with the reason) and a
  **Size** line (`large` where there are decisions to make or a model
  to write; `medium` where the design is agreed and the tests are
  named; `small` where the step is a pattern to repeat).

## The four parts

1. **Decisions**, in `docs/DECISIONS.md` after D7: everything step 1
   needs, with reasons and rejections, written so the traps are decided
   before a builder meets them. Think about what a calculator's first
   operators must settle: the shape of a call, how many operands, what
   happens when a result doesn't fit 63 bits, how division rounds and
   what a zero divisor does, which fault reports when more than one
   could, what a malformed form is, and whether anything is computed at
   compile time. Decide each, don't list it as open.
2. **The step's text**, in `docs/PLAN.md` in place of the placeholder
   `### 1.`, in the shape of step 0's: what it adds, what files it
   touches, every test it adds with its program and where its expected
   output comes from (by hand, with the value worked out, or from a
   model the builder writes), which documents it moves, what it leaves
   out, and its Referee and Size lines.
3. **The referee**, `t/referee/calc.py`, if your Referee line says one
   is wanted: an evaluator from your decisions, agreeing with tests 000
   and 001 (`make checks` must end `all: 0 failed`).
4. **A brief**, `docs/BRIEF.md`, for the builder: what to read, what to
   do in what order, what not to touch, when to stop and ask, and how to
   report. Say whether a builder smaller than the Size line is to stop
   or to build and say so.

## Rules

- Keep the language small: decide what step 1 needs and nothing more.
  Rejecting a feature is a decision too; write it down.
- Do not build. Do not write tests or models. Do not change `reader.ts`,
  `codegen.ts`, the runtime, `LANGUAGE.md`, or `CLAUDE.md`'s Status.
- `make test` must still pass when you are done (`make checks` runs
  your referee).
- Keep command outputs short; your context is limited.

## Order of work

Your context is small and does not carry your reasoning from one reply
to the next. So **do not design the whole step in your head and write
it afterwards: decide one thing, write it to the file, then decide the
next.** Each decision is one `write_file` or one appending `run`
(`cat >> docs/DECISIONS.md <<'EOF' ... EOF`), and the file is your
memory. A reply that reasons for thousands of words without a tool call
is cut off, and what it worked out is lost.

1. `make test` once for the baseline: 2 golden tests, green.
2. Read only these: `docs/DECISIONS.md`, step 0 in `docs/PLAN.md`,
   `docs/LANGUAGE.md`, `t/models/README.md`, `t/referee/README.md`,
   `compiler/src/codegen.ts`, `runtime/rt.h`, `runtime/rt.c`,
   `t/000-int.lang`. Not `PROCESS.md`, `MODELS.md`, `CLAUDE.md`,
   `DESIGN.md`, the reader or the tests' runner: this brief has what
   they'd tell you.
3. Decide and write, one at a time, appending each to
   `docs/DECISIONS.md` as soon as it's decided: the shape of a call and
   the number of operands (D8); what happens when a result doesn't fit
   63 bits (D9); how division rounds, and the zero divisor (D10); the
   order operands are evaluated in, and which fault reports when more
   than one could (D11); what is computed at compile time, if anything
   (D12); what a malformed form is, with its messages (D13). Then read
   the file back once, whole.
4. Write the step's text into `docs/PLAN.md`, replacing the `### 1.`
   placeholder, in two or three writes if it's long: the operations and
   files, then the tests with their programs and outputs, then the
   documents it moves, what it leaves out, and the Referee and Size
   lines.
5. Write `t/referee/calc.py` from your decisions; `make checks`.
6. Write `docs/BRIEF.md`.
7. `git add -A` and commit with a subject like `Propose step 1:
   arithmetic (D8 to D13)`. Do not push.
8. Call `done` with your report.

## Report

Say: which step you chose and why; each decision in one line; whether
a referee was wanted and why; the last lines of `make test`; and every
point where you were unsure.
