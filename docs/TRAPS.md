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
| T32 | `for my $i (1..3) { { last; } say $i }` | `1 2 3` | 6 | D59: refuse an unlabelled `last` or `next` whose nearest loop, as perl counts them, is a bare block. (The plan's first reading was to agree) |
| T33 | `say 2 == 2 == 2 ? "y" : "n"; say 1 < 5 < 3 ? "y" : "n";` | `y`, `n` | 4 | Refuse chained comparisons until proposed; read left to right they give `n`, `y` |
| T34 | `say "cost: $$";` | the process id; and `say "user@example.com";` doesn't compile | 3 | Refuse an unescaped `$` or `@` in a double-quoted string until step 16 |

## Numbers (D23)

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T35 | `my $x = 1e15; say $x; my $y = $x + 1; say $x;` | `1e+15`, `1000000000000000`. The same from 10^15 up to 2^53 - 1 and for no other value: `9007199254740992.0` and `1e16` print one way whatever came before, and so does everything below 10^15. The mark also shows through `-$x` and `--$x`, whose answers are an integer after it and a float before | 2 | Fault on making a whole Num from 10^15 to 2^53 - 1 a string (step 2's proposal, Q1; D23 said 10^15 or more) |
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

## Found at step 1

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T76 | `say (1 +` and, on the next line, `2);`. Or `say (1 + 2)` with its `;` on the next line, or after a comment | `3`, and a warning as it compiles: `say (...) interpreted as function`. With the bracket hard against `say`, or after two blanks, a tab or a newline, no warning; nor when the `)` and the `;` are on the line the `(` is on | 1 | Refuse `say`, one blank and a bracket unless the statement ends on that line. perl makes the check by reading along the line of text, not by parsing |

A review of this step's language, with a model of its own, found no
other: `briefs/step1-review/`. Two things it noted that a later step
will want. perl sometimes prints an Int on a line where the language
has already faulted, because perl went through an unsigned or a float
and came back: `say - - (-9223372036854775807 - 1);` prints
`-9223372036854775808`, and `say 0 * (9223372036854775807 + 1);`
prints `0`. The language faults at the inner operation, which D12
allows; step 2's model must not take perl's line for an answer there.
And perl compiles some shapes slowly: brackets nested 100,000 deep
round a `% 0`, which it can't fold, take `perl -c` 21 seconds, so a
test of that shape would run into the oracle's time limit.

Not traps, since no obvious parser takes them, but each is what perl
does where the language refuses: `say 2 * *3;` reads `*3` as a glob,
warns and prints `0`; `say * 2;` prints `*main::2`; `say % 2;` and
`say(());` print an empty line, in silence.

## Found proposing step 2

From perl's source (`pp.c`, `sv.c`), then run. `briefs/step2-perl-
numbers.py` is the rule and `briefs/step2-history.pl` the search for
where a number's past shows.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T77 | `say 10 ** 4611686018427387904; say 9 ** 4611686018427387904;` | `0`, `1`: perl asks whether (bits in the base) times (the power) is at most 64, in a 64-bit unsigned, and for a vast power the product wraps, so it takes the integer path and the answer is whatever is left modulo 2^64. `3 ** 9223372036854775807` is `Inf` | 2 | Fault: the rule asks the same question of the true product, and the float answer is not finite. A bug in perl, to all appearances |
| T78 | `say 00.5; say 0x1.8; say 1.5 .5;` | `05`, `18`, `1.55`: a dot after a whole literal is concatenation, and `1.5e3.2` is `15002` | 2, 3 | Refuse a number hard against a dot or another number (with T62); step 3 says what a dot after a blank is |
| T79 | `my $x = 0.0; say atan2(0, -$x);` and the same with `my $t = $x + 1;` in between | `3.14159265358979`, then `0`. The negation of a float zero is a negative zero, unless the zero has been used as an integer, when it is an integer zero. `say` prints `0` for both; `sprintf("%g")` prints `-0` for one; `(-$x) ** -1` is `-Inf` or `Inf` | 16, 22 | The second place a number's past shows. Fault on a negative zero given to `atan2` or formatted with `%g`, `%e` or `%f`; and no infinities (Q3) or a fault on zero to a negative power |
| T80 | `say 1e10 * 1e9; say 1e10 * 1e10;` | `10000000000000000000`, `1e+20`: whole floats are multiplied as integers, and the answer is an exact unsigned integer when it fits one and a float when it doesn't | 2 | Fault from 2^63 to 2^64 - 1, where perl's answer is an unsigned integer; a Num beyond (Q2) |
| T81 | `say 9223372036854775808; say 18446744073709551616; say 1e400;` | `9223372036854775808`, `1.84467440737096e+19`, `Inf`: a literal too large for its kind becomes the next kind, in silence | 0, 2 | Refuse a digits-only literal past 2^63 - 1 (step 0 does), and a float literal that isn't finite |
| T82 | `say 1_e3;`, and `1e_3`, `1__0`, `0x_ff`, `0_17`, `1_.5`, `1.5_` | The number, and `Misplaced _ in number` as it compiles. `1_000`, `1.5_0`, `1e1_0` and `0xff_ff` are silent | 2 | Refuse an underscore that isn't between two digits (D15) |

Not traps, but perl's answers where the proposal faults: `-7 % 9**9**9`
is `Inf`; `NaN <=> 1` is undef; `1e20 % 7` is 2, by `fmod`, where
`1e19 % 7` is 3, by integers.

## Found proposing step 3

`briefs/step3-strings-as-numbers.py` asks perl for every answer it can
give for a string where a number is wanted.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T83 | `my $s = "3.0"; say $s + 9007199254740990;` and the same with `my $t = $s > 0.5;` first | `9.00719925474099e+15`, then `9007199254740993`. perl settles what a string is worth at its first use as a number, one way for a use that wants an integer and another for a float, and keeps it. `"1e16"` is the other way round (T38) | 3 | The Num and float arithmetic, which is perl's answer for a string with no past; a fault where whole-number arithmetic would differ (Q2) |
| T84 | `my $s = "12abc"; my $t = $s + 0; say $s + 1;` | `13`, and one warning, at the first use only: perl keeps the number it guessed, and says nothing the second time | 3 | Fault at the first use (D15): there is no second |
| T85 | `say -"+0"; say -"-foo"; say -"foo";` | `-0`, `+foo`, `-foo`: a minus before a string that starts with a sign or a letter changes the text. `-"12"` is the integer -12 until the string has been used as a float, and the float after | 3 | The string must be a number; the answer is a Num; a string that starts with `+` faults (Q2) |
| T86 | `say length "\x"; say length "\x{}";` | `1`, `1`: a NUL, in silence. `"\q"` and `"\8"` warn and give `q` and `8`; `"\-"` gives `-` in silence | 3 | Refuse `\x` without digits and a backslash before any letter or digit that isn't an escape (Q5) |
| T87 | `say length "abc" + 1;` | `1`, and a warning: without brackets a named operator's argument runs over arithmetic. `length ("abc") . "de"` is `3de`: with brackets, hard against or not, they are the whole argument | 3 | Agree: perlop's row for named unary operators. The first is then a fault, `"abc" + 1` |
| T88 | `say length(chr(55296)); say chr(65534);` | `1`; then the character and a warning, `Unicode non-character U+FFFE is not recommended`. A surrogate and a number past U+10FFFF are built in silence and warned of when printed; under `use open` they print as the text `\x{D800}` | 3 | A character is a Unicode scalar value: `chr` faults otherwise. Printing a noncharacter faults (Q4) |
| T89 | `say "a" x -1; say "a" x 1e30; say "a" x 2.7;` | An empty line and `Negative repeat count does nothing`, twice (the second count having overflowed); `aa` | 3 | Fault on a negative count and on one too large; cut a fraction off, as perl does |
| T90 | `say "a".5; say 1 . .5;` | `a5`, `10.5`: after a value a dot is an operator, whatever follows it | 3 | Agree: the lexer knows whether a value or an operator comes next (D29) |

## Found by the review of step 2

A reader given step 2's definition, and the claim that a number's past
shows in two places only (T35, T79), with perl.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T91 | `say 1.000...0;` with 249 zeros: a decimal literal of 251 characters | Nothing: `Number too long`, as it compiles. 250 characters are read. Underscores aren't counted, and a hex literal may be any length | 2 | Refuse a decimal literal of more than 250 characters |
| T92 | `my $x = 10000000000000000; say $x + 1.0;` and the same with `my $t = $x / 3;` first | `10000000000000001`, then `1e+16`. When both operands carry a float, `+`, `-` and `*` work in floats, and an Int that has been used as a float carries one if a double holds it exactly. `2**53 + 1` and `2**63 - 1` don't change; `/`, `%` and `**` don't. A copy carries it, and so does `1.0` in a sub called twice | 5 | Fault: a whole number of 2^53 or more that is exactly a double, with a whole Num or a string (step 3's Q7, amending D35) |
| T93 | `my $x = -9007199254740991.0; $x--; say $x - 1;` and the same with `my $t = $x % 7;` before the `$x--` | `-9.00719925474099e+15`, then `-9007199254740993`: `--` on a Num subtracts as a float, unless the Num has been used as an integer. `++` asks each time, and doesn't change | 5 | `--` on a whole Num gives a Num, and faults when the answer reaches 2^53; what T79 and D36 fault on covers the rest (`1.0` decremented is a zero whose negation has a sign; `-999999999999999.0` decremented is in the window) |

The sign of a zero (T79) shows in more places than `atan2` and
`sprintf("%g")`: `pack("d")`, `sprintf("%a")`, `POSIX::copysign` and
`signbit`. And `Data::Dumper` reads the integer mark directly, printing
`'5'` for a Num 5 and `5` once it has been used as an integer: a
module, and a reason to be careful when one is proposed.

## Found building step 3

The model's tests, held to perl, and the hand tests found these after
the proposal was agreed. Each is a refusal or a fault where the
proposal had perl's answer, or none.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T94 | `say length - 5;` and `say length-5;` | `2`, and `Warning: Use of "length" without parentheses is ambiguous`, as it compiles. `length -5` is silent: perl goes by the blank before the sign and the lack of one after. With the sign on the line below it goes by how that line begins: a sign in the first column warns | 3 | Refuse a sign after a named unary operator unless it is on the name's line, with blanks before it and none after (D41) |
| T95 | `say "\x4 ";` and `say "\18";` | The character and a warning: `Non-hex character ' ' terminates \x early`, `Non-octal character '8' terminates \0 early`. `"\x4"` at the end of a string, `"\x41g"` and `"\0008"` are silent | 3 | `\x` takes two hex digits or braces; an octal escape of one or two digits may not be followed by `8` or `9` (D43) |
| T96 | `say substr("abcde", -8, 2);` | An empty line, and `substr outside of string`: the piece starts and ends before the beginning. `substr("abcde", -8, 3)` ends at the beginning, and is empty in silence | 3 | Fault, as for a start past the end (D41) |
| T97 | `say substr("abc", 0, 1e30); say substr("abc", 1e30); say index("abc", "c", 1e30);` | `ab`, `c`, `2`, in silence: a float past the Ints is cut to whatever the machine gives | 3 | Where a whole number is wanted, the number cut toward zero must be an Int, or it faults (D41) |
| T98 | `say "a" x -0.5;` and `say ord chr(-0.5);` | An empty line and `Negative repeat count does nothing`; `65533` and `Invalid negative number (-0.5) in chr`. perl tests the number before cutting it to 0. `"a" x "-0.5"`, a string, is silent | 3 | A count or a character number below zero faults before it is cut, a string's too (D42, D44) |
| T99 | `say "a"x 3; say "c" x.5; say "d" x"2"; say "a" x= 3;` | `aaa`, an empty line, `dd`; the last doesn't compile, `x=` being an assignment | 3 | Agree on the first three: after a value `x` is the operator, whatever it is hard against but a digit (T57). Refuse `x=` as the operator it is |

## Found by the review of step 3

A reader who hadn't seen the builder's model wrote one of its own from
the proposal, and ran it against perl: 2.9 million statements with
literal operands, and 82 million cases of one value used two ways. It
found twelve things. Eight the build had found for itself by then
(T94 to T98); these are the other four. Its model and generator are
kept, `briefs/step3-review/`, and the compiler agrees with them and
with perl on the statements `compiler.py` there draws.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T100 | `say ("(");` and `say (")" . "a");` | `(` and `)a`, each with `say (...) interpreted as function`: after `say`, one space and a bracket, perl looks for the closing bracket in the text of the line, and counts one inside a string or a comment. `say("(");`, two spaces, or a tab: silent | 3 | T76's rule by the text, as perl has it: the brackets close on the line, counted as characters, and `;` follows |
| T101 | `say(("a") x 3);` and `say "before"; say(("") x 9223372036854775807);` | `aaa`; then `before`, `Out of memory during list extend`, and exit 255. In `say`'s list of arguments, `x` with its left operand in brackets repeats a list: three values, or 2^63 of them. `say +("a") x 3` is the same; `length(("a") x 3)` and `("a") x 3 . ""` repeat a string | 3 | Refuse `(...) x N` where it is the whole argument of `say` or `print`, through brackets and unary plus. Step 9, which brings lists, says what it is there |
| T102 | `say "before"; say length("b" x 999999999999999);` | Nothing at all: perl works a constant `x` out as it compiles, runs out of memory doing it, and stops before the program starts (`panic: fold_constants`). The language prints `before` and faults: **not the beginning of what perl prints**, which D12 promises | 3 | D46: a perl that runs out of memory as it compiles is outside D12's promise. Every count is a constant until step 5; after that only a constant count is affected. No test asks perl for more than a megabyte; one count past what a string can be at all, 2^63 - 1 of `ab`, perl refuses as it runs, and that is test 148 |
| T103 | `my $x = "1.99999999999999999"; say substr("abcdefgh", $x);` and the same with `my $t = $x + 0.5;` first | `bcdefgh`, then `cdefgh`. Where a whole number is wanted, perl takes the digits before the point of a string it hasn't used as a float, and the double, cut, of one it has; and this string's double is 2. `"ab" x "0.99999999999999995"` is empty, or `ab`; `chr` goes the other way round | 3 | Where a whole number is wanted, a string with a point whose digits before it are not its number cut toward zero faults (D40) |

## Found proposing step 4

`briefs/step4-comparisons.py` asks perl for every comparison, test of
truth, and use of a boolean as a number, under every past of each
operand. Nothing there turns on a past that D40 doesn't already fault.
These are about how perl reads the words.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T104 | `say(0 \|\| ("a") x 3);` and `say(1 ? ("a") x 3 : "b");` | `aaa` both, as three values: the list that `say`'s argument is (T101) reaches the right operand of `\|\|`, `&&`, `//`, `or` and `and`, and both branches of `?:`. Not the left operand, and not through `xor`, `!`, a comparison or a dot | 4 | T101's refusal follows the same path down |
| T105 | `say "before"; say undef * 2;` and `say undef + 1;` | `before`, an empty line and `Use of uninitialized value in say`: `undef` takes an argument, and `*2` is one to it, a glob. `% 2` is a hash. `undef + 1`, `- 1`, `< 1`, `<=> 1`, `x 3`, `/ 2` and `.5` don't compile. `undef == 1`, `undef . "a"`, `undef // 1` are read as written | 4 | Bare `undef` may be followed by `)`, `,`, `;`, `?`, `:` or a logical operator, and by nothing else; elsewhere it is written `(undef)` |
| T106 | `say 0 or 2;` and `say true and false;` | `0`, with `Useless use of a constant`; `1`, with nothing at all. `or`, `and` and `xor` bind more loosely than `say` does: it is `(say 0) or 2` | 4 | Refuse a word operator after `say`'s argument; inside brackets, `say(0 or 2)`, it is the argument's |
| T107 | `say(not 0 \|\| 1);` and `say(not(0) \|\| 1);` | An empty line, then `1`: `not` takes everything to its right that binds tighter, unless a bracket follows it, and then the bracket is all it takes. `not (0) + 1` is 2 | 4 | Q5: refuse an operator that binds tighter than `not` after `not (...)`, or agree with perl |
| T108 | `say 1 != 1 == 0;` | An empty line: perl chains it, `(1 != 1) && (1 == 0)`, where reading from the left gives `1`. `1 < 2 == 1` isn't a chain, the two being of different rows, and `1 == 2 <=> 3` doesn't compile (T33, T51) | 4 | Refuse two operators of one row with no brackets between them |

## Found building step 4

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T109 | `say substr("abcdef", not 0, 1);` and `say index("abcabc", "c", 0 or 3);` | `abcdef`, in silence: `not` takes a list, and takes `0, 1`, so this is `substr("abcdef", "")`. The second doesn't compile: `or` binds more loosely than the commas | 4 | In a list of arguments a word operator is in brackets of its own (D51) |

## Found by the review of step 4

A reader with only the proposal's words and perl, on the step 3
reviewer's model extended: 1.26 million random statements over the
whole grammar, 950,000 comparisons, and a search of pasts by another
method than the builder's (every state perl can put a variable in,
found breadth-first through 134 kinds of use, then every look in
every state: 18 million looks, and 207,000 whole programs). **The
claim that no comparison, test of truth or boolean turns on a past
the language doesn't fault was not refuted.** Two findings: the word
operators in a list of arguments, which the build had met (T109), and
this one.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T115 | `say(!(undef) == 1);` and `say(! defined 1 == 0);` | `1` each, and as it compiles, `Possible precedence problem between ! and numeric eq (==)`: new in perl 5.42. It warns when an unbracketed `!` is the left operand of `== != < > <= >=` or `eq ne lt gt le ge`, unless it has folded the `!` to a constant (`!1 == 0` is silent) or the right operand is a `!` too; not for `<=>` or `cmp`. With variables every `!$x == $y` warns | 4 | Refuse an unbracketed `!` on the left of any comparison, a unary plus before it or not (D50) |

## Found proposing step 5

`briefs/step5-increments.py` asks perl what `++`, `--` and the
assigning operators leave in a variable, under seven pasts of it.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T110 | `my $x = 3; say(($x \|\| 0) + ($x = 5));` and `say(($x++) + ($x = 5));` | `10`, then `8`. `\|\|`, `&&`, `//` and `? :` give the variable itself when it is the operand they give, and so do brackets, `+$x`, `=`, `+=` and `++$x`: it is read when `+` runs, after the assignment. `$x++` and `-$x` give values; so does `$x . ""` beside anything but another dot (T117) | 5 | Agree (D14): where the value is one of two operands, the generated C keeps a pointer to it |
| T111 | `my $x = 5; say($x -1);`, `say $x +$y;`, `print $x .5;`, `say $x ++;` | The first three die as they run, `Can't use string ("5") as a symbol ref`: perl takes a variable that comes first after `say` or `print`, brackets or not, for a file handle when what follows the blank after it could begin a value. The last, `say(($x -1))` and `say $x <true` don't compile. `say $x - 1`, `say $x-1`, `say +$x -1` and `say $x ?1 : 2` are fine (T26) | 5 | Refuse, by perl's own list, less `?` (which its source lists, and which is fine): after the blank, a sign hard against what follows it, a dot and a digit, `*`, `%`, `<` or `&` hard against a name, `/` hard against anything but `=` or `/` |
| T112 | `my $x = 5; if ($x = 6) { say $x }` | `6`, and `Found = in conditional, should be ==`, as it compiles. Also for `($x = 6) && ...`, `\|\|`, `//`, `? :`, a modifier, `if (my $y = 6)`, `$x = true`, `$x = 2 + 3`, and `if (1 && ($x = 6))`, which perl has folded first. Not for `$x = $y`, `$x = undef`, `$x += 1`, under `xor`, in `say(!($x = 6))`, or in an `elsif` after `if (0)`. Under `!`, `not` or a unary plus *in a condition* it warns (`if (!($x = 6))`, `say(!($x = 6) && 1)`): perl takes the `!` away and tests the other way. And `$x = 1 and $y = 2;` warns, of the first | 5 | D53: refuse a `=` with no variable on its right wherever it is tested for truth, through `!`, `not` and `+` |
| T113 | `my $s = "009"; $s++; say $s;` and the same with `my $t = $s + 0;` first | `010`, then `10`: `++` on a string of digits makes the next string, of the same width, until the string has been used as a number. `"12"` is the string `13` or the integer; `"aa"` is `ab`, `"zz"` is `aaa`, `""` is 1, and `"ab"--` is -1, all in silence. `1e16--` warns `Lost precision when decrementing` and changes nothing | 5 | A numeric string stepped is a Num, and faults if it is digits that begin with a zero, or reaches 2^53; any other string faults (T44); a Num too large to step faults |
| T114 | `my $x = 1; my $x = 2;`, `my $x = 3; $x + 1;`, `my $x = 1; say ${x};` | Each prints or does what it looks like, and warns as it compiles: `"my" variable $x masks earlier declaration in same scope`, `Useless use of addition (+) in void context`, `Ambiguous use of ${x} resolved to $x`. `say $ x;`, `($x) = 4;`, `our $o = 1;` and `my $x = 10 if 1;` are silent | 5 | Refuse each: a second `my` in a scope, a statement that only has a value, every spelling of a variable but `$name` |

## Found building step 5

The model (`t/models/var.py`) was written before the compiler, and
held to perl: it found T116 and T117. T118 came from asking perl
about a statement that spans lines.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T116 | `{ }` as a statement; `say 1; { { } } say 2;`; `say 1; { } say 2;` | The first two warn `Useless use of anonymous hash ({}) in void context` (the second prints `1` and `2`); the third doesn't compile. An empty pair of braces where a statement begins is an anonymous hash, to perl. `if (1) { }` is silent | 5 | Refuse an empty bare block; an empty block of an `if` is fine |
| T117 | `my $x = 3; say $x . "a" . ($x = 5);`, `say((1 ? $x . "" : 0) . ($x = 5));`, `say(($x . "a") . ($x = 5));` | `5a5`, `55`, `5a5`: perl joins a row of dots as one operation (`multiconcat`) and reads every piece when it runs, brackets or not, and after folding what it can. `my $y = $x . "a"; say $y . ($x = 5);` is `3a5`, and so are `($x . "a") x 1 . ($x = 5)` and `($x + 0) . "a" . ($x = 5)` | 5 | D57: refuse a concatenation in which a later piece changes a variable an earlier piece reads |
| T118 | `say 1` / `if` / `$u + 1;` on three lines, `$u` undef; the same in an `elsif (` whose test is on the next line | The warning names the line of `say`, the first of the statement, and the line of the `elsif`: not the line the test or the `if` is on | 5 | A modifier's test is at its statement's line; an `elsif`'s at the `elsif` (tests 547 to 549) |

## Found by the review of step 5

A reader with the proposal and perl, and then with the compiler
(`briefs/step5-review/`): 698,000 programs against its model before
the build, 57,000 through the compiler after it, and texts rejoined
with blanks and comments at random, which is how T128 was found. One
of these prints what perl doesn't (T129); of the rest perl warns, or
doesn't compile.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T125 | `my $x = 5; say substr($x -1, 0);`, `say index($x .5, "c");` | Neither compiles: `Missing comma after first argument to substr function`. `substr` and `index` are list operators to perl, as `say` is, and it takes a variable that comes first after one for a file handle by the same guess (T111). Their second and third arguments are fine, and so are `length(`, `uc(` and the other named unary operators | 5 | Refuse, as after `say` |
| T126 | A variable whose name is 252 characters | `Identifier too long`, and no program. 251 is fine | 5 | Refuse a name of more than 251 characters |
| T127 | `my $x =- $y;`, `$x =+ $y;` | `-2` and `2`, and `Reversed -= operator`, `Reversed += operator`, as it compiles: a sign hard after `=` with a blank after the sign. `$x =-$y`, `$x = - $y`, `$x +=- 1` and `$x ==- 1` are silent | 5 | Refuse `=`, a sign, and a blank |
| T128 | `say ("a")` and `if $x;` on the next line; `print ("a" .` with `"b") unless $x;` on the next | Each prints, and warns `say (...) interpreted as function`: T76's look along the line is for a modifier as much as a semicolon. `say ("a") if $x;` on one line is silent | 5 | T76's rule, with a modifier after the brackets as with `;` |
| T129 | `my $t = "t"; my $u = "u"; my $x = "a"; my $z = "1"; $t .= ($u = $x . $z); say $t; say $u;` | `ta1` and then `u`: **perl never assigns `$u`**. It makes one operation of the `.=` and the dot, and loses the `=` between them; 5.38 does the same. Also without the brackets, behind a unary plus, behind a test it folds (`1 ? (...) : 0`). Not with `my $w` for `$u`, which is assigned; not when the right side of `.=` is more than the assignment (`($u = $x . $z) . "b"`), not for `$t = $t . (...)`, `($u .= $x)`, `($u = $x x 2)`, or three pieces (`$u = $x . $z . $x`) | 5 | D57: refuse a `.=` whose right side is an assignment of a concatenation |
| T130 | `my $x = 9007199254740994.0; $x++; say $x;` | `9.007199254741e+15`, and `Lost precision when incrementing 9007199254740994.000000 by 1`: perl warns by where the float is, 2^53 or past it, and not by whether the step was lost. One more than 2^53 + 2 is a tie that rounds to 2^53 + 4. Its lines: `++` warns from 2^53 up and below -2^53; `--` above 2^53 and from -2^53 down | 5 | D52: fault on exactly those |

T112 has more to it, found the same way: perl warns of a tested `=`
whose right side it *folds* to a constant, a variable written in it
or not: `if ($x = 0 && $y)`, `$x = "p" . (1 || $y)`, `my $w = (1 ||
$y)`. The refusal now takes a right side for a constant when every
variable in it is behind a test with none (`0 && $y`, `1 ? 2 : $y`),
which is a little more than perl folds.

## Found proposing step 6

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T119 | `my $i = 0; while ((my $x .= "a") && $i++ < 3) { print $x, " " }`; `while ($i < 4) { $i++; next if $i == 2; my $x; $x++; print $x }`; `my $x = 5 while $i++ < 3; say $x;` | `a a a`, `111`, and an empty line with `Use of uninitialized value`: a `my` in a loop's condition or its block is undef again each time round, a `next` before it or not, and one under a `while` modifier is undef afterwards. A `my` in the first part of a C-style `for` is one variable for the whole loop, and gone after it | 6 | Agree; a `my` under a `while` or `until` modifier is refused, as under `if` (T30) |
| T120 | `while ($i++ < 3) { last + 1; }`; `last $l;` and `last "L";` inside `L: while` | The first dies as it runs, `Label not found for "last 1"`; the others leave the loop: what follows `last` or `next` is an expression for a label's name. And `last` is an expression itself: `$i == 2 and last;`, `my $x = last;`, `say last;`, `last while 1;`, `last() if ...;` all leave the loop, in silence | 6 | `last` and `next` are statements: alone, with a label, and with an `if` or `unless` modifier. Anything else is refused |
| T121 | `L: say 1;`, `M: if (...) {...}`, `outer: while`, `N : while`; `last NOPE;`; `A: B: while (...) { last A; }`; `L: while (...) { L: while (1) { last L; } ... }` | perl takes a label on any statement, in any case, with a blank before the colon. A label that names no loop round the `last` dies only when the `last` runs, `Label not found for "last NOPE"`, after whatever came first; so does `A` of `A: B:`, since only the label nearest the loop names it. Of two loops with one label the inner is meant | 6 | A label is on a loop, one to a loop, capitals, hard against its colon; a `last` or `next` that names one no loop round it has is refused as it compiles |
| T122 | `for (my $i = 0, my $j = 9; $i < $j; $i++, $j--)`; `for (...; $i < 3, $j > 7; ...)`; `for ($i + 1; ...)`; `for (...; ...; my $k = $i++)`; `foreach (my $i = 0; $i < 3; $i++)` | The first is the loop it looks like. A comma in the condition warns `Useless use of numeric lt (<) in void context`, and only its last part is tested. A first or third part that only has a value warns `Useless use of addition (+) in void context`. A `my` in the second or third part is taken, and `foreach` is `for` | 6 | Q3: a comma joins assignments and steps in the first and third parts only; `my` in the first only; the word is `for` |
| T123 | `while () { last if $i++ > 2; }`; `until () { ... }` | `4`: an empty condition is true for `while`, and `until ()` doesn't compile. `for (;;)` is the loop with no condition | 6 | Refuse `while ()`: `while (1)` or `for (;;)` says it |
| T124 | A `while` whose condition warns the second time it is tested, over several lines | The warning names the line of the last statement the block ran, not the line of the `while`: perl keeps no line for a condition, and says the one it was last at. The first time, it is the `while`'s line. In a C-style `for` it is the line of the `for`, for the condition and the third part, every time; under a modifier, the line the statement starts on (T118) | 6 | A fault in a loop's condition names the line of its `while`, `until` or `for` (D34): the language's own line, where perl's is an accident |

`do BLOCK while COND` is T64: the block runs before the test. T64 has
more to it: a `last` in that block leaves the loop *round* the `do`,
in silence (`while ($i++ < 3) { do { last; } while (0); say "in"; }`
prints nothing), and with no loop round it dies, `Can't "last" outside
a loop block`. T32 has more too: `next` in a bare block leaves the
block, as `last` does, and one `last` inside two bare blocks leaves
the inner.

## Found building step 6

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T131 | `my $i = 9223372036854775806; while ($i > 0) { $i++; say $i; }` | Without end: where the language stops with `integer overflow`, perl goes on in silence, `9223372036854775808` and up as an unsigned integer and past 2^64 as a float, and the loop the fault would have ended runs for ever. The same for any fault perl only warns of (`"zero" == 0` warns once and is true). Run by a test it filled 19 GB of disk in two minutes, and a checker that kept perl's output in memory would have filled that | 6 | A fault test's loop is counted by something the fault doesn't touch. And the harness doesn't trust that: a test that prints past a limit is stopped by the system, in `t/run.sh` and in `t/checks.py` |

## Found proposing step 8

T1, T19, T28, T31, T55 and T60 are this step's from before. T1 has
more to it: an argument is read late as an operand is (`show($x,
set())`, with `set` making `$x` 9, hands `show` 9; `show($x, $x++)`
hands it 2 and 1; `show($x + 0, set())` hands it 1), and what a sub
returns is a copy (`get() + step()` is 6 where `$total + step()` is
106). T28 has more: perl warns as it compiles of a sub named for one
of the words `use v5.42` brings in (`trim`, `true`, `ceil`,
`indexed`), calls `BEGIN`, `END` and `AUTOLOAD` by itself, and takes
`x`, `any`, `main` and `STDOUT` as names without a word. T31: a sub in
a bare block or an `if` is as one at the top; one inside another sub
warns `will not stay shared`. T60: `last OUT;` in a sub leaves the
caller's loop, with a warning.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T132 | `my $x = "a"; sub ch() { $x = "b"; return "c" } say $x . "-" . ch();`; `say(($x . "-") . ch());`; `$t .= $x . ch();` | `b-c`, `b-c`, and `tbc`: T117 through a call. The row of dots is one operation, and reads `$x` after `ch` has run. `$x . ch()` is `bc` both ways (D14) | 8 | Q3 of step 8: refuse a concatenation in which a later piece calls a sub that can change a variable an earlier piece reads |
| T133 | `sub f() { return; } sub g($x = "default") { ... } say g(f());`; `say f();`; `my $v = f();` | `g`'s default: a sub that returns nothing is no argument at all. `say f();` is an empty line, in silence. `$v` is undef. A sub with an empty body is the same | 8 | Q5 of step 8: undef to a scalar call, as perl; a fault where perl wants a list, until step 10 |
| T134 | `bump(); my $x; say defined($x) ? "d[$x]" : "u"; sub bump() { $x++ }` | `d[1]`: a `my` at the top level doesn't empty its variable, and a sub written after it may be called before it runs. (A sub written *before* the `my` can't name the variable at all) | 8 | Agree: a file variable has a slot of its own, undef as the program starts, and its `my` stores nothing |
| T135 | `sub e($p) { return $p + 10 } my $n = -e(2);`; `say 5-f(2);` | undef, in silence: `-e` is the file test, of a file named `2`. So for 26 letters, `b c d e f g k l o p r t u w x z A B C M O R S T W X`. `- e(2)`, `-(e(2))` and `-ee(2)` are -12. `5-f(2)` doesn't compile | 8 | Refuse a minus hard against a name of one letter |
| T136 | `say f (1); sub f($x) { ... }`; `say v65(); sub v65() { ... }` | Neither compiles, and both do with the `sub` first: `f` is taken for a file handle, and `v65` for a version string. `say f(1);`, `say F(1);`, `my $r = f (1);` and `f` on one line with `(1)` on the next compile either way round | 8 | Refuse a blank between a call's name and its bracket after `say` or `print`; refuse `v` and digits as a sub's name |
| T137 | `sub f($x, $y) { return $x + $y } say f(1,,2);` | `3`: two arguments. `f(1, 2,)` is too, and a signature may end in a comma. `f(,1,2)` doesn't compile | 8 | Refuse two commas together; one after the last argument or parameter is as perl has it |
| T138 | `my $y = 10; sub f($x = $y, $y = 2) { return "$x $y" } say f();`; `my $x = 3; sub g($x = $x) { return $x }` | `10 2` and `3`: a default is resolved before its own parameter and those after it exist, and finds the file's variable of that name. With no such variable it doesn't compile | 8 | Agree: the resolver brings each parameter into scope after its default |
| T139 | `sub a1() { return (5) + 1 }`; `my $x = return 5;`; `return 1 + return 2`; `$c and return "t";`; `sub h($x = return 7)`; `return $v or 9;`; `return;` at the top level | 6 (`return` is not a function: `say (5) + 1` is another matter); 5; 2; `t`; 7: `return` is an expression, anywhere. `return $v or 9` warns of precedence, and at the top level perl dies as it runs, `Can't return outside a subroutine` | 8 | `return` is a statement: alone or with an expression, with an `if` or `unless` modifier, inside a sub. Anything else is refused |
| T140 | `sub f() { say "hi" } my $x = f();`; a sub that ends in a `while`; `sub a4($x) { $x * 2 }`; `sub f($x) { $x * 2; return 1 }` | 1; an empty string; 8, in silence; and the last warns `Useless use of multiplication`. A value alone is a statement only where it is the sub's last, and `if ($x) { $x * 2 }` as the last is silent too | 8 | D18, and Q4 of step 8: a last statement that is an expression is the sub's value, a value alone is allowed there and nowhere else, and a sub that ends any other way has none |
| T141 | `sub f($x, $x) { ... }`; `sub f($x) { my $x = 5; ... }` | Each warns as it compiles, `"my" variable $x masks earlier declaration in same scope`, and the second `$x` wins. A parameter of a file variable's name hides it in silence | 8 | Refuse the first two (D15); agree with the third |
| T142 | `sub d($n) { return $n == 0 ? 0 : 1 + d($n - 1) } say d(98);`, `say d(99);`; `ev` and `od` calling each other, 150 deep and 250; `{ no warnings "recursion"; say d(200); }` | Nothing; `Deep recursion on subroutine "main::d"`, once, when the 100th call of `d` is open; nothing at 150, where each has 75 or 76 open, and a warning for each at 250. The pragma silences the calls written in its scope: round the first call only, the warning still comes from the call inside `d`. At the top of the file it silences all | 8 | Q1 of step 8 |

