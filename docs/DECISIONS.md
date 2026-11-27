# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. **User** means Stevan decided it; **default** means the agent
proposed it and it wasn't explicitly discussed, and is fair to revisit.
D1 to D80 are all Stevan's: D1 to D9 from the first conversation, and
D10 to D32 on 2026-11-24, each either picked from options laid out for
it or accepted as the agent proposed it, which the attribution says.
D33 and D34 were defaults taken at steps 0 and 1, which he confirmed;
D35 to D38 are his answers to step 2's proposal, D39 to D45 to step
3's, D46 to what the review of step 3 left open, D47 to D51 to step
4's, and D52 to D56 to step 5's. D57 was a default the builder of
step 5 took, which he confirmed the same day. D58 to D62 are his
answers to step 6's proposal, D63 to D66 to step 7's, and D67 to D72
to step 8's (D68's number is the builder's default, which he said
to stay with). D73 and D74 were the builder's defaults, from the
review of step 8 and from building it, which he confirmed; D75 is
his, on seeing the build. D76 to D80 are his answers to step 9's
proposal, as its review had amended it. D91 to D94 are his answers
to step 11a's; D95 was the builder's defaults there, which he
confirmed. D96 and D97 are his, on the census; D98 to D101 his answers to
step 12's, D103 his, on the file of differences, D105 his answer on subs with no signature, and D102 the builder's defaults on its review, which he
confirmed. D104 was the builder's defaults from building step 12a,
which he confirmed.
What a decision leaves for a step to settle is listed under Open
questions at the end of [`DESIGN.md`](DESIGN.md).

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics (the person's words quoted where they
matter), the reason, and `Rejected:` with each alternative and why it
lost. A decision that's later changed stays, with a note pointing to the
entry that changed it; the new entry says what it retires.

Sections group entries by subject, not by time. Number by time.

The evidence these lean on is in [`BACKGROUND.md`](BACKGROUND.md), with
paths into the four repositories that were read. Where an entry says
"perl prints", it was run, under perl 5.38.2, on 2026-11-24; the
language's oracle is 5.42 (D10), and step 0 reran every one there
(`briefs/claims.py`): all of them hold under 5.42.0.

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

