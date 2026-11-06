# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. **User** means [the person] decided it; **default** means the
agent proposed it and it wasn't explicitly discussed. Defaults are fair to
revisit. Open questions are listed at the end of [`DESIGN.md`](DESIGN.md).

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics (quote the person where the words matter),
the reason, and `Rejected:` with each alternative and why it lost. A
decision that's later changed stays, with a note pointing to the entry
that changed it; the new entry says what it retires.

Sections group entries by subject, not by time; a new entry goes in the
section it belongs to. Number by time.

## Scope

**D1. [What it is.]** *(User)* [Why.]

**D2. [What's kept from before, what's dropped.]** *(User)* [Quote.]

**D3. [What the runtime does, what's written in the language.]** *(User)*

**D4. [Scale.]** *(User)*

**D5. Aggressively simple; practical over pure.** *(User)* Any feature
that adds complexity can be cut or changed.

**D6. [Compilation model.]** *(User)* Rejected: [the alternative, and
who proposed it, and why it lost].

## The core rule

**D7. [The decision everything leans on.]** *(User: "...")* [What it
removes. What it costs.] Rejected: [...].

## Language

## Values and memory

## Runtime

## Compiler

## Project

**D8. Golden tests' expected output comes from an independent source,
never from the compiler.** *(User)* See `t/README.md`.

**D9. Examples bend to the language.** *(User)* When a port needs a
feature, the example changes or is left out. Rejected: adding to the
language to make a port pass.
