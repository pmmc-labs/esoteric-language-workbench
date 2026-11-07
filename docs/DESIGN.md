# [name] design

This is the design as agreed so far. [`DECISIONS.md`](DECISIONS.md) has
the reasons and the alternatives that were turned down, and
[`PLAN.md`](PLAN.md) has the build order. Anything marked **(open)** is a
default the agent proposed that hasn't been confirmed: it's fine to build
on, but bring it up before baking it in further.

## Goals

- **[What the language is.]** One line each, with the `Dn` that
  settled it.
- **[Who it's for, and at what scale.]** The answers that fit a big
  system aren't automatically right for a small one.
- **Aggressively simple.** Anything that adds complexity gets cut or
  changed. Practical beats pure.
- **A calculator** (D1): a program is one expression, and its value is
  printed.
- **Run by an interpreter** (D28): a tree-walker in TypeScript, run by
  Node as it is (D29). main compiles the same language to C; what a
  program prints is the same.
- **[What's borrowed and what's new.]**

## Non-goals

- [What it's not for. Each one saves a proposal later.]

## The language

Integers of 63 bits (D4) and booleans (D11); seventeen operators on two
operands each (D3, D5, D12, D15 to D19); `if` (D13) and `within`, a
budget of operations (D20 to D24); evaluation left to right (D25); a
fault ends the program (D6). `LANGUAGE.md` has them in full.

## The core rule

[The one decision everything else leans on, if there is one. In
a64-slight it was where a process may wait, which decided what a waiting
process holds, and so the collector, the scheduler and the calling
convention. Name it, so a proposal that touches it is recognised.]

## What the host gives, and what the language overrides

Node's behaviour wherever it and the decisions could differ
(`docs/PROCESS.md`, "An interpreter instead of a compiler"). For each:
what Node does, which decision governs, and what the interpreter does:
**inherits** (and the test that shows that's right), **overrides** (and
how), or **asks** (a question for the person, under Open questions).
Answered at step 0, before the code; a step that brings a new kind of
value adds its lines. Node 22.23 and 24.22 were both checked where a line
says so.

- **Integers** (D4, D31): Node's `number` is a double, exact only to 2^53,
  and D4's range is 2^62 wide. *Overrides*: an integer is a `bigint`, and
  each operator's result is checked against the 63-bit range, faulting
  `overflow` outside it. A literal outside the range is an error before
  running (D33). Tests 001 (both ends) and 011 to 013.
- **Division and remainder** (D5): a `bigint`'s `/` truncates toward zero
  and its `%` takes the dividend's sign, as D5 says. *Inherits*: `(/ -7 2)`
  is -3 and `(% -7 2)` is -1 (checked). The zero divisor is checked first
  (D32). `-2^62 / -1` is 2^62, past the range, and the range check catches
  it (test 014). Tests 010, 014 and 015.
- **Bit operations and shifts** (D15, D16): a `bigint`'s `&`, `|` and `^`
  act on the infinite two's complement, as D15 defines them: *inherits*
  (`-1n & 7n` is 7n, checked). `>>` floors toward negative infinity, which
  is `bit/shr`'s rule: *inherits* (`-7n >> 1n` is -4n, checked). *Overrides*
  for `bit/shl`: the count is checked 0 to 62 before any shift is done, so
  a huge count is never handed to `<<`, and the result goes through the
  range check. Tests 030 to 036.
- **Exponentiation** (D18, D19): *Overrides*. Node's `**` on a `bigint`
  throws a `RangeError` for a result too large to build (checked:
  `2n ** 4611686018427387903n`), and a host that tried it would take the
  exponent at its word. So the evaluator doesn't call `**` for a large
  exponent: a base of 0, 1 or -1 is answered directly (the parity of the
  exponent for -1), any other base with an exponent past 62 faults
  `overflow`, and the rest is `**` on a small exponent, then the range
  check. A negative exponent faults `bad exponent` first (D32). Tests 040
  to 045 and 056.
- **Comparison and equality, across types** (D12): values are `bigint` or
  `boolean` (D31). *Inherits* `<`, `<=`, `>`, `>=` on `bigint` (test 020).
  *Overrides* `==` with `===`, never the loose `==`, which says `1n == true`
  is true (checked). Values of two types are then never equal, so `==` on
  them is `#false` (D12). Tests 020 and 021.
- **Printing a value** (D4, D11): a `bigint`'s `toString()` is the decimal
  with a `-` and no separators: *inherits* (test 001). *Overrides* for a
  boolean: `String(true)` is `true`, so `#true` and `#false` are written
  out. The driver adds the newline. Tests 000, 001 and 021.
- **The order of evaluation** (D25): JavaScript evaluates arguments left to
  right, but the evaluator doesn't rely on that: it evaluates the left
  operand, then the right, then charges the budget, then checks, in that
  order, as written. Tests 059 and 060.
- **Errors before running, faults, and the exit** (D6, D28, D34): an
  uncaught exception in Node exits 1, which is a fault's status, so the
  driver catches everything and sets the status itself (D34): 0, 1 for a
  fault (`fault: ...`), 2 for an error before running (`FILE:LINE:COL:
  ...`), and 3 for an internal error (`lang: internal error: ...` with the
  stack). Output is written with `process.stdout.write` and
  `process.stderr.write`, and the status set by assigning `process.exitCode`,
  never by calling `process.exit()`, which Node's own documentation warns
  can cut off writes to a pipe still in flight. Node 22 and 24 print no
  warning on stderr for type stripping (checked), which a golden test would
  see. Tests 000, 011 to 015, 023, 024 and 033 to 036 check the faults and
  the exit.
- **Depth** (nothing decided by the decisions): Node's stack is about 10,000
  frames of plain recursion on both versions (checked). *Overrides*: a
  program nested more than 1000 levels is an error before running (D30),
  so the host's stack is never the limit a program meets. The tests nest at
  most 147 (`010-arith`).
- **Not in the language yet** (strings, floats, collections, tail calls,
  time): nothing at step 0. A step that brings one adds its lines here.

## Values and memory

A value is a `bigint` for an integer and a `boolean` for `#true` and
`#false` (D31). Nothing is allocated for a value beyond what the host gives
a `bigint` and a `boolean`, and there's no tag: the two types are told apart
by `typeof`, and a check for an integer is `typeof v === "bigint"`. D14's
tags are main's encoding and don't bind this (D28).

## The runtime

Nothing at steps 0 to 4: a fault ends the program, and the only state is
the program's. Step 5 adds the budget (D20 to D24), as the two counts D27
gives, kept as `bigint`s, with no-budget as the largest 64-bit integer.

## The interpreter

Passes, a file each in `interp/src/`: read (forms with their line and
column), check (every error that D28 says comes before running), and
evaluate (a tree-walker over the forms, D29). `bin/lang.ts` is the
driver.

The reader turns text into forms: a form is an integer, a boolean, a symbol,
or a list, and carries the line and column of its first character. The
checker walks the forms once, before any evaluation, and reports the first
error it finds in the order of the text, as D33 says. The evaluator is a
recursive function over the checked forms, one call per form, with the
budget charged at each operator (step 5). The driver reads the file, runs
the three passes, prints a value or reports a fault, and sets the exit status
(D34). Nothing else is shared between passes.

## Open questions

Each default the builder of the interpreter chose, where the person could
settle it. Each is a `D` entry, attributed to the builder and not to the
person.

- **Depth**: a program nested more than 1000 levels is an error before
  running (D30). Default: the limit is the 1000, fixed, not measured.
- **Values**: an integer is a `bigint`, a boolean a JavaScript `boolean`,
  equality `===` (D31). Default.
- **Which fault reports when one operator could fault two ways**: this is
  the item `CLAUDE.md`'s Status lists as not agreed from main. D32 decides
  it, with the type check first, then the operator's own check, overflow
  last. Default; the person may want another order, which would change
  `(bit/shl #true 99)` and `(/ #true 0)` and no golden test.
- **Errors before running**: the messages and which error is reported first
  in a program with several (D33). Default.
- **Exit 3 for an internal error** (D34). Default.
