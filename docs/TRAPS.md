# Traps

Places where the obvious implementation runs, doesn't fault, and
prints something perl doesn't: a WRONG (D2). Each was run under perl
(5.38.2, on 2026-11-24; step 0 reruns them under 5.42), and each names
the step that has to deal with it and the way out proposed. A step's
builder reads its rows first, and each row becomes at least one golden
test. A trap found later is added here, with its program, before it is
fixed.

Most of these came from one adversarial review of the first draft of
this design, which is the argument for doing that again at every large
step: the draft's author had the rule in front of them and still
wrote down four things about perl that perl refuted.

The way out is one of: **agree** (do what perl does), **fault**,
**refuse**. In that order of preference, except where agreeing means
rebuilding something D17 to D22 cut.

## Reading and evaluating

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T1 | `my $total = 5; sub step() { $total += 100; return 1 } say $total + step();` | `106` | 5, 8 | Agree: a variable operand is read when the operator runs (D14) |
| T2 | `my %c = (n => 0); sub inc() { $c{n}++; return $c{n} } say join ",", $c{n}, inc(), $c{n};` | `1,1,1` | 12 | Agree: the same for an element (D14) |
| T3 | `my $n = 0; my @s = sort { $n++; $a <=> $b } (5,3,8,1,9,2,7); say $n;` | `14` | 10 | Fault on an effect in a comparator, or port perl's merge (D14) |
| T4 | `say join ",", sort { length($a) <=> length($b) } qw(bb a ccc dd e fff);` | `a,e,bb,dd,ccc,fff` | 10 | Agree: `sort` is stable; C's `qsort` isn't |

## Aliases (D17)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T5 | `my @a=(1,2,3); for my $x (@a) { $a[0] = 9; say $x }` | `9 2 3` | 9 | Fault: `@a` is frozen |
| T6 | `my @a=(3,1,2); for my $x (sort { $a <=> $b } @a) { $a[0]=7; $a[1]=7; $a[2]=7; say $x }` | `7 7 7` | 10 | Fault: frozen through `sort`; the same through `grep`, `reverse`, a slice, a ternary, `(@a, @b)`, `($a[0], $a[1])` |
| T7 | `my %h=(a=>1); for my $v (values %h) { $h{a} = 9; say $v }` | `9` | 12 | Fault: frozen through `values`, `%h` in a list and a hash slice; not through `keys` |
| T8 | `my @a=(1,2,3); say join ",", map { $a[2] = 8; $_ } grep { 1 } @a;` | `1,2,8` | 10 | Fault: `map` and `grep` freeze as `foreach` does |
| T9 | `my @a=("ab","cd"); for my $x (@a) { chop $x } say "@a";` | `a c` | 9, 16 | Refuse: also `substr($x, 0, 1, "Z")`, `undef $x`, `($x) = ("q")` |
| T10 | `my @a=(1,2); my @b = sort { $a = 5; 0 } @a; say "@a";` | `5 2` | 10 | Refuse: `$a` and `$b` are read-only |
| T11 | `my @a=(1,2); my @s; for my $x (@a) { push @s, sub { $x } } $a[0]=9; say $s[0]->();` | `9` | 14 | Refused until step 14 proposes |
| T12 | `my @a=(1,2); my @r; for my $x (@a) { push @r, \$x } ${$r[0]} = 7; say "@a";` | `7 2` | 13 | Refuse |
| T13 | `my ($p,$q)=(1,2); for my $x ($p,$q) { $p = 7; say $x }` | `7 2` | 9 | Refused until step 9 proposes |
| T14 | `my $x = 10; my $f = sub { $x }; for $x (1,2) { say $f->() }` | `10 10` | 9 | Refuse a `foreach` with a variable that isn't `my` |
| T15 | `sub show() { say $_ } for (1..2) { show() }` | `1 2` | 10 | Refuse `$_` outside the block that binds it |

## Context (D18)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T16 | `sub a() { my @a = (42); return @a } my $x = a(); say $x;` | `1` | 10 | Fault |
| T17 | `my @a=(7,8,9); sub f($c) { return $c ? @a : 0 } my $v = f(1); say $v;` | `3` | 10 | Fault: list-shaped through `?:`, `\|\|`, `//`, `do` |
| T18 | `sub f() { my @r = (5,6,7); } my $v = f(); say $v;` | `3` | 10 | Fault: a list assignment is list-shaped |
| T19 | `sub f($x) { if ($x) { "yes" } } say "[", f(0), "]";` | `[0]` | 8 | Fault: a sub that ends in a compound statement has no value |
| T20 | `sub f() { return (1,2,3) } f(); say "ok";` | `ok` | 10 | Agree: void is a third context, and nothing faults under it |
| T21 | `my @a=(1,2,3); say "x" . @a; say -@a; say uc(@a);` | `x3`, `-3`, `3` | 9 | Agree: an array in a scalar operand is its count |
| T22 | `my @a=("%s-%s",2,3); say sprintf(@a);` | `3` | 16 | Agree, or refuse an array as `sprintf`'s format |
| T23 | `say reverse("abc"); say scalar reverse("abc");` | `abc`, `cba` | 10, 16 | Agree: `reverse` is by context |

