# Brief: build steps 0 to 5 as an interpreter

You are building the calculator again, as a tree-walking interpreter in
TypeScript on Node: steps 0 to 5 of [`PLAN.md`](../PLAN.md), on this
branch (D28, D29). Paths here are from the repository's root.

The language is decided, D3 to D25, and every one of its 46 golden
tests is written, with its expected output from a model or by hand.
They passed on a compiler built from the same decisions, and a second
implementation agrees with every one. Your job is the interpreter, step
by step, and the documents that say so. Nothing is built yet: no
`bin/lang.ts`, no `interp/`.

## Size

Every step's Size line says **medium**. Compare it with your own model
by [`MODELS.md`](../MODELS.md)'s tiers and say which you are in the
first line of your report. You're a session with no one to ask, so
**build anyway**, whatever the comparison, and put a mismatch first in
your report.

## Read, in this order

1. `CLAUDE.md`, all of it.
2. `docs/PROCESS.md`, all of it, and "An interpreter instead of a
   compiler" closely.
3. `docs/LANGUAGE.md`.
4. `docs/DESIGN.md`.
5. `docs/PLAN.md`: steps 0 to 5 closely.
6. `docs/DECISIONS.md`: D3 to D29.
7. `t/README.md`, and the top of `t/run.sh`.

**Don't read anything under `t/referee/`.** It's the second
implementation your work is judged against, and agreement means
nothing if one was copied from the other. The models in `t/models/`
you may read: they're how the expected outputs were made.

## Do, step by step

Run `make hooks` once, first. Then, for each step from 0 to 5, in
order:

1. Step 0 only: answer `DESIGN.md`'s "What the host gives", every item,
   as the step says, and commit that alone, before any code.
2. Build what the step says, with its unit tests in `interp/tests/`.
3. Run the step's golden tests and every earlier step's, under both
   Nodes: `./t/run.sh t/0[0-N]*.lang` and
   `LANG_NODE=/opt/node24/bin/node ./t/run.sh t/0[0-N]*.lang`, N the
   step. Then `make unit`, `make checks`, and `make check` (`npm
   install` first; if it can't reach the registry, say so and go on).
4. Move the documents the step names.
5. Commit, with the step in the subject (`step 2: ...`); the hook
   checks it. More than one commit a step is fine if each leaves the
   earlier steps green. Push after each step.

After step 5, `make test` and `make golden-node` pass whole.

## Don't touch

- Anything under `t/`: no test, expected output, model, referee,
  `t/checks.py` or `t/run.sh` changes. A step adds no golden test.
- The `Makefile`, `package.json`'s scripts, `tsconfig.json`'s options.
- `docs/DECISIONS.md` D1 to D29 (add after them, as below),
  `docs/PROCESS.md`, `docs/MODELS.md`, `docs/REPORT.md`,
  `docs/BACKGROUND.md`, this brief, `README.md`, `tools/`, `exp/`.
- No form, operator, flag or environment variable beyond what the
  steps name; nothing from a step's "Leave out".

## When something isn't as the step says

- **A test fails and you think its expected output is wrong.** Don't
  edit it. It passed main's compiler and agrees with the referee, so
  the interpreter is wrong until you can show from the decisions that
  it isn't. Two honest attempts and the same test still red: stop, and
  report the test, your output, and the decision you read differently.
- **A step needs a decision D3 to D29 don't make**, or an item of
  "What the host gives" is a question for the person. Don't stop.
  Decide it, write it as the next entry (D30 and on) in the section it
  belongs to, attributed *(Default, written by the builder of the
  interpreter's step N, which could not ask; fair to revisit.)*, with
  its reasons and `Rejected:`, list it under `DESIGN.md`'s Open
  questions, and put it first in your report after the size line.
- **Something outside the steps is broken.** Leave it, unless a step
  can't pass without it; report it either way.
- `MODELS.md`'s escalation signals apply as written: the pull to edit
  an `.expected`, a diff past what a step describes, a test that passes
  under one Node and fails under the other.

## Report

One message, at the end, in this order:

1. Your model and tier against the steps' Size lines.
2. Any decision you added (D30 and on), a line each, or "none".
3. `DESIGN.md`'s "What the host gives": each item in a line, inherits,
   overrides or asks, and how.
4. Each step: its commits, and what failed first and why, if anything
   did.
5. The last lines of `make test`, `make golden-node`, `make unit`,
   `make checks`, `make commits`, and `make check` or why it didn't run.
6. Anything you found outside the steps, and what you did about it.
7. Every point where you were unsure, including those you settled
   yourself.