## Found by the review of step 8

`briefs/step8-review/FINDINGS.md` has each with its program. T135 has
more to it: `-t(2)` is defined, an empty string; the file test is
taken wherever a minus is hard against one letter (`!-e(3)`, `(-e(3))`,
an argument `-e(3)`, `-e (3)`), and `$q -e(3)` and `26-e(3)` don't
compile; so the refusal is the lexer's. T136 too: the file-handle
guess is made for the first word after `say` or `print` through any
number of opening brackets (`say((f (1)));` doesn't compile before
`sub f`, 22 shapes of 22), and a version string is `v`, a digit, and
then digits or underscores (`v1_0`). T28: `else elsif for foreach
unless until while` were in neither list `step8-names.py` used, and
none is a sub's name (66 of 3,455, then, not 59 of 3,448). And T132 is
not a rule to write expected output from: `"<" . ($x . "-") . ch()`
is `<a-c` where `($x . "-") . ch()` is `b-c`.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T143 | `sub g($p = "d") {...} my $n = 0; say g(("a") x $n);`; `cnt(("a") x 2)`; `sub three() { return ("a") x 3 }`; `sub last2($x) { ($x) x 2 }` | `g`'s default; two arguments; three values to a list and `aaa` to a scalar: a bracketed left operand of `x` repeats a *list* in an argument, a `return` and a last statement, through `? :` and `\|\|` too (T101, which a call can now count). In a default it is scalar, `aa` | 8 | Refuse it in those three places, as T101 does for `say`, until step 10 |
| T144 | `my $g = 1; sub bump() { $g = 9; return 5 } sub f($x //= bump(), $y = 0) {...} say f(undef, $g);` | `5,9`: perl copies each argument when it reaches that parameter, and a `//=` or `\|\|=` default runs in between. `f(undef, $g + 0)` is `5,1` | 8 | Agree: a sub is handed where its arguments are, and copies each as its parameter's turn comes |
| T145 | `sub a($x, $c) { $x * 2 if $c } say a(4, 0);`; `sub c($x, $c) { $x = 7 unless $c } say c(4, 3);` | `0` and `3`: a last statement under a modifier is worth its test when the test stops it. No `Useless use` for the value alone | 8 | A last statement with a modifier has no value, as an `if` (D18); a value alone with a modifier is refused |
| T146 | `cnt((none()))`, `cnt(+none())`, `cnt((1 and none()))`, `cnt((none()), "z")` with `sub none() { return; }` | No argument each time, and `"z"` the first: list context goes down through brackets, a unary plus, and the right of `and` and `or`, as through `? :` and `\|\|`. `xor`, `!` and the left of anything are scalar | 8 | The flag is passed down through all of them, so D71's fault is reached |
| T147 | `bump(); my $x += 10; say $x;` with `sub bump() { $x++ }` after; `my $s .= "a";`, `my $d //= 10;` | `11`, `qa`, `1`: T134 for a `my` with an assigning operator | 8 | Agree, as T134 |
| T148 | `my $n; sub v($x) { $x * 2 } v($n);` | A warning, `Use of uninitialized value $x in multiplication`: a void call still works its value out | 8 | Agree: nothing is skipped under void, so the fault comes |

