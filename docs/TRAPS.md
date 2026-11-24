# Traps

Places where the obvious implementation runs, doesn't fault, and
prints something perl doesn't: a WRONG (D2). Each was run under perl
(5.38.2 first, and again under 5.42.0 by step 0, on 2026-11-24: every
row here is what 5.42 does), and each names
the step that has to deal with it and the way out proposed.
[`briefs/claims.py`](briefs/claims.py) holds every row as a program
and reruns them all: start there when the perl changes. A step's
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
| T45 | `use utf8;` and, on a later line (T73), `say uc("straße"); say length(uc("straße"));` | `STRASSE`, `7` | 3 | Fault on case-mapping a code point past ASCII, until a step brings perl's tables |
| T46 | `say "12" & "10"; say "12" &. "10";` | `8`, `10` | 22 | `&` is numeric under `use v5.42`; `&.` and its kin are cut |
| T47 | `say -"foo"; say -"-foo";` | `-foo`, `+foo` | 3 | Fault: unary minus on a string that isn't a number |

## Reading that writes (step 13)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T48 | `my $h = {}; my $x = $h->{a}{b}; say exists $h->{a} ? "made" : "no";` | `made` | 13 | Fault on reading through a missing key |
| T49 | `my %h; for my $x ($h{l}->@*) { } say exists $h{l} ? "made" : "no";` | `made` | 13 | The same, in `foreach`, `map`, `keys` |
| T50 | `my @a; my $t = $a[3][0]; say scalar(@a);` | `4` | 13 | The same |

## Accepted by the obvious parser, refused by perl

The first half of D2: a program the compiler accepts is a program perl
accepts. Each of these is a compile error in perl, so each is a
refusal here, with a test.

| | Program | perl says | Step | Way out |
|---|---|---|---|---|
| T51 | `say 1 <=> 2 == -1;` | syntax error | 4 | Refuse: `<=>`, `cmp`, `==` and `..` don't associate; also `1 .. 2 .. 3` |
| T52 | `say 0 < $o isa P;` | syntax error, though `$o isa P == 1` parses | 17 | Refuse: `isa` sits above the relationals and doesn't mix with them |
| T53 | `try { ... } catch { ... }` | `catch block requires a (VAR)` | 15 | Refuse |
| T54 | `my %h = map { "$_" => 1 } @a;` | syntax error; `map {; ...}` and `map +( ... ),` work | 10 | Refuse the shapes perl guesses wrong (D21) |
| T55 | `sub n(:$x) { }` | `A signature parameter must start with '$', '@' or '%'` | 8 | Refuse: tree-sitter-perl accepts it, which is why a grammar is no oracle |
| T56 | A subclass method that reads its parent's `field $x` | `Global symbol "$x" requires explicit package name` | 17 | Refuse: fields are lexical |
| T57 | `my $s = "ab"; say($s x3);` | `Bareword "x3" not allowed` | 3 | Refuse: `x` needs a space before a digit here |

## Found by reading Crayon

Crayon's grammar, tree and plan were read against this design after
the first fifty; these are what they showed.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T58 | `my $x = 5; { my $x = $x // 9; say $x }` | `5` | 5 | Agree: the right side is resolved before the new `$x` exists |
| T59 | `for my $i (1..3) { my @r = map { last if $_ == 2; $_ } (1,2,3); say $i } say "done";` | `done` | 10 | Refuse `last` and `next` in a `map`, `grep` or `sort` block |
| T60 | `sub f() { next } for my $i (1..3) { f() if $i == 2; say $i }` | `1 3`, and a warning | 8 | Refuse loop control that isn't inside a loop of the same sub |
| T61 | `my $a = 5; my @s = sort { $a <=> $b } (3,1,2); say "@s";` | `2 1 3`, and a warning | 10 | Refuse `my $a` and `my $b` |
| T62 | `say 65.66.67;` | `ABC` | 2 | Refuse a number with two dots |
| T63 | `my %h = (010 => "a", 0x10 => "c"); say join ",", sort keys %h;` | `16,8` | 12 | Agree: the key is the number, as a string |
| T64 | `my $i = 5; do { say $i; $i++ } while ($i < 3);` | `5` | 6 | Agree if `do BLOCK` comes in: the block runs first |
| T65 | `sub f() { try { 42 } catch ($e) { 0 } } say "[", f(), "]";` | `[42]` | 15 | Fault (D18): a sub that ends in `try` has no value |
| T66 | `"abc" =~ /b/; say "xbx" =~ // ? "y" : "n";` | `y`: the empty pattern is the last one used | 19 | Refuse the empty pattern |
| T67 | `use utf8;` and, on a later line (T73), `say "٣" =~ /^\d$/ ? "digit" : "no"; say "a\n" =~ /a$/ ? "match" : "no";` | `digit`, `match` | 19 | Agree |
| T68 | `my $x = (4,5,6); say $x;` | `6`, and two warnings | 9 | Refuse (D15) |
| T69 | `say -foo;` | `-foo` | 3 | Refuse a bareword |
| T70 | `sub f() { ... } f();` | dies, `Unimplemented at FILE line N.` | 15 | Agree, as a `die`, or refuse until then |
| T71 | `my $name = "x"; say "$name's";` | `x's`, in silence (5.38 read `$name::s`, warned twice and printed an empty line) | 16 | Agree |

