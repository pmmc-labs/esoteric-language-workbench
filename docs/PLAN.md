# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. The budget is ten
steps, step 0 and the examples included (the brief); steps 0 to 8 are
planned and step 9 is held in reserve for friction the examples show.

**Progress:** design done; step 0 done (scaffold, 28 golden tests, 48 unit
tests); step 1 done (expressions on ints, bools and nil; 75 golden tests,
62 unit tests); step 2 done (variables and control flow; 151 golden tests,
88 unit tests); step 3 done (functions; 216 golden tests, 105 unit
tests); step 4 next.

Read [`DESIGN.md`](DESIGN.md) and [`LANGUAGE.md`](LANGUAGE.md) first.
`LANGUAGE.md` gives every message and position; a builder that finds a
silence takes a default, records it in `DECISIONS.md` as *(default)*,
and flags it in the report.

## How each step is built

- Tests are numbered by step: step k uses `t/k00-...` to `t/k99-...`
  (D33).
- First the model and the tests, committed red (`Step k: tests (red)`),
  then the code, committed green (`Step k: ...`). A test whose output is
  computed (arithmetic, loops, anything longer than a few lines to check
  by eye) gets its expected file from the step's model in `t/models/`;
  compile errors, faults and short programs may be written by hand.
- A model is a Python program that writes test programs and their
  expected outputs from the definition in `LANGUAGE.md`, never by
  running the compiler. Its docstring lists each command that writes a
  file, one per line, so `t/checks.py` can rerun it (see
  `t/models/README.md`).
- The step ends with `make test` green: unit tests, golden under `cc`,
  under `clang`, under clang's sanitizers, and `t/checks.py`.
- `LANGUAGE.md` is updated if anything landed differently, the progress
  line here and `CLAUDE.md`'s Status gain a sentence, and the step's
  text below gets **(done)** and a note of any difference.

## Layout

```
bin/ditto                 driver (a node script)
compiler/src/             lexer.ts parser.ts resolve.ts codegen.ts errors.ts main.ts
compiler/tests/           node --test unit tests, per pass
runtime/ditto.h ditto.c   the runtime
examples/                 NAME.ditto + NAME.expected (+ NAME.stdin)
t/                        NNN-name.ditto + .expected (+ .stdin); run.sh; checks.py; models/
build/                    output, ignored
Makefile
```

## Steps

### 0. Scaffold **(done)**

Landed as planned. Differences: tests 000 to 028 (no model: every output
is a few lines, written by hand); the runtime also has a unit test
(`compiler/tests/runtime.test.ts`) that links a hand-written C main, since
no Ditto program can fault yet; the golden runs under `cc` and clang add
`-Wall -Wextra -Werror` (D37); defaults D34 to D36.

- `Makefile` with `test`, `unit`, `golden`, `golden-clang`, `sanitize`,
  `checks` (D33). `sanitize` is clang with
  `-fsanitize=undefined,address -fno-sanitize-recover=all -g`.
