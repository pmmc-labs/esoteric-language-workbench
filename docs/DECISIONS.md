# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. **User** means Stevan decided it; **default** means the agent
proposed it and it wasn't explicitly discussed. Defaults are fair to
revisit, and every default here is also listed under Open questions at
the end of [`DESIGN.md`](DESIGN.md), so they can be settled in a batch.

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics (the person's words quoted where they
matter), the reason, and `Rejected:` with each alternative and why it
lost. A decision that's later changed stays, with a note pointing to the
entry that changed it; the new entry says what it retires.

Sections group entries by subject, not by time. Number by time.

The evidence these lean on is in [`BACKGROUND.md`](BACKGROUND.md), with
paths into the four repositories that were read. Where an entry says
"perl prints", it was run, under perl 5.38.2, on 2026-11-24; the
language's oracle is 5.42 (D10), and step 0 reruns them there.

## Scope

**D1. A new runtime for Perl 5, for a language that is modernized and
cleaned up, and not backward compatible.** *(User: "It does not need to
be a backwards compatible, rather I want to modernize and clean up the
language, and try to fulfill the promise of Perl 6 that never
arrived.")* It is Opal's goal again (`docs/NOTES.md` in
`stevan/pp`: "capture and distill the core essence of Perl, while
removing the cruft"; "not p5++ because we're taking stuff out as well
as adding"), on a different plan. It isn't a replacement for `perl`, a
way to run CPAN, or a compatibility project.

**D2. The core rule: erase and it's Perl.** *(User: picked from three
options, 2026-11-24.)* A program the compiler accepts is, once the
language's own annotations are stripped, a program perl 5.42 accepts;
and when it runs without faulting it prints what perl prints, byte for
byte. Cleaning Perl up means refusing a program at compile time or
faulting at run time, never giving it a different meaning. So `perl` is
the independent source of every expected output (D7, D10), and a
feature perl lacks is a numbered exception with tests of its own.
D12 to D16 work the rule out. Rejected: a Perl-shaped dialect that
changes meanings where Perl's are bad (`==` and `eq` unified, `foreach`
copying, new call syntax), because every expected output would then
need a hand-written model or a second implementation, and Chalk and
perl5-son show what an implementation of Perl without a trustworthy
oracle costs; a strict subset and nothing else, because it leaves no
room for types, roles or concurrency (D5).

**D3. The compiler is TypeScript run by Node as it is, and emits C,
linked with a C runtime into a native binary.** *(User: picked from
four options, 2026-11-24.)* The workbench's main line, so steps 0 and
1 of its template are the starting shape, and gcc, clang and the
sanitizers are three more oracles. It needs a closed world (D20).
Rejected: a tree-walking interpreter on Node (the host leaks: UTF-16
strings, doubles, its `RegExp`; each leak has to be found and
overridden); a bytecode VM in C (more machinery before the first
feature works); written in the subset and bootstrapped by perl, as
Chalk is (the slowest start: Chalk runs 2 of 288 of its own test files
natively, `BACKGROUND.md`).

**D4. The language starts from Chalk's subset.** *(User: "What is nice
about Chalk in particular is that it is the subset of Perl needed to
implement Perl, which is a good subset to start with.")* The subset as
Chalk declares it, `docs/chalk-grammar-spec.md` in `stevan/chalk`:
`class`, `field`, `method`, signatures, postfix dereference, `try` and
`catch`, lexical variables, and no `package`, `bless`, string `eval`,
typeglobs, `AUTOLOAD` or indirect object syntax. [`SURFACE.md`](SURFACE.md)
is that list worked through construct by construct, with what this
language does with each. Where Chalk's live pipeline accepts more than
its declared subset (it now takes whatever perl compiles, less what its
backend refuses), the declared subset is the one meant.

