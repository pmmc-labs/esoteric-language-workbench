# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Seven steps,
inside the brief's budget of ten.

**Progress:** design done; step 0 built (D33 to D35). Next: step 1.

Read [`DESIGN.md`](DESIGN.md), [`LANGUAGE.md`](LANGUAGE.md) and the
decisions each step cites first. Every step: write the model (if any)
and the golden tests first and commit them red (D32); then build until
`make test` is green under gcc, clang and the sanitizers; update
`LANGUAGE.md` if anything there moved, the progress line here, and
`CLAUDE.md`'s Status; commit with the step in the subject.

## Proposed layout

```
bin/strata                 driver (shell): build, run (D30)
compiler/src/lexer.ts      bytes to tokens
compiler/src/parser.ts     tokens to AST
compiler/src/resolve.ts    names, arity, return placement
compiler/src/codegen.ts    AST to C, temporaries in source order
compiler/src/errors.ts     compile errors
compiler/src/main.ts       command line
compiler/tests/*.test.ts   unit tests, node --test
runtime/strata.h, strata.c the runtime
examples/NAME.strata       example programs, each with NAME.expected
t/NNN-name.strata          golden tests, NNN-name.expected
t/run.sh                   run one golden test
t/checks.py                mechanical checks (models, pairs)
t/models/*.py              models
Makefile
```

## Steps

### 0. Scaffold (done)

- `bin/strata`, `Makefile`, `runtime/strata.{h,c}` with the arena
  (D26) and `strata_fault` (D23), linked into every program.
- The lexer for the whole token set (D16, D21: names, keywords,
  integers, strings with escapes, every operator and punctuation,
  `;` comments) with line and column, and its unit tests, including
  each lexical error of D24.
- A parser, resolver and codegen for exactly one statement form,
  `print INTEGER`, any number of them: `print 42` compiles to a binary
  that prints `42`. Anything else is a parse error in D24's format.
- `t/run.sh FILE`: compile with `bin/strata build`; on a compile error
  the output is the compiler's stderr plus `exit: 2`; otherwise run the
  binary with stdout and stderr together (`2>&1`), adding `exit: N` on a
  line of its own when N isn't 0 (after a newline, if the output didn't
  end with one); diff against `.expected`. It runs `.strata` files from
  `t/` and `examples/`, and builds under `build/t/`.
- `t/checks.py`: every `.strata` in `t/` and `examples/` has a
  `.expected`; every model's docstring commands (lines starting
  `python3 t/models/`) are rerun into a temporary file and compared with
  the committed file. Exit 1 on any mismatch.
- `make unit`, `make golden` (cc), `make golden-clang`
  (`LANG_CC=clang`), `make sanitize` (clang with
  `-fsanitize=undefined,address -fno-sanitize-recover=all -g`),
  `make checks`, and `make test` doing all five; `make tools` prints
  the Node, cc and clang versions.
- Golden tests: `000-print-42`, `001-print-several` (several prints,
  one line each), `002-zero` (`print 0`), `003-comment` (comments and
  blank lines), `004-parse-error` (`print` with no operand: `error at
  ...: expected ...`, `exit: 2`), `005-bad-char` (`unexpected
  character`).
- Leaves out: every other statement and expression.
- **Size:** medium.

### 1. Numbers: arithmetic, comparison, logic, write

- Expressions on numbers: `+ - * / %`, prefix `-`, the six comparisons,
  `and`, `or`, `not`, parentheses, with D19's checks and D20's 1/0
  results and short-circuit; `write`; the full precedence of
  `LANGUAGE.md`; `integer literal out of range` (D19). Every
  subexpression into a C temporary in source order (D25).
- Values in the runtime are already histories (D11): the literal and
  every result is a one-layer history; operators take tops. Strings
  don't exist yet, so type faults wait for step 5.
- Model `t/models/arith.py`: generates a program of many `print`
  lines over edge values (0, ±1, ±7, ±2, the 64-bit limits, values near
  overflow) for every operator, and its expected output from Python
  integers with C's truncating division, with the overflow cases
  written as separate fault tests. Faults are one per test since a
  fault ends the program.
