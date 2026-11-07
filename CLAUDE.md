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
Step 2 (variables and control flow) is done: `let`, assignment and
compound assignment to a variable (the target is a variable plus a list
of steps, empty until step 5), block scopes without shadowing (D12),
`if`/`else if`/`else` (with `else` on the next line), `while`, `for` over
`a..b` and `a..=b` (a counter that cannot overflow at the largest int),
`break`, `continue`, `;`, the condition, range-bound and iteration
faults, and the scope errors; `t/models/loops.py` writes golden tests 200
to 210 (fixed algorithms and three random programs checked against a
small interpreter), faults 211 to 229, semantics 230 to 236 and errors
240 to 278 are by hand; 151 golden tests and 88 unit tests, green under
`cc`, clang and the sanitizers. Builder defaults D39 and D40 are kept.
Step 3 (functions) is done: `fn` at the top level (parameter lists like
argument lists, D34), hoisted and of fixed arity, calls with the arity
error, `return` (bare or with a value, falling off the end gives `nil`),
parameters as copies, the depth limit of 1000 nested calls (`dt_enter` and
`dt_leave` around each call of a user function, D28), and the errors for
duplicate and builtin names, repeated parameters, `fn` below the top level,
`return` outside a function, top-level variables seen from a function and
functions used as values; `t/models/functions.py` writes golden tests 300
to 310 (gcd, factorial, Fibonacci, Ackermann, mutual recursion, parameter
copies, hoisting, `return` shapes, 1000 nested calls, two random programs
checked against a small interpreter), faults 311 to 319, semantics 326 to
329 and errors 340 to 380 are by hand; 216 golden tests and 105 unit
tests, green under `cc`, clang and the sanitizers. Builder default
awaiting review: D41.
Step 4 (strings) is done: string literals with escapes and
interpolation (each `{expr}` parsed on its own, parts evaluated left to
right and joined by `dt_interp`), strings as byte sequences with a length
(NULs from `read()` are ordinary bytes), `+`, the four orderings and
`==`, indexing (`dt_try_index` reports a miss, `dt_index` faults on it,
which is the shape step 7's `else` needs), `in` and `not in`, `for` over a
string, and the builtins `str len int lower upper slice read fail`; the
faults and errors of the plan; `t/models/strings.py` writes golden tests
400 to 410 (escapes, interpolation, comparisons, indexing, `in`, `int`
round trips, case and slice, two `read()` tests with `.stdin`, text
algorithms, a random program), faults 411 to 455, semantics 460 to 470
and errors 480 to 497 are by hand; 301 golden tests and 128 unit tests,
green under `cc`, clang and the sanitizers. Builder default awaiting
review: D42.
Step 5 (lists and the core rule) is done: list literals (items any
expressions, trailing comma, broken across lines), indexing, `+`, `==`
and the orderings (lexicographic, item pairs faulting as `<` would), `in`,
`for` over a list, assignment and compound assignment to a path of index
steps (keys evaluated, then the current value for a compound one, then the
right-hand side; the spine rebuilt from the inside out with `dt_set_index`,
D7), and the builtins `sort split join words` and `slice` on lists; the
printed form of lists with nested strings quoted (D24); the faults and
errors of the plan; `t/models/lists.py` writes golden tests 500 to 511
(literals, indexing, comparison pools, `in`, loops, `sort`, the DESIGN.md
sorts, text builtins, path updates, the core rule's cases, two random
programs against Python lists deep-copied at every store), faults 512 to
559, semantics 560 to 574 and errors 575 to 597 are by hand; 399 golden
tests and 149 unit tests, green under `cc`, clang and the sanitizers.
Builder default awaiting review: D43.
Step 6 (maps) is done: map literals (a key is a name, a string without
interpolation or an int with an optional `-`; `duplicate key` and the bad-key
error; newlines ignored between the braces), indexing and `.name` (a miss is
`missing key "qty"`), setting a key (in place if present, at the end if not),
paths mixing index and field steps with compound assignment, `==` regardless
of order, `in` on keys, `for` over keys, `len`, `keys`, `remove`, the printed
form `{"a": 1, 3: "x"}`; the faults and errors of the plan; maps are immutable
arrays of keys and values like lists (D7, D27) and every lookup keeps its try
form for `else`; `t/models/maps.py` writes golden tests 600 to 611 (Python
dicts deep-copied at every store, two random programs), faults 612 to 649,
semantics 650 to 666 and errors 670 to 699 are by hand; 496 golden tests and
169 unit tests, green under `cc`, clang and the sanitizers. Builder default
awaiting review: D44.
Step 7 (`else`) is done: `a else b` at its precedence (tighter than every
binary operator, looser than prefix minus, left-associative), the resolver's
`else needs a lookup on its left: an index, a field or int()` at the `else`,
and codegen with a stack of `goto` labels: a lookup written in a left operand
(index, field, `int`, including in index expressions, arguments, literals and
interpolations there) calls its `dt_try_` form and jumps to the innermost
`else`'s fallback on a miss, while a called function's body, compiled with no
labels, never catches (D20, D30); no runtime change; `t/models/fallback.py`
writes golden tests 700 to 709 (every lookup hitting and missing, chains,
precedence minimal and parenthesised, laziness and order, word count, routes
and config parsing with `.stdin`, `else` in every statement, two random
programs against a Python evaluator), faults 710 to 731, semantics 740 to 749
and errors 760 to 784 are by hand; 563 golden tests and 173 unit tests,
green under `cc`, clang and the sanitizers. Builder default awaiting review:
D46. **Next:** step 8, the examples.

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
