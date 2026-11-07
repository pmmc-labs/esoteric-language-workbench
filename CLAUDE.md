# Strata

Strata is a small imperative language in which every variable is a
history: a write lays a new value on top, `@` reads the variable as it
was, and nothing is ever overwritten. Its compiler is TypeScript run by
Node 22, emitting C that `cc` links with a small C runtime; it should
become a language in which ordinary small programs (FizzBuzz, sorting,
text) read plainly and the history makes some of them shorter.

## Status

**Design** (D1 to D32): the whole language is decided in `docs/DESIGN.md`,
`docs/DECISIONS.md` and `docs/LANGUAGE.md`; seven steps in
`docs/PLAN.md`. **Step 0** (scaffold) is built: `bin/strata build|run`
(D30), the Makefile with `unit`, `golden`, `golden-clang`, `sanitize` and
`checks`, `t/run.sh`, `t/checks.py`, the arena and `strata_fault` in
`runtime/` (D23, D26), the full-token-set lexer with every lexical error
of D24 unit-tested (integer range checked in the lexer, D34), and a
parser, resolver and codegen for `print INTEGER` only, whose values are
already one-layer histories (D11, D35); golden tests `000` to `005` pass
under gcc, clang and clang with `-fsanitize=undefined,address`. Parse
errors read `expected expression, found 'x'` (D33). **Next:** step 1,
numbers (D19, D20, D25), tests `100` up.

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
  special form or builtin, a change to the core rule (D7: every name is a history), or anything
  marked (open). Give options and a recommendation. Record the outcome in
  `docs/DECISIONS.md` (who decided, why, what was rejected) and update
  `docs/DESIGN.md`. In this run there is no person: a builder writes any
  default it has to take as a *(default)* decision and flags it in its
  report; the designer rules on it at review.
- When a special form or builtin is added or changes, update
  `docs/LANGUAGE.md` (no tables there).
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

- TypeScript: 2-space indent, lines under 100, camelCase, `.ts`
  imports with the extension. Erasable syntax only (Node strips types):
  no enums, no parameter properties, no namespaces.
- The compiler is pure functions over plain-object ASTs (tagged unions
  with a `k` field), no classes, one file per pass (D29). Compile errors
  are thrown as `{line, col, msg}` and caught once in `main.ts`.
- C: C11, no extensions, snake_case, runtime names prefixed `strata_`.
  Generated code puts every subexpression in a fresh temporary, in
  source order (D25). Never pass a variable and a call that sets it in
  one argument list: C doesn't order arguments, and gcc and clang differ.
- Terse where the code is simple, spelled out where it isn't.
- Comments explain why, not what.

## Toolchain

- Node 22 (v22.23 here; type stripping on by default), gcc 13 as `cc`,
  clang 18. One machine: the cloud x86-64 Linux box; no other target.
- `make tools` prints the three versions.

## Layout

| Path | |
|---|---|
| `bin/` | The driver |
| `compiler/src/` | One file per pass: reader, expander, checker, codegen, targets, errors |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | `strata.h`, `strata.c`: arena, histories, arithmetic, strings, faults |
| `examples/` | Example programs; each with a `.expected` is a golden test |
| `t/` | Golden tests: `NNN-name.strata` + `NNN-name.expected` (step n's are `n00` up, D31); `run.sh`; `checks.py`; `models/` |
| `build/` | Output (ignored) |

## Commands

- `make test`: unit, golden (gcc), golden-clang, sanitize, checks.
- `make unit`, `make golden`, `make golden-clang`, `make sanitize`,
  `make checks`: one at a time. `t/run.sh t/NNN-name.strata` runs one
  golden test (`LANG_CC`, `LANG_CFLAGS` pass through).
- `bin/strata build FILE -o OUT`: exit 0, 2 on a compile error
  (`error at L:C: message` on stderr), 3 if `cc` fails (a compiler bug).
  `bin/strata run FILE` builds into `build/` and runs it (D30).
- A compiled program reads no environment and no input (D28).

A program prints only through `print`/`write`, exits 0 at its end, and on
a fault flushes stdout, prints `fault at L:C: message` to stderr and exits
1 (D23). A golden test compares stdout and stderr together, plus a line
`exit: N` when N isn't 0.
