# The review of step 8's proposal, subs

2026-11-25, by a reader who didn't write the proposal (`docs/PLAN.md`,
"8. Subs"), before anything was built. The question was the rule for a
large step: a program with a sub in it that the proposal accepts, that
runs without a fault, and prints what perl 5.42.0 doesn't; or one it
accepts that perl refuses or warns about.

Everything below about perl was run under `/opt/perl-5.42/bin/perl`
(5.42.0), plain, from a file that begins `use v5.42;`. The programs
cited are in this directory, named by finding, and `outputs.txt` has
perl's stdout, stderr and exit status for every one of them. Nothing
of step 8 exists, so "the proposal would" is a reading of its text and
of the obvious build (straight-line C, operands left to right, a
variable read when its operator runs, D14).

**Four ways to be WRONG were found (A1 to A4), three programs the
proposal's wording accepts and perl refuses (B1 to B3), four sentences
about perl that are not so and one true but for one shape (C1 to C5),
and eight holes in the test plan (D1 to D8).** A1 and A2 are WRONG
under any reading of the text. A3 and A4 are WRONG under the reading
the text most easily gives, and one sentence each closes them. Q1's count, the pragma, T134, the late
reads, the names and "a value has no past" all held (E).

## A. WRONG under the proposal as written

### A1. `(...) x N` is a list, and a call can now count it

`A1-list-repeat.pl`:

```perl
use v5.42;
sub g($p = "d") { return "[" . $p . "]" }
sub cnt($p = "-", $q = "-", $r = "-") { return $p . "," . $q . "," . $r }
sub three() { return ("a") x 3 }
sub last2($x) { ($x) x 2 }
my $n = 0;
say g(("a") x $n);
say cnt(("a") x $n, "z");
say cnt(("a") x 2);
say cnt(1 ? ("a") x 2 : "b");
say cnt(0 || ("a") x 2);
say cnt(three());
say cnt(last2("k"));
my $s = three(); say $s;
```

perl: stdout

```
[d]
z,-,-
a,a,-
a,a,-
a,a,-
a,a,a
k,k,-
aaa
```

stderr empty, exit 0.

In an argument list, in a `return` and as a sub's last statement, a
bracketed left operand of `x` repeats a *list*: `("a") x 0` is no
argument at all (so `g`'s default is used, and `"z"` becomes the
*first* argument), `("a") x 2` is two arguments, and a sub that says
`return ("a") x 3;` gives three values to a list and `aaa` to a
scalar. It reaches through `? :` and `||`, as T101 found for `say`.

The proposal: "A sub returns one value under all three, with two
exceptions that the flag is for: a sub with no value (Q4) ... and a
sub that returns nothing (Q5)." and "the arguments are expressions
with commas between". Today `(...) x N` is refused only "as the whole
argument of `say`" (T101), because joined output couldn't tell; a
scalar assignment takes it (`my $y = ($x) x 3;` compiles today and is
`111`). So the obvious build hands `g` the one string `""` and prints
`[]`, `,z,-`, `aa,-,-`, `aa,-,-`, `aa,-,-`, `aaa,-,-`, `kk,-,-`: seven
lines WRONG, no fault. (With fewer parameters perl dies of `Too many
arguments` where the build prints.)

Way out: refuse. T101's refusal, with its reach through brackets,
unary plus, `? :` and `|| && //`, in three more places: an argument of
a call, the expression of a `return`, and a last statement that is a
value. (Agreeing needs step 10's lists. A default, `sub d($x = ("a")
x 2)`, is scalar and `aa` in perl, and can stay.)

### A2. A `//=` or `||=` default runs before the later arguments are copied

`A2-default-order.pl`:

```perl
use v5.42;
my $g = 1;
sub bump() { $g = 9; return 5 }
sub f($x //= bump(), $y = 0) { return $x . "," . $y }
say f(undef, $g);
$g = 1;
sub h($x ||= bump(), $y = 0) { return $x . "," . $y }
say h(0, $g);
$g = 1;
say f(undef, $g + 0);
```

perl: stdout

```
5,9
5,9
5,1
```

stderr empty, exit 0.

perl doesn't copy the arguments "as the sub begins": it copies each
one when it reaches that parameter, left to right, and a `//=` or
`||=` default is worked out in between. So a default that calls a sub
which changes a file variable changes what a *later* parameter gets,
when that argument is the variable itself. (`$g + 0` is a value, and
stays 1: the same line D14 draws.)