**D32. The language is Curly.** *(User: picked, 2026-11-24.)* From
Opal's notes: "The name `curly` is the natural successor to `moe` and
Perl is known for having a lot of curly braces `{{{}}}` so it kinda
works." The driver is `curlyc`, and the oracle's variable
`CURLY_PERL`. A program is a `.pl` file, since it is Perl (D2); what a
file that carries type annotations is called waits for step 25.
Rejected: Opal (the 2025 attempt's name; this is a different design);
no name yet.

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
*(User: accepted as proposed, 2026-11-24.)* A golden test is a `.pl` file that perl runs as it is. Each
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

The perl is pinned (`CURLY_PERL`, 5.42.x, with 64-bit integers and
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
ratchet.** *(User, 2026-11-24: "Use them, perigrin already said it
was okay.")* Chalk and perl5-son hold about 3,000 one-line Perl
programs written to find wrong answers, each with perl's own output,
and a graded corpus of 441 more (`BACKGROUND.md`); perigrin has agreed
to their use. From step 11 they are copied into `t/census/` and run as the workbench's interpreter experiment ran its probes: not
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

**D103. `DIFFERENCES.md` is kept: where the language and perl differ,
by how Perlish what is lost is, how likely it is to be met, and
where; and `make test` holds it.** *(User, 2026-11-26: "lets start
writing a document to specifically list the parts where curly and
perl differ", and then "Let's add the differences file to the process
and organize it by perlish ness and likeliness to be hit and in what
context." The ratings, their three scales and the check are the
builder's defaults, and his to move.)* The log says why each thing
was cut and `SURFACE.md` what is done with each construct; neither
says what a Perl programmer will feel, or how the hundred small
refusals add up, which is the question of how Perlish the language
is. A row is what perl does, what the language does, and three
ratings: **Feel** (an idiom, a habit, an accident), **Met** (often,
sometimes, rarely) and **Where** (loops, subs, printing and nine
more); † marks a row where the language is stricter than it has to
be. `t/checks.py differences`, part of `make test`: every program in
the file is run under perl and under the compiler and does what its
row says; every rated row has ratings from the lists, a decision that
exists, and stands in the section its ratings belong to; and **every
decision in the log is cited in the file or listed there as saying
nothing to a Perl programmer**, so a step that adds a decision says
which before its tests pass. A step that takes a construct in, or
cuts one, moves its rows. The ratings are a judgement and nothing
checks them: the census's counts of what its probes are refused for
are the only evidence for Met, and lean toward old Perl. It decides
nothing: where it and an entry here disagree, the entry is right.
Rejected: a list by decision, the first draft (it reads as a
catalogue of edge cases and hides the four or five rows that change
how the language feels); the document with no check (the first draft
again: it would be wrong within a step).

## The core rule, worked out

**D12. What agreement means: when a program ends normally, its stdout
and exit status are perl's; when it faults, its stdout up to the fault
is the start of perl's.** *(User: accepted as proposed, 2026-11-24.
D46 says what it promises of a perl that runs out of memory as it
compiles: nothing.)* Ending normally is falling off
the end, or `exit`. The second half is the whole rule in one line: the
language may stop early and loudly, and may not say anything perl
wouldn't have said. stderr is the language's own: a fault's text and a
warning's needn't match perl's. A program that ends with an uncaught
`die` exits 255 with the message on stderr, as perl does when `$!` and
`$?` are 0; perl's choice of status from `$!` isn't followed.
Rejected: matching stderr (perl's messages are not a language, and
most of them become faults); matching the status of a `die` (it would
drag in `$!` after every system call).

**D46. perl running out of memory as it compiles is outside what D12
promises.** *(User: picked from two options, 2026-11-25; found by the
review of step 3, T102.)* perl works a constant expression out as it
compiles, so `say "before"; say "b" x 999999999999999;` prints nothing
under perl: it stops for lack of memory before the program starts
(`panic: fold_constants`). The language prints `before` and then
faults, `repeated string too long`, which is not the beginning of what
perl printed. D12 stands as it reads for a perl that has the memory
for what the program asks; what a perl without it does, and when, is
the machine's and not the language's. Only a constant count is
affected (until step 5 they all are), and no test asks perl for a
long string. Rejected: having the compiler work constant counts out
and refuse the program (D12 exact, at the price of a constant folder
the language doesn't otherwise need, which would have to agree with
perl's about what a constant is).

**D13. Three ways to stop, and only one can be caught.** *(User: picked from three options, 2026-11-24.)*

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
catchable with a value that faults when printed (sound, and no
catalogue of messages, but a kind of value perl doesn't have); faults
catchable with their own text (breaks D12). To revisit with
concurrency (D5): a fault ending the task it happened in, not the
program, with a supervisor told, is where this wants to go.

**D14. Where perl's answer changes from run to run, the language pins
its own. Where perl's answer only looks arbitrary, the language
follows it.** *(User: accepted as proposed, 2026-11-24.)* The first kind is outside the
agreement: the
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
perl would warn at compile time, it refuses.** *(User: picked from three options, 2026-11-24.)* `"abc" +
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
reason: the recursion warning at 100 calls deep (D67: nothing
happens there, and `no warnings 'recursion';` keeps perl quiet), and
warnings about experimental features. Rejected: perl's guesses, with a warning (the
cruft D1 is about, and every guess would then have to be implemented
exactly); undef as an empty string in silence, with only the numeric
guesses faulting (friendlier to code that prints, but two rules, and
tests that have to tolerate perl's warning); a new, stricter rule of
the language's own for what converts to what (it would have to be
modelled; perl's warnings are already the line a careful Perl
programmer holds).

**D16. A program begins `use v5.42;`, and the pragmas are a closed
list.** *(User: accepted as proposed, 2026-11-24.)* That line is what makes the file
mean the same
thing to perl: strict, warnings, `say`, signatures, `try`, the Unicode
string rules, and a source that is ASCII unless `use utf8` follows.
Accepted besides: `use utf8`, `no warnings 'recursion'` (D67), `use experimental 'class'` (and the other
experimental names a step brings), and `use` of a module of the
program's own (step 18). `no strict`, `no warnings`, `use integer`,
`use bytes`, `use constant` and any other pragma are refused until a
step proposes them. Rejected: implying the line (the file would then
mean something else to perl, and D2 is about the file).

**D33. A line that starts `#!` is refused, the first line or any
other.** *(User: confirmed 2026-11-24; taken as a default at step 0.)* perl takes switches from
such a line, after any blanks, when it is line 1: under
`#!/usr/bin/perl -n`, `use v5.42; say 42;` prints nothing when stdin
is empty and `42` once for each line when it isn't; and a `#!` line
without the word `perl` in it names a program perl runs in its own
place (T72). A compiler that took the line for the comment it looks
like would print `42`: a WRONG, at step 0, which is why this couldn't
wait to be proposed. And line 1 is whichever line perl is calling 1: a
`# line 1` comment makes the next line that (and so, the review that
found this reports, does a file of 2^32 lines, perl's counter being 32
bits), so the refusal can't stop at the first line. (The first build
did stop there.) After code on its
line, `say 1; #!x`, it is a comment to perl and is one here. Rejected: reading the switches (`-n` loops over
stdin and `-l` makes `print` end its line: each switch is another
language, and the cruft D1 is about); allowing the line when it holds no switch
(`#!/usr/bin/perl`, or `#!/usr/bin/env perl`, which is how a script is
made runnable; it needs perl's own rule for what counts as a switch
and as the word `perl`, and a compiled program isn't run that way);
refusing `# line` comments and leaving `#!` alone after the first line
(it doesn't cover the long file, and what a line directive means is
step 15's to propose, T74).
Fair to revisit: allowing a first line with no switch is small if
it's wanted.

**D34. A fault names the line its statement starts on.** *(User:
confirmed 2026-11-24; taken as a default at step 1.)* `fault: MESSAGE at FILE line N.` needs an N,
and D13 doesn't say which. The statement's first line is where perl
points for the same mistake (`say 2`, `+ 5 % 0`, `+ 3;` over three
lines dies `Illegal modulus zero` at the line of the `say`), and it is
one store before each statement in the generated C. A fault's text is
the language's own (D12), so nothing depends on agreeing with perl
here; step 15 has to agree with it for `die`, byte for byte, and will
say then whether the two can share the rule. Rejected: the line of the
operator that faulted (more exact in a long statement, and a store
before every operation instead of every statement; cheap to change to
if it's wanted).

## The language: what the cleanup cuts

**D17. Values flow; containers don't.** *(User: picked from three options, 2026-11-24.)* Perl passes and
iterates over containers, so a write can reach back through an
argument, a loop variable, `$_`, or a `map`. That is the largest class
of wrong answers in perl5-son's audits (52 of 111 in the last one)
and, for a programmer, action at a distance. Raku's answer was
read-only bindings, and it is this language's:

- `@_` is refused; a sub has a signature, and its parameters are
  copies (as perl's signatures already are). *(D105: or it has no
  signature, and then takes any arguments and sees none.)*
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
writes through the variable of a `foreach` over one named array,
compiled as a loop over indexes (it keeps the commonest idiom, `$x *=
2 for` an array, and is a special case to explain: `@a = map { $_ * 2
} @a` says it without one); copying without freezing (silently differs
from perl, against D2).

**D18. Context is syntax. A sub can't see how it was called, and a
list-shaped `return` reached from a scalar call faults.** *(User: picked from three options, 2026-11-24.)*
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
once per caller context for it); agreeing where perl's answer is a
count or a last element and faulting only on the strange ones (more of
Perl kept, and every list builtin then needs its scalar meaning built
and tested, to carry something types will forbid); a list-shaped
return giving its
single value when it has exactly one (differs from perl, which gives
the count: the case above); refusing scalar calls of such subs at
compile time (needs the types of step 25, which will then turn this
fault into a refusal).

**D19. One object system, `class`, `field`, `method`, `ADJUST`,
`:isa`, `:param`, `:reader`; and `package`, only as a namespace for
subs.** *(User: picked from three options, 2026-11-24; the agent had
recommended `class` alone.)* A file may say `package Name;` to name
the subs it defines, which is how most Perl is written and is what
`use Name;` then loads (step 18). That is all a package is: no
`bless`, no `@ISA`, no `our` and no package variables, no `AUTOLOAD`,
no `DESTROY`, no `can` as a way to find code, and nothing that reaches
the symbol table. A sub in another package is called by its full name,
`Name::f($x)`, until step 18 proposes imports. Objects are `class`'s
alone, which is what Chalk kept, the one part of Perl it kept
unmodified. Roles and the metaobject protocol come by proposal (D5).
Rejected: `class` alone (it leaves the question of how a file of plain
subs is named to step 18, and the answers there were a class of subs,
as Chalk writes them, or this); both object systems (two ways to do
everything, and `bless` changes what a value is after others hold
it).

**D20. A closed world, in two phases.** *(User: accepted as proposed, 2026-11-24.)* The compiler sees
the whole program before any of it runs. String `eval`, `do FILE`, a
`require` at run time, `BEGIN` and the other phase blocks, source
filters and `__DATA__` are refused. Block `eval` is refused in favour
of `try`, which is what perl 5.42 has for it. Allium's triage of perl's
opcodes had already marked string `eval`, block `eval` and `do FILE`
Prohibited, and a closed world is what D3's compiler needs. Rejected: `BEGIN` as compile-time evaluation (a good
idea, Chalk's "fold only what cannot differ between build and run",
and a proposal for later, not a default).

**D21. Where perl's parser guesses, the language doesn't.** *(User: picked from three options, 2026-11-24.)*
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
of declarations); brackets on the builtins too, `say($x)` and
`push(@a, $x)` (it removes list-operator parsing and its traps
outright, and no longer reads as Perl).

**D22. The core is small, and the rest is libraries or gone.**
*(User: accepted as proposed, 2026-11-24.)* The core: values, variables, control, subs, classes,
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
builds.** *(User: picked from three options, 2026-11-24: fault where a
number's history would show. Step 2 confirms the exact line with a
model before building.)* The first three parts are simple, and a review checked the
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
enumerates the operators over the edge values, and confirms where the
faults go. Decided: a whole Num of magnitude 10^15 or more faults when
it is made a string (printed, joined, used as a hash key), which is
the only place its history shows (**step 2 measured it: D36 draws the
line at 10^15 up to 2^53, and D35 is the rule for which results are
Int and which Num**); and a string that isn't written as
a plain integer and whose value is whole and 2^53 or more faults when
used as a number. Both are loud and narrow, and the first makes `say
1e15` a fault. Rejected: doing as perl does, storing the integer back
into whatever was read (exact, and the cruft D1 is about: reading a
variable would change it).

Rejected already: unsigned integers (perl's implementation, not Perl
the language); integer division for integer operands (not what perl
prints); a pure rule by value, in which a whole Num below 2^53 simply
is an Int (it would print `1e15` as `1000000000000000`; this was the
first draft of this entry, and perl refuted it); "`**` gives a float"
and "`/` gives a whole result as an integer" (the second draft; a
review refuted both); bignums (machinery; a proposal if ever).

**D35. An operation is done on whole numbers when both operands are
integral, and on doubles otherwise; an operand is integral when it is
an Int, or a Num that is whole and below 2^53.** *(User: accepted as
proposed, 2026-11-24; step 2, Q2. It finishes D23. **Amended by D45**:
in `+`, `-` and `*`, an Int of 2^53 or more that is exactly a double
faults beside a whole Num or a string.)* This is perl's
own rule, from its source (`SvIV_please` and the operators in `pp.c`)
and then run: `docs/briefs/step2-perl-numbers.py` has it written out
and agreeing with perl on 129,801 operations. Operator by operator:

- `+` and `-`: both integral, the exact answer, an Int, or `integer
  overflow`. Otherwise the doubles added, a Num.
- `*`: both integral, the exact answer, an Int if it fits. If it
  doesn't: two Ints overflow (D23); so does an answer from 2^63 to
  2^64 - 1, which perl keeps as an unsigned integer the language
  doesn't have (`1e10 * 1e9`); beyond that the doubles are multiplied
  and the answer is a Num (`1e10 * 1e10` is `1e+20`). Otherwise the
  doubles multiplied, a Num.
- `/`: the doubles divided, a Num, so `6 / 2` is the Num 3; except
  that an Int past 2^53 which the right operand divides exactly gives
  the exact Int. By zero: `division by zero`.
- `**`: both integral and the power 0 or more: a base of 0, 1, -1 or
  plus or minus a power of two gives a Num, exact; any other base
  gives the exact Int when the bits in the base times the power are
  at most 64 (or `integer overflow`); otherwise, and in every other
  case, C's `pow`, a Num.
- `%`: each operand cut to its whole part, which must be an Int
  (`modulus of a number outside the integers` if not), then as step
  1. `10 % 3.7` is 1.
- Unary `-`: an Int negated, or `integer overflow` for -2^63; a Num
  with its sign changed.

For `+` and `-` this is a little stricter than perl, which gives a
float when a whole Num carries an Int past -2^63; the case needs an
Int within 2^53 of an end, and one sentence covers it. Rejected:
faulting whenever whole-number arithmetic leaves the Ints, Num or not
(one sentence instead of three, and `1e10 * 1e10` and `1.5e10 * 1e10`
fault, both being whole: float programs would trip on it); a rule by
type, in which an Int and a Num always make a Num (D23 turned it
down: it prints `1e15 + 1` as perl doesn't, so it would have to fault
on every whole answer of 10^15 or more).

**D36. A whole Num from 10^15 up to, not including, 2^53 faults when
it is made a string.** *(User: accepted as proposed, 2026-11-24; step
2, Q1. It replaces the line D23 drew at "10^15 or more".)* perl marks
a value that has been used as an integer, and
`docs/briefs/step2-history.pl` looked for where the mark shows: 41
values, 17 earlier uses, 31 later looks. Two places. A whole Num in
this range prints as `1e+15` before and `1000000000000000` after, and
so do its negation and its decrement. And the negation of a Num zero
is a negative zero before and an integer zero after, which `atan2`,
`sprintf("%g")` and a negative power can tell apart (T79: steps 16
and 22 fault there). Below 10^15 the two ways of printing are the
same digits; at 2^53 and beyond perl never takes a Num for an
integer, so `say 1e16` and `say 2 ** 62` print one way always, and
print. The language's values carry no mark, so in the range it stops:
`fault: a whole float this size prints two ways in perl (add 0 to
print the integer)`. `+ 0` makes the Int, in perl and here. So `say
1e15;`, `say 2 ** 50;` and `say 4000000000000000 / 2;` fault. Rejected:
D23's own line, 10^15 or more (one bound to remember, and `say 1e16`
faults for nothing).

**D37. A Num is finite.** *(User: picked from three options,
2026-11-24; step 2, Q3.)* A result that would be an infinity faults
`float overflow`, and one that would be a NaN faults `not a number`;
a float literal too large for a double is refused. It is what the
Ints do at their ends (D23), and it keeps a family of perl's oddest
answers out of every later step: `NaN <=> 1` is undef, `-7 %
(9**9**9)` is `Inf`, the strings `"inf"`, `"nan"` and `"Infinity"`
are numbers, and a negative zero shows through `0 ** -1`. The cost is
`my $min = 9**9**9;`, the idiom for "larger than anything", which now
stops, loudly. (perl 5.40's own `inf` and `nan` builtins are
experimental and warn.) Rejected: both as values, as perl has them
(every later step then owes perl's answer for each); infinity a value
and NaN a fault (keeps the idiom, and needs `0 ** -1` to fault as a
division and `%` to refuse an infinity).

**D38. Numeric literals: perl's, less two.** *(User: accepted as
proposed, 2026-11-24; step 2, Q4.)* In: decimal integers; `1.5`, `.5`,
`1e3`, `1.5e-3`, `1E3`, each a Num, read to the nearest double; hex,
binary and octal as `0x1F`, `0b101`, `0o17`, in either case, up to 32
bits (past that perl warns `non-portable`, and D15 refuses); an
underscore between two digits (`1_000`, `0xff_ff`). **Cut: octal by a
leading zero** (`017`; `010` is 8, the trap T24 was written about, and
`0o17` says it plainly), so a leading zero stays the refusal it has
been since step 0. **Cut: `1.`**, a point with nothing after it
(nobody writes it on purpose, and from step 3 a dot after a number is
concatenation: T78). Refused with nothing to choose: a hex float
(`0x1p3`, Later in `SURFACE.md`); a number hard against a dot, a
letter or another number (T62, T78); a digits-only literal past 2^63
- 1, which perl makes an unsigned integer and then a float in silence
(T81); an underscore anywhere else (T82). Rejected: all of perl's
forms (two more ways to be surprised, and nothing gained).

**D39. A program that prints a character past ASCII says `use open
':std', ':encoding(UTF-8)';`, and the oracle runs perl plain.**
*(User: accepted as recommended, 2026-11-24; step 3, Q1. It replaces
the `-CSDA` of D10 and D24.)* D24 made the streams UTF-8 and had the
oracle run perl with `-CSDA` to make perl agree, but then the file
alone didn't say what perl prints: plain `perl FILE` prints `é` as the
one byte E9, and `☺` as UTF-8 with a `Wide character` warning. So the
line joins the closed list of pragmas (D16), at the top, in that one
spelling (either kind of quote); with it plain perl prints UTF-8, and
so does the language. Without it, printing a character past ASCII is
a fault, `a character past ASCII printed without 'use open'`. A
program that prints only ASCII needs nothing, and a program may build
and measure any string without it. The oracle runs `perl FILE` with no
switches, which is D2 as written. (It is also the line Stevan's own
style asks for.) Rejected: nothing in the file, and a footnote on D2
("with perl's streams as UTF-8"); the line required in every program
(no fault to explain, and three lines of preamble on `say 42;`).
Other spellings perl takes, `use open qw(:std :encoding(UTF-8))` and
`':utf8'`, are refused: each is another thing to read, and `:utf8` is
perl's lax encoding.

**D40. A string is a number when it is written as one of the shapes
perl takes in silence, and which number it is turns on how it is
written.** *(User: accepted as recommended, 2026-11-24; step 3, Q2.
It finishes D23's "a string that looks like a float".)* The shapes:
blanks (space, tab, newline, carriage return, form feed, vertical
tab), a sign or none, digits with a point among them or not, an
exponent or none, blanks; so `"12\n"`, a line just read, is 12.
Anything else is `fault: not a numeric string`: perl warns on `""`,
`"abc"`, `"12abc"`, `"0x10"` and `"1_000"` (D15), and takes `"Inf"`,
`"NaN"` and `"0 but true"` in silence, which fault here all the same
(D37 for the first two; the third is one special case of perl's, for
`ioctl`). Then:

- **Digits only** (`"12"`, `" -12 "`, `"012"`, which is 12): the Int,
  or `integer overflow`: past the Ints perl goes on as an unsigned
  integer and then a float.
- **With an exponent** (`"1e3"`): the nearest double (or `float
  overflow`). Whole and below 2^53, the Int: perl gets there by either
  route. Whole and 2^53 or more (`"1e16"`), a fault: perl has the
  integer or the float, and `"1e16" + 1` prints `10000000000000001` or
  `1e+16` (T38). Otherwise the Num.
- **With a point and no exponent** (`"1.5"`, `"3.0"`, `"5."`): the
  Num. When it is whole and below 2^53, `"3.0"`, it is **soft**: perl
  adds it as a float until the string has been used as a float, and as
  an integer after (T83). So beside an integral operand, `+ - * / **`
  are float arithmetic, which is perl's answer for a string with no
  past, and fault when whole-number arithmetic would have given
  another: when either whole number, or the exact answer of `+ - *` or
  of `**` to a power of 0 or more, is 2^53 or more. `"3.0" + 1` is 4,
  `"10.00" * 3` is 30, and `"3.0" + 9007199254740990` faults.
- **A minus before a string**: the string must be a number, and the
  answer is the Num. It faults for a whole number of 2^53 or more
  (perl negates digits as an integer or as a float, by the string's
  past), and for a string whose first character is `+`, which perl
  negates as text: `-"+0"` is the string `-0` (T85). `-"foo"`, perl's
  `-foo` (T47), faults as not a number. A plus before a string is the
  string.

- **Where a whole number is wanted** (a count, a position, `chr`'s
  argument), a string with a point whose digits before the point are
  not its number cut toward zero is a fault: `"1.99999999999999999"`
  is the double 2, and perl takes the 1 or the 2 by the string's past
  (T103, found by the review of this step).

`docs/briefs/step3-strings-as-numbers.py` holds the rule to perl under
every past of every operand, 41,594 operations of which perl has more
than one answer for 9,596: the rule never gives a value perl doesn't.
The review's own search, 82 million cases, found the one hole above
and no other.
A value has no past here, which is the point. Rejected: a string with
a point or an exponent that is whole is not a number at all (one
sentence, and a price list read from a file stops at `"10.00"`).

**D41. `length`, `uc`, `lc`, `ord` and `chr` are perl's named unary
operators, with brackets or without; `substr` and `index` take
brackets.** *(User: accepted as recommended, 2026-11-24; step 3, Q3.)*
Without brackets a named unary operator's argument is everything that
binds tighter than its row of perlop's table: arithmetic and the dot,
so `length "abc" . "de"` is 5, and `length "abc" + 1` is
`length("abc" + 1)`, a fault (T87). With brackets, hard against the
name or after a blank, they are the whole argument: `length ("ab") .
"c"` is `2c`. `substr` and `index` take two or three arguments, in
brackets always: perl allows `substr $s, 0, 1`, the list-operator
parsing D21 is wary of, for a spelling nobody uses. Their edges are
perl's, enumerated by the model: `substr` with a start past the end
faults `substr outside of string`, and so does a piece that starts
and ends before the beginning (perl warns of both, and gives undef);
any other piece is moved in to what the string has. `index` moves its
position into the string. `uc` and `lc` change the ASCII letters and
fault on a character past ASCII, until a step brings perl's tables
(T45). **Found building it**: perl warns that `length - 5` and
`length-5` are ambiguous (it reads them as `length(-5)`), so after a
named unary operator a sign must be on the name's line, with a blank
before it and none after, `length -5`, or in brackets; refused
otherwise. And where a whole
number is wanted, a count or a position, the number is cut toward
zero and must then be an Int: perl's own cut of a float past the Ints
is whatever the machine gives, `substr("abc", 0, 1e30)` being `ab`.
Rejected: brackets required on all seven (it no longer reads as
Perl); `substr` and `index` without brackets as perl has them.

**D42. A character is a Unicode scalar value.** *(User: accepted as
recommended, 2026-11-24; step 3, Q4.)* 0 to U+10FFFF, less the
surrogates. perl's strings hold any number as a "character", a
surrogate or anything below 2^63, built in silence and warned of when
printed (T88). Here `chr` of anything else faults `not a character`,
and such an escape in a literal is refused. A number below zero
faults too, before it is cut, so `chr(-0.5)` does: perl warns and
gives U+FFFD. The 66 noncharacters (U+FFFE and its kin) are
characters, and printing one is a fault, `a noncharacter printed`,
because perl warns there (D15). Rejected: anything in a string, as
perl, and the fault only at printing (every later step would owe
perl's answer for a string no encoding can hold).

**D43. The escapes of a double-quoted string: perl's, less what it
warns about and what needs interpolation.** *(User: accepted as
recommended, 2026-11-24; step 3, Q5.)* In: `\n \t \r \f \b \a \e`;
`\\ \" \$ \@`; `\x41` (two hex digits) and `\x{263A}`; octal, one to
three digits, `\0 \12 \101`, and `\o{101}`; `\N{U+263A}`; and a
backslash before any other punctuation mark or a space, which is that
mark. An unescaped `$` or `@` is refused until interpolation (step
16, T34). In single quotes a backslash is itself, except before a
backslash or the quote. A string may run over lines. Refused: a
backslash before any other letter or digit (`\q`, `\8`: perl warns);
`\x` with no digits and `\x{}` (perl gives a NUL, in silence: T86);
`\c`; `\N{name}`, which needs every character's name; `\U \L \u \l
\Q \E \F`, which belong with interpolation; anything but digits
between the braces (perl takes blanks and underscores there).
**Found building it**, each a refusal where the proposal had said In:
`\x` with one hex digit (perl warns `Non-hex character terminates \x
early` unless the string ends there, so it is two digits or braces);
an octal escape of fewer than three digits followed by `8` or `9`
(perl warns likewise); and a backslash before a tab or the end of a
line, which perl takes in silence and nobody means.

**D44. The small things of strings: `x` is a word of its own; a dot
after a value joins; `print`.** *(User: accepted as recommended,
2026-11-24; step 3, Q6.)* `"ab" x 3`: perl takes `"ab" x3` too, and
stops at `$s x3`, where `x3` is a word to it (T57), so `x` hard
against a digit is refused; `x=` is the assignment and refused as
that. The count is cut to a whole number; a count below zero, before
it is cut, faults `negative repeat count` (perl warns, of `-0.5`
too), and a repeated string may not pass 2^31 - 1 characters
(`repeated string too long`: perl would build it if the machine
could). **`(...) x N` as the whole argument of `say` or `print` is
refused**, through brackets and unary plus: there perl repeats a list,
not a string, which prints the same and costs it a value each, so a
count the string would bear stops perl for lack of memory (T101,
found by the review). Lists are step 9's to bring. After a value a dot is the operator whatever follows it, as
in perl: `1 .5` is `15` and `"a".5` is `a5` (T90); hard against a
number it stays refused (D38). `print` is `say` without the newline:
one argument, a statement, and the rules `say` has for brackets (T25,
T76). T76's rule is now perl's own, by the text of the line: after
`say`, one space and a bracket, the brackets must close on that line
counted as characters, one in a string too, with `;` after them
(T100, found by the review). The lexer knows whether a value or an operator comes next from
the token before; D29 had the parser tell it, and will again when `/`
can begin a pattern.

**D45. In `+`, `-` and `*`, a whole number of 2^53 or more that a
double holds exactly faults unless the other operand is an Int.**
*(User: accepted as recommended, 2026-11-24; step 3, Q7. It amends
D35.)* D35 has two integral operands added, subtracted and multiplied
as whole numbers. perl has a shortcut in front of that rule: when
both operands carry a float it works in floats, and an Int that has
been used as a float carries one from then on, if a double holds it
exactly. `my $x = 10000000000000000; say $x + 1.0;` prints
`10000000000000001`, and `1e+16` once `$x` has been divided (T92).
The review of step 2 found it, where step 2's own search of pasts had
missed it. The two answers always print differently, so the only
sound rule is a fault, `an integer this large with a whole float or a
string has two answers in perl`, when one operand is such a number
(10^16, 2^60, a nanosecond clock that happens to be even enough) and
the other is integral and not an Int: a whole Num, or a string. With
another Int perl works on integers whatever came before, and nothing
changes; with a Num that isn't whole it works on floats whatever came
before. A number of that size that a double doesn't hold exactly
(2^53 + 1, 2^63 - 1) is untouched. Rejected: leaving D35 until step 5
brings variables (the rule would then change under programs already
written against it).

**D47. A boolean is a kind of its own, and as a number or a string it
is what perl makes of it, in silence.** *(User: accepted as
recommended, 2026-11-25; step 4, Q1.)* `true` and `false` are values,
and so is what a comparison, `!`, `not`, `xor` and `defined` give. As
a number a boolean is the Int 1 or 0; as a string, `"1"` or the empty
string; `say 1 == 2;` prints an empty line. It is not the empty
string: `"" == 0` is a fault (perl warns) and `false == 0` is true.
D15 has it that what perl does in silence stays, and `$count += $x >
3` is ordinary Perl. `docs/briefs/step4-comparisons.py` holds "the Int
1 or 0" to perl in arithmetic beside every other operand under every
past: 2,400 operations, no value perl doesn't give, so a boolean needs
none of D45's care. Rejected: a boolean that is only for testing, and
faults as a number or a string (a typed language's rule; `say $a ==
$b` stops).

**D48. `undef` is written bare only where perl can't take what follows
for its argument; an undef where a number or a string is wanted
faults.** *(User: accepted as recommended, 2026-11-25; step 4, Q2.)*
To perl `undef` is an operator with an argument, the thing to make
undefined, and it takes what follows for one whenever it can: `undef *
2` is undef of a glob called `2`, in silence, and `undef + 1`, `undef
< 1` and `undef x 3` don't compile (T105). So bare `undef` may be
followed by `)`, `,`, `;`, `?`, `:` or a logical operator (`//`, `||`,
`&&`, `and`, `or`, `xor`), and by nothing else; before anything else
it is refused, with a message that says to write `(undef)`.
`undef(...)` is the operator on a variable, cut already. An undef
where a number or a string is wanted is a fault (D15: perl warns),
`say undef` included: `undef where a number is wanted`, `undef where a
string is wanted`. What takes an undef: `defined`, the tests of truth
(`!`, `not`, `&&`, `||`, `and`, `or`, `xor`, `? :`), `//`, and
`length`, which gives undef for one, as perl does. Rejected: always in
brackets (one rule, and `$x // undef` needs brackets perl doesn't ask
for).

**D49. The comparisons, truth, and what the logical operators give are
perl's.** *(User: accepted, 2026-11-25; step 4, Q3 and what the
proposal had with nothing to choose.)* `== != < <= > >=` and `<=>`
make both operands numbers (D40) and ask D35's one question: both
integral, the whole numbers are compared exactly; otherwise the
doubles are, so `9007199254740993 == 2 ** 53` is true (T39). `<=>` is
the Int -1, 0 or 1. `step4-comparisons.py` asked perl for 57,376
comparisons under 25 pairs of pasts each: where the rule doesn't fault
for D40's reasons, perl has one answer and it is the rule's. (perl
marks a number as carrying a float only when the float is exactly the
number.) `eq ne lt le gt ge` and `cmp` make both operands strings, a
number being what `say` prints for it, and compare them character by
character, with no locale: `10 lt 9` is true, and `0.1 + 0.2 eq 0.3`
is true where `==` is false. False is undef, `false`, a number that is
zero, the empty string and the string `"0"`; `"0.0"` and `"00"` are
true. `!`, `not` and `xor` give booleans. **`&&`, `||`, `//`, `and`
and `or` give one of their operands**, not a boolean (`2 || 3` is 2,
`0 && 1` is 0), and don't work the right one out unless it is needed;
`? :` works out one branch. Later (not in the language): `^^`, `~~`,
the bit operators.

**D50. Two comparisons of one row with no brackets between them are
refused.** *(User: accepted as recommended, 2026-11-25; step 4, Q4.)*
Since 5.32 perl chains them: `1 < 5 < 3` is `1 < 5 && 5 < 3`, and `1
!= 1 == 0` is `(1 != 1) && (1 == 0)`, false, where reading from the
left gives true (T108); `<=>` and `cmp` don't chain and don't compile
in one (T51). `1 < 2 == 1` is two rows and is fine. **And an
unbracketed `!` on the left of a comparison is refused**, `!$x ==
$y`: it is `(!$x) == $y`, and perl 5.42 warns of a precedence problem
as it compiles, unless it has folded the `!` away (T115, found by the
review of this step). Rejected for now:
chaining as perl does (it reads well, `0 <= $i < $n`, and needs the
rule that the middle operand is worked out once); a later step can
take it without breaking a program this accepts.

**D51. The word operators: none after `say`'s argument, none bare in a
list of arguments, and nothing that binds tighter after `not (...)`.**
*(User: accepted as recommended, 2026-11-25; step 4, Q5.)* `and`, `or`
and `xor` bind more loosely than `say` does: `say 0 or 2;` is `(say 0)
or 2`, and `say true and false;` prints `1` without a word from perl
(T106). So one after `say`'s argument is refused, and inside brackets,
`say(0 or 2)`, it is the argument's; `... or die` comes with `die`
(step 15). They bind more loosely than the comma too, and `not` takes
a list: in `substr("abc", not 0, 1)` it takes `0, 1`. So in a list of
arguments a word operator stands in brackets or not at all. And a
bracket straight after `not` is all `not` takes, to perl: `not (0) ||
1` is `(not 0) || 1`, which is 1, where `not 0 || 1` is false (T107).
There an operator that binds tighter than `not` is refused after the
closing bracket, as T25 refuses one after `say (...)`; `not ($a ==
$b)` is fine. Rejected: perl's reading of `not (...)`, which is also
what D41 does for `length ("ab") . "c"` (consistent, and a known trap
kept).

**D52. `++` and `--`, by what the variable holds.** *(User: accepted
as recommended, 2026-11-25; step 5, Q1.)* An undef becomes 1 or -1
(and `$x++` is worth 0, `$x--` an undef, as in perl: T43). A boolean
becomes the Int one more or less. An Int steps by one, or `integer
overflow`. A Num: `++` is what `$x + 1` is (D35), the Int when the
Num is integral and otherwise the Num; `--` is the Num one less,
always, because perl subtracts as a float unless the Num has been
used as an integer, and it faults when the Num is integral and the
answer reaches 2^53 in size, where the two part (T93); either faults
where perl warns `Lost precision`, which is by where the Num is and
not by whether the step is lost: `++` from 2^53 up and below -2^53,
`--` above 2^53 and from -2^53 down (T130; as first built it faulted
only when one more was the same float, and the review found 2^53 +
2). A
string that is a number (D40) becomes the Num one more or less,
whatever kind of number it is: perl steps a fresh string of digits as
text (`"12"` to the string `"13"`) and one that has been used as a
number as an integer. It faults if the number is whole and it or the
answer reaches 2^53, and for `++` if the string is digits that begin
with a zero, `"009"`, which is `"010"` or 10 by its past (T113). Any
other string faults: perl's string increment (`"aa"` to `"ab"`) is
cut, and so is the -1 that `--` makes of `"ab"` in silence (T44).
`docs/briefs/step5-increments.py` holds the table to perl on 456
cases under seven pasts each. Rejected: `++` and `--` on an Int, a
Num or an undef only (two rows fewer, and `"12"` stops being a number
in one place).

**D53. A `=` whose right side has no variable in it is refused
wherever its value is tested for truth.** *(User: accepted as
recommended, 2026-11-25; step 5, Q2.)* `if ($x = 5)` is nearly always
a slip for `==`, and perl warns `Found = in conditional` when the
right side is a constant, after folding what it can (T112). Tested
for truth: the condition of an `if`, `elsif` or `unless`, block or
modifier; the test of `? :`; the left of `&&`, `||`, `//`, `and`,
`or`; and what those hand a test down to (the right of one of those
operators, and the branches of a `? :`, when the whole is tested).
That is every case perl warns of and some it doesn't, with no
constant folder. `if ($x = $y)` and `if ($x += 1)` are fine, as they
are to perl. *Two things were added after the build, both where perl
warns and the rule as built didn't refuse:* a test is handed down
through `!`, `not` and a unary plus (perl takes the `!` of a
condition away and tests the other way); and "no variable" means
none that perl can't fold away, so `$x = 0 && $y` and `$x = "p" . (1
|| $y)` are constants (the review of step 5; T112). Rejected: refusing every `=` as a condition (`if (my $m
= f())` would be lost for good).

**D54. `unless` takes no `else` and no `elsif`.** *(User: accepted as
recommended, 2026-11-25; step 5, Q3.)* perl allows both. With an
`else` it is an `if` written backwards. `unless (...) { }` alone, and
`... unless COND;`, are in.

**D55. A name is ASCII, and `$a` and `$b` are not names.** *(User:
accepted as recommended, 2026-11-25; step 5, Q4.)* A letter or `_`,
then letters, digits and `_`. Names past ASCII are Later (they were In
at this step): perl's rule for them is Unicode's with exceptions of
its own. `my $a` is allowed by perl, and breaks `sort { $a <=> $b }`
in its scope: refused here, with `$_` and every other special
variable until a step brings each. A variable is written `$name` and
no other way: `${name}` warns in perl, and `$ name` works. A name is
251 characters at most, which is where perl stops (T126).

**D56. What a variable, an assignment and a statement are.** *(User:
seen with the proposal, 2026-11-25; step 5, Q5: nothing to choose.)*
`my $x;` and `my $x = EXPR;` declare one variable, undef until given
a value, visible from the next statement to the end of its block; a
second `my` of a name in one scope is refused (perl warns), and so is
a use with no `my` in sight (perl doesn't compile it). A `my` may
also stand in the condition of an `if`, and is then visible in the
blocks of that `if` and no further. Not under a modifier, and not in
an operand that may not be worked out (D21, T30). **An assignment's
left side is a variable**: perl takes `($x = 5) = 7` and `(1 ? $x :
$y) = 8`, and D17 has values flowing, not places. `$x OP= E` is `$x =
$x OP E` (held to perl on 7,524 operations); an undef on the left is
0 for `+=` and `-=` and the empty string for `.=`, as in perl, and a
fault for `*= /= %= **= x=`, where perl warns. **Which expressions
are the variable itself**, read when the operator that uses them runs
(D14): `$x`, `($x)`, `+$x`, `my $x`, an assignment, `++$x`, and
whichever operand `||`, `&&`, `//`, `and`, `or` and `? :` give
(T110). `$x++`, `-$x` and everything else are values. **A statement**
is `say`, `print`, a `my`, an assignment, a `++` or `--`, a block or
an `if`; an expression that only has a value is refused (perl warns).
And **after `say` or `print`, a variable followed by a blank and
something that could begin a value is refused**, by perl's own list:
perl takes the variable for a file handle, and dies (T26, T111).
*The review of step 5* added three refusals of the same kind, each
where perl warns or doesn't compile: the file-handle guess is made
after `substr(` and `index(` too, which are list operators to perl
(T125); `$x =- $y`, a sign hard after `=` with a blank after it,
warns `Reversed -= operator` (T127); and `say ("a")` with its `if` on
the next line warns as T76's does (T128).
*Building it* added nothing to choose and four things to say. A
statement is **one** assignment: `$x = 1 and $y = 2;` is two joined,
to perl, which also warns of the first (`Found = in conditional`), and
is refused. An **empty bare block**, `{ }`, is an anonymous hash to
perl and a statement that only has a value (T116): refused; an empty
block of an `if` is fine. `$x = undef if $y;` is taken: a modifier is
not undef's argument. And a **fault in the test of a modifier** names
the line its statement starts on, as perl's warning does, not the
line of the `if` (T118).

**D57. In a concatenation, a later piece may not change a variable an
earlier piece reads.** *(User: a default taken building step 5, as
the safe side of a difference from perl, and accepted as recommended
when he saw it, 2026-11-25.)* perl compiles a row of dots into one operation
that reads every piece when it runs, so `my $x = 3; say $x . "a" .
($x = 5);` is `5a5`, where the first dot on its own would have made
`3a` before the assignment ran (T117). D14's late reads don't cover
it: `$x . "a"` is a value everywhere else. How far a row reaches
turns on what perl folds away first (`(1 ? $x . "" : 0) . ($x = 5)`
is a row, and `55`), on brackets (none stop it) and on its length.
So the pieces of a concatenation are found through brackets, a unary
plus, both sides of `||` `&&` `//` `or` `and`, and all three parts of
`? :`; the left side of `.=` is the first piece; and a piece that
assigns to or steps a variable which any piece before it reads is
refused, with a message that says to make the change a statement of
its own. It refuses more than it must (`$x . ++$x` is `44` both ways,
and `length($x) . ($x = 5)` reads a value), because the exact rule is
perl's optimiser. A change in an *earlier* piece is fine and is what
it looks like: `($x = 5) . $x`, `$x++ . $x`. *The review of step 5
added one refusal to this, for the same optimisation:* `$t .= ($u =
$x . $z);` never assigns `$u` in perl 5.42, which makes one operation
of the `.=` and the dot and loses the `=` between them (T129). A
`.=` whose right side, behind brackets, a unary plus and whatever
gives one operand or the other, is a plain assignment of a
concatenation is refused. This one is a fault in perl and not a rule
of it, and a perl that mends it will make the refusal needless.
Rejected: joining a row
as perl does, in the generated C (it would need perl's folding rules
to know what a row is, and step 16's interpolation will meet the same
thing and can decide it once); leaving it, which is WRONG.

**D58. `do BLOCK while COND` is left out.** *(User: accepted as
recommended, 2026-11-25; step 6, Q1.)* To perl it is not a loop: it
is `do BLOCK`, an expression, under a modifier that perl special-cases
to test afterwards (T64). So a `last` or `next` in its block leaves
the loop round the `do`, in silence, or dies with none round it.
`do BLOCK` has a value and a context of its own (D18) and belongs to
the step that takes it; until then the loop is `while (1) { ...; last
unless COND; }`. Rejected: taking it now as a loop form of its own,
with `last` and `next` refused inside its block.

**D59. A `last` or `next` with no label is refused when the nearest
thing round it that perl counts as a loop is a bare block.** *(User:
accepted as recommended, 2026-11-25; step 6, Q2. It reverses the
plan's reading of T32.)* To perl a bare block is a loop that runs
once, so `while (...) { { last; } say "here"; }` never leaves the
`while`, and perl says nothing. An `if`'s block is no loop, and
`last` goes through it. Here a bare block is a scope and nothing
else: the unlabelled `last` is refused, with a message that says
which braces it would leave, and `W: while (...) { { last W; } }`
says what was meant, to perl as well. Rejected: as perl, which keeps
the idiom of a block one can jump out of; it accepts strictly more
programs, so this can be reversed without breaking one.

**D60. A comma in a C-style `for`, in its first and third parts
only.** *(User: accepted as recommended, 2026-11-25; step 6, Q3.)*
`for (my $i = 0, my $j = 9; $i < $j; $i++, $j--)`. The comma joins
what could each be a statement: assignments and steps, and in the
first part a `my`. Not in the test, where perl tests the last part
alone and warns that the others are useless (T122). The comma
operator is nowhere else in the language. Rejected: no comma, one
expression to a part.

**D61. A label is on a loop, in capitals, and is checked as the
program compiles.** *(User: accepted as recommended, 2026-11-25; step
6, Q4.)* `NAME:` before a `while`, an `until` or a C-style `for`, one
to a loop; a capital letter, then capitals, digits and `_`; hard
against its colon. `last NAME` and `next NAME` must name a loop that
is round them, or the program is refused; of two loops with one name
the inner is meant, as in perl. perl takes a label on any statement,
in any case, with a blank before the colon, and looks the name up
only when the `last` runs: `Label not found`, in the middle of a run
(T121). Not on a bare block (the surface had cut that), an `if`, or
anything else. Rejected: no labels until something needs them, which
D59 does.

**D62. What a loop is.** *(User: seen with the proposal, 2026-11-25;
step 6, Q5: nothing to choose.)* `while (TEST) {...}`, `until (TEST)
{...}`, `for (FIRST; TEST; EACH) {...}` with any part empty and no
TEST true, and `STATEMENT while TEST;` and `until`, which test first.
A test is a test as an `if`'s is (D53). **`last` and `next` are
statements**: alone, with a label, and with an `if` or `unless`
modifier. perl takes them as expressions, `$done and last;`, `$x ?
last : next;`, and takes what follows one for an expression that
names a label, so `last + 1;` dies looking for a loop called `1`
(T120). `... or next` is asked again when `or die` comes (15). **A
`my` in a loop's block or in a `while`'s or `until`'s test is undef
again each time round**, as in perl; in a C-style `for` a `my` is in
FIRST only, where it is one variable for the whole loop; a `my` under
a `while` or `until` modifier is refused, as under `if` (T119).
**`while ()` is refused** (T123). **A fault in a loop's test or its
EACH names the line of its `while`, `until` or `for`**, and under a
modifier the line its statement starts on: perl agrees, but for a
`while`'s test after the first time round, where it names whichever
statement the block ran last (T124). `redo`, `goto` and `continue`
blocks stay cut; `foreach` and a `for` over a list are steps 9 and
10.

**D63. The collector's knobs are three environment variables that
every compiled program reads as it starts.** *(User: accepted as
recommended, 2026-11-25; step 7, Q1.)* `CURLY_GC_STRESS=N`: a
collection at every Nth allocation. `CURLY_GC_POISON=1`: a collected
string's memory is never handed out again. `CURLY_HEAP_CAP=BYTES`:
`out of memory` when more would be held. Each is a whole number in
digits, and 0 or unset is off; anything else stops the program
before it starts, with a message and exit status 2. The binary that
is tested is the binary that ships, and one build runs every way.
They are part of what a program is: anyone can slow one with the
first and stop one with the third, from outside; none changes what
it prints short of `out of memory`. Rejected: flags to `curlyc`,
baked in (the suite compiles again for each setting, and tests
another binary than ships); a test build of the runtime only (the
shipped collector is then code no test has run).

**D64. `t/run.sh` sets stress 1 and poison for every golden test.**
*(User: accepted as recommended, 2026-11-25; step 7, Q2.)* A test
finds a missed root only if a collection falls between an allocation
and a use, and under the ordinary policy a small test never collects.
A test about the cap or the ordinary policy says so in its `# env:`
header, and a test that grows slow from step 9, when a collection
walks every live value, raises its own interval there: the default
stays 1, because what is caught falls fast with the interval. The
knobs are said in one file, `t/knobs.sh`, for every place a test's
binary runs. Rejected: `make test` plain and a `make stress` beside
`make sanitize` (faster, and it will be skipped).

**D65. The language has no cap on memory of its own; every test has
one.** *(User: accepted as recommended, 2026-11-25; step 7, Q3.)*
256 MB, set with the other knobs, so a test that runs away faults in
a second and takes nothing with it. The cap counts what is held: the
living and, under poison, the dead that are kept. Rejected: a default
cap in the runtime (one more way a correct program stops); none
anywhere unless a test asks.

**D66. What the collector is, under D26.** *(User: seen with the
proposal, 2026-11-25; step 7, Q4: nothing to choose.)* **One rule: a
value the program can still use is in a slot whenever a collection
can happen, and one can happen only inside an allocation.** Every
variable and temporary of a function is a slot of one frame, linked
from the context; a variable's slot is its depth among the variables
in scope. A runtime function allocates at most once, as the last
thing it does, or holds what it has made in a frame of its own. A
number as a string never allocates: it is a scratch string on the C
stack for as long as the operation runs, and never a function's
result. **Precise is about what a slot holds**, not whether it will
be used: a string stays until its slot, a temporary's too, is given
something else or its function returns. **With no knob set**, a
collection runs when the bytes allocated since the last pass the
larger of 1 MB and what was live after it. **`out of memory` is a
fault** like any other. **A string used after it was collected is an
`internal:` error**, exit status 2: a bug in the compiler or the
runtime, never the program's. No finalisers. Left for their steps:
marking through a value that holds values, and a mark stack (9, 13);
a variable that outlives its frame (14); unwinding frames at a caught
`die` (15); a heap for each context (29).

**D67. Nothing happens at 100 calls deep. `no warnings 'recursion';`
is accepted, and is what keeps perl as quiet.** *(User, 2026-11-25;
step 8, Q1: "I do not want it to fault at 100 levels of recursion, I
want to support much deeper levels than that without warning. That
warning in Perl is old and from the days when subroutine recursion
was really slow." And before it: "lets add `no warnings 'recursion'`
to the perl 5.42 prelude". The builder first read the earlier answer
as the recommendation, a fault at 100 without the line, and was put
right.)* perl warns `Deep recursion on subroutine` when one sub has
100 calls of itself open at once, and carries on (T142). The language
does not fault there and says nothing: this is D15's one standing
exception, a run-time warning of perl's that is not a fault, because
the warning is about a cost perl no longer has and not about a
program that is wrong. The line `no warnings 'recursion';` joins
D16's list: after `use v5.42;`, with the other pragmas, before the
first statement, and nowhere else. It changes nothing here. Under
perl it silences that warning for the whole file, so a program that
carries it prints the same and is as quiet under both, and the
oracle check keeps its rule that perl's stderr is empty (D10): a test
that goes 100 deep carries the line, and one that doesn't is rejected
by the check as any test perl warns of is. A program without the
line that goes deep runs here as it does under perl, with perl's
warning the only difference, on stderr, which D12 doesn't count. The
only limit on depth is D68's. Rejected: a fault at the 100th open
call unless the program has the line (the recommendation: D15 with
no exception, at the cost of a fault for a warning nobody heeds); a
fault at 100 always; the oracle check forgiving that one warning
without the line (a hole in the one check that holds the suite to
perl); perl's rule in full, that the pragma covers the calls written
in its scope (a line at the top is the whole file).

**D68. Past a limit the implementation sets, recursion is a fault,
and the limit is not part of the language.** *(User, 2026-11-25; step
8, Q2: "ok, lets stick with what we are doing now. We can revisit
later as needed." And before it: "I would like to avoid being too tied to the C-stack, but this
is perhaps something to discuss later when we talk about concurrency
... I want to avoid boxing ourselves in such that we can't fix it
later." The number is the builder's default.)* perl keeps its calls on the heap and has no limit; a
compiled sub here is a C function, and the C stack ends. Today the
frames that are open may hold 4 MB, counted as 16 bytes a slot and
1 KB a call, which is more than a call takes under any build measured
(`briefs/step8-stack.c`), so the count runs out with half of an 8 MB
stack left: about 3,800 calls deep for a small sub. Past it,
`recursion too deep`. **What keeps this open for step 29**: the
language promises only that there is a limit and that reaching it is
a fault, so a higher limit, or none, changes no program that ran; no
test but the limit's own two knows the number; the count is of
frames' bytes, kept in the context, and not of the C stack's
addresses, so it means the same wherever frames come to live; the
generated C reaches a slot only as `f[n]` and a frame only through
`rt_enter` and `rt_leave`, so where slots are kept is the runtime's
business; and the runtime never calls generated code (step 10's
`sort` with a block is the first thing that will want to, and has to
say how). **What does tie it**: a sub is a C function and a call is
a C call (D3, D31). Being clean of the C stack between statements,
as perl is, is another code generator, and concurrency (step 29) is
where that is decided. Rejected for now: the body run on a stack the
runtime makes (about 60,000 deep; a thread or a hand-made stack on
two systems, which step 29 will choose anyway); frames on the heap
and no C recursion (not D31's C).

**D69. D57, through a call.** *(User: accepted as recommended,
2026-11-25; step 8, Q3.)* A concatenation is refused when a later
piece calls a sub that can assign or step a variable an earlier piece
reads, "can" worked out over the whole program: the sub's own body
and defaults, and those of every sub it calls. perl joins a row of
dots as one operation and reads each piece late, so `$x . "-" . ch()`
is `b-c` when `ch` sets `$x` to `b` (T132). Only a file variable can
be changed by a call. Step 14's code references will have to say "any
sub" where they can't tell. Rejected: refusing wherever an earlier
piece reads a file variable that any sub assigns and a later piece
calls anything (no walk over the calls, and it refuses `$count . ": "
. name($k)` in any program with a sub that counts); joining a row as
perl does (D57).

**D70. A sub that ends in `say` or `print` is worth `true`, as in
perl.** *(User, 2026-11-25; step 8, Q4: "The return value of say is
documented to be `true` I believe, which would print `1`. If this is
a problem, then do what you recommend." It is not a problem, so the
recommendation, no value, is what was turned down.)* perl's `say` and
`print` return the boolean true (`is_bool` says so), and a sub whose
last statement is one returns it. Here that is the one place either
has a value: they stay statements everywhere else, `my $x = say 1;`
is still refused. Under a modifier, `say "hi" if $c;`, the last
statement is an `if`, and the sub has no value (D18). perl's `say`
returns false when the write fails; the runtime doesn't look, and a
closed or failing stdout is outside what a program here can arrange
(step 21 meets it). Rejected: no value, like a sub that ends in an
`if` (a fault where perl has a plain answer, and D2 prefers the
answer).

**D71. A sub that returns nothing faults where perl wants a list,
until step 10.** *(Retired at step 9 by D79: there are lists, and it
is no value in one.)* *(User: accepted as recommended, 2026-11-25; step 8,
Q5.)* `return;` and an empty body give undef to a scalar call, as in
perl. To a list they give no values, so `g(f())` calls `g` with no
arguments and `say f();` prints an empty line (T133); there are no
lists yet, so that is a fault, `f returned nothing where a list is
wanted`, one of D15's list of faults where perl is silent. Step 10
brings list returns and can agree. Rejected: an argument list whose
length is known only as it runs, now, for this one case.

**D72. What a sub is.** *(User: seen with the proposal, 2026-11-25;
step 8: nothing to choose.)* `sub NAME(PARAMETERS) { ... }` at the top
level, before or after its calls; a signature always *(or none: D105)*. A parameter is
`$name`, `$name = EXPR`, `$name //= EXPR`, `$name ||= EXPR`, or a
placeholder, required ones first; a copy (D17); a default is worked
out at each call that needs it, left to right, and resolved before
its own parameter exists (T138). **A call** is `NAME(ARGUMENTS)`, an
expression and a statement; an argument that is a variable is read
when the sub is entered (D14, T1), and what a sub returns is a copy.
**A wrong number of arguments is a fault** (D13), after every
argument has run. **`return` is a statement**: alone or with an
expression, with an `if` or `unless` modifier, in a sub (T139). **A
sub's value** without a `return` is its last statement's when that is
an expression, and a value alone is a statement in that one place
(T140); D70 has `say`; any other ending has none, and using it
faults (D18). **Context** is perl's three, passed on by `return
f()`, a last statement `f()`, the arms of `? :` and the right of
`||`, `&&` and `//`. **A file variable has a slot of its own, undef
as the program starts, and its `my` stores nothing** (T134); a sub
may name those declared at the top level before it. **A sub's name**
is ASCII, at most 251 characters, not a word of perl's (D21), not one
perl calls by itself (`BEGIN`, `AUTOLOAD`, `import` and the rest),
not `v` and digits (T136), and not used twice; a call of a sub the
program doesn't have is refused. **Refused besides**: a minus hard
against a one-letter name (T135); a blank between a call's name and
its bracket after `say` or `print` (T136); two commas together
(T137); a parameter named `$a`, `$b` or `$_`, or named twice, and a
`my` in the body of a parameter's name (T141); a sub in a block, a
loop or a sub (T31). **A fault's line** is the statement's (D34),
the caller's again after a call returns.

**D73. What the review of step 8 changed.** *(User: a default of the
builder's, 2026-11-25, each on the safe side of a difference from
perl that the review found, T143 to T148; confirmed when he saw it,
"D73 and D74 are fine".)* **A sub is handed
where its arguments are, and copies each as its parameter's turn
comes**, a default running in between: perl's order, so `f(undef,
$g)` with a `//=` default that changes `$g` gives the second
parameter the new `$g` (T144). The arguments stay in the caller's
slots until then, which is what keeps them from the collector.
**`(...) x N` is refused as an argument, in a `return` and as a last
statement**, through brackets, a unary plus, `? :` and `|| && //`,
as it is for `say` (T101, T143): it is a list there, and step 10 can
agree. **A last statement with a modifier has no value**, as an `if`
has none (D18, T145), and a value alone with a modifier is refused.
**Context goes down through brackets, a unary plus, both arms of `?
:` and the right of `|| && // and or`** (T146); `xor`, `!`, `not` and
the left of every operator are scalar. A call that is a statement, a
`for`'s first or third part, or under a modifier is void; a test is
scalar. **Nothing is skipped under void** (T148). **After `say` or
`print`, behind any opening brackets, a call that comes first has its
bracket touching its name** (T136). **A sub's name is not `v`, a
digit, and digits or underscores**, and the table of perl's names is
perl's own keyword list, whole, with a check that each word of it is
refused (T28). **A minus hard against one letter that is not followed
by another is refused by the lexer**, wherever it stands (T135).
**`my $x += 10;` at the top level is the operator on what the
variable holds** (T147), as T134. Rejected: refusing a `//=` or `||=`
default that calls a sub when a parameter follows (agreeing costs a
calling convention and nothing else); agreeing with T145 (the test's
own value when it fails: T19, decided the other way in D18).

**D74. What building step 8 settled.** *(User: defaults of the
builder's, 2026-11-25, confirmed when he saw them, "D73 and D74 are
fine".)* **A call may be a part of
a `for`**, `for (init(); $n < 8; step())`, void as perl has it: D60
refused a part that only has a value, and a call is something done.
**`$x .= set();` is refused when `set` can change `$x`**: D69 through
D57's rule that the left of `.=` is the first piece of a row, though
here the straight-line C would have agreed with perl (`b3`). **The
words of the faults**: `too few arguments for f: got 1, expected 2`,
with `at least` and `at most` where perl has them; `f has no value: it
does not end in a return or an expression`; `f returned nothing where
a list is wanted`; `recursion too deep`. **Their lines**: a wrong
number of arguments and `recursion too deep` name the caller's
statement; a sub with no value, its last statement; `return;` to a
list, the `return`; an empty body, the `sub`; a fault in a default,
the line its parameter is on. **A sub's name is refused where the sub
is written**, not at the first call of it. **A program given less
than 8 MB of stack stops before it starts**, with a message and exit
status 2, as a bad knob does (D63): the limit on depth is counted
(D68), and the count assumes that much. Rejected: letting `$x .=
set()` through (one more shape of row to reason about, for a program
that is hard to read either way).

**D75. The last statement of a block may leave its semicolon out.**
*(User, 2026-11-25, on seeing that step 8's one-line subs were
refused: "Allow the last statement in a block to omit the
semicolon".)* `sub double($x) { $x * 2 }` and `if ($ok) { say "yes"
}` are how Perl is written, and perl takes both. Step 5 had every
statement end in one, the last in a block too, as a default nobody
had numbered. A block is a sub's, a loop's, an `if`'s or a bare one;
the last statement of the *file* still ends in its semicolon, which
is the smallest change that was asked for, though perl takes that
too. `;;` is still refused. Evidence: with the semicolon before
every closing brace taken out of every `same` test that has a block
(31 tests, 5,505 semicolons, `briefs/step8-semicolons.py`), perl
compiles each in silence and prints the same, and so does the
compiler. Rejected: the rule as it was.

**D76. A list is a row of values, copied as it is built; a later part
of an expression or a list may not change what an earlier part
names.** *(User: accepted as recommended, 2026-11-25; step 9, Q1, as
its adversarial review widened it.)* perl's lists are rows of the
containers themselves, so a change made after a list was begun shows
through it: `my @b = ($x, bump());` has the `$x` that `bump` left,
`$a[0] + chg()` what `chg` stored, `(@a, chg())` the stored element
(T149, T157). Past a store perl's own answer stops being a rule:
`$a[1] * splice(@a, 0, 1)` is 2, and one shape reads a value that
was freed. So here an element, a slice, an array and `$#a` are read
where they stand, a scalar variable that is an item of a list is
copied into it, and **the program is refused when a part worked out
later can change one of them**: by an assignment, a step, a store to
an element, a change of an array's size, itself or through a sub it
calls, worked out over the whole program as D69 is. "Later" is the
other operand, a later item or argument, a default of the sub being
called, an index of an assignment's target, a later piece of a row
of dots. One message, which says to take the value into a `my`
first. What is still agreed with, because the generated C keeps the
place and not the value: a scalar variable as an operand (D14) and
as an argument of a call (D73). Rejected: an element as a place read
late, with the array pinned against a change of size until the
operator has run (more of perl kept, a pin in the runtime, and
nothing for the scalar in a list); reading early and refusing
nothing (`$a[0] + ($a[0] = 10)` is 11 where perl has 20).

**D77. `for my $x ($p, $q)` walks copies, and is refused when the
loop can change a scalar its list names.** *(User: accepted as
recommended, 2026-11-25; step 9, Q2, as its review widened it.)* perl
walks the variables themselves (T13), and an array can be frozen
where a scalar can't. The refusal is of a loop whose block, or a sub
the block calls, can assign or step a scalar variable named anywhere
in the loop's list, whatever it stands in there (`substr($s, 0, 1)`
is `$s` to perl's `foreach`: T162). Rejected: refusing every scalar
named in the list; leaving it refused.

**D78. A list assignment is a statement.** *(User: accepted as
recommended, 2026-11-25; step 9, Q3.)* `if ((my @r = f()))`, `my $n =
(my ($p, $q) = @a);` and `my $c = () = LIST;` are the count of the
right side in perl (T151), and refused here; `my @r = f(); if (@r)`
says it. As a sub's last statement it has no value, like an `if`
(D18): perl gives the count to a scalar and the targets to a list
(T168). Rejected: the count, as perl has it (one more thing an
assignment can be).

**D79. A sub that returns nothing is no value in a list.** *(User:
accepted as recommended, 2026-11-25; step 9, Q4. Retires D71's
fault.)* `my @c = none();` is empty, `(1, none(), 2)` is two values,
`g(none())` calls `g` with nothing, `say none();` prints an empty
line: as perl has them. D71 made these a fault for want of lists.
Where one value is wanted it is undef, as before. Step 10 widens
"one value or none" to any number.

**D80. What an array and a list are.** *(User: seen with the proposal
and its review, 2026-11-25; step 9: nothing to choose.)* **An array**,
`@a`, is a variable of its own name (`@x` and `$x` are two), and
assigning one copies it. **A list** flattens. **An element**,
`$a[I]`: I a whole number by `substr`'s rule; a read past either end
is undef and makes nothing; a store past the end makes the array
longer; before the start it is a fault. **The order**, which is
perl's (T158, T159, T163): `$a[I] = V` works out V's calls, then I,
then reads V and stores; `$a[I] OP= V`, a step, `||=` and its kin
work out I, make the target (the array grows to hold it, or it is
the fault), then V; a list assignment works out its right side, then
every target's index, then stores; a list slice works out its
indexes before its list. **Where one value is wanted** an array is
its count (T21, T150), `(LIST)[N]` that element, and a slice, a
range, a comma list, `splice` and a list assignment are refused
(T151, T68). **`pop` and `shift`** take brackets unless the array
ends the expression, and always name an array (T152); `push` and
`unshift` need a value to add; `splice` has brackets, and its offset
and length go by the index's rule (T165). **A range** is whole
numbers, each end cut toward zero; a string or an undef end is a
fault (T154). **A slice of an empty list is empty** in a list
(T164). **`foreach`**: the block once for each value of a copy of
the list, `$x` read-only, and **every array named anywhere in the
list frozen** until the loop is left by any way (D17, T162): a store
to an element or a change of size, from anywhere, is the fault `an
array was changed while a foreach is over it`. A range freezes
nothing, so `for my $i (0 .. $#a) { $a[$i] *= 2 }` is how an array
is changed in a loop. A `foreach` over one range counts and builds
nothing, and faults where perl's does, on an end below -2^63 + 513
(T166). An element or a slice past either end in a `foreach`'s
list, and a slice past either end in a call's arguments, is a fault
(T161: perl makes the elements). **A file's array** has a slot of its
own, empty as the program starts, and its `my` stores nothing
(T156). **Refused besides**: `@a[one index]` (T167); `defined` and
`length` of an array, a comma after an assignment's right side, `[`
after a call's own brackets, `$a[0][0]`, `my ($x, $x)`, an array
among a list assignment's targets that is not the last (T168); `for
my $x ()` (T155); and, until their steps, a slice on the left of
`=`, `$#a = N`, `exists` and `delete` of an element, `for my ($i,
$x)`, a `for` with no `my`, `return` of a list, `@rest` in a
signature, `@a` in a string. **Built as two sub-steps** (Q5): 9a is
arrays, lists, elements, the builtins and D76; 9b is `foreach`,
ranges, the freeze and D77.

**D81. What building step 9 settled.** *(User: defaults of the
builder's, 2026-11-25, confirmed when he saw them: "D81 is
confirmed".)* **D77
holds for the end of a range too**: `for my $i (1 .. $n) { $n-- }`
is refused, though perl fixes a range's ends as the loop starts and
would have agreed (T172). D77's words are "named anywhere in the
loop's list, whatever it stands in", and one rule with no exceptions
is the cheaper; the cost is a `my $end = $n;`. Rejected for now: an
exception for a range's ends, which is sound and can be added.
**`foreach` is the loop over a list alone**: `foreach (FIRST; TEST;
EACH)` is refused, where to perl the two words are one (T122, T171).
**`for $x (LIST)` with no `my` is refused** (T14, T171: perl lends
the variable to the loop and gives it back). **A string that is no
number as a literal index, `$a['x']`, is refused** as the program
compiles, where perl warns as it compiles; through a variable it is
the fault. **Where perl would make an element in a `foreach`'s
list** (T169) is every place D80's fault is: the item itself, a
branch of `? :`, the right of `|| && //`, a list repeated, a unary
plus; the left of `||` and an operand of anything else is a value,
and undef past the end, as perl has it. **The freeze is by name, and
not by reach**: `for my $i (0 .. $#a)` freezes `@a`, since `$#a`
names it, and the loop that changes an array as it goes takes the
count into a `my` first. **The words of the faults**: `an array was
changed while a foreach is over it`; `an element past the end of the
array in a foreach, where perl would make it`; `a slice past the end
of the array, where perl would make the elements`; `a foreach over a
range that begins or ends this near the smallest integer: perl
refuses it`; and 9a's, `an element before the start of the array`,
`array too long`, `splice past the end of the array`, `splice before
the start of the array`, `a string as the end of a range`. **Their
lines**: a fault in a loop's list names the loop's line. **An array
is 40 bytes and its header**, the freeze's count among them, and an
array given back more often than it was frozen is `internal:`, exit
2: the compiler's mistake, never a program's.

**D82. `sort` makes perl's comparisons, in perl's order: perl's
merge, ported.** *(User: accepted as recommended, 2026-11-25; step
10, Q1: "go with your recommendation, and lets make a note that when
we add a license, we need to account for this.")* The order shows
three ways (T3, T173): an effect in the block, a block that is no
consistent order, and a fault that only some pairs reach; and `$a
<=> $b` itself is not a consistent order where an Int of 2^53 or
more meets a Num (D49). So the runtime has `pp_sort.c`'s merge, runs
found first and then merged, and the tests hold it to perl by a
block that logs every pair it is given. **The licence, to account
for when the repository gets one**: `pp_sort.c` is perl's, "under
the same terms as Perl itself" (the Artistic License or the GPL), a
port of it is a derived work, and the runtime is linked into every
compiled program. The port is kept in a file of its own that says
where it came from, so that it can be found and dealt with whole.
Rejected: a merge of the language's own with the block held to what
can't show (every comparison of a large Int with a Num would have to
fault inside a `sort`, and most blocks be refused).

**D83. The generated code drives a `sort`; the runtime never calls
the block.** *(User: accepted as recommended, 2026-11-25; step 10,
Q2.)* The runtime's merge can stop and be taken up again: it runs to
its next comparison and hands back the two values, the generated C
runs the block where it stands, as it does a loop's, and hands the
answer back. The runtime still calls no generated code (D68), and no
C frame of the runtime's sits between a program and what its block
calls. The cost is a port that is less of a copy of perl's text, and
leans on D82's logged comparisons. Rejected: the block as a C
function the runtime calls, handed its caller's frame.

**D84. Where one value is wanted, `grep` and `map` are their count;
`sort` and `reverse` are refused there.** *(User: accepted as
recommended, 2026-11-25; step 10, Q3.)* `my $n = grep { ... } @a;`
and `if (grep { ... } @a)` are as in perl (T178). perl's `sort`
there is undef with a warning, and its `reverse` joins its arguments
and reverses the characters, which is for the step that has strings
to propose. A `return grep { ... } @a;` reached by a call for one
value is still D18's fault. Rejected: refusing all four.

**D85. `map` and `grep` take a block, and `$_` is always written.**
*(User: accepted as recommended, 2026-11-25; step 10, Q4.)* `map
EXPR, LIST` and `grep EXPR, LIST` are refused: it is the form where
perl's parser guesses (`map ($_ * 2), (1, 2)` is a `map` of nothing,
T180). A builtin with no argument does not mean `$_`: `grep {
defined($_) } @a`, `say $_ for @a;`. Rejected: the form without a
block; the defaults.

**D86. Step 10 is built as three sub-steps**, each green and
committed. *(User: accepted as recommended, 2026-11-25; step 10,
Q5.)* 10a: list returns, D18's fault, slurpy parameters, `join`,
`reverse`. 10b: `$_`, `for (LIST)`, the `for` modifier, `map`,
`grep`. 10c: `sort`.

**D87. What step 10's review changed.** *(User: defaults of the
builder's, 2026-11-25, on the review's findings, confirmed
2026-11-26: "D87-D89 are confirmed"; none changes D82 to D86.)* **For D76's walk,
`grep`, `sort` and `reverse` name what their list names**, a scalar
counted as an item, and `join`'s separator is the first item of its
list (T185, T186: perl hands the containers on, and reads the
separator late); `map` names nothing. **An undef in an array sorted
in place is a fault** (T187): perl's in-place `@a = sort BLOCK @a`
drops the elements that were never stored, a past of the array's
that is not kept here; rejected, keeping that past through every
route that fills a slot. **D80's fault for an element or a slice
past the end holds in a `sort`'s list** (T188). **A word that is not
perl's own, first after `sort`, is refused** (T189: perl takes a
sub's name for the comparator, and `true` for a string). **`map`,
`grep` and `sort` are written without brackets of their own**
(T190); `join` and `reverse` with or without. **A `sort` of one
value**, with no block or one of the four perl throws away, checks
that value as a comparison would (T190). **`join`'s separator is
made a string always** (T190). **Under a `for` modifier** there is
no `last`, `next`, `return` or second modifier (T191, T192). **A
slurpy parameter is filled at its turn** (T191). **In a `map`,
`grep` or `sort` block**: no `return` at any depth; `last` and
`next` only to a loop inside the block; no `{` first; the last
statement is a value, `or` and `and` and a scalar assignment
included, and a list assignment is refused there (T192, D78).
**T143's refusals end** where a list is wanted. **`map` and `grep`
may be statements.**

**D88. What building step 10 settled (10a, 10b).**
*(User: defaults of the builder's, 2026-11-25, confirmed
2026-11-26.)* **A list after `return` is in brackets**, unless it is
one thing that is a list (T193: perl returns `1, 2` whole). **D18's
fault is raised before anything of the list is worked out**, and a
call for nothing works a list-shaped `return` out as a list.
**`reverse` with nothing to reverse, and a comma after a slurpy
parameter, are refused** (perl takes both). **A slice of a list by a
call that gives a list is refused where one value is wanted** (T193:
perl gives the slice's last). **A block that ends in a `say` or a
`print` is worth `true`**, as a sub that ends so is (D70).
**`$_` can not be declared**: perl refuses `my $_` too (T194).
**`say for LIST;` is refused**, by D85. **A `map` in a loop's list
freezes the arrays its own list names**, by D80's "named anywhere",
though perl's `map` gives copies: the stricter, and one rule. **The
fault's words are the `foreach`'s for every binder**: `an array was
changed while a foreach is over it`. And `f returned a list where
one value is wanted`; `joined string too long`.

**D89. What building `sort` settled (10c).** *(User: defaults of the
builder's, 2026-11-26, confirmed the same day.)* **`sort`
takes no brackets of its own**, as D87 has it, though `sort(@a)`
alone is silent in perl: one rule with `map` and `grep`. **A scalar
first after `sort` is refused**, as a word is (D21: perl takes it for
a sub to compare by); `sort +$x, $y` and a block are the ways round
(T195). **A `sort`'s block ends in an expression**, and not in a
`say`. **Its value is cut toward zero**, as perl cuts it, and is a
fault outside 32 bits, both ends (`a sort block's value is outside
32 bits, where perl wraps it`). **In place** is `@a = sort BLOCK @a`
with brackets round either side or neither, and nothing else: `an
undef in an array sorted in place: perl drops an element that was
never stored`. **`$a` and `$b`** are refused outside a `sort`'s
block and as declarations, by the resolver and the parser; the lexer
takes them. **The port lives in `runtime/sort.c`**, included by
rt.c, with its origin and perl's terms at its head (D82).

**D90. Interpolation is pulled forward, to before the census.**
*(User, 2026-11-26: "Lets pull interpolation forward and lets do it
before the census.")* Step 16 had it, with `q`, `qq`, `qw`, heredocs
and `sprintf`; it is now **step 11a**, alone, and the census is 11b.
The reason: nearly every Perl program anyone writes has a variable in
double quotes, so until it is in the census's probes are refused at
their first string and the census measures little; and the tests of
steps 9 and 10 were written round its absence. What it interpolates
is scalars, arrays and elements, as far as the language has them at
that point (no hashes, no references: steps 12 and 13 widen it), and
which shapes perl has to guess at and are refused (D21) is for 11a's
proposal to say. Step 16 keeps the rest: `q`, `qq`, `qw`, heredocs,
`sprintf`, `printf`, `\U` and its kin, the remaining string
builtins. Rejected: the census first (it would mostly count
refusals); all of step 16 forward (large, and most of it is not what
the probes are refused for).

**D91. In a string, an index is a whole number or a scalar
variable.** *(User: picked the recommendation, 2026-11-26; step 11a,
Q1, as its review amended it.)* `"$a[0]"`, `"$a[-1]"`, `"$a[$i]"`;
in a slice, two or more of those with commas between, or a range
between two of them. The number is the language's own whole-number
literal: no leading zero, which is octal to perl in silence (T211),
and no more than 2^63 - 1, past which perl's index wraps. To perl an
index in a string is any expression, read as code, and the pieces of
the string are read late (T197), so an index that changed a variable
would show in the pieces before it; with this rule nothing in a
string can change anything, and D57 and D76 have nothing to check
inside one. It is what 178 of the 184 elements in the census's
probes' strings are. Anything else is refused, with a message that
says to take the index into a `my` first. Rejected: an expression
that changes nothing (the lexer reading code inside a string, for
six of the probes' elements); whatever perl takes (calls in an
index, and D57's and D76's walks through a string).

**D92. A `$` or an `@` in double quotes begins a shape of the
language's, or is refused.** *(User: picked the recommendation,
2026-11-26; step 11a, Q2.)* The shapes: `$name`, `${name}`, `@name`,
`@{name}`, `$name[I]`, `@name[I, J]`, `$#name`, `$#{name}`, each
hard against its `$` or `@` (T200). What follows a shape is text, as
perl has it (`"$x's"`, `"$x: "`, `"$x->y"`), except what perl would
take into the variable, which is refused: `::` (T199), `{`, a second
`[`, `->` before `[`, `{`, `@` or `$` (T203), and a character past
ASCII (T205); after a name in braces nothing is. T34's refusal
stands for every other `$` and `@`: `"a @ b"` is text to perl, but
which `@` is text is a table of perl's (`"@-"`, `"@_"` and `"@1"`
are arrays, empty and silent: T204), and "an `@` in double quotes is
an array's or has its backslash" is one line. Rejected: text
wherever perl is silent; refusing `->`, `:` and `'` after a name
too, which would refuse what everyone writes.

**D93. `"$#a"` interpolates.** *(User: picked the recommendation,
2026-11-26; step 11a, Q3.)* And `"$#{a}"`. perl has one reading of
them. `::`, `[` and `{` hard after `$#a` are refused: `"$#a::"` is
`-1` to perl, in silence. Rejected: refusing it.

**D94. The tests written round interpolation's absence stay as they
are.** *(User: picked the recommendation, 2026-11-26; step 11a, Q4.)*
They test what they were written to test, and their models are
records of their steps. New tests use interpolation, and T34's
refusal tests whose shape is now in become tests of what they print.
Rejected: rewriting the models to print through strings.

**D95. An interpolated string is a value, made where it stands; and
what step 11a's review and build settled.** *(User: defaults of the builder's,
from the proposal's "What has nothing to choose", its review and the
build, laid out for him one by one and confirmed, 2026-11-26: "D95 is
confirmed".)* perl compiles a string as one operation of its
own, which the row of dots round it does not take in (T196: `"$x-" .
($x = 5)` is `3-5`). So it is no piece of a row for D57 or D69,
names nothing for D76, freezes no array in a loop's list and names
no scalar for D77 (T209); it is a Str whatever it holds, each piece
made a string as `.` makes one, an array as `join(" ", @a)` does
(`$"` is not in the language); an undef anywhere in it is D48's
fault. **Added to D57**: the right side of `.=` may not be an
assignment of an interpolated string, which perl never makes (T198),
unless the string is one variable, one array, one element, one slice
or one `$#a` and nothing else; however many pieces it has, and
through what D57's refusal looks through (T212). A character past
ASCII hard after a name is refused, perl's rule being Unicode's
tables (T205). From the review's open ends: a blank after an index's
minus is refused; a comma may follow a slice's last index; `...` is
refused. `${\ ...}`, `@{[ ... ]}`, `$$x` and `@$x` wait for step 13,
`"$x{...}"` for step 12. *What the build settled:* a character past
ASCII is refused after a bare name and not after an element or a
slice, where perl has no name to go on with and there are no braces
to write; a slice by one index is refused in a string as outside one,
a comma after it or not (T167); `"$x->$y"`, which is text and a
variable to perl, is refused with the other arrows before a `$`;
and of two faults in one string the left one's is raised, each piece
being joined on before the next is worked out.

**D96. The census imports its probes, with `use v5.42;` in front; a
probe refused by design is kept and not run; and its results are a
JSON file in git.** *(User, 2026-11-26: "it is okay to prepend use
v5.42. tests that we would refuse By Design should be included, but
we don't need to run them. Then if we do bring something back, we
move the tests where they can be run... `make census` should
generate a JSON file of the results. Then WRONG items can be
prioritized, etc. and if we track it in git, it also shows progress
towards the census goals"; and, of pvm's cases, "Lets import them
into t/census/".)* D11 said the probes are copied in and judged;
this says how. All but 21 of the 9,059 programs lacked the line the
language begins with, so without it the census is one refusal;
perl's own answer is taken from the file as imported. The probes
are perl5-son's two sets, Chalk's and pvm's `conformance/mdtest`
programs, 5,786 once copies are one probe. PerlOnJava's unit tests,
which pvm carries, are `Test::More` scripts and wait for step 18;
pvm's parser fragments print nothing and are no probes. Rejected:
reading pvm's cases in place (one corpus shared, and the census
tied to another repository's revision); running the probes as they
are; porting them (D8 bends an example, and a ported probe is no
longer somebody else's).

**D97. The census's verdicts, and its rules.** *(User: accepted as
recommended, 2026-11-26; step 11b, Q1 to Q4: "Sounds good, they
suit me".)* D11's four verdicts, and two more: **WARNS**, the same
output where perl also warns (D15 makes that no agreement, and it
is no WRONG), and **UNJUDGED**, where perl's own output moves with
the hash seed or perl does not end. A REFUSED has a reason, by a
table in the census's script from the compiler's message: `design`
with the decision, `later` with the step, or `open`; the compiler's
messages are not touched. **A probe's reason is its first
refusal's**, and the compiler does not go on past one to find the
rest. **A WRONG may stand in the committed file while it is worked
on, and fails `make test` while it does**, so no step ends with
one: D11's "WRONG is 0" holds at every step's end, and the finding
is in the history. A probe that was SAME in the last commit is SAME
in this one, or is named in `t/census/LEFT-SAME.tsv` with the
decision that moved it. The 206 probes perl itself stops at with
the line in front are kept in `not-perl/`, and never run. Rejected:
a reason on every refusal in the compiler (212 of them); a file
that may not hold a WRONG (the finding is then in nobody's
history); a WRONG marked as known and allowed (the door D11 shut);
one step for the import and another for the rest.

**D98. Hashes are two sub-steps.** *(User: picked the recommendation,
2026-11-26; step 12, Q1.)* 12a is the hash itself: declaring, the
literal and `=>`, elements, `exists`, `delete`, `keys`, `values`,
the count, copying, D76 and the orders, and the runtime's table. 12b
is what stands on it: the freeze in loops and binders, slices,
`%opts`, an element in a string. Rejected: one step.

**D99. In a string, a hash's key is a word or a scalar variable.**
*(User: picked the recommendation, 2026-11-26; step 12, Q2.)*
`"$h{name}"` and `"$h{$k}"`, and nothing else: D91 for a key. To
perl what stands in the braces is code. A slice of a hash in a
string is refused, since its keys would have to be quoted there. It
is what 304 of the 317 keys the census's probes write in strings
are. Rejected: a whole number and a string in single quotes too
(thirteen more keys, and `"$h{01}"` is the key `1` to perl);
whatever perl takes.

**D100. A slice may stand on the left of a list assignment, an
array's and a hash's.** *(User: picked the recommendation,
2026-11-26; step 12, Q3.)* `@a[0, 1] = ...` and `@h{"a", "b"} =
...`, as targets, by D80's order: the right side, every index or
key, then the stores. Step 9 had left the array's out. `%h{...}`,
the slice that gives keys and values, is cut: perl warns of it
where one value is wanted. Rejected: reading only.
*(Building step 12b, 2026-11-26: a slice is the one target of its
assignment, `@h{...} = LIST;`. Beside other targets in brackets,
`($x, @h{...}) = ...`, perl takes it and this refuses it. User: "Leave
the slice as the only target for now.")*

**D101. No `each`, and no loop of two variables, at step 12.**
*(User: picked the recommendation, 2026-11-26; step 12, Q4.)* `each`
was cut already, its iterator being hidden state in the hash.
`foreach my ($k, $v) (%h)` is not taken up: `for my $k (sort keys
%h)` says it, a test has to sort in any case, and a loop of two
variables is a second shape of `foreach` in every pass. It can be
proposed when a program wants it. Rejected: the loop of two
variables now.

**D102. What step 12's review settled.** *(User: defaults of the builder's
on the review's findings, confirmed 2026-11-26: "D102 is confirmed".)* **A word alone in
a hash's braces, and a word before `=>`, is a string only on one
line**: the word and its braces, or the word and its `=>`, with
nothing but blanks between; anything else is refused. perl reads
`true` as the boolean and `v65` as a version string once a line end
stands beside the word (T223, T224), and quotes every other word
across a line before `=>`, which this refuses too, for one rule
with no list. `keys` and `values` are refused before an operator
that binds tighter, as `exists` and `delete` are (T225). An odd
count for a `%` parameter, named or not, is the fault for a wrong
number of arguments, raised as the sub is entered (T226). After a
hash's element in a string, `[`, `{`, and `->` before `[ { @ $` are
refused (T227). `delete` and an assignment to a hash are changes
for D76. A slice on the left stores an undef for each target the
list does not reach; a slice of one there, a hash that is not the
last target, and `@h{...} OP= ...` are refused (T228). `%h` after
`return` is list-shaped (T229). `map { $_ => 1 } @l` stays refused
for its bare comma. And the oracle check's reading rule is mended
before the step's tests are written: it learns where a hash is
counted, copied or handed on, and rejects a `sort` block that does
not only compare `$a` with `$b`, a block that prints between a
`sort` and its `keys`, and a slice of `keys`.

**D104. What building step 12a settled.** *(User: defaults of the
builder's from the build, confirmed 2026-11-26: "D104 is confirmed".)* **Until step 12b, a hash named
in the list of a `for`, a `map`, a `grep` or a `sort`, other than
by `keys`, is refused**: `for my $v (values %h)`, `sort values %h`,
`map { ... } %h`, an element there. The freeze belongs to such a
list (D17, T217), and D98 put the freeze in 12b; taking the list
before its fault exists would be a feature with no fault test.
`for my $k (sort keys %h)` is in, since `keys` are copies and name
nothing (T218). **A blank between a variable and its key's brace,
`$h {a}`, is refused**, as `$a [0]` is: perl takes it. **`exists
$h{k};`, `keys %h;` and `values %h;` alone as statements are
refused**, as any statement that only has a value is, though perl is
silent about them (its `keys` there sets `each`'s place back, and
there is no `each`, D101). **`%h{...}` and `%a[...]`, perl's slices
of keys and values, stay out**, with no step named: the proposal
did not have them and nothing has asked. So do perl's `keys`
and `values` of an array, beside `exists` and `delete` of an
array's element, which the proposal left out: the four are for a
hash alone. **The index or the key of an element that is stored
to may not change a variable that a concatenation on the right
reads**, itself or through a sub it calls: `$a[$i = 2] = $i . "v"`
stores `2v` under perl, which joins the pieces as it stores, after
the index (T230). The compiler had printed `0v` since step 9, and
step 12a's breakages found it; refusing it is D57's answer to the
same habit of perl's. In the runtime **a hash is
the block an array is**, with its keys and values by turns in the
order stored and an index over them, so an array's own block is
three words longer than it was (88 bytes empty, from 64). Rejected:
building the lists without the freeze and adding the fault at 12b
(a program could change a hash under its own loop for one
sub-step, and perl's answer there is a freed value, D102); a
separate block for a hash (a second copy of the collector's
marking and sweeping, the cap's counting and the freeze, for 24
bytes an array).

**D105. A sub or a method with no signature takes any number of
arguments, each worked out, and sees none of them.** *(User: picked
the recommendation for both questions, 2026-11-26: "Q1 (a) and Q2
(a), go with your recommendations". It amends D17's first point and
D72's "a signature always".)* `sub f { ... }`, and when their steps
come `sub { ... }` (14) and `method m { ... }` (17). To perl such a
sub checks no count and has what it was handed in `@_`: `sub f {
return 7 } say f(1, 2, 3);` prints `7`, and `f($n++, $n++)` leaves
`$n` at 2. With `@_`, `$_[N]` and a `shift` or `pop` of no array
refused, as D17 has them, the sub cannot see its arguments, so
nothing it prints can differ from perl's: it is `sub f(@)`, a slurpy
parameter with no name, and is built as one. `()` is still the way to
say "takes none", with its fault. D17's reason for the rule was
`@_`, and the rule had been written wider than its reason: a sub
that ignores what it is handed is the callback everyone writes
(`sub { $count++ }`, which with `()` dies under perl itself), and
259 of the subs and methods in the parts of `stevan/grey-static` he
wants to port have no signature. D80's fault for a slice past the
end among a call's arguments holds whatever the sub is. Rejected:
the same as `()`, any argument a fault (one meaning for two
spellings, and a fault where perl runs on, at that callback);
refusing a call with arguments where the compiler can see one and
allowing it where it can't (two rules); deciding anonymous subs
apart, at step 14.

**D106 to D113. Step 13, references: each question answered with its
recommendation.** *(User, 2026-11-26, before the proposal was
written: "do not ask me questions, I will only agree with your
recommendations anyway." The recommendations are Fable 5.2's; each is
his to overturn. `PLAN.md`, step 13, has the text, the evidence and
what was rejected.)*
**D106.** Four sub-steps: 13a references to arrays and hashes and
elements through them, 13b the whole container through a reference,
13c references to scalars, 13d in a string.
**D107. Reading through undef, or through what is not there, is a
fault, everywhere; storing through it makes the container, as perl
does.** perl makes it on a read too, the variable itself included
(T231 to T233, T48 to T50), and for a whole container dies or makes
by the operator. A fault can be made to agree later and no program
changes. Rejected: perl's behaviour, for elements or exactly.
**D108. A dereference is an arrow, a postfix form (`->@*`, `->%*`,
`->$*`, `->$#*`, `->@[...]`, `->@{...}`) or braces round the whole
container (`@{ }`, `%{ }`, `${ }`, `$#{ }`).** Cut: every form with
no braces (`@$r`, `$$r`, `$$r[0]`; T246), a subscript after braces
(`${$r}[0]`), and the key-and-value slices (`%h{...}`, `->%[...]`).
It amends `SURFACE.md`, which had the last two In. Rejected: `@$r`,
`%$r` and `$$r` alone, though 237 of the 795 probes waiting use one:
a third spelling, and it can come in later.
**D109. Every walk over names has one more name, "what references
reach".** A read through a reference names it and what its chain
names; a store through one changes it; a variable whose reference is
taken anywhere is named and changed under it too. D76, D77, D57, D69
and T230's rule all use it (T235 to T238). Rejected for now: a guard
at run time, freezing what an expression read through until it is
done; it is the next move if the census shows the refusals bite.
**D110. `\` takes a named array, a named hash, or a `my` scalar
that is not a loop's variable.** A scalar whose reference is taken
lives in a cell. Cut: a reference to an element (T239), `\(LIST)`,
`\` before a slice, a value, a call or `my`.
**D111. In a string: a chain of subscripts after a variable, each
one D91 or D99 allows, and the whole-container forms.** Cut:
`"@{[ ... ]}"` and `"${\ ... }"`, code in a string.
**D112. A reference is true, defined, and `==` or `!=` to another
reference; any other use of one as a number or a string is a
fault** (D14; T241, T42). `ref` gives `ARRAY`, `HASH`, `SCALAR`,
`REF`, or the empty string.
**D113. Where a value may begin `{` is a hash and `[` an array;
where a statement may begin `{` is a block; what perl guesses at is
refused** (T243, T116, T175): `+{ ... }` or `return { ... }` says
a hash.

**D120 to D130. Step 16, strings: each question answered with its
recommendation.** *(User, 2026-11-26, of step 13 and standing for
this one, which another session's lead pulled ahead of steps 13 to
15 and handed to Fable 5.2 to build overnight in a worktree: "do not
ask me questions, I will only agree with your recommendations
anyway." The recommendations are Fable 5.2's, 2026-11-27; each is his
to overturn. `PLAN.md`, step 16, has the text, the evidence and what
was rejected.)*
**D120.** Three sub-steps: 16a `q`, `qq`, `qw` and heredocs, 16b
`sprintf` and `printf`, 16c `ucfirst`, `lcfirst`, `rindex`, `chomp`,
`chop`. Left as 16d, not proposed: the case escapes, `substr` with
four arguments, `reverse` of a string where one value is wanted,
`__FILE__` and `__LINE__`, POD, `fc`, `trim`.
**D121. `q`, `qq` and `qw` take one of the four bracket pairs, hard
against the word.** The string ends where perl's ends (brackets of
its kind nest; a backslash takes the next character with it); `q` is
single quotes with the bracket for the quote, `qq` double quotes with
D43 and D91 to D99, `qw` words between blanks. Cut: every other
delimiter, a blank before the bracket, and in `qw` a comma, a `#` or
a backslash (T261). Rejected: perl's whole rule (a `#` that is a
delimiter or a comment by the blank before it).
**D122. `qw(...)` is a bracketed list of strings and nothing else**
(T260): it can be sliced and repeated as `('a', 'b')` can, and is not
the brackets of a `for`, an `if` or a call.
**D123. Heredocs: `<<"END"`, `<<END`, `<<'END'`, each with `~` or
without**, the terminator a word hard against what is before it; one
on a line, and nothing after it on that line going past the end of
the line (T264); `'END'` keeps every character (T262); with `~` a
body line that does not begin with the terminator's blanks, and is not
empty, is refused (T263). Rejected: perl's quoted terminators with
blanks, the empty terminator, `<< "END"`, two on a line.
**D124. A format is a string literal with no variable in it** (T22,
T274), checked as the program compiles. Rejected: a format made as
the program runs.
**D125. The conversions are `%% %s %c %d %u %o %x %X %b %B %e %E %f
%g %G`, with the flags `- + 0 #` and a blank, a width and a
precision as digits or `*`.** Cut: `%i %D %U %O %F` (write the other
spelling), `%a %A`, `%n`, `%p`, `%v`, `%N$`, the size letters, a
flag, width or precision on `%%`, a width on `%c` (T277), a width or
precision of 2^31 or more (T271), an unknown or unfinished one (T270).
**D126. A format wants exactly as many values as its conversions and
stars take: one too few or too many is a fault** (T270; perl warns
`Missing argument` and `Redundant argument`).
**D127. A value is taken as its conversion wants it.** `%s` as `.`
makes a string, padded and cut in characters, `0` padding with zeros
(T268, T269); `%c` as `chr` takes a number; `%d` a whole number cut
toward zero, an Int or a fault (T265); `%u %o %x %X %b %B` the same,
a negative Int as its 64 bits (T266), a Num up to 2^64 as the whole
number it is; `%e %f %g` the double, and a negative-zero Num a fault
(T267, T79). undef is D48's fault.
**D128. `printf` is a statement, as `print` is, to stdout; `sprintf`
is a value, with brackets or without, as `join` is**, and its list is
a list as `join`'s is for D76 and D77.
**D129. `ucfirst` and `lcfirst` are named unary operators, as `uc`
and `lc`, and fault on a first character past ASCII; `rindex` is
`index` from the other end**, in brackets, two or three arguments.
**D130. `chomp` and `chop` are statements on one scalar variable**,
built as the variable assigned itself less its newline or its last
character, made a string as `.` makes one first (T272). Cut: their
values, arrays, hashes, elements, `chomp(my $x = ...)`, `$_`, `$/`.
Rejected: values (a change in the middle of an expression, for D76 to
learn).

**D24. A string is a sequence of Unicode code points, and the standard
streams are UTF-8.** *(User: picked from three options, 2026-11-24.)* `length`, `substr`, `ord` and `chr`
count code points. The source is ASCII, or UTF-8 with `use utf8`, as
`use v5.42` already demands. perl agrees when it's run with its
standard streams as UTF-8 (`-CSDA`), which is how the oracle ran it
until D39: now the file says so itself, with `use open`.
Strings are immutable in the runtime; since nothing can alias one
(D17), a program can't tell. Bytes, for binary files, are a later
proposal and a separate type. Rejected: perl's two kinds of string
with a hidden flag (the best-known cruft there is); bytes only, Chalk's
choice (`chr` above 255 stops at run time).

**D25. A value is two machine words: a tag and a payload.**
*(User: accepted as proposed, 2026-11-24.)* A 64-bit integer and a double fit in the payload unboxed;
a string, an array, a hash, code or an object is a pointer. Two words
pass in registers under both C compilers' calling conventions.
Rejected: one word with a tag in the low bits, the calculator's D4
(integers would be 63 bits and fault where perl is exact); NaN-boxing
(no room for a 64-bit integer).

**D26. Memory is collected by tracing: a precise, non-moving
mark-and-sweep, with its roots on a shadow stack the generated C
maintains.** *(User: picked from three options, 2026-11-24; step 7.)* With knobs from the start, as the
workbench asks: a collection at every nth allocation, freed memory
poisoned, a heap cap. No reference counts, so no `DESTROY` and no
`weaken`, both refused: a cycle is just collected. Cleanup at the end
of a scope is `defer`'s job, when a step proposes it. Rejected:
reference counting as perl does (it buys `DESTROY` at a known moment
and costs every assignment, and cycles leak); a conservative collector
from a library (no stress knob to find a missed root, and a dependency);
no collector, Chalk's state today.

**D27. A hash keeps its keys in the order they were first stored.**
*(User: accepted as proposed, 2026-11-24.)* perl's order changes with every run, so any order agrees
with perl (D14), and insertion order is the one that makes a run
reproducible without a seed. Rejected: perl's order for a fixed seed
(perl's hash function and its bucket layout would become the
language).

**D28. The runtime has no global state: everything hangs off one
context that every runtime function and every compiled sub takes as
its first argument.** *(User: accepted as proposed, 2026-11-24.)* Concurrency is planned (D5), and the
likely shape is tasks that share nothing, each with a heap of its own
(a64-slight's shape). That is cheap if the heap, the
collector's roots and the fault path were never global, and a rewrite
if they were. Nothing else about concurrency is decided.

## Compiler

**D29. The compiler's passes: lexer, parser, resolver, checker, code
generator; one table of names.** *(User: accepted as proposed, 2026-11-24.)* Each is a file under
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
*(User: accepted as proposed, 2026-11-24; retires the workbench's D7
for this language.)* The
workbench kept compile errors in unit tests because a calculator has
few. Here the refusals are half the language's definition, so a test
of kind `refused` (D10) is a `.pl` that must not compile, with the
compiler's message as its `.expected`. Unit tests stay for what a
golden test can't reach: token positions, the tree.

**D31. The generated C is straight-line: one statement per operation,
each result in a temporary.** *(User: accepted as proposed, 2026-11-24.)* C doesn't order a call's
arguments and clang stops at 256 nested brackets; the workbench met
both (its D25 and D26, and the limit that's still open there) and
called this shape "also right". Starting with it costs nothing here.
