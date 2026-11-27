# Step 16, adversarial review: findings

Reviewer: Opus 5.5, 2026-11-27. I did not write the proposal. I read
`docs/PLAN.md` "### 16. Strings, the rest", D120 to D130 and T260 to
T277. I did not run the compiler, because step 16 is not built. I ran
every program below under `/opt/perl-5.42/bin/perl` (5.42.0), and the
outputs here are pasted from those runs. Each program begins with
`use v5.42;`. Scratch files are in `/tmp/claude-0/review16/`.

There are five ways to be WRONG (1 to 5). Two of them (4 and 5) also
hide a place where perl has two answers. Then come ambiguities that an
obvious build would get WRONG (6 and 7), and risks in the build and
the test plan (8 to 11).

---

## 1. WRONG: in `qq` with bracket delimiters, a backslash before the bracket is gone before interpolation

D121 and 16a say that `qq` is "a double-quoted string, its escapes and
its variables exactly D43's and D91 to D99's". In perl that is not so.
When perl finds where the string ends, it removes a backslash that
stands before the delimiter's own bracket. Only then does it
interpolate. So `qq[$x\[0\]]` reaches the interpolator as `$x[0]`,
which is an element. `"$x\[0\]"` stays `$x` followed by the text
`[0]`. A build that finds the end and then hands the raw body to 11a's
lexer prints the double-quoted reading.

```perl
use v5.42; my $x = "X"; my @x = ("Y"); say qq[$x\[0\]];
```
```
Y
```
```perl
use v5.42; my $x = "X"; my @x = ("Y"); say "$x\[0\]";
```
```
X[0]
```
```perl
use v5.42; my $x = "X"; my %x = (a => "H"); say qq{$x\{a\}};
```
```
H
```
```perl
use v5.42; my %x = (a => "S"); my @x = ("A"); say qq{@x\{a\}};
```
```
Scalar value @x{"a"} better written as $x{"a"} at p.pl line 1.
S
```
```perl
use v5.42; my @x = ("A","B"); say qq[@x\[1\]];
```
```
Scalar value @x[1] better written as $x[1] at p.pl line 1.
B
```
```perl
use v5.42; my $x = "X"; say qq<$x-\>[0]>;
```
```
Can't use string ("X") as an ARRAY ref while "strict refs" in use at p.pl line 1.
```

Under the proposal as written, the first two lines print `X[0]` where
perl prints `Y` and `H` (WRONG). The last line prints `X->[0]` where
perl dies (category b). If `@x` or `%x` is not declared, perl stops
with `Global symbol` where the proposal prints. `\[` with nothing to
close it, as in `qq[$x\[0]]`, ends the string early in perl (`Missing
right curly or square bracket`).

**Fix:** remove the backslash before the delimiter's bracket first, as
16a already says for `q`. Then refuse a `qq` whose body, after that
removal, has a `$` or `@` shape that D92 refuses. The simplest rule is
to refuse a backslash before either bracket of the delimiter inside
`qq`, as D121 does for `qw`.

---

## 2. WRONG: `chomp` does not turn a number into a string; perl leaves it alone

D130 and 16c say that `chomp` makes the variable "a string as `.`
makes one, less a newline at its end". T272 gives the reason:
"`chomp` made the number the string `1e+15`, and the sum is a
float's". That reason is wrong. perl's `$s + 1` prints
`1000000000000001` whether or not there was a `chomp`, because perl
adds 1e15 as an integer. And perl's `chomp` keeps a number's numeric
value:

```perl
use v5.42; my $s = 1e15; say $s + 1;
```
```
1000000000000001
```
```perl
use v5.42; my $x = 1/3; chomp $x; say $x * 3;
```
```
1
```
```perl
use v5.42; my $x = 0.1 + 0.2; chomp $x; say $x == 0.3 ? "eq" : "ne";
```
```
ne
```
```perl
use v5.42; my $x = 0.1 + 0.2; chomp $x; say $x - 0.3;
```
```
5.55111512312578e-17
```
```perl
use v5.42; use Devel::Peek; my $x = 0.1+0.2; chomp $x; Dump $x; my $y = 7; chomp $y; Dump $y;
```
```
SV = PVNV(0x560f49950300) at 0x560f49980900
  REFCNT = 1
  FLAGS = (NOK,pNOK)
  IV = 0
  NV = 0.30000000000000004
  PV = 0x560f499737b0 "0.3"\0
  CUR = 3
  LEN = 32
SV = PVIV(0x560f49979ba0) at 0x560f49990760
  REFCNT = 1
  FLAGS = (IOK,pIOK,pPOK)
  IV = 7
  PV = 0x560f499b9080 "7"\0
  CUR = 1
  LEN = 16
```

