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
| T111 | `my $x = 5; say($x -1);`, `say $x +$y;`, `print $x .5;`, `say $x ++;` | The first three die as they run, `Can't use string ("5") as a symbol ref`: perl takes a variable that comes first after `say` or `print`, brackets or not, for a file handle when what follows the blank after it could begin a value. The last, `say(($x -1))` and `say $x <true` don't compile. `say $x - 1`, `say $x-1`, `say +$x -1` and `say $x ?1 : 2` are fine (T26) | 5 | Refuse, by perl's own list: after the blank, a sign or `?` hard against what follows it, a dot and a digit, `*`, `%`, `<` or `&` hard against a name, `/` hard against anything but `=` or `/` |
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
| T117 | `my $x = 3; say $x . "a" . ($x = 5);`, `say((1 ? $x . "" : 0) . ($x = 5));`, `say(($x . "a") . ($x = 5));` | `5a5`, `55`, `5a5`: perl joins a row of dots as one operation (`multiconcat`) and reads every piece when it runs, brackets or not, and after folding what it can. `my $y = $x . "a"; say $y . ($x = 5);` is `3a5`, and so are `($x . "a") x 1 . ($x = 5)` and `($x + 0) . "a" . ($x = 5)` | 5 | D57 (open): refuse a concatenation in which a later piece changes a variable an earlier piece reads |
| T118 | `say 1` / `if` / `$u + 1;` on three lines, `$u` undef; the same in an `elsif (` whose test is on the next line | The warning names the line of `say`, the first of the statement, and the line of the `elsif`: not the line the test or the `if` is on | 5 | A modifier's test is at its statement's line; an `elsif`'s at the `elsif` (tests 547 to 549) |

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
