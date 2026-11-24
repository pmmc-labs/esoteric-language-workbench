# [name] design

This is the design as proposed on 2026-11-24. [`DECISIONS.md`](DECISIONS.md)
has the reasons and the alternatives that were turned down,
[`SURFACE.md`](SURFACE.md) goes through Perl construct by construct,
and [`PLAN.md`](PLAN.md) has the build order. Anything marked
**(open)** is a default the agent proposed that Stevan hasn't
confirmed: fine to build on, but bring it up before baking it in
further. Nine decisions are his (D1 to D6, and the three process rules
D7 to D9); everything else is open, and listed at the end.
[`TRAPS.md`](TRAPS.md) has fifty programs, each run under perl, where
the obvious implementation would break the core rule.

## Goals

- **Perl, freed from `perl`** (D1). A language that reads as Perl 5 and
  is smaller and cleaner, with a runtime of its own. Not backward
  compatible, not for CPAN.
- **Erase and it's Perl** (D2). The core rule, below.
- **Aggressively simple.** Anything that adds complexity gets cut or
  changed. In this language that has a second meaning: cutting a
  feature of Perl is always allowed, and is usually the right answer.
- **Compiled ahead of time to a native binary** (D3): a compiler in
  TypeScript that emits C, and a runtime in C.
- **Borrowed:** the subset from Chalk (D4); the verdicts from Chalk
  and perl5-son (D11); the triage of builtins from Allium (D22); the
  goal, the syntax-tree phase and the small core from Opal; the
  process from the workbench. **New:** the core rule as the definition
  of the language, and perl as the test oracle.
- **Later, by proposal** (D5): gradual types, roles and a metaobject
  protocol, concurrency.

## Non-goals

- Running existing Perl programs unchanged. Most will be refused.
- Matching perl where perl is unspecified (D14), or matching its
  stderr (D12).
- An optimizing compiler. No Sea of Nodes and no optimization passes
  (D6).
- Self-hosting (D6).
- String `eval`, a REPL, loading code at run time (D20).
- Grammars and rules, multiple dispatch, macros, lazy lists (D5).

## The core rule

**A program the compiler accepts is Perl 5.42 once its annotations are
erased, and when it runs without faulting it prints what perl prints.**
(D2.)

Every program falls in one of four places, and the fourth is a bug in
the implementation, always:

```
                      the same file, given to perl 5.42
                                    |
           +------------------------+------------------------+
           |                        |                        |
       REFUSED                    LOUD                     SAME
   compile error            fault at run time          runs to the end
   FILE:LINE:COL            stdout so far is the       stdout and exit
   no binary                start of perl's            status are perl's

                    WRONG: ran, didn't fault, printed something else.
                    Never. A WRONG is fixed by making it SAME, LOUD
                    or REFUSED, in that order of preference.
```

What follows from it:

- **Cleanup is subtraction.** A cut feature is a refusal (D13) where
  the source shows it, and a fault where only the run does. Nothing
  Perl means is given a second meaning.
- **perl is the oracle** (D10). A golden test is a `.pl` file. perl's
  output is its expected output, and a script checks that on every
  run of the suite.
- **A fault can't be caught** (D13, open). If it could, a program
  could print something after one, which perl never would.
- **Where perl warns, the language faults or refuses** (D15, open).
  The line between what's kept and what's a fault is, mostly, perl's
  own warnings.
- **Where perl's answer changes from run to run, the language picks**
  (D14, open): hash order, addresses, the time.
- **Where perl's answer only looks arbitrary, the language follows
  it** (D14, open): a variable is read when its operator runs, so
  `$total + step()` sees what `step` did to `$total`.
- **The rule is easy to state and hard to keep.** The first draft of
  this design broke it in a dozen places that a review found by
  running perl (`TRAPS.md`). Every step's proposal gets the same
  treatment before it's built.
- **An exception is a decision.** A feature perl doesn't have (roles,
  concurrency) says so in its `Dn`, and brings a model or a referee.

A proposal that would give a Perl program a different meaning touches
this rule, and says so in its first line.

## The language

[`LANGUAGE.md`](LANGUAGE.md) will have it in full, for someone writing
programs, as it is built. In outline, all of it **(open)**:

- A program is a file that begins `use v5.42;` (D16). strict and
  warnings can't be turned off.
- **Values:** undef, booleans (`true`, `false`), Int, Num, Str,
  references to arrays, hashes, scalars and code, and objects.
- **Variables:** lexical only, `my` and `state`. No package
  variables, no `local` (D17).
- **Control:** `if`, `unless`, `while`, `until`, both `for`s, the
  statement modifiers, `last` and `next` with labels, `try` and
  `catch`, `die`.
- **Subs:** named, anonymous and lexical, each with a signature;
  closures. Called with brackets (D21). No `@_`, no `wantarray`.
- **Classes:** `class`, `field`, `method`, `ADJUST`, `:isa` (D19).
- **Strings and regexes:** Unicode strings (D24); Perl 5's regexes, a
  subset, compiled ahead of time (steps 19 and 20).
- **Data:** arrays, hashes in insertion order (D27), nested through
  references, postfix dereference, slices.

Four ideas do the cleaning, and `SURFACE.md` applies them:

1. **Values flow; containers don't** (D17). Arguments, loop variables
   and `$_` are values. No write reaches back through one.
2. **Context is syntax** (D18). List or scalar is read off the source.
   A sub can't see it.