Under D130, `$x` becomes `"0.333333333333333"` and `"0.3"`. The
language would then print `0.999999999999999`, `eq` and `0`, where
perl prints `1`, `ne` and `5.55111512312578e-17`. A number's string
form never ends in a newline, so perl's `chomp` of a number changes
nothing.

**Fix:** a `chomp` of a variable that holds a number (or a boolean)
leaves the variable as it is. Only a Str is chomped. `chop` is
different, as the proposal says: it has to make the string (`chop` of
0.1 + 0.2 is `0.`, as perl prints). Correct T272's explanation. Its
first program is still a fault under D36 only if `chomp` makes a
string, so with this fix it becomes a `same` test that prints
`1000000000000001`, or `1e+15` under `say $s`.

---

## 3. WRONG: `%.0f` is not C's `%.0f` in perl

The proposal says "perl's own numbers come from the same C library,
and `%.0f` of 2.5 is 2 in both", and the build goes "through C's
`snprintf` for the numbers". perl does not use C for a bare `%.0f`
(no flags, no width). It uses its own `F0convert`, which adds 0.5,
truncates, and steps back from an odd whole number. Adding 0.5 rounds
in double, so the value just above one half comes out differently:

```perl
use v5.42; printf("%.0f %.0f\n", 0.5000000000000001, -0.5000000000000001);
```
```
0 -0
```
C's `printf("%.0f", 0.5000000000000001)` prints `1`, and the negative
prints `-1` (glibc 2.39, run). `%.f` is the same as `%.0f`. Any width
or flag sends perl back to C, so `%1.0f` and `%#.0f` agree with C.

I compared perl with glibc over 44,781 values: every `k + 0.5` and its
four neighbours on each side up to 2^60, both signs, and 40,000 random
values. `0.5000000000000001` and its negative were the only values
that differ. The language's literal `0.5000000000000001` is that very
double. The proposed model, Python's `%`, prints `1` as C does, so the
model and the build would agree with each other and not with perl.

**Fix:** format a bare `%.0f` as perl's `F0convert` does, or fault on
exactly those two values. Add both to the fault or `same` tests.

---

## 4. WRONG: `rindex` with a negative position, and two answers near 2^63

16c and D129 say the position "is moved into the string". perl does
not clamp the position. It adds the length of SUB first, then clamps
the end of the search. So a negative position finds nothing unless
SUB is empty:

```perl
use v5.42; for my $p (-3,-2,-1,0,1,2,3,4,100, 2**31, 2**32, 9223372036854775807, -9223372036854775807) { say "$p: ", join ",", rindex("abc","a",$p), rindex("abc","c",$p), rindex("abc","",$p), rindex("abc","ab",$p), index("abc","c",$p), index("abc","",$p) }
```
```
-3: -1,-1,0,-1,2,0
-2: -1,-1,0,-1,2,0
-1: -1,-1,0,-1,2,0
0: 0,-1,0,0,2,0
1: 0,-1,1,0,2,1
2: 0,2,2,0,2,2
3: 0,2,3,0,-1,3
4: 0,2,3,0,-1,3
100: 0,2,3,0,-1,3
2147483648: 0,2,3,0,-1,3
4294967296: 0,2,3,0,-1,3
9223372036854775807: -1,-1,3,-1,-1,3
-9223372036854775807: -1,-1,0,-1,2,0
```

Clamping first gives `rindex("abc", "a", -1)` as `0`, where perl
prints `-1`. That is WRONG, and an ordinary program can meet it. The
proposal's own words, "where SUB last begins at or before the
position", are right *without* the clamp.

Near 2^63, `position + length(SUB)` overflows in perl. Whether it
overflows depends on whether the string is stored as UTF-8 inside,
which the program cannot see:

