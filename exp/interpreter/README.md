# The interpreter experiment

November 2026. The person asked, after the decision browser: "How
applicable would the process be for an interpreter rather than a
compiler?" The answer given was "most of it, with the independent
checks arranged on purpose", and this folder records how that answer
was built into a variant of the workbench and then tested: seven
builds of the calculator as an interpreter, by bare cloud sessions with
no person to ask, judged by the suite, by probes no golden test can
see, by random programs against the referee, by their history and by
their transcripts.

In short: the process carried. Every build was green, no golden test
failed once its step's code was written, every random program agreed
with the referee, and no builder read the referee. The host checklist
didn't change the obvious leak (every builder used `bigint`, with or
without it); it changed the quiet one, depth, from whatever Node's
stack allowed into a decided, flagged limit.

## What's here

| Path | |
|---|---|
| `README.md` | This record |
| `judge.py` | The judge: probes, random programs against the referee, the build's history; run from a build's checkout (below) |
| `briefs/` | What each builder was given: `interp-0-5.md` for steps 0 to 5, `interp-6-fn.md` and `interp-6-str.md` for step 6 |
| `step6/` | The two step 6s: their decisions (D31 on, defaults) and their step text, as the builders saw them |
| `results/` | The judge's output for every build, rerun at the end with the final `judge.py` |

## The branches

All in this repository. None is merged into main; `interpreter` is the
variant itself.

| Branch | What it is |
|---|---|
| `interpreter` | The workbench for an interpreter: D28 and D29, `PROCESS.md`'s "An interpreter instead of a compiler", `DESIGN.md`'s "What the host gives", the plan's steps 0 to 5 rewritten, the runner running `bin/lang.ts`, Sonnet's build of steps 0 to 5 adopted, `exp/interp/` (the plan and judge as run), and `MODELS.md`'s "An interpreter, from the decisions" |
| `exp-interp` | The base for steps 0 to 5: `interpreter` before any build, without `exp/`, with no history |
| `exp-interp-control` | The same without the checklist: no "What the host gives", no `PROCESS.md` interpreter section, no pointer to either |
| `exp-interp-fn`, `exp-interp-str` | The bases for step 6: the built interpreter, step 6 decided and its tests written, without `exp/`, with no history |
| `prep-fn`, `prep-str` | Where step 6 was prepared: the decisions, the model and the referee, and their merge |
| `interp-sonnet`, `interp-haiku`, `interp-control-sonnet` | The steps 0 to 5 builds |
| `interp-fn-sonnet`, `interp-fn-haiku`, `interp-str-sonnet`, `interp-str-haiku` | The step 6 builds |

## The setup

**The variant.** The calculator's language is unchanged: D3 to D25,
its 46 golden tests, its four models and its referee, as main has them
after step 5. What changed is the implementation and the process around
it.

- D28: an interpreter, not a compiler; what the compiler reported
  before running, the interpreter reports before evaluating anything,
  `FILE:LINE:COL: message`, exit 2, kept apart from a fault (exit 1).
  The person's choice to try an interpreter; the error rule a default.
- D29: a tree-walker in TypeScript on Node, so the referee (Python)
  stays in another host. A default.
- `PROCESS.md`'s new section: the host leaks into the language; what
  was static stays static; the referee in another host; the host's
  versions as the second oracle (`make golden-node`, Node 24 beside
  22); depth; determinism cheaper; adding cheaper, so simplicity
  guarded harder; an interpreter as a later compiler's oracle.
- `DESIGN.md`'s "What the host gives": a line per place Node could
  decide something for the language (integers, division, shifts,
  `**`, equality, printing, order, errors and exit, depth), each to be
  answered inherits, overrides or asks, at step 0, before the code.