- `bin/ditto` and `main.ts` with `build`, `run`, `c` (D31).
- The whole lexer (every token in `LANGUAGE.md`, interpolation, the
  newline rule's lexer half, every lexical error), with unit tests of
  tokens, positions and errors.
- The parser, resolver and codegen for a program of calls to `print`
  with int literal arguments, one per line. The error formats (D29),
  `expected X, found Y`, and `unknown function f`.
- The runtime: `Value`, the allocator (D26), printing ints, `fault`
  (D28) with standard output flushed first.
- `t/run.sh`: compile with `bin/ditto build`, run with the `.stdin`
  file or empty input, compare stdout and stderr together with
  `.expected`, plus `exit: N` when not 0; a compile error's output is
  the compiler's standard error and `exit: 2`. It takes test paths, or
  runs every `t/*.ditto` and `examples/*.ditto`; it runs tests in
  parallel and prints one line per failure and a count.
- `t/checks.py`: every test has an `.expected`; every model's commands
  rerun and their files compared.
- Tests 000 to 0xx: `print(42)`, several prints, `print()`,
  `print(1, 2, 3)`, the largest int, and by hand each lexer error and an
  `expected X, found Y`.
- Leaves out: every other expression.
- **Size:** medium.

### 1. Expressions on ints, bools and nil **(done)**

Landed as planned. Differences: tests 100 to 152 (the model writes 100 to
108; faults 111 to 133 and compile errors 140 to 152 are by hand, with
positions counted from the source); test 027 now expects `expression
statement must be a call` (D38); default D38. The runtime writes its
overflow checks out instead of using `__builtin_*_overflow`, an extension.

- `true false nil`, prefix `-` and `not`, `* / % + -`, comparisons on
  ints, `==`/`!=` on these types, `and`/`or` with short-circuit,
  parentheses, the precedence table (without `else` and `in`).
- Faults: `integer overflow`, `division by zero`,
  `cannot use + on bool and int`, `cannot use and on int` and the
  others for these types. Compile errors: `comparisons do not chain`,
  `expression statement must be a call`.
- Printing `true false nil`.
- Model `t/models/ints.py`: generated expressions over edge values
  (0, ±1, ±7, the extremes), computed with Python ints under D14's rules
  (truncation, overflow as a fault), several tests of many `print`
  lines, plus one test per fault kind.
- Leaves out: variables (a fault test is one `print` that faults).
- **Size:** medium.

### 2. Variables and control flow **(done)**

Landed as planned. Differences: tests 200 to 278 (the model writes 200 to
210, including three random programs run through a small interpreter of
the statement rules; faults 211 to 229, semantics 230 to 236 and compile
errors 240 to 278 are by hand); test 025 now expects `expression
statement must be a call` (a bare name is an expression now); parse
errors, scope details and the order of evaluation in `for` headers are
defaults D39 and D40; a builtin used as a value is already `functions
are not values`. The assignment target is a variable plus a list of steps
(empty until step 5), and codegen evaluates index temporaries, loads,
right-hand side, operator, store in that order, so step 5 fills in the
path cases.

- `let`, assignment to a variable, compound assignment on variables,
  blocks and scopes (D12), `if`/`else if`/`else` (with `else` on the
  next line), `while`, `for` over `a..b` and `a..=b`, `break`,
  `continue`, `;`.
- Errors: `unknown variable x`, `x is already declared`,
  `cannot assign to this`, `break outside a loop`,
  `continue outside a loop`. Faults: `condition must be a bool, got
  int`, `range bounds must be ints, got bool`, `cannot iterate over int`
  (a `for` over an int; the other types arrive later).
- Model `t/models/loops.py`: loops whose output is computed (sums,
  Collatz lengths, primes by trial division, FizzBuzz-like branching,
  `break`/`continue`, a range ending at the largest int).
- **Size:** medium.

### 3. Functions **(done)**

Landed as planned. Differences: tests 300 to 380 (the model writes 300 to
310, including two random programs of generated functions run through a
small interpreter; faults 311 to 319, semantics 326 to 329 and compile
errors 340 to 380 are by hand); test 278 now expects `expected a name,
found newline` for a bare `fn`; default D41. The runtime has `dt_enter` and
`dt_leave` for the depth counter, with a unit test; the 1000-deep call
test (308) passes under the sanitizers.

- `fn`, calls, `return`, hoisting, arity (D13), parameters as variables,
  the depth limit (D28), recursion.
- Errors: `unknown function f`, `f takes 2 arguments, got 3`,
  `duplicate function f`, `print is a builtin`, repeated parameter,
  `functions are defined at the top level`, `return outside a function`,
  the top-level-variable message, `functions are not values`. Fault:
  `stack overflow (more than 1000 nested calls)`, and 1000 nested calls
  succeeding.
- Model `t/models/functions.py`: gcd, factorial, Fibonacci, Ackermann
  for small arguments, mutual recursion, a parameter reassigned inside
  the function not changing the caller's variable.
- **Size:** medium.

### 4. Strings

- String literals with escapes and interpolation (the parser and
  codegen half: the lexer has them since step 0), `+`, comparisons,
  indexing, `in` and `not in` on strings, `for` over a string, and the
  builtins `str len int lower upper slice read fail` on strings and
  ints. (`words`, `split` and `join` make or take lists, so they land
  in step 5.)
- Faults per `LANGUAGE.md`: index out of range on strings, `not a
  number`, builtin type errors, `split: empty separator`, `fail`.
- Model `t/models/strings.py`: generated strings with escapes and
  interpolation, comparisons, indexing, `int` round trips, `lower` and
  `upper`, `slice`; and a `.stdin` test for `read()`.
- **Size:** large.

### 5. Lists and the core rule

- List literals, indexing, `+`, `==` and `<`, `in`, `for` over a list,
  assignment to a path of list indexes (D7) and compound assignment on
  one, `len`, `slice`, `sort`, `split`, `join`, `words`, and the
  printed form of lists with nested strings quoted (D24).
- The core rule's tests: `let b = a` then changing `b`; an argument
  changed inside a function; a list stored in a list then changed; a
  loop over a list that changes it; a list built with `+=` in a loop.
- Faults: index out of range and type faults for lists,
  `cannot assign into string`, `cannot iterate over` for the remaining
  types, `cannot use < on int and string` met inside lists and inside
  `sort`.
- Model `t/models/lists.py`: Python lists with `copy.deepcopy` at every
  assignment, argument and store, which is D7's definition; insertion
  sort, quicksort, nested updates, lexicographic comparison, and the
  core rule's cases above.
- **Size:** large.

### 6. Maps

- Map literals (key forms, `duplicate key`, the bad-key error), indexing,
  `.name`, setting a key (in place if present, at the end if not), path
  assignment mixing list indexes, keys and fields, compound assignment
  on a path, `for` over keys, `in`, equality regardless of order, `len`,
  `keys`, `remove`, the printed form.
- Faults: `missing key`, `map key must be an int or a string, got
  list`, `cannot use .name on list`.
- Model `t/models/maps.py`: Python dicts (insertion-ordered) with deep
  copies as in step 5; word frequencies, an inventory, nested records,
  the core rule's cases for maps.
- **Size:** medium.

### 7. `else`

- The operator (D20): parsing at its precedence, the resolver's
  `else needs a lookup on its left`, codegen that gives each lookup
  written in the left operand a branch to the fallback on a miss
  (index, field, `int`), nesting, interpolation inside, and misses in
  called functions *not* caught.
- Model `t/models/fallback.py`: lookups that hit and miss, chains
  `a else b else c`, precedence cases (`m[k] else 0 + 1`), defaults that
  are themselves lookups.
- **Size:** medium.

### 8. Examples

- `examples/` holds the six programs in `DESIGN.md` (FizzBuzz,
  recursion, sorting, word count with a `.stdin`, route finding, the
  ledger), each a golden test, with expected outputs from
  `t/models/examples.py`, which computes each program's output in
  Python from the definition.
- An example that reads awkwardly is reported, not worked around in
  the language (D9).
- `LANGUAGE.md` checked against what landed; `README.md` gets a section
  on Ditto.
- **Size:** medium.

### 9. Reserve

Held for one step of friction the examples or reviews show, by
decision. Unused if there's none.

## Example-port table

| Example | Needs | Status |
|---|---|---|
| fizzbuzz | steps 1, 2 | waits on step 8 |
| recursion | steps 3, 4 (interpolation) | waits on step 8 |
| sorting | step 5 | waits on step 8 |
| word count | steps 6, 7 | waits on step 8 |
| route finding | steps 6, 7 | waits on step 8 |
| ledger | step 6 | waits on step 8 |
