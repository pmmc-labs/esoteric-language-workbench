# Where Curly and Perl differ

A first draft, 2026-11-26, written from [`DECISIONS.md`](DECISIONS.md)
(D1 to D102) and [`SURFACE.md`](SURFACE.md), for a reader who knows
Perl. It lists what a Perl programmer will find different, grouped by
the idea behind each difference, and names the decision that made it.
It decides nothing: where it and a decision disagree, the decision is
right and this file has a mistake.

What it says perl does is taken from the decisions and from
[`TRAPS.md`](TRAPS.md), whose statements about perl are held to perl
5.42 by `briefs/claims.py`. The programs in "The first twenty" were
run again for this file, under perl 5.42.0 and under the compiler as
it stood at step 11.

**Built** below means steps 0 to 11: numbers, strings, booleans,
variables, control, subs, arrays and lists, `map`, `grep`, `sort`,
interpolation. Everything else is **decided, not built**, and says
which step has it.

## The shape of every difference

There is one rule (D2), and every difference is a consequence of it:

> A program Curly accepts is a program perl 5.42 accepts, and when it
> runs without faulting it prints what perl prints, byte for byte.

So Curly never gives a Perl program a *different meaning*. Given a
Perl program, exactly one of three things happens:

```
                     +--> refused        a compile error, no binary
   a Perl program ---+--> faults         stops at run time, having printed
                     |                   only the start of what perl prints
                     +--> runs           and prints what perl prints
```

A fourth outcome, running to the end and printing something perl
doesn't, is the bug the project calls WRONG, and the whole process is
built to keep it at zero.

The differences are therefore of four kinds, and each row below is
one of them:

- **Refused.** Perl accepts the program; Curly won't compile it.
  Either the construct was cut, or perl would warn as it compiles, or
  perl's reading of it is a guess a reader would get wrong.
- **Fault.** Perl carries on (with a warning, or a guess, or
  silently); Curly stops, with `fault: MESSAGE at FILE line N.` on
  stderr and exit status 1. A fault can't be caught (D13).
- **Pinned.** Perl's answer changes from run to run; Curly picks one
  and keeps it (D14). Hash order is the main one.
- **Outside the agreement.** The few things D2 doesn't promise at
  all: stderr, the status of a `die`, what happens when memory runs
  out.

What perl does *in silence* stays (D15): `"12" + 1` is 13, `"3 " + 1`
is 4, `$s .= "x"` on an undef works, `$n += 5` on an undef works.
The line a careful Perl programmer already holds, "no warnings", is
most of the line Curly draws.

And one thing runs the other way: Curly is sometimes **stricter than
it has to be**, refusing a program perl handles well, because one
rule with no exceptions was cheaper than the exact rule. Those are
collected at the end, since they are the ones most worth arguing
with.

## The first twenty

Each line is a whole program after `use v5.42;`. All run for this
file.

| Program | perl 5.42 prints | Curly |
|---|---|---|
| `my @a = (1, 2, 3); for my $x (@a) { $x *= 2 } say "@a";` | `2 4 6` | Refused: `$x` is read-only (D17) |
| `my @a = (1, 2, 3); for my $x (@a) { $a[0] = 9; say $x }` | `9`, `2`, `3` | Fault: an array was changed while a foreach is over it (D17) |
| `sub a() { my @a = (42); return @a } my $x = a(); say $x;` | `1` | Fault: a returned a list where one value is wanted (D18) |
| `sub f($x) { if ($x) { return "yes"; } } say f(0);` | `0` | Fault: f has no value (D18) |
| `say 9223372036854775807 + 1;` | `9223372036854775808` | Fault: integer overflow (D23) |
| `say 1e15;` | `1e+15` | Fault: a whole float this size prints two ways in perl (D36) |
| `say 2 ** 50;` | `1.12589990684262e+15` | The same fault (D36) |
| `say 9**9**9;` | `Inf` | Fault: float overflow (D37) |
| `my $x = "1e16"; say $x + 1;` | `10000000000000001` | Fault: two values in perl (D40) |
| `say "abc" + 1;` | `1`, and a warning | Fault: not a numeric string (D15, D40) |
| `my $u; say "x: $u";` | `x: `, and a warning | Fault: undef where a string is wanted (D48) |
| `my $s = "aa"; $s++; say $s;` | `ab` | Fault: not a numeric string (D52) |
| `say substr("abc", 5);` | an empty line, and two warnings | Fault: substr outside of string (D41) |
| `say (1 + 2) * 3;` | `3`, and two warnings | Refused (D21) |
| `say 0 or 2;` | `0`, and a warning | Refused (D51) |
| `say 1 < 5 < 3;` | an empty line | Refused: perl chains them (D50) |
| `say 010;` | `8` | Refused: write `0o10` (D38) |
| `my $x = 3; say $x . "a" . ($x = 5);` | `5a5` | Refused (D57) |
| `my @a = (1); say $a[0] + ($a[0] = 10);` | `20` | Refused (D76) |
| `while (1) { { last; } say "here"; last; }` | `here` | Refused: the `last` would leave only the bare block (D59) |
| `my @a = (1, 2, 3); my $r = reverse(@a); say $r;` | `321` | Refused: `reverse` where one value is wanted (D84) |
| `say 10 / 0;` | dies, status 255 | Fault: division by zero, status 1 (D13) |