```perl
use v5.42; my $w = substr("abc\x{263A}", 0, 3); my $p = "abc"; say $w eq $p ? "same string" : "differ"; say rindex($p, "a", 9223372036854775807), " ", rindex($w, "a", 9223372036854775807); say rindex($p, "ab", 9223372036854775806), " ", rindex($w, "ab", 9223372036854775806); say rindex($p, "a", 9223372036854775806);
```
```
same string
-1 0
-1 0
0
```

**Fix:** the answer is the last place SUB begins at or before
POSITION, with no clamping of a negative position. An empty SUB gives
POSITION clamped to the string. Fault when POSITION + length(SUB)
passes 2^63 - 1 (both answers are perl's).

---

## 5. WRONG: a negative zero that is a string, under `%e`, `%f` and `%g`

D127 faults "a negative-zero Num" under `%e %f %g` (T267). But the
string `"-0"` is not a Num. D40 makes `"-0"` and `"-0e0"` the Int 0.
perl reads the string as a double, `-0.0`:

```perl
use v5.42; say sprintf("%g|%e|%.1f|%.0f", "-0", "-0", "-0", "-0");
```
```
-0|-0.000000e+00|-0.0|-0
```
```perl
use v5.42; say sprintf("%g|%g|%g|%g", "-0.0", "-0e0", "-0.00", "-0e5");
```
```
-0|-0|-0|-0
```
```perl
use v5.42; my $s = "-" . 0; say sprintf("%g|%.0f|%e", $s, $s, $s);
```
```
-0|-0|-0.000000e+00
```

The proposal prints `0`, `0.000000e+00`, `0.0` and `0` for the
strings `"-0"`, `"-0e0"`, `"-0e5"` and `"-" . 0`. That is WRONG. The
answer also depends on the string's past, so agreeing is not possible
either:

```perl
use v5.42; my $s = "-0"; my $t = $s + 0; say sprintf("%g", $s);
```
```
0
```
```perl
use v5.42; my $s = "-0"; my $t = $s * 1.5; say sprintf("%g", $s);
```
```
-0
```

**Fix:** under `%e`, `%f` and `%g`, fault on a string whose number is
zero and which has a minus sign (any of D40's shapes), as for a
negative-zero Num. `%d` and `%s` of these strings are fine: `0`, `0`,
`0` and `-0.0` for `"-0"`, `"-0.0"`, `"-0.0"` (under `%x`) and
`"-0.0"` (under `%s`), as perl prints.

---

## 6. Ambiguous, and WRONG if built the obvious way: what a `*` takes

16b says a width or precision may be `*`, "taken from the list". It
does not say how that value is converted, what a negative one means,
or what bounds it has. D125 refuses a literal width of 2^31 or more
(T271), but a `*` can bring any value as the program runs. perl:

```perl
use v5.42; say "[", sprintf("%*s|%-*s|%0*d|%.*s|%.*f", -4, "a", -4, "b", -5, 42, -1, "abc", -2, 1.25), "]";
```
```
[a   |b   |42   |abc|1.250000]
```
```perl
use v5.42; say "[", sprintf("%*s|%.*s", 2.9, "a", 1.9, "abc"), "]";
```
```
[ a|a]
```
```perl
use v5.42; say length sprintf("%*d", 4294967297, 1);
```
```
4294967297
```
```perl
use v5.42; say length sprintf("%*d", 2**62, 1);
```
```
Integer overflow in format string for sprintf at p.pl line 1.
```
```perl
use v5.42; say "[", sprintf("%*s", undef, "a"), "]";
```
```
Use of uninitialized value in sprintf at p.pl line 1.
[a]
```

A negative width pads on the right, and `0` does not apply then. A
negative precision counts as none. A Num is cut toward zero. The
proposal pads `%s` "by hand", and that code has to follow all of
these rules. A build that hands a `*` value to `snprintf`'s `int`
turns 4294967297 into a width of 1 and prints `1`, which is WRONG.
perl prints 4 GB.

**Fix:** say that a `*` is a whole number taken as `%d` takes one; a
negative width means `-`; a negative precision means none; outside
±(2^31 - 1), fault; undef is D48's fault. Each needs a test.

---

## 7. Ambiguous: is the format checked as source text or as the string's value?

"The format is a string literal with no variable in it", and "every
conversion is checked as the program compiles". The checks must run on
the literal's *value* after D43's escapes, not on its source text.
`"\x25d"`, `"%\x64"` and `"\%d"` are all `%d` to perl. `"%2\$s"` is
`%2$s`, which D125 refuses. A source-text check would count no value
for `sprintf("\x25d", 5)`, and the runtime would then find a `%d`.

Also say whether `qw(...)` counts as "a quoting form that has none".
perl takes its first word as the format:

```perl
use v5.42; say sprintf(qw(%s-%s a b));
```
```
a-b
```
```perl
use v5.42; say join(qw(- a b));
```
```
a-b
```

Either answer is safe as long as a `qw` stays a flattened list here.
Reading it as a list where one value is wanted, giving its last word,
would be WRONG.

---

## 8. Risk: C's `printf` is not one thing (`%b`, and flags C leaves undefined)

I compared perl with glibc 2.39 over 29,190 cases: `d u o x X b B`
with 14 sets of flags, widths of none, 1 and 6, precisions of none,
`.`, `.0`, `.1` and `.4`, and the values 0, ±1, ±42, 255, IV_MAX and
IV_MIN. Every case agreed. (`%.0d` of 0 is empty, `%#o` of 0 is `0`,
`%#x` of 0 is `0`, `%+.0d` of 0 is `+`, `%u` of -1 is
`18446744073709551615`.) That agreement is glibc's, not C's:

- `%b` and `%B` exist in glibc only from 2.35. macOS's libc, which is
  Stevan's machine and clang's, has no `%b`.
- `#` on `%d %u %c %s`, and `+` or a blank on `%u %o %x`, are
  undefined in C. glibc happens to ignore them, as perl does.

**Recommendation:** format the integer conversions by hand in
`runtime/format.c`, as `%s` already is: perl formats them itself in
`sv_vcatpvfn`. Keep `snprintf` for `e f g` only, and handle `%.0f` as
in finding 3. Otherwise run the 16b tests on the Mac before calling it
done.

---

## 9. Test-plan risk: Python's `%` is not C's printf, and not perl's

16b says the model's formatter is "Python's `%` operator (C's printf,
written again)". It is not:

```
'%.0d' 0 '0'          (C and perl: '')
'%#o' 8 '0o10'        (C and perl: '010')
'%#x' 0 '0x0'         (C and perl: '0')
'%#o' 0 '0o0'         (C and perl: '0')
'%u' -1 '-1'          (perl: '18446744073709551615')
'%x' -1 '-1'          (perl: 'ffffffffffffffff')
'%05s' ab '   ab'     (perl: '000ab')
'%.0f' 0.5000000000000001 '1'   (perl: '0', finding 3)
```
It also has no `%b`. A model built on it writes wrong expected outputs
at exactly the edges a model exists for. The oracle check would catch
those, but only for values that some test contains. Write the
integer formatter by hand in the model, as for finding 8, and include
these rows in its tests.

---

## 10. Minor: `%c` and `%s` flags the proposal does not mention

perl ignores a precision on `%c` and the flags `+`, blank, `#` and
`0` there when there is no width:

```perl
use v5.42; print sprintf("[%.0c|%.3c|%-c|%+c|%#c|%0c]", 65,65,65,65,65,65);
```
```
[A|A|A|A|A|A]
```
On `%s`, perl ignores `+`, blank and `#` (in the comparison, every
`%+s`, `% s` and `%#s` row matched perl's padding in characters). Say
whether these are refused or ignored. Either is safe, but the
hand-written padding must not act on them.

---

## 11. Minor: heredoc points that are right in the text but easy to build wrong

- The body starts after the heredoc's *own* line, even when the
  statement goes on past it. An implementation that reads the body
  after the end of the statement is WRONG:

  ```perl
  use v5.42;
  my @a = (<<A,
  "x");
  body
  A
  say scalar @a; print @a;
  ```
  ```
  Global symbol "@a" requires explicit package name (did you forget to declare "my @a"?) at p.pl line 6.
  syntax error at p.pl line 6, near "@a;"
    (Might be a runaway multi-line << string starting on line 3)
  Execution of p.pl aborted due to compilation errors.
  ```
  (`"x");` was taken into the body.) D123 forbids only a *token* that
  crosses the heredoc's line, so an open bracket before the heredoc
  is allowed. Say so, and test a heredoc as the first of several
  arguments that go on over later lines.
- `<<123` is a heredoc to perl (it printed `x`). D123's "a word" can
  include it or refuse it. Either is safe.
- `q(ab)x3` runs under perl (`ababab`), unlike T57's `"ab" x3`. Either
  refusing it or taking it is safe.

---

## What I checked and found to hold

- **`%d %u %o %x %X %b %B`** against glibc, over the 29,190 cases in
  finding 8: perl and glibc agree in every case. **`%e %E %f %g %G`**
  with the same flags, widths and precisions, over 16 values, and with
  precisions up to `.100`: perl and C agree except for `%.0f` and
  `%.f` (finding 3). perl's `Gconvert` here is
  `sprintf((b),"%.*g",(n),(x))`, so `%.20g` agrees with C.
- **`%s`** counts its width and precision in characters for wide
  strings, Latin-1 strings, and Latin-1 strings in a wide result. So
  T277's byte padding is `%c`'s alone. `%05s` of `ab` is `000ab`, and
  `%01s` of `""` is `0`. Padding by hand, as the proposal plans, is
  right.
- **D127's numeric ranges**: `%d` of `2**63` is
  `-9223372036854775808`. `%x` of `2**63` is `8000000000000000`.
  `%u` of -1.5 is `18446744073709551615`. `%x` of -1e19 is
  `8000000000000000`, clamped, which the proposal faults. `%d` of
  `"1e3"`, `"1.9"` and `" 12 "` is `1000|1|12`. `%.0f` of the Int
  9007199254740993 is `9007199254740992`, the same as converting it to
  a double. `%s`, `%d` and `%g` of `true` and `false` give `1|1|1` and
  `[|0|0]`.
- **The `q` backslash rules** (T261): `q(it\'s)` is `it\'s`, and
  `q(a\{b)`, `q{a\{b}` and `q(a\\b)` are `a\{b`, `a{b` and `a\b`. A
  build that reuses the single-quote token for `q` would print
  `it's`, which is WRONG. The proposal's text is right.
- **`q`, `qq` and `qw` as words**: `(q=>1)`, `(qq=>1, qw=>2)`, `$h{ q
  }` and `$h{ qw }` are those words to perl.
- **`qw`**: `qw(a) x 3` where one value is wanted is `aaa`. `qw(a b)
  x 2` in `say` is `abab`. `(qw(a b)) x 2` is a list. `uc qw(a b)`
  does not compile (`Too many arguments for uc`). `qw()` where one
  value is wanted is undef.
- **`<<~`**: a line of blanks shorter than the indentation dies; a
  longer one keeps the rest; an empty line is allowed (`a\n\nb\n`); a
  tab where the terminator has spaces dies. `END ` with a trailing
  blank is not a terminator. A terminator at the end of the file with
  no newline after it works. `lc <<END . "x"` is `lc(body . "x")`.
  `<<END x 2` repeats the body.
- **`ucfirst` and `lcfirst`**: `ucfirst("aé")` is `Aé`, and so are
  `""`, `5`, `true` and `false`. perl's `ucfirst` uses titlecase
  (`ǆ` becomes `ǅ`, where `uc` gives `Ǆ`), so faulting past ASCII is
  needed, and the proposal does. The precedence is a named unary's.
- **`index`** clamps a negative position to 0 (`index("abc","c",-1)`
  is 2). Only `rindex` differs (finding 4).
- **`chop`** of a number makes the string as `.` does (`chop` of 1.5
  is `1.`, and that plus 1 is 2). `chomp` and `chop` of undef warn,
  so a fault is right. `chomp ($x);` with a blank is fine. `chomp ($x)
  . "a";` warns.
- **The repeated flags** `%--5d`, `%++d`, `%  d` and `%0-5d` give
  `1    |+1| 1|1    |`, as C does.
- **The stars' negative-value rules** (finding 6) are C's too. What is
  missing is only the proposal saying so, and the bounds.
