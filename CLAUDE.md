# [name]

[One paragraph: what the language is, what it runs on, what the compiler
is written in and what it should become. Two or three sentences.]

## Status

[A running paragraph of what's built, by plan step and decision number,
updated every time a step lands. This is the handoff between sessions:
a new session reads it before anything else. Keep it as one paragraph
per era, dense, with golden test numbers and `Dn` references, so a
claim can be checked against a test and a decision. Say what's **Next**
at the end, and what's a candidate but not agreed. The workbench's own:]

**This is the `interpreter` branch** (D28, D29): the calculator of
main after step 5, its decisions D3 to D27, its 46 golden tests, its
models and its referee, to be built again as a tree-walking
interpreter in TypeScript on Node, steps 0 to 5 of
[`docs/PLAN.md`](docs/PLAN.md), every step's tests already written.
main's compiler and runtime aren't here, nor are the decisions about
them binding (D2, D14's encoding, D26, D27): what a program prints is
the same, and what the compiler reported before running the
interpreter reports before evaluating (D28, exit 2). Step 0 is built:
the host's answers are in `DESIGN.md` (committed before any code), and
D30 to D34 are the interpreter's own defaults, written then because
nothing could be asked. The reader, the checker and the evaluator
exist, with `bin/lang.ts` on top, and only integers and booleans run:
golden tests 000 to 001, 010 to 015, 020 to 024 and 030 to 036 pass on
Node 22 and 24, and 26 unit tests in `interp/tests/`. Steps 1 to 3 are
built: `+ - * / %` (D3 to D6), the booleans and the six comparisons (D11,
D12), `if` (D13), and the five bit operations (D15 to D17), with the
errors before running that D33 gives them. Step 3's open point, which
fault reports for `(bit/shl #true 99)`, is settled by D32 as the
interpreter's default. **Next:** step 4 (tests 040 to 045). Not agreed,
from main: which fault reports when one operator could fault two ways.
D32 is the interpreter's default for it, and step 3 is where it bites.

## Read first, in this order

1. [`docs/LANGUAGE.md`](docs/LANGUAGE.md): the language as it is, every
   form and builtin, for someone writing programs in it.
2. [`docs/DESIGN.md`](docs/DESIGN.md): the language and implementation as
   agreed. **(open)** marks proposals that haven't been confirmed.
3. [`docs/PLAN.md`](docs/PLAN.md): the build order.
4. [`docs/DECISIONS.md`](docs/DECISIONS.md): why, and what was turned
   down. Check it before "improving" something; it may have been decided
   against.
5. [`docs/BACKGROUND.md`](docs/BACKGROUND.md): prior art and parked ideas.
   Optional.

## Working rules

- **Aggressively simple** is the main design rule. When a feature needs
  machinery, say so and offer to cut or change it.
- **Propose before building** any change to language semantics, a new
  special form or builtin, a change to [the core rule], or anything
  marked (open). Give options and a recommendation. Record the outcome in
  `docs/DECISIONS.md` (who decided, why, what was rejected) and update
  `docs/DESIGN.md`.
- When a special form or builtin is added or changes, update
  `docs/LANGUAGE.md` (no tables there), and the guide where it shows it.
- Keep a working interpreter with passing tests at the end of every step
  (Ghuloum). Each step adds golden tests.
- **Examples bend to the language, not the other way round.** When an
  example needs something the interpreter doesn't do, change the
  example, or leave it out; don't add to the language to make it pass.
- Verify a reported misbehavior against an independent implementation
  before calling it a bug.
- When a change moves an expected output that a model in `t/models/`
  wrote, rerun the model; don't patch the file. A patched file leaves the
  model stale, and the next change finds the two disagreeing.
- When editing with scripts, assert that each replacement matched.
- Test timing uses a virtual clock; real time is never used in tests.
- Update the Status section above as steps land.
- A commit that touches the implementation names its decision or plan
  step in the subject (`make hooks` installs the check).
- The builder of a step doesn't read `t/referee/`: it's the second
  implementation the step's model is checked against, and agreement
  means nothing if one was copied from the other.
- At the start of a step, compare the step's **Size** line with your own
  model, by `docs/MODELS.md`, and say so if they don't match. Then: in
  a session with a person, stop and ask; as a sub-agent with no one to
  ask, build and put the mismatch first in your report, unless the
  brief says to stop. Escalate on `MODELS.md`'s signals as they come.

## Code style

- [Indentation, line width, naming.]
- [The compiler's shape. a64-slight's rule: pure functions over immutable
  s-expressions, association lists for environments, no classes, so it
  can be ported to the language itself line by line. Pick the shape that
  makes self-hosting a translation rather than a rewrite.]
- [Constraints the host platforms impose, as you learn them. Name the
  symptom and the fix, so the lesson isn't relearned.] The host is
  Node (D29): its lessons go here as they're learned, and `DESIGN.md`'s
  "What the host gives" holds what the language takes from it or
  overrides. The rest of this item is main's, the compiler's lessons
  in C, kept for the record and not binding here. C doesn't order
  a call's arguments: never pass a variable and a call that sets it in
  the same argument list (`runtime/rt.c`'s arithmetic read `r` before
  `__builtin_add_overflow` set it under clang, and gcc hid it), and
  never two arguments that can fault or charge a budget: the compiler
  puts an operator's two list operands in temporaries with the comma
  operator (D26). The
  cloud machine's `cc` is gcc; the Mac's is clang; run the suite with
  `LANG_CC=clang` too before calling a runtime change done, and `make
  sanitize`, which found the second one: a left shift of a negative
  value is undefined before C23, so the tag multiplies instead. Clang
  also stops at 256 levels of brackets, so a generated expression that
  nests one level per term of a long chain won't compile (the bit model
  folds as a tree for this); the compiler itself nests one level per
  operator, so a program that deep fails under clang too, and nothing
  fixes that yet.
- Comments explain why, not what.

## Toolchain

- Node 22.18 or later (it runs the interpreter's TypeScript as it is,
  so the interpreter uses only erasable syntax: no parameter
  properties, no enums); a second Node for `make golden-node`
  (`/opt/node24/bin/node` on the cloud machine, `LANG_NODE_OTHER`
  elsewhere); Python 3 for the models, the referee and the checks. No
  C compiler.
- [The machine cloud sessions develop on, and how a target that isn't
  native runs there (cross-compile and an emulator, say), once there is
  one.]
- `t/run.sh t/000-int.lang` checks the setup; it should end
  `1 tests, 0 failed`.

## Layout

| Path | |
|---|---|
| `bin/` | The driver: `bin/lang.ts FILE` runs a program |
| `interp/src/` | One file per pass: reader, checker, evaluator, errors |
| `interp/tests/` | Unit tests, per pass |
| `lib/` | The prelude, compiled into every program, and the libraries a program asks for |
| `examples/` | Example programs; each with a `.expected` is a golden test |
| `docs/guide/` | The guide; its code blocks are golden tests too |
| `tools/decisions/` | The decision-log browser: `extract.py` (a `DECISIONS.md` to JSON), `page.py` and `page.html` (one HTML page of it); its README has the judgement calls |
| `t/` | Golden tests: `NNN-name.ext` + `NNN-name.expected`; `run.sh`; `models/`; `referee/` (an evaluator of the language from the decisions, run over every test by `checks.py`; the builder of a step doesn't read it); `data/` |
| `build/` | Output (ignored) |

## Commands

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`). A few seconds.
- `make unit`, `make golden`, `make checks`: one at a time.
  `t/run.sh t/000-int.lang` runs one golden test; `JOBS=1` runs them
  one at a time. `make models` reruns every model and writes its
  files; `make commits` checks the subjects since origin/main; `make
  hooks` installs the commit-msg hook.
- `make check`: `tsc --noEmit` (`npm install` once, for it).
- `make golden-node`: the golden tests under a second Node, not part
  of `make test`; run it at the end of every step.
- `node bin/lang.ts file.lang`: run a program: its value and a newline
  on stdout, exit 0; a fault, `fault: ...` on stderr, exit 1 (D6); an
  error before running, `FILE:LINE:COL: message` on stderr, exit 2
  (D28), as is a usage error or a file it can't read; a fault in the
  interpreter itself is `lang: internal error: ...` with Node's stack.
  `LANG_NODE` is the Node `t/run.sh` runs it under.
- `make decisions`: `build/decisions-workbench.html` and
  `build/decisions-a64-slight.html` (`A64=path`, `../a64-slight` by
  default), a browser of each decision log, one file each.
- [Environment variables a program reads: the virtual clock,
  the heap cap, record and replay, the scheduling seed, the GC stress
  and poison knobs. `t/run.sh` sets the ones the tests assume.]

The interpreter prints the program's value, then a newline, and exits
0. A fault is `fault: ...` on stderr and exit 1. The golden tests check
stdout and stderr together, plus `exit: N` when the status isn't 0.