The proposal: "a call opens a frame, copies its arguments into the
frame's first slots before anything can allocate", "perl passes the
variable and copies it as the sub begins", and "A default is worked
out at each call that needs it, left to right, after the parameters
before it are set". Read together: all arguments copied, then
defaults. That prints `5,1` twice. WRONG. With `=` alone it can't
happen (a default runs only for a missing argument, and those are
last), which is why T1's rows didn't find it.

Way out, in order: agree (for a parameter that follows a `//=` or
`||=` default, an argument that is a variable is read after that
default has run: a second read of the file variable, for those
parameters only); or refuse a `//=` or `||=` default that calls a sub
when a parameter follows it; or refuse, by Q3's walk, only when the
default can assign a file variable.

### A3. A last statement under a modifier is worth its test

`A3-modifier-last.pl`:

```perl
use v5.42;
sub a($x, $c) { $x * 2 if $c }
sub b($x, $c) { $x++ if $c }
sub c($x, $c) { $x = 7 unless $c }
sub d($x, $c) { a($x, 1) if $c }
say "[" . a(4, 1) . "]";
say "[" . a(4, 0) . "]";
say "[" . a(4, "") . "]";
say "[" . b(4, 0) . "]";
say "[" . c(4, 3) . "]";
say "[" . d(4, 0) . "]";
a(1, 1); a(1, 0);
```

perl: stdout

```
[8]
[0]
[]
[0]
[3]
[0]
```

stderr empty (no `Useless use` for `$x * 2 if $c` as the last
statement, called void or not), exit 0.

The proposal: "A sub's value, when it ends without a `return`, is its
last statement's, if that is an expression (D18): an assignment, a
step, a call, a `my`, or a value alone", and of a call: "It is an
expression, and it is a statement: `add(5);`, with any modifier."
Q4(a) speaks of modifiers only for `return`. An assignment, a step or
a call under `if` or `unless` is still "an assignment, a step, a
call", and a build that takes it so gives undef (or the statement's
value) where perl gives the test's: `c(4, 3)` is 3. Whatever it gives
when the test fails, short of a fault, is WRONG unless it is the
test's own value.

Way out: say it. A last statement with a modifier has no value, like
an `if` (a fault if the value is used, none if the call was void);
and a value alone is a statement only as a last statement *with no
modifier* (perl is silent about `$x * 2 if $c;` there, but it has no
use once it has no value: refuse). Agreeing is possible (the
expression's value if the test passed, the test's own if not), and is
T19 decided the other way.

### A4. Context goes through brackets, a unary plus, `and` and `or`

`A4-context-brackets.pl`:

```perl
use v5.42;
sub none() { return; }
sub show($p) { return defined($p) ? "[" . $p . "]" : "U" }
sub cnt($p = "-", $q = "-") { return show($p) . show($q) }
say cnt(none());
say cnt((none()));
say cnt(+none());
say cnt((1 and none()));
say cnt((0 or none()));
say cnt(1 && none());
say cnt(none() || none());
say cnt(1 ? none() : 0);
say cnt((none()), "z");
my $v = (none());
say show($v);
```

perl: stdout

```
[-][-]
[-][-]
[-][-]
[-][-]
[-][-]
[-][-]
[-][-]
[-][-]
[z][-]
U
```

stderr empty, exit 0.

The proposal names where list context is ("an argument of `say`,
`print` or another call") and what passes a context on ("`return
f();` and a last statement `f()` ...; so do the arms of `? :` and the
right side of `||`, `&&` and `//`"). Brackets, a unary plus, and the
right of `and` and `or` pass it on too, and are not named. If the
flag is set by "the argument *is* a call", then `cnt((none()))`,
`cnt(+none())` and `cnt((1 and none()))` call `none` scalar, get
undef in silence (which "is agreed with"), and hand `cnt` one
argument: `U[-]` where perl has `[-][-]`, and `U[z]` where perl has
`[z][-]`. WRONG, and Q5's fault never fires. (The left of `||` and
`//` is scalar in perl: `cnt(none() || none())` is no argument
because the *right* one is.)

