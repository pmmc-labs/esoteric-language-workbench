# Experiment: an interpreter, from the decisions

The person asked, after the decision browser: "How applicable would the
process be for an interpreter rather than a compiler?" The answer was
mostly, with the independent checks rearranged, and it became
`docs/PROCESS.md`'s "An interpreter instead of a compiler" and the
`interpreter` branch (D28, D29). This experiment tests that answer: a
bare session builds the calculator again as an interpreter, from the
decisions and the tests alone, and we see what the process caught and
what it didn't.

## The question

Does the process carry to an interpreter as written, and are the risks
the new section names (the host leaking into the language, static
errors becoming dynamic, depth) caught by the process, or only by luck?

## The setup

- **The base**, `exp-interp`: an orphan commit of the `interpreter`
  branch without this directory, so the builder sees no compiler in
  git history and doesn't know what's probed. It has the calculator's
  decisions (D3 to D25, and D28 and D29), its 46 golden tests, its four
  models and the referee, as on main; `t/run.sh` running each test
  through `bin/lang.ts`; no `bin/lang.ts` and no `interp/`.
- **The session**: a bare cloud session, given only the repository at
  `exp-interp` and the prompt below, with no person to ask. It builds
  steps 0 to 5 from `docs/briefs/interp-0-5.md` and pushes to
  `interp-MODEL`.
- **The model**: Sonnet 5.5 first, the tier `MODELS.md` says builds a
  decided step every time, and the builder of main's step 5, so the run
  is comparable with main's. Then, if it's worth comparing, Haiku 5.5
  on the same base, as `interp-haiku`. Opus only as a reference, if
  those two differ in a way worth explaining.

The prompt, all of it:

    Read CLAUDE.md, then docs/briefs/interp-0-5.md, and do what the
    brief says: build steps 0 to 5 of docs/PLAN.md as an interpreter,
    step by step, and end with the report it asks for. There's no one to
    ask in this session.

## What's watched, and how it's judged

1. **Green.** The 46 golden tests pass under Node 22 and Node 24, no
   file under `t/` changes, and `make unit`, `make checks`, `make
   commits` and `make check` pass. Every compiler build was green, so
   anything less is news.
2. **The host's answers, first and right.** `DESIGN.md`'s "What the
   host gives" committed before any code, as step 0 says, and right
   about Node: its numbers are doubles, exact to 2^53, where D4 needs
   2^62; `<<` on a number is 32 bits; BigInt's `/` and `%` truncate as
   D5 wants, which is an inheritance that happens to be right and
   should be written down as one; the stack runs out at about ten
   thousand frames. Judged by the answers against the probes
   `exact-max`, `past-2^53`, `shl-32`, `shr-negative` and
   `div-min-by-minus-one`, and, from the transcript, whether the
   builder avoided the double from the checklist or met it in a failing
   test. Either is the process working; the first is the new section
   working.
3. **Static stays static.** D28's errors before running, which no
   golden test can see (D7): the probes `untaken-*`, `literal-past-*`,
   `two-expressions`, `empty-program`, `unbalanced`, `position`,
   `usage-no-file` and `missing-file`, and whether the unit tests the
   steps list were written.
4. **Depth.** Nothing decided, and the deepest golden test nests 147.
   The process says depth is a decision, not an accident; the brief
   says a question for the person becomes a flagged default. Good: an
   "asks" in `DESIGN.md` and a D30-and-on default, flagged in the
   report. Bad: a silent RangeError. Probes `deep-1000`, `deep-20000`,
   `deep-100000`.
5. **The open order of one operator's own checks.** Left open, and the
   step says to say what the interpreter does. Recorded:
   `two-faults-shl`, `two-faults-pow`.
6. **Agreement with the referee beyond the suite.** 2,000 random
   well-formed programs, seed 1, edge values and nesting to six,
   compared with `t/referee/calc.py`. Expected: none differ.
7. **The process as practised.** Commits per step naming the step; the
   Status, the plan's headings and progress line moved at each step;
   `DESIGN.md`'s Values and memory and The interpreter filled; any
   decision added, and how it's attributed; `t/referee/` never read
   (the transcript: any tool call naming it); the report in the
   brief's order, its size line first.
8. **Cost.** Tokens, tool calls and wall time, from the session's
   events.

## After the run

In a checkout of `interp-MODEL`, with `judge.py` copied in from the
`interpreter` branch:

    make test && make golden-node
    python3 exp/interp/judge.py probes
    python3 exp/interp/judge.py fuzz 2000 1
    python3 exp/interp/judge.py process origin/exp-interp

Then the transcript, for the order things failed in, whether
`t/referee/` was read, and the cost; and the diff, read.

## The baseline

`judge.py` was checked against main's compiler, put behind a shim that
gives it `bin/lang.ts`'s interface (a compile error as exit 2): all 46
golden tests, every probe as wanted, and 600 random programs with none
differing from the referee. Where nothing is decided, main's compiler:

- `two-faults-shl`, `two-faults-pow`: `fault: not an integer`, the
  operand's type checked first.
- `deep-20000`, `deep-100000`: `langc: internal error: RangeError:
  Maximum call stack size exceeded`, in the reader. main has the depth
  gap too; nobody decided it there either.

## Record

A section of `docs/MODELS.md`, "An interpreter, from the decisions",
with a table per run as the others have, and whatever it says about
the new section of `PROCESS.md`, there.
