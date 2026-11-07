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

- **Integers** (D4): [Node: ... Interpreter: ...]
- **Division and remainder** (D5): [ ]
- **Bit operations and shifts** (D15, D16): [ ]
- **Exponentiation** (D18, D19): [ ]
- **Comparison and equality, across types** (D12): [ ]
- **Printing a value** (D4, D11): [ ]
- **The order of evaluation** (D25): [ ]
- **Errors before running, faults, and the exit** (D6, D28): what an
  uncaught exception does, how stdout and stderr are flushed, how the
  exit status is set. [ ]
- **Depth**: how deep the host's stack goes, and what a program nested
  deeper does. Nothing decided. [ ]
- **Not in the language yet** (strings, floats, collections, tail
  calls, time): answered when a step brings them.

## Values and memory

[How the interpreter represents a value: D28 leaves it its own, and
D14's tags are main's.]

## The runtime

[What it does and doesn't do; what's written in the language instead.]

## The interpreter

Passes, a file each in `interp/src/`: read (forms with their line and
column), check (every error that D28 says comes before running), and
evaluate (a tree-walker over the forms, D29). `bin/lang.ts` is the
driver. [The shape of the code.]

## Open questions

[Each **(open)** item, in one place, so the person can settle them in a
batch.]
