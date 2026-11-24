# Curly

Curly is a cleaned-up Perl 5 with a runtime of its own. A program it accepts is
Perl 5.42 once its annotations are erased, and prints what perl prints
unless it stops loudly first; what Perl has that the language cuts is a
compile error or a fault, never a different meaning. The compiler is
TypeScript run by Node as it is, and emits C that links with a C
runtime. The driver is `curlyc`, and a program is a `.pl` file.

## Status

**Steps 0 to 2 of [`docs/PLAN.md`](docs/PLAN.md) are done**
(2026-11-24, all by Fable 5.2). **The language** is `use v5.42;` and
then any number of `say EXPR;` or `say(EXPR);`, where an expression is
a number, brackets, unary `-` and `+`, and `+ - * / % **`, with
perlop's precedence ([`docs/LANGUAGE.md`](docs/LANGUAGE.md)). **A
number is an Int (64 bits, signed) or a Num (a finite double)**, and
which one an operation gives is perl's own rule (D35): it is done on
whole numbers when both operands are *integral* (an Int, or a whole
Num below 2^53) and on doubles otherwise; `/` gives a Num, except an
Int past 2^53 divided exactly; `**` gives a Num for a base that is a
power of two, an exact Int when the base's bits times the power are at
most 64, and C's `pow` otherwise; `%` cuts a Num to its whole part.
**Faults** (D13): `integer overflow` (two Ints, or an answer perl
would keep as an unsigned integer), `float overflow` and `not a
number` (a Num is finite, D37), `division by zero`, `modulus by zero`,
`modulus of a number outside the integers`, and printing a whole Num
from 10^15 up to 2^53, which perl prints two ways (D36: `+ 0` makes
the Int). A fault names the line its statement starts on (D34).
**Literals** (D38): decimal; `1.5`, `.5`, `1e3`; `0x1F`, `0b101`,
`0o17` up to 32 bits; `_` between digits. **Refused**: a leading zero
(`017`), `1.`, a literal too large for its kind, a number hard against
a letter, digit or dot (T62, T78); `say (1 + 2) * 3;` (T25); `say`,
one blank and a bracket that doesn't end on its line (T76); `--`, `++`
and every other operator of perl's, as the longest token perl would
take (T27); a line that starts `#!` (D33).
**The compiler**: `lexer.ts` (the whole file, a line and column on
each token, every character checked there), `parser.ts` (precedence
climbing over perlop's table), `ast.ts` (`int`, `num`, `unary`,
`binary`, each with a position and a mark for brackets that were
written), `checker.ts`, `codegen.ts`, `names.ts` (`use`, `say`, and
all 25 rows of perlop's table, of which four are live), `errors.ts`,
and the driver `bin/curlyc.ts` (D3, D29). **The generated C** is
straight-line (D31): each operation a statement with its result in a
temporary, operands left before right, the statement's line stored in
the context first; a Num literal goes over as its 64 bits. **The
runtime**: the two-word value (D25), the context first in every call
(D28), `rt_say` and the seven operators, each checking its operands'
tags and asking the one question, `integral`. **Tests**: golden 000 to
009 (step 0); 010 to 026 from `t/models/arith.py` and 030 to 038 by
hand (step 1; 039 is retired); 040 to 074 from `t/models/num.py`
(about 14,600 lines on which the model and perl agree, and 27 programs
that each fault once at an edge) and 080 to 092 by hand (step 2); 40
unit tests, the runtime's own in C. **The oracle check**
(`t/checks.py oracle`, D10) holds every test to perl 5.42 by its kind,
and has 40 tests of its own in `t/checks/`; its seeds are eight of 64
hex digits (`PERL_HASH_SEED=1` to `8` are nearly one seed to perl).
Its reading rule for hashes is by pattern and errs toward rejecting;
step 12 will meet it first. Green under gcc, clang, and UBSan with
ASan. **Each step's language was reviewed adversarially** (step 1's:
nothing found, and the compiler agrees with the reviewer's own model
on 1,271,555 programs, `docs/briefs/step1-review/`). Each step's
runtime was broken on purpose until every breakage was caught; step
2's found three holes in its own tests that way.

