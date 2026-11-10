# SMOL

SMOL is a small JavaScript-like language for personal experimentation with
bootstrapped object meta-models, after the Perl sketch in
`docs/prior-art/MiniMetaModel.pl`. It is not general-purpose and not for
speed: it exists to find the smallest runtime a bootstrapped meta-model
needs. It is a tree-walking interpreter in TypeScript, run by Node
(DECISIONS D14).

## Status

Steps 0 to 4 of [`docs/PLAN.md`](docs/PLAN.md) are done, and step 5 is split (D24). Step 0: a lexer, a parser, an evaluator and a runner for integers, strings, `nil`, `true`, `false`, names with sigils, `let`, and `//` comments. Step 1: function literals, calls with an arity check, lexical capture, and a body's value. Step 2: `catch`, a built-in that returns a caught fault's message as a string, or `nil`. Step 3: arrays and hashes, which are references and change in place, with their methods; `Array.new` and `Hash.new`; and the trailing `%name` parameter. Step 4: opaque instances, with the built-ins `create_opaque_instance`, `opaque_instance_id`, `opaque_instance_class`, `opaque_instance_attrs` and `create_class`, and method calls that walk the class chain. Step 5a: a prelude in `lib/prelude.smol` runs before every program and makes `Class` (object 1) and `Object` (object 2), with `opaque_instance_set_class`; a program's own objects start at 3 (D25). `create_class` makes instances of `Class` (D26). Golden tests 000 to 094 and 58 unit tests pass, and `make check` is clean. The decisions are D5 to D7 (the process), D8 to D13 (User: the scope, the object model and the syntax), D14 to D22 (User: the implementation and the open questions, each taken as recommended), D23 to D25 (defaults; D25 confirmed by the person), D26 (User: `create_class` returns instances of `Class`), and D27 (User: conditionals are methods of booleans, with a Boolean class). Steps 0 to 3 were built by a small-tier builder, and step 4 by a delegated larger builder, both as the person directed. Step 5a was built by the lead and reviewed by a larger model. **Next:** a decision on 5b (`Array` and `Hash` as classes, proposed in PLAN.md) and on the numbering that 5c's Boolean classes would need (PLAN.md, step 5). Nothing in 5b or 5c is built.

## Read first, in this order

1. [`docs/LANGUAGE.md`](docs/LANGUAGE.md): the language as it is, every
   form and builtin, for someone writing programs in it.
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
  on its signals rather than pressing on. The person can accept a
  mismatch, as with step 0; record it in the commit.

## Code style

- [Indentation, line width, naming.]
- Pure functions over immutable data, association lists for environments,
  no classes in the implementation (the one error class is the exception,
  since it plays the part of `raise`), so the passes can be ported to SMOL
  line by line (D14). The object model itself is SMOL source, not host code
  (D10).
- Host constraints: none yet. The calculator's C lessons (argument order,
  the clang bracket limit, a left shift of a negative value) are in git
  history at `4f6563e`, for the day a C target comes back.
- Comments explain why, not what.

## Toolchain

- Node 22.18 or later (it runs the TypeScript as it is, so the code uses
  only erasable syntax: no parameter properties, no enums). No C compiler
  is needed (D14).
- [The machine cloud sessions develop on, once there is one.]
- `npm install` once, for `make check`. `t/run.sh t/000-int.smol` checks
  the setup; it should end `1 tests, 0 failed`.

## Layout

| Path | |
|---|---|
| `bin/` | The driver: `node bin/smol.ts file.smol` |
| `compiler/src/` | The interpreter, one file per pass: `lexer.ts`, `parser.ts`, `eval.ts`, plus `ast.ts` and `errors.ts` |
| `compiler/tests/` | Unit tests: the parser's messages and positions, the evaluator |
| `lib/` | The prelude, when there is one (SMOL source) |
| `examples/` | Example programs; each with a `.expected` is a golden test |
| `docs/guide/` | The guide; its code blocks are golden tests too |
| `docs/prior-art/` | The Perl sketch the object model follows |
| `t/` | Golden tests: `NNN-name.smol` + `NNN-name.expected`; `run.sh`; `models/`; `referee/` (an evaluator of the language from the decisions, run over every test by `checks.py`; the builder of a step doesn't read it) |
| `build/` | Output (ignored) |

## Commands

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`). A few seconds.
- `make unit`, `make golden`, `make checks`: one at a time.
  `t/run.sh t/000-int.smol` runs one golden test; `JOBS=1` runs them one
  at a time. `make models` reruns every model and writes its files; `make
  commits` checks the subjects since origin/main; `make hooks` installs the
  commit-msg hook.
- `make check`: `tsc --noEmit` (`npm install` once, for it).

Programs print as LANGUAGE.md says: the value of the last statement, then a
newline, and exit 0. A syntax error or a fault exits 1. The golden tests
check stdout and stderr together, plus `exit: N` when the status isn't 0.
