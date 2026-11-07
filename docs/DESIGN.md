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
value adds its lines.

- **Integers** (D4): Node's numbers are doubles, exact only to 2^53,
  and wrap or round silently. **Overrides**: an integer is a `bigint`,
  and every operator's result is range-checked against -2^62 to
  2^62-1, faulting `overflow` (tests 001, 011 to 014); the reader
  parses a literal as a `bigint` and rejects one past the range before
  running.
- **Division and remainder** (D5): `bigint` `/` and `%` truncate toward
  zero and the remainder takes the dividend's sign, as D5 says.
  **Inherits** (test 010). A zero divisor throws a host `RangeError`,
  so **overrides** it: the operator checks for zero and faults
  `division by zero` itself (test 015). `MIN / -1` is out of range and
  caught by the range check (test 014).
- **Bit operations and shifts** (D15, D16): `bigint` `&`, `|` and `^`
  are two's complement at unbounded width, which is D15's "any width
  agrees". **Inherits** (test 030). `>>` floors, as D16's `bit/shr`
  does. **Inherits** (test 032). A `bigint` `<<` or `>>` by a negative
  count shifts the other way and by a huge one allocates, so
  **overrides**: the count is checked, 0 to 62, before the shift is
  taken (tests 034, 035), and `bit/shl`'s result goes through the range
  check (tests 031, 033).
- **Exponentiation** (D18, D19): `bigint` `**` throws on a negative
  exponent, and on 2^62 would not finish. **Overrides**: a negative
  exponent faults `bad exponent` first; an exponent of 0 gives 1; a base
  of 0, 1 or -1 is answered by the exponent's parity without a loop
  (test 056); any other base with an exponent past 62 faults `overflow`
  at once (test 042); the rest is `bigint` `**`, range-checked (tests
  040, 041).
- **Comparison and equality, across types** (D12): JS `==` coerces and
  `<` compares a boolean with a number. **Overrides**: a value is a
  `bigint` or a `boolean`, the orderings fault `not an integer` on
  anything else, and `==` and `!=` compare with `typeof` first, so two
  values of different types are unequal, never coerced (tests 020,
  021). Only `===` is used.
- **Printing a value** (D4, D11): `String(bigint)` is decimal with no
  `n` and a `-` for a negative, as the tests expect (tests 000, 001);
  a boolean is **overridden** to `#true` and `#false` (test 021). The
  value and a newline are written once, at the end.
- **The order of evaluation** (D25): JS evaluates operands left to
  right, but the interpreter doesn't lean on it: an operator evaluates
  its left operand into a variable, then its right, then charges, then
  applies (tests 059, 060). **Inherits** the order, written out.
- **Errors before running, faults, and the exit** (D6, D28): an
  uncaught exception in Node prints its stack and exits 1, which is
  also a fault's status. **Overrides**: the driver catches its own
  classes: a check error is `FILE:LINE:COL: message` on stderr and exit
  2, a fault is `fault: NAME` on stderr and exit 1, and anything else
  is `lang: internal error: ...` with Node's stack and exit 3 (D30).
  Output is written with `fs.writeSync` and the status set with
  `process.exitCode`, never `process.exit`, so a pipe isn't cut off.
  Nothing is written to stdout before the program ends, so a fault
  leaves stdout empty (D6).
- **Depth**: Node's stack takes some thousands of recursive calls and
  then throws `RangeError`, in a message of its own, at a depth that
  differs between versions and machines. **Overrides** (D30): the
  reader keeps its own stack and has no limit of its own, and a form
  nested more than 1000 deep is an error before running, so the
  evaluator's recursion is far inside the host's. Test 010 nests 147.
- **Code points** (D31): a JavaScript string is UTF-16, so its `length`,
  its indexes and its `<` count code units, and a character past U+FFFF
  counts two. **Overrides**: a string's code points are taken with
  `Array.from` and `codePointAt`, and `str/lt` compares them one by one
  (tests 073, 074, 077).
