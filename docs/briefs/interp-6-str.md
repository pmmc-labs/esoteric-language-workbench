# Brief: build step 6, strings

You are building step 6 of [`PLAN.md`](../PLAN.md), strings, in the
calculator's interpreter (TypeScript on Node, D28, D29), on this
branch. Paths here are from the repository's root.

Steps 0 to 5 are built: `bin/lang.ts` and `interp/`, with 46 golden
tests passing under two Nodes. Step 6 is decided, D31 to D33, as
defaults written for this experiment, and every one of its golden tests
is written, from `t/models/strings.py` and by hand, and agrees with a second
implementation extended for the step. Your job is the code that makes
them pass, and the documents that say so.

## Size

The step's Size line says **medium**. Compare it with your own model by
[`strings.pyS.md`](../strings.pyS.md)'s tiers and say which you are in the first
line of your report. You're a session with no one to ask, so **build
anyway**, whatever the comparison, and put a mismatch first in your
report.

## Read, in this order

1. `CLAUDE.md`, all of it.
2. `docs/PROCESS.md`, and "An interpreter instead of a compiler"
   closely.
3. `docs/LANGUAGE.md` and `docs/DESIGN.md`.
4. `docs/PLAN.md`: step 6 closely, and steps 0 to 5 for what landed.
5. `docs/D31 to D33.md`: D31 to D33, and what they cite.
6. `t/README.md`, the new tests (`t/07*`, `t/08*`), and
   `t/models/strings.py`.
7. The interpreter: `bin/lang.ts`, `interp/src/`, `interp/tests/`.

**Don't read anything under `t/referee/`.** It's the second
implementation your work is judged against, and agreement means
nothing if one was copied from the other.

## Do, in this order

1. `make hooks`, then `make test`: the 46 tests of steps 0 to 5 pass,
   and the new ones fail.
2. `DESIGN.md`'s "What the host gives": add a line for each thing Node
   could decide for this step, as step 0's lines do (inherits, with
   the test that shows it; overrides, and how; or asks), and commit
   that alone, before any code.
3. Build what the step says, with its unit tests in `interp/tests/`.
4. `make test`, `make golden-node`, `make check` (`npm install` first;
   if it can't reach the registry, say so and go on).
5. Move the documents the step names.
6. Commit, with the step and the decisions in the subject (`step 6:
   ... (D31 to D33)`); the hook checks it. More than one commit is fine
   if each leaves steps 0 to 5 green. Push.

## Don't touch

- Anything under `t/`: no test, expected output, model, referee,
  `t/checks.py` or `t/run.sh` changes.
- The `Makefile`, `package.json`'s scripts, `tsconfig.json`'s options.
- `docs/D31 to D33.md` up to the step's last decision (add after it, as
  below), `docs/PROCESS.md`, `docs/strings.pyS.md`, `docs/REPORT.md`,
  `docs/BACKGROUND.md`, this brief, `README.md`, `tools/`.
- Nothing from the step's "Leave out"; no form, operator, flag or
  environment variable it doesn't name.

## When something isn't as the step says

- **A test fails and you think its expected output is wrong.** Don't
  edit it. It came from a model of the decisions and agrees with the
  referee, so the interpreter is wrong until you can show from the
  decisions that it isn't. Two honest attempts and the same test still
  red: stop, and report the test, your output, and the decision you
  read differently.
- **The step needs a decision the log doesn't make**, or a line of
  "What the host gives" is a question for the person. Don't stop.
  Decide it, write it as the next entry in the section it belongs to,
  attributed *(Default, written by the builder of the interpreter's
  step 6, which could not ask; fair to revisit.)*, with its reasons and
  `Rejected:`, list it under `DESIGN.md`'s Open questions, and put it
  first in your report after the size line.
- **Something outside the step is broken.** Leave it, unless the step
  can't pass without it; report it either way.
- `strings.pyS.md`'s escalation signals apply as written: the pull to edit
  an `.expected`, a diff past what the step describes, a test that
  passes under one Node and fails under the other.

## Report

One message, at the end, in this order:

1. Your model and tier against the step's Size line.
2. Any decision you added, a line each, or "none".
3. The lines you added to "What the host gives", each in a line.
4. The commits, and what failed first and why, if anything did.
5. The last lines of `make test`, `make golden-node`, `make commits`,
   and `make check` or why it didn't run.
6. Anything you found outside the step, and what you did about it.
7. Every point where you were unsure, including those you settled
   yourself.