Way out: the sentence. Context is passed down through brackets, a
unary plus, both arms of `? :`, and the right operand of `|| && //
and or`, from wherever they stand: an argument, a `return`, a last
statement, `say`'s argument, and (scalar) the right of `=`. Then Q5's
fault covers all of the above. `xor`, `not`, `!` and the left of
every operator are scalar (`cnt((1 xor none()))`, `cnt(!none())` and
`cnt((not none()))` are each one argument, `1`, in perl).

## B. Accepted by the proposal's wording, refused by perl

### B1. `say((f (1)));` before `sub f`

`B1-say-bracket-blank.pl`:

```perl
use v5.42;
say((f (1)));
sub f($x) { return $x + 1 }
```

perl: stdout empty; stderr

```
Unquoted string "f" may clash with future reserved word at B1-say-bracket-blank.pl line 2.
syntax error at B1-say-bracket-blank.pl line 2, near "f ("
Execution of B1-say-bracket-blank.pl aborted due to compilation errors.
```

exit 255. With the `sub` first (`B1-say-bracket-blank-after.pl`) it
prints 2.

The proposal: "After `say` or `print`, a call's bracket touches its
name (T136). Elsewhere a blank or a new line may come between, as
perl has it either way round." The file-handle guess is made for the
first word of `say`'s argument *through any number of opening
brackets*: `say(f (1));`, `say (f (1));`, `say((f (1)));`, `say ((f
(1)));`, `say(((f (1))));`, `say((f (1)) + 1);`, `say((f (1) + 1));`,
`say( (f (1)));`, `say(( f (1)));`, `print(((f (1))));`, `say((f`
newline `(1)));`, `say f (1) if $c;`, `say((f (1))) if $c;`, a tab or
a comment for the blank: none compiles before the definition (22 of
22 shapes). Not first, it is fine either way round: `say(+(f (1)));`,
`say(!(f (1)));`, `say(-(f (1)));`, `say("" . (f (1)));`, `say(1 * (f
(1)));`, `say 1 + f (1);`, `say 0 || f (1);`, `say g(f (1));`, `my $r
= (f (1));`, `my $r = (f` newline `(1));`, `if (f (1)) {...}`,
`return (f (1));` (34 of 34).

Way out: refuse, by the rule T111 already has for a variable (today
`say(($x -1));` is refused and `say(($x) -1);` is not): a call that
is the first thing after `say` or `print`, behind any opening
brackets, has its bracket touching its name.

### B2. `v1_0` is a version string too

`B2-vstring-underscore.pl`:

```perl
use v5.42;
say v1_0();
sub v1_0() { return 1 }
```

perl: stdout empty; stderr

```
syntax error at B2-vstring-underscore.pl line 2, near "v1_0("
Execution of B2-vstring-underscore.pl aborted due to compilation errors.
```

exit 255. With the `sub` first (`B2-vstring-underscore-after.pl`), 1.

The proposal refuses "`v` and digits (T136)". Called before its
definition, every name that is `v`, a digit, and then digits or
underscores fails: `v1_`, `v12_`, `v1_0`, `v1__2`, `v1_2_3` (all 110
three-character names `v[0-9][0-9_]`, and the longer ones tried).
`v_1`, `v1a`, `v1_a`, `v1e5`, `v1x2`, `vv1`, `V1` are simply called.
(`step8-names.py`'s own docstring lists `v1_0` among its twelve; the
proposal's sentence lost the underscore.)

Way out: refuse `/^v[0-9][0-9_]*$/`.

### B3. Seven keywords are in neither list the evidence used

`B3-keyword-for.pl`:

```perl
use v5.42;
sub for($p) { return $p + 10 }
my $r = 1 + for(3);
say $r;
```

perl: stdout empty; stderr

```
syntax error at B3-keyword-for.pl line 3, near "+ for"
Execution of B3-keyword-for.pl aborted due to compilation errors.
```

exit 255.

The proposal refuses "any name in perl's own table (every keyword,
function and quote operator ...)", and rests on `step8-names.py`:
"for all but 59 the sub is simply called, and each of the 59 is one
of those". That script leaves out what `Pod::Functions` lists and
adds a hand list. Of the 266 words in perl's keyword table
(`regen/keywords.pl` of the 5.42.0 source), 42 are not in
`Pod::Functions`, and seven of those are not in the script's list
either: `else elsif for foreach unless until while`. Each was run
(with `perl -c`, since some would loop): none compiles as a sub's
name called as `1 + NAME(3)`. So it is 66 of 3,455, not 59 of 3,448,
and a `names.ts` built from `Pod::Functions` plus the 59 would let
`sub for` through. If `names.ts` takes the keyword table whole, this
is only a correction to the sentence.

