# Curly

Curly is a cleaned-up Perl 5 with a runtime of its own. A program it accepts is
Perl 5.42 once its annotations are erased, and prints what perl prints
unless it stops loudly first; what Perl has that the language cuts is a
compile error or a fault, never a different meaning. The compiler is
TypeScript run by Node as it is, and emits C that links with a C
runtime. The driver is `curlyc`, and a program is a `.pl` file.

## Status

**Steps 0 to 3 of [`docs/PLAN.md`](docs/PLAN.md) are done**
(2026-11-24, all by Fable 5.2). **The language** is `use v5.42;`,
then `use utf8;` and `use open ':std', ':encoding(UTF-8)';` if wanted,
then any number of `say EXPR;` and `print EXPR;` (brackets or not),
where an expression is a number, a string, brackets, unary `-` and
`+`, `+ - * / % **`, `.` and `x`, and the builtins `length uc lc ord
chr` (perl's named unary operators, D41) and `substr` and `index` (in
brackets), with perlop's precedence
([`docs/LANGUAGE.md`](docs/LANGUAGE.md)). **A number is an Int (64
bits, signed) or a Num (a finite double)**, and which one an
operation gives is perl's own rule (D35): it is done on whole numbers
when both operands are *integral* (an Int, or a whole Num below 2^53)
and on doubles otherwise; `/` gives a Num, except an Int past 2^53
divided exactly; `**` gives a Num for a base that is a power of two,
an exact Int when the base's bits times the power are at most 64, and
C's `pow` otherwise; `%` cuts a Num to its whole part. **A Str is
Unicode scalar values** (D24, D42), immutable, UTF-8 inside, counted
in characters. **A string where a number is wanted** (D40) is one of
the shapes perl takes in silence, or `not a numeric string`: digits
are the Int; an exponent gives the Int if whole and below 2^53, a
fault if whole and larger, else the Num; a point gives the Num, and a
whole one below 2^53 (`"3.0"`) is *soft*: float arithmetic beside an
integral operand, and a fault if either number or the exact answer
reaches 2^53; and where a whole number is wanted, a string with a
point whose digits before it aren't its number cut down faults
(T103). **perl has two answers in those places, by what was
done with the value before, and a value here has no past**: that is
the reason for every fault that says `two answers` or `two values`,
and for D45, which amends D35: in `+ - *`, an Int of 2^53 or more
that is exactly a double faults beside a whole Num or a string (T92).
**Faults** (D13): `integer overflow`, `float overflow`, `not a
number` (D37), `division by zero`, `modulus by zero`, `modulus of a
number outside the integers`, a whole Num from 10^15 up to 2^53 made
a string (D36: `+ 0` makes the Int); `not a numeric string`, the
two-answer faults above, a minus before a string that starts with
`+`; `substr outside of string`, `negative repeat count`, `repeated
string too long`, `not a character`, `uc` or `lc` of a character past
ASCII, a whole number wanted that isn't an Int; printing a character
past ASCII without `use open` (D39), or a noncharacter. A fault names
the line its statement starts on (D34).
**Literals**: numbers as D38 (decimal; `1.5`, `.5`, `1e3`; `0x1F`,
`0b101`, `0o17` up to 32 bits; `_` between digits); strings as D43
(`'...'`; `"..."` with `\n \t \r \f \b \a \e \0`, `\\ \" \$ \@`,
`\xHH`, `\x{...}`, octal, `\o{...}`, `\N{U+...}`, a backslash before
a punctuation mark). **Refused**: a leading zero (`017`), `1.`, a
literal too large for its kind, a number hard against a letter, digit
or dot (T62, T78); an unescaped `$` or `@` in double quotes (T34), an
escape perl warns about or that needs interpolation (T86, T95); a
character past ASCII outside a string or a comment, or on any line up
to the one that says `use utf8;` (T73); a file that isn't UTF-8; `say
(1 + 2) * 3;` (T25); `say`, one space and a bracket, unless the
brackets close on that line counted as text, one in a string too, and
`;` follows (T76, T100); `(...) x N` as the whole argument of `say`,
which is a list to perl (T101); `"ab" x3` (T57); `substr` without
brackets; `length - 5` (T94); any pragma or spelling of one outside D16's list; `--`,
`++` and every other operator of perl's, as the longest token perl
would take (T27); a line that starts `#!` (D33).
**The compiler**: `lexer.ts` (the whole file, a line and column on
each token, every character checked there; it knows whether a value
or an operator comes next from the token before, T90), `parser.ts`
(precedence climbing over perlop's table), `ast.ts` (`int`, `num`,
`str`, `unary`, `binary`, `apply`; `use`, `pragma`, `call`),
`checker.ts`, `codegen.ts`, `names.ts` (the statements, the builtins
by shape, the pragmas, and all 25 rows of perlop's table, of which
five are live), `errors.ts`, and the driver `bin/curlyc.ts` (D3,
D29). **The generated C** is straight-line (D31): each operation a
statement with its result in a temporary, operands left before right,
the statement's line stored in the context first; a Num literal goes
over as its 64 bits, a string literal as a constant with its bytes
and characters counted. **The runtime**: the two-word value (D25),
the context first in every call (D28), strings on a list the context
owns and frees at the end (no collector until step 7), every operator
checking its operands' tags. **Tests**: golden 000 to 009 (step 0);
010 to 026 from `t/models/arith.py` and 030 to 038 by hand (step 1);
040 to 078 from `t/models/num.py` and 080 to 093 by hand (step 2);
100 to 169 and 180 to 191 from `t/models/str.py` (about 15,000 lines
on which the model and perl agree, and 62 programs that each fault
once), 170 to 179 by hand with perl's answers, 200 to 237 refusals
by hand (step 3); 58 unit tests, the runtime's own in C. **The oracle
check** (`t/checks.py oracle`, D10) holds every test to perl 5.42 by
its kind, **run plain, with no switches** (D39), and has 43 tests of
its own in `t/checks/`; its seeds are eight of 64 hex digits
(`PERL_HASH_SEED=1` to `8` are nearly one seed to perl). Its reading
rule for hashes is by pattern and errs toward rejecting; step 12 will
meet it first. Green under gcc, clang, and UBSan with ASan. **Each
step's language was reviewed adversarially** (step 1's: nothing
found, and the compiler agrees with the reviewer's own model on
1,271,555 programs, `docs/briefs/step1-review/`). Each step's runtime
was broken on purpose until every breakage was caught: step 2's found
three holes in its own tests that way, and step 3's six of 70
(`docs/briefs/step3-mutations.py`); the limit of `x` is tested from C
(`runtime/tests/limit.c`), since perl can't be asked for 2^31
characters. **A fault that never happens is
invisible to a test of what prints: every fault needs a fault test of
its own, at its edge.**

