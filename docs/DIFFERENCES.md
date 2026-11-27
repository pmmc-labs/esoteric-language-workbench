# Where Curly and Perl differ

For a reader who knows Perl: what will be different, sorted by how
much of Perl's character each difference takes, how likely it is to
be met, and where. It decides nothing. Where it and a decision
disagree, [`DECISIONS.md`](DECISIONS.md) is right and this file has a
mistake.

**Built** means steps 0 to 12, 13a, 15 and 16a to 16c: numbers,
strings, booleans, variables, control, subs, arrays and lists, `map`,
`grep`, `sort`, interpolation, hashes, references to arrays and hashes
with elements through them, `die`, `try`, `catch` and `warn`, and `q`,
`qq`, `qw`, heredocs, `sprintf`, `printf` and the rest of the string
builtins. What is decided and not built is at the end.

## How this file is kept

It is part of the process (D103), and `make test` holds it three
ways (`t/checks.py differences`):

- **Every program in "Run for this file"** is run under perl 5.42
  and under the compiler, and must do what its row says.
- **Every rated row** has a Feel, a Met and a Where from the lists
  below, and names a decision that exists; and it stands in the
  section its ratings belong to.
- **Every decision in the log is accounted for**: cited somewhere in
  this file, or listed under "Decisions that say nothing here". So a
  step that adds a decision can't finish without saying what, if
  anything, a Perl programmer will notice.

What it says perl does comes from the decisions and
[`TRAPS.md`](TRAPS.md), which `briefs/claims.py` holds to perl, and
from the programs run here.

**The ratings are a judgement**, the builder's, and are Stevan's to
move. The only evidence behind Met is the census: of 5,786 Perl
programs other people wrote to break Perl implementations, 2,633 are
refused by design, and the counts below are of those, by the first
thing each was refused for. They lean toward old Perl and toward
trick programs.

- **Feel**: what is lost. An **idiom** is something a Perl programmer
  writes on purpose and thinks of as Perl. A **habit** is ordinary
  code with nothing distinctive about it. An **accident** is what
  nobody means: a slip, or a corner of the implementation.
- **Met**: **often** (most programs), **sometimes**, **rarely**.
- **Where**: `loops`, `subs`, `printing`, `strings`, `numbers`,
  `data`, `control`, `variables`, `layout` (how a file is laid out),
  `errors`, `objects`, and `old code`, for what is met mostly when
  reading or porting Perl written before signatures and `class`.
- **†** after a decision: Curly is stricter here than it has to be.
  perl's answer could have been agreed with, and one rule with no
  exceptions was cheaper. These are the cheapest to give back.

## The shape of every difference

There is one rule (D2), and every difference follows from it:

> A program Curly accepts is a program perl 5.42 accepts, and when it
> runs without faulting it prints what perl prints, byte for byte.

So Curly never gives a Perl program a *different meaning*. Exactly
one of three things happens to a Perl program:

```
                     +--> refused        a compile error, no binary
   a Perl program ---+--> faults         stops at run time, having printed
                     |                   only the start of what perl prints
                     +--> runs           and prints what perl prints
```

**Refused**: perl accepts it and Curly won't compile it. **Fault**:
perl carries on, with a warning or a guess or in silence, and Curly
stops (`fault: MESSAGE at FILE line N.`, exit 1). A fault can't be
caught (D13).

What perl does *in silence* stays (D15): `"12" + 1` is 13, `"3 " +
1` is 4, and `$x++`, `$x += 2`, `$x .= "a"` on an undef work.

## The map

Perl's syntax and data model are whole: sigils, contexts, lists that
flatten, the operators and their precedence, statement modifiers,
`map` and `grep` and `sort`. What is reduced is terseness and
forgiveness. Curly reads as Perl under `strict`, with every warning
fatal and a severe style policy enforced by the compiler.

| | Met often | Met sometimes | Met rarely |
|---|---|---|---|
| **An idiom** | implicit `$_`; `map EXPR, LIST`; changing a list in place; `... and last`; `@_`; `eval { }`; `bless` | a count from `return @list`; calls without brackets; `local`; `9**9**9`; `sort by_name @a`; `each`; `BEGIN` | string `++`; `() = `; a block to `last` out of; the flip-flop; `redo` |
| **A habit** | `use strict; use warnings;`; `#!`; an undef printed or added | `my $a`; pushing onto the array a loop is over; catching a division by zero; an expression in a string's index; `substr` without brackets; `do { } while` | `unless ... else`; `0 <= $i < $n`; `017`; integers past 2^63 |
| **An accident** | | `say (1 + 2) * 3;`; `my $x = 10 if $c;`; `if ($x = 5)` | everything about 2^53; perl's parsing guesses; the order perl reads a row of dots in |

By where: **loops** take the heaviest loss (the first three rows of
the next section), then **subs** and **objects** for anyone coming
from older Perl, where it is a rewrite and not an adjustment. In
**printing** and **numbers** the one thing met daily is undef.
**Strings**, **data** and **control** lose spellings, not ideas.
Nearly all of the accidents are in **numbers** and in parsing, and a
careful programmer does not meet them.

## Run for this file

Each row is a whole program after `use v5.42;`. `make test` runs
every one under both.

