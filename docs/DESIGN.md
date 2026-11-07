# Strata design

This is the design as agreed. [`DECISIONS.md`](DECISIONS.md) has the
reasons and the alternatives that were turned down, and
[`PLAN.md`](PLAN.md) has the build order. Nothing is **(open)**: in this
run the designer and the builder are the same agent, and every question
was settled before code (see the brief, `docs/briefs/design-and-build.md`).

## Goals

- **A small imperative language where every name is a history** (D1,
  D7). Writing to a variable lays a new layer on top; the old layers stay
  and can be read; nothing is ever overwritten.
- **Usable for ordinary small programs** (D4): FizzBuzz, recursion,
  sorting, text, written plainly. The core rule should feel like a
  feature, not a tax.
- **Aggressively simple** (D5). Two kinds of atom, one container, seven
  statements, no I/O but printing.
- **Compiled**: a compiler in TypeScript (Node 22, type stripping) emits
  C, linked with a small C runtime by `cc` (D6).
- **Borrowed**: the persistent linked list (Lisp's cons), checked integer
  arithmetic, a C-like expression grammar. **New**: histories as the only
  container, and `@` as the one way into the past (`docs/BACKGROUND.md`).

## Non-goals

- Input of any kind: no stdin, arguments, files, clock or randomness
  (D28). Programs are closed and deterministic.
- Floats, booleans, characters, records, nested containers (D10).
- First-class or nested functions, closures, globals, modules (D18).
- Freeing memory (D26). Programs are small.
- Speed beyond "C, without trying".

## The language

A program is a file of top-level function definitions and statements.
The statements run top to bottom; functions may be defined anywhere at
top level and called from anywhere (D18).

**Atoms** are 64-bit signed integers and immutable byte strings (D10).
**A history** is a stack of atoms, newest on top; it may be empty.
**Every expression evaluates to a history** (D11). A literal `5` is the
one-layer history `[5]`; `x + 1` takes the top of `x` and the top of `1`
and yields a one-layer history of the sum. A bare name evaluates to that
name's whole history.

The statements (D16, D17):

- `let x = e`: declare `x`, naming the whole history `e` evaluates to
  (D12). `let y = x` gives `y` all of `x`'s past.
- `x <- e`: write: lay the top of `e` on `x` (D12).
- `print e`, `write e`: print the top of `e`, with or without a newline
  (D22).
- `if e { ... } else { ... }` (with `else if`), `while e { ... }`.
- `return e`, in a function.
- `f(a, b)`: a call, its result discarded.

The expression operators, loosest first: `or`; `and`; `not`; the
comparisons `= != < <= > >=` (not chained); `+ -`; `* / %`; prefix `-`
and `#`; postfix `@`. Primaries: integers, strings, names, calls,
history literals `[a, b, c]` (oldest first, so `c` is the top: D15), and
parentheses.

- `#e` is the depth of `e`: how many layers it has (D13).
- `e@k` is `e` as it was `k` writes ago: the history with its top `k`
  layers removed. `x@0` is `x`; `x@1` is `x` before its last write;
  `x@(#x)` is the empty history. `k` outside `0..#e` faults (D13).

Because `@` returns a history, it is both "the previous value"
(`x@1 + 1` uses its top) and "the rest of the list" (`f(xs@1)` recurses
on it).

**No form replaces a variable's history** (D14). A name is declared once
in its function (no shadowing, no redeclaration); after that it only
grows. Calls pass histories, and since histories are immutable and
shared, a callee writing to its parameter grows its own copy, never the
caller's (D18).

Integers are checked: overflow faults; `/` truncates toward zero and `%`
takes the dividend's sign; division by zero faults (D19). Conditions take
the top of a number; zero is false; comparisons and `and`/`or`/`not`
yield 1 or 0 (D20). Strings concatenate with `+` and compare bytewise;
three builtins, `len`, `at`, `str`, cover the rest (D21).

Evaluation is left to right, every operand and every argument (D25).

## The core rule

**D7: every name is a history. A write lays a new layer on top; `@`
reads the name as it was; nothing can change or remove the past.**

What it decides: there is one container, the history, so lists are
histories and "the rest of a list" is `@1`. Assignment can't destroy, so
there is no rebinding (D14) and no shadowing. Since the past is
immutable, histories are persistent linked lists and are passed by
sharing, with no copying and no aliasing surprises (D18), and the
runtime never needs to free (D26). What it costs: memory grows with
every write (a loop counter keeps every value it ever had), and lists
are built newest-first, so programs that want oldest-first walk with
`@` from the bottom or build reversed.

A proposal that touches assignment, `@`, `#`, `let`, or what a call
passes touches the core rule.

## Values and memory

An atom is a tagged pair: a tag (number or string) and either an
`int64_t` or a pointer to a string (length, bytes). A history is a
pointer to a layer `{atom, below, depth}` or NULL for empty; `depth` is
stored so `#` is O(1); `@k` walks `k` links. Strings and layers are
allocated from an arena of large chunks linked from a global, never
freed (D26), so LeakSanitizer sees them as reachable.

## The runtime

`runtime/strata.c` and `runtime/strata.h`: the arena, history
operations (push, top, drop, depth), the arithmetic and comparison
operations with their checks, strings and the three builtins, printing,
the call-depth counter (limit 10000, D27), and `strata_fault`, which
flushes stdout, writes `fault at L:C: message` to stderr and exits 1
(D23). There is no prelude (D3).

## The compiler

`compiler/src/`, TypeScript run by Node 22 directly (type stripping,
erasable syntax only). Pure functions over plain-object ASTs (tagged
unions), no classes (D29). Passes, one file each:

- `lexer.ts`: bytes to tokens with line and column.
- `parser.ts`: tokens to AST, by recursive descent on the grammar in
  `LANGUAGE.md`.
- `resolve.ts`: names: unknown, duplicate, builtin clashes, arity,
  `return` outside a function. Reports the first error only.
- `codegen.ts`: AST to C. Every subexpression goes into a fresh C
  temporary in source order, so C's unspecified argument order never
  shows (D25). Variables become C locals named `v_<name>`, functions
  `f_<name>`.
- `errors.ts`: the compile-error type and its format.
- `main.ts`: the command line.

`bin/strata build FILE -o OUT` compiles; `bin/strata run FILE` compiles
to `build/` and runs. A compile error prints `error at L:C: message` to
stderr and exits 2 (D24, D30).

## Open questions

None. Every default the builders take is recorded as *(default)* in
`DECISIONS.md` and decided by the designer when the step lands.