## 1. Where the outcome itself is not perl's

These are the only places where a program that Curly runs to the end
can be told from the same program under perl. None of them is on
stdout, except hash order.

- **stderr is Curly's own** (D12). A fault's text and a warning's
  needn't match perl's. Only stdout and the exit status are promised.
- **A fault exits 1.** Where perl itself dies (`Illegal division by
  zero`, a wrong number of arguments), Curly faults: another message,
  and status 1 where perl has 255 (D13).
- **A fault can't be caught** (D13; `try` is step 15, not built).
  `try { 1 / $zero } catch ($e) { ... }` runs the `catch` in perl.
  In Curly it will fault: a program that caught a fault and went on
  would print what perl never does. `die` is perl's, and is caught.
- **An uncaught `die` exits 255**, always. perl takes the status from
  `$!` when it is set; Curly doesn't follow (D12).
- **A hash keeps its keys in the order they were first stored**
  (D27; step 12, not built). perl's order changes with every run, so
  any order agrees with it; this one makes a run repeatable.
- **Nothing happens at 100 calls deep** (D67). perl warns `Deep
  recursion`. This is the one run-time warning of perl's that is not
  a fault. `no warnings 'recursion';` is accepted, changes nothing
  here, and is what keeps perl as quiet; it covers the whole file,
  where perl's covers its scope.
- **Recursion has a limit** (D68): `recursion too deep`, about 3,800
  calls for a small sub today. perl has none. The number is the
  implementation's and not the language's.
- **Memory.** `out of memory` is a fault (D66). There are no
  reference counts, so no `DESTROY` and no `weaken`, and a cycle is
  just collected (D26). perl working a huge constant out as it
  compiles, and running out of memory before the program starts, is
  outside the agreement (D46).
- **Every compiled program reads three environment variables**, the
  collector's knobs (D63). None changes what a program prints short
  of `out of memory`.
- **Where Curly faults, perl may never stop.** A loop that only the
  fault would end (`$i++` past the largest integer, in a `while ($i >
  0)`) runs for ever under perl, which goes on into floats (T131).
  Not a difference in meaning, but the reason a fault's test is
  written with care.

## 2. Values flow; containers don't (D17)

The largest cut, and the one a Perl programmer feels most. Perl
passes and iterates over the containers themselves, so a write can
reach back through an argument, a loop variable, `$_` or a `map`.
Curly's bindings are read-only copies, and it makes sure a copy and
an alias can't be told apart.