Way out: build the table from perl's own keyword list, with a check
that every word of it is refused as a sub's name.

## C. Statements about perl that are false or imprecise

- **C1. "A sub returns one value under all three, with two
  exceptions"** There is a third: `return (EXPR) x N;` and a last
  statement `(EXPR) x N` (A1).
- **C2. "perl passes the variable and copies it as the sub begins"**
  (and T1's "an argument is read late"). It copies each argument as
  its parameter is reached, and `//=` and `||=` defaults run in
  between (A2). True as written only of signatures whose defaults are
  all `=`.
- **C3. "`-e(2)` is a file test ...: undef, in silence, for 26
  one-letter names"** `-t(2)` is defined, the empty string
  (`C2-filetest-t.pl`: `d[]` for `t`, `u` for `e`). And it is not
  only a leading minus: `- -e(3)` is 0 with a warning, `!-e(3)` is 1,
  `(-e(3))`, `id(-e(3))` and `-e (3)` are undef, in silence, and `$q
  -e(3)`, `id(26)-e(3)`, `($q)-e(3)`, `26-e(3)` and `"26"-e(3)` don't
  compile (`D5-minus.pl`, `D5-minus-binary.pl`; all 26 letters, both
  orders). "A minus hard against a one-letter name is refused" is
  right if it is the lexer's rule: a `-`, then one letter and no
  second, wherever it stands. `- e(3)`, `-(e(3))` and a `-` with the
  name on the next line are -13 for all 26.
- **C4. "perl agrees in the cases tried"** (the fault's line). It
  does, in every shape tried but one (`C4-lines.pl`, nine statements
  that run over lines): a sum with a call in its first, second or
  last line; a last statement that is a value; a default (the line
  the default starts on); a `while`'s test and a `for`'s third part
  (the loop's line); and the arity death of a four-line call (`Too
  few arguments for subroutine 'main::two' (got 1; expected 2) at
  C4-lines.pl line 36.`, the statement's first line). The one:
  `return` alone on a line with its expression on the next. perl
  names the *expression's* line (`... in concatenation (.) or string
  at C4-lines.pl line 7.`, the `return` being on line 6), and D34's
  rule names the `return`'s. A fault's line is the language's own
  (D34), so nothing is WRONG; step 15 inherits it for `die`.
- **C5. "`v` and digits"** (B2) **and "each of the 59"** (B3).

Run and true, for the record: required parameters first; T138;
`return (5) + 1`; T140's values (`[0]` after an `if`, 1 after `say`,
an empty string after a `while` and after a `for (;;)`); T141; Q1's
98/99 and 150/250 (and `ev(197)` is silent, `ev(198)` warns: 199
deep); the pragma at the top silences every such warning and nothing
else (`E-pragma.pl`: `Useless use`, `uninitialized` and `isn't
numeric` still come); written *before* `use v5.42;` it silences
nothing; an identifier of 251 characters is a sub's name and 252 is
`Identifier too long`; two subs of one name warn `Subroutine ff
redefined` and the second wins; a missing sub dies when reached,
after the output before it; arity is checked after every argument has
run (three `say`s, then `Too many arguments`); a million deep took
0.6 seconds.

## D. Holes in the test plan

- **D1. Nothing separates "all arguments copied, then defaults" from
  perl's order** (A2). Whatever A2's way out, `f(undef, $g)` with a
  `//=` default that changes `$g` is a test, and "the later arguments
  copied before a `//=` default runs" a mutation.
- **D2. A void call still works its value out.**
  `D2-void-evaluates.pl`: `sub v($x) { $x * 2 } v($n);` with `$n`
  undef warns `Use of uninitialized value $x in multiplication (*)`,
  `w($n)` with `return $x . "a"` warns in the concatenation, and
  `u(1)` with a last statement `"abc" + $x` warns `Argument "abc"
  isn't numeric`, all called void. A build that skips a last value
  or a `return`'s expression when the flag says void runs in silence
  where perl warns. No listed test or mutation sees it: a fault test
  of each, called as a statement.
- **D3. `my $x OP= EXPR;` after a call that set `$x`.** Today's
  compiler takes `my $x += 10;`, `my $s .= "a";` and `my $d //= 10;`.
  `D3-my-compound.pl`: with a sub called first that sets each, perl
  prints `11`, `qa`, `1`. T134's test has `my $x;` only; a build that
  stops storing undef for the plain `my` and keeps "undef, then the
  operator" for these prints `10`, `a`, `10`.
- **D4. Q3's walk.** `D4-rows.pl`, each `b-c` (or `b-2`) in perl and
  so each to be refused: the changing call inside another call's
  argument (`$x . "-" . id(ch())`), inside a builtin's or an
  operator's (`(1 + length(ch()))`), reached only through a *default*
  (`dflt()` with `sub dflt($p = ch())`), reached through a second sub
  (`deep()`); and the row itself inside an argument, a `return` and a
  default. The walk needs a test where two subs call each other (it
  must end) and one where the assigning sub is defined after the row.
  And one thing a test must not assume: `"<" . ($x . "-") . ch()` is
  `<a-c` in perl where `($x . "-") . ch()` is `b-c`, so "perl reads
  late" is not a rule to write expected output from; the refusal is.
- **D5. The minus rule's positions** (C3): refusal tests for `- -e(`,
  `!-e(`, `(-e(`, an argument `-e(`, `-e (`, `$q -e(`, `)-e(`.
- **D6. The `say` rule's positions** (B1): refusal tests through one,
  two and three brackets, with a new line and with a modifier, and
  `same` tests for the shapes that are fine.
- **D7. The flag in the positions the proposal doesn't name.** A
  call as a `for`'s first or third part and under a modifier (`f() if
  $c;`, `f() while g();`) is void to perl; a `while`'s test and a
  modifier's are scalar. A sub with no value (Q4) called in a `for`
  part should not fault; a test for each. And A4's shapes, whichever
  way they go.
- **D8. The count for a sub, from a default and across re-entry.**
  `E-recursion-1.pl`: `d(98)` five times over, three of them in a
  loop, is silent (99 open, again and again); and a sub whose
  recursion goes through its own *default* (`sub e($n, $v =
  e2($n))`) warns at 100 open calls like any other, perl naming the
  line of the call inside the default. `E-recursion-2.pl`: `self(98)`
  with the recursion in the default is silent where `self(99)` warns;
  and a sub that reaches 100, comes back and goes down again warns
  each time it reaches 100. The listed mutation ("the count ... not
  taken down on the way out") needs the way out to be a `return` from
  inside a loop and the fall off the end as well as a plain `return`.

## E. What held

- **Late reads, 53 expressions** (`E-late-reads.pl`): a call as an
  operand of `+= .= x= ||= &&= //= **= -=`, of `+`, `<`, `? :`, beside
  `$x`, `($x)`, `+$x`, `-$x`, `$x++`, `++$x`, `($x += 1)`, `($x = 5)`,
  `(1 ? $x : 0)`, `($x || 0)`, `($x && 1)`, `($x // 0)`; and 28
  argument shapes against a later argument that changes the variable.
  Every one is what D14's list of "the variable itself" gives:
  `two($x, set9())` is `9,2`, and so are `($x)`, `+$x`, `$x = 4`, `$x
  += 4`, `++$x`, `$x ||= 3`, `$x .= "z"` and what `? :`, `||`, `//`,
  `&&` give; `$x + 0`, `$x . ""`, `$x++`, `-$x`, `!$x`, `$x x 2`,
  `length($x)`, `id($x)` and `my $w = $x` are `1,2`. A returned value
  is a copy through `? :`, `||`, `//`, brackets, a unary plus, an
  assignment and `++` as the last statement (10 shapes). Loop tests
  and `for` parts that call a sub which steps the loop's variable: 6
  shapes, as D14 has them.
- **Signatures, 31 shapes**: `$`, `$=`, `$ = 5`, `$=5`, `$//=5`, `$
  //= 5`, `$||=5` all compile and take an argument (the proposal
  takes the first three; the rest it may refuse); `$x =` and `$x //=`
  with nothing after are `Optional parameter lacks default
  expression`; a comment or a new line inside a signature, a blank
  before it, a trailing comma; a default that assigns a file
  variable, that steps an earlier parameter (`sub f($x, $y = $x++, $z
  = $x)` is `212`), that assigns one (`99`), that calls its own sub,
  that holds `? :`, `||`, a string with `,` and `)` in it; a default
  naming a later parameter, or its own, with no file variable of the
  name doesn't compile; `//=` and `||=` by value (`f(undef, 0)`,
  `f(0, "")`). All as "left to right, after the parameters before it
  are set" says, but for A2.
- **What a sub is worth, 24 shapes**: `return` with `-`, `- `, `!`,
  `+`, `not`, `||`, brackets and `? :`; `return` on one line and its
  value or its modifier on the next; `return $x = 5`, `return $x++`,
  `return my $y = $x`; code after a `return`; a last `my $x;` (one
  undef, to a list too); a last compound assignment of each kind; a
  last `--$x` and `$x--`; a last call. 18 kinds of value alone as the
  last statement, called void, are silent. All as the proposal has
  them. `return $x and $y;` and `return $x xor $y;` warn as `or` does
  (refused already, by "anything else").
- **T134, 20 programs**: `my $x = setx();` with `setx` writing `$x`
  is 7; three calls before `my $x;` and one after give 3; a sub can't
  see a `my` in a top-level `if`'s test, a `for`'s first part or a
  bare block (perl doesn't compile it); a block's `my $x` at the call
  doesn't hide the file's from the sub; a `my` in a loop's body at
  the top level is not the file's variable of that name; a sub's own
  `my` is new at each call and at each depth. "Every file variable is
  undef as the program starts and its `my` stores nothing" is perl,
  with D3's three forms to remember.
- **Q1**: the count is per sub, at the 100th open call, at the call's
  entry, every time the depth reaches 100 again; a call from a
  default counts; `no warnings 'recursion';` after `use v5.42;`,
  before or after `use utf8;` and `use open`, silences all of it and
  nothing else. No program was found where a fault at the 100th open
  call would fire and perl is silent, or the reverse.
- **Names** (`E-sweep.py`): 213,685 names (every name of one to
  three characters that `Pod::Functions` doesn't list, less 33 that
  `step8-names.py` had found: its keywords and `v0` to `v9`), each
  defined and called in 33
  positions it didn't try, definition first and calls first: hard
  against a binary minus, a unary minus, `<`, `/`, `*`, `%`, `?`,
  `:`, `.`, `!`, `=` and `{`; before a `:`; right of `x`; in all
  three parts of a `for`; in a `while`'s and an `until`'s test; with
  a blank and with a new line before the bracket; after `print`;
  after `say` with `+ 1` behind; as two arguments; inside its own
  argument; inside `defined(...)`; after `length` with no brackets;
  under `if` and `unless` modifiers; after a block, on the same line
  and the next; on both sides of `==`, `eq`, `lt`, `<=>`, `.`, `||`,
  `&&`, `//` and in every part of `? :`. Besides the 26 file-test
  letters (the two minus positions only), `for`, and the 110
  `v[0-9][0-9_]` (calls first only), every name is simply called in
  every position. 78 longer names the same way, in the first 24
  positions: only the `v` ones of B2 and `__SUB__`, `__FILE__`,
  `__LINE__`, `__PACKAGE__` (in perl's table) fail. `STDERR`,
  `STDOUT`, `STDIN`, `ARGV`, `DATA`, `ENV`, `_`, `__`, `e1`, `x3`,
  `x10`, `xx`, `inf`, `nan`, `CORE`, `any`, `all`, `defer`, `class`,
  `field`, `method` are called.
- **A value has no past** (`E-past.py`): 63 values (the edges of
  T92, T93, T130, D40's string shapes, booleans, 2^53 and 2^63 from
  both sides), each fresh and after nine kinds of use, through nine
  routes (argument and return, last statement, two subs deep, made
  inside the sub, an expression as argument, as `return`, as last
  statement, and used only inside the callee), then 35 operations on
  the copy: 136,710 comparisons of perl against perl with the same
  value assigned directly. None differs. A value used as a number
  inside a callee leaves the caller's variable as it was.

## Not checked

The generated C, the frame, the collector's roots and Q2's numbers:
nothing is built. Q3(a)'s walk was read, not run. clang, the
sanitizers and the Mac. Names of four characters and more, beyond the
78. `E-sweep.py` writes its temporary files into the directory it is
run from and wants `ulimit -v` set: a sub named for a loop keyword,
called blind, once filled the memory of the machine it ran on (those
words are not in its list now).
