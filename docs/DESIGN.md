# Curly design

This is the design as agreed on 2026-11-24. [`DECISIONS.md`](DECISIONS.md)
has the reasons and the alternatives that were turned down,
[`SURFACE.md`](SURFACE.md) goes through Perl construct by construct,
and [`PLAN.md`](PLAN.md) has the build order. D1 to D38 are Stevan's.
Anything marked **(open)** from here on is a default a later step
proposed that he hasn't confirmed: fine to build on, but bring it up
before baking it in further. What the decisions leave for a step to
settle is listed at the end.
[`TRAPS.md`](TRAPS.md) has ninety-three programs, each run under perl
5.42, where the obvious implementation would break the core rule.

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
  protocol, concurrency. Roles are to be part of the object system,
  taken up with `class` at step 17 rather than with the metaobject
  protocol: Stevan's wish, not yet a proposal (`PLAN.md`, step 17,
  says what to read first).

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
- **A fault can't be caught** (D13). If it could, a program
  could print something after one, which perl never would.
- **Where perl warns, the language faults or refuses** (D15).
  The line between what's kept and what's a fault is, mostly, perl's
  own warnings.
- **Where perl's answer changes from run to run, the language picks**
  (D14): hash order, addresses, the time.
- **Where perl's answer only looks arbitrary, the language follows
  it** (D14): a variable is read when its operator runs, so
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
programs, as it is built. In outline:

- A program is a file that begins `use v5.42;` (D16). strict and
  warnings can't be turned off.
- **Values:** undef, booleans (`true`, `false`), Int, Num, Str,
  references to arrays, hashes, scalars and code, and objects.
- **Variables:** lexical only, `my` and `state`. No package
  variables, no `local` (D17, D19).
- **Control:** `if`, `unless`, `while`, `until`, both `for`s, the
  statement modifiers, `last` and `next` with labels, `try` and
  `catch`, `die`.
- **Subs:** named, anonymous and lexical, each with a signature;
  closures. Called with brackets (D21). No `@_`, no `wantarray`.
- **Classes:** `class`, `field`, `method`, `ADJUST`, `:isa` (D19).
- **Packages:** `package Name;` names a file's subs, and nothing
  more: no `bless`, no package variables (D19).
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
   any of it runs: no `eval`, no symbol table, one object system, and
   a package that is only a name.
4. **No guessing** (D21, D15). Not by the parser, and not by the
   runtime about what a string or an undef was meant to be.

## Values and memory

- A value is two words, a tag and a payload (D25). Int and Num are in
  the payload; everything else is a pointer into the heap.
- Int is 64 bits signed and faults on overflow. Num is a double, and
  always finite (D37). Which of the two a result is follows perl,
  which decides by the operands' values: an operation is done on whole
  numbers when both operands are integral (an Int, or a whole Num
  below 2^53), and on doubles otherwise (D35). perl also lets a number
  remember having been used as an integer; the language faults where
  that shows, making a whole Num from 10^15 up to 2^53 a string (D23,
  D36).
- A string is immutable, a sequence of Unicode scalar values (D24,
  D42), held as UTF-8 with its length in characters beside its length
  in bytes. A program that prints a character past ASCII says `use
  open ':std', ':encoding(UTF-8)';` (D39).
- A string where a number is wanted is a number if it is written as
  one of the shapes perl takes in silence, and faults otherwise (D40).
  perl settles what a string is worth at its first use as a number and
  keeps the answer, one way for a use that wants an integer and
  another for a float; a value here has no past, so the rule gives
  perl's answer where every past agrees and faults where they differ:
  `"1e16"`, `"3.0"` in arithmetic that passes 2^53, a minus before a
  large or a signed string. The same is true of a number alone, in one
  place: `+ - *` with an Int of 2^53 or more that is exactly a double,
  beside a whole Num or a string (D45).
- A boolean is a kind of its own, the Int 1 or 0 where a number is
  wanted and `"1"` or `""` where a string is (D47). undef is the one
  value that is no value: an operator that wants a number or a string
  of it faults, and `defined`, `//` and the tests of truth take it
  (D48). The comparisons ask D35's question again, and `&&`, `||` and
  `//` give one of their operands (D49).
- Arrays and hashes are mutable and have identity; assigning one
  copies it, as in Perl.
- **A reference is a value of its own** (step 13a; D106 to D114): its
  payload is the container's block, the very block an array's or a
  hash's variable holds, so `\@a` is that block with another tag and
  `[ LIST ]` the list built for it. Reading through what is not a
  reference is a fault, storing through undef makes it (D107); a
  reference is true, defined, and `==` or `!=` to another by identity,
  and a fault wherever else a number or a string is wanted (D112).
  Every walk over names has one more, "what references reach" (D109),
  and a store through a chain also changes the head it starts from
  (D114). The collector walks from a container to what it holds with
  a stack of its own, so a chain of references takes none of C's, and
  a cycle is collected like anything else (D26).