**The bases** are orphan commits: the tree without history and without
`exp/`, so a builder sees no compiler in git, no earlier run's
transcript (the ones in `exp/local/` quote main's compiler), and not
what's judged. The control base removes the checklist and every pointer
to it, so nothing hints that it was there.

**Step 6** was written for these rounds, twice, on what is particular
to an interpreter on Node:

- **Functions, tail calls and depth** (D31 to D34): first-order
  definitions, a call charged as an operation, tail calls in constant
  space, and 10,000 calls in progress before `stack`. A tree-walker
  recursing on Node's stack can't reach that, and Node has no tail
  calls, so the interpreter must keep its own stack.
- **Strings** (D31 to D33): sequences of code points, printed with the
  language's escapes, six operators, a source that must be valid UTF-8,
  columns in code points. Placed where Node differs: UTF-16 `length`
  and `<`, `JSON.stringify`'s escapes, `TextDecoder` dropping a byte
  order mark, `\s` taking U+00A0.

The large model (Opus) wrote each step's decisions as defaults. Sonnet
wrote its model and 20 tests; Opus, apart, extended the referee from
the decisions alone; neither read the other's work. Both pairs agreed
on all 20 tests at the first run. Both pairs' reports found holes in
the decisions (what white space is, what ends a name, a byte order
mark, C1 controls; what a name is, budgets across calls, the program's
expression not a tail position, D30's reason overtaken), which were
closed before the bases were cut.

**The builders** were bare cloud sessions on the base, with this
prompt and nothing else:

    Read CLAUDE.md, then docs/briefs/interp-0-5.md, and do what the
    brief says: build steps 0 to 5 of docs/PLAN.md as an interpreter,
    step by step, and end with the report it asks for. There's no one to
    ask in this session.

(For step 6, `interp-6-fn.md` or `interp-6-str.md`, "build step 6".)

## How it was judged

From the root of a checkout of the build, with this `judge.py` copied
in as `exp/interp/judge.py` (it runs `bin/lang.ts` and
`t/referee/calc.py` from there):

    make test && make golden-node
    python3 exp/interp/judge.py process origin/BASE   host answers before code, t/ untouched, decisions added
    python3 exp/interp/judge.py probes                25 probes of steps 0 to 5
    python3 exp/interp/judge.py fuzz 2000 1           2,000 random programs against the referee
    python3 exp/interp/judge.py probes-fn             28 probes of step 6, functions
    python3 exp/interp/judge.py probes-str            38 probes of step 6, strings
    python3 exp/interp/judge.py fuzz-str 1000 1       1,000 random string programs against the referee

The probes are what no golden test sees: errors before running in
branches that never run, positions, usage; the host's numbers past
2^53, 32-bit shifts, `MIN / -1`, a huge exponent; names a JavaScript
object would answer for (`toString`, `constructor`, `__proto__`);
nesting at 1,000, 20,000 and 100,000; for functions, 10,000,000 tail
calls, a `within` body not in tail position, deep calls that also nest
evaluations; for strings, every literal error, invalid UTF-8, overlong
encodings and encoded surrogates, a byte order mark, U+00A0 and U+2028
as non-space, columns after a character past U+FFFF or a combining
accent, printing of NUL, DEL, U+2028, U+FEFF and C1, and ordering where
UTF-16 and code points part. Where nothing is decided, a probe records
what happened rather than judging it. Every probe's expected value was
checked against the extended referees, and the judge itself against
main's compiler behind a shim (every probe as wanted, 600 random
programs agreeing).

Each transcript was read for any tool call naming `t/referee/`; none
read it (the only mentions were their own edits to documents that name
it).

## Results

### Steps 0 to 5

| | Sonnet | Haiku | Sonnet, no checklist |
|---|---|---|---|
| 46 tests under Node 22 and 24, every check | yes | yes | yes |
| 25 probes; 2,000 random programs | all; none differ | all; none differ | all; none differ |
| Host answers committed before code | yes | yes | (no checklist) |
| A golden test failed while building | none | none | none |
| A program nested 20,000 deep | an error with a position, a limit of 1,000 (D30), flagged | the same, the same limit, chosen independently | Node's `RangeError`, exit 3, past about 6,000; noticed and noted, not decided |
| Decisions added | 1 | 5 | 0 |
| Size line against tier | match | mismatch, said first | match |
| `t/referee/` read | no | no | no |
| Time, turns, output tokens, cost | 6.8 min, 39, 34K, $1.33 | 10.4 min, 63, 111K, $0.87 | 4.2 min, 27, 28K, $0.97 |
| Session | `session_017A3bHV7BnwfYh9RUNs32bw` | `session_017A3bHX8nMSKzdqJ9sxJ521` | `session_017A3bHVySjupwdfzeGCw2ad` |

### Step 6

| | Functions, Sonnet | Functions, Haiku | Strings, Sonnet | Strings, Haiku |
|---|---|---|---|---|
| 66 tests under both Nodes, every check | yes | yes | yes | yes |
| The step's probes | 28 of 28 | 28 of 28 | 38 of 38 | 38 of 38 |
| Random programs against the referee | 2,000, none differ | 2,000, none differ | 1,000 string and 2,000, none differ | the same |
| Host lines committed before code | yes | yes | yes | yes |
| Decisions added | 0 | 1, the wording of D31's errors | 0 | 1, the wording of literal errors |
| 10,000,000 tail calls, two runs | 10.6 s and 9.9 s, flat at 78 MB | 6.2 s and 7.6 s, flat at 79 MB | | |
| Time, turns, output tokens, cost | 5.5 min, 26, 22K, $0.77 | 14.2 min, 56, 77K, $0.76 | 3.6 min, 26, 20K, $0.78 | 5.9 min, 66, 63K, $0.57 |
| Session | `session_017A3bHY5Xfog1cEiS9rwzeD` | `session_017A3bHUwMhqGi6tRcL7YFtb` | `session_017A3bHW5EkUFBiW9bvmRS6C` | `session_017A3bHVWARHdUAL13oKtQ84` |

The step 6 writers: the functions model 131K tokens and 4.9 minutes
(Sonnet), its referee 155K and 5.1 (Opus); the strings model 159K and
4.0 (Sonnet), its referee 136K and 3.9 (Opus).

## The interpreters they built

Every build has the same skeleton: `bin/lang.ts`, then a reader, a
checker that finds every error before running, and an evaluator, 300
to 600 lines of source and as much again of unit tests. Every build
holds integers as `bigint` range-checked after each operation, compares
with `===` only, answers `**` without building huge intermediates, and
cites the decision behind each override in a comment.

The three steps 0 to 5 builds were written apart and differ:

- **Sonnet**: a recursive tree-walker over the reader's forms; the
  reader a loop with its own stack, where the nesting limit lives;
  budget counts as `bigint`.
- **Haiku**: the same shape, the operator table in a file of its own,
  unit tests per feature rather than per pass.
- **The control**: the checker compiles forms to a small node tree
  (`lit`, `op`, `if`, `within`) and a 53-line evaluator walks it, the
  cleanest of the three; but it recurses on Node's stack with no
  limit, and keeps the budget counts as JavaScript numbers with
  `Infinity`, a host inheritance that would be wrong past 2^53
  operations.

The step 6 builds start from Sonnet's interpreter, so their operator
tables are inherited. Depth and tail calls forced a new evaluator:

- **Functions, Sonnet**: a loop over a task stack and a value stack. A
  call in progress is marked by a `ret` task, and a call is a tail call
  exactly when `ret` is the next task: nothing is left to do after it,
  so it replaces its caller. Tail position falls out of the stack
  rather than being tracked.
- **Functions, Haiku**: a frame stack with an explicit `tail` flag
  threaded through each frame. More code (242 lines to 191), as
  correct, and faster on the tail loop.
- **Strings, both**: a strict UTF-8 decoder that keeps a byte order
  mark (`TextDecoder("utf-8", { fatal: true, ignoreBOM: true })`), a
  reader with exactly four white-space characters stepping one code
  point at a time so columns count code points, operators over
  code-point arrays (`[...s]`), and a printer of the language's own
  escapes. Haiku noted the cost: every `str/at` builds the array, so
  it's linear in the string.

Leaks the builders found without a probe pointing at them: Haiku, that
`1n == true` is `true` in JavaScript; Sonnet, that names in plain
objects would find `constructor` and `__proto__` (probed afterwards,
and every build passes).

None of them wrote the interpreter in a self-hostable style, as
a64-slight's compiler is written; the template leaves that rule a
placeholder, so none was asked to.

## What this says

- **The process carries to an interpreter.** Seven builds, two tiers,
  two kinds of step, all green, the same discipline: tests from an
  independent source, the decisions, the checks, the referee unread.
- **The checklist's worth is in what no test sees.** On the leaks a
  test catches, a capable model didn't need it. On depth, which no
  test reached, it turned the host's stack into a decision.
- **A decision that names where the host differs is cheaper than a
  probe that finds it later.** Step 6's decisions were written at
  those places, and every builder met them.
- **Write the model and the referee before cutting the base.** Both
  pairs found holes in the large model's decisions; closed in time, no
  builder had to invent white space or what ends a name.
- **Haiku builds an interpreter.** More turns and tokens than Sonnet,
  less money, the same result, more of its silences written down as
  defaults, and its size mismatch said first every time.

## The experimenter's errors

- D28 was first attributed wholly to the person; its error rule and
  exit 2 were the agent's, and the attribution was corrected on both
  branches before any build.
- One base (`exp-interp-fn`) was pushed once from unedited decisions
  when an edit's assertion failed and the script went on; it was
  rebuilt before any session used it.
- The step 6 briefs were made from one template by substitution, and
  the size check's `MODELS.md` came out `fn.pyS.md` and
  `strings.pyS.md`. Three of the four step 6 builders reported the
  file missing; the two Sonnet runs couldn't place their tier. A brief
  made by substitution is checked for everything the substitution
  reached.
- The Haiku builders found the session's attribution reminder and its
  system prompt in conflict over naming the model in commit trailers,
  and left the model's name out. Not an error of the experiment, but
  worth a rule.

## Open, for the person

- D30, nesting limited to 1,000, both builders' default.
- Step 6, either one: its decisions are defaults (`step6/`); the
  strings decisions print C1 controls raw, which both writers
  questioned.
- Which fault reports when one operator could fault two ways: every
  build checks types first, as main does; Haiku made it a decision.
- Whether the interpreter should be written to be ported to the
  language later, as a64-slight's compiler is.

## Running it again

A new base is an orphan commit of a branch's tree without `exp/`:

    git read-tree BRANCH                     # into a temporary GIT_INDEX_FILE
    git rm --cached -r -f exp
    tree=$(git write-tree)
    git branch BASE $(git commit-tree $tree -m "...")

A run is a cloud session on the base with the prompt above and an
outcome branch, then the commands under "How it was judged". The
judge's outputs for these runs are in `results/`.