## Found proposing step 9

T5, T9, T13, T14, T21 and T68 are this step's from before. T5 has
more to it: a `push` in the loop makes the walk longer (`1 2 3 11
12`), a `shift` skips an element, and a new list assigned to the
array is walked from where the loop was; the same through `(@a, @b)`,
a slice, `? :`, a named element `($a[0], $a[1])`, `(@a, ())`, and
from a sub the block calls. A range is fixed when the loop starts
(`for my $i (0 .. $#a)` with a `push` inside walks the old indexes),
and its variable may be assigned in perl. T68: `my $g = (@a, 9);`
warns too. T14: `for (1, 2)` walks `$_`.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T149 | `my @a = (1,2,3); say $a[0] + ($a[0] = 10) + $a[0];`; `say $a[0] + shift(@a);`; `say $a[2] + pop(@a);`; `say $a[0] + chg();` with `chg` storing 50; `say $a[1] * splice(@a, 0, 1);`; `say $a[0] + (@a = (7,8))[0];`; `f(undef, $a[1])` and `f(@a)` with a `//=` default that stores to `$a[1]`; `two($a[0], chg())` | `30`, `2`, `6`, `51`, `2`, and `7` with a warning for a value that was freed; the default's `9` both times; `50\|1`: an element as an operand or an argument is the container, read late, and one that has left the array is still read. `@a + grow()` is the count before `grow`: a count is a value at once | 9 | Q1 of step 9: an element is read where it stands, and an expression whose later part can change that array is refused |
| T150 | `my @f = @a \|\| (9);` for an array of three; `my @d = @e \|\| (1,2);` for an empty one | One element, `3`; two: the left of `\|\|` is one value, the count | 9 | Agree: an array where one value is wanted is its count |
| T151 | `my $x = @a[0,1];`; `my $s = splice(@a, 0, 2);`; `my $n = (my ($p, $q) = @a);`; `my $c = () = (4,5,6);`; `my $x = (1..3);` | The slice's last, `5`; the last removed, `5`; the count of the right side, `3` and `3`; and the last is perl's flip-flop, with a warning about `$.` | 9 | Refuse a slice, a range, `splice` and a list assignment where one value is wanted (Q3 for the assignment) |
| T152 | `my $x = pop @a + 1;`; `my $x = pop @a \|\| 0;`; `my $x = shift;` at the top level | Doesn't compile (`pop on scalar is now forbidden`); `6`; undef: `shift` alone shifts the program's arguments, and in a sub `@_` | 9 | `pop` and `shift` take brackets unless the array ends the expression, and always name an array |
| T153 | `my @a = (1); my $v = $a[1e30]; say defined($v) ? "d" : "u";` | `d`: an index too large for a whole number wraps to one that is there | 9 | Fault |
| T154 | `("a".."e")`, `("08".."11")`, `("a".."5")`, `("1".."3")`; `(1..$u)` | 5 letters; `08` to `11`, four strings; 26; and 1 to 3: a range of strings is string increment, unless both look like numbers. An undef end warns | 9 | Fault on a string or an undef for either end of a range |
| T155 | `for my $x () { say "never"; }` | Doesn't compile | 9 | Refuse an empty list after `for my $x` |
| T156 | `fill(); my @a; say scalar(@a);` with `sub fill() { push @a, 1, 2; }` after | `2`: T134 for an array. `my @a = ();` empties it | 9 | Agree: a file's array has a slot of its own, empty as the program starts, and its `my` stores nothing |

