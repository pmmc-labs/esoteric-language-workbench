# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** steps 0 to 3 were done on 2026-11-24: arithmetic on Ints
and Nums, and strings, compile, run, and are checked against perl
5.42. So do booleans, undef, comparison and logic: **steps 0 to 4
are done** (step 4 on 2026-11-25). **Step 5, variables, assignment,
blocks and `if`, is proposed, below, and waits on four answers from
Stevan** (Q1 to Q4); nothing of it is built. Steps 6 to 30 are
outlines: each is proposed, with options, when it's next.

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
  something else; 380 to 406 are the refusals.

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

### 5. Lexical scalars, assignment, blocks, `if` (proposed, not agreed)

Referee: perl. Size: large.

**Proposed 2026-11-25. Nothing is built, and four questions are
Stevan's: Q1 to Q4 below; Q5 is four things with nothing to choose
that are worth his eye.** Everything here about perl was run under
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

### 6. Loops

Referee: perl. Size: medium.

`while`, `until`, their postfix forms, the C-style `for`, `last` and
`next`, labels. A bare block is a loop that runs once, for `last` and
`next` (T32). `last` and `next` are allowed only inside a loop of the
same sub, as written (T60). If `do BLOCK while` is wanted, it runs the
block first (T64). The comma operator, in a C-style `for`'s slots
only. A program can now run for a long time: `t/run.sh`'s
watchdog matters from here.

### 7. The collector

Referee: none; the knobs are the test. Size: large.

D26: precise mark-and-sweep, the shadow stack in the generated C, the
stress interval, poison on free, a heap cap. Tests: every earlier
golden test under stress 1 (a collection at every allocation); a loop
that allocates a gigabyte of strings under a 16 MB cap; `make
sanitize`. Before arrays, so that every container after is written
with roots from its first line.

### 8. Subs

Referee: perl. Size: large.

Named subs with signatures, positional parameters and defaults; calls
with brackets (D21), before or after the definition; `return`;
recursion. A wrong number of arguments is a fault (perl dies). A sub
stands at the top of the file and may not be named for anything perl
knows (D21; T28, T31). A sub that ends in a compound statement has no
value (D18, T19). Signature placeholders and `//=` defaults; `:$x`
is not Perl (T55). Traps: T1, T19, T28, T31, T55, T60.
Decides: **how deep a program may recurse**, and what happens past it
(perl has no limit and only warns at 100; the C stack does have one,
so the limit is a number, a fault, and a test, not an accident; the
workbench's interpreter experiment found exactly this), and how a
test that goes 100 deep is checked, since perl warns there (D10); the
hidden context flag (D18), though nothing list-shaped exists yet.

### 9. Arrays and lists

Referee: perl. Size: large.

`my @a`, literals, elements, negative indexes, `$#a`, the count in
scalar position, list assignment and swaps, `push`, `pop`, `shift`,
`unshift`, `splice`, ranges, `foreach my $x`, an array as an argument
(it flattens). `return @a` and slurpy parameters wait for step 10 and
are refused until then. Decides: D17's freezing, with its tests of
kind `fault`, each written so that perl finishes; `for my $x ($p,
$q)`; an index past the end (perl: undef reading, extends writing);
slices; a list assignment as a condition; an element read in an
expression that also removes it (D14). Traps: T5, T9, T13, T14, T21,
T68.

### 10. List operators, `$_`, list returns

Referee: perl. Size: large.

`map`, `grep`, `sort` with and without a block, `join`, `reverse`,
`foreach` and postfix `for` over `$_`; slurpy parameters; `return` of
a list, and D18's fault, with void as the third context. Decides:
block or hash after `map` (D21); `sort`'s comparator (D14: frozen so
that an effect faults, or perl's merge ported; `$a` and `$b` are the
block's, read-only, and refused elsewhere); a string as a range's end
(T41); `map EXPR, LIST`; `my $a` and `my $b` refused (T61); `last`
out of a `map` block refused, and the freeze released on every exit
that is allowed (T59). Traps: T3, T4, T6, T8, T10, T15 to T18, T20,
T23, T29, T41, T54, T59, T61.

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
oracle.

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
