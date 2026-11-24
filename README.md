# Curly: a spec for a new Perl

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
   curlyc             perl 5.42            (the oracle; never the product)
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
| [`docs/DESIGN.md`](docs/DESIGN.md) | The design, with what is left for a step to settle listed at the end. Read this first. |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | D1 to D32: who decided, why, what was rejected |
| [`docs/SURFACE.md`](docs/SURFACE.md) | Perl construct by construct: in, a fault, later, or cut |
| [`docs/PLAN.md`](docs/PLAN.md) | Steps 0 to 30; 0 and 1 in full |
| [`docs/TRAPS.md`](docs/TRAPS.md) | Seventy-one programs, run under perl, where the obvious implementation would be wrong |
| [`docs/BACKGROUND.md`](docs/BACKGROUND.md) | What Chalk, perl5-son, Opal, Allium and Crayon taught, with paths |
| [`docs/LANGUAGE.md`](docs/LANGUAGE.md) | The language as built: empty |
| [`t/README.md`](t/README.md) | The five kinds of golden test, and the oracle check |

## What is decided and what isn't

D1 to D32 are Stevan's, all settled on 2026-11-24. The ones that give
the language its character:

- Erase and it's Perl (D2); a TypeScript compiler that emits C (D3);
  Chalk's subset as the start (D4); no Sea of Nodes (D6).
- A fault can't be caught (D13), and where perl warns, the language
  faults (D15).
- Loop variables and `$_` are read-only, containers freeze while
  iterated, and there is no `local` (D17).
- A sub can't see its caller's context (D18).
- `class` for objects, and `package` only as a namespace for subs
  (D19). Brackets on a program's own calls (D21).
- Strings are Unicode code points (D24); memory is traced, so no
  `DESTROY` (D26).
- Gradual types, roles with a metaobject protocol, and concurrency are
  planned later steps (D5).

What isn't decided is what those hand to a step: fourteen items at the
end of `docs/DESIGN.md`.

## How far to trust it

The first draft was given to a reviewer with a real perl and one
instruction: break it. It found four false statements about perl and
about twenty programs the design as written would have got wrong.
Seven decisions were rewritten, and the programs are kept in
`docs/TRAPS.md`. One part is decided in principle and not yet pinned
down: exactly where numbers fault because perl's printing depends on a
number's history (D23, step 2). And everything was run under perl
5.38.2, the one the cloud machine has; step 0 reruns it under 5.42. Read the design as a strong first
proposal that has survived one attack, and expect the next to find
more.

## Starting

A fresh session, on this branch: "Read `CLAUDE.md`, then do step 0 of
`docs/PLAN.md`." Step 0 copies `main`'s tree (af8e3a3) in under these
files, keeping these where the two collide, installs perl 5.42, and
ends with `say 42;` compiled and checked against perl.

This is an empty branch of the workbench: it shares no history with
`main` and holds only these documents, as the seed of a language to
be started from the template. `docs/BACKGROUND.md` has the four
projects read for the design: Chalk, perl5-son, Opal in `stevan/pp`,
and Allium.