## Found by the review of step 9

`briefs/step9-review/FINDINGS.md` has each with its programs. One line
covers most of them: **perl's lists hold every container, not only an
array's elements**: a scalar variable, a whole array, a slice, `$#a`,
and the targets of an assignment; and three forms don't run left to
right.

| | Program | perl prints | Step | Way out |
|---|---|---|---|---|
| T157 | `my @b = ($x, bump());` with `bump` making `$x` 9; `say $x, bump();`; `my ($p, $q) = ($x, bump());`; `@b = ($i, $i++);`; `@b = (@a, chg());` with `chg` storing to `$a[0]`; `for my $x (@a, chg())` | `9 5` each time; `2 1` for `$i` of 1; the stored 50 first: a variable or an array in a list is read when the list is used, through a list repeat, a list slice and `? :` too. In the `foreach` the store comes before any freeze | 9 | A later item of a list may not change a variable or an array an earlier item names: refused, by the walk |
| T158 | `$a[$i] = ($i = 2);`; `$a[bump()] = $a[0];` with `bump` storing 99; `($i, $a[$i]) = (1, 5);` | Stored at 2; 99 stored; `$a[0]` is 5: `=` works its right side's calls out, then the target's index, then reads the right side and stores; a list assignment works out every target's index before it stores anything | 9 | Agree on the order; an index of a target is a later part, to the walk |
| T159 | `$a[$i] += ($i = 2);`; `$a[0] += shift(@a);`; `$a[$#a] += pop(@a);`; `$e[5] //= push(@e, 1);` | Index 0; `2 3`, the sum gone with the element that left; `1 2`; seven elements: an assigning operator finds its element *before* its right side runs, and keeps it though it has left the array | 9 | Agree on the order; refuse a right side that can change the size of the target's array |
| T160 | `my @a; $a[5] &&= 1; say scalar(@a);`; `$e[-1] &&= 5;`; `$a[-9] += p(5);` | 6: the target is made though nothing is stored; before the start it dies, and before `p` has run | 9 | Agree: an assigning operator or a step makes its target first, and faults first |
| T161 | `for my $x ($a[5]) { }` on an empty array; `for my $x (@b[5, 6]) { }`; `f(@c[5, 6])`; `for my $x ($a[-5])` | The array is 6 long, 7, 7; and the last dies. A plain read, `//`, an element as an argument, `push`'s list and an assignment's right side make nothing | 9 | Fault: an element or a slice past either end in a `foreach`'s list, a slice past either end in a call |
| T162 | `for my $x ((@a) x 2)`, `((@a)[0, 1])`, `(@a && @b)`, `($#a)`, `(substr($s, 0, 1))`, each with a change in the block; `for my $x (@a \|\| @b)` | The change shows in every one; the last runs once, over the count 3 | 9 | The freeze is of every array named anywhere in the list; Q2's refusal of every scalar named anywhere in it |
| T163 | `say((p(10), p(20))[p(1)]);` with `p` printing; `say(($i, 5)[$i++]);` | `<1><10><20>20`; 1: a list slice works its indexes out before its list | 9 | Agree |
| T164 | `my @b = (@e)[0, 1];` for an empty `@e`; `(1, 2, 3)[5, 6]`; `f((@e)[0])` | None; two undefs; no argument: a slice of an empty list is empty, in a list | 9 | Agree |
| T165 | `splice(@a, 0, 1e30)`, `splice(@a, 1e30)` on five elements | Four removed; one: a number too large wraps (T153) | 9 | Fault: an offset and a length go by the index's rule |
| T166 | `for my $i ($lo .. $lo + 1)` with `$lo` the smallest integer; the same range as a list, and beside another item in the `foreach` | Dies, `Range iterator outside integer range`; two values; walked. The top three integers are walked, and the loop ends | 9 | Fault in a `foreach` over one range on an end below -2^63 + 513; the counter must not pass the largest integer |
| T167 | `@a[0]`, `@a[$j]` | A warning as it compiles, `Scalar value @a[0] better written as $a[0]`; not for `@a[0,]`, `@a[(0)]`, `@a[@b]`, `@a[0 .. 0]` | 9 | Refuse a slice whose index list is one item that is not an array, a slice, a range, a call or in brackets |
| T168 | `my @a = 1, 2, 3;`; `defined(@a)`; `say(1, 2)[1];`; `sub f3() { ($p, $q) = (4, 5, 6) }` to a scalar and to a list; `(1, 2) x 2 x 2` | One element and two warnings; doesn't compile; doesn't compile; 3 and two values; one value, `2222` | 9 | Refuse each: a comma after an assignment's right side, `defined` and `length` of an array, `[` after a call's own brackets, a list assignment as a sub's last statement with its value used (no value, D18), a comma list on the left of an `x` that is itself where one value is wanted |
| T169 | `for my $x (1 ? $a[5] : 0)`, `(0 \|\| $a[5])`, `(1 && $a[5])`, `(($a[5]) x 2)`, `(+$a[5])` on an array of one; and `($a[5] \|\| 0)`, `($a[5] // 1)`, `($a[5] ? 1 : 2)`, `(($a[5], 1)[0])` | The first five make the element, and the array six long; the last four make nothing | 9 | T161's fault reaches an element through a branch of `? :`, the right of `\|\|` `&&` `//`, a list repeated and a unary plus; a slice of a list is held to it too, where perl would not have made it |
| T170 | `for my $x (@a) { my $x = 5; print $x; }` | `55`, and no warning: the block is a scope inside the loop's | 9 | A `my` of the loop variable's name in the block is another variable, as it is to perl |
| T171 | `my $x = 7; for $x (1, 2) { print $x; } say $x;`; `foreach (my $k = 0; $k < 2; $k++) { print $k; }` | `127`: the variable is lent to the loop and given back; `01`: `foreach` is `for` | 9 | Refuse both: a loop over a list declares its variable, and `for` is the loop of three parts (D81) |
| T172 | `my $n = 3; for my $i (1 .. $n) { $n = 1; print $i; }` | `123`: a range's ends are fixed as the loop starts | 9 | Refused all the same, by D77's one rule (a scalar named anywhere in the list); `my $end = $n;` says it. The language is the stricter here, and nothing is WRONG either way |
| T173 | `sort { push @log, "$a$b"; $a <=> $b } (5,3,8,1,9,2,7)`; `sort { 1 } (1..5)`, `sort { -1 } (1..5)`; `sort { $r } (1, 2)` for `$r` of 0.5, 2147483648, 4294967296; `sort { $a <=> $b }` of 2^53 + 1, the Num 2^53 and 2^53 | `53 81 92 31 38 58 27 79 12 23 37 75 78 89`, every run; `5 4 3 2 1` and `1 5 3 2 4`; equal, less, equal: the block's value is cut to a whole number and to 32 bits; `9007199254740992 9007199254740993 9.00719925474099e+15` | 10 | Q1: perl's merge ported, so that every comparison is perl's. The block's value: a whole number, and a fault outside 32 bits |
| T174 | `sub f() { my @s = sort { return 5 } (3,1,2); return "@s"; }`; the same with `map` | `2 1 3`: the `return` ended the comparison; `5`: it ended the sub | 10 | Refuse `return` in a `map`, `grep` or `sort` block |
| T175 | `map { "a", $_ } @x`, `map { 1, $_ } @x`, `map { } @x`, `grep { 1, 0 } @x`; `map { $_, 1 }`, `map { 1.5, $_ }`, `map { -1, $_ }`, `map { true, $_ }`, `map {; }` | The first four don't compile: a hash, to perl's guess. The rest are blocks | 10 | Refuse a block whose first token is a string, a number or a word with a comma after it, and an empty one (D21, T54) |
| T176 | `map { if ($_ > 1) { $_ } } (1,2,3)`; `grep { ($_, 0) } (1,2,3)` | Three values, the first the empty string; none, with a warning | 10 | Refuse a block that does not end in an expression; one value in a `grep` block, by step 9's rule |
| T177 | `map { $_ } $a[5]`, `grep { 1 } $a[7]`, `map { $_ } @a[9, 10]` on an array of one; `join(",", $a[9] // 0)`, `reverse(...)`, `sort { } $a[9], 1` | 6, 8 and 11 long; `join` and `reverse` make nothing, and a `sort` whose block is `{ $a <=> $b }` (but see T188) | 10 | D80's fault for an element or a slice past the end in the list of a `map`, a `grep`, a `for` and (T188) a `sort`; not of `join` or `reverse` |
| T178 | `my $n = grep { $_ > 1 } @a; my $m = map { ($_, $_) } @a;`; `my $r = reverse("abc", "def");`; `my $s = sort { $a <=> $b } @a;` | `2 6`; `fedcba`; undef and `Useless use of sort in scalar context` | 10 | Q3: `grep` and `map` are the count; `sort` and `reverse` are refused where one value is wanted |
| T179 | `@a = sort { push @log, "$a[0]$a[1]$a[2]"; $a <=> $b } @a`; `my @b = sort { $a[0] = 0; $a <=> $b } @a`; `sort { $a++; 0 } @c`; `@a = sort { push @a, 1; $a <=> $b } @a` | `312 312 312`; `0 1 2` for both arrays; `@c` is `5 1 3`; the pushes are lost | 10 | The array is frozen while it is sorted, and `$a` and `$b` are read-only |
| T180 | `sub show() { return $_ * 2 } map { show() } (1,2)`; `sub cmpf() { return $a <=> $b } sort { cmpf() } (3,1,2)`; `for (@a) { $_ *= 2 }`, `map { $_ *= 2 } @a`, `grep { $_++ } @a`; `map { $p = 7; $_ } ($p, $q)`; `map { length } @x`, `say for 1, 2`; `map lc, @x`, `map ($_ * 2), (1,2)` | `2 4`, `1 2 3`: one global `$_`, and `$a` a package's; the array rewritten each time; `7 2`; `$_` meant; `map` of nothing, and a warning, for the last | 10 | `$_`, `$a` and `$b` are seen in the block that binds them alone, read-only; D77 for the binders; Q4 for the forms without a block and without `$_` |
| T181 | `my @r = map { push @a, 9 if @a < 6; $_ } @a;`; `for (@a) { push @a, 8 if @a < 8; print $_; }`; `push @a, 9 for @a;` | `1 2 3`, the array six long; the loop walks what was pushed; the last never ends | 10 | The freeze, for every binder. A fault test's loop ends by something the fault doesn't touch (T131) |
| T182 | `sub f(@rest, $x)`, `sub g(@r = (1,2))`; `sub g(@all) { $all[0] = 9 }`; `join(@a, 1, 2)` for an `@a` of two | Neither compiles; the caller's array is not changed; `122`: the separator is one value | 10 | A slurpy parameter is last, has no default, and is a copy; `join`'s first argument is one value |
| T183 | `my $x = f()` for an `f` that ends `return (4, 5, 6)`, `return reverse @a`, `return map { $_ } (4,5)`, `return splice(@a, 0, 2)`, `return sort { } @a`, `return 1 .. 3`, `return $c ? @a : 0`; `return ()`, `return (7)` | 6; `321`; 2; 8; undef; the empty string and a warning (the flip-flop); 3 or 0; undef; 7 | 10 | D18's fault for each shape, by the tree; `return ()` is `return;`, `return (7)` one value |
| T184 | `$n += $_ for 1, 2, 3;`, `push @b, $_ * 2 for (1,2), 3;`; `$_ = 5; for (1) { } print $_;` | 6, `2 4 6`: the modifier takes a list with no brackets; 5: `$_` is given back | 10 | `STATEMENT for LIST;`; `$_` outside a binder is refused |
| T185 | `my @r = (reverse(@a), chg());` with `chg` storing 50 to `$a[0]`; the same with `(grep { 1 } @a)`, `(sort { $a <=> $b } @a)`, `(map { $_ } @a)`; `join("-", reverse(@a), chg())` | `3 2 50 7`, `50 2 3 7`, `50 2 3 7`; `1 2 3 7` for `map`, which copies; `3-2-50-7` | 10 | D87: `grep`, `sort` and `reverse` name what their list names, for D76's walk; found by the review |
| T186 | `join($sep, chs(), 2, 3)` with `chs` setting `$sep` to `+` | `1+2+3`: the separator is read when `join` runs | 10 | The separator is the first item of `join`'s list, for D76's walk |
| T187 | `my @d = (3); $d[3] = 1; @d = sort { ($a // 0) <=> ($b // 0) } @d;`; the same for `(3, undef, undef, 1)`; into another array; under `reverse` | 2 elements; 4; 4; 4: the in-place sort drops what was never stored | 10 | Fault: an undef in an array sorted in place |
| T188 | `sort { ($a // 0) <=> ($b // 0) } @a[0 .. 3]`, `sort { 0 } $b[5]`, `sort { 1; ... } $c[5], 1` on arrays of one | 4, 6 and 6 long: a `sort` with a block makes the elements, unless the block is one of the four perl throws away (T177) | 10 | D80's fault in a `sort`'s list, whatever the block |
| T189 | `sort true, false`; `sort false, 3, 2`; `sort k(), 3, 1`; `sort(k(), 3, 1)`, `sort +k(), 3, 1` | `\|true`; `2\|3\|false`; `1 3`: `k` is the comparator; `1 3 5` for the last two | 10 | Refuse a word that is not perl's own first after `sort`; `sort` takes no brackets of its own |
| T190 | `sort { $a <=> $b } ("abc")` and `sort (undef)` through arrays of one; `sort { 1; 0 } ...` of the same; `(sort (@a), 9)`; `join(undef, "a")` | A warning for the one value; none with another block; `sort (...) interpreted as function`; a warning for the separator that is never used | 10 | A lone value is looked at, for the forms perl throws the block of; the separator is made a string always |
| T191 | `for my $i (1 .. 3) { last for 1, 2; print $i; }`; `f(1, $v, bump())` for `sub f($x, @rest)`; `for (1, 2) { my @r = map { $_ * 10 } ($_, 5); }` | `123`: `last` left the modifier's loop; `1\|9 5`: the slurpy is filled late; `10 50` and `20 50`: the list sees the outer `$_` | 10 | No `last`, `next` or `return` under a `for` modifier; a slurpy parameter is filled at its turn; a binder's list is outside its binding |
| T192 | `map { { 5 } } 1`; `for () { }`; `$n += $_ for 1 .. 3 if 1;`; `map { say $_ -1 } (5)`; a `next` and a `last` for a loop inside a `map` block; `sort { $a <=> $b or $a cmp $b }` | A hash, and a warning; two syntax errors; dies, a file handle; fine; fine | 10 | Refuse the first four; allow `last` and `next` to a loop inside the block, and a word operator in a block's last statement |
| T193 | `return 1, 2;`; `sub g(@r,)`; `my @b = reverse;`; `(5, 6, 7)[two()]` where one value is wanted, `two` giving `(1, 0)`; `sub h(@v) { my @v = (1); }` | Both returned; a comma after a slurpy compiles; the empty list; 5, the last of the slice; a warning that it masks the first | 10 | Found building 10a. Refuse each: a list after `return` is in brackets, a slurpy parameter is the last thing in a signature, `reverse` has something to reverse, and a slice by a call that gives a list is no one value |

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
- **`PERL_HASH_SEED=1` to `8` are nearly one seed.** The value is hex
  for the front of a 256-bit seed, the rest zero
  (`PERL_HASH_SEED_DEBUG=1` shows `0x1000...`), and
  `Hash::Util::hash_value("pine")` is 1813974225 under every one of
  them: only the order of walking the buckets moves. `my %h = (pine
  => 1, yew => 2, nut => 3); my @k = sort { 0 } keys %h;` puts `yew`
  second under none of the seeds 1 to 300, and in 9 of 40 runs
  without a seed. The check's seeds are 64 hex digits each.