**perl 5.42 was installed and everything rerun under it**:
`docs/briefs/claims.py` holds every statement these documents make
about perl as a program, 354 of them now, and all hold under 5.42.0,
run plain as the oracle runs it. [`docs/TRAPS.md`](docs/TRAPS.md)
keeps the programs, T1 to T108, by step. **Found at step 0**: T72 (a
line that starts `#!`, D33), T73 (`use utf8;` on a line before the
first character past ASCII), T74 (`# line N "file"` comments, step
15), T75 (`use v5.42#c`). **At step 1**: T76. **Proposing step 2**:
T77 to T82. **By the review of step 2**: T91 (a literal over 250
characters), T92 (D45), T93 (`--` on a Num, step 5). **Proposing and
building step 3**: T83 to T90 and T94 to T99, the last six each a
place where perl warns or answers with garbage that the proposal
hadn't seen (`length - 5`; `\x4 `; `substr("abcde", -8, 2)`;
`substr("abc", 0, 1e30)`, which is `ab`; `"a" x -0.5`). **By the
review of step 3**: T100 to T103; the reviewer's model and generator
are kept, `docs/briefs/step3-review/`, and the compiler agrees with
them and with perl on 54,969 of the 55,002 random statements the
model prints for, refusing the other 33 by two rules where it is the
stricter. T102 became D46: perl works a constant `x` out as it
compiles, so `say "before"; say "b" x 999999999999999;` prints
nothing under perl (it runs out of memory before the program starts),
where the language prints `before` and faults; a perl without the
memory for what a program asks is outside what D12 promises. No test
asks perl for a large string. What the
review of the oracle check left open is listed in `docs/TRAPS.md`,
"The checks themselves", by the step that has to close it (15: a
`dies` test that also warns; 21 and 22: files, the environment, the
clock; 16 and 19: quotes the reading rule can't pair). A test with a
sort in it breaks its ties.

**D1 to D46 are all Stevan's.** The ones a builder meets first: the
core rule (D2); a TypeScript compiler emitting C (D3); a fault can't
be caught (D13); perl's warnings are faults (D15); loop variables are
read-only and containers freeze (D17); a sub can't see its context
(D18); `class`, and `package` only as a namespace (D19); brackets on
a program's own calls (D21); a number is integral or it isn't (D35),
and a value has no past (D36, D40, D45); the name (D32). perigrin has
agreed to the probe corpus (D11). **Next: step 4**, booleans, undef,
comparison and logic, is **proposed in full in `docs/PLAN.md` and
waits on Stevan's answers to its five questions** (Q1: a boolean as a
number and a string, as perl has it; Q2: where bare `undef` may
stand, perl taking what follows it for an argument, T105; Q3: `&&`
and `||` give an operand; Q4: chained comparisons, refused or perl's;
Q5: the word operators, which bind more loosely than `say`, T106, and
the bracket after `not`, T107). Nothing of step 4 is built.
`docs/briefs/step4-comparisons.py` holds the proposed rule for
comparing to perl under every past of each operand: 57,376
comparisons, no new fault needed. **What step 5 must ask again**:
once there are variables, whether a value's past shows anywhere the
rules don't fault. The claim was refuted once (T92), by a review,
after the builder's own search had passed it. The evidence is kept:
`docs/briefs/step2-perl-numbers.py` (D35 against perl, 129,801
operations), `step2-history.pl`, `step2-literals.py` (perl reads and
prints floats as C does; run it on a new machine), and
`step3-strings-as-numbers.py` (D40 and D45 under every past of every
operand: 41,594 operations, perl having more than one answer for
9,596, the rule never giving a value perl doesn't). One risk to watch
on the Mac: `**` with a fractional operand is the C library's `pow`.
Not agreed: what the decisions leave to steps, listed at the end of
[`docs/DESIGN.md`](docs/DESIGN.md).

## Read first, in this order

1. [`docs/LANGUAGE.md`](docs/LANGUAGE.md): the language as it is, for
   someone writing programs in it.
2. [`docs/DESIGN.md`](docs/DESIGN.md): the language and implementation
   as agreed. **(open)** marks a later proposal that hasn't been
   confirmed; there are none yet.
3. [`docs/SURFACE.md`](docs/SURFACE.md): Perl, construct by construct:
   in, a fault, later, or cut.
4. [`docs/PLAN.md`](docs/PLAN.md): the build order.
   [`docs/TRAPS.md`](docs/TRAPS.md): for the step in hand, the
   programs where the obvious implementation is WRONG.
5. [`docs/DECISIONS.md`](docs/DECISIONS.md): why, and what was turned
   down. Check it before "improving" something; it may have been
   decided against.
6. [`docs/BACKGROUND.md`](docs/BACKGROUND.md): the five projects this
   learned from, and what is parked. Optional.

The process is the workbench's: `docs/PROCESS.md` and `docs/MODELS.md`
in `pmmc-labs/esoteric-language-workbench`.

## Working rules

- **The core rule (D2) is the design.** Before accepting a construct,
  ask what perl does with it. If the language would do anything else,
  it refuses or faults. A change that gives a Perl program a new
  meaning is a proposal that says so in its first line.
- **Never WRONG.** A program that runs, doesn't fault, and prints what
  perl doesn't is a bug, whatever else is true. Fix it by agreeing
  with perl, or faulting, or refusing, in that order of preference. A
  refusal has a message that names what was refused.
- **Aggressively simple.** When a feature needs machinery, say so and
  offer to cut it. Cutting is always allowed here.
- **Propose before building** any change to semantics, a construct
  moved between In, Fault, Later and Cut in `SURFACE.md`, a builtin,
  or anything marked (open). Give options and a recommendation. Record
  the outcome in `docs/DECISIONS.md` (who decided, why, what was
  rejected) and update `docs/DESIGN.md` and `docs/SURFACE.md`.
- **perl is the oracle, and memory isn't.** Never write what perl does
  from memory, in a test, a decision or a document: run perl 5.42 and
  paste. (perl5-son recorded being wrong from memory twice in one fix;
  this design's first draft had `2 ** 62` as an exact integer, and
  perl prints `4.61168601842739e+18`.)
- **A proposal for a large step is reviewed adversarially before
  it's built**: a reader who didn't write it, given the proposal and
  perl, asked to find a program that would run, not fault, and differ.
  What it finds goes into `docs/TRAPS.md` with the program and perl's
  output, and into the step as a test.
- **Expected output never comes from the compiler** (D7). A `same`
  test's comes from perl; a `fault` or `refused` test's is worked out
  by hand; a model writes the edges. When a model's output moves,
  rerun the model; don't patch the file.
- **Make a check fail on purpose before trusting it.** A new check,
  a new kind of test, a new script: break what it guards and see it
  go red. (perl5-son's harness once reported 986 of 986 clean when
  857 were, because a loop ate its own input.)
- **Tests run programs.** A check that reads the tree or the C and
  never runs the binary proves nothing about what a program prints.
- Keep a working compiler with passing tests at the end of every step
  (Ghuloum). Each step adds golden tests.
- **Examples bend to the language** (D8). A port of a Perl program
  will want something that was cut; change the port.
- When a construct or builtin is added or changes, update
  `docs/LANGUAGE.md` (no tables there) and its row in
  `docs/SURFACE.md`.
- When editing with scripts, assert that each replacement matched.
- Test timing uses a virtual clock; real time is never used in tests.
- Update the Status section above as steps land. It is the only
  handoff: there is no `docs/plans/`, and a plan that isn't a step in
  `PLAN.md` or a `Dn` doesn't exist.
- A commit that touches the implementation names its decision or plan
  step in the subject (D9; `make hooks` installs the check).
- At the start of a step, compare the step's **Size** line with your
  own model, by the workbench's `docs/MODELS.md`, and say so if they
  don't match.

## Code style

- TypeScript that Node runs as it is: only erasable syntax (no enums,
  no parameter properties, no namespaces).
- The compiler is plain functions over plain data: tree nodes are
  objects with a `kind`, lists are arrays, and nothing is mutated
  after the pass that made it. One file per pass. No class
  hierarchies. (If the compiler is ever ported to the language, this
  is the shape that ports; nothing depends on that.)
- **One table of names** (`compiler/src/names.ts`): keywords, builtins,
  their argument shapes and contexts. No pass switches on a source
  string that isn't in it.
- An error is a diagnostic with a position, raised where it's found.
  It is never a node in the tree.
- The generated C is one statement per operation, each result in a
  temporary (D31). C doesn't order a call's arguments: never pass a
  variable and a call that sets it in the same argument list, and
  never two arguments that can fault. A C compiler takes more than
  proportionally longer over one long function (gcc at `-O1`, 36
  seconds for ten thousand statements): the driver compiles the
  program's C at `-O0` and the runtime at `-O1`, and a model keeps a
  program to about three thousand statements. The cloud machine's `cc` is gcc
  and the Mac's is clang: run the suite under both, and `make
  sanitize`, before calling a runtime change done. A left shift of a
  negative value is undefined before C23. (All three are the
  workbench's findings, each from a bug.)
- The runtime has no global state: one context, first argument of
  everything (D28).
- Every runtime operator checks its operands' tags and faults by name.
  No operator trusts the compiler until types (step 26) give it a
  reason to.
- The passes walk the tree by recursion, so an expression some
  thousands of terms long or brackets deep stops the compiler (exit 2,
  with a message). A pass that must take more becomes a loop.
- Comments explain why, not what.

## Toolchain

- Node 22.18 or later, and a C compiler as `cc`; clang as well.
- **perl 5.42**, as `CURLY_PERL` (default `perl`). The checks fail
  without it; they don't skip, and `make doctor` says what is wrong.
  The cloud machine's own perl is 5.38.2. 5.42 comes from the
  environment's setup script, built from cpan.org's source (reachable;
  no network change needed) into `/opt/perl-5.42`, with
  `CURLY_PERL=/opt/perl-5.42/bin/perl` set on the environment:

      if [ ! -x /opt/perl-5.42/bin/perl ]; then
        cd /tmp
        curl -fsSLO https://www.cpan.org/src/5.0/perl-5.42.0.tar.gz
        echo "e093ef184d7f9a1b9797e2465296f55510adb6dab8842b0c3ed53329663096dc  perl-5.42.0.tar.gz" | sha256sum -c -
        tar xzf perl-5.42.0.tar.gz
        cd perl-5.42.0
        ./Configure -des -Dprefix=/opt/perl-5.42 -Dman1dir=none -Dman3dir=none
        make -j"$(nproc)"
        make install
      fi

  It runs at the start of a session, and step 0 found it done: the
  download at 17:42:29, `Configure` finished by 17:42:59, perl built
  by 17:43:25 and installed by 17:44:05, so about a minute and forty
  seconds on four cores before the session can work. `perl -V:ivsize
  -V:nvsize` gives 8 and 8. The same script installs
  `libclang-rt-18-dev`, clang's sanitizer runtime, for `make
  sanitize`. On a Mac, any perl 5.42 will do (perlbrew, plenv, or the
  script above with another prefix), named by `CURLY_PERL`.
- Python 3 for `t/checks.py` and the models.
- `make doctor` checks the setup, and `t/run.sh t/000-say.pl` should
  end `1 tests, 0 failed`.

## Layout

| Path | |
|---|---|
| `bin/curlyc.ts` | The driver: `curlyc -o out file.pl` |
| `compiler/src/` | One file per pass: `lexer.ts`, `parser.ts`, `checker.ts`, `codegen.ts`; `ast.ts`, the tree; `names.ts`, the one table of names: statements, builtins, pragmas, operators (D29); `errors.ts` |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | `rt.h`, `rt.c`; `tests/`, C programs that call the runtime directly, each run by `rt.test.ts` |
| `t/` | Golden tests `NNN-name.pl` and `.expected`; `run.sh`; `checks.py`; `checks/`, the oracle check's own tests; `models/` |
| `docs/` | The documents above; `PROCESS.md`, `MODELS.md` and `REPORT.md`, the workbench's; `briefs/`, with `claims.py` (every statement about perl, as a program), `step1-review/` (a reviewer's model of step 1's language, and the scripts that ran the compiler against it), `step2-*` and `step3-strings-as-numbers.py` (the evidence for those steps' rules), `step3-mutations.py` (the runtime broken on purpose) and `step3-review/` (the reviewer's model of step 3, and the script that ran the compiler against it) |
| `exp/`, `tools/decisions/` | The workbench's: its experiments (`MODELS.md` cites them) and the decision-log browser |
| `build/` | Output (ignored) |

`docs/PLAN.md` has what is still to come: `lib/`, `examples/`,
`t/census/`.

## Commands

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`), which ask perl. About two minutes, most of
  it the oracle running perl eight times over each test.
