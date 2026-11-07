# [name]

[One paragraph: what the language is, what it runs on, what the compiler
is written in and what it should become. Two or three sentences.]

## Status

[A running paragraph of what's built, by plan step and decision number,
updated every time a step lands. This is the handoff between sessions:
a new session reads it before anything else. Keep it as one paragraph
per era, dense, with golden test numbers and `Dn` references, so a
claim can be checked against a test and a decision. Say what's **Next**
at the end, and what's a candidate but not agreed.]

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
- Keep a working compiler with passing tests at the end of every step
  (Ghuloum). Each step adds golden tests.
- **Examples bend to the language, not the other way round.** When an
  example needs something the compiler or runtime doesn't do, change the
  example, or leave it out; don't add to the language to make it pass.
- Verify a reported misbehavior against an independent implementation
  before calling it a bug.
- When a change moves an expected output that a model in `t/models/`
  wrote, rerun the model; don't patch the file. A patched file leaves the
  model stale, and the next change finds the two disagreeing.
- When editing with scripts, assert that each replacement matched.
- Test timing uses a virtual clock; real time is never used in tests.
- Update the Status section above as steps land.

## Code style

- [Indentation, line width, naming.]
- [The compiler's shape. a64-slight's rule: pure functions over immutable
  s-expressions, association lists for environments, no classes, so it
  can be ported to the language itself line by line. Pick the shape that
  makes self-hosting a translation rather than a rewrite.]
- [Constraints the host platforms impose, as you learn them. Name the
  symptom and the fix, so the lesson isn't relearned.]
- Comments explain why, not what.

## Toolchain

- [Primary machine: compiler, versions.]
- [The machine cloud sessions develop on, and how a target that isn't
  native runs there (cross-compile and an emulator, say).]
- [One command that checks the setup, and what it should print.]

## Layout

| Path | |
|---|---|
| `bin/` | The driver |
| `compiler/src/` | One file per pass: reader, expander, checker, codegen, targets, errors |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | [C, assembly, whatever the language runs on] |
| `lib/` | The prelude, compiled into every program, and the libraries a program asks for |
| `examples/` | Example programs; each with a `.expected` is a golden test |
| `docs/guide/` | The guide; its code blocks are golden tests too |
| `t/` | Golden tests: `NNN-name.ext` + `NNN-name.expected`; `run.sh`; `models/`; `data/` |
| `build/` | Output (ignored) |

## Commands

- `make test`: everything, for every target. [How long it takes.]
- `make unit`, `make golden`, ...: one at a time. `t/run.sh t/NNN-name.ext`
  runs one golden test.
- [The compiler's command line, its exit codes.]
- [Environment variables a compiled program reads: the virtual clock,
  the heap cap, record and replay, the scheduling seed, the GC stress
  and poison knobs. `t/run.sh` sets the ones the tests assume.]

[How the runtime reports a program's value, a fault, a deadlock, and the
exit code for each; what a golden test compares (stdout and stderr
together, plus `exit: N` when not 0).]