3. **A closed world** (D20, D19). The whole program is known before
   any of it runs: no `eval`, no symbol table, one object system.
4. **No guessing** (D21, D15). Not by the parser, and not by the
   runtime about what a string or an undef was meant to be.

## Values and memory

All **(open)**.

- A value is two words, a tag and a payload (D25). Int and Num are in
  the payload; everything else is a pointer into the heap.
- Int is 64 bits signed and faults on overflow. Num is a double.
  Which of the two a result is follows perl, which decides by the
  operands' values; perl also lets a number remember having been used
  as an integer, and step 2 has to choose what to do about that
  before it builds (D23).
- A string is immutable, a sequence of code points (D24).
- Arrays and hashes are mutable and have identity; assigning one
  copies it, as in Perl.
- The collector traces: precise, non-moving, roots on a shadow stack
  (D26), with stress and poison knobs. No `DESTROY`.
- No global state in the runtime: one context, passed everywhere (D28).

## The runtime

`runtime/rt.c` and `rt.h`: the value, the heap and collector, the
operators as checked functions (every one tests its operands' tags,
converts as perl does, and faults by name where perl would warn),
strings, arrays, hashes, the regex matcher, the fault path, and the
standard streams. It calls the C library for what perl takes from it
(formatting a double, `strtod`, the system calls). What perl has
tables of its own for, the C library doesn't: Unicode case mapping is
the first, and faults past ASCII until a step brings the tables
(T45). As the language grows, builtins that can be written in
the language are (step 23: the prelude), and the runtime keeps the
primitives.

Knobs, set by `t/run.sh` so no test depends on its machine: the
collector's stress interval, poison and heap cap (step 7); a virtual
clock and a fixed seed (step 22).

## The compiler

```
file.pl
  |  lexer       whole file; every token has a line and column;
  |              the parser says "term next" or "operator next"
  |  parser      statements by recursive descent, expressions by
  |              precedence climbing (perlop's table)
  v
syntax tree, with positions            <- the one data structure
  |  resolver    names to declarations, captures, context (D18)
  |  checker     the refusals (D17 to D22); types, from step 25
  |  codegen     straight-line C: one statement per operation (D31);
  |              a variable is read where it's used, never copied (D14)
  v
file.c  --cc-->  binary, linked with runtime/rt.c
```

(D29, open.) One file per pass under `compiler/src/`, and one table of
keywords and builtins that every pass reads. No intermediate form
until a step needs one. Errors are diagnostics with positions. The
compiler is TypeScript that Node runs as it is, so only erasable
syntax: no enums, no parameter properties.

Types (steps 25 and 26) are where speed will come from, as Opal's design said:
"if we know the types, we do not need to do runtime checks". A sub
whose parameters are known to be Int compiles to C arithmetic on
`int64_t` with an overflow test, and no tags. That is the whole
optimization plan.

## Testing

- **Golden tests** are `.pl` files, in five kinds (D10): `same`,
  `dies`, `fault`, `refused`, `new`. `t/run.sh` compiles and runs them;
  `t/checks.py oracle` runs perl on them.
- **Models** (`t/models/`) are for the edges: a model writes a test
  program over the values that find them, and the expected output from
  the definition; the oracle check then holds perl to the same
  answer. Two derivations, neither the compiler's.
- **The census** (D11): other people's probes, with a ratchet, from
  step 11.
- **An adversarial review of each large step's proposal**, by someone
  who didn't write it, with perl to hand. It found what the author of
  this design couldn't see.
- **gcc, clang and the sanitizers** on every runtime change, as the
  workbench found it needed.
- **Stevan's machine** after every step.

## Open questions

Everything below is a default. Roughly in the order it will matter.

1. **The name**, and with it the driver's name and the extension of a
   file that carries type annotations. The driver is `langc` and tests
   are `.pl` until then.
2. **D13**: faults can't be caught, and perl's own runtime errors
   (division by zero, a missing method) are faults. This is the
   decision with the most reach.
3. **D15**: perl's warnings as the line between kept and fault.
4. **D17**: read-only loop variables and `$_`, frozen containers, no
   `local`. `s/^\s+// for @lines` and `chomp(my @l = ...)` go with it.
5. **D18**: a list-shaped `return` faults in a scalar call, and a sub
   that ends in an `if` has no value.
6. **D21**: brackets on every call of a program's own sub; named subs
   only at the top of a file.
7. **D14**: operands that are variables are read late, as perl reads
   them.
8. **D23**: overflow faults; no unsigned; and the one part of the
   design known to be unfinished: what to do where perl's printing of
   a number depends on the number's history.
9. **D24**: strings as code points; bytes later, apart.
10. **D26**: a tracing collector, and so no `DESTROY`.
11. **D19 and D22**: no `package`, and the list of what's gone for
    good.
12. **D11**: asking perigrin for the probes and the graded corpus.
13. D10, D12, D16, D20, D25, D27 to D31: the working-out, each
    small.

Not yet proposed, and named so they aren't forgotten: how deep a
program may recurse (step 8); what `for my $x ($p, $q)` means (step
9); a closure over a loop variable, which perl keeps as an alias
after the loop and which is refused until then (step 14); whether reading through undef faults (step 13); `$1` or only named
and returned captures (step 19); how files in several modules name
each other without `package` (step 18); the syntax of a type (step
25); whether roles erase by flattening into classes, which would keep
perl as their oracle (step 27); the shape of concurrency (step 29).
