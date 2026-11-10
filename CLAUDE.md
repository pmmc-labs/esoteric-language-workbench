# SMOL

SMOL is a small JavaScript-like language for personal experimentation with
bootstrapped object meta-models, after the Perl sketch in
`docs/prior-art/MiniMetaModel.pl`. It is not general-purpose and not for
speed: it exists to find the smallest runtime a bootstrapped meta-model
needs. Nothing is built yet. It is a tree-walking interpreter in TypeScript,
run by Node (DECISIONS D14).

## Status

Nothing in SMOL runs yet. The decisions are D5 to D7 (the process), D8 to
D13 (User: the scope, the object model and the syntax), and D14 to D22 (User:
the implementation and the open questions, each taken as recommended). The
calculator's D1 to D4 were removed. The calculator's compiler, runtime and
golden tests 000 and 001 are still in the tree and go when step 0 lands.
**Next:** step 0 in [`docs/PLAN.md`](docs/PLAN.md), which is agreed but not
started. It is marked large, and this session's builder is small-tier, so it
waits: a larger model writes or splits it first, or the person accepts a
small builder for it (PLAN.md, "Step 0 waits on a size check").

## Read first, in this order

1. [`docs/LANGUAGE.md`](docs/LANGUAGE.md): the language as it is, every
   form and builtin, for someone writing programs in it. Still the
   calculator's until step 0 lands.
2. [`docs/DESIGN.md`](docs/DESIGN.md): the language and implementation as
   agreed. **(default)** marks something taken without discussion.
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
  special form or builtin, a change to the core rule (DESIGN.md), or
  anything marked (open). Give options and a recommendation. Record the
  outcome in `docs/DECISIONS.md` (who decided, why, what was rejected) and
  update `docs/DESIGN.md`.
- When a special form or builtin is added or changes, update
  `docs/LANGUAGE.md` (no tables there), and the guide where it shows it.
- Keep a working interpreter with passing tests at the end of every step
  (Ghuloum). Each step adds golden tests.
- **Examples bend to the language, not the other way round.** When an
  example needs something the runtime doesn't do, change the example, or
  leave it out; don't add to the language to make it pass.
- Verify a reported misbehavior against an independent implementation
  before calling it a bug. The Perl sketch is one, for the meta-model.
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
  model, by `docs/MODELS.md`; say so if they don't match, and escalate
  on its signals rather than pressing on.

## Code style

- [Indentation, line width, naming.]
- Pure functions over immutable data, association lists for environments,
  no classes in the implementation, so the reader, parser and evaluator
  can be ported to SMOL line by line (D14). The object model itself is SMOL
  source, not host code (D10).
- Host constraints: none yet. The calculator's C lessons (argument order,
  the clang bracket limit, a left shift of a negative value) are in git
  history at `4f6563e`, for the day a C target comes back.
- Comments explain why, not what.

## Toolchain

- Node 22.18 or later (it runs the compiler's TypeScript as it is, so
  the compiler uses only erasable syntax: no parameter properties, no
  enums). No C compiler is needed by the interpreter (D14); the
  calculator's C runtime goes when step 0 lands.
- [The machine cloud sessions develop on, once there is one.]
- `t/run.sh t/000-int.lang` checks the setup for the calculator; it
  changes with the interpreter (PLAN.md, step 0).

## Layout

| Path | |
|---|---|
| `bin/` | The driver |
| `compiler/src/` | One file per pass: reader, expander, checker, codegen, targets, errors |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | The calculator's C runtime, to go at step 0 |
| `lib/` | The prelude, compiled into every program, and the libraries a program asks for |
| `examples/` | Example programs; each with a `.expected` is a golden test |
| `docs/guide/` | The guide; its code blocks are golden tests too |
| `docs/prior-art/` | The Perl sketch the object model follows |
| `t/` | Golden tests: `NNN-name.ext` + `NNN-name.expected`; `run.sh`; `models/`; `referee/` (an evaluator of the language from the decisions, run over every test by `checks.py`; the builder of a step doesn't read it); `data/` |
| `build/` | Output (ignored) |

The layout is the template's. It changes at step 0.

## Commands

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`). A few seconds.
- `make unit`, `make golden`, `make checks`: one at a time.
  `t/run.sh t/000-int.lang` runs one golden test; `JOBS=1` runs them
  one at a time. `make models` reruns every model and writes its
  files; `make commits` checks the subjects since origin/main; `make
  hooks` installs the commit-msg hook.
- `make check`: `tsc --noEmit` (`npm install` once, for it).
- [Environment variables a SMOL program reads, once the runtime has any:
  the virtual clock, the heap cap, the scheduling seed. `t/run.sh` sets
  the ones the tests assume.]

The runtime prints the program's value, then a newline, and exits 0. A
fault is `fault: ...` on stderr and exit 1. The golden tests check
stdout and stderr together, plus `exit: N` when the status isn't 0.
This is the default proposed in `PLAN.md`, step 0, and isn't agreed.
