### 14. Closures

Referee: perl. Size: large.

**Proposed 2026-11-27, by Fable 5.2, under Stevan's standing
instruction of the night before ("do not ask me questions, I will
only agree with your recommendations anyway"): each question is
answered with its recommendation, as D160 to D165, his to overturn;
D166 is what its review changed.**
This file is the proposal until step 13 is built; its builder moves
it into `PLAN.md` under "### 14." and its claims into
`briefs/claims.py` (the programs under "Claims" at the end, each run
under perl 5.42.0 when this was written, 2026-11-27). The outline it
replaces said: anonymous subs, captured variables, `my sub`,
`__SUB__`, calling through a reference, `state`; a captured variable
lives in a cell on the heap; decides a closure over a `foreach`
variable (D17, T11). About 100 programs were run.

**The census**: 185 of the refused probes have an anonymous sub and
185 a call through a reference; 5 take `\&name`, 3 use `state`, none
`my sub` or `__SUB__`. Most also need references (step 13).

#### The picture

**An anonymous sub is a value: its code, and the variables it uses
from outside.** Step 13c gave a variable whose reference is taken a
cell on the heap; a variable an anonymous sub uses from an enclosing
sub or block is the same thing, and the sub's value holds the cell.
An array or a hash is already a block on the heap, and the sub's
value holds that. So the runtime gains one kind of value (a block
with a C function and a row of what was captured) and one call.

What is new for the rules is that **a call through a reference does
not know its sub**. Everything the compiler works out by a sub's
name (what it can change, for D69, D76, D77 and D109; whether it
gives a list, for D18) has to be answered without one. The world is
closed (D20), so the answer exists: **such a call is, to every walk,
a call of any sub a reference can be to** (D163).

#### The language at step 14

- **`sub (PARAMETERS) { ... }`** and **`sub { ... }`** where a value
  may begin: a sub with no name, by step 8's rules for a body
  (signature, defaults, `return`, the value of a last statement,
  D105 for no signature). It may stand anywhere: in a sub, a block,
  a loop, another anonymous sub, a list, a hash's value. A statement
  may not begin with it.
- **It may use every variable in scope where it is written**, and
  uses the variable, not its value (the same `$x`, read when the sub
  runs and stored to if the sub stores): `my $x = 1; my $f = sub {
  $x }; $x = 2;` and `$f->()` is 2. A `my` reached again is a new
  variable (step 13c), so each closure made in a loop or in a call
  has its own.
- **`EXPR->(ARGUMENTS)`** calls it, by the rules of a call with
  brackets: a wrong count is a fault after the arguments have run,
  perl's context is handed on, an array among the arguments
  flattens. The arrow may be left out after a subscript or a call's
  brackets: `$h{add}(1, 2)`, `$f->(1)(2)`. `$f(1)` is not Perl.
  Calling undef is `undef where a reference is wanted`; anything
  else that is not a sub's reference, `not a reference to a sub`.
- **`\&name`** is a reference to a named sub of the program; `\&`
  before a name the program does not have is refused.
- **`__SUB__`** inside an anonymous sub is that sub's own value,
  for recursion without a cycle through a variable.
- **As a value** it is step 13's reference (D112): true, defined,
  `==` and `!=` to another, `ref` gives `CODE`, and a fault as a
  number or a string. **`sub` gives a new value each time it is
  reached if it uses any variable declared outside it, the file's
  too, and one value for the whole run otherwise**, which is what
  perl's `==` shows (D161).
- **A closure over a `foreach` variable** (D162, T11): the sub gets
  the variable's value in a cell of its own, and **every array and
  hash the loop froze stays frozen for good from the moment the sub
  is made**: `an array was changed while a foreach is over it` if
  the program ever stores to one again. To perl the variable is the
  element, so the sub would see a later store; with the store a
  fault, a copy cannot be told from it. A loop whose list names a
  scalar variable directly (`for my $x ($p, $q)`) may not have its
  variable captured: a scalar has no freeze. **`$_`, `$a` and `$b`
  are not seen inside an anonymous sub** written in their block: to
  perl they are globals read when the sub runs (T15's kin).
- **Refused** (D165): `&$f(...)`, `&{$f}(...)`, `->&*` (D21);
  `sort $f LIST` (step 10's rule); `last` and `next` to a loop
  outside the anonymous sub (perl warns `Exiting subroutine`); a
  prototype or an attribute; `wantarray`, `@_` (D17, D18); a named
  sub inside a block stays refused (T31). **Not built at this
  step**: `state` and `my sub` (three probes and none); they stay
  Later, to be proposed when something wants them.

#### What perl does that the obvious build gets wrong

- **A closure sees the variable, not a copy**, and two closures
  over one variable share it; one made in a loop over `my $j`
  inside the block has its own each time round, and one over a
  C-style `for`'s variable shares the one variable (`3,3,3`).
- **A closure over a `foreach` variable sees a later store to the
  array** (T11), through `values` too; not through `keys`, a range
  or a literal list.
- **`sub { $_ }` in a `map` or a `for` reads `$_` when it is
  called**: undef, later.
- **Identity**: `sub { 1 }` in a loop is one value every time
  round; `sub { $g }`, with `$g` the file's, a new one.
- **A sub called through a reference still reads its arguments
  late** and still returns by the caller's context: `my $c =
  $f->();` with `return (1, 2, 3)` is D18's fault.
- **`$total + $step->()`** sees what `$step` did to `$total`
  (D14), and `($x, $bump->())` has the new `$x`: D76's refusal,
  which needs D163 to see it.
- **`last` inside an anonymous sub leaves the caller's loop**, with
  a warning.

#### The decisions, each the recommendation

- **D160: one step, closures and calls through a reference; `state`
  and `my sub` not built.** Rejected: all four now (two features no
  probe needs, each with rules of its own: `state` is one variable
  per closure value, and a `my sub` cannot call itself by name).
- **D161: a captured scalar lives in a cell, a captured array or
  hash is held by its block, and a closure's value is its code and
  that row. New each time it is reached if it uses any outside
  variable, else one value.** Rejected: copying values in (WRONG
  at once); a fault on `==` between two sub references (perl's
  answer is fixed, so it is followed, D14).
- **D162: a closure over a `foreach` variable takes a copy, and
  what the loop froze stays frozen for good.** Rejected: refusing
  it (the outline's "too common an idiom"; `my $y = $x;` first
  still works and freezes nothing); perl's alias (an element would
  have to be a cell); freezing until the closure is collected (the
  moment would depend on the collector).
- **D163: a call through a reference is a call of any sub a
  reference can be to**: every anonymous sub, and every named sub
  that has a `\&name` somewhere. Its changes are the union of
  theirs; it may give a list if any of them may. Rejected:
  following the values (no types yet); refusing such a call inside
  an expression.
- **D164: calling what is not a sub's reference is a fault**, by
  D107's two messages.
- **D165: the refusals above.**

#### Tests

A model, `t/models/clo.py`, with cells written out by hand (Python's
own closures bind late and would hide the loop cases): counters,
shared variables, closures in each kind of loop, nested closures,
dispatch tables, recursion both ways, context, defaults; the oracle
check holds perl to it. A fault test each for a wrong count, undef
called, a non-sub called, the list-where-one-value fault through a
reference, and the frozen-for-good array (by `push`, by a store, by
assignment; through `values`; not through `keys`). Refusals from a
table by hand. The collector: a closure that is the only thing
holding its cell, under the stress knob; a cycle of a closure and
its own variable, dropped under the cap.

#### How it moves the other files

`SURFACE.md`: anonymous subs, closures, `->( )`, `\&name` and
`__SUB__` to In; `my sub` and `state` stay Later; `&$f()` is Cut
already. `DIFFERENCES.md` gains: an array stays frozen after a
closure took its loop's variable (a guess: accident, rarely); `$_`
is not seen in an anonymous sub (habit, sometimes); D163's wider
refusals (a guess: medium, sometimes); no `state` yet. The census:
its step-14 rows go, and the account says what moved.

#### What the review found

An adversarial review (2026-11-27, a reader who did not write this,
with perl; `briefs/step14-review/`, 325 programs) found **five ways
to be WRONG**, one shape perl refuses, and six gaps. **D166** is what
is done about each, the builder's defaults under the same standing
instruction. Where this section and the text above differ, this
section is right. All 27 claims held.

- **perl works out the sub to call after the arguments** (T370):
  `fn()->(arg());` runs `arg` and then `fn`; `$fs[$i]->($i = 1)`
  calls `$fs[1]`; `$f->(($f = $g) ? 1 : 0)` calls `$g`. **So a call
  through a reference is generated as its arguments, then the whole
  of what stands before the arrow (variable, subscripts, inner
  calls), then the check that it is a sub, then the call; and in
  every walk what stands before the arrow is the last part of its
  call.** Arguments that are variables stay places until the sub
  copies them (`mk()->($x)` sees what `mk` did to `$x`). The value
  called sits in a slot for the whole call, so that a closure which
  drops the last reference to itself as it runs is not collected
  under it.
- **A loop's variable can be a scalar through more than its name**
  (T371): through `? :`, `||`, `&&`, `//`, brackets, a unary plus,
  `scalar()`, an assignment, `++$p`, `grep`, `sort`, `reverse`, a
  list slice, `(...) x N`, `->$*` and `${ }`, and an inner loop's
  variable through `grep { 1 } $x`. **The capture is refused when
  the loop's list names any scalar variable anywhere (D77's set, an
  outer loop's variable and a parameter among them), or reads
  through a reference to a scalar.**
- **A captured loop variable is still the loop's variable** (T372):
  read-only in every sub written inside the loop (to perl a store
  from the closure lands in the array), and a store through it that
  would make a hop is T250's fault.
- **A list assignment as a sub's last statement** (T257) gave undef
  in the compiler as it stood, where D78 says it has no value: a
  WRONG since step 9, fixed with step 13a.
- **`\&name->()` is `\(&name->())` to perl** (T373), and
  `\&name(1)` a call: `\&name` is refused before `->`, `(`, `[`
  or `{`; `(\&name)->(...)` says it.
- **`name()()` and `(EXPR)(...)` do not compile** (T374): the arrow
  may be left out only after a subscript, or after the brackets of
  a call through a reference.
- **`__SUB__`** is refused outside an anonymous sub (at the top
  level perl gives undef, in a named sub that sub); in a `map`,
  `grep` or `sort` block inside one it is that sub.
- **"Uses a variable from outside" counts uses inside nested
  anonymous subs** (T375): `sub { sub { $g } }` is new each time.
- **A parameter is a cell before its defaults run** when a default's
  closure uses it (`sub g($x, $f = sub { $x }) { $x = 9; return
  $f->() }` is 9).
- **`my $f = sub { $f->() };` does not compile** (T376; D55 has it:
  a variable is seen from the next statement): the message says to
  write `my $f; $f = sub { ... };` or `__SUB__`.
- The fault for a list where one value is wanted names an anonymous
  sub as `an anonymous sub`.
- **What stood**: D161's sharing (39 programs: every kind of loop
  and block, recursion, parameters, arrays reached again, the
  file's variables before their `my`); D162 outside the two points
  above (freezing for good never changes what is printed before the
  fault); D163's union, given the order above; D165 and the parsing
  (108 programs).

Claims from the review, for the builder to add with the others:

- T370 `sub arg() { say "arg"; 1 } my $f = sub ($x) { say "called"; $x }; sub fn() { say "fn"; $f } fn()->(arg());` → `arg|fn|called`
- T370 `my $i = 0; my @fs = (sub { "zero" }, sub { "one" }); say $fs[$i]->($i = 1);` → `one`
- T370 `my $x = 1; sub mk() { $x = 5; return sub ($v) { $v } } say mk()->($x + 0), mk()->($x);` → `15`
- T371 `my ($p, $q, $c) = (1, 2, 1); my @s; for my $x ($c ? $p : $q) { push @s, sub { $x } } $p = 9; say $s[0]->();` → `9`
- T371 `my @a = (1, 2); my @s; for my $x (@a) { for my $y (grep { 1 } $x) { push @s, sub { $y } } } $a[0] = 9; say $s[0]->();` → `9`
- T372 `my @a = (1, 2); my @s; for my $x (@a) { push @s, sub { $x = 5 } } $s[0]->(); say "@a";` → `5 2`
- T373 `sub nm() { return sub { 42 } } my $r = \&nm->(); say ref($r);` → `SCALAR`
- T374 `sub mk2() { return sub { 12 } } say mk2()();` → does not compile, `syntax error`
- T375 `my $g = 1; my @s; for my $i (1..2) { push @s, sub { sub { $g } } } say $s[0] == $s[1] ? "same" : "diff";` → `diff`
- T376 `my $f = sub { $f->() };` → does not compile, `Global symbol "$f"`

#### Claims

Each line is a program and what perl 5.42.0 printed for it on
2026-11-27 (stdout, lines joined by `|`); the builder adds them to
`briefs/claims.py` as T360 onward and reruns them.

- T360 `my @s; for my $i (1..3) { push @s, sub { return $i } } say join ",", map { $_->() } @s;` → `1,2,3`
- T360 `my @s; for (my $i = 0; $i < 3; $i++) { push @s, sub { $i } } say join ",", map { $_->() } @s;` → `3,3,3`
- T360 `my @s; for my $i (1..3) { my $j = $i; push @s, sub { $j++ } } say $s[0]->(), $s[0]->(), $s[1]->();` → `122`
- T360 `sub counter() { my $n = 0; return sub { return ++$n } } my $c = counter(); my $d = counter(); say $c->(), $c->(), $d->();` → `121`
- T360 `my $x = 1; my $f = sub { $x }; $x = 2; say $f->(); my $g = sub { $x = 5 }; $g->(); say $x;` → `2|5`
- T11 `my @a=(1,2); my @s; for my $x (@a) { push @s, sub { $x } } $a[0]=9; say $s[0]->();` → `9`
- T361 `my %h = (a => 1); my @s; for my $v (values %h) { push @s, sub { $v } } $h{a} = 9; say $s[0]->();` → `9`
- T361 `my %h = (a => 1); my @s; for my $k (keys %h) { push @s, sub { $k } } delete $h{a}; say $s[0]->();` → `a`
- T361 `my ($p, $q) = (1, 2); my @s; for my $x ($p, $q) { push @s, sub { $x } } $p = 9; say $s[0]->();` → `9`
- T361 `my @a = (1,2,3); my @s; for my $x (@a) { push @s, sub { $x } } push @a, 4; shift @a; say $s[0]->(), $s[2]->();` → `13`
- T362 `my @a = (1,2); my @s = map { sub { $_ } } @a; say defined $s[0]->() ? "def" : "undef";` → `undef`
- T363 `my @s; for my $i (1..2) { push @s, sub { 1 } } say $s[0] == $s[1] ? "same" : "diff";` → `same`
- T363 `my @s; for my $i (1..2) { push @s, sub { $i } } say $s[0] == $s[1] ? "same" : "diff";` → `diff`
- T363 `my $g = 1; sub mk() { return sub { $g } } say mk() == mk() ? "same" : "diff";` → `diff`
- T363 `sub mk() { return sub { 1 } } say mk() == mk() ? "same" : "diff";` → `same`
- T364 `my $f = sub { return (1,2,3) }; my @l = $f->(); my $c = $f->(); say scalar(@l), $c;` → `33`
- T364 `my $total = 5; my $step = sub { $total += 100; return 1 }; say $total + $step->();` → `106`
- T364 `my @l; my $x = 1; my $bump = sub { $x = 9; 0 }; @l = ($x, $bump->()); say "@l";` → `9 0`
- T365 `my $f = sub { last }; for my $i (1..3) { say $i; $f->() } say "done";` → `1|done`, and a warning `Exiting subroutine via last`
- T366 `my $f = sub () { 42 }; say $f->(1);` → dies, `Too many arguments for subroutine`
- T366 `my $f; $f->();` → dies, `Can't use an undefined value as a subroutine reference`
- T366 `my $f = [1]; $f->();` → dies, `Not a CODE reference`
- T366 `my $f = 5; $f->();` → dies, `as a subroutine ref while "strict refs"`
- T367 `my %d = (add => sub ($x, $y) { $x + $y }); my @fs = (sub { 7 }); say $d{add}->(1,2), $fs[0](), $d{add}(3,4); my $add = sub ($x) { sub ($y) { $x + $y } }; say $add->(1)->(2), $add->(1)(2); say sub { 3 }->();` → `377|33|3`
- T368 `sub named($x) { return $x + 1 } my $r = \&named; say $r->(1), ref($r), $r == \&named ? "same" : "diff"; my $f = sub ($n) { return $n <= 1 ? 1 : $n * __SUB__->($n - 1) }; say $f->(5);` → `2CODEsame|120`
- T369 `my sub fact($n) { return $n <= 1 ? 1 : $n * fact($n - 1) } say fact(5);` → dies, `Undefined subroutine &main::fact`
- T369 `my @s; for my $i (1..2) { push @s, sub { state $n = 0; return ++$n } } say $s[0]->(), $s[0]->(), $s[1]->();` → `121`
