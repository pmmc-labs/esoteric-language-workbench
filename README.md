# A spec for a new Perl

A design for a second attempt at the question
[`stevan/pp`](https://github.com/stevan/pp) asks (*if it looks, smells
and tastes like Perl, but isn't `perl`, is it Perl?*), written so that
it can be built with this repository's process (`docs/PROCESS.md` on
`main`): an agent builds, a person decides, one feature a step, and every
expected output comes from somewhere other than the compiler.

Nothing here is built. It is the workbench's documents, filled in.

## The idea in one paragraph

Take Perl 5.42 and only ever subtract. A program the compiler accepts
is still Perl, and prints what `perl` prints; anything Perl does that
the language doesn't want is a compile error or a loud stop at run
time, never a quiet difference. That one rule makes `perl` itself the
test oracle, which is what Chalk and perl5-son show an implementation
of Perl most needs and can least afford to build. Types are added the
way TypeScript adds them to JavaScript: erase them and it's Perl
again.

```
        your program.pl
              |
     +--------+---------+
     |                  |
   langc              perl 5.42            (the oracle; never the product)
     |                  |
  native binary      its output
     |                  |
     +----  compare  ---+
              |
   SAME      prints the same bytes
   LOUD      stopped early, with a fault; said nothing perl didn't
   REFUSED   would not compile, and says why
   WRONG     never
```

## What's here

| File | |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | The agent's standing instructions and the Status paragraph |
| [`docs/DESIGN.md`](docs/DESIGN.md) | The design, with every unconfirmed default marked **(open)** and listed at the end. Read this first. |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | D1 to D31: who decided, why, what was rejected |
| [`docs/SURFACE.md`](docs/SURFACE.md) | Perl construct by construct: in, a fault, later, or cut |
| [`docs/PLAN.md`](docs/PLAN.md) | Steps 0 to 30; 0 and 1 in full |
| [`docs/TRAPS.md`](docs/TRAPS.md) | Fifty programs, run under perl, where the obvious implementation would be wrong |
| [`docs/BACKGROUND.md`](docs/BACKGROUND.md) | What Chalk, perl5-son, Opal and Allium taught, with paths |
| [`docs/LANGUAGE.md`](docs/LANGUAGE.md) | The language as built: empty |
| [`t/README.md`](t/README.md) | The five kinds of golden test, and the oracle check |

## What is decided and what isn't

Stevan's, on 2026-11-24: the scope (D1), the core rule (D2), a
TypeScript compiler that emits C (D3), Chalk's subset as the start
(D4), gradual types, roles with a metaobject protocol, and concurrency
as planned later steps (D5), and no Sea of Nodes (D6).

Everything else, D10 to D31, is the agent's proposal and open. The
ones with the most reach: a fault can't be caught (D13); where perl
warns, the language faults (D15); loop variables and `$_` are
read-only and there is no `local` (D17); a sub can't see its caller's
context (D18).

## How far to trust it

The first draft was given to a reviewer with a real perl and one
instruction: break it. It found four false statements about perl and
about twenty programs the design as written would have got wrong.
Seven decisions were rewritten, and the programs are kept in
`docs/TRAPS.md`. One part is known to be unfinished: how numbers
behave where perl's printing depends on a number's history (D23). And
everything was run under perl 5.38.2, the one the cloud machine has;
step 0 reruns it under 5.42. Read the design as a strong first
proposal that has survived one attack, and expect the next to find
more.

## Starting

1. Settle the open questions at the end of `docs/DESIGN.md`, at least
   the ones steps 0 and 1 cite.
2. Copy `main`'s tree (af8e3a3) in under these files, keeping
   these where the two collide: `CLAUDE.md`, `docs/`, and
   `t/README.md` merged as it says.
3. Give it a name.
4. Step 0 of `docs/PLAN.md`.

This is an empty branch of the workbench: it shares no history with
`main` and holds only these documents, as the seed of a language to
be started from the template. `docs/BACKGROUND.md` has the four
projects read for the design: Chalk, perl5-son, Opal in `stevan/pp`,
and Allium.
