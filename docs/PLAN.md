# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** steps 0 to 3 were done on 2026-11-24: arithmetic on Ints
and Nums, and strings, compile, run, and are checked against perl
5.42. So do booleans, undef, comparison and logic, and variables,
assignment, blocks and `if`: **steps 0 to 5 are done** (steps 4 and 5
on 2026-11-25); and loops: **steps 0 to 6 are done** (step 6 the same
day). Stevan's Mac ran `make test` green after step 6. And the collector:
**steps 0 to 7 are done** (step 7 the same day). Steps
7 to 30 are outlines: each is proposed, with options, when it's
next.

[`TRAPS.md`](TRAPS.md) lists, by step, the programs where the obvious
implementation would be WRONG. A step's proposal starts from its rows,
and adds an adversarial review of its own before the build: someone
who didn't write the proposal, with perl to hand, trying to break it.

Read [`DESIGN.md`](DESIGN.md) first. Where a step meets an **(open)**
item, propose options to Stevan before building (see `CLAUDE.md`).

Each step carries a **Referee** line and a **Size** line, as the
workbench's do (`docs/PROCESS.md` and `docs/MODELS.md` there). In this
language the referee is perl wherever the step's tests are of kind
`same` (D10), so the line usually reads `Referee: perl`. A step that
is an exception to D2 names its own.

## Proposed layout

The workbench's, with these differences. `CLAUDE.md` has the layout
as built; what is here and not there is still to come.

| Path | |
|---|---|
| `bin/curlyc.ts` | The driver: `curlyc -o out file.pl` |
| `compiler/src/` | `lexer.ts`, `parser.ts`, `ast.ts`, `resolver.ts` (step 5), `checker.ts`, `codegen.ts`, `names.ts` (the one table, D29), `errors.ts` |
| `compiler/tests/` | Unit tests per pass |
| `runtime/` | `rt.h`, `rt.c`, and a file per subsystem as they come (`gc.c`, `str.c`, `re.c`); `tests/`, C programs that call it directly |
| `lib/` | The prelude and the libraries, in the language (step 23 on) |
| `t/` | Golden tests `NNN-name.pl` and `.expected`; `run.sh`; `checks.py`; `checks/`, the oracle check's own tests; `models/` |
| `t/census/` | Other people's probes and their verdicts (step 11) |
| `examples/` | Ports; each with a `.expected` is a golden test |
| `docs/` | These documents, and `LANGUAGE.md` |

There is no `t/referee/` until a step needs one: perl is the referee.

## Steps

Each step says what it adds, what it decides, what tests it adds, and
what it leaves out on purpose.

### 0. Scaffold: `say 42;` (done)

Referee: perl. Size: medium; large for `t/checks.py oracle`, which is
new and which everything after leans on.

Decisions: D3, D10, D12, D13, D16, D23 (the range of a literal), D25,
D28, D29, D30, D31, D32, all made. Traps: T24.

**Done, 2026-11-24**, by Fable 5.2, as written below, and with these
differences and findings:

- **perl 5.42 agrees with every statement these documents make about
  perl.** `docs/briefs/claims.py` holds each as a program (184 of
  them, the traps included) and reruns them; under 5.38.2 the same
  programs differ only where `TRAPS.md` had said they would. Three
  rows were corrected: T71 (5.42 prints `x's`), and T45 and T67, whose
  `use utf8;` has to be on a line of its own (T73).
- **Four traps were found**, T72 to T75. T72 was a WRONG in this
  step's own language (a line that starts `#!`), so it is refused, by
  a default: **D33, for Stevan to confirm.** T73 is step 3's and T74
  step 15's. T75 (`use v5.42#c`) is a program perl doesn't compile,
  and is refused.
- **Two adversarial reviews**, each by a reader who hadn't written
  the thing and had perl, as the working rules ask of a large step.
  One was given the definition of this step's language: it found T75
  and the half of T72 that a `# line 1` comment opens, both of which
  the compiler as first committed got wrong while every test passed.
  The other was given the oracle check and asked to get a wrong test
  past it, and did, sixteen ways. The worst: `PERL_HASH_SEED=1` to `8`
  are nearly one seed to perl, so the eight runs D10 asks for were
  catching far less than eight would. The check now uses seeds of the
  full width; what else was cheap is closed, and the rest is listed in
  `TRAPS.md`, "The checks themselves", by the step that owns it.
- **Golden tests 006 to 009** beside the six planned: a `#!` first
  line, a character past ASCII, a `#!` line after `# line 1`, and a
  comment hard against the version.
- **The fixtures in `t/checks/`** are forty, not six, and every rule
  of the check was broken on purpose to see a fixture go red.
- **A `fault` test must compile under perl in silence**, where D10
  says only that perl compiles it: a warning as perl compiles is a
  refusal (D15), so such a program is no fault test.
- **`# limit: seconds`** is a header the plan didn't have: the fixture
  that never ends under perl would otherwise cost every `make test`
  ten seconds.
- **The generated C doesn't set the context's line**: nothing can
  fault, so nothing could test it. Step 1 does, with its first fault.
- **The table of names holds `use` and `say`**, not yet every name
  perl knows (D21): that list is step 8's, where a sub could take one.
- **Kept from the workbench**, beyond what was listed: `exp/` (its
  experiments, which `MODELS.md` cites), `tools/decisions/` (`make
  decisions` works on this log), and `docs/briefs/`.

