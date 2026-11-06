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
- **[How it's compiled, and to what.]**
- **[What's borrowed and what's new.]**

## Non-goals

- [What it's not for. Each one saves a proposal later.]

## The language

A program is one form: an integer, or an operation `(op a b)` of one of
`+ - * / %` and exactly two operands, each an integer or an operation
(D8). An integer is 63 bits; an operation's result is the exact one, and
a result out of range is the fault `integer overflow`, intermediate
results included, so the check is at 63 bits and not at the machine's 64
(D9). `/` and `%` truncate toward zero, `%` takes the dividend's sign,
and a divisor of zero is the fault `division by zero` (D10). Operands
are evaluated left to right and the first fault ends the program (D11).
Nothing is folded at compile time, so a fault is a run-time event and
its message has no position (D12). A malformed program is a compile
error at the form at fault, one of six messages, the whole program
checked before anything runs (D13). `LANGUAGE.md` has them in full for a
user.

[The rest of the language, as it is added.]

## The core rule

[The one decision everything else leans on, if there is one. In
a64-slight it was where a process may wait, which decided what a waiting
process holds, and so the collector, the scheduler and the calling
convention. Name it, so a proposal that touches it is recognised.]

## Values and memory

[Encodings, allocation, collection.]

## The runtime

[What it does and doesn't do; what's written in the language instead.]

## The compiler

[Passes, the shape of the code, targets.]

## Open questions

[Each **(open)** item, in one place, so the person can settle them in a
batch.]