## Parsing (D21)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T24 | `say 010;` | `8` | 0 | Refuse a leading zero until step 2; `say 08;` doesn't compile in perl |
| T25 | `say (1+2)*3;` | `3`, and a warning | 1 | Refuse: a builtin, brackets, then an operator |
| T26 | `my $x = 5; say $x -1;` | nothing; dies (`$x` taken as a filehandle) | 5 | Refuse the shapes perl reads as a handle |
| T27 | `say - -5;` | `5`; `say --5;` doesn't compile | 1 | `--` and `++` are tokens |
| T28 | `sub q($x) { return $x * 2 } say q(5);` | `5` | 8 | Refuse a sub named for anything perl knows |
| T29 | `sub dbl(@x) { return map { $_ * 2 } @x } my @s = sort dbl(3,1,2); say "@s";` | `3 1 2` | 10 | Refuse `sort NAME(...)` |
| T30 | `sub f($c) { my $x = 10 if $c; $x++; return $x } say f(1); say f(0); say f(0);` | `11 1 2` | 5 | Refuse `my` under a modifier |
| T31 | `for my $i (1..3) { my $n = $i * 10; sub get() { return $n } say get(); }` | `10 10 10` | 8 | Refuse a named sub inside a block |
| T32 | `for my $i (1..3) { { last; } say $i }` | `1 2 3` | 6 | Agree: a bare block is a loop that runs once |
| T33 | `say 2 == 2 == 2 ? "y" : "n"; say 1 < 5 < 3 ? "y" : "n";` | `y`, `n` | 4 | Refuse chained comparisons until proposed; read left to right they give `n`, `y` |
| T34 | `say "cost: $$";` | the process id; and `say "user@example.com";` doesn't compile | 3 | Refuse an unescaped `$` or `@` in a double-quoted string until step 16 |

## Numbers (D23)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T35 | `my $x = 1e15; say $x; my $y = $x + 1; say $x;` | `1e+15`, `1000000000000000` | 2 | Fault on making a whole Num of 10^15 or more a string |
| T36 | `say 4000000000000000/2; say 18014398509481984/2;` | `2e+15`, `9007199254740992` | 2 | The model enumerates `/` |
| T37 | `say 10**15; say 7**20; say 2**50;` | `1000000000000000`, `79792266297612001`, `1.12589990684262e+15` | 2 | The model enumerates `**` |
| T38 | `say "1e16" + 1; say 1e16 + 1;` | `10000000000000001`, `1e+16` | 3 | Fault on such a string used as a number |
| T39 | `say 9007199254740993 == 2**53 ? "eq" : "ne";` | `eq` | 4 | Agree: an Int and a Num compare as floats; step 4 has a model |
| T40 | `say -10 % 3e19; say 7 % 0.5;` | `3e+19`; dies | 2 | Fault on `%` with an operand outside Int; agree on truncation |
| T41 | `say join ",", "08".."11"; say join ",", "a".."e";` | `08,09,10,11`, `a,b,c,d,e` | 10 | Fault on a string as a range's end |
| T42 | `my ($p, $q) = ([], []); say $p <=> $q;` | `-1` or `1` | 13 | Fault: only `==` and `!=` between two references |
| T43 | `my $x; my $y = $x--; say defined $y ? "[$y]" : "undef";` | `undef`; with `++`, `[0]` | 5 | Agree; and `*=` on undef warns where `+=` doesn't |
| T44 | `my $s = "ab"; $s--; say $s;` | `-1`, no warning | 5 | Fault: `--` on a string that isn't a number, as `++` |

## Strings (D24)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T45 | `use utf8; say uc("straße"); say length(uc("straße"));` | `STRASSE`, `7` | 3 | Fault on case-mapping a code point past ASCII, until a step brings perl's tables |
| T46 | `say "12" & "10"; say "12" &. "10";` | `8`, `10` | 22 | `&` is numeric under `use v5.42`; `&.` and its kin are cut |
| T47 | `say -"foo"; say -"-foo";` | `-foo`, `+foo` | 3 | Fault: unary minus on a string that isn't a number |

## Reading that writes (step 13)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T48 | `my $h = {}; my $x = $h->{a}{b}; say exists $h->{a} ? "made" : "no";` | `made` | 13 | Fault on reading through a missing key |
| T49 | `my %h; for my $x ($h{l}->@*) { } say exists $h{l} ? "made" : "no";` | `made` | 13 | The same, in `foreach`, `map`, `keys` |
| T50 | `my @a; my $t = $a[3][0]; say scalar(@a);` | `4` | 13 | The same |

## The checks themselves

- A `fault` test that perl can't compile passes a check that only
  compares stdout, whenever nothing was printed first. Hence `perl -c`
  in D10.
- The natural test of "resizing a frozen array faults" never ends
  under perl: `for my $x (@a) { push @a, $x }`. Hence the time limit
  in D10, and such a test is written so that perl finishes.
- Two hash seeds agree on a two-key hash 48% of the time and on a
  three-key hash 25%. Hence eight seeds and the reading rule in D10.
- A program more than 100 calls deep makes perl warn, so it can't be
  a `same` test as D10 stands. Step 8.