- Golden tests: `100-arith` (the model's), `101-precedence` (by hand),
  `102-compare-logic`, `103-short-circuit` (a right side that would
  fault, `1 / 0`, is not evaluated), `104-write`, `105-overflow-add`,
  `106-overflow-mul`, `107-overflow-neg` (prefix minus on a computed
  minimum), `108-div-zero`, `109-mod-zero`, `110-div-min-by-minus-one`,
  `111-literal-range` (compile error), `112-chained-compare` (compile
  error), and fault-position checks within them.
- Leaves out: variables, strings.
- **Size:** medium.

### 2. Histories: let, write, @, #, history literals

The core rule (D7, D11 to D15).

- `let`, `<-`, blocks are not yet needed (top level only), `#`, `@`,
  `[...]`, names, `unknown variable`, `x is already declared`, the
  `empty history` fault (reading the top of `[]`, `print []`, `x <- []`),
  `@ out of range`.
- The runtime's history: `{atom, below, depth}` layers from the arena,
  NULL for empty (DESIGN.md, "Values and memory").
- Golden tests: `200-let-print`, `201-write-grows` (`#` after writes),
  `202-at-past` (`@0`, `@1`, `@(#x)` then `#` of it is 0),
  `203-let-shares` (`let y = x` keeps `x`'s past; `let y = x + 0`
  doesn't), `204-literal-order` (`[1,2,3]` top is 3, `@2` is 1),
  `205-at-chain` (`x@1@1` = `x@2`), `206-empty-top` (fault),
  `207-at-range` (fault, both sides: negative and beyond),
  `208-write-empty` (fault at `<-`), `209-unknown-variable`,
  `210-redeclare`, `211-long-history` (a 10000-write history, its depth
  and its oldest layer: proves the arena chains chunks).
- Leaves out: blocks (step 3), functions (step 4).
- **Size:** medium.

### 3. Control: if, else, while, blocks

- `if`/`else if`/`else`, `while`, blocks with D14's scoping (a `let`
  in a block is visible to its end; redeclaring a name from an
  enclosing block is an error; a `let` in a loop body is fresh each
  round).
- Golden tests: `300-if-else`, `301-else-if`, `302-while-count`,
  `303-nested-loops`, `304-block-scope` (a name from a finished block
  is `unknown variable`), `305-let-in-loop` (each round's variable has
  depth 1), `306-shadow-error` (redeclare inside a block),
  `307-condition-fault` (`if []`: `empty history` at `if`).
- Leaves out: functions, strings.
- **Size:** small.

### 4. Functions

- `fn`, calls as expressions and as statements, `return`, hoisting,
  parameters as whole histories (D18), the empty result, the depth
  limit (D27), and the errors `unknown function`, `f is already
  defined`, `f takes N arguments, given M`, `return outside a
  function`, `unknown variable` for a main-program name used in a
  function. Builtin names are reserved now (`f is a builtin`) even
  though the builtins arrive in step 5.
- Golden tests: `400-call`, `401-recursion` (factorial of 20, by
  hand), `402-hoisting`, `403-param-history` (callee reads `x@1` of
  the caller's variable), `404-param-write-private` (callee's write is
  invisible to the caller), `405-return-list` (a function building and
  returning a history), `406-no-return` (`#f()` is 0),
  `407-arg-order` (arguments evaluated left to right, shown by a fault
  in the first of two faulting arguments), `408-depth-limit` (10000
  nested calls succeed, 10001 fault), `409-arity`, `410-unknown-fn`,
  `411-return-outside`, `412-no-globals`, `413-builtin-name`.
- Leaves out: strings, closures (never).
- **Size:** medium.

### 5. Strings

- String literals and escapes in codegen, `+` concatenation, bytewise
  comparisons, `len`, `at`, `str`, printing strings, and every type
  fault of D21: `expected a number`, `expected a string`, `mismatched
  types` for `+` and comparisons, strings as conditions and `and` /
  `or` / `not` operands, a string `@` index, `at` out of range.
- Golden tests: `500-hello`, `501-escapes`, `502-concat`,
  `503-compare` (bytewise, prefix, equal), `504-len-at`, `505-str`
  (including the minimum number, computed), `506-mismatch-add`,
  `507-mismatch-compare`, `508-expected-number`,
  `509-expected-string`, `510-at-range`, `511-string-condition`,
  `512-unknown-escape` (compile error), `513-unterminated` (compile
  error), `514-string-history` (a history of strings, read with `@`).
- Leaves out: character codes, parsing numbers (D21).
- **Size:** medium.

### 6. Examples

- `examples/fizzbuzz.strata` (1 to 100; expected from a model,
  `t/models/fizzbuzz.py`), `examples/factorial.strata` (recursive,
  1! to 20!, model), `examples/sort.strata` (insertion sort by
  recursion on `@1`, of a literal list of at least 12 numbers with
  duplicates and negatives, printed ascending one per line; model),
  `examples/reverse.strata` (reverse words and count a letter, using
  that a history read from the top is the reverse of the order it was
  written; by hand), `examples/history.strata` (the core rule shown
  off: Fibonacci by `f <- f + f@1`, an undo of the last writes by
  reading `@`, a function that reads its argument's past to report a
  trend, and `#` as a write counter; by hand or model).
- `docs/LANGUAGE.md` and `CLAUDE.md` final pass.
- Leaves out: anything the examples want that the language lacks
  (D9): change the example instead.
- **Size:** medium.

## Proposals

None open.

## Example-port table

| Example | Needs | Status |
|---|---|---|
| fizzbuzz | steps 1, 3, 5 | waits on step 6 |
| factorial | steps 1, 4 | waits on step 6 |
| sort | steps 2, 3, 4 | waits on step 6 |
| reverse | steps 2, 3, 5 | waits on step 6 |
| history | steps 2, 3, 4, 5 | waits on step 6 |