| Program | perl 5.42 | Curly |
|---|---|---|
| `my @a = (1, 2); say for @a;` | `1` `2` | Refused |
| `my @w = ("A", "B"); my @l = map lc, @w; say "@l";` | `a b` | Refused |
| `my @a = (1, 2, 3); $_ *= 2 for @a; say "@a";` | `2 4 6` | Refused |
| `my @a = (1, 2, 3); for my $x (@a) { $x *= 2 } say "@a";` | `2 4 6` | Refused |
| `for my $i (1 .. 5) { $i == 3 and last; say $i; }` | `1` `2` | Refused |
| `sub add { my ($x, $y) = @_; return $x + $y; } say add(1, 2);` | `3` | Refused |
| `sub hi($n) { return "hi $n"; } say hi "bob";` | `hi bob` | Refused |
| `sub f { return 7 } say f(1, 2, 3);` | `7` | Same |
| `sub a() { my @a = (42); return @a } my $x = a(); say $x;` | `1` | Fault: `a returned a list where one value is wanted` |
| `sub f($x) { if ($x) { return "yes"; } } say f(0);` | `0` | Fault: `f has no value` |
| `use strict; use warnings; say 1;` | `1` | Refused |
| `my $a = 1; my $b = 2; say $a + $b;` | `3` | Refused |
| `my $u; say "x: $u";` | `x: `, and warns | Fault: `undef where a string is wanted` |
| `my $x; say $x + 1;` | `1`, and warns | Fault: `undef where a number is wanted` |
| `my $n = "5 apples"; say $n + 1;` | `6`, and warns | Fault: `not a numeric string` |
| `my @q = (1, 2); for my $x (@q) { push @q, 9 if @q < 3; } say scalar(@q);` | `3` | Fault: `an array was changed while a foreach is over it` |
| `my @a = (1, 2, 3); for my $x (@a) { $a[0] = 9; say $x }` | `9` `2` `3` | Fault: `an array was changed while a foreach is over it` |
| `my @a = (1, 2, 3); my $i = 0; say "$a[$i + 1]";` | `2` | Refused |
| `my %h = (a => 1, b => 2); for my $v (values %h) { $h{new} = 1; } say scalar(%h);` | `3` | Fault: `a hash was changed while a foreach is over it` |
| `my %h = (a => 1, b => 2); for my $k (sort keys %h) { delete $h{$k}; } say scalar(%h);` | `0` | Same |
| `my %h = ("a b" => 1); say "$h{'a b'}";` | `1` | Refused |
| `my %h = (a => 1); my $k = "a"; say "$h{a} $h{$k}";` | `1 1` | Same |
| `my %h = (a => 1, b => 2); @h{"a", "b"} = @h{"b", "a"}; say "$h{a}$h{b}";` | `21` | Same |
| `my $s = "abc"; say substr $s, 0, 1;` | `a` | Refused |
| `my @a = ("b", "a"); my @s = sort(@a); say "@s";` | `a b` | Refused |
| `my $i = 0; do { say $i; $i++; } while ($i < 2);` | `0` `1` | Refused |
| `my @a = (1, 2, 3); my $r = reverse(@a); say $r;` | `321` | Refused |
| `my $s = "Az"; $s++; say $s;` | `Ba` | Fault: `not a numeric string` |
| `while (1) { { last; } say "here"; last; }` | `here` | Refused |
| `say 1 < 5 < 3;` | an empty line | Refused |
| `say 010;` | `8` | Refused |
| `say 9223372036854775807 + 1;` | `9223372036854775808` | Fault: `integer overflow` |
| `say 9**9**9;` | `Inf` | Fault: `float overflow` |
| `say (1 + 2) * 3;` | `3`, and warns | Refused |
| `say 0 or 2;` | `0`, and warns | Refused |
| `my $c = 0; my $x = 10 if $c; say defined($x) ? "def" : "undef";` | `undef` | Refused |
| `say 1e15;` | `1e+15` | Fault: `a whole float this size prints two ways in perl` |
| `say 2 ** 50;` | `1.12589990684262e+15` | Fault: `a whole float this size prints two ways in perl` |
| `my $x = "1e16"; say $x + 1;` | `10000000000000001` | Fault: `two values in perl` |
| `my $x = 3; say $x . "a" . ($x = 5);` | `5a5` | Refused |
| `my @a = (1); say $a[0] + ($a[0] = 10);` | `20` | Refused |
| `say "abc" + 1;` | `1`, and warns | Fault: `not a numeric string` |
| `say substr("abc", 5);` | an empty line, and warns | Fault: `substr outside of string` |
| `say 10 / 0;` | dies | Fault: `division by zero` |
| `my $x; $x++; $x += 2; $x .= "a"; say $x;` | `3a` | Same |
| `say "3 " + 1;` | `4` | Same |
| `say 1e15 + 0;` | `1000000000000000` | Same |
| `my @a = (3, 1, 2); my ($min) = sort { $a <=> $b } @a; say $min;` | `1` | Same |
| `my @l = (1, 2); my %s = map { $_ => 1 } @l; say join(",", sort keys %s);` | `1,2` | Refused |
| `my @l = (1, 2); my %s = map { ($_ => 1) } @l; say join(",", sort keys %s);` | `1,2` | Same |
| `my %h = (1, 2, 3); say scalar(%h);` | `2`, and warns | Fault: `an odd number of values for a hash` |
| `my %h = (if => 1, q => 2); say $h{if} + $h{q}, exists $h{x} ? "x" : "no x";` | `3no x` | Same |
| `my %h = (a => 1); my @a = (0); say exists $a[0] ? "yes" : "no";` | `yes` | Refused |
| `my $h; $h->{a}{b} = 1; my @g = ([1, 2], [3]); say ref($h->{a}), $g[1][0];` | `HASH3` | Same |
| `my %h; my $x = $h{a}{b}; say exists $h{a} ? "made" : "no";` | `made` | Fault: `undef where a reference is wanted` |
| `my $r = [1, 2]; say $$r[0];` | `1` | Refused |
| `my $p = [1]; my $q = $p; say $p == $q ? "one" : "two", [] == [] ? "one" : "two";` | `onetwo` | Same |
| `my $r = [1]; say $r + 0 > 0 ? "an address" : "no";` | `an address` | Fault: `a reference where a number is wanted` |
| `my @a = (1); my $r = \@a; say $a[0], ($r->[0] = 5);` | `55` | Refused |
| `my @rows = ([1, 2]); my @c = @rows; $c[0][0] = 9; say $rows[0][0];` | `9` | Same |
| `try { my $x = 1 / 0; } catch ($e) { say "caught"; }` | `caught` | Fault: `division by zero` |
| `sub f($n) { try { return $n * 2; } catch ($e) { return 0; } } say f(4);` | `8` | Same |
| `my $x = 0; $x or die "zero\n";` | dies | Refused |

