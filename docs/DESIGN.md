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

## Values and memory

An integer is a JavaScript `bigint`, kept in the 63-bit range of D4 by
a check after every operation that can leave it, and a boolean is a
JavaScript `boolean` (D11). The two never mix in JS: `typeof` is the tag
the arithmetic checks. D28 leaves the representation the interpreter's
own, and D14's tags are main's.

## The runtime

[What it does and doesn't do; what's written in the language instead.]

## The interpreter

Passes, a file each in `interp/src/`: read (forms with their line and
column), check (every error that D28 says comes before running), and
evaluate (a tree-walker, D29). `bin/lang.ts` is the driver.

The reader (`reader.ts`) turns text into forms, each with its line and
column; it keeps a stack of its own, so nesting depth is not bounded by
Node's. The checker (`checker.ts`) walks the forms in reading order and
makes a tree of nodes, or throws the first `CompileError` (D28); nothing
is evaluated until the whole program has passed. The evaluator
(`evaluator.ts`) walks the nodes and throws `Fault` (D6). `errors.ts` has
both. The driver is the only place that prints or exits: 0 and the value,
1 for a fault, 2 for an error before running, a usage error or a file it
can't read, 3 for a fault in the interpreter itself. The tree-walker
recurses, so a program nested a few thousand levels deep may overflow
Node's stack; the tests go 147 deep.

## Open questions

- **(open)** Which fault reports when one operator's own checks could
  fault two ways, as in `(bit/shl #true 99)` (D25 leaves it, `PLAN.md`
  step 3). The interpreter reports `not an integer`: both operands'
  types are checked, then the operator's own rule. No test has one.