- **A sort with a tie shows the hash's order**, and reading can't see
  a tie: `sort { $count{$b} <=> $count{$a} } keys %count` with two
  words at 7. Under eight real seeds two tied keys agree by luck about
  once in 128. Tests break their ties; steps 10 and 12 write tests
  that sort, so they are where this bites first, and a ninth seed is
  cheap if one in 128 turns out to be too many (D10 says eight).
- A program more than 100 calls deep makes perl warn, so it can't be
  a `same` test as D10 stands. Step 8.
- Plain `perl FILE` prints `é` as the single byte E9, in silence;
  with `-CSDA`, or with `use open ':std', ':encoding(UTF-8)';` in the
  file, it prints the two bytes of UTF-8. The oracle ran perl with
  `-CSDA` until step 3 (D24), so "the same file, given to perl" was
  true only with a flag the file didn't carry. Closed by D39: the
  oracle runs perl plain, and `t/checks/same-latin1-no-open` and
  `same-wide-no-open` go red if the flag comes back.
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
- **What a review got past the oracle check, and which step closes
  it.** A reader was given `t/checks.py` and perl and asked to get a
  wrong test through. What was cheap is closed (the seeds; `scalar`,
  `sort` and a string that runs code in the reading rule; headers
  that `t/run.sh` and the check read differently; `PERL_HASH_SEED` or
  `PERL5OPT` in a test's `# env:`; a `.stdout` beside a real test)
  and each has a fixture in `t/checks/`. What is left:
  - A `dies` test in which perl also warns, or which ends with `exit
    255` and no `die`, is accepted: perl's stderr is the `.expected`,
    whatever is in it. Step 15, with `die` and `warn`.
  - A test that writes a file leaves it for the next of perl's nine
    runs (one to compile, eight seeds), so the check fails it the
    first time, blaming the seed, and passes it ever after. Step 21:
    each run gets a clean place to write.
  - perl is given an environment of `PATH` and the seed, and a pipe
    for stdin; the compiled program gets the whole environment and a
    file. `%ENV`, `-t`, `localtime` and `time` show the difference.
    Steps 21 and 22: one environment for both, and `TZ` pinned.
  - `-CSDA` is not `perl FILE` for a character past ASCII: closed at
    step 3 (D39).
  - A `new` test is not checked at all. Step 27, where the first one
    is.
  - The reading rule pairs quotes by counting them, so an apostrophe
    in a heredoc, a `q{"}`, a `tr/'//` or a `#` in a pattern hides
    what follows; and it doesn't know `% h` with a space, `%::h`, or a
    dumper. Steps 16 and 19 bring those constructs and teach the
    reader each one; until a step does, the compiler refuses them.
  - `no warnings`, `$SIG{__WARN__}` and closing STDERR keep a warning
    off stderr. None is in the language (D16), so the compiler is the
    net: a test must compile. The same goes for `BEGIN { exit }`,
    which makes `perl -c` say nothing about the rest of a file.
- A program's own `sub trim` or `sub ceil` is still the one called
  under `use v5.42`, not the builtin, and perl says so twice as it
  compiles (`Prototype mismatch: sub trim ($) vs none`, `Subroutine
  trim redefined`). So it is refused on both counts (D21, D15).