## 1. Idioms you will miss

What a Perl programmer writes on purpose, and will reach for. This
is where the feel changes.

<!-- rows: idiom; often, sometimes -->

| Perl | Curly | Feel | Met | Where | Decision |
|---|---|---|---|---|---|
| A builtin with no argument means `$_`: `say for @a;`, `grep { defined } @a` | `$_` is always written: `say $_ for @a;`, `grep { defined($_) } @a` | idiom | often | loops | D85 † |
| `map EXPR, LIST` and `grep EXPR, LIST`: `map lc, @w` | A block always: `map { lc($_) } @w` | idiom | often | loops | D85 † |
| A loop variable or `$_` is the element itself: `$_ *= 2 for @a;`, `for my $x (@a) { $x *= 2 }`, `chomp` or `s///` on one | Read-only (108 and 58 of the census's programs). `@a = map { $_ * 2 } @a;`, or `for my $i (0 .. $n) { $a[$i] *= 2 }` | idiom | often | loops | D17 |
| `last` and `next` are expressions: `$done and last;`, `$ok or next;` | Statements: `last if $done;`, `next unless $ok;` | idiom | often | control | D62 † |
| `my ($x, $y) = @_;`, `my $self = shift;`, `$_[0]` | A sub names its arguments in a signature. With none, `sub f { ... }`, it takes any arguments and sees none (about 900 of the census's programs use `@_`) | idiom | often | subs, old code | D17, D105 |
| `eval { ... }; if ($@) { ... }` | Cut, for `try` and `catch` (step 15) | idiom | often | errors, old code | D20 |
| `bless`, `@ISA`, `our`, package variables, `AUTOLOAD`, `can` to find code | One object system, `class`; `package` only names a file's subs (453 of the census's programs; step 17) | idiom | often | objects, old code | D19 |
| A `return` is worked out in its caller's context: `return @list` is a count to `my $n = f();`; `wantarray` | A fault when a list-shaped `return` is reached by a call for one value; `wantarray` is refused. Return the count, or call it for a list | idiom | sometimes | subs | D18 |
| A sub of the program's called without brackets: `hi "bob";` | `hi("bob");` | idiom | sometimes | subs | D21 |
| `sort by_name @a`, `sort $by @a`: a sub to compare by | A block: `sort { by_name($a, $b) } @a` | idiom | sometimes | data | D89 |
| `local $x`, and the variables it is for: `$/`, `$,`, `$\`, `$"`, `$;` | Cut. An array in a string is joined with one space | idiom | sometimes | printing, old code | D17, D22 |
| `9**9**9` for "larger than anything"; `inf`, `nan` | A Num is finite: `float overflow`, `not a number` | idiom | sometimes | numbers | D37 |
| `each %h`; `while (my ($k, $v) = each %h)` | Cut: `for my $k (sort keys %h)` | idiom | sometimes | data | D22, D101 |
| A set or an index built by `map`: `my %seen = map { $_ => 1 } @list;` | Refused, for the comma in the block (perl has to guess whether the braces are a block or a hash): `map { ($_ => 1) } @list` | idiom | sometimes | data | D102 † |
| `BEGIN`, `eval STRING`, a `require` at run time, `do FILE`, `__DATA__` | Cut: the compiler sees the whole program before any of it runs | idiom | sometimes | layout | D20 |
| A dereference without braces: `@$r`, `%$r`, `$$r[0]`, `$#$r`, the commonest spelling in old Perl | The arrow: `$r->[0]`, `$r->{k}`; and for the whole container `$r->@*` or `@{ $r }` (step 13b). (237 of the 795 census programs that wait for references use a spelling without braces) | idiom | often | data, old code | D108 |
| `open(...) or die "...";`, `$ok or die "...";`: a statement joined to `die` by a word operator | Refused, as every statement joined by one is: `die "..." unless $ok;` (a guess: files, at step 21, will make it common) | idiom | sometimes | errors | D146 |
| `chomp(my $line = <STDIN>)`, `my $n = chomp($s)`, `chomp(@lines)`, `chomp;` | `chomp` and `chop` are statements on one scalar variable, `chomp $line;` (about 20 of the census's programs use the rest) | idiom | sometimes | strings | D130, D131 |
| `sprintf($fmt, @args)`, a format made as the program runs | A format is a string literal with no variable in it; pick between literals, or join | idiom | sometimes | printing | D124 |

## 2. Habits that now stop

Ordinary code, nothing clever, that perl takes and Curly doesn't.
Each is a small adjustment; together they are what the first day
feels like.

<!-- rows: habit; often, sometimes -->

| Perl | Curly | Feel | Met | Where | Decision |
|---|---|---|---|---|---|
| `use strict; use warnings;`, and any pragma | Refused: `use v5.42;` is both. Then `use utf8;`, `use open ':std', ':encoding(UTF-8)';`, `no warnings 'recursion';`, and nothing else (57 of the census's programs) | habit | often | layout, old code | D16 |
| A file with no `use v5.42;` | It is the first line, always | habit | often | layout, old code | D16 |
| `#!/usr/bin/perl` on the first line | Refused, on any line: perl reads switches from it | habit | often | layout | D33 † |
| An undef printed, interpolated or joined: the empty string, and a warning | Fault. `$x // ""` says it | habit | often | printing | D48, D15 |
| An undef in arithmetic or a comparison: 0, and a warning | Fault. (`++`, `+=`, `-=`, `.=`, `\|\|=`, `//=` on an undef are silent in perl, and work) | habit | often | numbers | D48 |
| `"5 apples" + 1` is 6, `"" + 0` is 0, `"abc" == 0` is true, each with a warning | Fault: `not a numeric string`. `"12\n"` and `" 12 "` are numbers, as in perl | habit | sometimes | numbers, strings | D40 |
| `my $a`, `my $b` | Refused: they are `sort`'s (40 of the census's programs) | habit | sometimes | variables | D55 |
| Changing an array inside a loop over it: `push @q, ...` in `for (@q)` | Fault, from the block or a sub it calls (the commonest fault in the census: 28 programs). Loop over a copy, or over `0 .. $n` | habit | sometimes | loops | D17 |
| Changing a hash inside a loop over its `values`, over itself, or over a slice or an element of it: `for my $v (values %h) { $h{new} = 1 }` | Fault. A loop over `keys %h` may change it: the keys are copies | habit | sometimes | loops, data | D17 |
| `for my $i (0 .. $#a) { ... push @a, ... }` | The same fault: `$#a` names `@a`. Take it into a `my` first | habit | sometimes | loops | D81 † |
| `for $x (@a)` with a variable declared outside | `for my $x (@a)` | habit | sometimes | loops | D81 |
| `try { $n / $d } catch ($e) { ... }` catches the division by zero; so with a wrong number of arguments, a method that isn't there | A fault can't be caught. Test first. `die` is caught, as in perl | habit | sometimes | errors | D13 |
| A sub that ends in an `if` or a loop returns the last thing evaluated | It has no value, and using it is a fault. End it in a `return` | habit | sometimes | subs | D18 |
| Any expression as an index in a string: `"$a[$i + 1]"`, `"$a[-$n]"` | A whole number or a scalar variable; take the index into a `my` | habit | sometimes | strings | D91 |
| Any expression as a key in a string: `"$h{'a b'}"`, `"$h{$i + 1}"`, `"$h{ a }"`; a slice there, `"@h{...}"` | A word or a scalar variable, hard against the braces: `"$h{name}"`, `"$h{$k}"`. Take the value into a `my`, or join | habit | sometimes | strings | D99 |
| A `$` or `@` in double quotes that begins no variable is text, or one of perl's own: `"cost: $ 5"`, `"@-"` | Refused: a backslash says the character (74 of the census's programs) | habit | sometimes | strings | D92 |
| `"$x::y"`, `"$x{"`, `"$x->[0]"`: the variable goes on | Refused; `"${x}::y"` or a backslash says what is meant | habit | sometimes | strings | D92, D95 |
| `substr $s, 0, 1;`, `index $s, "a";` | Brackets. `length`, `uc`, `lc`, `ord` and `chr` go without, as in perl | habit | sometimes | strings | D41 † |
| `substr($s, 0, 1) = "x";`, and assigning to any place that isn't a variable or an element | Refused: values flow, places don't | habit | sometimes | strings | D17, D56 |
| `uc` and `lc` of a character past ASCII | Fault, until a step brings perl's tables | habit | sometimes | strings | D41 |
| Printing a character past ASCII with no layer: bytes, or `Wide character` | Fault, unless the file says `use open ':std', ':encoding(UTF-8)';`, in that spelling | habit | sometimes | printing | D39 |
| `sort(@a)`, `map(...)`, `grep(...)` with brackets of their own | Without: `sort @a` | habit | sometimes | data | D89 † |
| `reverse` where one value is wanted reverses a string's characters; `sort` there is undef | Both refused there. `grep` and `map` are their count, as in perl | habit | sometimes | strings, data | D84 |
| `do { ... } while (...);` | Left out, for the step that takes `do BLOCK`. It is not a loop to perl either: `last` in it leaves the loop round it | habit | sometimes | control | D58 † |
| Reading through what is not there makes it, in silence: `if ($seen{$x}{$y})`, `my $n = $tree->{left}{size};`, `exists $h{a}{b}` | Fault: `undef where a reference is wanted`. `if ($seen{$x} && $seen{$x}{$y})`. Storing makes it, as in perl | habit | often | data | D107 |
| A later part reads through a reference that an earlier one stores through, or a sub it calls does: `say $o->{name}, bump($o);` | Refused when a later part, or anything it calls, can store through any reference at all (a guess at how often: no program has met it yet). Take the value into a `my` first | habit | sometimes | data | D109, D114 † |
| perl's own errors, `Illegal division by zero` and the rest, are caught by `try` (or `eval`) | A fault, which nothing catches: only a `die` is caught | habit | sometimes | errors | D13, D143 |
| A message split over lines, `die "no such ",` newline `$name;` | Refused, unless the message is written to end in a newline: perl names a line of its own choosing in a statement over several lines, or in a `while`'s test | habit | sometimes | errors | D150 † |
| `q/.../`, `qq{...}` and `qw/a b/` with any delimiter, `q (x)` with a blank | A bracket hard against the word: `q(...)`, `qq[...]`, `qw<...>` | habit | sometimes | strings | D121 † |

## 3. Rare, but you meant it

Idioms and habits that few programs have. Each is a real loss to
someone.

<!-- rows: idiom, habit; rarely -->

| Perl | Curly | Feel | Met | Where | Decision |
|---|---|---|---|---|---|
| String increment: `"aa"++` is `"ab"`, `"Az"++` is `"Ba"` | Fault. A numeric string that is stepped becomes a number | idiom | rarely | strings | D52 |
| A list assignment has a value, its right side's count: `my $n = () = f();`, `if ((my @r = f()))` | A statement, and refused as a value | idiom | rarely | data | D78 |
| A bare block is a loop that runs once: `{ ...; last if $x; ... }` | A scope and nothing else; an unlabelled `last` nearest one is refused. Label the loop that is meant | idiom | rarely | control | D59 † |
| The flip-flop, `..` where one value is wanted; a range of strings, `"a" .. "e"` | Refused; a string as the end of a range is a fault | idiom | rarely | control, data | D80 |
| `redo`, `goto`, `continue` blocks | Cut | idiom | rarely | control | D62 |
| `last` or `next` in a called sub, or in a `map`, `grep` or `sort` block, leaves the loop round it | Refused | habit | rarely | control | D87 |
| `unless (...) { } else { }` | Refused: it is an `if` written backwards | habit | rarely | control | D54 † |
| Chained comparisons: `0 <= $i < $n` (since 5.32) | Refused; `0 <= $i && $i < $n`. A later step can take them | habit | rarely | control | D50 † |
| A label in any case, on any statement | On a loop, in capitals, checked as the program compiles | habit | rarely | control | D61 † |
| `foreach (my $i = 0; $i < 3; $i++)`: the two words are one | `for` has three parts; `foreach` is over a list | habit | rarely | loops | D81 † |
| `for my $i (1 .. $n) { $n-- }`: perl fixes a range's ends as the loop starts | Refused: a loop may not change a scalar its list names | habit | rarely | loops | D77, D81 † |
| A reference to an element, `\$a[0]`, `\$h{k}`; `\` before a list or a slice; a closure that keeps a loop variable's alias | Refused | idiom | rarely | data | D17, D110 |
| A reference printed, joined, used as a hash's key or compared with `<`: `say $r;`, `$seen{$r}++` | Fault: `a reference where a string is wanted`, `... a number ...`. `==` and `!=` between two references say whether they are one container | habit | rarely | printing, data | D112 |
| `$#a = N` to cut or grow an array | Refused | habit | rarely | data | D80 |
| `%h{...}`, the slice of keys and values | Not in, and not proposed. `@h{...}` and `@a[...]` are in, on the left of `=` too | idiom | rarely | data | D100, D104 |
| A slice among other targets, `($x, @h{"a", "b"}) = ...`; `@a[0, 1] += 1` | A slice is the one target of its assignment, with `=` | habit | rarely | data | D100 |
| `exists $a[0]`, `delete $a[0]`, `keys @a`: the hash builtins on an array | For a hash alone | habit | rarely | data | D104 |
| `caller` | Cut: a sub can't see how it was called | idiom | rarely | subs | D18 |
| `DESTROY` at a known moment; `weaken` | No reference counts: a cycle is just collected | idiom | rarely | objects | D26 |
| Formats, `tie`, `reset`, `study`, `$[`, one-argument `select` | Gone for good | idiom | rarely | old code | D22 |
| `${name}` outside a string; a name past ASCII | `$name`, ASCII | habit | rarely | variables | D55 |
| `017` is octal | Refused: `0o17` | habit | rarely | numbers | D38 |
| An integer past 2^63 - 1 becomes unsigned, then a float, in silence | Fault: `integer overflow` (12 of the census's programs) | habit | rarely | numbers | D23 |
| No limit on recursion | `recursion too deep`, about 3,800 calls for a small sub today. The number is the implementation's | habit | rarely | subs | D68 |
| The file's last statement needs no semicolon | It does; the last of a block doesn't | habit | rarely | layout | D75 † |
| `use open qw(:std :encoding(UTF-8));`, `':utf8'` | The one spelling | habit | rarely | layout | D39 † |
| `try { ... } catch ($e) { ... } finally { ... }`; `defer { ... }` | Not in: `finally` is experimental in 5.42 and `defer` needs `use feature` | idiom | rarely | errors | D144 |
| A sub that ends in a `try`, worth its last statement's value | A fault where its value is used, as for a sub that ends in an `if` | idiom | rarely | errors, subs | D143, D18 |
| Two heredocs on a line, `<< "END"`, `<<""`, a terminator with a blank in it | One heredoc on a line, its terminator a word hard against `<<` | habit | rarely | strings | D123 † |
| `%i`, `%ld`, `%F`, `%2$s`, `%v`, `%n` in a format; a flag perl ignores | `%d`, `%f`; no argument by its number | habit | rarely | printing | D125 |
| `sprintf("%s-%s", "a")`: a missing value printed as nothing, a value too many dropped | A fault, both ways | habit | rarely | printing | D126 |

## 4. Accidents

What nobody means: slips perl lets by, and corners of perl's
implementation. Most of the decision log is about these, and almost
none of a working day is. A programmer who keeps perl's warnings
quiet has met few of them.

<!-- rows: accident; often, sometimes, rarely -->

| Perl | Curly | Feel | Met | Where | Decision |
|---|---|---|---|---|---|
| `say (1 + 2) * 3;` prints 3 | A builtin's brackets and then an operator: refused. `say +(1 + 2) * 3;` is perl's own way round | accident | sometimes | printing | D21 |
| `my $x = 10 if $c;` leaves in `$x` what it last held | `my` under a modifier, or in an operand that may not be worked out: refused | accident | sometimes | variables | D56 |
| `if ($x = 5)`: perl warns that `==` was meant | Refused, wherever a `=` with a constant on its right is tested for truth | accident | sometimes | control | D53 |
| A second `my` of a name in one scope; a statement that only has a value; `$x = 1 and $y = 2;` | Each refused. A value alone is a sub's last statement | accident | sometimes | variables | D56 |
| `*=`, `/=`, `**=`, `%=`, `x=` on an undef: a warning | Fault | accident | sometimes | numbers | D56 |
| `say 0 or 2;` is `(say 0) or 2`; `not (0) \|\| 1` is `(not 0) \|\| 1` | A word operator after `say`'s argument or bare among arguments, a tighter operator after `not (...)`: refused | accident | rarely | printing | D51 |
| `say $x -1;` takes `$x` for a file handle | Refused | accident | rarely | printing | D56 |
| `undef * 2` is undef of a glob named `2`, in silence | Bare `undef` only where perl can't take what follows for its argument; else `(undef)` | accident | rarely | variables | D48 |
| A sub named for a word of perl's is never called: after `sub q($x) {...}`, `q(5)` is the string `5` | A sub may have no name perl gives a meaning to (266 words) | accident | rarely | subs | D21 |
| `-e(2)` is a file test | A minus hard against one letter: refused | accident | rarely | subs | D73 |
| `!$x == $y` is `(!$x) == $y`, and 5.42 warns | Refused | accident | rarely | control | D50 |
| `"ab" x3`; `length - 5`; `$x =- $y`; `65.66.67`, which is `ABC` | Each refused | accident | rarely | strings, numbers | D44, D41, D56, D38 |
| `{ }` alone is an anonymous hash; `while ()` loops for ever | Each refused | accident | rarely | control | D56, D62 |
| Whether `{` is a block or a hash is perl's guess: `{ $x => 1 }` as a sub's last statement is a block, `{ "$x" => 1 }` a hash; `say { ... }` is a file handle | Where a value may begin `{` is a hash; where a statement may, a block, and the shapes perl guesses at are refused: `+{ ... }` says a hash | accident | rarely | data | D113 |
| A store through a loop variable or `$_` that holds undef makes an array in the list itself; `($c ? $r : $s)->[0] = 5` makes `$r`, where `f()->[0] = 5` dies | Fault: only a variable or an element is made, and not a read-only one | accident | rarely | data, loops | D114 |
| `my $x = (4, 5, 6);`: the comma operator, and a warning | Refused: no comma operator, but in a `for`'s first and third parts | accident | rarely | variables | D60 |
| A word before `=>` is quoted across a line end, but `true` and `v65` are not | A word is a string before `=>`, or alone in braces, only on one line with them | accident | rarely | data | D102 † |
| `-bar => 1` and `$h{-bar}` are the string `-bar` | Refused: write `"-bar"` | accident | rarely | data | D102 |
| A list with an odd number of values assigned to a hash warns, and the last key has no value; an undef as a key warns, and is the empty string | Each a fault | accident | rarely | data | D15, D48 |
| `$h {a}`, a blank before the brace; `exists $h{k};` or `keys %h;` alone as a statement, in silence | Each refused | accident | rarely | data | D104 † |
| `exists $h{a} + 1` dies as it runs; `keys %h + 1` does not compile | Refused, with the brackets that say what was meant: `exists($h{a}) + 1` | accident | rarely | data | D102 |
| A row of dots is one operation that reads each piece late: `$x . "a" . ($x = 5)` is `5a5` | Refused when a later piece, or a sub it calls, changes a variable an earlier piece reads. It refuses `$x . ++$x` too, which is `44` either way | accident | rarely | strings | D57, D69, D74 † |
| `$a[$i++] = $i . "v";` joins the string after the index is worked out, and stores `1v` | Refused when the index or key of an element changes a variable that a concatenation on the right reads | accident | rarely | data, strings | D57, D104 |
| `$t .= ($u = $x . $z);` never assigns `$u`, in 5.42 | Refused. A fault of perl's, not a rule of it | accident | rarely | strings | D57 |
| A list is the containers themselves: `$a[0] + ($a[0] = 10)` is 20; `my @b = ($x, bump());` has the `$x` that `bump` left | Refused when a later part can change what an earlier part names (81 of the census's programs, which hunt for this) | accident | rarely | data | D76 |
| `for my $x ($p, $q)` walks the variables themselves | Copies; refused when the block can change one | accident | rarely | loops | D77 |
| A `map` in a loop's list gives copies | Its arrays are frozen all the same | accident | rarely | loops | D88 † |
| An element or a slice past the end, in a `foreach`'s list or a call's arguments, is quietly made | Fault | accident | rarely | loops, subs | D80 |
| `substr` past the end is undef, `"a" x -1` is empty, each with a warning | Fault | accident | rarely | strings | D41, D44 |
| `"\q"`, `"\x4 "`, an octal escape cut short by an `8`: a warning, or a NUL in silence | Refused | accident | rarely | strings | D43 |
| A "character" is any number below 2^63, a surrogate too; printing a noncharacter warns | `chr` of anything but a Unicode scalar value: `not a character`. Printing a noncharacter: fault | accident | rarely | strings | D42 |
| `@a[0]`, a slice of one; `defined(@a)`; `my ($x, $x)`; an array among the targets that isn't last | Each refused | accident | rarely | data | D80 |
| A store before the start of an array dies | Fault | accident | rarely | data | D80 |
| `@a = sort { ... } @a` sorts in place and drops elements that were never stored | An undef there is a fault | accident | rarely | data | D87 |
| A `sort` block's value past 32 bits wraps | Fault | accident | rarely | data | D89 |
| `0x1_0000_0000` warns non-portable; `1.` is a number; digits past 2^63 - 1 are a float in silence | Each refused | accident | rarely | numbers | D38 |
| A whole float from 10^15 up to 2^53 prints as `1e+15` or as `1000000000000000`, by what was done with it before | Fault when it is made a string; `+ 0` makes the Int, in both. So `say 1e15;` and `say 2 ** 50;` fault | accident | rarely | numbers | D36 |
| `"1e16" + 1` is `10000000000000001` or `1e+16`, by the string's past; `"3.0"` is added as a float or as an integer, by its past | Fault where the two answers part. A string is a number by how it is written | accident | rarely | numbers | D40 |
| An Int of 2^53 or more that is exactly a double, beside a whole float or a string: two answers, by the Int's past | Fault | accident | rarely | numbers | D45 |
| `++` on a float past 2^53 warns `Lost precision`; `"009"++` is `"010"` or 10 | Fault | accident | rarely | numbers | D52 |
| `"Inf"`, `"NaN"` and `"0 but true"` are numbers, in silence | Fault | accident | rarely | numbers | D40 |
| `substr("abc", 0, 1e30)` is `ab`: the machine's own cut of a float | Where a whole number is wanted it is cut toward zero and must then be an Int | accident | rarely | strings | D41 |
| `die("a") . "b"`, `if (die ...)`, `say 1 if die ...;`: perl warns of a precedence problem, and dies with `a` | Refused: a `die` is never tested or a left operand | accident | rarely | errors | D146 † |
| `# line 100 "other.pl"`, a comment that changes the line and the file a `die` names | Refused | accident | rarely | layout | D147 |
| After a string read as a number underflows (`"1e-310" + 0`), an uncaught `die` exits 34, perl's `$!`, not 255 | A fault at the `die` | accident | rarely | errors | D151 |
| `sprintf("%d", 1e30)` is `-1`; `%g` of `-$x` is `-0` or `0` by what `$x` was; `%3c` pads a wide character by its bytes | A fault where perl's conversion is the machine's or has two answers; `%c` takes no width | accident | rarely | printing | D127, D131 |
| `qq[$x\[0\]]` is an element of `@x`: the backslash before the bracket goes before the variables are read | A backslash before a `qq`'s own bracket is refused | accident | rarely | strings | D131 |
| `ucfirst("éa")` is `Éa`, by perl's tables | A first character past ASCII is a fault, as for `uc` | accident | rarely | strings | D129 |

The thread through the last six rows: **in perl a value remembers
what was done with it, and in Curly a value has no past.** `my $x =
1e15; say $x;` prints `1e+15`; after `my $y = $x + 1;`, the same `say
$x` prints `1000000000000000`. Wherever perl has two answers by a
value's past, Curly faults.

## Where the outcome itself is not perl's

The only places a program that Curly runs to its end can be told from
the same program under perl. None is on stdout but hash order.

- **stderr is Curly's own** (D12): a fault's text needn't match
  perl's. Only stdout and the exit status are promised, and the text
  of a `die` and a `warn`, which is perl's byte for byte (D148). A fault
  names the line its statement starts on (D34).
- **A fault exits 1**, where perl, when it dies itself, exits 255;
  an uncaught `die` exits 255 always, where perl takes the status
  from `$!` when it is set (D12, D13).
- **A hash keeps its keys in the order they were first stored**
  (D27). perl's order changes with every run, so any order agrees
  with it; a program that is to print the same under both sorts.
- **Nothing happens at 100 calls deep** (D67), where perl warns `Deep
  recursion`: the one run-time warning that is not a fault. `no
  warnings 'recursion';` changes nothing here and keeps perl as
  quiet; it covers the file, where perl's covers its scope.
- **`out of memory` is a fault** (D66), and a perl that runs out of
  memory as it compiles a huge constant is outside the agreement
  (D46). No test has a cap of the language's (D65).
- **Every compiled program reads three environment variables**, the
  collector's knobs (D63). None changes what a program prints short
  of `out of memory`.
- **Where Curly faults, perl may never stop**: a loop that only the
  fault would end runs for ever under perl (T131).

## Where Curly keeps Perl, and a simpler language wouldn't

The other half of how Perlish it is: places where agreeing with perl
took work, and was done.

- **A variable is read when its operator runs** (D14): `$x + ($x =
  5)` is 10, `$total + step()` sees what `step` did, and an argument
  that is a variable is read as the sub takes it (D72).
- **Which results are integers and which floats is perl's own
  rule**, measured on 129,801 operations (D35): `1e15 + 1` is
  `1000000000000001`, `7 / 2` is 3.5, `10 ** 15` is exact.
- **Truth, the comparisons and what `&&` and `||` give are perl's**
  (D49); a boolean is 1 or 0, `"1"` or `""`, in silence (D47).
- **Every comparison a `sort` makes is perl's, in perl's order**:
  the runtime has perl's own merge, ported (D82, D83). A block that
  counts or prints shows what it shows under perl.
- **An interpolated string is a value made where it stands**, as in
  perl: `"$x-" . ($x = 5)` is `3-5` (D95); `"$#a"` interpolates
  (D93).
- **A sub that ends in `say` is worth `true`** (D70); one that
  returns nothing is undef to a scalar and no value in a list (D79);
  a block's last statement may leave its semicolon out (D75).
- **A string is characters** (D24), and what perl does to a string
  in silence stays (D15).
- **A `die`'s message is perl's, byte for byte** (D142, D148): the
  list joined, `Died` when it is empty, ` at FILE line N.` when it
  does not end in a newline, on the line perl names; `return`, `last`
  and `next` in a `try` do what they do anywhere (D143); `...` is a
  `die` (D145).

## Decided, not built

What the decisions already say of steps to come. Each is proposed in
full when its step is, and its rows join the sections above then.

- **References, the rest** (steps 13b to 13d; D106, D108, D110,
  D111). 13a is built, and its rows are above. To come: the whole
  container through a reference, `$r->@*`, `@{ $r }` and the slices,
  where reading a whole container through undef is a fault too
  (D107), as perl does for half the operators and not the other half;
  `\$x` and `$r->$*`; and in a string, chains and the whole-container
  forms, with no code in a string, `"@{[ ... ]}"` (D111).
- **Strings, the rest, 16d** (D120): the case escapes `\U \L \u \l
  \Q \E`, `substr` of four arguments, `reverse` of a string where one
  value is wanted, `__FILE__` and `__LINE__`, POD, `printf` to a handle
  (step 21). 16a to 16c (D121 to D131) are built, and their rows are in
  the sections above.
- **Objects** (step 17; D19). `class` as 5.42 has it. Roles are
  wanted, and perl has none: an exception to D2 (D5).
- **Regexes** (steps 19, 20). Perl's syntax and matching order, a
  subset, compiled. No `s///e`, no `(?{ })`, no string interpolated
  as a pattern. **How `s///` and a match read with `$_` read-only
  and always written is the largest open question for the feel**,
  and is not decided.
- **The core is small** (D22): files, the environment and processes
  are libraries, each by proposal.
- **What perl doesn't have** (D5): gradual types, erased before perl
  sees the file; a metaobject protocol; concurrency.

## Decisions that say nothing here

Accounted for, with nothing a Perl programmer would notice: how the
project is run, how the compiler and the runtime are built, and
decisions since retired.

D1, D3, D4, D6, D7, D8, D9, D10, D11, D25, D28, D29, D30, D31, D32,
D64, D71, D86, D90, D94, D96, D97, D98, D140, D141, D149.

## What this leaves out

- Every row marked **Later** in [`SURFACE.md`](SURFACE.md): not a
  difference, only not built. A program that uses one is refused
  today.
- The words of each refusal and fault: [`LANGUAGE.md`](LANGUAGE.md).