- The collector traces: precise, non-moving, roots on a shadow stack
  (D26), with stress and poison knobs. No `DESTROY`. Built at step 7
  (D66): every variable and temporary of a function is a slot of one
  frame, and a value the program can still use is in a slot whenever
  a collection can happen, which is only inside an allocation; a
  runtime function allocates at most once, last, or opens a frame of
  its own.
- **A sub is a C function with a frame of its own** (step 8; D72,
  D73). It is handed perl's context of the call (D18), and where
  each argument is, a pointer into its caller's frame or the file's:
  it copies each as that parameter's turn comes, a default running
  in between, which is perl's order, and until then the argument is
  in a slot the collector sees. What it returns is a copy. The
  file's variables are the first slots of the file's frame, each its
  own, undef from the start, and a sub reaches them through the
  context.
- **Recursion has a limit that is the implementation's** (D68): the
  frames that are open are counted, 16 bytes a slot and 1 KB a call,
  and past 4 MB the next call is the fault `recursion too deep`. The
  count is of frames and not of the C stack, and the generated C
  touches a frame only through `rt_enter` and `rt_leave`: so that
  when concurrency comes (step 29) a call can stop being a C call.
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
collector's stress interval, poison and heap cap (step 7; D63 to D65:
`CURLY_GC_STRESS`, `CURLY_GC_POISON` and `CURLY_HEAP_CAP`, read from
the environment by every compiled program, and said for the tests in
`t/knobs.sh`); a virtual clock and a fixed seed (step 22).

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

(D29.) One file per pass under `compiler/src/`, and one table of
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
- **The checks are tested**: `t/checks/` holds tests the oracle check
  must fail, each in its own way, and they run with it.

## Open questions

D1 to D114 are decided. What is left is what the decisions hand to a
step, roughly in the order it will matter:

1. **Whether perl 5.42 agrees with what was run under 5.38.2**: it
   does. Step 0 ran every "perl prints" in these documents and every
   trap under both (`briefs/claims.py`), and the two differ only where
   `TRAPS.md` already said they would.
2. **Whether a program must say `use open ':std',
   ':encoding(UTF-8)';`**: settled, D39 (step 3). To print a character
   past ASCII it must, and the oracle runs perl plain.
3. **The exact line of D23**: settled, D35 to D38 (step 2), and for a
   string used as a number, D40 and D45 (step 3). Left to later steps:
   a negative zero given to `atan2` or formatted with `%g` (T79; steps
   16 and 22); `--` on a Num (T93, step 5); and **whether a variable's
   past can show anywhere the rules don't fault**, which step 5 has to
   ask again once there are variables to have one.
4. **How deep a program may recurse**: settled for now, D67 and D68
   (step 8). Nothing happens at perl's 100; `no warnings 'recursion';`
   keeps perl quiet there too. The only limit is the
   implementation's, 4 MB of frames today. **Left for step 29**: whether a call stays a
   C call at all; perl is clean of the C stack between statements,
   and D68 lists what was kept open so that this can be too.
5. **`for my $x ($p, $q)`**, a `foreach` over variables named directly,
   and an element read in an expression that also removes it:
   settled, D77 and D76 (step 9). Each is a refusal, by one walk over
   the whole program.
6. **`sort`'s comparator**: settled, D82 and D83 (step 10). perl's
   merge is ported, so that every comparison is perl's, and the
   generated code drives it: the runtime calls no block. The licence
   of the port, `runtime/sort.c`, is to be settled with the
   repository's.
7. **Reading through undef** (step 13): settled, a fault (D107), built
   for elements at 13a and for the whole container at 13b. And
   **dereference without braces**, `@$x` and `$$x[0]`: cut (D108),
   leaving the arrow, `->@*` and `@{ }`, as Stevan's style guide has
   it.
8. **A closure over a loop variable** (step 14): refused until then,
   and too common an idiom to leave refused.
9. **`finally` and `defer`; how `warn` is tested** (step 15).
10. **Modules** (step 18): `package Name;` is decided (D19); imports,
   and how files are found, are not.
11. **Regex captures** (step 19): `$1`, or only named and returned.
12. **Bytes**, for binary files, as a type apart from strings (with
    step 21).
13. **The syntax of a type** (step 25); **roles**, as part of the
    object system and whether they erase by flattening into classes,
    which would keep perl as their oracle (step 17, which reads
    `stevan/p5-roles-algebra` and `stevan/p5-core-role-tests` first;
    step 27 before); the shape of concurrency, and D13 revisited with it
    (step 29).
14. **The extension of a file that carries type annotations** (step
    25). A program is a `.pl` file until then.