**D5. Of Perl 6's promises, three are planned and one is parked:
gradual types, roles and a metaobject protocol, and concurrency are
later steps; grammars and rules are not.** *(User: picked from four,
2026-11-24; grammars and rules were offered and not picked.)* Each is
proposed when its step comes (`PLAN.md`, steps 25 to 29). Types are
erasable, so D2 holds for them as it stands. Roles and concurrency
have no perl to agree with, so each will be an exception to D2 with a
model or a referee of its own. Concurrency constrains the runtime from
the start (D28). Parked, in `BACKGROUND.md`: grammars and rules,
multiple dispatch, macros, lazy lists, junctions.

**D6. No Sea of Nodes, no Earley parser, and the compiler need not be
written in Perl or host itself.** *(User: "I am not completely sold on
the Sea Of Nodes approach, and it does not need to be written in Perl
and self-bootstrapping either." The shape is a default.)* A
hand-written lexer and a precedence parser produce a plain syntax tree
with positions; the code generator walks it. An intermediate form comes
when a step needs one, and is proposed then. Rejected: Sea of Nodes
(reads float, so order exists only where a memory edge was placed by
hand, and Perl's effects are everywhere; perl5-son's last audit found
111 silent wrong answers in 847 fresh programs, every one on a graph
its verifier passed); an ambiguous grammar filtered by semirings
(Chalk's takes 126 seconds and 609 MB for a 15 KB file, and was set
aside as the producer of its IR); self-hosting as a goal (it stays
possible, since D4's subset is the one a compiler is written in, but
nothing is bent toward it).

## Project

**D7. Golden tests' expected output comes from an independent source,
never from the compiler.** *(User; the workbench's D8, carried.)* Here
the source is perl wherever D2 says the two agree (D10), a hand
working for a fault or a refusal, and a model or a referee for an
exception to D2.

**D8. Examples bend to the language.** *(User; the workbench's D9,
carried.)* When a port needs a feature, the example changes or is left
out. This is the rule that keeps the cleanup: every port of an
existing Perl program will want something that was cut.

**D9. A commit that touches the implementation names a decision or a
plan step in its subject.** *(User; the workbench's D10, carried.)*

**D10. perl 5.42 is the independent source for every test in which the
language and perl agree, and a script holds the suite to it.**
*(Default)* A golden test is a `.pl` file that perl runs as it is. Each
has a kind, in a header comment, and `t/checks.py oracle` checks each
kind against perl:

- `same` (the default): perl compiles the file without a word
  (`perl -c`, nothing on stderr: D15), runs it with nothing on stderr,
  and its stdout and exit status are the `.expected`. It is run under
  eight hash seeds and all eight must match. And a `same` test that
  prints from `keys`, `values` or a hash in a list without `sort` is
  rejected by reading it, because seeds agree by luck on a small hash:
  two seeds give a two-key hash the same order about half the time
  (measured: 209 of 435).
- `dies`: an uncaught `die`. perl's stdout and stderr are the
  `.expected`, with `exit: 255`, and perl's own status must be 255
  (D12).
- `fault`: the `.expected` is by hand: what the program printed, then
  the fault's line, then `exit: 1`. The check requires perl to compile
  the file, runs the compiled program, and requires its stdout to be
  the start of perl's (D12), under each seed. A perl that doesn't
  finish in the time allowed fails the test: a fault test must be a
  program that ends under perl.
- `refused`: the `.expected` is the compiler's message, by hand. perl
  isn't consulted: it may run the program happily.
- `new`: an exception to D2. The decision that makes the exception
  names the model or referee the output comes from.

The perl is pinned (`LANG_PERL`, 5.42.x, with 64-bit integers and
doubles, which `make doctor` checks), and the checks fail, not skip,
without it. The compiler is given the same path perl is, from the same
directory, since a `die`'s message carries it. How `warn` is tested,
and a program more than 100 calls deep (perl warns), are for steps 15
and 8 to say; until then no test does either. Rejected: a Python
referee for the whole language (a second implementation of Perl, the
cost D2 was picked to avoid); trusting perl's output without the
stderr and seed conditions (a warning means the language should have
faulted, D15, and a seed dependence means the test proves nothing);
two seeds (the first draft; measured, above).

**D11. A census of other people's probes, run at every step, with a
ratchet.** *(Default; importing the files needs perigrin's agreement,
which is open.)* Chalk and perl5-son hold about 3,000 one-line Perl
programs written to find wrong answers, each with perl's own output,
and a graded corpus of 441 more (`BACKGROUND.md`). From step 11 they
are run as the workbench's interpreter experiment ran its probes: not
golden tests, but a judge. Each gets a verdict: **SAME** (agrees with
perl), **REFUSED** (compile error), **LOUD** (a fault, having printed
only the start of what perl prints), or **WRONG** (anything else:
ran, didn't fault, and differed; or faulted after printing something
perl doesn't). The counts are kept in a
file; WRONG must be 0, and SAME may not fall. The verdict names are
theirs, and so is the rule that a named refusal is acceptable and a
silent wrong answer never is. Rejected: making them golden tests (they
test Perl 5, not this language, and most will be refusals); waiting
until the language is large (their lesson: a suite measures itself,
and only programs nobody wrote for the implementation find its wrong
answers).

## The core rule, worked out

**D12. What agreement means: when a program ends normally, its stdout
and exit status are perl's; when it faults, its stdout up to the fault
is the start of perl's.** *(Default)* Ending normally is falling off
the end, or `exit`. The second half is the whole rule in one line: the
language may stop early and loudly, and may not say anything perl
wouldn't have said. stderr is the language's own: a fault's text and a
warning's needn't match perl's. A program that ends with an uncaught
`die` exits 255 with the message on stderr, as perl does when `$!` and
`$?` are 0; perl's choice of status from `$!` isn't followed.
Rejected: matching stderr (perl's messages are not a language, and
most of them become faults); matching the status of a `die` (it would
drag in `$!` after every system call).

**D13. Three ways to stop, and only one can be caught.** *(Default)*

- A **refusal** is a compile error: `FILE:LINE:COL: message`, and no
  binary. Everything the language cuts from Perl that can be seen in
  the source is a refusal.
- A **fault** ends the program at run time: stdout is flushed, then
  `fault: MESSAGE at FILE line N.` on stderr, exit 1. A fault is not
  an exception: `try` doesn't catch it, since a program that caught one
  and carried on would print what perl never would (D12).
- A **`die`** is Perl's, and `try`/`catch` catch it, as in perl.

Where perl itself dies (`Illegal division by zero`, a wrong number of
arguments, a method that isn't there, not a reference), the language
faults. So `try { 1 / 0 } catch ($e) { ... }` faults where perl would
run the `catch`. Rejected: perl's runtime errors as catchable
exceptions carrying perl's text (every message perl has would become
part of the language, to the byte, since a program can print `$e`);
faults catchable with their own text (breaks D12). To revisit with
concurrency (D5): a fault ending the task it happened in, not the
program, with a supervisor told, is where this wants to go.

**D14. Where perl's answer changes from run to run, the language pins
its own. Where perl's answer only looks arbitrary, the language
follows it.** *(Default)* The first kind is outside the agreement: the
order of a hash's keys (D27); a reference's address, and so what a
reference prints as, numbers as, or sorts as; the real time, an
unseeded `rand`, the process id; the text of a system error. Where
it's cheap the language refuses or faults (a reference used as a
string faults, and so does `<` or `<=>` on one), and the tests keep
away (D10).

The second kind is not unspecified, and is followed. **An operand that
is a variable or an element is read when its operator runs, not when
it is reached.** perl puts the variable itself on its stack and reads
it late, so with `my $total = 5; sub step() { $total += 100; return 1
}`, `say $total + step()` prints 106; `say f(1), $r->[0], f(0),
$r->[0]`, with `f` storing its argument in `$r->[0]`, prints `1000`;
and `$a[0] + ($a[0] = 10) + $a[0]` is 30. So the generated C never
copies a variable into a temporary: the operands that are calls or
operators are evaluated left to right into temporaries, and the
variables and elements are read at the operation. It is the cheaper
code as well. What that leaves is an expression that reads an element
and, in a later operand, removes or replaces the container that held
it; step 9 finds whether that can be a fault, and the tests keep away
until then.

`sort`'s comparator is the same kind of thing: perl makes the same
comparisons in the same order on every run, so a comparator with an
effect shows. Step 10 chooses between running the comparator with
everything frozen, so that an effect faults, and porting perl's merge,
as Chalk did. `sort` is stable, as perl's is.

Rejected: evaluating every operand to a value, left to right. That
was this entry's first draft, which called perl's late reads
unspecified on the strength of `perlop`'s note about `$i++ + $i++`. A
review refuted it with five everyday programs that change a variable
once, the first of which is above. Also rejected: perl's hash order
for a fixed seed (D27).

**D15. Where perl would warn at run time, the language faults; where
perl would warn at compile time, it refuses.** *(Default)* `"abc" +
1`, `my $u; $u + 1`, `"x: $u"`, `substr` past the end: perl warns and
carries on with a guess; the language stops. `say (1 + 2) * 3;` and
`my $x; my $x;` draw a warning before the program runs, and are
refused. This is most of the cleanup, and the warnings `use v5.42`
turns on are its list: a `same` test must leave perl's stderr empty,
compiling and running (D10), so the suite can't hold a program that
warns. The language also faults in some places where perl is silent,
because it cut what perl does there (string increment, a reference as
a string, a list-shaped return in a scalar call, reading through
undef); those are the rows marked Fault in `SURFACE.md`, and they are
a list. What perl does silently stays: `"12" + 1` is 13, `"3 " + 1` is
4, `$count{$word}++` on a missing key is 1, `$total{$k} += 5` and
`$s .= "x"` on undef don't warn and work. Exceptions, each for its
reason: the recursion warning at 100 calls deep (how deep a program may go is
step 8's to propose), and warnings about experimental features. Rejected: perl's guesses (the
cruft D1 is about); a new, stricter rule of the language's own for
what converts to what (it would have to be modelled; perl's warnings
are already the line a careful Perl programmer holds).

**D16. A program begins `use v5.42;`, and the pragmas are a closed
list.** *(Default)* That line is what makes the file mean the same
thing to perl: strict, warnings, `say`, signatures, `try`, the Unicode
string rules, and a source that is ASCII unless `use utf8` follows.
Accepted besides: `use utf8`, `use experimental 'class'` (and the other
experimental names a step brings), and `use` of a module of the
program's own (step 18). `no strict`, `no warnings`, `use integer`,
`use bytes`, `use constant` and any other pragma are refused until a
step proposes them. Rejected: implying the line (the file would then
mean something else to perl, and D2 is about the file).

## The language: what the cleanup cuts

**D17. Values flow; containers don't.** *(Default)* Perl passes and
iterates over containers, so a write can reach back through an
argument, a loop variable, `$_`, or a `map`. That is the largest class
of wrong answers in perl5-son's audits (52 of 111 in the last one)
and, for a programmer, action at a distance. Raku's answer was
read-only bindings, and it is this language's:

- `@_` is refused; a sub has a signature, and its parameters are
  copies (as perl's signatures already are).
- A `foreach` variable, `$_`, and `sort`'s `$a` and `$b` are
  read-only: any use of one in a position that can change it is
  refused. That is every assignment, `++`, `s///`, `tr///`, `chomp`,
  `chop`, `undef`, four-argument `substr`, and a place on the left of
  a list assignment; the positions come from the table of builtins
  (D29), not from this sentence. (In perl, `for my $x (@a) { $x *= 2
  }` rewrites `@a`, and so does `chop $x`.)
- While a `foreach`, `map` or `grep` runs, every array and hash whose
  elements can reach its list is frozen: storing into one or resizing
  it faults. So a copy and an alias can't be told apart. perl's
  aliases reach a list through more than an array's name: through
  `grep`, `sort`, `reverse`, a slice, `values`, a hash in a list, an
  element, a ternary and a comma list. (In perl, `for my $x (sort {
  $a <=> $b } @a) { $a[0] = 7; say $x }` shows the 7.) `keys`, a
  range, `map`'s results, `splice` and a sub's return are copies and
  freeze nothing, so `for my $k (keys %h) { $h{$k}++ }` is as in
  perl. The freeze is a count, since a sub can recurse over the same
  array, and is released on every way out, a `die` included. Freezing
  too much is only ever loud.
- A reference to a loop variable or to `$_`, and a closure that
  captures one, are refused until step 14 proposes what they mean:
  the freeze ends with the loop, and perl's alias doesn't. (In perl,
  `for my $x (@a) { push @s, sub { $x } }`, then `$a[0] = 9`, then
  `$s[0]->()` gives 9; and `push @r, \$x` lets `${ $r[0] } = 7`
  rewrite `@a`.) Copying first, `my $y = $x`, is the same in both.
- A `foreach` over a list that names a scalar variable directly,
  `for my $x ($p, $q)`, is refused until step 9 proposes what it
  means: perl aliases `$p`, and nothing can be frozen.
- No lvalue subs, no `substr`, `vec` or `pos` on the left of `=`, no
  assignment to a ternary or to an assignment, no reference to an
  element (`\$a[0]`, `\$h{k}`), no `local`.

Rejected: aliasing as perl has it (every element becomes a box with an
address, which is how perl is built and why it is hard to compile);
copying without freezing (silently differs from perl, against D2).

**D18. Context is syntax. A sub can't see how it was called, and a
list-shaped `return` reached from a scalar call faults.** *(Default)*
Whether an expression is in list, scalar or void position is read off
the source, as in perl: `my $n = @a` is the count and `my ($f) = @a`
the first. What goes is context leaking through a call. In perl a
`return` is evaluated in the caller's context, so with `sub a { my @a
= (42); return @a }`, `my $x = a()` is 1, the count, and `return (4,
5, 6)` gives 6. Here a call carries a hidden flag with perl's three
values, list, scalar and void, and:

- A `return` whose expression is **list-shaped** faults when the flag
  says scalar. List-shaped is defined on the tree: an array, a hash, a
  comma list, a slice, a range, a list assignment, a list repeated
  with `x`, any builtin the table says returns a list (`map`, `grep`,
  `sort`, `keys`, `values`, `reverse`, `splice`, and more as steps
  bring them); and a ternary, `||`, `&&`, `//`, `or`, `and`, brackets
  or a `do` block with a list-shaped arm. (`return $c ? @a : 0` gives
  3 in perl for a three-element `@a`.) Each step that brings a
  builtin says which side it is on.
- `return f()` passes the flag on.
- Under void nothing faults: `f();` is fine whatever `f` returns.
- A sub's last expression, where it ends without a `return`, is
  treated the same.
- A sub whose last statement is an `if`, `unless`, a loop or a block
  has no value here: reaching its end and having the value used
  faults. (perl returns the last thing evaluated, which is the
  condition: `sub f($x) { if ($x) { "yes" } }` gives 0 for `f(0)`.)
- A sub called as an `if`'s test is a scalar call, so `if (f())`
  faults when `f` returns an array. `my @r = f(); if (@r)` says what
  was meant.
- `wantarray` is refused.

Rejected: perl's rule (a sub with two meanings; Chalk compiles a sub
once per caller context for it); a list-shaped return giving its
single value when it has exactly one (differs from perl, which gives
the count: the case above); refusing scalar calls of such subs at
compile time (needs the types of step 25, which will then turn this
fault into a refusal).

**D19. One object system: `class`, `field`, `method`, `ADJUST`,
`:isa`, `:param`, `:reader`.** *(Default)* `package`, `bless`, `@ISA`,
`AUTOLOAD`, `DESTROY`, `can` as a way to find code, and anything that
reaches the symbol table are refused. It is what Chalk kept, the one
part of Perl it kept unmodified. Roles and the metaobject protocol
come by proposal (D5). Rejected: both object systems (two ways to do
everything, and `bless` changes what a value is after others hold it).

**D20. A closed world, in two phases.** *(Default)* The compiler sees
the whole program before any of it runs. String `eval`, `do FILE`, a
`require` at run time, `BEGIN` and the other phase blocks, source
filters and `__DATA__` are refused. Block `eval` is refused in favour
of `try`, which is what perl 5.42 has for it. Allium's triage of perl's
opcodes had already marked string `eval`, block `eval` and `do FILE`
Prohibited, and a closed world is what D3's compiler needs. Rejected: `BEGIN` as compile-time evaluation (a good
idea, Chalk's "fold only what cannot differ between build and run",
and a proposal for later, not a default).

**D21. Where perl's parser guesses, the language doesn't.** *(Default)*
The parser never needs to know what has been declared to know how to
read a line.

- A call of a sub the program defines has brackets: `f($x)`. Without
  them it is refused.
- A closed table of builtins may be written without brackets (`say
  $x`, `push @a, $x`, `return $x`, `die "..."`, `map { ... } @a`),
  each with the shape of its arguments in the table.
- The table holds every name perl gives a meaning to, keywords,
  builtins and quote operators, whether the language has it or not,
  and a program may not define a sub with one. perl would ignore the
  definition: `sub q($x) { ... }` then `q(5)` is the string `5`, and
  a program's own `say`, `print` or `defined` is never called, all in
  silence.
- A builtin's name, then brackets, then an operator is refused: in
  perl `say (1 + 2) * 3;` prints 3.
- `sort` followed by a name or a scalar is refused: in perl `sort
  dbl(3, 1, 2)` uses `dbl` as the comparator.
- `my` under a statement modifier, or in the right operand of `&&`,
  `||`, `//` or `?:`, is refused: in perl `my $x = 10 if $c;` leaves
  the last call's value in `$x` when `$c` is false.
- A named sub stands at the top of the file and names only variables
  declared there, until step 14 proposes more: perl binds a named sub
  to the first instance of a variable in a loop or an enclosing sub.
- No indirect object syntax, no prototypes, no `&f` forms, no
  barewords as strings, except before `=>` and as a hash key in
  braces.
- Where perl looks ahead to guess, a block or a hash after `map`, a
  filehandle or a value after `print`, a regex or a division after a
  word, the language takes one reading fixed by the table and refuses
  the shapes where perl's guess could be the other.

Chalk's hardest parsing came from here: list operators took two
rollbacks, and its lesson was that being a builtin is a fact about
names, not grammar. Opal had dropped bracketless calls in its last
commits for the same reason. Rejected: perl's rule that a predeclared
sub may be called without brackets (parsing would depend on the order
of declarations).

**D22. The core is small, and the rest is libraries or gone.**
*(Default)* The core: values, variables, control, subs, classes,
strings, lists, hashes, references, regexes, `say`, `print`, `die`.
Files, directories, the environment and processes are libraries with
perl's own names (`open`, `close`, `readline`), each brought by a step
that proposes it; sockets and the system databases wait for someone to
want them. Gone for good: formats, `tie`, `dbmopen`, `each` and the
iterator a hash carries, `reset`, `dump`, `lock`, one-argument
`select`, System V IPC, `study`, `$[`, and the punctuation variables
that set global behaviour (`$,`, `$\`, `$/`, `$;`, `$"`). This is
Allium's triage (248 of perl's 415 opcodes Core, 84 IO, 42 OS, 10
Processes, 24 Deprecated, 7 Prohibited) and the 2007 conversation in
Opal's `docs/HISTORY.md` ("no reason I/O shouldn't be a library that happens
to be in core"). Rejected: nothing in particular; the list is a
default and each item is cheap to argue.

## Values and memory

**D23. Numbers are Int, 64 bits signed, and Num, a double; an Int
result that doesn't fit faults; and which of the two a result is
follows perl, by a rule step 2 has to pin down against perl before it
builds.** *(Default; the last part is open in a way the others
aren't.)* The first three parts are simple, and a review checked the
Int half: Python's integers and perl agree on 6,286 edge cases of `+`,
`-`, `*`, `%` and unary minus. Where perl moves an integer past 2^63
into an unsigned or a float (`9223372036854775807 + 1` prints
`9223372036854775808`, and `5_000_000_000 * 5_000_000_000` prints
`2.5e+19`), the language faults `integer overflow`: it has no unsigned
integers and doesn't round in silence. A Num prints as perl prints it,
to 15 significant digits. `%` works on integers and takes the sign of
its right operand (`-7 % 3` is 2).

The last part is where perl's implementation shows. All of these were
run:

- perl picks integer or float arithmetic by the operands' *values*.
  A float that is a whole number below 2^53 is used as an integer:
  `1e15 + 1` is `1000000000000001`, `1e15 * 10` is
  `10000000000000000`; but `1e16 + 1` is `1e+16`. This is Chalk's
  finding. A rule by type would not agree with perl.
- Neither `/` nor `**` has a one-line rule. `7 / 2` is 3.5.
  `4000000000000000 / 2` prints `2e+15`, a float, and
  `18014398509481984 / 2` prints `9007199254740992`, an integer.
  `10 ** 15` and `7 ** 20` are exact integers; `2 ** 50` prints
  `1.12589990684262e+15`.
- An Int and a Num compare as floats: `9007199254740993 == 2 ** 53`
  is true.
- **A number remembers having been used as an integer.** `my $x =
  1e15; say $x;` prints `1e+15`. After `my $y = $x + 1;`, `say $x`
  prints `1000000000000000`. Reading the variable changed how it
  prints, and a comparison, `%`, `int`, an array index or a `sort`
  does the same.
- **So does a string.** `"1e16" + 1` is `10000000000000001`, where
  the literal `1e16 + 1` is `1e+16`; and after `$h > 0.5`, the same
  `$h = "1e16"` gives `1e+16`.

The last two are the history a value carries in perl, and the language
can't both ignore it and never be WRONG. Step 2 writes the model that
enumerates the operators over the edge values, and proposes where the
faults go. The recommendation today: a whole Num of magnitude 10^15 or
more faults when it is made a string (printed, joined, used as a hash
key), which is the only place its history shows; and a string that
isn't written as a plain integer and whose value is whole and 2^53 or
more faults when used as a number. Both are loud and narrow, and the
first makes `say 1e15` a fault. The alternative is doing as perl does,
storing the integer back into whatever was read, which is exact and is
the cruft D1 is about.

Rejected already: unsigned integers (perl's implementation, not Perl
the language); integer division for integer operands (not what perl
prints); a pure rule by value, in which a whole Num below 2^53 simply
is an Int (it would print `1e15` as `1000000000000000`; this was the
first draft of this entry, and perl refuted it); "`**` gives a float"
and "`/` gives a whole result as an integer" (the second draft; a
review refuted both); bignums (machinery; a proposal if ever).

**D24. A string is a sequence of Unicode code points, and the standard
streams are UTF-8.** *(Default)* `length`, `substr`, `ord` and `chr`
count code points. The source is ASCII, or UTF-8 with `use utf8`, as
`use v5.42` already demands. perl agrees when it's run with its
standard streams as UTF-8 (`-CSDA`), which is how the oracle runs it.
Strings are immutable in the runtime; since nothing can alias one
(D17), a program can't tell. Bytes, for binary files, are a later
proposal and a separate type. Rejected: perl's two kinds of string
with a hidden flag (the best-known cruft there is); bytes only, Chalk's
choice (`chr` above 255 stops at run time).

**D25. A value is two machine words: a tag and a payload.**
*(Default)* A 64-bit integer and a double fit in the payload unboxed;
a string, an array, a hash, code or an object is a pointer. Two words
pass in registers under both C compilers' calling conventions.
Rejected: one word with a tag in the low bits, the calculator's D4
(integers would be 63 bits and fault where perl is exact); NaN-boxing
(no room for a 64-bit integer).

**D26. Memory is collected by tracing: a precise, non-moving
mark-and-sweep, with its roots on a shadow stack the generated C
maintains.** *(Default; step 7.)* With knobs from the start, as the
workbench asks: a collection at every nth allocation, freed memory
poisoned, a heap cap. No reference counts, so no `DESTROY` and no
`weaken`, both refused: a cycle is just collected. Cleanup at the end
of a scope is `defer`'s job, when a step proposes it. Rejected:
reference counting as perl does (it buys `DESTROY` at a known moment
and costs every assignment, and cycles leak); a conservative collector
from a library (no stress knob to find a missed root, and a dependency);
no collector, Chalk's state today.

**D27. A hash keeps its keys in the order they were first stored.**
*(Default)* perl's order changes with every run, so any order agrees
with perl (D14), and insertion order is the one that makes a run
reproducible without a seed. Rejected: perl's order for a fixed seed
(perl's hash function and its bucket layout would become the
language).

**D28. The runtime has no global state: everything hangs off one
context that every runtime function and every compiled sub takes as
its first argument.** *(Default)* Concurrency is planned (D5), and the
likely shape is tasks that share nothing, each with a heap of its own
(a64-slight's shape). That is cheap if the heap, the
collector's roots and the fault path were never global, and a rewrite
if they were. Nothing else about concurrency is decided.

## Compiler

**D29. The compiler's passes: lexer, parser, resolver, checker, code
generator; one table of names.** *(Default)* Each is a file under
`compiler/src/`.

- The **lexer** reads the whole file, with a line and column on every
  token. The parser tells it whether a term or an operator may come
  next, which is what settles `/` as division or the start of a regex.
- The **parser** is recursive descent for statements and precedence
  climbing for expressions, from `perlop`'s table.
- The **resolver** binds every name to its declaration, finds what a
  closure captures, and gives every expression its context (D18).
- The **checker** makes the refusals (D17 to D22) and, later, checks
  types.
- The **code generator** writes C.
- Keywords, builtins and their argument shapes are **one table** that
  all of them read.

An error is a diagnostic with a position, never a node in the tree.
Opal's lessons, each from its code: four stages that each switched on
source text again, so a keyword changed in three places; no positions
anywhere; statements compiled one at a time, so no forward references
and no scopes at compile time; errors as tree nodes that crashed the
next stage.

**D30. A refusal is tested as a golden test of its own kind.**
*(Default; retires the workbench's D7 for this language.)* The
workbench kept compile errors in unit tests because a calculator has
few. Here the refusals are half the language's definition, so a test
of kind `refused` (D10) is a `.pl` that must not compile, with the
compiler's message as its `.expected`. Unit tests stay for what a
golden test can't reach: token positions, the tree.

**D31. The generated C is straight-line: one statement per operation,
each result in a temporary.** *(Default)* C doesn't order a call's
arguments and clang stops at 256 nested brackets; the workbench met
both (its D25 and D26, and the limit that's still open there) and
called this shape "also right". Starting with it costs nothing here.
