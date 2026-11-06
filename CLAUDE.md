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

**Steps 0 to 2 of [`docs/PLAN.md`](docs/PLAN.md) are done**: a reader
with positions, a program of one expression compiled to C and linked
with `runtime/rt.c` (D2), integers of 63 bits (D4), the five operators
on two arguments each (D3), division C's way (D5), faults ending the
program (D6; golden tests 000, 001, and 010 to 015 from
`t/models/arith.py`), compile errors as unit tests (D7), and the
mechanical checks, `t/checks.py` (D8, D10). Step 2 (D11 to D14):
`#true` and `#false` as immediates tagged `11` (golden tests 021, 023,
024), the six comparisons on integers, `==` and `!=` on any values
(020, from `t/models/compare.py`), and `if`, the test checked to be a
boolean, only the taken branch run (022); built by Haiku 5.5 on a step
marked medium. Step 3 (D15 to D17): `bit/and`, `bit/or` and `bit/xor`,
and the shifts `bit/shl` (checked as a multiplication, so `overflow`)
and `bit/shr` (floor division), a count outside 0 to 62 faulting `bad
shift`; golden tests 030 to 036 from `t/models/bits.py`, which Haiku 5.5
wrote, the model being the step's large part, and committed red before
the code (the model's fold is a balanced tree, for clang's bracket
limit). Not agreed, and avoided by the tests: which fault reports when a
call could fault two ways (a boolean value and a bad count, say; the
runtime checks the boolean first). **Next:** nothing agreed; step 4 is
still a placeholder in the plan, and the calculator grows only when a
step of the process needs it.

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
- A commit that touches the implementation names its decision or plan
  step in the subject (`make hooks` installs the check).
- At the start of a step, compare the step's **Size** line with your own
  model, by `docs/MODELS.md`; say so if they don't match, and escalate
  on its signals rather than pressing on.

## Code style

- [Indentation, line width, naming.]
- [The compiler's shape. a64-slight's rule: pure functions over immutable
  s-expressions, association lists for environments, no classes, so it
  can be ported to the language itself line by line. Pick the shape that
  makes self-hosting a translation rather than a rewrite.]
- [Constraints the host platforms impose, as you learn them. Name the
  symptom and the fix, so the lesson isn't relearned.] C doesn't order
  a call's arguments: never pass a variable and a call that sets it in
  the same argument list (`runtime/rt.c`'s arithmetic read `r` before
  `__builtin_add_overflow` set it under clang, and gcc hid it). The
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

- Node 22.18 or later (it runs the compiler's TypeScript as it is, so
  the compiler uses only erasable syntax: no parameter properties, no
  enums) and a C compiler as `cc`.
- [The machine cloud sessions develop on, and how a target that isn't
  native runs there (cross-compile and an emulator, say), once there is
  one.]
- `t/run.sh t/000-int.lang` checks the setup; it should end
  `1 tests, 0 failed`.

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

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`). A few seconds.
- `make unit`, `make golden`, `make checks`: one at a time.
  `t/run.sh t/000-int.lang` runs one golden test; `JOBS=1` runs them
  one at a time. `make models` reruns every model and writes its
  files; `make commits` checks the subjects since origin/main; `make
  hooks` installs the commit-msg hook.
- `make check`: `tsc --noEmit` (`npm install` once, for it).
- `make sanitize`: the golden tests under UBSan and ASan, not part of
  `make test` (it needs clang's sanitizer runtime).
- `node bin/langc.ts -o out file.lang`: compile and link. It writes
  `out.c` next to `out`. Exit codes: 0 ok, 1 compile error, 2 usage or
  toolchain error, or a file it can't read or write; a fault in the
  compiler itself is `langc: internal error: ...` with Node's stack.
  `LANG_CC` overrides the C compiler.
- [Environment variables a compiled program reads: the virtual clock,
  the heap cap, record and replay, the scheduling seed, the GC stress
  and poison knobs. `t/run.sh` sets the ones the tests assume.]

The runtime prints the program's value, then a newline, and exits 0. A
fault is `fault: ...` on stderr and exit 1. The golden tests check
stdout and stderr together, plus `exit: N` when the status isn't 0.