| Perl | Curly |
|---|---|
| `@_` aliases the arguments | Refused. A sub has a signature, always, and its parameters are copies (as perl's signature parameters are) |
| A `foreach` variable, `$_`, and `sort`'s `$a` and `$b` alias the element: `$x *= 2`, `chop $x`, `s///` on `$_` rewrite the array | Read-only. Any use in a position that can change one is refused |
| A loop's list is live: changing `@a` inside `for my $x (@a)` shows in `$x` | The list is copied once, and every array named anywhere in it is frozen while the loop runs; a store or a change of size is a fault, from the block or from a sub it calls. The same in `map`, `grep` and `sort` |
| The alias reaches through `sort`, `grep`, `reverse`, a slice, a ternary, a comma list | So does the freeze: "named anywhere in the list" |
| `for my $x ($p, $q)` aliases the scalars | Copies; refused when the block, or a sub it calls, can change a scalar the list names (D77) |
| `for $x (@a)` with an outer `$x`, lent to the loop and given back | Refused: `for my $x` (D81) |
| `\$a[0]`, `\$h{k}`: a reference to an element | Refused (step 13) |
| A closure over a loop variable keeps the alias after the loop | Refused until step 14 proposes what it means |
| `($x = 5) = 7`, `(1 ? $x : $y) = 8`, `substr(...) = ...`, lvalue subs | Refused: an assignment's left side is a variable (D56) |
| `local` | Cut |

What still works and matters: `for my $i (0 .. $n) { $a[$i] *= 2 }`
(a range freezes nothing; take `$#a` into a `my` first, since `$#a`
names `@a`), `@a = map { $_ * 2 } @a`, and `for my $k (keys %h) {
$h{$k}++ }` (`keys` gives copies).

## 3. Context is syntax (D18)

Whether an expression is in list or scalar position is read off the
source, as in perl: `my $n = @a` is the count. What goes is context
*leaking through a call*: a Perl sub's `return` is evaluated in its
caller's context, so one sub has two meanings.

| Perl | Curly |
|---|---|
| `return @a` to a scalar call gives the count; `return (4, 5, 6)` gives 6; `return $c ? @a : 0` gives 3 for three elements | Fault, when a `return` that is list-shaped *as written* is reached by a call that wants one value. Raised before anything of the list is worked out |
| A sub ending in an `if`, a loop or a block returns the last thing evaluated, which is the condition | The sub has no value; using it is a fault |
| `wantarray` | Refused |
| `if (f())` when `f` returns an array: the count | A scalar call, so the fault above. `my @r = f(); if (@r)` |
| A list assignment has a value, the count of its right side: `my $n = () = f();`, `if ((my @r = f()))` | A statement, and refused as a value (D78) |
| `sort` where one value is wanted: undef and a warning. `reverse` there: joins and reverses the characters | Both refused there (D84). `grep` and `map` are their count, as in perl |
| A slice, a range or a comma list where one value is wanted: the last element, or the flip-flop | Refused (D80); `(LIST)[N]` is that element |

## 4. Where perl's parser guesses, Curly doesn't (D21)

The parser never needs to know what has been declared to read a line.

| Perl | Curly |
|---|---|
| A predeclared sub may be called without brackets | A program's own sub is called with brackets: `f($x)` |
| A sub named for a word of perl's is ignored in silence: after `sub q($x) {...}`, `q(5)` is the string `5` | A sub may not have any name perl gives a meaning to (266 words), nor `v` and digits |
| `say (1 + 2) * 3;` prints 3 | A builtin's brackets and then an operator: refused. `say +(1 + 2) * 3;` is perl's own way round |
| `sort dbl(3, 1, 2)` takes `dbl` for the comparator; `sort $f @a` likewise | A word or a scalar first after `sort`: refused. `sort`, `map` and `grep` take no brackets of their own (D87, D89) |
| `map EXPR, LIST`, where `map ($_ * 2), (1, 2)` is a `map` of nothing | A block always (D85) |
| A builtin with no argument means `$_`: `say for @a;`, `grep { defined } @a` | `$_` is always written (D85) |
| `my $x = 10 if $c;` leaves the last value in `$x` when `$c` is false | `my` under a modifier, or in an operand that may not be worked out: refused (D56) |
| `say $x -1;` takes `$x` for a file handle | A variable, a blank, and what could begin a value, first after `say`, `print`, `substr(` or `index(`: refused (D56) |
| `-e(2)` is a file test; `-foo` is the string `-foo` | A minus hard against one letter: refused. `-bareword`: refused |
| `say 0 or 2;` is `(say 0) or 2`; `not (0) \|\| 1` is `(not 0) \|\| 1` | A word operator after `say`'s argument, or bare in a list of arguments; a tighter operator after `not (...)`: refused (D51) |
| `undef * 2` is undef of a glob named `2`, in silence | Bare `undef` only where perl can't take what follows for its argument; else `(undef)` (D48) |
| `1 < 5 < 3` chains (since 5.32) | Two comparisons of one row with no brackets: refused (D50). A later step can take chaining without breaking a program |
| `!$x == $y` is `(!$x) == $y`, and 5.42 warns | Refused (D50) |
| `$x =- $y`, `"ab" x3`, `length - 5`, `65.66.67` (a v-string: `ABC`) | Each refused |
| A line that starts `#!` gives perl switches (`-n`, `-l`) | Refused, on any line (D33) |
| Indirect object syntax, prototypes, `&f`, barewords as strings | Cut, but a word before `=>` and alone in a hash's braces, on one line (D102) |
| Named subs anywhere, bound to the first instance of what they close over | A named sub stands at the top level (D72); closures are step 14 |

## 5. Where perl warns, Curly stops (D15)

A run-time warning is a fault; a compile-time warning is a refusal.
The warnings `use v5.42` turns on are the list. Some of them:

| Perl warns, and carries on with | Curly |
|---|---|
| `"abc" + 1` as 1; `"12abc"` as 12; `""` as 0 | Fault: not a numeric string |
| An undef as 0 or `""`, in arithmetic, a comparison, a string, `say` | Fault: undef where a number (or a string) is wanted (D48) |
| `substr` past the end: undef | Fault |
| `"a" x -1`: the empty string | Fault: negative repeat count |
| `*=`, `/=`, `**=`, `%=`, `x=` on an undef | Fault. (`+=`, `-=`, `.=`, `\|\|=`, `//=`, `++` are silent in perl, and work) |
| `++` on a float past 2^53: `Lost precision` | Fault (D52) |
| Printing a character past ASCII with no layer: `Wide character` | Fault, unless the program says `use open ':std', ':encoding(UTF-8)';` (D39) |
| Printing a noncharacter | Fault (D42) |
| A second `my` of a name in one scope | Refused |
| A statement that only has a value, `$x + 1;` | Refused; but a value alone is a sub's last statement (D72) |
| `if ($x = 5)`: `Found = in conditional` | Refused, wherever a `=` with a constant on its right is tested for truth (D53) |
| `my $x = (4, 5, 6);`: useless constants | Refused: no comma operator, outside a `for`'s first and third parts (D60) |
| `"\q"`, `"\x4 "`, an octal escape cut short by an `8` | Refused (D43) |
| `@a[0]`, a slice of one | Refused (D80) |
| `0x1_0000_0000`: non-portable | Refused: hex, binary and octal up to 32 bits (D38) |

And the faults where perl is **silent**, because Curly cut what perl
does there. These are a list, and each is a deliberate loss:

- String increment: `"aa"++` is `"ab"` in perl; `"ab"--` is -1.
- A list-shaped return reached by a scalar call, and a sub that ends
  in an `if` (section 3).
- Integers past 2^63, infinities and NaN, and the two-answer cases
  (section 6).
- An element or a slice past the end of an array in a `foreach`'s
  list or a call's arguments, where perl quietly makes the elements
  (D80).
- An undef in `@a = sort { ... } @a`: perl sorts in place and drops
  elements that were never stored (D87).
- A `sort` block's value outside 32 bits, where perl wraps it (D89).
- `"Inf"`, `"NaN"` and `"0 but true"` as numbers (D40).
- Decided, not built: a reference used as a string or compared with
  `<`; reading through an undef, which in perl creates the container
  on the way (`$h->{a}{b}`); both step 13.

## 6. Numbers

Curly has two kinds, Int (64 bits, signed) and Num (a finite double),
and which one an operation gives is **perl's own rule**, measured
(D35): whole-number arithmetic when both operands are integral (an
Int, or a whole Num below 2^53), doubles otherwise. So `1e15 + 1` is
`1000000000000001` and `7 / 2` is 3.5, as in perl. The differences
are at the edges, and nearly all come from one fact:

> **In perl a value remembers what was done with it. In Curly a value
> has no past.**

`my $x = 1e15; say $x;` prints `1e+15` in perl; after `my $y = $x +
1;` the same `say $x` prints `1000000000000000`. Reading the variable
changed how it prints. Curly's values carry no such mark, so wherever
perl has two answers by a value's past, Curly faults.

| Perl | Curly |
|---|---|
| An integer past 2^63 - 1 becomes unsigned, then a float, in silence | Fault: integer overflow. No unsigned integers (D23) |
| A whole float from 10^15 up to 2^53 prints as `1e+15` or `1000000000000000`, by its past | Fault when it is made a string; `+ 0` makes the Int, in both (D36). So `say 1e15;` and `say 2 ** 50;` fault |
| `Inf` and `NaN` are values; `9**9**9` is the idiom for "larger than anything" | A Num is finite: `float overflow`, `not a number` (D37) |
| `"1e16" + 1` is `10000000000000001` or `1e+16`, by the string's past | Fault. A string is a number by how it is written (D40): digits are the Int; with an exponent, the Int if whole and below 2^53; with a point, the Num |
| `"3.0"` is added as a float until it has been used as one, then as an integer | Float arithmetic, and a fault if either number or the exact answer reaches 2^53 (D40) |
| An Int of 2^53 or more that is exactly a double, beside a whole float or a string, in `+ - *`: two answers, by the Int's past | Fault (D45) |
| `--` on a whole float reaching 2^53; `++` on `"009"` (`"010"` or 10); a string of digits stepped as text or as a number | Fault where the two part (D52). A numeric string that is stepped becomes a Num |
| `substr("abc", 0, 1e30)` is `ab`: the machine's own cut of a float | Where a whole number is wanted it is cut toward zero and must then be an Int, or a fault (D41) |
| `017` is octal; `1.` is a number | Refused: `0o17`; a dot after a number is concatenation (D38) |
| A digits-only literal past 2^63 - 1 becomes a float in silence | Refused (D38) |
| `use integer`, bignums | Cut |

## 7. Strings and characters

| Perl | Curly |
|---|---|
| Two kinds of string, bytes and characters, with a hidden flag | One: a sequence of Unicode scalar values, immutable, counted in characters (D24, D42). Bytes are a later proposal and a separate type |
| A "character" is any number below 2^63, a surrogate included | `chr` of anything but a scalar value: fault, `not a character` (D42) |
| `uc` and `lc` know Unicode | They fault on a character past ASCII, until a step brings perl's tables (D41) |
| `substr $s, 0, 1`; `index $s, "a"` | Brackets always. `length`, `uc`, `lc`, `ord`, `chr` are named unary operators as in perl (D41) |
| `(...) x N` | A list where a list is wanted, as in perl; a repeated string may not pass 2^31 - 1 characters (D44) |
| Every `$` and `@` in double quotes is looked up; `"@-"` and `"@_"` are arrays, empty and silent; `"a $ b"` is `$b` | A `$` or `@` begins one of eight shapes, hard against it, or is refused; a backslash says the character (D92) |
| An index in a string is any expression, read as code: `"$a[$i + 1]"` | A whole number or a scalar variable (D91). A leading zero there is octal to perl, and refused |
| `"$x::y"`, `"$x{"`, `"$x->[0]"`: the variable goes on | Refused; braces or a backslash say what is meant (D92) |
| `$"`, `$,`, `$\`, `$/` | Cut: an array in a string is joined with one space (D22, D95) |
| `use open` in several spellings, `:utf8` | One spelling (D39) |
| `\N{name}`, `\c`, `\U \L \Q \E` | Later (step 16) |

## 8. undef, booleans, truth

Truth is perl's exactly (false: undef, `false`, zero, `""`, `"0"`),
and `&& || // and or` give one of their operands and don't work the
right one out unless it is wanted, as in perl (D49).

- **A boolean is a kind of its own** (D47), and as a number or a
  string it is what perl makes of it in silence: 1 or 0, `"1"` or
  `""`. `false == 0` is true; `"" == 0` is a fault (perl warns).
- **undef faults** where a number or a string is wanted, printing
  included (D48). What takes one: `defined`, `//`, the tests of
  truth, and `length`, which gives undef, as in perl.
- `undef($x)`, the operator on a variable: cut.

## 9. Variables, assignments, statements (D55, D56)

| Perl | Curly |
|---|---|
| `our`, package variables, `$Pkg::x`, `local` | Cut (D19) |
| `my $a`, `my $b` are allowed, and break `sort` in their scope | `$a` and `$b` are `sort`'s alone; `$_` is its binder's alone, and can't be declared |
| Names past ASCII under `use utf8`; `${name}`; `$ name` | ASCII, written `$name`. Past ASCII is Later |
| Any expression is a statement | A statement does something: `say`, `print`, a `my`, an assignment, a step, a call, a block, a control form |
| `$x = 1 and $y = 2;` | Refused: one assignment to a statement |
| `{ }` is an anonymous hash | An empty bare block is refused |
| The last statement of a file needs no semicolon | It does; the last of a *block* doesn't (D75) |
| `no strict`, `no warnings`, any pragma | `use v5.42;` first, then a closed list (D16) |
| `BEGIN`, `eval STRING`, `require` at run time, `do FILE`, `__DATA__` | Cut: the compiler sees the whole program first (D20) |
| `eval { }` and `$@` | Cut, for `try` (D20) |

## 10. When a variable is read

Here Curly *agrees* with perl where a simpler language wouldn't, and
it is worth knowing why. **Perl reads a variable when the operator
that uses it runs, not when it is reached**: `$x + ($x = 5)` is 10,
and `$total + step()` sees what `step` did to `$total`. Curly does
the same (D14); its generated C never copies a variable into a
temporary.

The differences are the places where perl's late read goes further
than a rule can follow, and Curly refuses the program:

| Perl | Curly |
|---|---|
| A row of dots is one operation that reads every piece late: `$x . "a" . ($x = 5)` is `5a5` | Refused when a later piece changes a variable an earlier piece reads (D57), a call that can change it included, worked out over the whole program (D69) |
| `$t .= ($u = $x . $z);` never assigns `$u`, in 5.42 | Refused (D57). This one is a fault of perl's, not a rule of it |
| A list is a row of the containers themselves: `$a[0] + ($a[0] = 10)` is 20; `my @b = ($x, bump());` has the `$x` that `bump` left | Refused when a later part of an expression or a list can change what an earlier part names: an element, a slice, an array, `$#a`, a scalar that is an item of a list (D76) |
| An interpolated string is one operation of its own: `"$x-" . ($x = 5)` is `3-5` | The same: a value, made where it stands (D95) |
| An argument that is a variable is read as the sub takes it, a default running in between | The same (D73) |

Inside `sort`, every comparison is perl's, in perl's order: the
runtime has perl's own merge, ported (D82). So a block that counts,
prints or is inconsistent shows what it shows under perl.

## 11. Control

| Perl | Curly |
|---|---|
| A bare block is a loop that runs once: `last` leaves it | A scope and nothing else; an unlabelled `last` or `next` nearest a bare block is refused (D59) |
| `last` and `next` are expressions: `$done and last;` | Statements, with a label, an `if` or an `unless` (D62) |
| A label on any statement, in any case, looked up when the `last` runs | On a loop, in capitals, checked as the program compiles (D61) |
| `last` in a called sub, or in a `map`, `grep` or `sort` block, leaves the caller's loop | Refused |
| `do { } while (...)`, which is not a loop to perl | Left out, for the step that takes `do BLOCK` (D58) |
| `unless ... else`, `unless ... elsif` | Refused (D54) |
| `foreach (init; test; step)`: the two words are one | `for` has three parts; `foreach` is over a list (D81) |
| `redo`, `goto`, `continue` blocks, `given`, `when` | Cut |
| The flip-flop, `..` where one value is wanted; a range of strings, `"a" .. "e"` | Refused; a string as the end of a range is a fault (D80) |
| `while ()` loops for ever | Refused |

## 12. Subs (D72)

- A signature, always. No `@_`, no prototypes, no `&f`, no
  `goto &sub`.
- At the top level of the file, until closures (step 14). Called
  before or after it is written.
- A wrong number of arguments is a fault, after the arguments have
  all run. perl dies there too; Curly's can't be caught.
- `return` is a statement: not `... and return`, not an operand.
- A sub that ends in `say` or `print` is worth `true`, as in perl
  (D70); a sub that returns nothing is undef to a scalar and no
  value in a list, as in perl (D79).
- `caller`: cut.

## 13. Arrays and lists (D80)

Mostly perl's: lists flatten, a read past either end is undef and
makes nothing, a store past the end grows the array, an array where
one value is wanted is its count. The differences:

| Perl | Curly |
|---|---|
| A store before the start of an array dies | Fault |
| `$a[0][0]` on a plain array (autovivification) | Refused until references (step 13) |
| `$#a = N` | Refused |
| `defined(@a)`, `length(@a)` | Refused |
| `pop;` and `shift;` with no array | Always name an array |
| `my ($x, $x)`; an array among the targets that isn't last | Refused |
| `each`, the iterator a hash carries; `foreach my ($k, $v) (%h)` | Cut; not taken up (D101) |
| `%h{...}`, the slice of keys and values | Cut (D100) |
| `delete` and `exists` on an array | Later |

## 14. Decided, not built

What the decisions already say about the steps to come. Each will be
proposed in full when its step is.

- **Hashes** (step 12; D27, D98 to D102). Insertion order. In a
  string a key is a word or a scalar variable. A word is a string
  before `=>` or alone in braces only when it is on one line with
  them: perl reads `true` as the boolean, and `v65` as a version
  string, once a line end stands beside the word.
- **References** (step 13). `\` on a variable, `[ ]`, `{ }`; not on
  an element or a slice. A reference as a string, or under `<`, is a
  fault: its address is not part of the agreement (D14). Reading
  through an undef is a fault, where perl creates what it read
  through; writing through one is perl's. Whether `@$x` and `$$x`
  stay, beside `->@*`, is for the step to propose.
- **Objects** (step 17; D19). `class`, `field`, `method`, `ADJUST`,
  `:isa`, `:param`, `:reader`, as 5.42 has them, and nothing else:
  no `bless`, no `@ISA`, no `AUTOLOAD`, no `DESTROY`, no `can` to
  fetch code, no overloading. `package` only names a file's subs.
  Roles are wanted, and perl has none: an exception to D2, with a
  model of its own.
- **Errors** (step 15). `die`, `try`, `catch`. No `eval`.
- **Regexes** (steps 19, 20). Perl's syntax and matching order, a
  subset, compiled; a pattern is known as the program compiles. No
  `s///e`, no `(?{ })`, no string interpolated as a pattern.
- **The core is small** (D22). Files, the environment and processes
  are libraries, each by proposal. Gone for good: formats, `tie`,
  `each`, `reset`, `study`, `$[`, and the punctuation variables that
  set global behaviour.
- **What perl doesn't have** (D5): gradual types, erased before perl
  sees the file; roles and a metaobject protocol; concurrency.

## 15. Stricter than it has to be

Places where Curly refuses or faults a program whose perl answer it
could have agreed with, by choice. Each is small, each was taken for
"one rule with no exceptions", and most say in their decision that
they can be reversed without breaking a program.

- A row of dots is refused wherever a later piece changes what an
  earlier one reads, though `$x . ++$x` is `44` either way: the exact
  rule is perl's optimiser (D57). `$x .= set();` likewise (D74).
- A range's end named in its own loop, `for my $i (1 .. $n) { $n-- }`:
  perl fixes the ends as the loop starts and would have agreed (D81).
- A `map` in a loop's list freezes the arrays its own list names,
  though perl's `map` gives copies (D88).
- `sort(@a)` with brackets of its own is silent and plain in perl;
  refused, with `map`'s and `grep`'s (D89).
- A label in small letters, or on an `if` (D61).
- `unless` with an `else` (D54).
- The last semicolon of the file (D75).
- A first line `#!/usr/bin/perl` with no switch on it (D33, which
  says it is fair to revisit).
- `use open qw(:std :encoding(UTF-8));`, the other spelling (D39).
- `substr $s, 0, 1` without brackets (D41).
- A word across a line end before `=>`, which perl quotes for every
  word but a few (D102).
- Chained comparisons, `0 <= $i < $n` (D50).
- `"a @ b"`, where the `@` is text to perl (D92).
- A bare block one can `last` out of (D59).

## What this draft leaves out

- Every row marked **Later** in `SURFACE.md`: not a difference, only
  not built. A program that uses one is refused today.
- The exact text of refusals and faults, which
  [`LANGUAGE.md`](LANGUAGE.md) has.
- The differences that come with steps 12 and after, beyond what the
  decisions already fix (section 14).
- It has no check of its own. The perl half of each row is a
  decision's or a trap's; if this file is to be kept, its rows want
  the treatment `briefs/claims.py` gives the others, and a rule for
  who updates it when a step lands.