- `make unit`, `make golden`, `make checks`: one at a time.
  `t/run.sh t/000-say.pl` runs one golden test; `JOBS=1` runs them one
  at a time.
- `make oracle`: writes each `same` and `dies` test's `.expected` from
  perl. That is how such a file is made; never by hand, and never from
  the compiler. It writes nothing for a test perl warns on or whose
  output moves with the hash seed.
- `make doctor`: each tool's version, and a failure for a perl that
  isn't 5.42 with 64-bit integers and doubles.
- `make golden-clang`: the golden tests with clang as the C compiler.
  `make sanitize`: with UBSan and ASan, every finding fatal. Neither
  is part of `make test`. `CURLY_CC=clang make unit` does the same for
  the runtime's own tests.
- `make models` reruns every model and writes its files;
  `make commits` checks the subjects since origin/main; `make hooks`
  installs the commit-msg hook.
- `make check`: `tsc --noEmit` (`npm install` once, for it).
- `python3 docs/briefs/claims.py`: every statement the documents make
  about perl, rerun. Not part of `make test`.
- `make decisions`: `build/decisions-curly.html`, a browser of the
  decision log.
- `node bin/curlyc.ts -o out file.pl`: compile and link. It writes
  `out.c` and `out.rt.o` (the runtime, compiled) next to `out`. Exit codes: 0 ok; 1 a refusal, `FILE:LINE:COL:
  message` on stderr and no binary; 2 usage, the toolchain, or a file
  it can't read or write; a fault in the compiler itself is `curlyc:
  internal error: ...` with Node's stack, and 2.
- `make census` comes with step 11.
- Environment: `CURLY_PERL`, the oracle (default `perl`); `CURLY_CC`,
  the C compiler (default `cc`); `TIMEOUT`, the seconds a golden test
  may run (default 60); `JOBS`. A compiled program reads none yet.

A compiled program prints to stdout and exits 0. A fault is `fault:
MESSAGE at FILE line N.` on stderr and exit 1, after whatever stdout
had. An uncaught `die` is its message on stderr and exit 255. The
golden tests check stdout and stderr together, plus `exit: N` when the
status isn't 0.