- **Source encoding** (D31): `readFileSync(f, "utf8")` turns an invalid
  byte into U+FFFD and drops a leading byte order mark. **Overrides**:
  the driver decodes with `TextDecoder("utf-8", { fatal: true,
  ignoreBOM: true })`. An invalid file is `not valid UTF-8` before
  running (D34), and a byte order mark stays a character, so it begins
  a name the checker doesn't know (unit tests in `interp/tests/`).
- **Columns** (D28, D31): a JavaScript index counts code units, so a
  column after `"😀"` would be one too many. **Overrides**: the reader
  advances a code point at a time, and `col` counts those (a unit test
  with a form after `"😀"`).
- **White space** (D31): a regular expression's `\s` takes U+00A0, U+FEFF
  and a form feed. **Overrides**: the reader's white space is its own
  four characters, and the delimiters are those and the brackets, `;`
  and `"`. A unit test has U+00A0 and a form feed each read as an unknown
  name.
- **Equality of strings** (D12, D31): JavaScript's `===` on strings
  compares code units. A string here is well formed (the source is valid
  UTF-8, and a surrogate escape is an error), so equal code units are
  equal code points: **inherits**, with test 086 (`"é"` and `"e\u{301}"`
  differ, `"😀"` and `"\u{1F600}"` agree).
- **Printing a string** (D32): `JSON.stringify` writes `\u0007`, and
  surrogate pairs past U+FFFF, neither of which is D32. **Overrides**:
  `show` writes D32's escapes itself, a code point at a time (tests 070
  to 072).
- **Output encoding** (D32): `fs.writeSync` of a string writes UTF-8, as
  D32 says. **Inherits**, with test 071.
- **Code points from integers** (D33): `String.fromCodePoint` throws a
  host `RangeError` past 10FFFF and accepts a surrogate. **Overrides**:
  `str/char` checks the range and the surrogates itself and faults
  `not a character` (tests 079, 081 to 083).
- **Ordering of strings** (D33): JavaScript's `<` on strings compares
  code units, which puts `"\u{10000}"` before `"\u{FFFF}"`. **Overrides**:
  `str/lt` compares code points (test 077).
- **Not in the language yet** (floats, collections, tail calls, time):
  answered when a step brings them.

## Values and memory

A value is a `bigint` (an integer, D4, range-checked after every
operator) or a `boolean` (D11); the host's `typeof` is the tag, so D14's
bit tags are main's and not here (D28). A form is a plain object with
`line` and `col`. There is no heap yet, and the host's collector does
whatever memory there is.

## The runtime

[What it does and doesn't do; what's written in the language instead.]

## The interpreter

Passes, a file each in `interp/src/`: read (forms with their line and
column), check (every error that D28 says comes before running), and
evaluate (a tree-walker over the forms, D29). `bin/lang.ts` is the
driver. The reader is a loop over characters with a stack of its own
and enforces D30's depth; the checker and evaluator recurse. Errors are
two classes (`interp/src/errors.ts`): `CheckError` (a position, exit 2)
and `Fault` (a name, exit 1); anything else is an internal error, exit 3
(D30).
The budget is two counts threaded through the evaluator (D27's shape,
which D28 allows): `spent`, the operations done, and `limit`, the count
at which the next is refused. An operator is charged after its operands
and before its checks; `within` evaluates its budget under the budgets
around it, lowers `limit` to `spent + n` if that is lower, runs the
body, and puts the saved `limit` back. A run starts with a fresh pair.

## Open questions

- **(open)** D30: nesting limited to 1000 deep (an error before
  running), and exit 3 for an internal error. Defaults, written by the
  builder of step 0.
- **(open)** From main, not agreed: which fault reports when one
  operator could fault two ways.
- **(open)** D34: the messages and positions of a string literal's
  errors, and of a file that isn't UTF-8. Defaults, written by the builder
  of step 6, which could not ask.
