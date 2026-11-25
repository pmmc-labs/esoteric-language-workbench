# Curly: a spec for a new Perl

A design for a second attempt at the question
[`stevan/pp`](https://github.com/stevan/pp) asks (*if it looks, smells
and tastes like Perl, but isn't `perl`, is it Perl?*), written so that
it can be built with this repository's process (`docs/PROCESS.md` on
`main`): an agent builds, a person decides, one feature a step, and every
expected output comes from somewhere other than the compiler.

Steps 0 to 5 are built: arithmetic on integers and floats, strings,
comparison and logic, variables, assignment, blocks and `if` compile
to a native binary, and a script holds every test to what perl 5.42
prints. The rest is the workbench's
documents, filled in.

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
| [`docs/TRAPS.md`](docs/TRAPS.md) | Ninety-three programs, run under perl 5.42, where the obvious implementation would be wrong |
| [`docs/BACKGROUND.md`](docs/BACKGROUND.md) | What Chalk, perl5-son, Opal, Allium and Crayon taught, with paths |
| [`docs/LANGUAGE.md`](docs/LANGUAGE.md) | The language as built: `say`, and arithmetic on integers and floats |
| [`t/README.md`](t/README.md) | The five kinds of golden test, and the oracle check |
| [`docs/briefs/claims.py`](docs/briefs/claims.py) | Every statement these documents make about perl, as a program, rerun under 5.42 |

## What is decided and what isn't

D1 to D62 are Stevan's, settled on 2026-11-24 and 25. The ones that give the language its
character:

- Erase and it's Perl (D2); a TypeScript compiler that emits C (D3);
  Chalk's subset as the start (D4); no Sea of Nodes (D6).
- A fault can't be caught (D13), and where perl warns, the language
  faults (D15).
- Loop variables and `$_` are read-only, containers freeze while
  iterated, and there is no `local` (D17).
- A sub can't see its caller's context (D18).
- `class` for objects, and `package` only as a namespace for subs
  (D19). Brackets on a program's own calls (D21).
- Strings are Unicode characters (D24, D42), and a string is a number
  only where perl has one answer for it whatever was done with it
  before (D40); memory is traced, so no `DESTROY` (D26).
- Gradual types, roles with a metaobject protocol, and concurrency are
  planned later steps (D5).

What isn't decided is what those hand to a step: fourteen items at the
end of `docs/DESIGN.md`.

## How far to trust it

The first draft was given to a reviewer with a real perl and one
instruction: break it. It found four false statements about perl and
about twenty programs the design as written would have got wrong.
Seven decisions were rewritten, and the programs are kept in
`docs/TRAPS.md`. The part that was only decided in principle then,
where numbers fault because perl's printing depends on a number's
history, has since been measured and settled (D35, D36, step 2), and
then found to have a hole by the review of that step, which step 3
closed (D45). Everything was run under perl 5.38.2
first, and step 0 reran it all under 5.42: every statement held, and
building `say 42;` still found four traps the first review hadn't
(`docs/TRAPS.md`, T72 to T75), two of them by a second review, of
step 0's own language, after the compiler was passing its tests. Read the design as a strong first
proposal that has survived one attack, and expect the next to find
more.

## Starting

    make doctor     # node, cc, clang, and perl 5.42 as CURLY_PERL
    make test

A fresh session, on this branch: "Read `CLAUDE.md`, then propose step
5 of `docs/PLAN.md`."

This is a branch of the workbench that shares no history with `main`:
it began as these documents alone, the seed of a language to be
started from the template, and step 0 brought `main`'s tree (af8e3a3)
in under them. `docs/BACKGROUND.md` has the five projects read for the
design: Chalk, perl5-son, Opal in `stevan/pp`, Allium and Crayon.
