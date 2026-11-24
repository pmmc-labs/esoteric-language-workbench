# Plan

Ghuloum's incremental approach: the compiler works and its tests pass at
the end of every step, and each step adds one feature. Steps are sized to
be a session or two each.

**Progress:** nothing is built. Steps 0 and 1 are written in full, and
every decision they cite is made. Next: step 0. Steps 2 to 30 are
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

The workbench's, with these differences:

| Path | |
|---|---|
| `bin/curlyc.ts` | The driver: `curlyc -o out file.pl` |
| `compiler/src/` | `lexer.ts`, `parser.ts`, `ast.ts`, `resolver.ts`, `checker.ts`, `codegen.ts`, `names.ts` (the one table, D29), `errors.ts` |
| `compiler/tests/` | Unit tests per pass |
| `runtime/` | `rt.h`, `rt.c`, and a file per subsystem as they come (`gc.c`, `str.c`, `re.c`) |
| `lib/` | The prelude and the libraries, in the language (step 23 on) |
| `t/` | Golden tests `NNN-name.pl` and `.expected`; `run.sh`; `checks.py`; `models/` |
| `t/census/` | Other people's probes and their verdicts (step 11) |
| `examples/` | Ports; each with a `.expected` is a golden test |
| `docs/` | These documents, and `LANGUAGE.md` |

There is no `t/referee/` until a step needs one: perl is the referee.

## Steps

Each step says what it adds, what it decides, what tests it adds, and
what it leaves out on purpose.

### 0. Scaffold: `say 42;`

Referee: perl. Size: medium; large for `t/checks.py oracle`, which is
new and which everything after leans on.

Decisions: D3, D10, D12, D13, D16, D23 (the range of a literal), D25,
D28, D29, D30, D31, D32, all made. Traps: T24.

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

### 1. Integer arithmetic

Referee: perl. Size: large for the model, medium for the build once
the model and its tests are red.

Decisions: D23 (the Int half), D13, D15 and D21 (the refusals below).
Traps: T25, T27.

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

### 2. Num, division, `**`, numeric literals

Referee: perl. Size: large.

Decides: D23 in full, against perl, before building. Which results
are Int and which Num, operator by operator, from a model that
enumerates and perl that confirms; **what to do about the history a
number carries in perl** (D23's three options; `my $x = 1e15; my $y =
$x + 1; say $x;` is the test any answer must pass or fault on). What a
Num prints as, digit for digit, including `1e+16`, `0.1 + 0.2` (perl
prints `0.3`), and whether `Inf` and `NaN` are values or faults (perl
prints `Inf`, `-Inf` and `NaN` for `9**9**9`, its negation and their
difference). `%` on a Num (perl truncates the operands: `10 % 3.7` is
1; past the range of an integer it does something else, so that
faults). Octal by a leading zero and as `0o17`; `.5`, `1.` and `1e3`;
a number with two dots refused (T62); a hex float. Traps: T35, T36,
T37, T40, T62. What
perl warns about in a literal at compile time (`1__0`, a hex literal
past 32 bits) is refused (D15). Division by zero is a fault. Hex, binary and octal
literals, `_` in a literal, a literal with a point or an exponent.
The model is Python's `float` and `fractions`, and perl agrees or the
step stops.

### 3. Strings

Referee: perl. Size: large.

Single and double quotes with their escapes and no interpolation; `.`
and `x`; `length`, `uc`, `lc`, `substr` reading, `index`; a number as a
string and a numeric string as a number. Decides: D24; exactly which
strings are numbers (perl takes `"3 "`, `" 3"`, `"1e3"`, `".5"`,
`"+3"`, `"Inf"` and `"0 but true"` in silence, and warns on `""`,
`"abc"`, `"12abc"` and `"0x10"`; the model enumerates and perl
confirms); a numeric string perl reads differently from the same
literal (T38); `use utf8` and a source that isn't ASCII; `print`. An
unescaped `$` or `@` in double quotes is refused until step 16 (T34).
Case-mapping past ASCII faults until a step brings perl's Unicode
tables, which the C library doesn't have (T45); unary minus on a
string that isn't a number faults (T47), and on a bareword is refused
(T69); `x` before a digit (T57); what `chr` gives for a surrogate or a
number past Unicode. **Decides whether a program with text past ASCII
must carry `use open ':std', ':encoding(UTF-8)';`**: the oracle runs
perl with `-CSDA`, and plain `perl` prints `é` as one byte, so as it
stands the file alone doesn't say what the language does with it. The first heap values: allocated
and never freed until step 7.

### 4. Booleans, undef, comparison, logic

Referee: perl. Size: large, for the model of comparing an Int with a
Num (T39). Traps: T33, T39.

`true`, `false`, `undef`, `defined`; the numeric and string
comparisons, `<=>` and `cmp`; `!`, `&&`, `||`, `//`, `not`, `and`, `or`,
`xor`; `?:`. Truth is perl's. Decides: what a boolean prints as and
adds as (perl: `true` is `1`, `false` is `""` as a string and 0 as a
number, in silence); undef in a comparison or a concatenation faults
(D15); chained comparisons refused (T33), and the mixes perl itself
refuses (T51). The expected grouping in a precedence test comes from
perl, `perl -MO=Deparse,-p`, which prints the brackets perl sees.

### 5. Lexical scalars, assignment, blocks, `if`

Referee: perl. Size: medium.

`my $x`, assignment and the assigning operators, `++` and `--`, blocks
and their scopes, `if`, `elsif`, `else`, `unless`, the `if` and
`unless` modifiers. The resolver arrives: a name to its declaration, a
use before `my` refused, as perl refuses it; a second `my` of a name
in one scope refused (perl warns, D15). Variables are read when their
operator runs (D14, T1). Decides: `++` and `--` on a string that
isn't a number (proposed: fault, T44); the assigning operators on
undef (perl is silent for some and warns for others: T43). In `my $x
= $x`, the right side is the outer `$x` (T58). Traps: T1, T26, T30,
T43, T44, T58.

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
list and scalar position, slurpy `%opts`, slices. D27. A hash is
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
tests of what `try` does not catch. Traps: T53, T65, T70.

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

None waiting. D1 to D32 are agreed, and steps 0 and 1 are written from
them. The next proposal is step 2's.

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
