# Ditto

Ditto is a small, practical, dynamically typed imperative language
whose core rule is that every value is a value: lists and maps are
copied, never shared, so nothing you hold changes behind your back (D7).
Its compiler is TypeScript run directly by Node 22; it compiles a
`.ditto` file to C11 and links it with a runtime in C by `cc`. It stays
small: one file per program, no floats, no first-class functions, memory
never freed.

## Status

Design complete (D1 to D33, every form, error and fault in
`docs/LANGUAGE.md`; the six examples drafted in `docs/DESIGN.md`). Step 0
(the scaffold) is done: the whole lexer (every token, interpolation,
newline rule, every lexical error), and a parser, resolver, codegen and
C runtime for calls of `print` with int arguments; `bin/ditto`
`build`/`run`/`c` (D31); `t/run.sh` (parallel), `t/checks.py`, the
Makefile; golden tests 000 to 028 and 48 unit tests, all green under
`cc`, clang and the sanitizers. Builder defaults D34 to D37 are kept. Step 1
(expressions on ints, bools and nil) is done: the precedence table
without `else` and `in`, checked 64-bit arithmetic with truncating
`/` and `%` (D14), comparisons, `==`/`!=` on any pair (D18), short-circuit
`and`/`or`, every fault and the two compile errors of the plan;
`t/models/ints.py` writes golden tests 100 to 108, faults and errors
are 111 to 152 by hand; 75 golden tests and 62 unit tests, green under
`cc`, clang and the sanitizers. Builder default awaiting review: D38.
**Next:** step 2, variables and control flow.

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

- **In this run there is no person to ask** (`docs/briefs/design-and-build.md`).
  The design is decided in full; a builder who meets a silence takes
  the simplest default, records it in `docs/DECISIONS.md` as
  *(default)*, and flags it in its report. Never stop to ask.
- **Aggressively simple** is the main design rule. When a feature needs
  machinery, say so and offer to cut or change it.
- **Propose before building** any change to language semantics, a new
  special form or builtin, a change to the core rule (D7: every value is a value), or anything
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
- Update the Status section above as steps land.

## Code style

- TypeScript: 2 spaces, 100 columns, `camelCase` functions and
  variables, `PascalCase` types. Erasable syntax only (Node runs the
  `.ts` files by stripping types): no `enum`, no parameter properties,
  no namespaces; imports name the `.ts` file.
- The compiler's shape (D29): pure functions over plain data. AST nodes
  are objects with a `kind` string and a `pos` (`{line, col}`),
  discriminated unions, no classes. Self-hosting isn't a goal.
- C: C11, 2 spaces, `snake_case`, runtime functions prefixed `dt_`,
  generated names prefixed (`v_` variables, `f_` functions, `t` temps).
- Generated C computes every subexpression into a temporary in source
  order (D30). Never pass a variable and a call that sets it in one
  argument list, and never nest two calls that can fault or print in
  one expression: C doesn't order a call's arguments, and gcc and clang
  order them differently.
- Comments explain why, not what.

## Toolchain

- Node 22 (22.23 here; runs `.ts` directly), `cc` = gcc 13, clang 18,
  Python 3 for models and checks. Linux x86-64; the target is the host,
  so nothing is emulated.
- `make test` checks the setup: it should end with every golden test
  passing under each of the three compiler configurations.

## Layout

| Path | |
|---|---|
| `bin/` | The driver |
| `compiler/src/` | One file per pass: lexer, parser, resolve, codegen, errors, main |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | `ditto.h`, `ditto.c`: values, operators, builtins, faults, the allocator |
| `examples/` | Example programs; each with a `.expected` is a golden test |
| `t/` | Golden tests: `NNN-name.ditto` + `NNN-name.expected` (+ `.stdin`); `run.sh`; `checks.py`; `models/` |
| `build/` | Output (ignored) |

## Commands

- `make test`: unit tests, golden tests under `cc`, under `clang`, under
  clang's `-fsanitize=undefined,address`, and `t/checks.py`.
- `make unit`, `make golden`, `make golden-clang`, `make sanitize`,
  `make checks`: one at a time. `t/run.sh t/NNN-name.ditto` runs one
  golden test.
- `bin/ditto build FILE -o EXE`, `bin/ditto run FILE`, `bin/ditto c FILE`
  (D31). Exit 2 for a compile error or bad usage, 3 if the C compiler
  fails. `LANG_CC` picks the C compiler, `LANG_CFLAGS` adds flags.
- A compiled program reads no environment variables: there is no clock,
  randomness or concurrency to pin down. Its only input is standard
  input (`read()`), which a test supplies in `NNN-name.stdin`.

A program prints only what it `print`s. A fault prints
`path:line:col: fault: message` on standard error and exits 1; a
compile error prints `path:line:col: error: message` and exits 2. A
golden test compares stdout and stderr together, plus `exit: N` when not
0.