- **Start from the workbench template**: this branch holds only these
  documents, so bring `main`'s tree (af8e3a3) in under them (`git
  checkout origin/main -- .`, then restore these documents where the
  two collide: `CLAUDE.md`, `README.md`, `docs/DESIGN.md`,
  `DECISIONS.md`, `PLAN.md`, `LANGUAGE.md`, `BACKGROUND.md`; merge
  `t/README.md` as it says; keep the workbench's `PROCESS.md`,
  `MODELS.md` and `REPORT.md`), rename `lang` and `langc` to `curly`
  and `curlyc`, and remove the calculator: `reader.ts`,
  `sexp.ts`, its `codegen.ts`, `t/0*.lang`, `t/models/*.py`,
  `t/referee/`, the calculator's decisions and plan. Keep `t/run.sh`,
  `t/checks.py`, the `Makefile`, the driver and `runtime/` as
  shapes to rewrite.
- **The toolchain.** Node 22.18 or later; `cc`, and clang for `make
  golden-clang` and `make sanitize`; **perl 5.42** as `CURLY_PERL`
  (default `perl`). The cloud machine's perl is 5.38.2, so 5.42 has
  to be installed there: from cpan.org's source, which the machine
  can reach, by the environment's setup script (`CLAUDE.md`'s
  Toolchain has it). **Then rerun every "perl prints" in these
  documents and every row of `TRAPS.md` under 5.42**, before anything
  is built: they were run under 5.38.2. A row that differs is
  reported to Stevan, with both outputs, and corrected in the
  document that holds it. `TRAPS.md`, "The checks themselves", lists
  where the two versions are known to differ; look there first, and
  at whether a program's own `sub trim` or `sub ceil` is still called
  under `use v5.42` (it must be refused either way: D21).
  `make doctor` prints each tool's version and fails on a perl that
  isn't 5.42 with 64-bit integers and doubles (`perl -V:ivsize
  -V:nvsize`, 8 and 8).
- **The language at step 0.** A program is `use v5.42;` and then any
  number of `say N;`, where `N` is a decimal integer literal from 0 to
  9223372036854775807, written without a leading zero (`010` is 8 in
  perl, and `08` doesn't compile: T24). `#` starts a comment. That is
  all.
- **The lexer**: the whole file, a line and column (in code points) on
  each token; white space, comments, decimal integers, words, `;`,
  the version literal. A byte that isn't ASCII is a refusal for now
  (D16; step 3 brings `use utf8`).
- **The parser, the tree, the checker, the code generator**: each a
  file, each as small as the language. The generated C is one
  statement per `say` (D31).
- **The runtime**: the two-word value (D25), `rt_say`, the context
  that everything takes (D28), the fault path (D13): flush stdout,
  `fault: MESSAGE at FILE line N.` on stderr, exit 1. Nothing can
  fault yet; the path is built and unit-tested from C.
- **`t/run.sh`**: the workbench's, for `.pl`, and for the kinds: a
  `refused` test must fail to compile, and its `.expected` is the
  compiler's stderr and `exit: 1`.
- **`t/checks.py oracle`** (D10): for each test, by kind, as D10
  says. For `same`: `$CURLY_PERL -c FILE` with nothing on stderr, then
  `PERL_HASH_SEED=1` to `8`, `$CURLY_PERL -CSDA FILE`, each with empty
  stderr, the eight stdouts and statuses equal, and equal to the
  `.expected`. For `fault`: perl compiles the file, and the compiled
  binary's stdout alone is the start of perl's, with a time limit on
  perl. perl and the compiler are given the same path, from the
  repository's root. Then **make each check fail on purpose once** and
  keep those as the check's own tests, in `t/checks/`. The step-0
  language can't fault or warn, so these fixtures are not compiled
  programs: each is a Perl file (all of Perl is allowed in them) and
  a file standing for what a binary printed. One has a wrong byte in
  its `.expected`; one warns under perl; one prints a line perl
  doesn't before its fault; one perl can't compile; one never ends
  under perl; one prints unsorted keys.
- **Headers** (`# kind:` and the rest) are comments anywhere before
  the first statement, before `use v5.42;` too, since test 002 has no
  such line.
- **Golden tests**: 000 `say 42;`. 001 several lines: `say 0;`, the
  largest Int, a comment between. Both `same`. 002, `refused`: a file
  without `use v5.42;`. 003, `refused`: `say 9223372036854775808;`
  (perl prints it, as an unsigned; the language has none, D23). 004,
  `refused`: `say 010;`. 005, `refused`: `say 08;`.
- **Unit tests**: token positions; each refusal's message and position.
- **Documents**: `LANGUAGE.md` begun; `CLAUDE.md`'s Status, Toolchain
  and Commands; this heading marked done.
- Leave out: negative numbers (a unary minus, step 1), any other
  statement, any other literal, strings.

### 1. Integer arithmetic (done)

Referee: perl. Size: large for the model, medium for the build once
the model and its tests are red.

Decisions: D23 (the Int half), D13, D15 and D21 (the refusals below).
Traps: T25, T27.

**Done, 2026-11-24**, by Fable 5.2, as written below, and with these
differences and findings:

- **The model and perl agree on every line**: `t/models/arith.py`
  writes 10,592 lines over 58 edge values, and perl 5.42 prints the
  model's answer for each. It was committed red, before any code.
- **A test an operator** (010 to 014), not one test: gcc at `-O1` took
  36 seconds over the 10,592 statements as one C function. For the
  same reason the driver now compiles the runtime at `-O1` and the
  program's own C at `-O0`: the suite takes about six seconds.
- **Twelve fault tests** (015 to 026), at the edges of each operator,
  not one for each kind: a pair that should fault and doesn't is a
  WRONG that only a fault test can show.
- **T76 was found** probing the step's grammar: `say (1 +` with its
  bracket closing on a later line makes perl warn, so `say`, one
  blank and a bracket must end on its line. `say(...)` needn't.
- **D34, a default: a fault names the line its statement starts on**,
  as perl's own messages do. For Stevan to confirm.
- **The table of names has perlop's whole table** (25 rows, from
  5.42's own `perlop.pod`), and the lexer takes the longest operator
  in it: `--`, `**`, `<=>` and the rest are refused as the operators
  they are to perl, by name.
- **A very long or deep expression** (some thousands of terms, or of
  brackets) stops the compiler with a message and exit 2: its passes
  walk the tree by recursion. perl takes them. A limit to lift when
  a program meets it.
- **The oracle's `fault` half met real tests** and was failed on
  purpose: with overflow wrapping in silence, ten tests fail it.
- **An adversarial review of the step's language** found nothing: no
  program the definition accepts that perl treats otherwise, over
  about 1.2 million statements and half a million programs, many of
  them every string of up to seven fragments after `say`. The
  reviewer wrote its own model of the definition to do it, and **the
  compiler was then run against that model**, a second implementation
  nobody here wrote: the same 20,304 programs accepted of 1,271,555,
  the same output, the same faults (`docs/briefs/step1-review/`).
  What the review did note: perl prints an Int on some lines where
  the language faults (`say 0 * (9223372036854775807 + 1);` prints
  0), which D12 allows; and perl takes expressions a million terms
  long or brackets deep, where the compiler stops at some thousands.

- `say EXPR;` and `say(EXPR);`, where an expression is an integer,
  `( )`, unary `-`, and binary `+`, `-`, `*`, `%`, with `perlop`'s
  precedence and associativity. The precedence parser arrives here,
  with the whole of `perlop`'s table in `names.ts` though only these
  rows are live.
- **`say (1 + 2) * 3;` is refused** (T25): perl takes the brackets as
  `say`'s whole argument list and prints 3, with a warning. `say`,
  then brackets, then an operator is a refusal; `say((1 + 2) * 3);`
  and `say 3 * (1 + 2);` are fine, and so is `say +(1 + 2) * 3;`,
  which is 9: unary `+` is in from this step, as perl's own way of
  saying the bracket isn't an argument list. `--` and `++` are tokens, and
  refused (T27): `say --5;` doesn't compile in perl, and `say - -5;`
  is 5.
- **Faults**: a result outside Int is `integer overflow`; `% 0` is
  `modulus by zero`. Each is where perl would print something else (a
  float, an unsigned) or die.
- **The oracle's seeds** are eight of 64 hex digits (step 0 found
  that 1 to 8 are nearly one seed). Nothing in this step has a hash,
  so nothing here depends on them.
- `%` takes the sign of its right operand: `-7 % 3` is 2 and `7 % -3`
  is -2 (run under perl; C's `%` is the other rule, so the runtime
  can't just use it).
- **`t/models/arith.py` first**, red before any code: the four
  operators over the values that find the edges (0, 1, -1, 2^31,
  2^32, 2^53 and its neighbours, 2^63 - 1 and -2^63 built by
  subtraction, and what multiplies to just inside and just outside).
  (`docs/briefs/arith-review.py` is the script a review used to check
  this against perl: a starting point for the values, not the model.)
  From Python's integers and the definition it writes one `same` test
  of every pair whose result is an Int, a line each, every line
  written `say(EXPR);` (T25: an expression that starts with a bracket
  would otherwise be read as `say`'s arguments), and one `fault` test
  for each kind of fault. A review ran this model's shape against
  perl: 6,286 lines, all agreeing. Then `t/checks.py oracle` holds perl to
  the same answers: two derivations, and neither is the compiler's.
  Where the model and perl disagree, stop and report; that is a
  finding about D23, not a test to fix.
- **By hand**: precedence and associativity (`2 - 3 - 4`, `2 + 3 * 4`,
  `-2 * -3`, `2 * (3 + 4)`), a fault after output (the lines before it
  are printed, D12), `refused` tests for a missing operand, an
  unbalanced bracket, `say (1 + 2) * 3;` and `say --5;`.
- **The tree** (`compiler/src/ast.ts`) gets its shape here, since
  this is the first step with expressions. Start from the vocabulary
  of Crayon's `lib/Crayon/AST.pm` (`BACKGROUND.md`), with a position
  on every node, a flag for brackets that were written (T25, and list
  against scalar assignment later, need it), and none of its
  conflations: `return` is not loop control, a slice is not a
  subscript, a call through a reference is not a method call.
- **A fault's line**: the generated C stores each statement's line in
  the context (`cx->line`) before the statement, which step 0 left at
  0 since nothing could fault. The first `fault` test is also the
  first real use of the oracle check's `fault` half, which has only
  met fixtures: break it on purpose once (`t/checks/README.md`).
- **Runtime**: `rt_add`, `rt_sub`, `rt_mul`, `rt_mod`, `rt_neg`, each
  checking its operands' tags (nothing but an Int can reach them yet;
  the check is there for step 2) and overflowing by the compilers'
  builtins. The workbench's lesson applies as written: never a
  variable and the call that sets it in one argument list. `make
  golden-clang` and `make sanitize` before calling it done.
- Leave out: `/` and `**` (they give Nums, step 2), `++`, bit
  operators, hex and other literals, the smallest Int as a literal
  (`-9223372036854775808` is a minus applied to a refused literal;
  write `-9223372036854775807 - 1`).

### 2. Num, division, `**`, numeric literals (done)

Referee: perl. Size: large.

**Built 2026-11-24**, by Fable 5.2, as agreed below, and with these
differences and findings:

- **The model and perl agree on every line**: `t/models/num.py` writes
  040 to 047, about 14,600 lines over the edges, and perl 5.42 prints
  the model's answer for each; 048 to 074 fault once each. Committed
  red, before any code.
- **A line with `**` is in a test only if no last bit can change what
  it prints** (the answer one double up and one down prints the same),
  so that another machine's `pow` can't fail a test here.
- **The runtime was broken 22 ways on purpose, and three got through
  the first time**: a power of two as an Int where it must be a Num,
  the `**` test off by one at 65 bits, and a negated zero losing its
  sign. Each was a hole in the tests, not the runtime. The model has
  the missing edges now (a base of every number of bits, with the
  power on each side of 64; `1024 ** 5`), and
  `runtime/tests/zero.c` tests the sign of a zero from C, since no
  program can see it until `atan2` comes (T79). All 22 are caught.
- **Test 039 is retired**: it refused `**`.
- **The driver links `-lm`.**
- Not done here, and noted where it will be needed: a negative zero
  given to `atan2` or `%g` (T79; steps 16 and 22).
- **The adversarial review of the definition** (about 3.7 million
  statements against a model of its own) found one program the
  compiler accepted and perl refuses: a decimal literal of more than
  250 characters, which perl stops at with `Number too long` (T91).
  Refused now; test 093. And it **refuted the claim this step rested
  on**, that a number's past shows in two places only: an Int of 2^53
  or more that a double holds exactly, once used as a float, adds to
  a whole Num as a float (T92). Nothing built is wrong by it, there
  being no variables; step 3's proposal carries the amendment to D35
  (its Q7), and `--` on a Num is step 5's to settle (T93).

**Proposed 2026-11-24, and agreed the same day: Stevan took the
recommendation on each of the five questions below, which are now D35
(the rule, Q2), D36 (Q1), D37 (Q3) and D38 (Q4); Q5's names stand as
proposed.** The text is kept as it was proposed, questions and all,
since it is the reasoning. Everything here about perl was run under
5.42.0, and the scripts are kept:
[`briefs/step2-perl-numbers.py`](briefs/step2-perl-numbers.py) (every
operator over every pair of 147 edge values, 129,801 operations),
[`briefs/step2-history.pl`](briefs/step2-history.pl) (where a number's
past shows), [`briefs/step2-literals.py`](briefs/step2-literals.py)
(reading and printing a float), and `briefs/claims.py`.

Decisions it settles: D23 in full. Traps: T35 to T37, T40, T62, and
T77 to T82, found writing this.

#### The picture

A number is an **Int** (64 bits, signed, exact) or a **Num** (a
double). That much is D23. What this step has to say is which of the
two each operation gives, and D23 has already answered: whichever
perl gives. So the work was finding perl's rule. It is in perl's
source, and it is one question asked of each operand:

```
 Int ............................ integral      42, -7, 2**63 - 1
 Num, whole, below 2^53 ......... integral      3.0, 1e3, 1e15, 6 / 2
 Num, anything else ............. not           1.5, 0.1, 1e16, 2**62
```

**perl works on whole numbers, exactly, when both operands are
integral, and on doubles otherwise.** A float that happens to be whole
is quietly treated as an integer, up to the point (2^53) where a
double stops being able to hold every integer. That is why `1e15 + 1`
is `1000000000000001` and `1e16 + 1` is `1e+16`, and it is the whole
of what looked arbitrary in D23.

Following it has a price, which D23 named and this step measures. A
value in perl carries a mark of having been used as an integer, and
[`step2-history.pl`](briefs/step2-history.pl) tried 17 earlier uses
and 31 later looks on 41 values to find where the mark shows. **Two
places, and no others**: a whole Num from 10^15 to 2^53 - 1 prints as
`1e+15` before and `1000000000000000` after; and the negation of a
Num zero is a negative zero before and a plain zero after, which only
`atan2`, `sprintf("%g")` and a negative power can see (T79; steps 16
and 22). The language's values carry no mark, so it faults in the
first place (Q1) and will in the second when those builtins come.

#### The rule

| Operator | Both operands integral | Otherwise |
|---|---|---|
| `+` `-` | Exact. An Int, or `integer overflow` | The doubles, added: a Num |
| `*` | Exact, and an Int if it fits. If not: two Ints overflow, and so does an answer from 2^63 to 2^64 - 1 (perl's unsigned integers, Q2); past that the doubles are multiplied, a Num | The doubles, multiplied: a Num |
| `/` | The doubles, divided: a Num, so `6 / 2` is the Num 3. One exception: an Int past 2^53 that the right operand divides exactly gives the exact Int | The doubles, divided: a Num |
| `**` | For a whole power, 0 or more: a base of 0, 1, -1 or plus or minus a power of two gives a Num, exact; any other base gives the exact Int when (bits in the base) times (the power) is at most 64; otherwise as on the right | C's `pow`: a Num |
| `%` | As step 1 | Each operand is cut to its whole part, which must be an Int, and then as step 1: `10 % 3.7` is 1 |
| unary `-` | An Int: negated, or `integer overflow` for -2^63. A Num: its sign changed | |

`/` and `%` by zero fault, as perl dies. A Num is always finite: a
result that isn't faults (Q3). Precedence is perlop's: `**` binds
tighter than unary minus and groups from the right, so `-2 ** 2` is
-4, `2 ** 3 ** 2` is 512, and `2 ** -1` is 0.5.

`briefs/step2-perl-numbers.py` has this rule written out from these
words (`language`), beside a model of perl's own code (`model`), and
runs both against perl: the model of perl agrees with perl on all
129,801 operations, and wherever the rule gives a value, perl gives
the same value of the same kind. Step 1's programs mean what they
meant: two Ints are always integral.

What perl prints, and what the language does (each line was run):

| Program | perl prints | The language |
|---|---|---|
| `say 7 / 2; say 6 / 2;` | `3.5`, `3` | the same |
| `say 0.1 + 0.2; say 1 / 3;` | `0.3`, `0.333333333333333` | the same |
| `say 1e3 + 1; say 1e15 + 1; say 1e16 + 1;` | `1001`, `1000000000000001`, `1e+16` | the same |
| `say 10 ** 15; say 2 ** 10; say 2 ** 0.5; say 3 ** 40;` | `1000000000000000`, `1024`, `1.4142135623731`, `1.21576654590569e+19` | the same |
| `say 18014398509481984 / 2; say 9223372036854775807 / 2;` | `9007199254740992`, `4.61168601842739e+18` | the same |
| `say 1e10 * 1e10; say 5e9 * 5e9;` | `1e+20`, `2.5e+19` | the same |
| `say 5_000_000_000 * 5_000_000_000;` | `2.5e+19` | `integer overflow`, as D23 has it: two Ints |
| `say 1e10 * 1e9;` | `10000000000000000000` | `integer overflow`: perl's answer is an unsigned integer (Q2) |
| `say 9223372036854775807 + 1.0;` | `9223372036854775808` | `integer overflow`, the same way |
| `say 1e15; say 2 ** 50; say 4000000000000000 / 2;` | `1e+15`, `1.12589990684262e+15`, `2e+15` | a fault at `say`: each is a whole Num in the window (Q1). `say 1e15 + 0;` prints `1000000000000000` in both |
| `say 1e16; say 2 ** 62;` | `1e+16`, `4.61168601842739e+18` | the same: past 2^53 perl never takes a Num for an integer |
| `say 9**9**9; say 1e308 * 10;` | `Inf`, `Inf` | `float overflow` (Q3) |
| `say (-8) ** 0.5`, bracketed | `NaN` | `not a number` (Q3) |
| `say 1 / 0; say 1.5 / 0.0; say 0 / 0;` | dies, each | `division by zero` |
| `say 10 ** 4611686018427387904;` | `0`, and `9 **` the same is `1` | `float overflow`: perl's test for "fits in 64 bits" wraps (T77) |

#### The questions

**Q1. Where a whole Num faults when it is made a string.** D23 says
"10^15 or more". The measurement says the past shows only from 10^15
to 2^53 - 1: at 2^53 and beyond perl never treats a Num as an
integer, so `say 1e16` and `say 2 ** 62` print one way always.
(a) **Recommended: fault from 10^15 up to, not including, 2^53**
(9007199254740992). It agrees with perl on everything D23's line
would have faulted needlessly. (b) As D23 has it, 10^15 or more:
one bound to remember instead of two, and `say 1e16` faults.
Either way `+ 0` is the way through, in perl and here: it makes the
Int. The message needs your ear; proposed: `fault: a whole float this
size prints two ways in perl (add 0 to print the integer)`.

**Q2. Overflow with a Num in it.** D23 settled two Ints: overflow
faults. With a Num among integral operands, perl's exact answer can
still leave the Ints, and then: from 2^63 to 2^64 - 1 perl keeps an
exact unsigned integer, which the language doesn't have, so that has
to fault; beyond, perl multiplies the doubles and gives a Num.
(a) **Recommended: as the table has it.** `1e10 * 1e10` is `1e+20`,
as a float program expects, and `1e10 * 1e9` faults, which is odd
but narrow and loud. For `+` and `-` the table is simpler than perl
(any answer outside the Ints faults): the case needs an Int within
2^53 of either end. (b) Fault whenever whole-number arithmetic
leaves the Ints, Num or not. One sentence instead of three, and
`1e10 * 1e10` and `1.5e10 * 1e10` fault, since both are whole.

**Q3. Infinity and NaN.** perl has both as values, prints `Inf`,
`-Inf` and `NaN`, and gets them silently from `9**9**9`, `1e308 *
10`, `0 ** -1`, `(-8) ** 0.5`, and the literal `1e400`.
(a) Values, as perl. Then every later step owes perl's answers for
them: `NaN <=> 1` is undef, `-7 % (9**9**9)` is `Inf`, the strings
`"inf"`, `"nan"` and `"Infinity"` are numbers, and a negative zero
shows through `0 ** -1` (T79).
(b) Infinity a value, NaN a fault. Keeps `my $min = 9**9**9;`, the
idiom for "larger than anything". Needs `0 ** -1` to fault as a
division by zero, and `%` to refuse an infinity.
(c) **Recommended: both fault. A Num is finite.** `float overflow`
for a result too large, `not a number` for one with no real answer,
and a float literal too large for a double is refused. It is what
the Ints already do at their ends, it removes a family of perl's
oddest answers from every later step, and it costs the `9**9**9`
idiom, loudly. (perl 5.40 has `inf` and `nan` builtins of its own;
both are still experimental and warn, so neither is a way round.)

**Q4. Which literals.** In, as perl has them: `1.5`, `.5`, `1e3`,
`1.5e-3`, `1E3`; hex, binary and octal as `0x1F`, `0b101`, `0o17`,
in either case, up to 32 bits (past that perl warns `non-portable`,
so D15 refuses); `_` between two digits (`1_000`, `0xff_ff`; perl
warns of any other: T82). Two cuts proposed:
- **Octal by a leading zero, `017`: cut.** It is the trap T24 was
  written about (`010` is 8), `0o17` says it plainly, and a leading
  zero then stays the refusal it is today. `SURFACE.md` has it In.
- **`1.`, a point with nothing after it: cut.** `.5` stays. Nobody
  writes `1.` on purpose, and from step 3 a dot after a number is
  concatenation (`say 1.5 .5;` prints `1.55`: T78).
Also refused, with nothing to choose: a hex float (`0x1p3`: Later
in `SURFACE.md`); a number hard against a dot or another number
(T62, T78); a digits-only literal past 2^63 - 1, which perl turns
into an unsigned integer and then a float in silence (T81): write
`1e19`.

**Q5. The faults' names.** `integer overflow` (also for the
unsigned band of Q2), `division by zero`, `modulus by zero` (step
1's), `float overflow`, `not a number`, `modulus of a number outside
the integers` (for `1e20 % 7`: perl has an answer, by another
route), and Q1's. Say if any should read otherwise.

#### How a Num prints

As perl prints it, which is C's `%.15g`: `0.1 + 0.2` is `0.3`, `1e21`
is `1e+21`, `1 / 3` is `0.333333333333333`, `3.0` is `3`. A zero
prints `0` whatever its sign. perl reads a decimal literal to the
correctly rounded double, as C, Python and JavaScript do
(`briefs/step2-literals.py`: 60,029 literals, no difference in the
reading or the printing), so the compiler reads it with JavaScript's
own and writes the double's bits into the C.

#### The build, once the questions are answered

- **`t/models/num.py` first, red before any code**: the rule above
  from Python's integers and floats (and C's `pow`, through
  `ctypes`), over the edges, a test an operator as `arith.py` does,
  and a fault test for each kind of fault at each edge. The oracle
  holds perl to the same answers. `briefs/step2-perl-numbers.py` is
  its starting point and is not it.
- **An adversarial review of this proposal** before the build, as the
  rules ask; and the compiler held to the reviewer's model, as step 1
  was.
- **Lexer**: the numeric literals, each a token with its text; the
  refusals of Q4. **Tree**: a `num` node beside `int`. **Names**: `/`
  and `**` live, in the rows they already have. **Checker**: a
  literal's range. **Code generator**: a Num literal as its 64 bits.
  **Runtime**: the Num tag; `rt_div` and `rt_pow`; each of step 1's
  operators asking the one question; `rt_say` for a Num; the faults.
- **By hand**: precedence and grouping of `**`; every literal form;
  each refusal; the lines of the table above as tests.
- **One risk to watch on the Mac**: `**` with a fractional operand is
  the C library's `pow`, and two libraries can differ in the last
  bit. perl and the compiled program use the same one on the same
  machine, but the `.expected` files are written on this one. `+ - *
  /` are exact by IEEE and can't differ.
- Leave out: comparison (step 4), strings as numbers (step 3),
  `int`, `sqrt`, `abs` and the bit operators (step 22), `++`.

### 3. Strings (done)

Referee: perl. Size: large.

**Built 2026-11-24**, by Fable 5.2, as agreed below, and with these
differences and findings:

- **The model first, and perl agreed with it almost everywhere.**
  `t/models/str.py` writes 100 to 116 (about 15,000 lines: every
  operator over strings and numbers at the edges of D40, every way of
  writing a number in a string, `substr` and `index` over every
  position, the rest) and 62 programs that fault once each. perl 5.42
  printed the model's answer for every line but one family, below.
  The compiler passed all of them the first time it ran.
- **`substr` has a second way to be outside its string** (T96): a
  piece that starts and ends before the beginning. perl warns, so it
  faults; the proposal had only the start past the end. The model
  found it, 90 lines of 995.
- **Five more refusals and faults than the proposal had, each because
  perl warns or answers with garbage**, found by the model's tests
  and by writing the hand tests: a sign after a named unary operator
  that perl calls ambiguous, `length - 5` (T94); `\x` with one hex
  digit, and an octal escape cut short by an 8 or a 9 (T95); a count
  or a character's number below zero before it is cut, `"a" x -0.5`
  (T98); a whole number wanted that isn't an Int once cut, where
  perl's `substr("abc", 0, 1e30)` is `ab` (T97). And one refusal of
  taste: a backslash before a tab or the end of a line. D41 to D44
  carry them.
- **One thing the proposal's table had and the first rule didn't**: a
  string of the digits of -2^63 is that Int. The evidence script holds
  under every past without the special case that had faulted it.
- **`-CSDA` is gone from the oracle** (D39), and three fixtures in
  `t/checks/` go red if it comes back: it was put back on purpose to
  see them fail.
- **The lexer keeps its own count of where it is**: after a value a
  dot is an operator and `x` is one. D29 has the parser tell the
  lexer; the token before says the same, until `/` can begin a
  pattern.
- **Strings are on the heap and never freed** while the program runs:
  a list of blocks on the context, released at the end and at a
  fault, so the sanitizers find nothing left. Step 7 brings the
  collector.
- **Test 092 changed sides**: `say 1.5 .5;` was refused and is now
  perl's `1.55`.
- **The runtime was broken 70 ways on purpose** (kept:
  `briefs/step3-mutations.py`). Eight got through. Six were holes in
  the tests, each closed by a fault test (180 to 186): a fault that
  never happens is invisible to a test of what prints, so every fault
  needs a test of its own at its edge. Two changed nothing a program
  can see, and one of those was a condition that could never be
  false, since removed.
- **The adversarial review of the definition** was run beside the
  build, by a reader with only the proposal's words and perl, who
  wrote a model of its own: 2.9 million statements with literal
  operands (no disagreement in arithmetic at all: where the rule
  doesn't fault, its answer is perl's), 1.2 million random statements
  over the whole grammar, and 82 million cases of one value used two
  ways. Twelve findings. Eight the build had met already (T94 to
  T98). Four it had not, and each is fixed, with a test: `say ("(");`,
  where perl counts the bracket in the string and warns (T100);
  `say(("a") x 3)`, a list to perl (T101, refused until step 9); a
  string like `"1.99999999999999999"` where a whole number is wanted,
  which perl cuts to 1 or to 2 by its past (T103: **the claim that a
  value's past shows nowhere the rule doesn't fault was refuted again,
  in this one place, and holds on the 82 million cases with it
  closed**); and a sign on the line below a named unary operator.
- **One finding was a question, T102, and is D46 now.** perl works a
  constant `x` out as it compiles, so a count too large for memory
  stops perl before the program starts, having printed nothing, where
  the language prints what came before and faults. That isn't the
  beginning of what perl prints (D12). Stevan's answer (2026-11-25):
  a perl that runs out of memory as it compiles is outside the
  promise. The other option was a constant folder in the compiler.
- **The compiler was held to the reviewer's model and to perl**
  (`briefs/step3-review/compiler.py`): 106,000 random statements over
  the whole grammar, half of them with newlines and comments for
  blanks. The model prints for 55,002 of them; the compiler prints
  what perl prints for 54,969 and refuses 33, each for one of two
  rules where it is stricter than the model (brackets round the left
  of `x` in `say`'s argument; a sign on the line below a named unary
  operator). Of the statements the model faults on or refuses, 1,800
  were tried one to a program. Nothing WRONG.
- `make test` takes about two minutes now, most of it perl run eight
  times over each test by the oracle. No test asks perl for a long
  string: the first draft of two did (2 GB, as perl compiled them,
  eight times each), and the machine killed processes for it.
- An identifier past ASCII (SURFACE had it at this step) waits for
  step 5, where names begin.

**Proposed 2026-11-24, and agreed the same day: Stevan took the
recommendation on each of the seven questions below, which are now
D39 (Q1), D40 (Q2), D41 (Q3), D42 (Q4), D43 (Q5), D44 (Q6) and D45
(Q7, which amends step 2's D35).** The text is kept as it was
proposed, since it is the reasoning. Everything here
about perl was run under 5.42.0:
[`briefs/step3-strings-as-numbers.py`](briefs/step3-strings-as-numbers.py)
(strings and numbers under every past perl can give them: 41,594
operations) and `briefs/claims.py`. Traps: T34, T38, T45, T47, T57,
T69, T73, T78, and T83 to T93, found writing this and by the review
of step 2.

#### The picture

A third kind of value, the **Str**: a sequence of Unicode characters,
immutable (D24). This step brings the literals, `.` and `x`, seven
builtins, `print`, and the two crossings between strings and numbers.

```
   "12" + 1        a Str where a number is wanted  --->  Int or Num     (Q2)
   "n = " . 0.3    a number where a string is wanted --->  Str          (settled: what say prints)
```

A number as a string is settled: what `say` prints (D36's fault
included). **A string as a number is the hard half**, and D23 saw
only part of it. perl decides what a string is worth the first time
it is used as a number, and keeps the answer in the value; and it
decides differently for a first use that wants an integer and one
that wants a float. So one string can have two numeric values:

```
my $s = "3.0";                            my $s = "3.0";
                                          my $t = $s > 0.5;
say $s + 9007199254740990;                say $s + 9007199254740990;
# 9.00719925474099e+15                    # 9007199254740993
```

`step3-strings-as-numbers.py` asks perl for every answer it can give
(each operand fresh, after a float use, after an integer use): for
9,596 of 41,594 operations there is more than one. A value in the
language has no past, so the rule has to give perl's answer where
every past agrees and fault where they differ (Q2). The review of
step 2 found the same thing in plain numbers, where step 2's own
search had missed it (Q7).

#### The language at step 3

- **Literals.** `'...'` with `\\` and `\'`. `"..."` with the escapes
  of Q5, and no interpolation: an unescaped `$` or `@` is refused
  until step 16 (T34). A string may run over lines.
- **`.`** joins two values as strings, at the level of `+` and `-`.
  **`x`** repeats a string, at the level of `*`: `"ab" x 3`.
- **Builtins**: `length`, `uc`, `lc`, `ord`, `chr`, `substr` (reading,
  two or three arguments), `index` (two or three). Q3.
- **`print`**, as `say` without the newline: one argument, a statement.
- **`use utf8;`** for a source with characters past ASCII, on a line
  before the first of them (T73); **`use open`**, Q1.
- A Str where a number is wanted, and a number where a string is.

Left for later steps, and refused until then: interpolation, `q`,
`qq`, heredocs, `sprintf`, `join`, `reverse`, `ucfirst`, `lcfirst`,
`rindex`, four-argument `substr` (16); `eq` and the comparisons (4);
lists, so `say "a", "b";` (9, 10); case mapping past ASCII (T45).

#### The questions

**Q1. Text past ASCII on standard output.** D24 says the streams are
UTF-8, and the oracle runs perl with `-CSDA` to make perl agree. But
the file alone doesn't say so: plain `perl FILE` prints `é` as the
one byte E9, and `☺` as UTF-8 with a `Wide character` warning.
(a) As it is: nothing in the file, and D2 carries a footnote, "with
perl's streams as UTF-8".
(b) **Recommended: the file says it, and only when it needs to.**
`use open ':std', ':encoding(UTF-8)';` joins the closed list of
pragmas (D16), after `use v5.42;` and beside `use utf8;`. With it,
plain perl prints UTF-8, and so does the language. Without it,
printing a character past ASCII is a fault, since perl would print
something else (one byte) or warn. A program that prints only ASCII
needs nothing. The oracle then runs plain `perl FILE`, with no
switches, which is D2 as written; D10's `-CSDA` goes. It is also what
your own style guide asks for.
(c) Require the line in every program: no fault to explain, and
three lines of preamble on `say 42;`.

**Q2. Which strings are numbers, and what of the two answers.** In
silence perl takes: digits; digits with a point; an exponent; a sign;
blanks before and after (so `"12\n"`, a line just read, is 12). It
warns on anything else (`""`, `"abc"`, `"12abc"`, `"0x10"`,
`"1_000"`), so those fault (D15). It also takes `"Inf"`, `"NaN"` and
`"0 but true"` in silence: D37 makes the first two faults, and I
propose the third is one too. Then, by how the string is written:

| The string | perl, by the string's past | Proposed |
|---|---|---|
| Digits: `"12"`, `" -12 "`, `"012"` (which is 12) | always the integer | The Int; a fault past the Ints |
| An exponent, whole, below 2^53: `"1e3"`, `"1.5e1"` | always the integer | The Int |
| An exponent, whole, 2^53 or more: `"1e16"` | the integer, or the float: `"1e16" + 1` is `10000000000000001` or `1e+16` | A fault (D23 has this) |
| A point or exponent, not whole: `"1.5"`, `".5"`, `"1e-3"` | always the float | The Num |
| A point, no exponent, whole, below 2^53: `"3.0"`, `"5."`, `"0.0"` | the float, or the integer once it has been used as a float | See below |
| A point, whole, 2^53 or more: `"10000000000000000.0"` | always the float | The Num |

The fifth row is the new one. `"3.0" + 1` is 4 either way, and the
two answers differ only when something is too large for a double to
hold exactly, as in the example above.
(a) **Recommended: such a string is the Num, arithmetic with it is
float arithmetic (perl's answer for a string with no past), and it
faults when whole-number arithmetic would have given another answer**:
when the other operand, or the exact answer, is 2^53 or more. So
`"3.0" + 1` is 4, `"10.00" * 3` is 30, and the example above faults.
The model has this rule and never gives a value perl doesn't, under
any past, on the 41,594 operations.
(b) A string with a point or an exponent that is whole is not a
number at all: `"3.0" + 1` faults. One sentence, and a price list
read from a file stops at `"10.00"`.

A minus sign before a string has the same trouble, and one more:
perl negates `"+0"` as text, into the string `-0`. Proposed: the
string must be a number, the answer is a Num, and a whole number of
2^53 or more, or a string that starts with `+`, is a fault. T47's
`-"foo"` (which perl makes `-foo`) is a fault as not a number.

**Q3. The builtins, and how they are called.** `length`, `uc`, `lc`,
`ord` and `chr` take one argument, and are written as perl's named
unary operators are, with brackets or without: `length $s` in time,
`length "abc"` now. Without brackets the argument runs over
arithmetic and `.` and stops before a comparison, which is perl's
rule and has a trap in it that falls out loudly: `length "abc" + 1`
is `length("abc" + 1)`, a fault. `substr` and `index` take two or
three arguments, and **I propose brackets are required on them**:
perl allows `substr $s, 0, 1`, and it is the list-operator parsing
D21 is wary of, for a spelling nobody uses. (`ord` and `chr` aren't
in the outline; D24 needs some way to make a character and to look
at one.) What they do at the edges is perl's, enumerated by the
model: `substr("abcdef", -9, 3)` is empty in silence, and
`substr("abcdef", 7)` warns, so that one faults (`substr outside of
string`). `uc` and `lc` fault on a character past ASCII until a step
brings perl's tables (T45).

**Q4. Which characters a string may hold.** perl's strings hold any
number as a "character": surrogates, numbers past U+10FFFF, anything
below 2^63. It builds them in silence and warns when one is printed.
(a) **Recommended: a character is a Unicode scalar value** (0 to
U+10FFFF, less the surrogates). `chr` of anything else is a fault,
and such an escape in a literal is refused. The 66 noncharacters
(U+FFFE and its kin) are characters, and printing one is a fault,
because perl warns there (D15).
(b) As perl: anything in a string, and the fault only at printing.

**Q5. Escapes in double quotes.** In, as perl has them: `\n \t \r \f
\b \a \e \0`; `\\ \" \$ \@`; `\x41`, `\x{263A}`; octal `\101`
and `\o{101}`; `\N{U+263A}`. A backslash before any other
punctuation mark is that mark (perl says nothing). Refused: a
backslash before any other letter or digit (`\q`, `\8`: perl warns);
`\x` with no digits after it, and `\x{}` (perl gives a NUL, in
silence: T86); `\c`; `\N{name}`, which needs the names of every
character; and `\U \L \u \l \Q \E \F`, which belong with
interpolation (step 16).

**Q6. Small cuts, and the faults' names.**
- `x` is a word on its own: `"ab" x 3`. `"ab"x3` and `"ab" x3` work
  in perl and are refused (T57). Its count is cut to a whole number;
  a negative one is a fault (perl warns), as is a string that isn't a
  number.
- A dot after a blank is concatenation, as in perl: `1 .5` is `15`
  (T90). Hard against a number it stays refused (D38).
- New faults: `not a numeric string`; `two answers in perl` for Q2's
  cases (the wording to be settled with the code); `substr outside of
  string`; `negative repeat count`; `not a character` (Q4); `a
  character past ASCII printed without use open` (Q1); `uc` and `lc`
  past ASCII.

**Q7. A hole in D35, found by the review of step 2.** D35 says two
integral operands are added, subtracted and multiplied as whole
numbers. perl has a shortcut in front of that rule: when both
operands carry a float, it works in floats; and an Int that has been
used as a float carries one from then on, if a double holds it
exactly.

```
my $x = 10000000000000000;                my $x = 10000000000000000;
                                          my $t = $x / 3;
say $x + 1.0;                             say $x + 1.0;
# 10000000000000001                       # 1e+16
```

Without variables nothing has a past, so nothing built is wrong: `say
10000000000000000 + 1.0;` prints `10000000000000001` in perl and
here. From step 5 it would be. The two answers always differ in what
they print, so the only sound rule is a fault.
(a) **Recommended: in `+`, `-` and `*`, a whole number of 2^53 or
more that a double holds exactly (10^16, 2^60, a nanosecond clock)
faults when the other operand is integral and not an Int**: a whole
Num, or a string. With another Int, perl works on integers whatever
came before, and nothing changes; with a Num that isn't whole it
works on floats whatever came before. Two Ints are the common case
and are untouched. The model has this, and holds under every past.
(b) Leave D35 as it is until step 5, and decide there. The rule would
then change under programs already written against it.

#### The build, once the questions are answered

- **`t/models/str.py` first, red before any code.** Python's `str` is
  D24's string, code point for code point. The model writes: every
  operator over strings and numbers at the edges of Q2; `substr` and
  `index` over every position from well before to well past each of a
  few strings; `x`, `.`, `length`, `ord`, `chr`, `uc`, `lc`; and a
  fault test for each fault. perl confirms each line.
  `briefs/step3-strings-as-numbers.py` is its starting point.
- **An adversarial review of this proposal** before the build, and of
  the claim behind Q2 (that a string's past shows nowhere the rule
  doesn't fault).
- **The lexer learns where it is**: after a value, a dot is an
  operator and `x` is one; before one, a dot begins `.5` (D29 said
  the parser would tell it). **Strings on the heap**, allocated and
  never freed until step 7 brings the collector. **The oracle** loses
  `-CSDA` if Q1 is (b).
- Leave out: everything listed above as later.

### 4. Booleans, undef, comparison, logic (done)

Referee: perl. Size: large.

**Built 2026-11-25**, by Fable 5.2, as agreed below, and with these
differences and findings:

- **The model and perl agree on every line**: `t/models/bool.py`
  writes 300 to 307, about 13,000 lines (every comparison over the
  edges of D35 and D40, truth of every kind of value, what each
  logical operator gives, a boolean wherever a number or a string is
  wanted, what is not worked out) and 40 programs that fault once
  each, an undef in every place that wants a value among them. perl
  5.42 printed the model's answer for each.
- **The model was not written first this time.** The compiler was,
  and the model the same hour, from the definition and not from the
  compiler; it found nothing in the runtime. The order matters less
  than that the two are separate derivations, but the plan said
  model first, and step 5 should do it that way.
- **One refusal more than the proposal had** (T109, D51): in a list
  of arguments a word operator takes the list. `substr("abcdef", not
  0, 1)` is `abcdef` in perl, in silence, `not` having taken `0, 1`.
  So `not`, `and`, `or` and `xor` are in brackets of their own there.
- **T101's refusal follows the list down** (T104): through the right
  of `||`, `&&`, `//`, `or`, `and` and both branches of `? :`.
- **The generated C has its first branches**: an operand that may not
  be worked out is an `if` round its statements, with the value in a
  temporary declared before it. Breaking that on purpose, both ways,
  fails tests 305, 307 and 362.
- **The runtime was broken 50 ways on purpose**
  (`briefs/step4-mutations.py`): 49 caught the first time, and the
  other changes nothing a program can see (a whole Num is below 2^53,
  so beside it an Int's double is on the same side as the Int).
- 364 and 360 to 363 are by hand with perl's answers: how the new
  rows group, each line chosen so that a wrong grouping prints
  something else; 380 to 407 are the refusals.
- **The adversarial review of the definition** ran beside the build:
  1.26 million random statements over the whole grammar, 950,000
  comparisons, and a search of pasts by a method of its own (every
  state perl can put a variable in, found breadth-first through 134
  kinds of use, then every look in every state: 18 million looks; and
  207,000 whole programs). **The claim that no comparison, test of
  truth or boolean turns on a past the language doesn't fault was not
  refuted**, the first of three such claims to stand. Two findings.
  One the build had met (T109). The other is new in perl 5.42: it
  warns of a precedence problem when an unbracketed `!` is the left
  operand of a comparison, `!$x == $y` (T115). Refused now, test 407;
  D50 carries it.
- **The compiler was held to the reviewer's model and to perl**
  (`briefs/step4-review/compiler.py`), as step 3's was: 83,000
  random statements, of which the model prints for 37,103. The
  compiler prints what perl prints for 36,866 and refuses 236, by
  rules where it is the stricter (a bare `not` as a last argument,
  `!` before `<=>`). The one left over is D46's case: a constant
  perl can't build, in an operand that is never worked out.

**Proposed 2026-11-25, and agreed the same day: Stevan took the
recommendation on each question below, which are now D47 (Q1), D48
(Q2), D49 (Q3, and what had nothing to choose), D50 (Q4) and D51
(Q5).** The text is kept as it was proposed. Everything here about perl was run under
5.42.0: [`briefs/step4-comparisons.py`](briefs/step4-comparisons.py)
(every comparison, test of truth and boolean in arithmetic, under
every past of each operand) and `briefs/claims.py`. Traps: T33, T39,
T51, and T104 to T108, found writing this.

#### The picture

Two more kinds of value, and the operators that ask questions.

```
            as a number      as a string       true?
 undef      a fault          a fault           no
 false      0                ""                no
 true       1                "1"               yes
 Int, Num   itself           as say prints     unless it is zero
 Str        by D40           itself            unless it is "" or "0"
```

A comparison gives a **boolean**: `true` or `false`, which are also
words a program may write. **undef** is the one value that is no
value: asking whether something is defined, or true, is all that may
be done with it. Then the ladder, perlop's, tightest first; this step
adds what is in capitals:

```
 **
 NOT-SIGN !, and the signs - +
 * / % x
 + - .
 length uc lc ord chr DEFINED            (the named unary operators)
 < > <= >= LT GT LE GE
 == != <=> EQ NE CMP
 &&
 || //
 ? :
 NOT
 AND
 OR XOR
```

**What I expected to be the hard part wasn't.** Steps 2 and 3 each
claimed that a value's past shows nowhere their rule doesn't fault,
and each had that refuted by a review. So before writing this I asked
perl first: 57,376 numeric comparisons, each under 25 pairs of pasts
(fresh, used as a float, as an integer, as a string, as both), 12,412
string comparisons and tests of truth, and 2,400 uses of a boolean in
arithmetic. perl has more than one answer for 8,609 of the
comparisons, every one of them a string D40 already faults on. The
rule is D35's one question again and needs no new fault. (The reason
is in perl's source: it marks a number as carrying a float only when
the float is exactly the number, so two whole numbers past 2^53 that
differ are never compared as the one double they share.) The review
will try to refute it with more pasts than my five.

What is hard is how perl reads the words, which is where Q2, Q4 and
Q5 come from.

#### The language at step 4

- **`true` and `false`**, bare; and the results of the comparisons,
  of `!`, `not`, `xor` and `defined`. Q1.
- **`undef`**, bare, and **`defined`**, a named unary operator like
  `length`. Q2.
- **`== != < <= > >=`** and **`<=>`**: both operands as numbers
  (D40: a string that isn't a number faults). Both integral, the
  whole numbers compared exactly; otherwise the doubles compared, so
  `9007199254740993 == 2 ** 53` is true, as in perl (T39). `<=>` is
  the Int -1, 0 or 1.
- **`eq ne lt le gt ge`** and **`cmp`**: both operands as strings, a
  number being what `say` prints for it (so `10 lt 9` is true, `0.1 +
  0.2 eq 0.3` is true where `==` is false, and D36's fault applies),
  compared character by character. No locale.
- **Truth is perl's**: false is undef, `false`, a number that is
  zero, the empty string, and the string `"0"`. `"0.0"`, `"00"` and
  `" "` are true.
- **`!`**, at the level of the signs, gives a boolean. **`&&`, `||`
  and `//`** give one of their operands, not a boolean: `2 || 3` is
  2, `0 && 1` is 0, and `//` asks defined, not true. The right
  operand is not worked out unless it is needed, so `1 || 1 / 0` is
  1, and a fault there doesn't happen. **`? :`**, grouping from the
  right, works out one branch.
- **`not`, `and`, `or`, `xor`**: `not` and `xor` give booleans, `and`
  and `or` an operand. Q5.
- Faults: `undef where a number is wanted`, `undef where a string is
  wanted` (which is what `say undef` is).

Left for later, and refused: `^^` (new in 5.40), `~~`, the bit
operators and shifts, `<` `>` chains (Q4), `unless`-style words,
assignment.

#### The questions

**Q1. What a boolean is, when it isn't being tested.** perl prints
`true` as `1` and `false` as an empty string, adds them as 1 and 0,
and says nothing: `say 1 == 2;` prints an empty line, `true + 1` is
2, `false . "x"` is `x`. And false is not the empty string: `"" == 0`
warns and `false == 0` doesn't.
(a) **Recommended: as perl.** A boolean is a kind of its own; as a
number it is the Int 1 or 0, as a string `"1"` or `""`, in silence.
D15 already says what perl does silently stays, and `$count += $x >
3` is ordinary Perl. The script holds "the Int 1 or 0" to perl beside
every other operand under every past.
(b) A boolean is only for testing: as a number or a string it faults,
printing included. Stricter than perl in the way a typed language
would be, and `say $a == $b` stops.

**Q2. Where `undef` may stand.** To perl `undef` is an operator that
takes an argument, the thing to make undefined, and it takes what
follows for one whenever it can (T105): `undef * 2` is undef of a
glob called `2`, in silence; `undef + 1`, `undef < 1` and `undef x
3` don't compile; `undef == 1` and `undef // 1` are read as written.
(a) **Recommended: bare `undef` may be followed by `)`, `,`, `;`,
`?`, `:` or a logical operator (`//`, `||`, `&&`, `and`, `or`,
`xor`), and by nothing else.** That is every place it is useful.
Before any other operator it is refused, with a message that says to
write `(undef)`; and there it faults when the program runs, since
undef is no number and no string (D15). `undef(...)` with an
argument is the operator on a variable, already cut.
(b) Always in brackets, `(undef)`, wherever it is an operand: one
rule, and `$x // undef` needs brackets it doesn't need in perl.
With either: **`length(undef)` is undef**, in silence, as perl has
it, and `defined`, `//`, `!` and the tests of truth take an undef;
everything else that wants a number or a string of it faults.

**Q3. Nothing to choose, but worth your eye: `&&` and `||` give an
operand.** `say 0 || "x";` prints `x` and `say 5 && 7;` prints 7. It
is what makes `$x || "default"` work, and it means these two are not
"boolean operators" in the language's types later (step 25). The
alternative, booleans only, isn't Perl.

**Q4. Chains.** Since 5.32 perl chains comparisons of one row: `1 < 5
< 3` is `1 < 5 && 5 < 3`, false; `1 != 1 == 0` is `(1 != 1) && (1 ==
0)`, false, where reading from the left gives true (T108). `<=>` and
`cmp` don't chain and don't compile in one.
(a) **Recommended: refuse two operators of one row with no brackets
between them**, as `SURFACE.md` already has it (Later). `1 < 2 == 1`
is fine, being two rows. Nothing is lost that brackets or `&&` don't
say.
(b) Chain as perl does. It is in the language of the day, `0 <= $i <
$n` reads well, and it costs the rule that the middle operand is
worked out once. A later step can take it without breaking a program
that (a) accepts.

**Q5. `not`, `and`, `or`, `xor`.** Two traps.
The first has one answer. These bind more loosely than `say` does:
`say 0 or 2;` is `(say 0) or 2`, prints `0`, and perl warns; `say
true and false;` prints `1` and perl says nothing at all (T106). So
**a word operator after `say`'s argument is refused**, and inside
brackets, `say(0 or 2)`, it is the argument's. `... or die` comes
with `die` (step 15).
The second is a choice. `not 0 || 1` is `not (0 || 1)`, false. But
`not(0) || 1`, and `not (0) || 1`, are `(not 0) || 1`, which is 1: a
bracket after `not` is all it takes, as after `length` (T107).
(a) **Recommended: refuse an operator that binds tighter than `not`
after `not (...)`.** `not ($a == $b)` is fine; `not ($a) || $b` is
refused, with a message that says which brackets to add. It is T25's
rule for `say (...)`, for the same reason: the two readings differ in
silence.
(b) As perl, which is also what D41 does for `length ("ab") . "c"`.
Consistent, and a known trap kept.

#### The build, once the questions are answered

- **`t/models/bool.py` first, red before any code.** The comparisons
  over the Ints, Nums and strings at the edges of D35 and D40 (it
  imports `str.py` and `num.py`); truth of every kind of value; what
  each operator gives, operand or boolean; a boolean wherever a
  number or a string is wanted; and a fault test for each fault at
  its edge, an undef in each place that wants a value.
- **An adversarial review of this proposal**, started with it: the
  definition against perl, and the claim that no comparison turns on
  a past the rule doesn't fault.
- **By hand, with perl's answers**: precedence and grouping, each
  line chosen so that two readings print differently; what each
  operator leaves unevaluated, by a fault that doesn't happen;
  spellings (`1<2`, `"a"lt"b"`, `1?2:3`); each refusal.
- **Lexer**: `true`, `false` and `undef` end a value, so an operator
  comes next; the word operators after a value. **Parser**: the
  rows, `? :`, the rule for one row; what may follow `undef`. **The
  checker**: T101's list context goes down through the right of `||`,
  `&&`, `//`, `or`, `and` and both branches of `? :` (T104).
  **Generated C**: the first branches. An operand that may not be
  worked out is a block of its own, entered or not: `if` and a
  temporary, no `goto`. **Runtime**: two tags, undef and boolean;
  `rt_truth`; the comparisons; every operator's fault for an undef.
- Leave out: variables, so `defined $x` and `$x // 1` wait for step
  5; `if` and the other statements (5, 6); `^^`; chains unless Q4 is
  (b).

### 5. Lexical scalars, assignment, blocks, `if` (done)

Referee: perl. Size: large.

**Built 2026-11-25**, by Fable 5.2 (the size the line asks for), as
agreed below, and with these differences and findings:

- **The model was written first, and was red before there was any
  code** (`t/models/var.py`, commit 529a134). It is the first model
  of statements: a program is a list of them run against scopes of
  places, and an expression gives a place or a value, so that a late
  read is the model's own and not the compiler's. It writes 500 to
  504, about 5,000 lines on which perl 5.42 agrees with it (every
  `++` and `--` over D52's table, fresh and after the variable has
  been used each way; every assigning operator over step 3's and 4's
  values; each shape of late read; scopes; `if` chains with each arm
  taken and not), and 29 programs that fault once each, 520 to 546
  and 550, 551.
- **Holding the model to perl found two things before the compiler
  existed.** A row of dots is one operation to perl, which reads
  every piece of it late: `$x . "a" . ($x = 5)` is `5a5` (T117). And
  an empty bare block is an anonymous hash (T116). The second is
  refused. The first is **D57**: a concatenation in
  which a later piece changes a variable an earlier piece reads is
  refused. It was not in what Stevan agreed, and he took it when he
  saw it, the same day. T110's row had `$x . ""` down as a value,
  which it isn't beside another dot.
- **The compiler went green on the model's 32 tests the first time
  it ran**, which is what a model written first is for; what was
  wrong was found by asking perl about what the model doesn't write.
  `if (!($x = 5))`, `if (not $x = 5)` and `if (+($x = 5))` warn in
  perl and were accepted: D53's rule now goes through `!`, `not` and
  a unary plus (T112's row said perl was quiet under `!`; it is, in
  `say(!($x = 5))`, and not in a condition). `$x = undef if $y;` was
  refused and is plain perl. A fault in the test of a modifier that
  spans lines named the line of the `if`, where perl names the line
  the statement starts on (T118). After `$x++` the lexer expected a
  value, so `$x++ or ...` and `$x++ x 3` didn't parse.
- **A statement is one assignment**: `$x = 1 and $y = 2;` is refused
  (D56 says what a statement is; perl also warns of this one, `Found
  = in conditional`).
- **A new pass**, `resolver.ts`, as D29 drew it: each variable to its
  `my`, by number, before any C is made. It runs before the checker.
- **The generated C**: a variable is a C local in the C block of its
  scope, never copied into a temporary, so it is read when the
  runtime call that uses it is made (D14). Where an operator gives
  one of two operands (`||`, `? :`) the C keeps a pointer to it, and
  a statement's temporaries are all declared at its top so that a
  pointer set in a branch is good after it.
- **The runtime and the code generator were broken 74 ways on
  purpose** (`briefs/step5-mutations.py`: 37 in `rt.c`, 37 in the
  compiler, the second kind new with this step). 71 were caught the
  first time. One was a hole: a string that is exactly 2^53, stepped
  back under it, had no test at its edge (550 and 551 now). One was
  a check that could never matter, and is gone from the runtime
  (every double of 2^53 and up is whole). And one no program of this
  step can see: a `my` that isn't made undef again when its block is
  entered a second time. **Step 6 must test that**, with its first
  loop.
- 560 to 565 are by hand with perl's answers (how `++`, `--` and
  assignment group; the shapes after `say $x` that are not a file
  handle; scopes; `if`; the assigning operators; the concatenations
  D57 lets through); 547 to 549 are faults whose line is the point;
  570 to 613 are the 44 refusals, each with what perl does in its
  comment, run to write it.
- **The adversarial review** (`briefs/step5-review/`) ran beside the
  build and then on the compiler: 698,000 programs against a model
  of its own before there was a compiler, 57,000 through the
  compiler afterwards, and texts cut into tokens and joined again
  with blanks and comments at random. It found the three things the
  build had found (D57, the empty block, `!` over a tested `=`), on
  its own, and **seven kinds of program the compiler took that it
  should not have** (T125 to T130, and more of T112):
  - **One printed what perl doesn't.** `$t .= ($u = $x . $z);` never
    assigns `$u` in perl 5.42 or 5.38: a fault in perl's own joining
    of dots (T129). Refused, under D57.
  - **`++` and `--` on a float of 2^53 or more** faulted only when
    one more was the same float, and perl warns by where the float
    is: 2^53 + 2 and one more is a tie that rounds away (T130). The
    builder's evidence script had no such value; it has them now,
    went red, and the rule in it, the model and the runtime is
    perl's own line. Tests 523 and 552 to 554, each edge broken on
    purpose and caught.
  - **Five where perl warns or doesn't compile**: a tested `=` whose
    right side perl folds to a constant, `$x = 0 && $y`; a variable
    taken for a file handle after `substr(` and `index(` (T125); a
    name of more than 251 characters (T126); `$x =- $y` (T127); and
    `say ("a")` with its `if` on the next line (T128).
  All seven are refused or faulted now, tests 566 and 614 to 624.
- **The claim stood**: that a variable's past shows nowhere the
  language doesn't fault. 10,000 pairs of programs, one with reads
  put in that give its variables a past: perl's two outputs parted
  in 325, and in every one the model had faulted by then. 223,000
  single programs of pasts broke nothing but T130. That is the
  second such claim of five to stand, and the first with variables.
- **The compiler and the reviewer's model never disagreed**: wherever
  the compiler printed, the model printed the same. Of 57,000
  programs the compiler agreed with perl on 32,060, faulted on
  3,886, refused 5,810, and was wrong on 145, all of the seven
  kinds; 15,099 that the model faults on were sampled, not run.
- **Not checked by the review**: characters past ASCII; programs of
  more than about forty statements; the line a fault names; clang.
  The builder's tests cover the third (547 to 549) and the fourth.

**Proposed 2026-11-25, and agreed the same day: Stevan took the
recommendation on each question below, which are now D52 (Q1), D53
(Q2), D54 (Q3), D55 (Q4) and D56 (Q5, what had nothing to choose).**
The text is kept as it was proposed. Everything here about perl was run under
5.42.0: [`briefs/step5-increments.py`](briefs/step5-increments.py)
(`++`, `--` and the assigning operators under every past of the
variable) and `briefs/claims.py`. Traps: T1, T26, T30, T43, T44, T58,
T93, and T110 to T114, found writing this.

#### The picture

Until now a program was a list of things to print, each worked out
from literals. This step gives it **places to keep a value**, and
**statements that choose**.

```
 my $x = 5;              a place, in the block it is declared in
 $x = $x + 1;  $x += 1;  $x++;      putting a value in a place
 { ... }                 a block: a scope for the places declared in it
 if (...) { ... } elsif (...) { ... } else { ... }
 say $x if $x > 3;       one statement, on a condition
```

Three things are new for the compiler, and they are the step.

**A resolver.** Every `$x` is tied to its `my` before any code is
made: use before `my`, a second `my` in one scope, and `my $x = $x`
with no outer `$x` are refused, as perl refuses or warns of each.

**A value now has a past, in perl.** Every rule of steps 2 to 4 was
written so that a value needs none: it faults where perl's answer
turns on what a value was used as before. With no variables that was
a promise about the future; from here a program can use `$x` as a
float on one line and as an integer on the next. Those rules were
each tested that way (their evidence scripts are programs with
variables), so nothing changes, but this is the step where they are
load-bearing, and the review is asked to break them again. What this
step adds to the question is `++` and `--`, which change a variable
where it stands by routes of their own (Q1).

**An operand that is a variable is read when its operator runs** (D14,
decided). `my $x = 3; say $x + ($x = 5);` prints 10. The generated C
already has the shape for it: a variable is a C local and is never
copied into a temporary. What is new is how far "is a variable"
reaches (Q5).

#### The language at step 5

- **`my $x;`** and **`my $x = EXPR;`**: one variable, undef until it
  is given a value, visible from the next statement to the end of its
  block. A name is a letter or `_`, then letters, digits and `_` (Q4).
- **`$x = EXPR`**, and **`+= -= *= /= %= **= .= x= ||= &&= //=`**:
  `$x OP= E` is `$x = $x OP E` (held to perl on 7,524 operations
  under every past), with `||=`, `&&=` and `//=` working `E` out only
  if it is wanted.
- **`++$x`, `$x++`, `--$x`, `$x--`** (Q1).
- **Blocks** `{ ... }`; **`if`**, **`elsif`**, **`else`**,
  **`unless`** (Q3); **`STATEMENT if COND;`** and **`unless`**.
- A statement is `say`, `print`, a `my`, an assignment, a `++` or
  `--`, a block, or an `if`. An expression that only has a value,
  `$x + 1;`, is refused: perl warns that it is useless.

Left for later, and refused: `my ($a, $b)` and every list (9);
`our`, `local`, `state`; loops (6); `do BLOCK`; a `my` in the right
operand of `&&`, `||`, `//` or a branch of `? :`, or under a
modifier (D21, T30); the special variables.

#### The questions

**Q1. `++` and `--`.** perl has five routes through each, by what
the variable holds and what it has been used as. The rule, held to
perl on 456 cases under seven pasts each:

| The variable holds | `++` | `--` |
|---|---|---|
| undef | 1 (and `$x++` is worth 0) | -1 (and `$x--` is worth undef: T43) |
| true, false | the Int one more | the Int one less |
| an Int | the Int one more, or `integer overflow` | one less, or `integer overflow` |
| a Num | what `$x + 1` is (D35): the Int if the Num is whole and below 2^53, otherwise the Num | the Num one less, always; a fault if the Num is whole and the answer reaches 2^53 in size (T93) |
| a Num so large that the step is lost (`1e16`) | a fault: perl warns | a fault: perl warns |
| a string that is a number | the Num one more or less, whatever kind of number it is; a fault if it is whole and reaches 2^53, and for `++` if it is digits that begin with a zero | |
| any other string | a fault (T44) | a fault |

Three rows need a word. **`--` on a Num is not `$x - 1`**: perl
subtracts as a float unless the Num has been used as an integer, so
the answer is a Num where `$x - 1` is an Int, and at 2^53 the two
part. **A string stepped is a Num**, because perl steps a fresh
string of digits as text (`"12"` becomes the string `"13"`, `"009"`
becomes `"010"`) and one that has been used as a number as an
integer, 10. The Num prints as both do, and faults where they
differ. (My first run of the evidence missed the `"009"` case: it
compared the numbers and not what printed. It compares both now.)
**perl's string increment** (`"aa"` to `"ab"`, `"Az"` to `"Ba"`,
`"zz"` to `"aaa"`) is cut, as `SURFACE.md` has had it, and so is the
silent -1 that `--` makes of `"ab"`.
(a) **Recommended: the table.**
(b) `++` and `--` on an Int, a Num or an undef only, and a fault on a
string or a boolean. Two rows fewer, and `"12"` stops being a number
in this one place.

**Q2. An assignment as a condition.** `if ($x = 5)` is nearly always
a slip for `==`, and perl warns `Found = in conditional` when the
right side is a constant, after it has folded what it can: `if ($x =
2 + 3)`, `($x = 6) && ...`, `if (my $y = 6)`, `if (1 && ($x = 6))`.
It says nothing of `if ($x = $y)` or `if ($x += 1)` (T112).
(a) **Recommended: refuse a `=` whose right side has no variable in
it, wherever its value is tested for truth** (an `if` or `unless`, a
modifier, the test of `? :`, the left of `&&`, `||`, `//`, `and`,
`or`, and what those pass a test down to). That is every case perl
warns of and a few it doesn't, with no constant folder; and `if ((my
$n = next_one()) > 0)` and, later, `if (my $m = f())` stay.
(b) Refuse every `=` as a condition. Simpler to say, and the idiom
`if (my $m = f())` is lost for good.

**Q3. `unless` with `else`.** perl allows `unless (...) { } else { }`
and `unless (...) { } elsif (...) { }`.
(a) **Recommended: `unless` alone, and as a modifier.** With an
`else` it is an `if` written backwards, and most style guides say
so.
(b) As perl.

**Q4. Names.** `SURFACE.md` has "an identifier past ASCII, with `use
utf8`" as In at this step. perl's rule for which characters make a
name is Unicode's, with its own exceptions.
(a) **Recommended: names are ASCII for now** (Later, not Cut). A
character past ASCII stays refused outside strings and comments.
(b) Unicode names now, as perl has them, which is a table and its
edges.
With either, **`$a` and `$b` are refused as names**: perl allows `my
$a`, and then `sort { $a <=> $b }` in the same scope is broken. Say
if you would rather meet that at step 10.

**Q5. Nothing to choose, but worth your eye.**
- **How far "the variable itself" reaches** (T110). `$x`, `($x)`,
  `+$x`, `$x = E`, `$x += E`, `++$x`, and whichever operand `||`,
  `&&`, `//` and `? :` give, are the variable, read late: `($x || 0)
  + ($x = 5)` is 10. `$x++`, `-$x`, `$x . ""` are values: 8, 2. The
  language agrees, as D14 has it; the generated C keeps a pointer
  where it used to keep a copy.
- **What an assignment may be assigned to**: a variable. perl takes
  `($x = 5) = 7`, `($x += 1) *= 3` and `(1 ? $x : $y) = 8`; D17
  already has values flowing and not places, and these are refused.
- **`say $x -1;` dies** (T26, T111): perl takes `$x` for a file
  handle when a variable comes first after `say` or `print` and what
  follows the blank after it could begin a value: `-1`, `+$y`, `.5`,
  `++`, `<name`. `say($x -1)` dies the same way. `say $x - 1;` and
  `say $x-1;` are fine. Refused, by perl's own list of what it looks
  for, read from its source.
- **Which statements are refused**: one that only has a value (perl
  warns); `my` under a modifier, `my $x = 10 if $c;`, which is
  silent and leaves the last call's value behind (T30).

#### The build, once the questions are answered

- **`t/models/var.py` first, red before any code** (step 4 didn't,
  and the plan said it should). The model has an environment, and
  writes programs of several statements: every `++` and `--` over
  the edges of Q1's table, before and after the variable is used
  each way; every assigning operator over step 3's and 4's values,
  an undef on the left included; late reads, each shape of T110;
  scopes and shadowing; each branch of an `if` chain taken and not.
  And a fault test for each fault at its edge.
- **An adversarial review of this proposal**, started with it: the
  definition against perl, and the claim that a variable's past
  shows nowhere the language doesn't fault, now that a program can
  give it one. The last three reviews each refuted a claim of that
  kind.
- **Lexer**: `$name`; `++` and `--`; the assigning operators; `{`
  `}`; perl's file-handle guess after `say` (T111). **Parser**:
  statements in blocks; `if` chains and modifiers; assignment, right
  to left; `my`. **Resolver** (new): scopes, each name to its
  declaration, the three refusals. **Checker**: Q2's rule; what a
  statement may be; D21's places for `my`. **Generated C**: a
  variable is a C local in a C block; a value that is one of two
  operands (`||`, `? :`) is a pointer to it; temporaries are declared
  at the top of their statement so that a pointer to one outlives
  the branch that set it. **Runtime**: `rt_inc`, `rt_dec`; the
  assigning operators are the operators.
- Leave out: everything listed above as later.

### 6. Loops (done)

Referee: perl. Size: medium.

**Built 2026-11-25**, by Fable 5.2 (a size above what the line asks
for), as agreed below, and with these differences and findings:

- **The model first, red before any code** (`t/models/loop.py`,
  commit 394c2ab), on step 5's: a `last` or a `next` is a Python
  exception that the loop it is for catches. It writes 700 to 703,
  about 3,900 lines on which perl 5.42 agrees with it (each kind of
  loop run no times, once and many; `last` and `next` from a loop in
  a loop, of each kind, to the inner or the outer, through an `if`,
  an `else`, a modifier and a labelled bare block; what is new each
  time round; and every operator of steps 1 to 5 run again and again
  in a loop with its operands' kinds changing each time), and 13
  programs that fault once each, 720 to 732.
- **The compiler went green on all 17 the first time it ran.** The
  runtime is untouched. The parser has the loops, a label, `last`
  and `next` as statements and the two modifiers; the resolver ties
  each `last` and `next` to its loop and makes the three refusals
  (none round it, no loop of that name, a bare block in the way:
  D59); the checker holds a loop's test to D53 and a `for`'s parts
  to D60. The C is `for (;;)` with the test inside it, the block in
  a C block of its own, and a `goto` for each `last` and `next`: the
  first jumps in the generated C, and the only kind.
- **Where the language faults perl may carry on, and then a loop
  never ends** (T131). The model's first fault test for an
  overflowing counter was `while ($i > 0) { $i++; ... }`: the
  language stops at the overflow, and perl goes on as an unsigned
  integer and then a float, for ever. Run against perl it wrote 19
  GB to disk in two minutes before it was stopped by hand, and took
  the machine's memory with it. So: a fault test's loop is counted by
  something the fault doesn't touch; and **the harness no longer
  trusts that**. `t/run.sh` stops a test that prints past 8 MB, and
  `t/checks.py` stops perl at 16 MB, each by the system's own limit
  on a file's size; `t/harness/run.test.ts` and
  `t/checks/same-prints-for-ever.pl` make both bite, with the
  watchdog on time that was there already.
- **A fault's line** is the line perl warns or dies at in 9 of the
  model's 13 fault tests. Two differ, a `while`'s and an `until`'s
  test after the first time round, where perl names the last
  statement the block ran (T124, D62) and the language names the
  loop; and at the two overflows perl says nothing.
- **`$done and last;` has a message of its own**, since it is the
  commonest thing D62 cuts: `last is a statement, not a value: write
  'last if ...;'`.
- **The compiler was broken 49 ways on purpose**
  (`briefs/step6-mutations.py`, which compiles and runs the refused
  tests too, a resolver and a checker being half refusals; each run
  has ten seconds and a limit on what it may print, since a broken
  loop may never end). 46 were caught the first time. The three that
  weren't were holes in the tests, each closed: a fault under a
  `while` modifier whose statement begins on an earlier line (743),
  D53 in a `for`'s test (790), and a `my` in a modifier's test (791).
  Step 5's unseen breakage, a `my` not made undef again each time
  round, is caught now, by 702 and 730.
- 740 to 742 are by hand with perl's answers (how loops are written;
  which variable a name means in and round one; a dozen small
  programs, FizzBuzz to Newton's square root, which the language can
  now say); 743 is a fault whose line is the point; 750 to 791 are
  the 42 refusals, each with what perl does in its comment, run to
  write it.
- **No adversarial review**, as the proposal said: the step is
  medium, and adds no value and no arithmetic. What stands in for one
  is the model's fourth test, the operators run again in a loop:
  nothing turned on an operation having run before.

**Proposed 2026-11-25, and agreed the same day: Stevan took the
recommendation on each question below, which are now D58 (Q1), D59
(Q2), D60 (Q3), D61 (Q4) and D62 (Q5, what had nothing to choose).**
The text is kept as it was proposed. Everything here about perl was run under
5.42.0 and is in `briefs/claims.py` (31 rows, `T32-next` to
`PLAN6-cut`). Traps: T32, T64, and T119 to T124, found writing this.
The outline this replaces said: `while`, `until`, their postfix
forms, the C-style `for`, `last` and `next`, labels; a bare block as
a loop that runs once (T32); the comma in a C-style `for`'s slots
only; `do BLOCK while` if wanted (T64).

#### The picture

Step 5 gave a program places and choices. This step lets it **go
round**.

```
 while (TEST) { ... }        test, block, test, block, ... until the test fails
 until (TEST) { ... }        the same, until the test holds
 for (FIRST; TEST; EACH) { ... }
                             FIRST once; then test, block, EACH, test, block, EACH, ...
 $i++ while $i < 10;         one statement, round and round: test first
 last;   next;               out of the loop; on to its next time round
 OUTER: while (...) { while (...) { next OUTER; } }
```

A loop is three places a program can be sent to, and that is all the
compiler adds:

```
           +--> TEST --false--------------------------+
           |      | true                              |
           |    BLOCK  ... next; --+   ... last; -----+
           |      |                |                  |
           |      v                v                  v
           +--- EACH <-------------+               after the loop
```

`next` goes to EACH (which is nothing in a `while`), `last` goes to
after the loop, and the end of the block goes to EACH too. A label
says which loop's two places are meant. **The runtime gains
nothing**: every operation a loop runs is one steps 1 to 5 already
have.

Two things that were true by construction until now have to be made
true:

**A variable declared in a block is new each time round.** perl makes
a `my` in a loop's block, or in a `while`'s condition, undef again on
every pass (T119). In the generated C it is a local declared inside
the loop's C block with its undef, so it is; but step 5's mutation
run could not see a compiler that got it wrong, and this step's
tests must.

**The same operation now runs more than once.** A value has no past
here; in perl an *operation* has one too, a scratch value of its own
that it reuses each time it runs. Nothing known turns on it, and the
model will ask anyway: every edge table of steps 2 to 5 again,
inside a loop, with the kind of each operand changing from one time
round to the next.

#### The language at step 6

- **`while (TEST) { ... }`** and **`until (TEST) { ... }`**. The
  test is a test as an `if`'s is: D53 holds (`while ($x = 5)` is
  refused; perl warns of it in all four kinds of loop), and a `my`
  may stand in it, visible in the block, new each time round, gone
  after the loop.
- **`for (FIRST; TEST; EACH) { ... }`**: the C-style loop. Each part
  may be empty; no TEST is true, so `for (;;)` runs until a `last`.
  FIRST and EACH are what a statement may be: an assignment or a
  step, and in FIRST a `my`, which is one variable for the whole
  loop and gone after it (Q3 for the comma).
- **`STATEMENT while TEST;`** and **`STATEMENT until TEST;`**: the
  test comes first, so `say $i++ while $i < 3;` prints nothing when
  `$i` is 5. The statement is `say`, `print`, an assignment or a
  step, as under `if`, and one modifier to a statement.
- **`last;`** and **`next;`**, each with a label or without, and with
  an `if` or `unless` modifier: `last if $i > 5;`, `next OUTER
  unless $ok;`. In a C-style `for`, `next` runs EACH and then the
  test.
- **Labels** (Q4).

Left for later, and refused: `foreach` and `for` over a list, with a
variable or without (9, 10), and postfix `for` (10); `do BLOCK`, so
`do BLOCK while` (Q1); `redo`, `goto` and `continue` blocks (cut);
`last` and `next` anywhere but in a loop of their own, which until
subs (8) means anywhere outside one.

#### The questions

**Q1. `do { ... } while (TEST);`**, the loop that runs its block
before the first test (T64). It is not a loop to perl: it is `do
BLOCK`, an expression, with a `while` modifier that perl special-
cases to test afterwards. So `last` and `next` in its block don't
see it. They leave the loop *round* it, in silence, or with none
round it die as they run (`Can't "last" outside a loop block`).
(a) **Recommended: leave it out for now.** `do BLOCK` is its own
construct with a value and a context (D18), and belongs with whatever
step takes it. The loop is written `while (1) { ...; last unless
TEST; }` in the meantime.
(b) Take it at this step, as a loop form of its own, with `last` and
`next` refused inside its block unless they are in an inner loop.
More surface, for one trap fenced off.

**Q2. `last` and `next` in a bare block** (T32). To perl a bare
block is a loop that runs once. So `while (...) { { last; } say
"still here"; }` never leaves the `while`: the `last` leaves the
inner braces, and so does a `next`. `if` blocks are not loops, and
there `last` does what it looks like. This is the trap in the step,
and perl says nothing about it.
(a) As perl, which is the plan's reading and what T32's row says:
agree. It keeps the idiom of a block one can jump out of, `{ ...;
last if $done; ... }`.
(b) **Recommended: refuse a `last` or `next` with no label when the
nearest thing round it that perl counts as a loop is a bare block.**
The message says which braces it would leave, and to label the loop:
`W: while (...) { { last W; } }` is the `while` to perl as well. A
bare block is then a scope and nothing else, which is all step 5 made
it. This is T25's and T107's habit: where the reading a person takes
and perl's differ in silence, refuse. It reverses the plan's reading,
and since (a) accepts strictly more programs, it can be reversed
later without breaking one.

**Q3. The comma in a C-style `for`** (T122). `for (my $i = 0, my $j
= 9; $i < $j; $i++, $j--)` is the two-ended loop, and the only place
the outline lets a comma operator in.
(a) **Recommended: in FIRST and EACH only, joining what could each
be a statement**: assignments, steps, and in FIRST a `my`. Not in
the TEST, where perl tests the last part alone and warns that the
others are useless.
(b) No comma: one expression to a part. Simpler by a little; the
two-ended loop becomes a `while` with its steps in the block, where
a `next` then skips them.

**Q4. Labels** (T121). `OUTER: while (...) { ... next OUTER; ... }`.
perl takes a label on any statement, in any case, checks nothing as
it compiles, and looks the name up when the `last` runs: a wrong
name is a death in the middle of a run.
(a) **Recommended: labels now, cut down to what they are for.** A
label goes on a `while`, `until` or C-style `for`, one to a loop,
written in capitals, digits and `_`, hard against its colon. `last
NAME` and `next NAME` must name a loop that is round them, or the
program is refused as it compiles. Of two loops with one name the
inner is meant, as in perl. Not on a bare block (the surface cuts
that already), not on `if` or any other statement.
(b) No labels until something needs them. Then Q2's (b) has no way
to say "the outer loop" from inside a bare block, so (b) here goes
with (a) there.

**Q5. Nothing to choose, worth your eye.**
- **`last` and `next` are statements, not expressions** (T120). perl
  takes `$done and last;`, `$x ? last : next;`, `my $v = last;`,
  `last + 1;` (which dies looking for a loop called `1`) and `last
  $name;`. Here: `last;`, `last NAME;`, and each with an `if` or
  `unless` modifier, which says everything the first two do. It
  follows from D56, a statement being one thing; it is also the one
  item on this list that cuts an idiom people write (`... or next;`).
  `or die` comes with `die` (15), and that is the place to ask
  whether `or next` comes with it.
- **A `my` new each time round** (T119), as above: in a block, in a
  `while`'s or `until`'s test. In a C-style `for` a `my` is in FIRST
  only: perl takes one in the TEST or EACH too, and nobody means it.
  A `my` under a `while` or `until` modifier is refused, as under
  `if`.
- **`while ()` is refused** (T123): it is `while (1)` to perl, where
  `until ()` doesn't compile. `while (1)` or `for (;;)` says it.
- **The line a fault names** (T124): in a loop's test or its EACH,
  the line of the `while`, `until` or `for`; under a modifier, the
  line its statement starts on. perl agrees for `for` and for a
  modifier. For a `while`'s test it agrees the first time and after
  that names the line of whichever statement the block ran last,
  which is an accident of how it keeps its place and not something
  to copy. The tests check a fault's line by hand; perl's warning
  line was never part of what the oracle compares.
- **A program can run for ever now.** `t/run.sh` already stops a
  test after `TIMEOUT` seconds and fails it; this step makes that
  check fail on purpose, with a loop that never ends, before
  trusting it.
- **No collector until step 7**: a string made in a loop stays until
  the program ends. Nothing a program can see, short of running out
  of memory; the model keeps its loops short, and step 7 is next for
  this reason.

#### The build, once the questions are answered

- **`t/models/loop.py` first, red before any code**, on `var.py`:
  each kind of loop taken no times, once and many; `last` and `next`
  from each depth, through `if` blocks and (by Q2) bare blocks, with
  labels and without; `next` in a C-style `for` reaching EACH; a
  `my` in a block and in a test, read each time round before it is
  set; the edge tables of steps 2 to 5 inside a loop, the operands'
  kinds changing each time round. Fault tests: a fault the third
  time round, with what the first two printed before it; in a test
  the first time and a later time, in EACH, under a modifier, each
  for its line.
- **By hand, with perl's answers**: the shapes (`while` after `}`
  with no semicolon between, a label and its loop on two lines, an
  empty block, empty parts of a `for`); nested loops with one label
  twice; each refusal with what perl does in its comment.
- **Lexer**: nothing new but the words; the colon is there already.
  **Parser**: the three loops, a label before one, `last` and
  `next`, the parts of a `for` and their commas, the two new
  modifiers. **Resolver**: a loop's scopes (a `for`'s FIRST is round
  its TEST, EACH and block); each `last` and `next` to its loop, by
  label or nearest; the refusals for one with no loop, or a name
  that isn't round it, or (Q2) a bare block in the way. **Checker**:
  D53 in a loop's test; where a `my` may stand. **Generated C**:
  `for (;;)` with the test inside it; the block in a C block of its
  own, so its variables are made again each time round; `last` and
  `next` as `goto` to a label after the loop or at the end of its
  block, since C's own `break` and `continue` reach only the nearest
  loop. D31's "no `goto`" was for an operand that may not be worked
  out; this is the first jump, and the only kind. **Runtime**:
  nothing.
- **Break it on purpose**: step 5's unseen mutation first (a `my`
  not made undef again), then each jump sent to the wrong place,
  each test turned round, EACH skipped by `next`.
- **Review**: the rule asks for an adversarial review of a *large*
  step's proposal, and this one is medium, with no new values and no
  new arithmetic. None is planned. The step 5 review came in after
  this was written, and touches it in two places: T128's rule (a
  modifier after `say (...)` is on the bracket's line) goes for
  `while` and `until` as it does for `if`, and D53's constant is
  what perl folds to one, in a loop's test as anywhere.
- Leave out: everything listed above as later.

### 7. The collector (done)

Referee: none; the knobs are the test. Size: large.

**Built 2026-11-25**, by Fable 5.2 (the size the line asks for), as
agreed below, and with these differences and findings:

- **The cap first, then tests that were red, then the collector.**
  The knobs and the cap went in alone (a count and a fault). 800 to
  805 each make a gigabyte of strings under a cap of 16 MB, one for
  each way garbage is made, and with nothing freed each ended in
  `out of memory`; 806 and 807 are the cap's own faults. The
  collector turned them green, and changed no byte of what the 462
  tests before them print.
- **What was built is what D66 says**: every variable and temporary
  is a slot of its function's frame (`f[3]`, where `v3_x` and `t2`
  were C locals), a variable's slot its depth among those in scope;
  the mark walks every slot of every frame and the sweep frees what
  it didn't reach; a number as a string is on the C stack, so each of
  the five functions that allocate does so once, last; a string read
  after it was collected is `internal:`, checked in each of the five
  places a string's bytes are read and again after the allocation in
  the four functions that read an operand after allocating.
- **Measured.** A loop that makes a gigabyte of strings a kilobyte at
  a time peaks at 13 MB and takes 2.4 seconds, with the knobs off or
  with a collection at every allocation. The whole golden suite takes
  86 seconds under stress 1 with poison and 83 with the knobs off: so
  D64's default costs four in a hundred, today. It will cost more
  from step 9, as the review said.
- **The runtime's own tests in C** (`runtime/tests/collect.c`, 12 of
  the unit tests): what a slot keeps and what is freed, every frame,
  a frame that opens empty and one left open, each knob and what a
  bad value does, the policy with no knob, and a dead string read
  each way. Every count in them was worked out by hand before the
  program was run, and each was right: 100 collections in 100,000
  kilobyte strings, and 701 strings on the heap at the end.
- **The collector and the code generator were broken 47 ways on
  purpose** (`briefs/step7-mutations.py`; a broken runtime is linked
  with each test's C as first compiled, a broken compiler compiles
  each again; the runtime's own tests run against each copy). 45
  were caught the first time. The two that weren't were tests that
  did not test what they were written for: the test of a frame
  opening empty filled its slots with a pattern the collector skips,
  and 810's string was not in the frame's last slot. Both put right,
  and the last slot is now seen by a golden test as well as by C.
- **One expected output of mine was wrong**, worked out by hand and
  corrected by hand: 807's loop makes two kilobyte strings each time
  round, not one, so its cap is reached at about 950 and not 1,900.
- **`make sanitize` runs the suite twice** now: with poison on, as
  every test runs, where the runtime itself sees a dead string; and
  with it off, where the memory is really freed and the sanitizer
  sees a use of it.
- **The knobs are said in one file**, `t/knobs.sh`, which `t/run.sh`
  sources and `t/checks.py` and the mutation scripts read, so a
  test's binary runs the same way wherever it is run.
- Left for their steps, as D66 lists: marking through a value that
  holds values, and a mark stack (9, 13); a variable that outlives
  its frame (14); unwinding at a caught `die` (15); a heap for each
  context (29). And from the review: step 8's limit on recursion
  must count a frame's bytes, not calls; step 9 must say that a stale
  slot can hold a whole array.

**Proposed 2026-11-25, amended the same day by its adversarial
review, which could not break its rule and corrected a good deal
round it ("What the review found", below; the text here is as
amended), and agreed: Stevan took the recommendation on each
question, which are now D63 (Q1), D64 (Q2), D65 (Q3) and D66 (Q4,
what had nothing to choose).** D26 is decided and is not reopened here: a
precise, non-moving mark and sweep, its roots on a shadow stack the
generated C maintains, with a stress interval, poison and a heap cap
from the start; no reference counts, so no `DESTROY` and no `weaken`.
This is how. The outline it replaces said: every earlier golden test
under stress 1; a loop that allocates a gigabyte of strings under a
16 MB cap; `make sanitize`; before arrays, so that every container
after is written with roots from its first line.

#### The picture

**This step changes nothing a program can print.** It is the first
step with no language in it and no perl to say what is right. What
changes is that a program which makes a gigabyte of strings, a
kilobyte at a time, runs in a few megabytes and not in a gigabyte.

Today every string a program makes goes on one list and stays there
until the program ends. After this step the runtime can tell which
strings the program can still reach, and frees the rest:

```
   the generated C                          the heap
  +------------------------------+
  | frame of curly_main          |         +-----------+
  |  slot 0   $total   Int 15    |    +--> | "abcabc"  |  reached: kept
  |  slot 1   $name    Str  -----+----+    +-----------+
  |  slot 2   $line    Str  -----+----+    +-----------+
  |  slot 3   t1       Str  -----+--+ +--> | "x: 15"   |  reached: kept
  |  slot 4   t2       undef     |  |      +-----------+
  +------------------------------+  |      +-----------+
     every variable and every       +----> | "x: "     |  reached: kept
     temporary of the function             +-----------+
     is a slot the collector               +-----------+
     can see                               | "old"     |  no slot points here: freed
                                           +-----------+
  constants ("abc" in the source) are not on the heap, and are never looked at
```

A collection is two walks. **Mark**: every slot of every frame; a
slot that holds a heap string marks it. **Sweep**: every string on
the heap's list; one that wasn't marked is freed. Strings hold no
other values, so marking goes no deeper yet; arrays, hashes and
closures will each add how to find what they hold, and that is why
this comes before them.

The whole of the step is one rule and the three places it has to be
made true:

> **A value the program can still use is in a slot, at every moment
> a collection can happen.** A collection can happen only inside an
> allocation.

1. **The generated C.** A variable and a temporary are C locals
   today, which the collector can't see. They become slots of one
   array per function, linked from the context. D31's shape already
   has every result stored before the next operation begins, so the
   change is where a value lives, not what the code does.
2. **Inside the runtime.** `"n = " . $n` allocates twice today: a
   string for the number, and then the answer. The first is held only
   in a C local of the runtime when the second is allocated, and a
   collection there would free it. The cure is to stop allocating for
   a conversion: a number as a string is at most 22 bytes, and can
   sit on the C stack for as long as the operation runs (a *scratch*
   string: neither on the heap nor a constant, flagged as neither,
   and never the value a function returns). Then **every runtime
   function allocates at most once, and it is the last thing it does,
   or it holds what it has made in a frame of its own**. Today all
   five that allocate are of the first kind; the second is for steps
   9 and 10 (`split`, `sort` with a block, building a list), so the
   frame is something runtime C can open too, from the start.
3. **Between the two.** A fresh string is in a C return value for
   the instant between `rt_concat` returning and the assignment to
   its slot. No allocation can fall in that instant, because the
   generated C never passes one call's result straight to another
   (D31).

Nothing proves the rule but the knobs, which is why D26 has them:

- **Stress**: a collection at every allocation (or every nth). A
  root that is missed is then missed the first time it could matter,
  not on the day the heap happens to fill at the wrong line.
- **Poison**: a freed string is overwritten and marked dead, and
  under the knob its memory is never handed out again. Anything that
  still points at it and reads it stops with `internal: a string was
  used after it was collected`, where a plain `free` would let it
  read whatever was put there next. Two things make that true, and
  the review found both missing: the runtime reads a string's bytes
  in three places today, not one, so they go through one accessor
  that checks; and an operation that allocates and *then* reads its
  operands checks them again after the allocation, since under
  stress that allocation is the collection that killed them.
- **A heap cap**: a program that would hold more than the cap after
  a collection faults with `out of memory`. What is held counts the
  poisoned dead too, or a runaway loop under poison never reaches
  it. A loop that makes a
  gigabyte of garbage under a 16 MB cap passes only if the garbage
  is really freed, so this is the one way a golden test can see the
  collector work.

#### What changes

- **`rt.h`**: a frame (`{ previous frame, how many slots, the slots
  }`) and the context's list of them; a heap string gains a header
  (the next string, its size, a mark), and a constant's `rt_str` a
  flag that says it is one; the context gains the heap's list, its
  counters and the three knobs. D28 holds: none of it is global.
- **Generated C**: each function opens a frame for all its variables
  and the most temporaries any one statement needs, zeroed (a zero
  tag is no value, and is skipped), and closes it on the way out.
  `v3_x` and `t2` become `f[3]` and `f[9]`. A variable's slot is its
  depth among the variables in scope, so a block's slots are used
  again by the next block.
- **Runtime**: `str_new` is where a collection may start, before it
  allocates; conversions go to the C stack; the mark and the sweep,
  about a hundred lines; the knobs read from the environment once,
  as the program starts.
- **Every operator still checks its operands' tags**, and the one
  place a value becomes a string to read checks that it wasn't
  collected.

#### The questions

**Q1. How the knobs are set.** They have to reach a compiled program
somehow, and "you are about to add an environment variable" is a
point the process says to stop at.
(a) **Recommended: three environment variables that every compiled
program reads as it starts**: `CURLY_GC_STRESS=N` (a collection at
every Nth allocation; unset, the ordinary policy), `CURLY_GC_POISON=1`
and `CURLY_HEAP_CAP=BYTES`. The binary that is tested is the binary
that ships, and one build can be run every way. The cost is that
they are part of what a program is: anyone can slow a program with
the first, and stop it with the third, from outside. None changes
what a program prints short of `out of memory`.
(b) Flags to `curlyc`, baked into the binary. The suite compiles
every test again for each setting, and what is tested is a different
binary from what ships.
(c) A test build of the runtime only (`-DRT_KNOBS`). The same, and
the shipped runtime's collector is then code no test has run.

**Q2. `make test` under stress.** A golden test finds a missed root
only if a collection falls between the allocation and the use, and
under the ordinary policy a small test never collects at all.
(a) **Recommended: `t/run.sh` sets stress 1 and poison for every
golden test**, as the place where what every test assumes of the
runtime is set; a test that is about the cap or the ordinary policy
says so in its `# env:` header. One run, the strongest one. The cost
is time, and the review measured it on a prototype: nothing yet
(every test in under a second, collecting always or never; the
largest frame is 30 slots). It will cost from step 9, when a
collection walks every live value. A test that is too slow then
raises its own interval in its `# env:` header; the default stays
1, because coverage falls fast with the interval (with every root
missed, intervals 1, 2, 3 and 10 turn 78, 64, 52 and 31 tests red).
(b) `make test` plain, and `make stress` beside `make sanitize` as
something to run before calling a runtime change done. Faster, and
it will be skipped.

**Q3. A cap by default.** With no cap a program takes memory until
the machine says no, which on a shared machine is everyone's
problem (step 6's runaway test took this one down, by disk).
(a) **Recommended: the language has no cap of its own, and
`t/run.sh` gives every test one** (256 MB, far above any test), so a
test that runs away faults with `out of memory` in a second and
takes nothing with it.
(b) A default cap in the runtime, say 1 GB, raised by the variable.
Safer for a stranger's first program, and one more way a correct
program stops.
(c) No cap anywhere unless a test asks.

**Q4. Nothing to choose, worth your eye.**
- **"Precise" is about what a slot holds, not about whether it will
  be used.** A variable keeps its last string alive until its slot
  is given something else or its function returns, and so does a
  temporary: after `$s = $x . $y;` the string is in `$s` and in the
  temporary it came through, and `$s = "";` frees nothing until a
  later statement uses that temporary. No analysis of what is still
  wanted. What is kept that nothing can reach is bounded by the
  slots of the frames that are open, times the largest value: small
  now, and from step 9 a stale slot can hold a whole array, which
  that step has to say.
- **The ordinary policy**, when no knob is set: a collection when
  the bytes allocated since the last one pass the larger of 1 MB and
  what was live after it, so the heap at most about doubles between
  collections. It is the policy every shipped program runs and the
  one the suite under stress never does, so it has a test of its own
  in C, with no knobs.
- **A number as a string no longer allocates**, anywhere: comparing,
  joining, measuring. It is the cure for (2) above and it also takes
  most of the garbage out of arithmetic-heavy string code.
- **`out of memory` is a fault like any other**, with the line of
  the statement, when `malloc` refuses or the cap is passed after a
  collection. perl's own death for lack of memory is outside what
  D12 promises (D46), so there is nothing to agree with.
- **The collector's failures are `internal:` errors**, not faults: a
  string used after it was collected is a bug in the compiler or the
  runtime, never in the program, and says so, with exit status 2 as
  the compiler's own internal errors have.
- **No finalisers**, as D26 says; nothing runs when a value dies.
- **What this leaves for later steps, by design**: marking through
  a value that holds values, and a mark stack so that a long list
  doesn't overflow C's (arrays, 9, and references, 13); a variable
  that outlives its frame (closures, 14); unwinding the frames when
  a `die` is caught (15); a heap for each context (29). Each has a
  place to go in this shape, and none is built now.
- **No model.** There is no second derivation of what a collector
  should free: any program must print the same whatever is freed or
  kept. The tests are the knobs over everything already tested, the
  cap tests, and the runtime's own tests in C.

#### The build, once the questions are answered

- **The cap first, and then tests that are red before the
  collector**: the cap is a count and a fault and needs no
  collector, and without it a gigabyte loop today just takes a
  gigabyte. Then the cap tests. Loops that make a gigabyte of
  strings in pieces, each under a 16 MB cap, one for each way
  garbage is made: a temporary in an expression, a variable given a
  new value, a `my` in a loop's block, a string grown and cut back
  (kept under half the cap: old and new both exist inside `.=`), a
  number joined to a string; and beside each, what must *not* be
  freed: a string held in an outer variable across a million
  collections, read at the end. They are `same` tests (perl runs
  them too), and with the cap and no collector each ends in `out of
  memory`. And one `fault` test that holds more than the cap live
  and must fault: without it nothing shows the cap is counted.
- **The runtime's own tests in C** (`runtime/tests/`): frames built
  by hand; make, drop, collect, count; a string in a slot survives,
  one in no slot doesn't, a constant and a scratch string are never
  touched; two frames, with a string only in the outer; a frame
  opened by the runtime itself; the ordinary policy with no knobs,
  100 MB of garbage and the counters; each knob, and what `0`, `-1`,
  `abc` and nothing do as its value. `rt_run` stops with `internal:`
  if a frame is still linked when the program's body returns.
- **Tests written for what the suite cannot see by luck**: the last
  temporary of the statement that has the most, and the deepest
  variable, each holding a made string read after two more
  allocations (no golden test today turns red when the last
  temporary slot is left out of the mark).
- **Every golden test of steps 0 to 6 under stress 1 with poison**,
  byte for byte what it prints today; under gcc, clang, and the
  sanitizers, whose own check for a use after a free needs the
  poison's quarantine off, so both ways.
- **Break it on purpose**, the collector: a slot left out of the
  mark, each kind (a variable, a temporary, the first slot, the
  last); a frame not linked, or not unlinked; only the newest frame
  marked; the sweep freeing what is marked; the marks not cleared; a
  constant treated as heap; a conversion allocating again; the cap
  not counted; the ordinary policy never collecting, or its
  threshold not growing. **And the code generator**, where most of
  the change is: a `my` that doesn't make its slot undef;
  temporaries that begin one slot early; a frame one slot short; a
  block's variable given a slot still in use. Each must turn a test
  red.
- **The knobs wherever a test's binary runs**, not only in
  `t/run.sh`: `t/checks.py` runs fault tests itself, and the
  mutation scripts run binaries. One place says what the knobs are.
- **An `internal:` error flushes what the program printed first**,
  and the quarantine is freed on every way out, or the sanitizers
  report a leak on each fault test.
- **An adversarial review of this proposal**, started with it, as
  the rule for a large step asks: a sequence of operations that
  frees a string still in use, or keeps garbage without bound, under
  this design.
- **Measure**: the suite's time plain and under stress, and the
  gigabyte loop's time and peak memory, into this section.
- Leave out: everything listed above as later; any change to what a
  program means.

#### What the review found

A reader with this proposal and the code, who also built the design
as a prototype (`briefs/step7-review/`: `proto.py` patches a copy of
the runtime to collect before every allocation and poison what is
unreached, and rewrites each test's generated C to frames by macros).
All 275 golden tests that compile print what they print today under
it.

- **The rule was not broken.** No program and no path through the
  runtime frees a string in use. Of 653,853 lines of generated C,
  every runtime call's result is the whole right side of an
  assignment to a temporary or a variable, every argument is a slot,
  a pointer to one, or a constant, and no temporary is live across a
  nested statement. With conversions on the C stack there are five
  allocation sites, each once and last.
- **Four things the proposal had wrong about today's code**, put
  right above: the number of allocations in its own example; the
  "one place" a string is read (three); "at once and every time"
  for poison (70 of the 78 tests that turn red with every root
  missed printed poisoned bytes and no `internal:` line, and one
  probe stayed green); and "today each ends in `out of memory`"
  (there is no cap today).
- **Poison with a cap that counts only the living never stops a
  runaway**: the suite's own default settings, as Q2 and Q3
  recommend them, together. The cap counts the dead.
- **Holes in the test plan**, ten, each taken above: the last slot;
  variables hidden by the stale temporary beside them; a cap that is
  never seen to trip; an ordinary policy nothing runs; one function
  and so one frame until step 8; mutations for the code generator;
  the knobs' own parsing; and the places a binary runs that are not
  `t/run.sh`.
- **For the later steps**: the second half of the rule for runtime
  functions (above); a per-test interval, not a global one; and step
  8's recursion limit must count a frame's bytes, not calls, since
  frames differ in size.
- **Not checked by it**: the cap and the ordinary policy (its
  prototype has neither); a chain of frames, frames on the C stack,
  or state in the context (its frame is one static array); clang and
  the sanitizers; a gigabyte loop.

### 8. Subs (done)

Referee: perl. Size: large.

**Built 2026-11-25**, by Fable 5.2 (the size the line asks for), as
agreed below and as D67 to D73 have it, and with these differences
and findings:

- **The model first, red before any code** (`t/models/sub.py`,
  commit 2545ef2), on step 6's: a call is a Python call with its
  context, a `return` an exception, an argument a place that is read
  when its parameter's turn comes. It writes 900 to 904, about 1,100
  lines on which perl 5.42 agrees with it (every form of parameter
  and default with each kind of value; what is read when; recursion,
  99 deep at the most; context; and the operators of steps 1 to 6 on
  values that came through a sub), and 21 programs that fault once
  each, 919 to 939. **perl agreed with the model on all five the
  first time they were compared**, once the model's own layout of a
  `return` was right; and every fault test's output is the start of
  perl's, with perl's line where perl has one.
- **The compiler went green on all 25 the first time it compiled
  them.** The parser has `sub`, a signature, `return`, a call and
  `no`; the resolver gives each sub a function of its own, ties each
  call to its sub, and gives the file's variables slots of their
  own; the checker has D69's walk and T143's refusals; the code
  generator writes a C function for each sub. The runtime gained
  the count of open frames, the stack check, and two faults that
  take a name: no operator.
- **D67 changed what was built**: there is no count for each sub,
  and nothing happens at 100 calls deep. `no warnings 'recursion';`
  is a pragma that does nothing here. 942 goes 3,000 deep with it.
- **The limit, measured where it is.** A call of the smallest
  recursive sub (`depth`, 6 slots) counts 1,120 bytes, so 3,743 of
  them may be open: 943 makes exactly that many and prints, 944
  makes one more and faults, at the line worked out by hand, under
  gcc, clang and the sanitizers. The runtime's own test
  (`runtime/tests/deep.c`) has the numbers with no compiler in the
  way: 4,096 frames of no slots, and not 4,097; and a program given
  a 4 MB stack stops before it starts.
- **By hand**: 940 to 942 with perl's answers (a dozen small
  programs, factorial to the Tower of Hanoi; how a sub and a call
  may be written; deep recursion); 943 to 946, the limit from both
  sides and two faults whose line is the point; 950 to 999, fifty
  refusals (and 947 and 948, from the mutation run), each with what perl does in its comment and its line,
  column and message worked out before the compiler was run. 33
  were right. Of the 17 that weren't, two were the builder's own
  miscounted columns; one was the lexer refusing `v65(` before the
  parser could, with a message of its own; **and 14 were one rule
  the builder had forgotten: every statement ends in a semicolon,
  the last in a block too (step 5, t/604), so `sub f() { return 1 }`
  is refused**, and so was every one-line sub in the proposal's own
  examples. The rule stands; it is worth Stevan's eye now that subs
  make it bite (below).
- **A test of the builder's that perl rejected**: 940's Collatz
  count of 27 is 112 calls deep, and perl warned, which the oracle
  check would not have. It counts from 7 now.
- **One refusal D69 makes that the proposal didn't spell out**:
  `$x .= set();`, where `set` can change `$x`. The left of `.=` is
  the first piece of a row (D57), so it is refused (988), though the
  generated C would have agreed with perl there.
- **A call may be a part of a `for`**, `for (init(); ...; step())`,
  where D60 had refused whatever only has a value: a call is
  something done. It is void there, as the review said (D7 of its
  findings).
- **A sub's name is refused where it is defined**, by the parser,
  so that `sub q(...)` is what the message is about and not the
  first `q(5)`. A word perl has no meaning for, at the head of a
  statement with no bracket after it, is now told that a call has
  brackets.
- **The runtime and each pass were broken 81 ways on purpose**
  (`briefs/step8-mutations.py`, which runs every test of step 8, the
  refused ones too). 77 were caught the first time. Three were
  holes in the tests, each closed: a last statement that is a call
  handing its context on (919), a default that is not checked (947),
  and a `$` alone outside a signature (948). The last can't be
  caught: a sub that ends in `say` being worth the Int 1 and not
  `true`, which nothing in the language can tell apart.
- **gcc, clang, and the sanitizers with poison on and off**: green.
- Left for their steps: lists in and out of a sub, and with them
  the end of D71's fault and T143's refusals (9, 10); `@rest` and
  `%opts` (10, 12); anonymous subs, closures, a sub in a block
  (14); a caught `die` unwinding frames, and a `return` on its own
  line with its value on the next, where perl names the value's
  line (15); a call that is not a C call (29, D68).

**For Stevan, from the build**: (1) D73, the review's ways out, and
D74, what the build settled, were defaults; he confirmed both. (2) The semicolon before a closing
brace. `sub double($x) { $x * 2 }` is how Perl is written, and it is
refused for want of a `;`. perl takes both. Letting the last
statement of a block go without one is a small change to the parser
and to what step 5 decided; it is not made here. **He asked for it
the same day, and it is D75**: 905 has every shape of it, 604, which
was the test of the refusal, is a `same` test now, and 906 is the
file's own last statement, which still ends in its semicolon.

**Proposed 2026-11-25, by Fable 5.2 (the size the line asks for),
and answered the same day: D67 (Q1: not the recommendation; nothing happens at 100 calls
deep, and `no warnings 'recursion';` is accepted to keep perl as
quiet, so there is no count for each sub to build), D68 (Q2: the recommendation as a default, on
his condition that it box nothing in, which the entry spells out),
D69 (Q3, as recommended), D70 (Q4: not the recommendation; a sub that
ends in `say` is worth `true`, as in perl), D71 (Q5, as recommended)
and D72 (what had nothing to choose). The text is kept as it was
proposed, and **its adversarial review found four ways to be WRONG:
"What the review found", at the end, and D73 for what was done about
each**.** Everything here about perl was run under 5.42.0
and is in `briefs/claims.py` (59 rows, `T1-args` to `T60-label`).
Traps: T1, T19, T28, T31, T55, T60, and T132 to T142, found writing
this. The outline this replaces said: named subs with signatures,
positional parameters and defaults; calls with brackets (D21), before
or after the definition; `return`; recursion; a wrong number of
arguments is a fault; a sub stands at the top of the file and may not
be named for anything perl knows; a sub that ends in a compound
statement has no value; signature placeholders and `//=` defaults;
and that the step decides how deep a program may recurse, how a test
that goes 100 deep is checked, and the hidden context flag.

#### The picture

Until now a program was one run of statements. This step lets it
**name a piece of itself and call it**, and a piece may call itself.

```
 the file                                 as it runs

 use v5.42;                               frames, the newest first
 my $total = 0;       file variables:
                      every sub after      +---------------------------+
 sub add($n) {        them may read        | fact(1)   $n = 1          |
     $total += $n;    and write them       +---------------------------+
     return $total;                        | fact(2)   $n = 2          |
 }                                         +---------------------------+
                                           | fact(3)   $n = 3          |
 sub fact($n) {       parameters:          +---------------------------+
     return 1 if $n < 2;   copies, new     | the file  $total  ...     |
     return $n * fact($n - 1);  at every   +---------------------------+
 }                    call
                                          a call opens a frame; every way
 say fact(3);                             out of the sub closes it
 add(5);
```

A sub is three things the compiler has not had before:

1. **A second function in the generated C.** Step 7 made every
   variable and temporary a slot of its function's frame, so that
   this would be a matter of opening one more: a call opens a frame,
   copies its arguments into the frame's first slots before anything
   can allocate, and closes it on every way out.
2. **A way out from the middle.** `return` leaves from inside any
   number of loops and blocks. It is one `goto` to the one place
   where the frame is closed, the third kind of jump the C has.
3. **Variables that are not the function's own.** A sub reads and
   writes the file's variables, which are slots of another frame.

And one thing perl has that the language has to choose about:
**a program can now run out of something other than memory.** perl
keeps its calls on the heap and has no limit; C has a stack, and it
ends (Q1, Q2).

#### The language at step 8

- **`sub NAME(PARAMETERS) { ... }`**, at the top level of the file,
  among the statements, before or after the calls of it. A signature
  is required, `()` for none. Not in a block, a loop or another sub
  (T31: perl ties a named sub to the first time round, and warns
  `will not stay shared` in a sub).
- **A parameter** is `$name` (required); `$name = EXPR`, `$name //=
  EXPR` or `$name ||= EXPR` (optional: the default is used when the
  argument is missing; with `//=`, also when it is undef; with `||=`,
  also when it is false); or a placeholder, `$`, `$=`, `$ = EXPR`,
  which takes an argument and names nothing. Required ones first
  (perl refuses otherwise). A default is worked out at each call that
  needs it, left to right, after the parameters before it are set, so
  it may read them: `sub f($x, $y = $x * 2)`. `@rest` and `%opts` are
  steps 10 and 12.
- **A parameter is a copy** (D17), and a variable like any other in
  the sub: it may be assigned.
- **The body** is the statements of steps 0 to 6, and `return`. Its
  `my` variables are new at every call. It may name the file's
  variables: those declared by a `my` at the top level, before the
  sub in the file. A `last` or `next` is tied to a loop of the same
  sub or refused (T60, already so).
- **`return;`** and **`return EXPR;`**, with an `if` or `unless`
  modifier or without. A statement, as `last` is (T139).
- **A sub's value**, when it ends without a `return`, is its last
  statement's, if that is an expression (D18): an assignment, a
  step, a call, a `my`, or **a value alone, `$x * 2`, which is now a
  statement in that one place** (perl warns `Useless use` of one
  anywhere else, and not there). A sub that ends in anything else
  has no value (D18, Q4).
- **A call** is `NAME(ARGUMENTS)`: the arguments are expressions
  with commas between, and one comma may follow the last. It is an
  expression, and it is a statement: `add(5);`, with any modifier.
- **Too few or too many arguments is a fault** (D13 has it so; perl
  dies), raised after every argument has been worked out, as perl
  does it, and naming the caller's line, as perl does.

**Context** (D18) starts here, though nothing list-shaped exists. A
call carries perl's three: *void* (`f();`), *scalar* (an operand,
the right of `=`, a test, a builtin's argument), and *list* (an
argument of `say`, `print` or another call). `return f();` and a
last statement `f()` pass on what their own sub was called with; so
do the arms of `? :` and the right side of `||`, `&&` and `//`. A sub
returns one value under all three, with two exceptions that the flag
is for: a sub with no value (Q4) faults unless it was called void,
and a sub that returns nothing (Q5).

#### What perl does that the obvious build gets wrong

Each is a row of `TRAPS.md`, with the program.

- **Arguments are read late too** (T1). `show($x, set())` hands
  `show` what `set` left in `$x`: perl passes the variable and
  copies it as the sub begins. So an argument that is a variable is
  read at the call, after the other arguments have run, which is
  D14's rule and its machinery. A sub's own value is a copy as it
  returns: `get() + step()` is 6 where `$total + step()` is 106.
- **A row of dots and a call** (T132, Q3). `$x . "-" . ch()` is
  `b-c` when `ch` sets `$x` to `b`: D57's trap, through a sub.
- **A sub that returns nothing is no argument at all** (T133, Q5).
  With `sub f() { return; }`, `g(f())` calls `g` with nothing, and
  `g`'s default is used.
- **A call before a variable's `my`** (T134). `bump(); my $x; say
  $x;` with `sub bump() { $x++ }` after it prints 1: at the top
  level a `my` doesn't empty a variable. The generated C sets a
  variable to undef at its `my` today.
- **`-e(2)` is a file test** (T135), not minus `e(2)`: undef, in
  silence, for 26 one-letter names; and `5-f(2)` doesn't compile.
- **How perl reads a call depends on whether it has seen the sub**
  (T136): `say f (1);` compiles after `sub f` and not before, and
  `v65()` is a version string before `sub v65` and a call after.
- **`f(1,,2)` is two arguments** (T137), in silence.
- **A default sees the file's variable of a later parameter's
  name** (T138): with `my $y = 10;`, `sub f($x = $y, $y = 2)` gives
  `10 2`.
- **`return` is an expression to perl** (T139): `my $x = return 5;`,
  `1 + return 2`, `$c and return "t";`, a default that returns.
- **What a sub is worth when it just ends** (T19, T140): its last
  `if`'s test, 1 after `say`, an empty string after a `while`.
- **Two parameters of one name, and a `my` of a parameter's name**
  (T141): perl warns as it compiles, and takes the second.
- **The warning at 100 is counted for each sub** (T142, Q1).

#### The questions

**Q1. Recursion, where perl warns.** perl warns `Deep recursion on
subroutine "main::d"` when one sub has 100 calls of itself open at
once, and carries on. It counts each sub by itself: two subs calling
each other warn at 199 deep, not 100. D15 makes perl's warnings
faults and left this one out for this step to settle. A `same` test
must leave perl's stderr empty (D10), so today no test may go that
deep.
(a) **Recommended: a fault at the 100th open call of one sub, unless
the program says `no warnings 'recursion';`**, which joins D16's
list: one line, with the other pragmas, before the first statement.
Under perl the line silences exactly this warning, so the file means
the same to both, the oracle check keeps its rule that stderr is
empty, and D15 has no exception. It is what Perl programmers who
recurse already write. The fault names the sub and the line to add.
The cost: one more pragma, a count for each sub, and a recursive
program over anything long carries the line. (perl decides by where
the *call* is written, so a pragma inside one block covers the calls
in that block only; a line at the top is the whole file and the only
place it is allowed.)
(b) No fault at 100, and the pragma is accepted only so that a test
can be silent under perl. Kinder, and it is D15's one exception made
permanent: a program perl warns about that runs here without a word.
(c) A fault at 100, always. No pragma, and no recursion over a list
of a hundred things.

**Q2. How deep, at the most.** The C stack ends, so there is a
number whatever Q1 says. Measured (`briefs/step8-stack.c`): a call
of a small sub takes 223 bytes of stack under gcc, 335 under clang,
and about 790 under the sanitizers; each slot of its frame is 16
more. On the 8 MB stack that Linux and macOS both give a program, a
four-slot sub reaches 37,000 calls deep under gcc, 25,000 under clang
and 10,500 under the sanitizers, and then the program dies of a
segmentation fault. The limit has to be the same number on every
build, or a test of it passes on one and not another.
(a) **Recommended: the open frames may hold 4 MB**, counted as 16
bytes a slot and 1 KB a call, which is more than any build measured
takes, so the count runs out while half of the real stack is left.
Past it: `fault: recursion too deep`, at the caller's line. That is
about 3,800 calls deep for a small sub and 2,500 for one with forty
slots. The runtime checks as it starts that the stack it was given
is 8 MB or more, and stops with a message if not, so that the fault
is never beaten to it by a crash. Twenty lines, and no new moving
part. It is far less than perl allows (a million deep took it 0.7
seconds), and it can be raised later without changing what any
program that ran means.
(b) The program's body runs on a stack the runtime makes, 256 MB,
with 64 MB counted: about 60,000 deep. It no longer matters what
stack the program was started with. It is a thread, or a hand-made
stack, on two systems and under the sanitizers; step 29 will want
stacks of its own and could bring this then.
(c) No limit, as perl: frames on the heap and no C recursion. The
generated C would no longer be D31's.

**Q3. D57, now that a call can change a variable.** `$x . "-" .
ch()` reads `$x` after `ch` has run (T132), and the straight-line C
would have joined `$x` and `-` before it. Only a file variable can
be changed by a call: parameters are copies.
(a) **Recommended: refuse a concatenation in which a later piece
calls a sub that can assign a variable an earlier piece reads**,
"can" worked out from the whole program: the sub's own assignments
and steps, and those of every sub it calls. It is D57's rule with
one more way to change a variable, and the same message: make the
change a statement of its own. A closed world (D20) makes it exact
today; step 14's code references will have to say "any sub" where
they can't tell.
(b) Refuse wherever an earlier piece reads a file variable that any
sub assigns and a later piece calls anything. No walk over the
calls; it refuses `$count . ": " . name($k)` in any program with a
sub that counts.
(c) Join a row as perl does. D57 turned this down.

**Q4. A sub that ends in `say` or `print`.** D18 has decided that a
sub ending in an `if`, a loop or a block has no value, and that
using it faults. `say` is left: perl's `say` returns 1, so `my $x =
f();` is 1 when `f` ends in one.
(a) **Recommended: no value, like the rest.** `say` and `print` are
statements here and have never had a value. A sub's value is then a
`return`'s, or a last statement that is an expression, and nothing
else: a `return` under a modifier (`return 1 if $c;` as the last
line gives perl's caller the test's value when `$c` is false), an
`if`, a loop, a block, `say`, `print` all fault if the value is
used, and none if the call was void.
(b) 1, as perl. Then `say` has a value in one place and is a
statement in every other.

**Q5. A sub that returns nothing, where perl wants a list.** `return;`
and a sub with an empty body give undef to a scalar call, in
silence, and that is agreed with. To a list they give no values: so
`g(f())` calls `g` with no arguments, and `say f();` prints an empty
line (T133). There are no lists until step 9.
(a) **Recommended: a fault**, `f returned nothing where a list is
wanted`, until step 10 brings list returns and can agree. It is a
fault where perl is silent, on D15's list of those, and a rare
program: one that passes on or prints the value of a sub that has
none.
(b) Agree now: an argument list whose length is known only as it
runs. That is step 10's work, done early for one case.

**Nothing to choose, worth your eye.**

- **A file variable keeps one slot for the whole run, and its `my`
  no longer makes it undef** (T134): every slot is undef as the
  program starts, and at the top level a `my` runs once. So perl's
  answer is agreed with and nothing is refused. A `my` in a block, a
  loop or a sub is undef at each entry, as now.
- **A sub's name** is ASCII, at most 251 characters, and not: any
  name in perl's own table (every keyword, function and quote
  operator, and the words `use v5.42` brings in: `true`, `trim`,
  `ceil`, `indexed` and the rest); `BEGIN`, `END`, `INIT`, `CHECK`,
  `UNITCHECK`, `AUTOLOAD`, `DESTROY`, `import`, `unimport`, which
  perl calls by itself; `v` and digits (T136). `briefs/step8-names.py`
  asked perl about 3,448 names, each defined and called eight ways,
  before and after the definition: for all but 59 the sub is simply
  called, and each of the 59 is one of those. `x` works in perl, and
  is refused with the rest of its table. Two subs of one name are
  refused (perl warns, and takes the second), and so is a call of a
  sub the program doesn't have (perl dies when it gets there).
- **A minus hard against a one-letter name is refused** (T135): `-
  e(2)` and `-(e(2))` are how to say it.
- **After `say` or `print`, a call's bracket touches its name**
  (T136). Elsewhere a blank or a new line may come between, as perl
  has it either way round.
- **`return` is a statement** (T139): not an operand, not after
  `and`, not in a default, not at the top level. `$c and return 1;`
  gets a message of its own, as `$done and last;` has. `return (5) +
  1;` is 6 in perl, where `say (5) + 1;` is not, so that is agreed
  with.
- **A parameter may not be `$a`, `$b` or `$_`** (D55, and perl
  refuses the last); nor a name used twice in a signature; nor may a
  `my` at the top of the body take a parameter's name (T141). A
  parameter may hide a file variable, in silence, as in perl; and a
  default is resolved before its own parameter exists (T138).
- **A fault's line** is still the statement's (D34), the sub's own
  statement while the sub runs and the caller's again once it
  returns: the generated C stores the line again after each call.
  perl agrees in the cases tried.
- **A value has no past, asked again.** An argument and a returned
  value are copies, as an assignment's is, so nothing new is
  expected; the model will put every edge table of steps 2 to 6
  through a sub, as an argument and as a return, and ask.
- **No model of the limit.** Q2's number is tested from both sides
  in a golden test, under all three builds: the deepest call that
  returns, and one more.

#### The build, once the questions are answered

- **The model first, red before any code** (`t/models/sub.py`, on
  step 6's): a call is a Python call with the flag as an argument,
  and `return` an exception. Its `same` tests: every form of
  parameter and default, with each kind of value; arguments and
  returns read late and copied (T1); recursion, two subs calling
  each other, a call before its definition; `return` out of loops in
  loops; the file's variables read and written from three calls
  deep; each context, passed on through `return f()`, `? :` and
  `||`; and every edge table of steps 2 to 6 through an argument and
  through a return. Its fault tests, each at its edge: one argument
  too few, one too many, with and without defaults; a sub with no
  value used, for each way of ending; whatever Q5 makes a fault; the
  99th call and the 100th (Q1); the deepest call and one more (Q2).
  **A fault test's recursion is bounded** (T131): under perl the
  program must end.
- **By hand, with perl's answers**: the small programs the language
  can now say (factorial, Fibonacci, Ackermann, greatest common
  divisor, a string reversed by recursion, Hanoi counted); and every
  refusal above as a test, with what perl does in its comment.
- **The compiler**: the parser has `sub`, a signature, `return`, a
  call; the resolver gives each sub its scope, ties each call to its
  sub and each `return` to its own, and finds the file variables a
  sub names; the checker has the refusals and Q3's walk; the code
  generator writes a C function for each sub, declared before any is
  defined. `names.ts` gains perl's table.
- **The runtime**: a frame knows its size in bytes and the context
  counts them (Q2); a count for each sub (Q1); the file's slots
  reached through the context (D28: nothing global). No new
  operator.
- **Every golden test under stress 1 with poison**, as D64 has it:
  an argument in flight is the new place a root could be missed.
- **Break it on purpose**: an argument copied after the default
  that allocates; a frame not closed on `return`, or on a `return`
  from inside a loop; arguments worked out right to left; a variable
  argument copied early; the line not stored again after a call; the
  count for a sub not taken down on the way out; the bytes not
  counted; a file variable given a slot a block uses; a default run
  when the argument was given; `//=` treated as `=`; the flag not
  passed through `return f()`. Each must turn a test red.
- **gcc, clang and `make sanitize`**, and Stevan's Mac for the
  limit's test above all: the 1 KB a call is measured on Linux.
- **An adversarial review of this proposal**, started with it: a
  program with a sub in it that would run, not fault, and differ.
- Leave out: lists in or out of a sub, `@rest`, `%opts` (9, 10, 12);
  anonymous subs, `my sub`, closures, a sub in a block (14); `die`
  (15); `Name::f()` (18); any change to what steps 0 to 7 mean.

#### What the review found

A reader with the proposal and perl, before anything was built
(`briefs/step8-review/`: `FINDINGS.md`, the programs it cites with
perl's output, and its two harnesses). Each finding was run again by
the builder and is in `claims.py`. **D73 has what was done about
each**, defaults of the builder's on the safe side, for Stevan to
see.

- **Four ways to be WRONG.** `(...) x N` is a list in an argument, a
  `return` and a last statement, and a call can count it (T143). A
  `//=` or `||=` default runs before the arguments after it are
  copied, so "copies its arguments ... as the sub begins" is not what
  perl does (T144). A last statement under a modifier is worth its
  test (T145), which the proposal said only of `return`. And list
  context goes down through brackets, a unary plus and the right of
  `and` and `or`, none of which the proposal named (T146).
- **Three shapes perl refuses**: `say((f (1)));` before `sub f`, the
  file-handle guess through brackets; `v1_0` as a name; and seven
  loop and branch words that neither list behind the names sweep had
  (T136, T28).
- **Sentences put right**: `-t(2)` is defined; the minus rule is the
  lexer's, wherever a minus is hard against one letter (T135);
  "perl agrees" on a fault's line holds in nine shapes and not for a
  `return` alone on a line with its expression on the next, where
  perl names the expression's line and D34 the statement's.
- **Holes in the test plan**, each a test and a mutation now: the
  order of copies and defaults; a void call still works its value
  out (T148); `my $x += 10;` after a call that set `$x` (T147); the
  walk of D69 through an argument, a builtin, a default and a second
  sub, with two subs that call each other, and the row inside an
  argument, a `return` and a default; the minus rule's seven
  positions and the `say` rule's; the flag for a call in a `for`'s
  parts and under a modifier (void) and in a loop's test (scalar).
- **What held**: late reads in 53 expressions and 28 argument
  shapes; 31 shapes of signature; 24 of what a sub is worth; T134 in
  20 programs; the pragma silences the recursion warning and nothing
  else; 213,685 names of one to three characters, each in 33
  positions the builder's sweep didn't try, both orders; and **a
  value has no past through a sub**: 63 values after nine kinds of
  use, through nine routes, 35 operations on each copy, 136,710
  comparisons of perl with perl, none different.
- **Not checked by it**: the generated C, the collector's roots and
  D68's numbers, nothing being built; clang, the sanitizers, the Mac.

### 9. Arrays and lists (done)

Referee: perl. Size: large.

**Built 2026-11-25**, by Fable 5.2 (the size the line asks for), in
the two sub-steps Q5 asked for, as agreed below and as D76 to D80
have it, with the builder's own defaults in D81 and these findings:

- **9a, arrays and lists. The model first, red before any code**
  (`t/models/list.py`, commit 6d946b0), on step 8's: an array is a
  Python list with a name, a list is the values copied as they are
  met, and the orders of D80 are written out (an assignment to an
  element, `OP=`, a list assignment, a slice of a list). It writes
  410 to 417, about 900 lines on which perl 5.42 agrees with it, and
  20 programs that fault once each, 420 to 439. `t/models/sub.py`
  has D79: 930 to 933, D71's faults, are gone, and a sub that
  returns nothing is no value in a list.
- **The runtime's array** is the collector's second kind of thing: a
  block with its count, its room and storage of its own, which counts
  against the cap. A list is an array with no name, in a temporary of
  the statement that builds it. The kind is a bit of the header's
  mark word, so a string's block is the size it was and step 7's
  numbers stand. Nothing allocates twice: a list is made empty, in a
  slot, and grows by `realloc`, which starts no collection.
- **A call's arguments** are a pointer each when none of them is a
  list, as at step 8, and otherwise one list and a pointer into it
  for each value (`rt_arguments`); either way the sub is handed a
  count and the pointers, and faults for a wrong count itself.
- **D76's walk** is `checkOrder` in the checker: over the parts of
  an expression or a list in the order they run, what each names,
  and whether a later one can change it, through the subs it calls
  (step 8's sets of what each sub changes, which now hold arrays).
- **What the oracle and the sanitizers found in 9a**: `$a['x']`
  warns as perl compiles it, and is refused (the fault test goes
  through a variable); `@a[]` does not compile; `splice` on an array
  that has never held a value did arithmetic on a null pointer, which
  C leaves undefined (UBSan; `shift_values`).
- **9a broken on purpose** (`briefs/step9a-mutations.py`): 66 of 69
  caught the first time. Two were holes, a `splice` whose length runs
  past the end from where it starts, and the left of `||` in a list
  when it is the one given, and 453 closes both; the third was caught
  by a test of step 5's that the script had not been running.
- **9b, `foreach` and the freeze. The model first** again
  (`t/models/each.py`, on `list.py`): 811 to 813, and 35 programs
  that fault once each, 820 to 854, one for every way a frozen array
  is changed, from the block and from a sub, and one for every shape
  that names an array. **T131 came back while it was being
  written**: three of the fault tests pushed onto the array in the
  loop, and perl, which carries on where the language faults, never
  left them. Every change in a fault test's loop is followed by a
  `last`.
- **The freeze is a count on the array**, added to as the loop
  starts, for each array the resolver saw named in the loop's list,
  and taken off on every way out: after the loop's `last_` label,
  before the `goto` of a `last` or `next` to a loop further out, and
  before a `return`'s. The code generator keeps the loops that are
  open round a statement for that. Whatever stores to an array or
  changes its size asks the count first.
- **The loop's list is in a slot of its own**, a declaration no
  program can name, since a statement's temporaries are the next
  statement's too. A loop over one range has no list: two C integers.
- **D77 and the read-only variable** are two walks in the checker.
  D77's is over every scalar anywhere in the list, as its words have
  it, and so it refuses `for my $i (1 .. $n) { $n-- }`, where perl
  would have agreed (T172, D81).
- **T169, found building**: which shapes in a loop's list make the
  element. The fault reaches each of them.
- **9b broken on purpose** (`briefs/step9b-mutations.py`): all 55
  caught the first time it ran; but writing the list of breakages had
  already shown five that nothing would have caught (a change inside
  an expression of the block, in a loop of the sub's own, in the
  third part of a `for`; a string as a counted range's first end; a
  range too long to build), and each got its test before the run.
- **The numbers**: 691 golden tests, 124 unit tests, 609 statements
  about perl; green under gcc, clang, and UBSan with ASan, poison on
  and off.
- **What step 9 hands step 10**: `return` of a list, `@rest` in a
  signature and a list as a sub's last statement are refused still,
  and D79's "one value or none" widens to any number; `$_`, and with
  it `for (LIST)` and the `for` modifier; `map`, `grep` and `sort`,
  which freeze as `foreach` does and are the first to want the
  runtime to call generated code (D68); a slice on the left of `=`,
  `$#a = N`, `exists` and `delete` of an element, `@a` in a string,
  `join`, `reverse`, `wantarray`. The exception D81 leaves open, a
  range's ends in D77, is one line in the checker.

**The proposal, as it was agreed**, with its review's amendments at
the end:

**Proposed 2026-11-25, by Fable 5.2 (the size the line asks for),
and agreed the same day: Stevan took the recommendation on each
question, as the review had amended it, which are now D76 (Q1), D77
(Q2), D78 (Q3), D79 (Q4), and D80 (what had nothing to choose, the
review's amendments, and Q5: two sub-steps). Its adversarial review
found eleven ways to be WRONG: "What the review found", at the end,
says what each is and how the proposal is amended. The text is kept
as it was proposed.**
Everything here about perl was run under 5.42.0
and is in `briefs/claims.py` (52 rows, `T5-more` to `PLAN9-later`,
and the review's 23, `T157` to `T168-repeat`).
Traps: T5, T9, T13, T14, T21, T68, and T149 to T156, found writing
this. The outline this replaces said: `my @a`, literals, elements,
negative indexes, `$#a`, the count in scalar position, list
assignment and swaps, `push`, `pop`, `shift`, `unshift`, `splice`,
ranges, `foreach my $x`, an array as an argument (it flattens);
`return @a` and slurpy parameters wait for step 10; and that the step
decides D17's freezing, `for my $x ($p, $q)`, an index past the end,
slices, a list assignment as a condition, and an element read in an
expression that also removes it.

#### The picture

Until now a variable held one value. This step gives the program
**a row of them, with a name**, and with it the thing Perl is built
round: the **list**, a row of values with no name, which exists only
while a statement is making or using it.

```
 an array: a variable, @a                a list: no variable

   @a  --->  +----+----+----+            (1, 2, @a, f(), 5..7)
             | 10 | 20 | 30 |              |
             +----+----+----+              v   flattened as it is built
              [0]  [1]  [2]              +---+---+----+----+----+---+---+---+---+
              [-3] [-2] [-1]             | 1 | 2 | 10 | 20 | 30 | f | 5 | 6 | 7 |
                                         +---+---+----+----+----+---+---+---+---+
   $a[1]      one element: a value         |
   scalar(@a) how many: 3                  +--> assigned:   my @b = (...);
   $#a        the last index: 2            +--> counted over:  for my $x (...) { }
                                           +--> handed to a sub:  f(...)
                                           +--> printed:   say ...;
```

An array is the first value that **holds values** and the first that
**changes in place**. Both are new to the runtime. The collector has
to follow an array to what it holds, which step 7 was built before
arrays to make room for. And a program can now hold a thing in one
place and change it from another, which is where every question of
this step comes from: perl's lists are rows of *the containers
themselves*, so a `foreach`, an argument, an operand all see a
change made after they were handed their value. D17 decided that
here values flow and containers don't. This step is where that has
to be made true.

The rule for all of it, in one line:

> **A list is a row of values, copied as it is built. Wherever perl
> would have shown a later change through one, the program is
> refused or faults.**

Two ways it is kept: a **freeze**, as the program runs, for
`foreach` (D17: an array that a `foreach` is over can't be changed
until the loop is done); and a **refusal**, as it compiles, for an
element used in an expression whose later part can change its array
(Q1).

#### The language at step 9

- **`my @a;`**, **`my @a = LIST;`**, **`@a = LIST;`**. An array's
  name is its own: `@x` and `$x` are two variables. `@a` and `@b`
  are names an array may have (D55 was about `$a`).
- **A list**: values, arrays, slices, ranges and calls with commas
  between, in brackets; it flattens, so `(1, (2, 3), @a)` is one
  row. One comma may follow the last.
- **An element**, `$a[EXPR]`: the index a whole number, by the rule
  `substr` has for a position. A negative one counts from the end.
  **Reading past either end is undef, in silence, and the array is
  not made longer.** **Storing past the end makes it longer**, the
  gap undef. Storing before the start is a fault (perl dies). An
  element is assigned, stepped and worked on as a variable is:
  `$a[0]++`, `$a[$i] .= "x"`, `$a[5] //= 7`.
- **How many**: `scalar(@a)`, and an array wherever one value is
  wanted: `my $n = @a;`, `"n: " . @a`, `@a + 1`, `if (@a)`,
  `while (@a > 2)`. **`$#a`** is the last index, -1 for none.
- **List assignment**: `my ($p, $q) = LIST;`, `($p, $q) = ($q,
  $p);`, with `undef` for a value to skip, an element as a target,
  and one array last, which takes the rest. The right side is
  finished first. Too few values leave undef; too many are dropped.
- **`push @a, LIST`** and **`unshift`** (each gives the new count),
  **`pop(@a)`** and **`shift(@a)`** (undef from an empty array),
  **`splice(@a, OFFSET, LENGTH, LIST)`** with its shorter forms.
- **A range**, `FROM .. TO`, in a list: whole numbers, each end cut
  toward zero, nothing if FROM is past TO.
- **A slice**, `@a[LIST]`, and of a list, `(LIST)[LIST]`: the
  elements at those indexes, as values.
- **`(LIST) x N`** in a list: the list N times (T101's refusal ends
  for `say`, and T143's for an argument).
- **`for my $x (LIST) { ... }`**, and spelled `foreach`: the block
  once for each value. `$x` is read-only (D17). `last` and `next`
  as in any loop.
- **`say LIST;`** and **`print LIST;`**: each value, one after
  another, nothing between.
- **An array in a call's arguments flattens**, so the count of
  arguments is known only as the program runs; the fault for a
  wrong count is step 8's.
- **In a sub**: its own arrays, new at each call, and the file's.
  `return @a`, a list-shaped last statement, and `@rest` in a
  signature are step 10's, and refused.

#### What perl does that the obvious build gets wrong

- **A `foreach` walks the array itself** (T5): a store to an element
  shows in the loop, a `push` makes it longer, a `shift` skips, a
  new list assigned to the array is walked. Through `(@a, @b)`, a
  slice, `? :`, a named element, and from inside a sub the loop
  calls. A range is fixed when the loop starts.
- **An element as an operand is the container** (T149): `$a[0] +
  chg()` has what `chg` stored; `$a[0] + shift(@a)` is 2 for an
  array that starts 1, 2; `$a[1] * splice(@a, 0, 1)` is 2, where
  reading late gives 3 and reading early gives 2 by luck; and one
  shape warns of a value that was freed. An array's count is a value
  at once: `@a + grow()` is the count before.
- **Flattened arguments are the elements** (T149): `f(@a)` whose
  `//=` default stores to `$a[1]` hands the second parameter the new
  one.
- **`@a || LIST` is the count** (T150): `my @f = @a || (9);` is
  one element, 3.
- **Where one value is wanted, a list-shaped thing is its last, its
  count, or nothing sensible** (T151, T68): `my $x = @a[0,1];` is
  the last; `my $s = splice(...)` the last removed; `my $n = (my
  ($p, $q) = @a);` the count of the right side; `my $x = (1..3);`
  is perl's flip-flop.
- **`pop @a + 1` doesn't compile** (T152), `pop @a || 0` does;
  `shift` alone, at the top level, shifts the program's arguments.
- **An index too large for a number wraps** (T153): `$a[1e30]` is
  defined, for an array of one.
- **A range of strings is another thing** (T154): `"a".."e"`,
  `"08".."11"`; an undef end warns.
- **`for my $x () { }` doesn't compile** (T155).
- **A `my @a` at the top level doesn't empty the array** (T156), as
  T134 has it for a scalar.

#### The questions

**Q1. An element as an operand.** A scalar variable is read when its
operator runs (D14), and the generated C does that by never copying
one. An element could be treated so, but perl's own answer stops
being a rule once the array can change size under it (T149): what it
gives turns on which of its internal values was freed.
(a) **Recommended: an element is read where it stands, a value, and
an expression is refused when a later part of it can change that
array**: store to an element of it, resize it or assign it, by
itself or through a sub it calls, worked out over the whole program
as D69 is. "A later part" is the other operand, a later argument, a
default of the sub being called, a later piece of a row of dots. So
`$a[0] + $a[1]`, `$a[$i++] + $a[$i++]`, `$t[$i] = $t[$i - 1] +
$t[$i]` are as perl has them, and `$a[0] + chg()`, `f($a[0],
shift(@a))`, `f(@a)` with a default that stores to `@a` are refused,
with a message that says to take the element into a `my` first. An
assignment needs nothing new: its right side runs first, as now.
(b) An element is a place, read late like a variable, and the
runtime pins its array against a change of size until the operator
has run: a store is agreed with (`$a[0] + chg()` is 51), a resize
faults. More of perl kept, for a pin in the runtime and its release
on every way out.
(c) Read early and refuse nothing. `$a[0] + ($a[0] = 10)` is then
11 where perl has 20: WRONG.

**Q2. `for my $x ($p, $q)`**, a `foreach` over scalar variables
named in the list (T13): perl walks the variables, so `$p = 7` in
the block shows in `$x`. An array can be frozen; a scalar can't.
(a) **Recommended: the values are copied, and the loop is refused
when its block, or a sub the block calls, can assign a variable
named in its list.** The same walk again. The common loops, `for my
$x ($lo, $hi)` over things the block only reads, are in.
(b) Refuse a scalar variable named in the list always; `($p + 0,
$q + 0)` says a copy is meant.
(c) Leave it refused, as it is.

**Q3. A list assignment as a value.** `if ((my @r = f()))`, `my $n
= (my ($p, $q) = @a);`, `my $c = () = LIST;`: in perl it is the
count of the right side.
(a) **Recommended: a list assignment is a statement, and refused
anywhere else.** `my @r = f(); if (@r)` says it. The countof idiom
`() =` is rare outside golf.
(b) In, as the count. One more thing an assignment can be, and a
test of `if ((my @r = ...))` against D53.

**Q4. A sub that returns nothing, in a list** (D71). Step 8 made it
a fault "until step 10", having no lists. There are lists now, and
the answer is none of them: `my @c = none();` is empty, `(1, none(),
2)` is two values, `g(none())` calls `g` with nothing.
(a) **Recommended: agree now, and D71's fault ends.** A call in a
list gives its one value or none; the argument count is already
counted as the program runs. Step 10 widens "one or none" to any
number.
(b) Keep the fault until step 10.

**Q5. Two sub-steps.** This is the largest step so far: a new kind
of value in the collector, lists through every expression, a loop,
and two static rules.
(a) **Recommended: build it as 9a and 9b, each green and committed**:
9a is arrays, lists, elements, the builtins, list assignment, `say
LIST`, flattening and Q1; 9b is `foreach`, ranges walked without
being built, the freeze, and Q2. One proposal, one review, this one.
(b) One build.

**Nothing to choose, worth your eye.**

- **The freeze** (D17), as it will be: an array is frozen while a
  `foreach` is over a list that names it: the array, a slice or an
  element of it, through brackets, `? :` and `||`. A range, a call
  and any other value freeze nothing, so **`for my $i (0 .. $#a) {
  $a[$i] *= 2 }` is how an array is changed in a loop**. Frozen,
  it may be read by anyone, and any store to an element or change of
  its size, from the loop or from a sub, is a fault, `an array was
  changed while a foreach is over it`. It is a count (two loops over
  one array), and it is given back on every way out: the end,
  `last`, a `next` or `last` to an outer loop, a `return`.
- **What is refused where one value is wanted** (T151, T68): a
  slice, a range, a comma list, `splice`, a list assignment. An
  array there is its count, and `(LIST)[N]` with one index is that
  element.
- **`pop` and `shift` take their brackets**, `pop(@a)`, unless
  nothing follows the array but the end of the expression (T152);
  each names an array, always. `push` and `unshift` are written
  either way, and need a value to add. `splice` has brackets.
- **`scalar(@a)`**, of an array and nothing else.
- **Faults**: an index that is not a whole number by `substr`'s
  rule, undef, or too large to be one (T153); a store before the
  start; `splice` past the end (perl warns) or before the start; a
  range with a string or an undef for an end (T154), or an end
  outside the integers; an array of more than 2^31 elements.
  `out of memory` is as it was.
- **A range as a list is built**, so `my @a = (1 .. 1e9);` is a
  fault for memory; a `foreach` over one range counts and builds
  nothing.
- **A file's array** keeps its slot and is empty as the program
  starts; `my @a;` at the top level stores nothing (T156).
- **Later, and refused with a message**: a slice on the left of
  `=`; `$#a = N`; `exists` and `delete` on an element; `for my ($i,
  $x) (...)`; `for` with no `my`, and over `$_`; `each`, `keys` and
  `values` of an array; `wantarray`; `@a` in a string.
- **The collector** follows an array to its values. A collection
  now costs the live values and not only the slots, so under D64's
  stress a test that builds a large array says its own interval.
- **No reference to an array, and none to an element** (step 13):
  an array is its variable's, and assigning one copies it.
- **A value has no past, asked again**: through an element, a list,
  a slice, `push` and `pop`.

#### The build, once the questions are answered

- **The model first, red** (`t/models/list.py`, on step 8's): an
  array is a Python list in a place, a list a Python list of
  values, the freeze a count. `same` tests: every form above with
  each kind of value; indexes at and past each end; list assignment
  of every shape; each builtin at its edges (`splice` with every
  sign of offset and length); ranges; slices; flattening into calls
  with defaults; `foreach` over every kind of list, nested, left by
  `last`, `next` and `return`; counts in every scalar position; the
  file's arrays from subs; and the operators of steps 1 to 6 on
  values that came through an element. Fault tests, each at its
  edge and each ending under perl: every fault listed; every way a
  frozen array is changed, and that it is not frozen after each way
  out of the loop.
- **By hand**: the programs the language can now say (a sieve, a
  bubble sort, a stack and a queue, Pascal's triangle, a moving
  average); every refusal, with what perl does in its comment.
- **The runtime**: an array as a heap value with its own storage,
  counted against the cap; the mark through it, with no recursion to
  overflow C's stack (arrays hold no arrays yet, and the mark is
  written for when they do); a runtime function that builds a list
  opens a frame; the freeze count. Its own tests in C.
- **The compiler**: arrays and lists in the tree; the resolver's
  second namespace; context in the checker (where a list may stand
  and where one value must); the two walks, with D69's; a call
  handed a count and where each argument is, flattened or not.
- **Break it on purpose**: the mark not following an array; a list
  built in no slot; the freeze not counted, not given back on each
  way out, not looked at by each of the six things that change an
  array; an element copied late, or its index worked out after the
  right side; each walk skipping defaults, or subs; a range built
  for a `foreach`; an off-by-one at each end of every index.
- **gcc, clang, `make sanitize`**; every golden test under stress.
- **An adversarial review of this proposal**, started with it.
- Leave out: `map`, `grep`, `sort`, `join`, `reverse`, `$_`, list
  returns and slurpy parameters (10); hashes (12); references and
  arrays of arrays (13); `@a` in a string (16).

#### What the review found

A reader with the proposal and perl, before anything was built
(`briefs/step9-review/`: `FINDINGS.md`, 45 programs with perl's
output, and its harness for pasts). Each finding was run again by
the builder and is in `claims.py`; T157 to T168 are its traps. **The
proposal's rule was stated for elements and for `foreach`, and
perl's lists hold every container.** Its two tools were the right
ones; each had too short a list of shapes, and the proposal had no
order of evaluation written down, where three forms don't run left
to right. **The text above is as it was proposed. This is how it is
amended, as the builder's recommendation, and all of it is Stevan's
to answer with Q1 and Q2.**

- **Q1, widened: one walk, for everything a list or an expression
  names.** A scalar variable in a list is read when the list is used
  (T157), exactly as an operand is (D14) and an argument (D73). So:
  **a later part of an expression or a list may not change what an
  earlier part names**, where what is named is a scalar variable
  standing as an item of a list, an element, a slice, a whole array,
  or `$#a`; "change" is by itself or through a sub; and "a later
  part" is anything worked out after it, an index of an assignment's
  target included. Refused, with one message. What stays agreed with,
  because the generated C already keeps the place: a scalar variable
  as an operand and as an argument of a call.
- **The order, written down** (T158, T159, T163), and agreed with:
  `$a[I] = V` works out V's calls, then I, then reads V and stores;
  `$a[I] OP= V` and a step work out I, **make the target** (the
  array grows to hold it, or it is the fault for before the start:
  T160), then V, then read, work and store; a list assignment works
  out its right side, then every target's index, then stores; a list
  slice works out its indexes before its list. A right side that can
  change the size of its target's array is refused by the walk.
- **The freeze, widened** (T162): of **every array named anywhere in
  the `foreach`'s list**, whatever it stands in; and Q2's refusal of
  every scalar named anywhere in it. It costs only loops that were
  going to be WRONG.
- **Past the end, where perl makes the element** (T161): an element
  or a slice past either end in a `foreach`'s list, and a slice past
  either end in a call's arguments, is a fault.
- **A slice of an empty list is empty** in a list (T164), and undef
  where one value is wanted: agreed with.
- **More faults**: `splice`'s offset and length by the index's rule
  (T165); a `foreach` over one range whose end is below -2^63 + 513,
  where perl dies (T166).
- **More refusals** (T167, T168): `@a[one index]`; `defined` and
  `length` of an array; a comma after an assignment's right side,
  `my @a = 1, 2, 3;`; `[` after a call's own brackets; `$a[0][0]`;
  `my ($x, $x)`; an array among a list assignment's targets that is
  not the last; a list assignment as a sub's last statement has no
  value (D18); a comma list on the left of an `x` where one value is
  wanted.
- **Three sentences of the proposal that were wrong about perl**,
  put right here: "the right side is finished first" (its calls
  are; what it names is read at the store); "its index worked out
  after the right side" as a breakage (for `=` that is perl's
  order); and "`splice` past the end (perl warns)" (only with a
  length; the fault stands for both).
- **Holes in the test plan**, each a test now: a printing sub in
  every operand of every new form; every one of the 22 ways an array
  is changed, against the freeze, from the block and from a sub;
  the freeze given back through two loops; T156 for each shape of
  `my`; indexes at both edges of the integers; `1..3` with no blanks
  (today's lexer reads a number); `say` with an undef in its list.
- **What held**: an array's count in 29 positions; 60 ranges against
  the rule; 53 calls of `splice`; Q4(a) in 14 positions; T155, T156;
  about 25 list assignments whose right side names what the left
  changes; and **a value has no past through an array**: 443,205
  comparisons of perl with perl, through 23 routes, none different.
- **What the freeze costs**, for Stevan to know: perl prints what a
  copy would, and the language faults, for doubling in place by an
  index kept beside the loop (`$a[$i] = $x * 2; $i++;`), which is
  the common one; for `push` and then `last`; for `pop` on the last
  time round.

### 10. List operators, `$_`, list returns

Referee: perl. Size: large.

**Proposed 2026-11-25, by Fable 5.2 (the size the line asks for),
and agreed the same day: Stevan took the recommendation on each
question, which are now D82 (Q1, with a note on the licence), D83
(Q2), D84 (Q3), D85 (Q4) and D86 (Q5). Its adversarial review
found six ways to be WRONG: "What the review found", at the end,
says what each is and how the proposal is amended (D87). The text
is kept as it was proposed.**
Everything here about perl was run under 5.42.0 and is in
`briefs/claims.py` (46 rows, `T173` to `T184-global`). Traps: T3,
T4, T6, T8, T10, T15 to T18, T20, T23, T29, T41, T54, T59, T61, and
T173 to T184, found writing this. The outline this replaces said:
`map`, `grep`, `sort` with and without a block, `join`, `reverse`,
`foreach` and postfix `for` over `$_`; slurpy parameters; `return` of
a list, and D18's fault, with void as the third context; and that
the step decides block or hash after `map` (D21), `sort`'s
comparator (D14), a string as a range's end (T41), `map EXPR, LIST`,
`my $a` and `my $b` (T61), and `last` out of a `map` block (T59).

#### The picture

Three things, each standing on the one before.

**1. A sub gives back a list.** Step 8 gave every call a flag with
perl's three contexts, and step 9 a list to put values in. So this
is small: where a list is wanted, a call adds every value its sub
returned, where step 9 had "one or none". `return LIST`, a list as a
sub's last statement, `@rest` in a signature, and D18's fault for a
list-shaped `return` that reaches a call wanting one value. `join`
and `reverse` come here, being the two list builtins that are only
functions.

**2. `$_`, and the constructs that bind it.** `for (LIST) { }`,
`STATEMENT for LIST;`, `map { } LIST` and `grep { } LIST` are each
step 9b's `foreach` under another spelling: the list copied once,
every array named in it frozen, D77's refusal, and a block that runs
once for each value with `$_` that value. The block is compiled where
it stands, as a loop's block is: **`map` is a loop that adds its
block's value to a list**, and `grep` one that adds `$_` when the
block is true. Nothing calls anything, and D68's question does not
come up for them.

**3. `sort`, which is not a loop.** Which two values are compared
next depends on how the last comparison came out, so the block can't
be laid out as a loop's body by the compiler alone: the sorting and
the block have to take turns. Q1 is what order perl's comparisons
come in and whether it shows; Q2 is who is in charge of the taking
of turns.

#### The language at step 10

- **`return LIST;`** and a list as a sub's last statement: to a call
  where a list is wanted, every value. **D18's fault**: a `return`
  (or a last statement) that is *list-shaped*, reached by a call
  that wants one value, faults: `f returned a list where one value
  is wanted`. List-shaped is by the tree, as D18 has it: an array, a
  comma list, a slice, a range, `(LIST) x N`, `splice`, `map`,
  `grep`, `sort`, `reverse`, and `? :` or `|| && //` with such an
  arm, whichever arm is taken. `return (7);` is one value, and
  `return ();` is `return;`. `return f();` hands its own context on.
  A void call faults for nothing.
- **`sub f($x, @rest)`**: a last parameter that takes every argument
  left, as a new array of copies; `@` alone takes and names nothing.
  No default, and nothing after it: perl compiles neither (T182).
- **`join(SEP, LIST)`**, with brackets or without: SEP is one value
  (an array there is its count, T182), each value of the list is
  made a string as `.` makes one, so undef faults.
- **`reverse LIST`**, where a list is wanted.
- **`for (LIST) { ... }`** and **`STATEMENT for LIST;`**: `foreach`
  with `$_` for its variable. The statement is what may stand before
  `if` today.
- **`map { ... } LIST`** and **`grep { ... } LIST`**. The block is
  statements, the last an expression with no modifier, which is its
  value: for `map` a list (any number of values, none too), for
  `grep` one value, tested for truth. A `my` in the block is new
  each time round. They take every value to the end of the list they
  stand in, as perl's list operators do: `(9, map { $_ * 2 } 1, 2)`.
- **`$_`** is read-only (D17), and is seen in the block or the
  statement of the construct that binds it and nowhere else: not in
  a sub that block calls (to perl it is one global variable, T180).
  A binder inside another hides the outer `$_`.
- **`sort LIST`**: by string, as `cmp` orders, and stable. **`sort
  { ... } LIST`**: `$a` and `$b` are the two values being compared,
  read-only, seen in the block alone; the block's value says which
  comes first.
- **Frozen while they run**: every array named anywhere in the list
  of a `for`, a `map`, a `grep` or a `sort`; and D77's refusal for a
  scalar named there that the block can change.

#### What perl does that the obvious build gets wrong

- **`sort`'s comparisons come in an order, and it shows** (T3, T173):
  for `(5,3,8,1,9,2,7)` perl compares `53 81 92 31 38 58 27 79 12 23
  37 75 78 89`, the same pairs every run, and another sequence when
  the block is `$b <=> $a`. A block that prints, counts or stores
  shows the order. So does one that is not a consistent order: `sort
  { 1 }` of 1 to 5 is `5 4 3 2 1`, `sort { -1 }` is `1 5 3 2 4`.
  **And the commonest block of all is not consistent at the edge**:
  D49 compares an Int with a Num as doubles, so 2^53 + 1 equals the
  Num 2^53, which equals the Int 2^53, which is less than 2^53 + 1;
  perl sorts those three one way, and another merge would sort them
  another.
- **The block's value is cut to a whole number and then to 32 bits**
  (T173): 0.5 is "equal", 4294967296 is "equal", 2147483648 is
  "less".
- **`return` in a `sort` block ends the comparison, and in a `map`
  block ends the sub** (T174).
- **A block or a hash?** (T175, T54) perl looks at the first thing
  after `{`: a string or a number or a capitalised word, and then a
  comma, and it is a hash and a syntax error; so is `{ }`. `map {
  "a", $_ }` and `map { 1, $_ }` do not compile; `map { $_, 1 }`,
  `map { 1.5, $_ }` and `map { -1, $_ }` do.
- **A block that ends in an `if`** gives the empty string where the
  test fails (T176); `grep { ($_, 0) }` takes the last and warns.
- **`map` and `grep` make an element that is not there, as `foreach`
  does; `sort`, `join` and `reverse` do not** (T177).
- **Where one value is wanted** (T178): `grep` and `map` are a
  count; `reverse` joins its arguments and reverses the characters;
  `sort` is undef, with a warning.
- **`sort` works on the array's own elements** (T179, T10): a store
  to the array in the block shows in the result, `$a++` rewrites the
  array, and a `push` in the block of `@a = sort { } @a` is lost.
- **`$_` is one global variable** (T180, T15): a sub called from the
  block sees it, and a sub called from a `sort` block sees `$a`.
  `$_ *= 2` in a `for`, a `map` or a `grep` rewrites the array.
  `map { length }`, `grep { defined }` and `say for` mean `$_`.
- **`push @a, 9 for @a;` never ends** (T181; T131's kind).
- **A list where one value is wanted, through a call** (T183, T16 to
  T18): `(4, 5, 6)` is 6, `reverse` the joined string, `map` a
  count, `splice` its last, `sort` undef, a range the flip-flop.
- **Context is syntax** (T183): the last statement of a `map` block
  is called for a list, of a `grep` or `sort` block for one value,
  `join`'s first argument for one value, and a `map` in a `return`
  is a list whatever the sub was called for.

#### The questions

**Q1. The order of `sort`'s comparisons.** perl's is fixed, and a
program can see it three ways: an effect in the block, a block that
is no consistent order, and a fault in the block (which pairs are
compared decides whether a division by zero is ever reached).
(a) **Recommended: perl's merge, ported.** It is `pp_sort.c`'s
`S_sortsv_flags_impl`: runs found first (`dynprep`), then merged,
about 450 lines of C. Every comparison is then the one perl makes,
in perl's order, so every block agrees, an inconsistent one too, and
the oracle is exact: a block that logs each pair it is given, run
under perl and here over some thousands of arrays (sorted, reversed,
runs of sixteen and more for the long-run path, many equal keys for
the galloping one). D14 named this choice, and Chalk made it.
**One thing for Stevan to say yes to**: that file is perl's, "under
the same terms as Perl itself", and a port of it into the runtime is
a derived work that is linked into every compiled program; the
repository has no licence file yet.
(b) A merge of the language's own, and the block held to what can't
show: refused if it or a sub it calls changes anything or prints,
and a fault... for what? The edge of `<=>` above is the ordinary
block on ordinary values. Every comparison of an Int of 2^53 or more
with a Num would have to fault inside a `sort`, and a block that is
not `KEY($a) OP KEY($b)` refused. More rules, and they buy only not
porting.

**Q2. Who is in charge: the sort, or the generated code?**
(a) **Recommended: the generated code.** The runtime's sort is made
so that it can stop and be taken up again: `rt_sort_next` runs the
merge as far as the next comparison and hands back the two values;
the generated C runs the block, inline, as it would a loop's, and
hands the answer to the next `rt_sort_next`. In C that is the ported
merge with its variables in a struct and each comparison a place it
can return from and come back to (a `switch` on where it was). The
runtime still never calls generated code, a `sort` block is laid out
like a `map` block, and nothing new sits on the C stack between the
program and its block: what D68 asked to be kept open for step 29
stays open. The cost: the port is less of a copy of perl's text, so
it leans on the logged comparisons to show it is the same.
(b) The runtime calls the block, as a C function handed its
caller's frame. The port stays close to perl's text. It is the first
call from the runtime into generated code, and it puts the runtime's
C frames between a program and what its block calls, which is the
shape that is hard to undo when a call stops being a C call.

**Q3. `grep` and `map` where one value is wanted.** `my $n = grep {
... } @a;` and `if (grep { $_ eq $x } @a)` are the count, in perl,
and everyday (T178).
(a) **Recommended: the count, for both, as perl has it.** It is
what an array is where one value is wanted, and costs a line.
`sort` and `reverse` there are refused: perl's `sort` is undef with
a warning, and its `reverse` is another function (of strings, for
the step that has strings to propose). A `return grep { ... } @a`
reached by a call for one value is still D18's fault.
(b) Refused, with step 9's lists: `my @m = grep ...; my $n = @m;`.

**Q4. `map EXPR, LIST`, and the builtins that mean `$_` when given
nothing.** perl has `map lc, @a`, `grep $_ > 1, @a`, `grep {
defined } @a`, `say for @a` (T180).
(a) **Recommended: neither. A block always, and `$_` always
written.** `map EXPR, LIST` is the form where perl's parser guesses
(`map ($_ * 2), (1, 2)` is a `map` of nothing, with a warning), and
a builtin with no argument is already refused for what perl reads
after it (T94). `grep { defined($_) } @a` says it.
(b) `map EXPR, LIST` too. (c) Both.

**Q5. One step or three?**
(a) **Recommended: three, each green and committed.** 10a: list
returns, D18's fault, slurpy parameters, `join`, `reverse`. 10b:
`$_`, the two `for`s, `map`, `grep`. 10c: `sort`.
(b) One.

#### What has nothing to choose

- **Refused in a `map`, `grep` or `sort` block**: `return` (T174:
  perl gives it two meanings), `last` and `next` to any loop (T59).
- **A block's first token** (T175, D21): refused when it is a string
  or a number or a word and a comma follows, and when the block is
  empty; perl compiles none of them as a block. No comma after the
  block.
- **A block that does not end in an expression** is refused (T176),
  as a sub that ends so has no value.
- **The block's value in a `sort`** is a whole number by the index's
  rule, a fraction cut toward zero as perl cuts it, and a fault
  outside 32 bits, where perl wraps (T173).
- **Past the end** (T177): D80's fault for an element or a slice in
  the list of a `for`, a `map` or a `grep`; not of a `sort`, a
  `join` or a `reverse`, where perl makes nothing.
- **`$a` and `$b`** are names in a `sort` block alone (T61, T10);
  `$_` in its binder alone. A sub can't see either.
- **`sort` with no list, `sort NAME LIST`, `sort $f LIST`** (T29),
  `wantarray`, a string as a range's end (T41: still the fault).
- **D76 goes through a block**: what a block changes is what its
  `map`, `grep` or `sort` changes, for the walk.

#### The build, once the questions are answered

- **10a.** The model first, on `list.py`: a call's values, the
  fault by shape and by context, slurpy parameters, `join`,
  `reverse`. The call convention grows by one case: to a list a sub
  hands back a list. Fault tests: every list shape, through every
  arm, to every kind of place that wants one value.
- **10b.** The model on `each.py`: the binders are `foreach` with a
  name. Fault tests: 9b's, again for each binder (every way of
  changing a frozen array, every shape that names one, every way
  out), and T131's rule for every one of them.
- **10c.** The merge twice: in the model, in Python, and in the
  runtime, in C, each held to perl by logged comparisons, and to
  each other. Unit tests in C for the machine itself: stopped and
  taken up at every comparison, a collection at each.
- Tests are numbered from 1000: 000 to 999 has two small gaps left.
- **Adversarial review before any of it is built**, as the rule has
  it. What I would ask it first: whether perl's numeric `sort`
  leaves the values it sorted with a past that shows (it turns
  strings to numbers in place); `$_` and `$a` reached in ways the
  lexical rule does not see; contexts D18's shapes miss.

#### What the review found

**Six ways to be WRONG, eleven shapes perl warns of or refuses, and
a dozen places the text left a builder to guess**
(`briefs/step10-review/`, with its programs and two harnesses; T185
to T192, 20 more rows of `claims.py`). None changes an answer to Q1
to Q5. One line covers the three largest: `grep`, `sort` and
`reverse` hand on the containers they were given, as a list does; a
`sort` with a block treats its list as `map` and `grep` do; and what
perl does for a `sort` turns on whether it could throw the block
away, which it does for `{ $a <=> $b }` and its three kin, the only
block this proposal had tried. The amendments, which D87 records:

- **`grep`, `sort` and `reverse` name what their list names** (T185,
  W1): for D76's walk, with a scalar counted as an item. `(reverse(@a),
  chg())` has what `chg` stored, in perl. `map` copies and names
  nothing.
- **`join`'s separator is the first item of its list**, for that
  walk (T186, W2): perl reads it when `join` runs.
- **An undef in an array sorted in place is a fault** (T187, W3).
  `@a = sort BLOCK @a` is done in place by perl, which drops every
  element that was never stored, and whether one was is a past of
  the array's that the language does not keep. In place is `@a = sort
  ... @a`, through brackets on either side; `reverse sort` and a
  `sort` into another array are not.
- **Past the end, in a `sort`'s list too** (T188, W4): D80's fault,
  whatever the block. The proposal's "not of a `sort`" was wrong.
- **A word first after `sort`** that is not one of perl's own words
  is refused (T189, W5 and W6): a sub's name, with its brackets too,
  is the comparator to perl, and `true` there is the string `true`.
  `sort +k(), 3` and a block say what was meant.
- **A `sort` of one value** with no block, or with one of the four
  blocks perl throws away, looks at that value as a comparison would
  (T190): perl turns every value to a number or a string before it
  sorts, and warns.
- **`map`, `grep` and `sort` take no brackets of their own**: `sort
  (@a), 9` warns (T190), `sort(k(), 3)` and `sort k(), 3` differ,
  and `[` after them does not compile. `join(...)` and `reverse(...)`
  are functions, with brackets or without.
- **`join`'s separator is made a string whatever the list holds**
  (T190): an undef there faults with nothing to join.
- **Under a `for` modifier**: not `last`, `next` or `return` (T191:
  `last for 1, 2;` leaves the modifier's own loop), and not a second
  modifier (T192). `for () { }` is refused, as T155.
- **A slurpy parameter is filled when its turn comes**, after every
  default, from where the arguments are (T191), as each parameter
  before it is.
- **A binder's list sees the `$_` outside it**; and `$_`, `$a` and
  `$b` are seen through a block that binds another of them (T191).
- **In a block**: `return` at any depth is refused; `last` and
  `next` are refused when their loop is outside the block, and fine
  for a loop inside it (T192). A `{` first is refused (T192: a hash,
  to perl). A block's last statement is a value: two joined by `or`
  or `and` too (`$a <=> $b or $a cmp $b`), and an assignment to a
  scalar; a list assignment has none (D78) and is refused there.
- **T111's refusal knows `$_`, `$a` and `$b`** (T192): `say $_ -1`
  is a file handle to perl. `$_[0]` is refused.
- **T143's refusals end**: `(LIST) x N` after `return`, as a last
  statement and in a `map` block is a list, and list-shaped for D18.
- **`map` and `grep` may be statements** (perl does not warn);
  `sort`, `reverse` and `join` alone are a statement that only has a
  value.
- **What stood**: the numeric past, which the proposal asked about
  first. 108,416 comparisons of perl with perl through 32 routes;
  1,106 differ, and the compiler already faults on every one. The
  blocks perl throws away decide as the block would, pair by pair:
  21,600 sorts, values on both sides of 2^53 among them. The order
  of comparisons is the same in place, into a copy and under
  `reverse`, over 3,000 arrays. Context is syntax, 75 calls; D18's
  shapes, 47 `return`s.

### 11. The census

Referee: perl. Size: medium.

D11; perigrin has agreed. Import the probes and the graded corpus into
`t/census/`, each with perl 5.42's output regenerated here; `make
census` gives each a verdict and writes the counts; `t/checks.py`
holds WRONG to 0 and SAME from falling. From here every step's report
says how the census moved. Every WRONG found is fixed before the next
step, and turned into a golden test.

### 12. Hashes

Referee: perl. Size: medium.

Literals, elements, `exists`, `delete`, `keys`, `values`, a hash in
list and scalar position, slurpy `%opts`, slices. D27. The first step
to meet the oracle check's reading rule in earnest: read `TRAPS.md`,
"The checks themselves", and `t/checks/README.md` first, and have the
check reviewed again once this step's tests exist. A hash is
frozen while `values`, a slice or the hash itself is being iterated,
and not while its `keys` are (D17, T7). A `same` test sorts its keys;
D10's check rejects one that doesn't. `=>` quotes the word on its
left, whatever the word. Traps: T2, T7, T63.

### 13. References and nested data

Referee: perl. Size: large.

`\@a`, `\%h`, `\$x`, `[ ]`, `{ }`, the arrows, postfix dereference,
`ref`. Decides: writing through undef (proposed: as perl, which is
silent); reading through undef or a missing key (proposed: fault; perl
creates the container on the way, and so do `foreach`, `map` and
`keys` over a missing one); a reference as a string or a number, and
which comparisons of references are allowed (D14: `==` and `!=`
only); dereference without braces, `@$x` and `$$x[0]` (proposed:
cut, as Stevan's own style guide has it, leaving `->@*` and `@{ }`).
Traps: T12, T42, T48 to T50.

### 14. Closures

Referee: perl. Size: large.

Anonymous subs, captured variables, `my sub`, `__SUB__`, calling
through a reference, `state`. The resolver's capture analysis; a
captured variable lives in a cell on the heap. Decides: a closure
over, or a reference to, a `foreach` variable (D17: refused so far,
since perl's closure keeps the alias to the array's element after the
loop has ended; `for my $x (@list) { push @subs, sub { $x } }` is too
common an idiom to leave refused, so this step either gives it perl's
meaning or finds the fault that makes a copy safe). Traps: T11.

### 15. `die`, `try`, `catch`

Referee: perl. Size: large.

A `die` with a string (and perl's ` at FILE line N.` when there's no
newline, byte for byte) or with an object; `try` and `catch`; an
uncaught `die` (D12, tests of kind `dies`); `warn`, and how a test of
it is checked (D10). Decides: how unwinding is compiled
(`setjmp` and the shadow stack, or a test after each call); `finally`
and `defer`; `...`. `return` inside `try` returns from the sub, so
unwinding can't be one mechanism shared with `die`. Confirms D13 with
tests of what `try` does not catch. Which line a `die` reports, and a
comment that changes it (T74). Traps: T53, T65, T70, T74.

### 16. Strings, the rest

Referee: perl. Size: large.

Interpolation, `q`, `qq`, `qw`, heredocs, `sprintf` and `printf`, the
remaining string builtins. Decides: exactly which shapes interpolate
(perl guesses at `"$x[1]"`, `"$h{a}"`, `"@name"` and an email address;
D21 says refuse what it has to guess). Traps: T9, T22, T23.

### 17. Classes

Referee: perl. Size: large.

D19: `class`, `field`, `:param`, `:reader`, `method`, `ADJUST`,
`:isa`, `new`, method calls, `isa`, `SUPER::`. A missing method is a
fault, and so is an unknown constructor argument. A field is a slot
of the object, never a copy. From `perlclass`, each to be run under
5.42 first: a parent's fields are not visible in a subclass (T56); a
`:reader` on an array field is list-shaped (D18); `:writer` makes
`set_x`, not `x`; a lexical method is called with `->&`; `:isa` loads
its parent, so a parent the program doesn't define is refused (D20).
Traps: T52, T56.

**Roles, from the start** (Stevan, 2026-11-25). He wants roles to be
a key part of the object system, and not left for the metaobject
protocol, so this step's proposal takes them up beside `class`
instead of leaving them to step 27. Nothing about them is decided;
this is a note of where the question is to be raised, not an answer
to it. Read two of his repositories first, both public (a session
clones them with `add_repo`):

- `stevan/p5-roles-algebra`: `ROLE_ALGEBRA.md`, an algebra of role
  composition for `feature 'class'` (every class and role built from
  a proto-role; composition that never fails, and a resolution step
  apart from it; two methods or fields the same only when they come
  from the same package); `SLOTS.md`, the same algebra over slots;
  and tests of it against Moose, Moo, Role::Tiny, Object::Pad and the
  mop (`t/`, `bin/conformance-report`).
- `stevan/p5-core-role-tests`: programs written for roles in core,
  `role Name { }` and `class Name :does(...)`, with the roles they use
  in `lib/`.

**perl 5.42 has neither** (run 2026-11-25: `role Eq {` is a syntax
error, and `:does(...)` is `Unrecognized class attribute does`), so
roles are still an exception to D2 (D5) wherever they are built, and
the proposal says what referees them: whether they erase by being
flattened into the classes that use them, which would keep perl as
the oracle (step 27's option), and whether the algebra's tests can be
the model. It also says whether roles are a step of their own,
straight after this one, and what is then left for step 27.

### 18. Modules

Referee: perl. Size: large.

`package Name;` as the name of a file's subs, and nothing more (D19);
`use Name;` of the program's own files, found at compile time; a sub
of another package called as `Name::f($x)`. Decides: how files are
found; imports, if any (`Exporter` needs package variables, which are
cut); `package Name { }` as a block; `__PACKAGE__`; core modules
(`List::Util`, `Scalar::Util`, `POSIX`, `constant`). Crayon's four
modules are the worked example of what a port has to bend: `use
Exporter 'import'; our @EXPORT_OK`, and a trailing `1;`.

### 19, 20. Regexes

Referee: perl. Size: large, twice.

Matching, then substitution, `split`, `tr` and `qr`. The pattern is
compiled by the compiler into a program the runtime's matcher runs, a
backtracking matcher with perl's order of trying. Decides: the subset
(`SURFACE.md`); `$1` or only returned and named captures; a step limit
on backtracking, since a regex is the one place a small program can
run for ever by accident. Traps: T66, T67.

### 21. Files and the outside

Referee: perl. Size: large.

`open`, `close`, `readline`, `eof`, `print` to a handle, stdin,
`@ARGV`, `%ENV`, `exit`, file tests. Decides: handles as values;
`print $fh LIST` or only `print {$fh} LIST` (D21); what an error from
the system is (`$!`'s text comes from the C library and differs
between machines, so a `same` test can't print it).

### 22. Numbers and time

Referee: perl. Size: medium.

The numeric builtins, the bit operators on integers (T46), `rand` and
`srand` (perl's own generator, so a seeded program agrees with perl on
every machine), `time` on a virtual clock in tests.

### 23. The prelude, in the language

Referee: perl. Size: medium.

`lib/prelude.pl`, compiled into every program. Builtins that can be
written in the language move there from the runtime, with the same
tests. The 2007 idea: a small set of primitives, and the rest as
library.

### 24. Examples

Ports, each a golden test, each bending to the language (D8). The
table below. And one measurement, not a gate: Chalk's own `lib/`,
file by file, as REFUSED (and for what) or compiled. It is the subset
this language started from (D4), and the list of reasons is the
truest account of how far apart the two have grown.

### 25, 26. Gradual types

Referee: perl, through the erasure. Size: large, twice.

To be proposed. Annotations on variables, parameters, fields and
returns, checked over the tree and erased (`curlyc --erase` prints the
Perl); then types put to work, removing the runtime's checks where a
value's type is known, and turning D18's fault and several of D15's
into refusals. Starting points: Chalk's lattice and `Maybe[T]`
(`BACKGROUND.md`), Opal's typed builtins, Allium's tower. D2 holds:
erased, it's Perl.

### 27, 28. Roles; the metaobject protocol

Referee: to be decided. Size: large, twice.

To be proposed; exceptions to D2. One option to weigh: roles that
erase by being flattened into the classes that use them, which is
what composing a role means, and which would keep perl as their
oracle. **Roles are to be taken up at step 17 instead** (Stevan,
2026-11-25: see there), so what is left here, if anything, is what
step 17 doesn't take.

### 29. Concurrency

Referee: a model of the schedule. Size: large, several steps.

To be proposed; an exception to D2. D28 is the only commitment so far.
The workbench's determinism rules apply in full: a seeded scheduler, a
virtual clock, record and replay. D13 is revisited here.

### 30. Tooling

The runtime cached between compiles, tests in parallel, the guide's
code checked, a decision browser (`tools/decisions/` in the workbench).

## Proposals

Waiting: **step 5**, written out above with its four questions. D1
to D51 are agreed.

## Example-port table

| Example | From | Needs | Status |
|---|---|---|---|
| Factorial, Fibonacci, gcd, even and odd | Opal `tests/` | step 8 | waits |
| 99 bottles | Opal `tests/` | steps 6, 16 | waits |
| Ackermann, Hanoi, Collatz, binomial | Opal `author/TESTING.md` | step 8 | waits; none may go 100 calls deep until step 8 says how that is tested |
| Sum of digits | Opal `author/TESTING.md` | steps 8, 22 (`int`) | waits |
| Opal's `t/*.t` with a TAP library in the language | Opal `t/`, `lib/Test.opal.pm` | steps 14, 18 | waits; the library leans on dynamic scope and must change (D8) |
| `Chalk::Grammar::Symbol`, `Rule` | Chalk `lib/Chalk/Grammar/` | step 17 | waits |
| About 25 small programs: subs, classes, references, `try` | Crayon `docs/superpowers/plans/2026-03-31-crayon-interpreter.md` | steps 8 to 17 | waits; their expected values were written by hand and some are wrong, so perl writes them (D7); four must bend (`show 42`, `:writer`, roles, a subclass reading a parent's field) |
| The graded corpus, tier by tier | perl5-son `t/corpus/mdtest/pvm/` | step 11 | waits on D11 |
