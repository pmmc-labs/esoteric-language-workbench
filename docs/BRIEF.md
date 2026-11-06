# Brief: step 5, a budget

For the builder of step 5 in [`PLAN.md`](PLAN.md), `(within n expr)`. Read
this whole brief, then the step, then build. The decisions are D20 (from
the person) and D21 to D27 (defaults, not yet picked; see the note at the
end). The step's own text names its tests and their expected outputs.

## Your tier

The step is marked **large** for its model and **medium** for its build
(`docs/MODELS.md`). Compare your own tier with that before you start.
You are a sub-agent with no one to ask, so the rule is: build, and put
the mismatch first in your report. Do not stop for the tier alone. Do
stop for the things listed under "Stop rules" below.

## What to read, in this order

1. `CLAUDE.md`: "Read first", "Working rules", "Code style" (the
   `checked` lesson, and the argument-order rule), and "Commands".
2. `docs/LANGUAGE.md`: the language as it is.
3. `docs/PLAN.md`: steps 3 and 4 for the shape (model and tests committed
   red, then the code), then step 5 in full.
4. `docs/DECISIONS.md`: D3, D5 to D8, D10 to D14, D16 to D19, and D20 to
   D27. Where a decision and the plan disagree, the decision wins; report
   the disagreement.
5. `docs/PROCESS.md`: "Golden tests from an independent source".
6. `t/models/README.md`, `t/models/pow.py` (the shape of a model), and
   `t/models/arith.py` (the fold).
7. The code you change: `compiler/src/codegen.ts`, `runtime/rt.c`,
   `runtime/rt.h`, `compiler/tests/codegen.test.ts`.

**Do not read `t/referee/`.** It is the judge's second implementation.
`make test` runs it, and you may see what it prints, but do not read its
source or change it. Its job is that your model and its agreement are two
derivations, not one copied.

## What to do, in order

1. **The model and the tests, red.** Write `t/models/within.py` from the
   decisions alone, not from `compiler/` or `runtime/`. Its docstring
   lists every command that writes a file, one a line, as `pow.py` does.
   Write `t/050-within-every-op.lang` and its `.expected` by its commands.
   Write `t/051-*.lang` to `t/063-*.lang` by hand, one per test in the
   plan, each with a comment giving its count and saying it is by hand.
   For each, work out the output from the decisions first, then compare
   with the value the plan lists. If they differ, stop on that test and
   report both. Run `make test`: the 26 existing tests pass, the new ones
   fail. Commit: subject names the step and D20 to D26.
2. **The generated C, D27.** Change `codegen.ts` so each operation's
   non-literal operands go into temporaries, in order, and the operation
   is one statement after them; literals stay where they stand; an `if`'s
   branches are statements, only the taken one runs. Update the two unit
   assertions that match the nested form (the nested expression, and the
   `if`'s test). Say so in the commit. All 26 existing golden tests must
   pass. Commit: subject names D21 and D27.
3. **The runtime counter and the charges, D23 to D26.** In `rt.c` and
   `rt.h`: a `uint64_t` count and a limit (none outside any `within`).
   Charge once on entry to each operator's runtime function, before its
   type checks, and once for `if` after its test's operands, before
   `rt_test`'s check. Helpers an operator calls do not charge again. The
   fault is `budget spent`. Add only the entry points `within` needs, and
   declare them in `rt.h`. Commit: subject names D23 to D26.
4. **The special form, D22.** In `codegen.ts`, `within` beside `if`, with
   the compile errors and messages in the plan, and their unit tests in
   `compiler/tests/codegen.test.ts`. Commit: subject names D22.
5. **Verify.** `make test` (all 26 existing and all of 050 to 063
   green); `LANG_CC=clang make golden-clang`; `make sanitize` (the
   runtime changed); `make check` if `npm install` has been run.
6. **Document.** `docs/LANGUAGE.md`: a budgets section in prose (no
   tables), the operand order in its forms section, and `budget spent` in
   its faults section. `docs/PLAN.md`: step 5's heading becomes "(done)"
   with a note where what landed differs from the text; the progress line.
   `CLAUDE.md`'s Status: one paragraph for step 5 with its decisions, its
   test numbers and what's Next (step 6, to be proposed). Also say in the
   Status that D21 settles the open item about which fault reports when a
   call could fault two ways. Do not change `docs/DESIGN.md`.
7. **Commits.** One subject per commit, each naming its decision or step.
   Run `make commits` before you report. Do not push.

## What not to touch

- `t/referee/`, in any file.
- The existing golden tests (`t/000` to `t/045`, `.lang` and `.expected`)
  and the models `arith.py`, `compare.py`, `bits.py`, `pow.py`. A change
  to an expected output means a model rerun, not a patch, and a model is
  not changed to match the code.
- `docs/DECISIONS.md` entries D1 to D27. Don't edit a decision. If one
  is wrong, stop and report it.
- `docs/DESIGN.md`, `bin/langc.ts`, the reader, `compiler/src/errors.ts`.
- Any flag, environment variable, or knob. Any language feature beyond
  `within`.
- `make hooks` in this worktree. It writes the hook into the git
  directory that `git rev-parse --git-path hooks` names, which in a
  worktree can be another checkout's. Check that path first, and write
  nothing outside this worktree.

## Stop rules

- A question the decisions don't answer: stop that part and report it.
  Do not write a default into `DECISIONS.md`. A silence you fill in the
  code is a default that the person has not seen, so don't fill one.
- A hand-worked value that differs from the plan: stop that test; report
  both values.
- A model and the referee disagree, or `make checks` says so: stop, and
  report the test and what `make checks` printed. Do not read the
  referee to settle it.
- An existing golden test fails after step 2: stop; the change must keep
  all 26 passing.
- You feel the need for a flag, an environment variable, or a knob: stop.

## How to report

Your final message, in this order:

1. The mismatch between your tier and the step's Size line, first.
2. Each decision you followed, D21 to D27, one line each, and every point
   where the decisions were silent: what it was, and whether you stopped
   or filled it.
3. Each stop, with its output.
4. Each existing unit test you changed, and why.
5. The last lines of `make test`, and the results of `make golden-clang`
   and `make sanitize`.
6. The commits: subject and hash for each, and the result of `make commits`.
7. Anything you were unsure of, one line each.

## A note for whoever picks the decisions

D21 to D27 are defaults, written by a proposer and not yet picked. The
person can change any of them before step 5 is built. If they change one,
the plan, the referee, and the tests move with it, so this brief is
written for D21 to D27 as they stand. If a pick reverses one of them,
the builder stops; do not hand it to a builder until the picks are in.