## Found at step 0

Building `say 42;` and rerunning everything above under 5.42. T72's
first half, T73 and T74 came from the builder's own probes. T75 and
T72's second half came from an adversarial review of the step's
language, a reader given its definition and perl and asked to break
it: both were programs the compiler as first built accepted and got
wrong. The reviewer also found that a file of 2^32 lines wraps perl's
line counter back to 1, with the same result as `# line 1`.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T72 | A first line `#!/usr/bin/perl -n`, then `use v5.42; say 42;` | nothing, stdin being empty; once for each line of stdin otherwise. With blanks before the `#!`, the same. `#!/bin/echo hello` there, and perl runs `echo`. **And on any line perl calls line 1**: after `use v5.42; say 1;`, the lines `# line 1`, `#!perl -n` and `say 2;` print `1` alone, and `perl -c` sees nothing wrong | 0 | Refuse every line that starts `#!` (D33). After code on its line it is a comment, to perl too |
| T73 | `use v5.42;` and then, on one line, `use utf8; say uc("straße");` | doesn't compile: `Use of non-ASCII character 0xC3 illegal when 'use source::encoding "ascii"' is in effect`. On the line after `use utf8;`, it runs. In a comment with no `use utf8`, the same error | 3 | Refuse a character past ASCII on any line up to and including the one that says `use utf8;`, comments included |
| T74 | `# line 100 "other.pl"` on a line of its own, then `say 42; die "x";` | `42`, and the `die` says `x at other.pl line 101.` With `#line 100`, the same line and this file. Indented, or with more words after the number, it is a comment | 15, 16 | To be proposed with `die` and `__LINE__`: refuse a comment perl reads as a line directive. Until then the only thing a directive could change on stdout was which line is line 1 (T72), and that is closed; a fault's line is the language's own (D12) |
| T75 | `use v5.42#c`, then `;` on the next line, then `say 42;` | doesn't compile: `Can't locate v5.pm in @INC`. With a space before the `#`, it prints `42` | 0 | Refuse a version literal that isn't followed by a blank or `;`: perl decides it is a version by that one character |

## The checks themselves

- A `fault` test that perl can't compile passes a check that only
  compares stdout, whenever nothing was printed first. Hence `perl -c`
  in D10.
- The natural test of "resizing a frozen array faults" never ends
  under perl: `for my $x (@a) { push @a, $x }`. Hence the time limit
  in D10, and such a test is written so that perl finishes.
- Two hash seeds agree on a two-key hash 48% of the time and on a
  three-key hash 25%. Hence eight seeds and the reading rule in D10.
  (Under 5.42, over the 435 pairs of seeds 1 to 30: 211 for the keys
  `a` and `b`, and 100 for `a`, `b` and `c`, which is 23%.)
- A program more than 100 calls deep makes perl warn, so it can't be
  a `same` test as D10 stands. Step 8.
- Plain `perl FILE` prints `é` as the single byte E9, in silence;
  with `-CSDA`, or with `use open ':std', ':encoding(UTF-8)';` in the
  file, it prints the two bytes of UTF-8. The oracle runs perl with
  `-CSDA` (D24), so "the same file, given to perl" is true only with
  a flag the file doesn't carry. Step 3 proposes whether a program
  with text past ASCII must say `use open` itself.
- `perl -c` says `FILE syntax OK` on stderr when all is well, so
  "nothing on stderr" for a compile means nothing but that line.
- 5.38 and 5.42 differ here, and nowhere else that these documents
  speak of (step 0 ran all of it under both): the apostrophe as a
  package separator (T71); `source::encoding`, which makes a non-ASCII
  source without `use utf8` an error, by the line (T73); the builtins
  `use v5.42` imports (`true`, `false`, `trim`, `ceil` and nine more);
  `for my ($k, $v)`, experimental until 5.40; `try`, stable from 5.40;
  `:reader`, `__CLASS__`, `:writer`, `my method` and `->&`, each newer
  than 5.38; `^^`, `^^=`, `any`, `all`.
- A program's own `sub trim` or `sub ceil` is still the one called
  under `use v5.42`, not the builtin, and perl says so twice as it
  compiles (`Prototype mismatch: sub trim ($) vs none`, `Subroutine
  trim redefined`). So it is refused on both counts (D21, D15).