**perl 5.42 was installed and everything rerun under it**:
`docs/briefs/claims.py` holds every statement these documents make
about perl as a program, 189 of them, and all hold under 5.42.0; under
5.38.2 they differ only where `docs/TRAPS.md` had said. T71 is settled
(5.42 prints `x's`). **Found at step 0**: T72, a line that starts
`#!`, from which perl takes switches when it calls that line 1 (the
first line, or any line after a `# line 1` comment), a WRONG in step
0's own language and so refused at once, on every line (**D33, a
default: Stevan to confirm**); T73, `use utf8;` must be on a line
before the first character past ASCII (step 3); T74, `# line N "file"`
comments (step 15); T75, `use v5.42#c`, which perl doesn't compile,
refused. **Found at step 1**: T76. [`docs/TRAPS.md`](docs/TRAPS.md)
keeps the programs, T1 to T82, by step; `claims.py` has 251 programs
now. **Two adversarial reviews** were run, of the step's
language and of the oracle check. The first found T75 and the `# line
1` half of T72 after the compiler was green: the rule about reviewing
a large step paid for itself on the smallest one. The second got wrong
tests past the check sixteen ways; the seeds were the worst of it.
What was cheap is closed, each with a fixture, and **what is left is
listed in `docs/TRAPS.md`, "The checks themselves", by the step that
has to close it** (15: a `dies` test that also warns; 21 and 22:
files, the environment, the clock; 16 and 19: quotes the reading rule
can't pair). A test with a sort in it breaks its ties.

**D1 to D38 are all Stevan's.** The ones a builder
meets first: the core rule (D2); a TypeScript compiler emitting C
(D3); a fault can't be caught (D13); perl's warnings are faults (D15);
loop variables are read-only and containers freeze (D17); a sub can't
see its context (D18); `class`, and `package` only as a namespace
(D19); brackets on a program's own calls (D21); a whole Num of 10^15
up to 2^53 faults when made a string (D23, D36), and a number is
integral or it isn't (D35); the name (D32). perigrin has
agreed to the probe corpus (D11). **Next:** step 3, strings, which is
an outline: it is **proposed first**, with options, and reviewed
adversarially before it is built. It decides D24's details, which
strings are numbers, and whether a program with text past ASCII must
say `use open`. The evidence for step 2's rule is kept:
`docs/briefs/step2-perl-numbers.py` (the rule against perl, 129,801
operations), `step2-history.pl` (the two places a number's past shows:
T35, T79) and `step2-literals.py` (perl reads and prints floats as C
does; run it on a new machine). One risk to watch on the Mac: `**`
with a fractional operand is the C library's `pow`. Not agreed: what
the decisions leave to steps, listed at the end of
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
| `compiler/src/` | One file per pass: `lexer.ts`, `parser.ts`, `checker.ts`, `codegen.ts`; `ast.ts`, the tree; `names.ts`, the one table of names (D29); `errors.ts` |
| `compiler/tests/` | Unit tests, per pass |
| `runtime/` | `rt.h`, `rt.c`; `tests/`, C programs that call the runtime directly, each run by `rt.test.ts` |
| `t/` | Golden tests `NNN-name.pl` and `.expected`; `run.sh`; `checks.py`; `checks/`, the oracle check's own tests; `models/` |
| `docs/` | The documents above; `PROCESS.md`, `MODELS.md` and `REPORT.md`, the workbench's; `briefs/`, with `claims.py` (every statement about perl, as a program), `step1-review/` (a reviewer's model of step 1's language, and the scripts that ran the compiler against it) and `step2-*` (the evidence for step 2's proposal) |
| `exp/`, `tools/decisions/` | The workbench's: its experiments (`MODELS.md` cites them) and the decision-log browser |
| `build/` | Output (ignored) |

`docs/PLAN.md` has what is still to come: `lib/`, `examples/`,
`t/census/`.

## Commands

- `make test`: the unit tests, the golden tests, then the mechanical
  checks (`t/checks.py`), which ask perl. About fifteen seconds.
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
