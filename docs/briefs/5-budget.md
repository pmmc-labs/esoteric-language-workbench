<!-- The brief Opus wrote for step 5, which Sonnet built from, kept as
     the worked example of a brief (docs/PROCESS.md, "The loop"). Paths
     in it are as the proposal left them. -->

# Brief: build step 5, a budget

You are building step 5 of [`PLAN.md`](PLAN.md), `(within n expr)`, in
the repository you were given, on its branch. Paths here are from the
repository's root. Work only there, and don't push.

The step is designed. D20 is the person's; D21 to D27 decide the rest,
down to the shape of the generated C and of the runtime's counter.
Every test's program and expected output is written in the step. Your
job is the code that makes them pass, and the documents that say so.

## Size

The step's Size line says **medium**. Compare it with your own model by
[`MODELS.md`](MODELS.md)'s tiers and say which you are in the first
line of your report. If you're smaller than medium, **build anyway**
and put the mismatch first in your report: you're a sub-agent with no
one to ask, the step leaves nothing to judgement, and the suite and the
referee will catch what goes wrong. If you're larger, build too, and
say so. Don't stop for the size alone.

## Read, in this order

1. `CLAUDE.md`, all of it.
2. `docs/LANGUAGE.md`.
3. `docs/PLAN.md`: step 5 closely, and steps 2 to 4 for the shape of a
   step that landed.
4. `docs/DECISIONS.md`: D20 to D27, and the ones they cite (D4, D6,
   D7, D13, D14, D17, D19).
5. `t/README.md`, `compiler/src/codegen.ts`, `compiler/tests/codegen.test.ts`,
   `runtime/rt.h`, `runtime/rt.c`, the top of `t/run.sh`.

`docs/PROCESS.md` and the rest of `docs/MODELS.md` are there if you want
the why. **Don't read anything under `t/referee/`**: it's the second
implementation your work is judged against, and agreement means
nothing if one was copied from the other. Don't read other worktrees or
branches.

## Do, in this order

1. `make hooks` (in a worktree it writes the hook into the shared git
   directory; that's expected), then `make test`: it should end `all:
   0 failed`, with 26 golden tests.
2. Write the twenty golden tests, 050 to 069, as step 5 gives them: a
   comment line of your own naming the decisions and saying the output
   is by hand from step 5 (don't put a `t/models/` path in it), then
   the program; the `.expected` exactly as given, newline-terminated, a
   fault as its two lines. Don't run the compiler to get an expected
   output; they're given. Run `./t/run.sh t/05*.lang t/06*.lang` and
   `LANG_CC=clang ./t/run.sh t/05*.lang t/06*.lang`: all twenty should
   fail under gcc, and all but 059 under clang. Commit them alone, red,
   with the step in the subject (`Tests for step 5, red: ...`).
3. The runtime, D27: `spent` and `limit`, the charge first in all
   seventeen operator functions, `rt_within` and `rt_within_end`.
4. The compiler, D24 and D26: `within` beside `if`, the two
   temporaries where both operands are lists, the declarations at the
   top of `lang_main`. Then the unit tests the step lists, added beside
   the others.
5. `make test`, `make golden-clang`, `make sanitize`. And `make check`
   if `npm install` works; if it can't reach the registry, say so and
   move on.
6. The documents the step names: `LANGUAGE.md`, the step's heading and
   the progress line in `PLAN.md`, `CLAUDE.md`'s Status and the
   argument-order lesson in its code style.
7. Commit the code and documents with the step and the decisions in the
   subject (`... (step 5, D20 to D27)`); the hook checks it. More than
   one commit is fine if each is green.

## Don't touch

- Any test or model that existed before you started: `t/0[0-4]*`,
  `t/models/`, and the existing assertions in
  `compiler/tests/codegen.test.ts` (add yours; change none). D26 is
  written so that none of them moves. If one does, your C differs from
  D26's; fix the C.
- `t/referee/`, `t/checks.py`, `t/run.sh`, the `Makefile`.
- `docs/DECISIONS.md` D1 to D27, `docs/PROCESS.md`, `docs/MODELS.md`,
  `docs/DESIGN.md`, `docs/BACKGROUND.md`, this brief, `README.md`.
- No environment variable, flag or knob; no new form or builtin beyond
  `within`; nothing from the step's "Leave out".

## When something isn't as the step says

- **A given test fails and you think its expected output is wrong.**
  Don't edit it. Every expected output in step 5 was worked by hand
  from the decisions and agrees with the referee and with a prototype,
  so the code is wrong until you can show from the decisions that it
  isn't. Two honest attempts and the same test still red: stop, and
  report the test, your output, and the decision you read differently.
- **The step needs a decision D20 to D27 don't make.** Don't stop.
  Decide it, write it as the next entry (D28) in the section it belongs
  to, attributed *(Default, written by the builder of step 5, which
  could not ask; fair to revisit.)*, with its reasons and `Rejected:`,
  and put it first in your report after the size line.
- **Something outside the step is broken.** Leave it, unless the step
  can't pass without it; report it either way.
- The rest of `MODELS.md`'s escalation signals apply as written: the
  pull to edit an `.expected`, a diff past what the step describes, a
  test that passes plain and fails under the sanitizers.

## Report

One message, in this order:

1. Your model and tier against the step's Size line.
2. Any decision you added (D28 and on), each in a line, or "none".
3. What landed: the commits (`git log --oneline` since the base), and
   `git diff --stat` since the base.
4. The last lines of `make test`, `make golden-clang` and `make
   sanitize`, and of `make check` or why it didn't run.
5. Anything you found outside the step, and what you did about it.
6. Every point where you were unsure, including any you settled
   yourself.
