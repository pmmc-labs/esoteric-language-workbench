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

A program is one form, an integer or a call `(op a b)`; the five
operators `+ - * / %` each take exactly two operands (D8 **(open)**).
An integer is an optional `-` and digits, nothing else (D9 **(open)**),
63 bits, and an operation whose exact result is out of range is the
fault `integer overflow`, checked at every node (D10 **(open)**). `/`
truncates toward zero and `%` takes the dividend's sign; a zero divisor
is `division by zero` (D11 **(open)**). Operands are evaluated left to
right, always both, and nothing is folded: the first fault to happen is
the one reported (D12 **(open)**). `LANGUAGE.md` has them in full.

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

Defaults the agent proposed that the person hasn't confirmed:

- **D8**: a call is `(op a b)`, five binary operators, no one-operand `-`.
- **D9**: what an integer is, so `+5`, `1_0`, `1.5`, `0x10` are symbols.
- **D10**: out-of-range results fault at every node; no wraparound,
  saturation or bignums.
- **D11**: `/` truncates toward zero, `%` takes the dividend's sign.
- **D12**: left to right, no short-circuit, no constant folding.
