# Curly

The language as it is, for someone writing programs in it: every form
and builtin, in prose with examples, no tables, changed in the same
commit as the feature.

What the language is meant to become is in [`DESIGN.md`](DESIGN.md),
and [`SURFACE.md`](SURFACE.md) says, for each construct of Perl,
whether it will be in. Neither is a description of what works. This
is, and so far it is short: a program can do arithmetic, build
strings, compare and choose, keep values in variables, take one path
or another, go round a loop, and print.

## A program

A program is a file of Perl, named `something.pl`. Compile it and run
what comes out:

    node bin/curlyc.ts -o hello hello.pl
    ./hello

Every program the compiler accepts is a program perl 5.42 accepts, and
prints what perl prints. So `perl hello.pl` is always a second opinion,
and the two never differ: where the language doesn't do what perl
does, the compiler refuses the program, with a message that starts
`FILE:LINE:COL:`, and makes no binary.

The first statement of a program is

    use v5.42;

and nothing may stand before it but blank lines and comments. That
line is what makes the file mean one thing to perl, so it can't be
left out, and it must be `v5.42` exactly. It appears once. The `v5.42`
is followed by its semicolon or by a blank: a comment hard against it,
`use v5.42#`, is refused, because perl then reads something else.

Three more lines may follow it, in any order, each once, before
anything else:

    use utf8;
    use open ':std', ':encoding(UTF-8)';
    no warnings 'recursion';

The first lets the program's text hold characters past ASCII, the
second lets the program print them, and the third keeps perl quiet
about a sub that calls itself a hundred deep; each is described where
it matters, below. They are written exactly so (either kind of quote
will do), and no other `use` or `no` is in the language.

## The text of a program

A program is written in ASCII: the printable characters, the space,
the tab and the newline. A carriage return is refused, so a file with
Windows line endings has to be converted, and so is every other
control character, wherever it is.

A character past ASCII may stand in a string or in a comment, and
nowhere else, in a file that is UTF-8 and says `use utf8;` **on an
earlier line**:

    use v5.42;
    use utf8;
    use open ':std', ':encoding(UTF-8)';
    say "café";   # and in a comment: ☺

On the line that says `use utf8;` itself it is too soon, as it is to
perl, which reads a line at a time; and without the pragma the
character is refused, in a comment too, as perl refuses it.

Spaces, tabs and newlines separate words and are otherwise ignored. A
statement may be spread over several lines, and several statements may
share one.

A comment starts at `#` and runs to the end of its line.

    use v5.42;
    # on a line of its own
    say 42;   # or after a statement

One comment is refused: a line that starts `#!`, with or without
blanks before it. perl reads switches from such a line when it is the
first (`#!/usr/bin/perl -n` wraps the whole program in a loop over its
input), and there are ways to make perl take a later line for the
first, so no line may start that way. After a statement on its line,
`say 42; #!`, it is an ordinary comment.

## Statements

Every statement ends with a semicolon, and there is no empty
statement: `;;` is refused. The last statement of a block may leave
its semicolon out, `if ($ok) { say "yes" }`, as in perl; the last
statement of the file may not. A block and an `if`
end with their closing brace. The statements are `say` and `print`,
the ones that work on variables (a `my`, an assignment, `++` and
`--`), blocks, `if` and `unless`, the loops `while`, `until` and
`for`, `last` and `next`, a call of a sub, and in a sub `return`;
each is described below. A `sub` is written at the top level, and
ends with its closing brace.

## say and print

`say` prints the value of an expression and a newline. `print` prints
the value and no newline.

    use v5.42;
    say 42;
    say 2 + 3 * 4;
    say(7 / 2);

prints

    42
    14
    3.5

    print "no newline";
    print "\n";

Each takes one expression or a list of them, with brackets or
without, and prints each value with nothing between: `say "a", "b";`
prints `ab` (see "Arrays and lists"). Neither has a value, so neither
can stand inside an expression. What is said of `say` below goes for `print` too.

**To print a character past ASCII, the program says `use open ':std',
':encoding(UTF-8)';` at the top.** With that line perl writes its
output as UTF-8, and so does the language. Without it perl writes `é`
as a single byte that isn't UTF-8 and warns about `☺`, so the language
stops there: `fault: a character past ASCII printed without 'use
open'`. A program that prints only ASCII doesn't need the line, and
may still build and measure any string it likes.

Without brackets, the expression runs to the semicolon. With them,
**the brackets are the whole of what `say` is given**, and nothing but
the semicolon may follow:

    say (1 + 2) * 3;      # refused

perl prints 3 for that line and throws the multiplication away, which
nobody means. Write `say((1 + 2) * 3);`, or `say 3 * (1 + 2);`, or put
a plus in front, `say +(1 + 2) * 3;`, which is perl's own way of
saying that a bracket doesn't begin the argument list. All three print
9.

Write the bracket hard against the word, `say(1 + 2);`. With exactly
one space between them, `say (1 + 2);`, the statement has to end on
that line, bracket, semicolon and all: perl looks along the line for
them and warns when they aren't there, and a program perl warns about
is refused. It looks at the text, not at what the text means, so a
bracket inside a string counts: `say ("(");` is refused, and
`say("(");` is fine.

## Numbers

There are two kinds of number. An **Int** is a whole number from
-9223372036854775808 to 9223372036854775807 (-2^63 and 2^63 - 1), and
arithmetic on Ints is exact. A **Num** is a floating-point number, a
double, with about 15 significant digits and a range to about 1.8e308.
A Num is always finite: there is no infinity and no NaN.

Which kind a literal is depends on how it is written, and which kind
an answer is depends on the operation and its operands, below. Mostly
you needn't care, because perl doesn't make you: the language follows
perl exactly, and stops where it can't.

## Writing numbers

An Int is decimal digits, `0` to `9223372036854775807`; or hex,
binary or octal, as `0x1F`, `0b101`, `0o17` (the letters in either
case), up to 32 bits, which is `0xFFFFFFFF`.

A Num is written with a point, an exponent, or both: `1.5`, `0.25`,
`.5`, `1e3`, `1.5e-3`, `1E3`. So `1.0` and `1e3` are Nums, though
they are whole.

An underscore may stand between two digits, anywhere digits are:
`1_000_000`, `0xff_ff`, `1.000_1`.

There is no negative literal: `-5` is a minus applied to `5`. So the
smallest Int can't be written directly, its digits being one past the
largest; write `-9223372036854775807 - 1`.

Refused, each for something perl does with it that nobody means:

- A leading zero, `010`. perl reads that as octal, 8. Octal is
  `0o10`.
- A point with nothing after it, `1.`. Write `1.0`.
- A whole literal past the largest Int, and a hex, binary or octal
  one past 32 bits; a float literal past the largest double, `1e400`.
  perl takes the first as a float and the last as infinity, without a
  word. For a large float, write the exponent: `1e19`.
- An underscore anywhere but between two digits: `1__0`, `1_`, `0x_ff`.
- A number that runs straight into a letter, a digit or a dot:
  `1.5.5`, `0x1.8`, `1e`, `42x3`. perl reads those as a version
  string, as two numbers joined into a string, and so on.

## Arithmetic

`+`, `-`, `*`, `/` and `**` (to the power of) do what they say, and a
`-` before an expression negates it. `%` is the remainder. A `+`
before an expression does nothing to it.

    say 7 / 2;       # 3.5
    say 2 ** 10;     # 1024
    say 0.1 + 0.2;   # 0.3
    say -7 % 3;      # 2

### Whole numbers, and the rest

An operand is **integral** when it is an Int, or a Num that is whole
and below 2^53 (9007199254740992, where a double stops being able to
hold every whole number). `3`, `3.0`, `1e3` and `6 / 2` are integral;
`1.5`, `0.1` and `1e16` are not.

**When both operands are integral, `+`, `-` and `*` work on whole
numbers and the answer is exact, an Int. Otherwise they work on
doubles and the answer is a Num.** That is perl's rule, and it is why

    say 1e15 + 1;    # 1000000000000001
    say 1e16 + 1;    # 1e+16

An exact answer has to fit an Int. For `+` and `-`, one that doesn't
is a fault, `integer overflow`. For `*` it depends on what was
multiplied: two Ints overflow; with a Num among them the answer is a
Num, as a float program would expect, except in the narrow band from
2^63 to 2^64 - 1, where perl keeps an exact unsigned integer and the
language, which has none, faults.

    say 5_000_000_000 * 5_000_000_000;   # fault: integer overflow
    say 5e9 * 5e9;                       # 2.5e+19
    say 1e10 * 1e9;                      # fault: integer overflow (the band)

### Division

`/` divides doubles, and its answer is a Num, even when it is whole:
`6 / 2` is the Num 3. (It prints `3`, and it is integral, so nothing
shows.) One exception, perl's: an Int too large for a double, past
2^53, divided exactly, gives the exact Int.

    say 7 / 2;                    # 3.5
    say 18014398509481984 / 2;    # 9007199254740992

Dividing by zero, of either kind, is a fault, `division by zero`.

### Powers

`**` binds tighter than a minus sign in front of it and groups from
the right; its own right side may start with a sign.

    say -2 ** 2;        # -4
    say 2 ** 3 ** 2;    # 512
    say 2 ** -1;        # 0.5

Its answer is a Num, from the C library's `pow`, with two exceptions
for a whole number to a whole power of 0 or more. A base of 0, 1, -1,
or plus or minus a power of two gives a Num that is exact: `2 ** 10`
is the Num 1024. Any other base gives an exact Int when it is sure to
fit, which is when the number of bits in the base times the power is
at most 64: `10 ** 15` and `7 ** 20` are Ints, `3 ** 40` is the Num
1.21576654590569e+19.

### Remainders

`%` works on whole numbers only. A Num operand is cut to its whole
part first, toward zero, so `10 % 3.7` is `10 % 3`, which is 1. The
answer is an Int, and takes the sign of the right operand, as perl's
does and C's doesn't:

    say 7 % 3;       # 1
    say -7 % 3;      # 2
    say 7 % -3;      # -2

A remainder by zero is a fault, `modulus by zero` (and `7 % 0.5` is
one: 0.5 is cut to 0). An operand too large to be an Int once cut is
a fault too, `modulus of a number outside the integers`.

### No infinity, no NaN

A Num that would be too large is a fault, `float overflow`, and so is
one that would be infinite for another reason, like `0 ** -1`. An
operation with no real answer, like `(-8) ** 0.5`, is a fault, `not a
number`. In perl these go on as `Inf` and `NaN`; here they stop. The
idiom `9**9**9` for "larger than anything" is therefore a fault.

### Grouping

Operators group as in perl. `**` binds tightest, then a minus or plus
sign before an expression, then `*`, `/` and `%`, then `+` and `-`.
Operators of one level group from the left (`2 - 3 - 4` is -5, `4 / 2
* 3` is 6), except `**`, which groups from the right. Brackets group
as you'd expect.

    say 2 + 3 * 4;       # 14
    say (2 + 3) * 4;     # refused: see say
    say((2 + 3) * 4);    # 20
    say -2 * -3;         # 6
    say - -5;            # 5

Two minus signs with nothing between them, `--5`, are one thing to
perl, a decrement, and are refused; so is `++`, until its step. The
operands of an operator are worked out from left to right, so of two
faults in one expression, the left one is the one that happens.

## How a number prints

An Int prints as its digits. A Num prints as perl prints it, to 15
significant digits: `0.1 + 0.2` is `0.3`, `1 / 3` is
`0.333333333333333`, `3.0` is `3`, and a large or small one takes an
exponent, `1e+21`, `1e-05`. A zero prints `0`.

**One kind of Num doesn't print: a whole one from 10^15 up to 2^53.**

    say 1e15;                    # fault
    say 2 ** 50;                 # fault
    say 4000000000000000 / 2;    # fault

perl prints such a number two ways, `1e+15` or `1000000000000000`,
depending on whether the value has ever been used as an integer
before, and a value here carries no such past. So the language stops
rather than pick: `fault: a whole float this size prints two ways in
perl (add 0 to print the integer)`. Adding 0 makes the Int, here and
in perl, and that prints one way:

    say 1e15 + 0;                # 1000000000000000

Outside that range there is nothing to choose. Below it, both ways
are the same digits. From 2^53 up perl always prints the float, so
`say 1e16;` prints `1e+16`.

## Strings

A **Str** is a sequence of characters, of any length, the empty string
included. A character is a Unicode character: `length` counts
characters, not bytes, and so does everything else. A string never
changes; every operation makes a new one.

### Writing strings

In single quotes, what is written is what the string holds:

    say 'a $ and an @, and a \n that is two characters';

Only two things are special there: `\\` is one backslash and `\'` is
a quote.

In double quotes a backslash begins an escape:

    say "a tab\tand a newline\n";

The escapes are `\n` (newline), `\t` (tab), `\r`, `\f`, `\b`, `\a`,
`\e` (escape) and `\0` (a NUL); `\\`, `\"`, `\$` and `\@` for those
four characters; and four ways to name a character by its number:
`\x41` (two hex digits), `\x{263A}` (any number of them), `\101` or
`\o{101}` (octal), and `\N{U+263A}`. A backslash before any other
punctuation mark, or a space, is that mark.

**A `$` or an `@` in double quotes begins a variable**, whose value
goes into the string: see "A variable in a string", below. For the
character itself, a backslash: `"cost: \$5"`, `"me\@example.com"`.

Everything else is refused, because perl warns about it or reads it
as something nobody means: a backslash before a letter or a digit that
isn't an escape (`\q`, `\8`); `\x` with fewer than two digits; an
octal escape of one or two digits with an `8` or a `9` after it (write
all three digits, `\001`); a number that isn't a character
(`\x{D800}`, `\x{110000}`); `\c`, a character by its name
(`\N{LATIN SMALL LETTER E}`), and the case escapes `\U \L \u \l \Q
\E`.

A string may run over several lines, and then it holds the newlines. A
tab may be written as itself; any other control character is written
as an escape.

### q, qq, qw and heredocs

`q(...)` is a string in single quotes, `qq(...)` one in double quotes,
and the bracket is the quote, so a string can hold both kinds of quote
as they are:

    say q(it's "here");          # it's "here"
    say qq(it's "$name");        # the variable's value between the quotes

The bracket may be `( )`, `[ ]`, `{ }` or `< >`, hard against the
word, and a bracket of the same kind inside nests: `q(a (b) c)` is `a
(b) c`. In `q` a backslash before a backslash or before either bracket
is that character, and every other backslash is itself. In `qq` the
escapes and the variables are those of double quotes, exactly; a
backslash before the `qq`'s own bracket is refused, since perl takes it
away before it reads the variables (`qq[$x\[0\]]` is an element of
`@x` to perl): write such a string with another bracket.

Refused: any other delimiter (`q/.../`, `q!...!`, `q#...#`) and a
blank before the bracket. One spelling is enough.

**`qw(...)` is a list of words**, the characters between blanks, and is
exactly the bracketed list of those words in quotes:

    my @days = qw(mon tue wed);
    say qw(a b c)[1];            # b, a slice of the list
    my @twice = qw(x y) x 2;     # x y x y

So it is not the brackets of anything else: `for my $d qw(a b) {...}`
is refused, as perl refuses it, and so is `qw(a b)` where one value is
wanted. A word may not hold a comma or a `#` (perl warns that you may
have meant something else) or a backslash (perl keeps it, or takes it
away before a bracket).

**A heredoc** is a string over the lines after the line it stands on:

    print <<"END";
    Dear $name,
      your total is $total.
    END

The body ends at a line that is the terminator alone. `<<"END"` and
`<<END` are double-quoted, with escapes and variables; `<<'END'` takes
every character as it is, a backslash too. With a `~`, `<<~"END"`, the
terminator may be indented, and its indentation is taken off every line
of the body; a line of the body that does not begin with it, and is not
empty, is refused (perl dies). A heredoc is a value where it stands:
`lc <<END`, `<<END . "more"`, `print(<<END);`.

The terminator is a word hard against the `<<`, the `~` or the quote.
One heredoc on a line, and nothing after it on that line may go on past
the end of the line (a string, a `qw`): perl reads the body after the
line the heredoc is on, and a string that goes on hides it. Refused too:
a blank after `<<`, an empty terminator or one with a blank in it, and a
heredoc that never finds its terminator.

### A variable in a string

In double quotes a variable is replaced by its value:

    my $name = "Ada";
    my @langs = ("Perl", "C");
    say "$name writes @langs.";          # Ada writes Perl C.
    say "first: $langs[0], last: $langs[-1], last index: $#langs";

The shapes that do this are a short list:

- **`$x`**, a scalar. The name is the longest one that could be meant:
  in `"$x_y"` the variable is `$x_y`. **`${x}`** ends the name where
  you say: `"${x}_y"`, `"${n}th"`.
- **`@a`**, an array: its values with one space between each two, and
  nothing for an empty array. `@{a}` is the same.
- **`$a[0]`**, an element. The index is **a whole number or a scalar
  variable**: `"$a[0]"`, `"$a[-1]"`, `"$a[$i]"`. Anything more is
  refused: take the index into a `my` first.
- **`@a[0, 1]`** and **`@a[1 .. 3]`**, a slice: indexes of that kind
  with commas between, or a range between two; joined with a space.
- **`$#a`**, the last index; `$#{a}` is the same.

In the block of a `for`, a `map`, a `grep` or a `sort`, `$_`, `$a` and
`$b` are variables like any other: `map { "<$_>" } @a`.

**Each value is made a string as `.` makes one**: a number as it
prints, `true` as `1` and `false` as the empty string. **An undef is a
fault**, `undef where a string is wanted`, wherever it stands: a
scalar, an element past the end, a value in an array or a slice. So
is a whole Num from 10^15, as it is under `.`.

**A string with a variable in it is one value, a Str, made where it
stands.** `"$n"` is a string and not the number: `"$x" + ($x = 5)`
adds 5 to what `$x` was. Nothing in a string can change anything, so
the order its pieces are read in never shows; and nothing later in the
statement reaches back into it, which is what perl does too:

    my $x = 3;
    say "$x-" . ($x = 5);       # 3-5: the string was made first

(A row of dots is different: `$x . "-" . ($x = 5)` is refused, since
perl reads `$x` late there. See "When a variable is read".)

**Where a variable ends.** What comes hard after one of those shapes
is text: `"$x's"`, `"$x: $y"`, `"$x->y"`, `"$x."`, `"$a[0]s"`. A few
things perl would take into the variable are refused, each with a
message that says how to write it:

- **`::`** after a name: `"$x::y"` is a variable of another package to
  perl. Write `"${x}::y"` or `"$x\::y"`.
- **`{`**: after an array or an element; `"$x{a}"` is an element of
  the hash `%x` ("A hash's element in a string").
  Write `"${x}{a}"` or `"$x\{a}"`.
- **`[`** after a scalar is always the element, `"$x[1]"` of `@x`,
  whether or not there is a `$x`. For the scalar and a bracket, write
  `"${x}[1]"` or `"$x\[1]"`. A second `[`, after an element or a
  slice, is refused.
- **`->`** before `[`, `{`, `@` or `$`: a dereference, to perl. Write
  `"$x\->[0]"`.
- **A character past ASCII** after a bare name: `"$xé"` is the
  variable `$xé` to perl. Write `"${x}é"`.

After a name in braces none of that applies: everything after
`"${x}"` and `"@{a}"` is text.

**Every other `$` and `@` in double quotes is refused**, and needs its
backslash: a `$` or `@` with a blank after it or at the end, `$1`,
`$$`, `@_`, an email address. To perl some of these are text and some
are variables of its own that print nothing, and the rule here is one
line: a `$` or `@` begins one of the shapes above, hard against it,
or it has a backslash. A variable in a string is declared like any
other: `"user@example.com"` is refused for want of an `@example`.

Not in the language yet: an expression in a string (`"@{[ ... ]}"`,
`"${\ ... }"`), which waits for references;
the case escapes, `\U` and its kin.

### Joining and repeating

A dot joins two values into a string, and `x` repeats one:

    say "ab" . "cd";      # abcd
    say "ab" x 3;         # ababab
    say "-" x 10 . ">";   # ---------->

The dot sits with `+` and `-` in the order of operations, and `x` with
`*`, so `"a" . "b" x 2` is `abb`, and `1 + 2 . 3` is `33`: the sum
first, since the two are equals and group from the left.

`x` is a word, with a blank or a bracket after it: `"ab" x3` is
refused. Its count is cut to a whole number, so `"a" x 2.7` is `aa`. A
count below zero is a fault (`negative repeat count`), `-0.5`
included, and so is a result of 2^31 characters or more.

Brackets round the left operand, where a list is wanted, make it a
list that is repeated: `say(("ab") x 3);` is three values to `say`,
which prints the same, and `my @r = ("ab") x 3;` is three elements
(see "Arrays and lists"). Where one value is wanted, `("ab") x 3 .
"!"`, the brackets are harmless and it is a string.

After a value, a dot is always the operator, whatever follows it: `1
.5` is `15`, and `"a".5` is `a5`.

### Numbers as strings, and strings as numbers

A number where a string is wanted becomes what `say` would print for
it:

    say "n = " . 0.1 + 0.2;   # a fault: see below
    say "n = " . (0.1 + 0.2); # n = 0.3
    say length 1000;          # 4

(The first is `("n = " . 0.1) + 0.2`, and `"n = 0.1"` is no number.)
The one kind of Num that doesn't print, above, doesn't become a string
either: `"a" . 1e15` faults.

A string where a number is wanted must be written as a number: blanks,
a sign, digits with a point among them or not, an exponent, blanks.

    say "12" + 1;       # 13
    say " 12\n" + 1;    # 13: blanks before and after are fine
    say "1.5" * 2;      # 3
    say "1e3" + 1;      # 1001

Anything else is `fault: not a numeric string`: `""`, `"abc"`,
`"12abc"`, `"0x10"`, `"1_000"`. perl warns about each of those and
carries on with a guess. It doesn't warn about `"Inf"`, `"NaN"` or `"0
but true"`, and they are faults here all the same.

Which number a string is depends on how it is written, as with a
literal. Digits alone are an Int, and fault if they are past the Ints.
A point or an exponent makes a Num, except that an exponent with a
whole value, `"1e3"`, is the Int. Three corners fault, because perl
has two answers in each, depending on what was done with the string
earlier, and a value here has no earlier:

- a string with an exponent whose value is whole and 2^53 or more,
  `"1e16"`;
- arithmetic on a string like `"3.0"`, whole with a point, when the
  other number or the exact answer is 2^53 or more. `"3.0" + 1` is 4
  and `"10.00" * 3` is 30; `"3.0" + 9007199254740990` stops;
- a minus before a string whose number is whole and 2^53 or more, or
  before a string that starts with `+`.

A minus before a string negates its number: `-"12"` is -12. (perl's
`-"foo"`, which is the string `-foo`, is a fault.) A plus before a
string does nothing at all: `+"abc"` is `abc`.

One more corner is about numbers alone, and is step 2's rule made
exact: in `+`, `-` and `*`, an Int of 2^53 or more that happens to be
exactly a double (10000000000000000, 2^60) faults beside a whole Num
or a string, `10000000000000000 + 1.0`: perl answers
`10000000000000001` or `1e+16` by the Int's past. Beside another Int
it is exact as ever, and so is every Int a double can't hold exactly.

### length, uc, lc, ord, chr

`length` is the number of characters. `uc` and `lc` change the case of
the ASCII letters, and fault on a character past ASCII, until perl's
own tables for the rest of Unicode are in. `ord` is the number of a
string's first character (0 for the empty string), and `chr` is the
character with a number.

    say length "café";     # 4
    say uc "abc";          # ABC
    say ord "A";           # 65
    say chr 65;            # A

`chr` wants a character's number: 0 to 0x10FFFF, less the surrogates
(0xD800 to 0xDFFF). Anything else is `fault: not a character`, a
number below zero too. A fraction is cut off, `chr 65.9` is `A`.

These five are written with brackets or without. With brackets, the
brackets are the argument: `length("ab") . "c"` is `2c`. **Without
them, the argument is everything up to something that binds more
loosely than arithmetic and the dot**, which is perl's rule:

    say length "ab" . "c";    # 3: the length of "abc"
    say length "abc" + 1;     # a fault: "abc" + 1

One spelling is refused: a sign after the name must be on the same
line, with a blank before it and none after, `length -5`. perl warns that `length - 5`
and `length-5` are ambiguous (it means `length(-5)` by both).

### substr and index

`substr(STRING, START)` is the string from a position to its end, and
`substr(STRING, START, LENGTH)` is that many characters from the
position. Positions count from 0, and a negative one counts from the
end; a negative length leaves that many off the end.

    say substr("abcdef", 2);       # cdef
    say substr("abcdef", 2, 3);    # cde
    say substr("abcdef", -2);      # ef
    say substr("abcdef", 1, -1);   # bcde

A piece that hangs over an end of the string is cut to what the string
has. A start past the end is `fault: substr outside of string`, and
so is a piece that starts and ends before the beginning. (perl warns
of both.)

`index(STRING, PIECE)` is the position of the first place the piece
is found, or -1, and `index(STRING, PIECE, START)` looks from a
position on.

    say index("abcabc", "c");      # 2
    say index("abcabc", "c", 3);   # 5
    say index("abcabc", "x");      # -1

These two are always written with brackets. A position or a length
that isn't a whole number is cut to one, toward zero; one too large
to be an Int is a fault. So is a string with a point that is a hair
below a whole number, `"1.99999999999999999"`, here and as a count or
for `chr`: its nearest double is 2, and perl cuts it to 1 or to 2 by
what was done with the string before.

### sprintf and printf

`sprintf(FORMAT, LIST)` makes a string from a format and values, and
`printf(FORMAT, LIST);` prints one, as `print` would:

    my $line = sprintf("%-8s %5.2f %03d", $name, $price, $count);
    printf("%d%% done\n", $percent);

`sprintf` is written with brackets or without, as `join` is, and is
one value; `printf` is a statement, as `print` is, to standard
output. **The format is a string literal with no variable in it**, in
any of the quotes (a heredoc too), so that the compiler can read it:
perl takes the first value of an array for a format (`sprintf(@a)`
formats the array's count), and a `%` in a variable would be a
conversion.

The conversions are `%s` (a string), `%c` (a character, by its
number), `%d` (a whole number), `%u`, `%o`, `%x`, `%X`, `%b` and `%B`
(the same with no sign, in decimal, octal, hex and binary), `%e`,
`%E`, `%f`, `%g` and `%G` (a number as a float), and `%%` for the
character. Between the `%` and the letter may come the flags `-`
(padded on the right), `+` and a blank (a sign for a positive `%d` or
float), `0` (padded with zeros) and `#` (`0x`, `0b`, a leading `0` for
`%o`, a point for a float), then a width, then a point and a
precision; a width or a precision may be `*`, taken from the list
before the value (a negative width pads on the right, a negative
precision is none). What each prints is what perl prints, which is
C's, but for a bare `%.0f`, where perl rounds by adding a half, and so
does the language.

**The format takes exactly as many values as it has conversions and
stars**: one too few or too many is a fault (perl warns, and prints a
blank or ignores the rest).

Each value is taken as its conversion wants it. `%s` makes it a string
as `.` does, and its width and precision count characters; `0` pads
`%s` with zeros, as perl does. `%c` takes a character's number, as
`chr` does. `%d` cuts a number toward zero; past the Ints it is a
fault (perl prints what the machine gives, `-1` for 1e30). The
unsigned conversions take a negative Int as its 64 bits (`%x` of -1
is `ffffffffffffffff`) and a Num up to 2^64; past that, a fault. A
zero with a minus sign, a Num or a string, is a fault to `%e`, `%f`
and `%g`: perl prints `-0` or `0` by what the zero was used as before.
undef is a fault, as everywhere.

Refused: `%i`, `%D`, `%U`, `%O` and `%F` (perl's other spellings:
write `%d`, `%d`, `%u`, `%o`, `%f`); `%a`, `%n`, `%p`, `%v` and an
argument by its number, `%2$s`; the size letters `h`, `l`, `q` and the
rest, which perl ignores; a flag or a width on `%%`; a width, a
precision or a flag on `%c` (perl pads a wide character by its bytes);
`+`, a blank or `#` on `%s`; a width or precision of 2^31 or more; and
a conversion perl doesn't know or that the format cuts short. A string
of more than 2^31 - 1 characters is a fault.

## Comparing, and true and false

### Booleans

A comparison gives a **boolean**: true or false. The two are also
words a program may write, `true` and `false`.

    say 1 < 2;        # 1
    say 1 > 2;        # (an empty line)
    say true;         # 1

A boolean prints as perl prints it: true is `1` and false is nothing
at all. Where a number is wanted, true is 1 and false is 0; where a
string is wanted, they are `"1"` and the empty string. So `true + 1`
is 2, and `"[" . (1 > 2) . "]"` is `[]`. False is not the empty
string, though: `"" == 0` is a fault, since `""` is no number, and
`false == 0` is true.

### Comparing numbers

`==`, `!=`, `<`, `<=`, `>` and `>=` compare two numbers and give a
boolean. `<=>` gives -1, 0 or 1: less, equal, greater.

    say 2 <=> 10;     # -1
    say "2" == 2.0;   # 1

Both sides are made numbers, by the rules above: `"abc" == 0` is a
fault, where perl warns and says yes. Two whole numbers are compared
exactly. When either side is a Num that isn't whole, or is 2^53 or
more, both are compared as floats, as perl compares them, and an Int
past 2^53 can then equal a float it isn't quite: `9007199254740993 ==
2 ** 53` is true.

### Comparing strings

`eq`, `ne`, `lt`, `le`, `gt` and `ge` compare two strings, character
by character, and `cmp` gives -1, 0 or 1.

    say "apple" lt "banana";   # 1
    say "2" cmp "10";          # 1: "2" comes after "1"
    say 10 lt 9;               # 1, for the same reason

A number on either side is compared as the string `say` would print
for it. That is why `0.1 + 0.2 eq 0.3` is true and `0.1 + 0.2 == 0.3`
is not: the two floats differ past the fifteenth digit, and print the
same.

These are words, and need to be words of their own: `"a" lt "b"`, or
even `"a"lt"b"`, and never `1 lt2`.

### One comparison at a time

Two comparisons of the same rank can't stand side by side without
brackets:

    say 1 < 5 < 3;      # refused
    say 1 != 1 == 0;    # refused

perl chains them, so the first means `1 < 5 && 5 < 3`, and anyone who
reads from the left gets the other answer. Write what is meant: `1 < 5
&& 5 < 3`, or `(1 != 1) == 0`. A `<` beside an `==` is fine, since
`<` binds tighter: `1 < 2 == 1` is `(1 < 2) == 1`.

### What is true

Every value is true or false when a test asks. **False** is: `false`;
a number that is zero; the empty string; the string `"0"`; and
`undef`. Everything else is true, the strings `"0.0"`, `"00"` and `"
"` among them.

### not, and, or

`!` turns a truth round and gives a boolean; it binds as tightly as a
minus sign, so `!1 + 1` is `(!1) + 1`, which is 1. Before a
comparison it wants brackets, one way or the other: `!$x == $y` is
refused, because it means `(!$x) == $y`, which is rarely what was
meant, and perl warns of it. Write `!($x == $y)`, or `$x != $y`.

`&&` and `||` are "and" and "or", and they give back **one of their
operands**, not a boolean:

    say 0 || "default";   # default
    say 5 && 7;           # 7
    say 0 && 7;           # 0

`a || b` is `a` if `a` is true, and otherwise `b`. `a && b` is `a` if
`a` is false, and otherwise `b`. The right side is not worked out at
all unless it is needed, so `1 || 1 / 0` is 1 and nothing faults.

`?` and `:` choose: `test ? this : that` is `this` if the test is
true and `that` if not, and only the one chosen is worked out. Chosen
tests read down the page:

    say 0 ? "a" : 1 ? "b" : "c";   # b

The words `not`, `and`, `or` and `xor` do what `!`, `&&` and `||` do
(`xor` is true when exactly one side is), and bind more loosely than
everything else: `not 0 || 1` is `not (0 || 1)`. That looseness has
three consequences, and each is refused where it would bite:

- They bind more loosely than `say`. To perl, `say 0 or 2;` is "say
  0, or else 2", and prints 0. Put them inside brackets:
  `say(0 or 2);`.
- They bind more loosely than a comma, so in a list of arguments they
  are in brackets of their own: `substr($s, (not 0), 1)`.
- A bracket straight after `not` is the whole of what `not` takes, to
  perl, so `not (0) || 1` is `(not 0) || 1`. That one is refused: say
  which you mean, `not ((0) || 1)` or `(not 0) || 1`.

### undef

`undef` is the value that is no value: what a variable holds before
it is given one, and what `length` gives for an undef. The tests take
it:

    say defined undef ? "yes" : "no";   # no
    say undef // "fallback";            # fallback

`defined` asks whether a value is anything but undef. `//` is `||`
with that question in place of truth: `a // b` is `a` unless `a` is
undef. `0 // 5` is 0, where `0 || 5` is 5.

An undef where a number or a string is wanted is a fault, `undef
where a number is wanted` or `undef where a string is wanted`, and
printing wants a string. (perl warns, and carries on with 0 or
nothing.)

`undef` is written bare only at the end of an expression or before
one of `//`, `||`, `&&`, `and`, `or`, `xor`, `?` and `:`. Anywhere
else it goes in brackets, `(undef) + 1`, because perl takes whatever
follows a bare `undef` for something to make undefined: `undef * 2`
is not a multiplication to perl, and `undef + 1` doesn't compile.

## Variables

A variable holds one value. `my` declares it, and it must be declared
before it is used:

    use v5.42;
    my $count = 3;
    my $name;
    say $count + 1;                             # 4
    say defined $name ? "named" : "no name";    # no name

A variable declared without a value holds undef until it is given
one. Using it as a number or a string before then is a fault, as any
undef is.

A name is a letter or an underscore, then letters, digits and
underscores, all ASCII, hard against its dollar: `$total`, `$x2`,
`$_tmp`. It is 251 characters at most, as in perl. Three names are
not a program's to declare, `$a`, `$b` and `$_`: perl keeps them for
itself. (`$_` is what a `for`, a `map` or a `grep` gives its block,
and `$a` and `$b` what a `sort` gives its: "Arrays and lists",
below.) `${name}` and
`$ name`, which perl takes, are refused too.

A variable is visible from the statement after its `my` to the end of
the block it is declared in. So `my $x = $x + 1;` in an inner block
makes a new `$x` from the outer one, and at the top of a program,
where there is no outer one, it is refused. A second `my` of a name
in the same block is refused (perl warns that it masks the first);
in an inner block it is a new variable, which hides the outer one
until the block ends.

A `my` begins a statement. It can't stand in the middle of one, `say
my $x;`, or under a modifier, `my $x = 5 if $y;`, where perl would
leave in the variable whatever it last held when the test fails. The
other places are the test of an `if`, a `while` or an `until`, and
the first part of a `for`, described below.

### Assignment

`=` puts a value in a variable. Its left side is a variable, or a
`my`, and nothing else: no brackets round it, no expression.

    my $x = 1;
    $x = $x + 1;
    my $y = $x = 10;      # right to left: both are 10

A sign straight after the `=` needs no blank after it or one before
it: `$x = -$y` and `$x =-$y` are fine, and `$x =- $y` is refused,
because perl warns that it reads as `-=` written backwards.

An assignment has a value, which is the variable, so it can stand
inside an expression in brackets: `say 1 + ($x = 5);` prints 6 and
leaves 5 in `$x`. Assignment binds more loosely than everything but
`not`, `and`, `or` and `xor`, so the whole of `$x = $y || 2` or `$x =
$n > 0 ? "some" : "none"` is assigned.

The assigning operators are `+=`, `-=`, `*=`, `/=`, `%=`, `**=`,
`.=`, `x=`, `||=`, `&&=` and `//=`. `$x += 2` is `$x = $x + 2`, and
so on for each:

    my $total = 10;
    $total += 5;          # 15
    $total .= "!";        # the string 15!
    my $name;
    $name //= "nobody";   # nobody: it was undef
    $name ||= "somebody"; # still nobody: it is true

`||=`, `&&=` and `//=` work their right side out only if they are
going to assign it. A variable that holds undef may be the left side
of `+=` and `-=`, where it counts as 0, and of `.=`, where it is the
empty string; perl says nothing about those either. Under `*=`, `/=`,
`%=`, `**=` and `x=` an undef is the fault it would be without the
`=`.

### ++ and --

`$x++` and `++$x` add one to a variable, and `$x--` and `--$x` take
one away. They are hard against the variable and work on nothing else:
`++5` and `($x)++` are refused. Before the variable, the value of the
expression is the variable afterwards; after it, the value is what the
variable held before.

    my $n = 5;
    say $n++;     # 5
    say $n;       # 6
    say --$n;     # 5

What is left in the variable depends on what it held. An Int goes up
or down by one, and faults with `integer overflow` at either end. An
undef becomes 1 or -1, and `$x++` on an undef is worth 0. A boolean
becomes the Int. A Num goes up or down by one as arithmetic would have
it: `++` on 5.0 leaves the Int 6, `--` leaves the Num 4.

A string must be a number, and is stepped as one: `"12"` becomes 13,
and `"1.5"` becomes 2.5. In perl `++` on a string that isn't a number
makes the next string in a sequence of its own (`"aa"` to `"ab"`);
here that is the fault `not a numeric string`.

perl has two answers for some steps, by what the variable was used as
before, and each of those is a fault, as everywhere: `++` on a string
of digits that begins with a zero (`"009"` becomes the string `010`,
or the number 10); `++` or `--` on a string that is a whole number
whose size is 2^53 or more, before the step or after it; `--` on a
whole Num that would reach 2^53 below zero; and a Num that is 2^53 or
more in size, where perl warns that precision is lost (`++` from 2^53
up and below -2^53, `--` above 2^53 and from -2^53 down).

### When a variable is read

A variable is read when the operator it is an operand of runs, not
when it is written down. That only shows when the same statement
changes it:

    my $x = 3;
    say $x + ($x = 5);      # 10: both operands are $x, read after the assignment
    say $x++ + $x;          # 11: 5, and then the 6 that is in $x by then

perl does the same, and the language follows it. What is "the
variable" here: `$x` itself, in brackets or after a unary plus; an
assignment, and `++$x` and `--$x`, whose value is the variable; and
whichever operand `||`, `&&`, `//`, `or`, `and` or `? :` gives.
Anything else is a value, worked out where it stands: `$x++`, `-$x`,
`$x + 0`.

One place is refused. perl joins a row of dots as a single operation
and reads every piece of it late, so in perl `$x . "a" . ($x = 5)` is
`5a5`. In a concatenation, **a later piece may not change a variable
that an earlier piece reads**: make the change a statement of its
own. A change in an earlier piece is fine, `($x = 5) . $x`, and so is
a change to another variable.

And one more, for a fault in perl itself: `$t .= ($u = $x . $z);`
never assigns `$u` in perl 5.42. So **the right side of `.=` may not
be an assignment of a concatenation**. Make the assignment first, in
a statement of its own. A string with more in it than one variable is
a concatenation to perl, so `$t .= ($u = "$x$z");` is refused too.

### A statement that is an expression

An assignment, a `++` or `--`, and a `my` are statements. Nothing
else that is only an expression is: `$x + 1;` and `$x;` are refused,
since perl warns that each is useless. And a statement is one of
them, not two joined: `$x = 1 and $y = 2;` is refused (perl warns of
it too): write it as an `if`.

### say and a variable

After `say` or `print`, perl takes a variable for a file handle when
it is followed by a blank and then by something that could begin a
value: in `say $x -1;` perl reads `-1` as the thing to print and `$x`
as where to print it, and stops. The language refuses each such
shape, with a message that says so: a blank after the variable and
then a `-` or `+` hard against what follows, a dot and a digit, a
slash hard against what follows, or a `*`, `%`, `<` or `&` hard
against a name. `say $x - 1;` and `say $x-1;` are what they look
like, to perl and here. perl makes the same guess about the first
argument of `substr` and `index`, so `substr($x -1, 0)` is refused
too; `substr($x - 1, 0)` is fine.

## Blocks, if and unless

A block is statements in braces. It runs them in order, and a
variable declared in it ends with it:

    my $x = 1;
    {
        my $x = 2;
        say $x;     # 2
    }
    say $x;         # 1

A block on its own must have a statement in it: `{ }` is something
else to perl (an empty hash), and is refused.

`if` runs its block when its test is true, by the rules of truth
above. It may be followed by any number of `elsif`s, each with a test
and a block, and by an `else`; one block runs at most, the first
whose test is true, and the tests after that one are not worked out.

    my $n = 15;
    if ($n % 15 == 0) {
        say "FizzBuzz";
    } elsif ($n % 5 == 0) {
        say "Buzz";
    } elsif ($n % 3 == 0) {
        say "Fizz";
    } else {
        say $n;
    }

The test is in brackets and each block in braces, always; the word is
`elsif`, and `else if` is refused. A block of an `if` may be empty.

`unless` runs its block when its test is false. It takes no `else`
and no `elsif`: that is an `if` written backwards, and is refused.

A `my` may stand in the test of an `if` or an `unless`, where it is
always reached. The variable is then visible in the blocks of that
`if`, in the tests of its later `elsif`s, and not after it:

    if ((my $rest = $n % 7) > 3) {
        say "more than three over: " . $rest;
    } else {
        say "at most three over: " . $rest;
    }

It can't stand on the right of `&&`, `||` or `//` or in a branch of `?
:` there, where it might not be reached.

A statement may be followed by `if TEST` or `unless TEST` in place of
a block:

    say "negative" if $n < 0;
    $n = 0 unless defined $n;

The statement before the modifier is `say`, `print`, an assignment or
a `++` or `--`: not a `my`, not a block, not another `if`. One
modifier to a statement. After `say (...)` written with a blank
before its bracket, the modifier is on the line the brackets close
on, as the semicolon would be.

**A `=` where a value is tested for truth is refused when its right
side is a constant**: `if ($x = 5)` is almost always a mistyped `==`,
and perl warns of it. A right side is a constant when it has no
variable in it, or none that matters: in `$x = 0 && $y` the `$y` is
behind a test that is already decided, and perl warns of that as
well. That goes for the test of an
`if`, `unless` or modifier, the left of `&&`, `||`, `//`, `and` and
`or`, the test of `? :`, and any of those through a `!` or `not`.
`if ($x = $y)` and `if ((my $r = $n % 7) > 3)` are fine.

A fault in a test names the line of its `if` or `elsif`; in the test
of a modifier, the line its statement starts on.

## Loops

`while` runs its block as long as its test is true, testing before
each time round. `until` runs it as long as the test is false.

    my $n = 3;
    while ($n > 0) {
        say $n;
        $n--;
    }
    until ($n == 3) {
        $n++;
    }

The test is in brackets and the block in braces, as with `if`, and
the test is a test in every way an `if`'s is: `while ($n = 5)` is
refused. A loop that should run until something inside it says stop
is `while (1) { ... }`. `while () { ... }`, which perl takes for the
same thing, is refused.

`for` is the loop with three parts:

    for (my $i = 0; $i < 3; $i++) {
        say $i;
    }

The first part runs once. Then the test; if it is true, the block,
then the third part, then the test again. Any part may be left out,
and a `for` with no test runs until it is told to stop: `for (;;) {
... }`.

The first and third parts are what could be statements: an
assignment or a `++` or `--`, and in the first part a `my`. Each may
be several of those with commas between, which run left to right:

    for (my $lo = 0, my $hi = 9; $lo < $hi; $lo++, $hi--) {
        say $lo . " " . $hi;
    }

That is the only place a comma joins expressions. The test is one
expression. `for` with a list to go through, `for my $x (1, 2, 3)`,
is another loop, under "Arrays and lists" below.

A statement may be followed by `while TEST` or `until TEST`, and then
it runs again and again, the test first each time:

    $n++ while $n < 10;
    say $n-- until $n < 8;

so `say "never" while 0;` prints nothing. The statement is `say`,
`print`, an assignment or a `++` or `--`, as under `if`.

perl's `do { ... } while (TEST);`, which runs its block before the
first test, is not in the language. Write `while (1) { ...; last
unless TEST; }`.

### What is new each time round

A variable declared in a loop's block is a new variable each time
round, undef until it is given a value:

    my $i = 0;
    while ($i++ < 3) {
        my $seen;
        say defined $seen ? "still here" : "new";    # new, three times
        $seen = $i;
    }

So is one declared in the test of a `while` or an `until`, which the
block can see: `while ((my $left = $total - $used) > 0) { ... }`.
Neither is visible after the loop.

A `my` in the first part of a `for` is one variable for the whole
loop, as it has to be for the loop to count, and is gone after the
loop too. A `my` may not stand in a `for`'s test or its third part,
or before a `while` or `until` modifier.

### last and next

`last;` leaves the loop it is in, and `next;` goes on to the loop's
next time round: in a `for`, the third part runs and then the test.

    for (my $i = 0; $i < 10; $i++) {
        next if $i % 2;         # odd: on to the next one
        last if $i > 6;         # and no further than 6
        say $i;                 # 0, 2, 4, 6
    }

They are statements, and take an `if` or an `unless` after them and
nothing else. perl takes them inside expressions as well, `$done and
last;`; here that is `last if $done;`.

They go through the blocks of an `if`, as above and as in:

    while (1) {
        if ($n > 100) {
            last;
        }
        $n *= 2;
    }

**But not through a bare block.** To perl a block on its own is a
loop that runs once, so in `while (...) { { last; } ... }` the `last`
leaves the inner braces and the `while` carries on, with nothing said.
A `last` or `next` whose nearest surrounding loop or bare block is a
bare block is refused, with a message that says which braces it would
have left. Give the loop a label and say which loop is meant.

### Labels

A loop may have a label, and `last` and `next` may name it, to leave
or go on with a loop further out than the nearest:

    ROW: for (my $row = 0; $row < 3; $row++) {
        for (my $col = 0; $col < 3; $col++) {
            next ROW if $col > $row;
            say $row . "," . $col;
        }
    }

A label is written in capitals, digits and underscores, starting with
a capital, hard against its colon, before a `while`, an `until` or a
`for`: one label to a loop, and on nothing else. A `last` or `next`
that names a label must be inside a loop with that label, or the
program is refused. (perl looks for the loop only when the `last`
runs, and stops the program there if there is none.) If two loops,
one inside the other, have the same label, the inner one is meant.

### Faults in a loop

A fault in a loop's test, or in the first or third part of a `for`,
names the line of the `while`, `until` or `for`. Under a `while` or
`until` modifier it names the line the statement starts on.

A loop that never ends is a program that never ends; nothing stops
it.

## Subs

A sub is a piece of the program with a name, which the program calls:

    sub area($width, $height) {
        return $width * $height;
    }
    say area(3, 4);

It stands at the top level of the file, among the statements, and may
be called from anywhere in the file, before the sub is written or
after. It is not written inside a block, a loop or another sub: perl
ties a sub written there to the first time round, and warns of one in
a sub.

A sub's **signature** is the brackets after its name, with `()` for
no parameters. A sub may be written with none, `sub f { ... }`: it
then takes any number of arguments, each of them worked out, and
sees none of them. To perl they are in `@_`, which is not in the
language; a sub that wants its arguments names them in a signature.
`sub f() { ... }` takes no arguments, and one is a fault.

A sub's name is letters, digits and `_`, at most 251 characters. It
may not be a word perl has a meaning for, whether the language has
the word or not: perl would ignore the sub, or not compile the call
(with `sub q($x) {...}`, `q(5)` is the string `5`). That is perl's
whole list of keywords and functions; the names `use v5.42;` brings
in, `trim`, `ceil`, `indexed` and the rest; the names perl calls by
itself, `BEGIN`, `END`, `AUTOLOAD`, `DESTROY`, `import`; and its file
handles, `STDIN`, `STDOUT`. Nor may it be `v` and digits, `v65` or
`v1_0`, which perl reads as a version string where it hasn't yet seen
the sub. Two subs may not have one name.

### Parameters

A parameter is a variable of the sub's, given its value by the call:

- `$name`: an argument is required.
- `$name = EXPR`: the argument may be left out, and then the
  parameter is EXPR, the default.
- `$name //= EXPR`: the default is used when the argument is left
  out and also when it is undef.
- `$name ||= EXPR`: when it is left out, and when it is false.
- `$` alone takes an argument and names nothing; `$=` takes one or
  none; `$ = EXPR` runs EXPR when there is none.

The required ones come first. A last parameter may be `@rest`, which
takes every argument that is left ("Arrays and subs", below);
or `%opts` ("A hash as the last parameter").

    sub greet($name, $greeting = "hello") {
        return $greeting . ", " . $name;
    }
    say greet("world");             # hello, world
    say greet("world", "goodbye");  # goodbye, world

A default is worked out at each call that needs it, and only then, so
`$n++` as a default counts those calls. The parameters are filled in
from the left, and a default may use the ones before it: `sub box($w,
$h = $w)`. A default is read before its own parameter exists, as the
right side of a `my` is: in `sub f($x = $x)`, the default is the
file's `$x`.

**A parameter is a copy.** Assigning to one changes nothing outside
the sub. Two parameters may not have one name, and a `my` at the top
of the body may not take a parameter's name: perl warns of both. A
parameter may have the name of one of the file's variables, and hides
it.

**Too few arguments, or too many, is a fault**: `too few arguments
for area: got 1, expected 2`. Every argument is worked out first, as
in perl, which dies there.

### Calling

A call is the name and brackets, `area(3, 4)`, with `()` for no
arguments: always the brackets, since without them perl has to know
whether it has seen the sub. A comma may follow the last argument. Two
commas together are refused: perl takes `f(1,,2)` for two arguments,
in silence.

A call is a value, and it is a statement by itself:

    hanoi(10, "a", "c", "b");
    log_line("done") if $verbose;

The arguments are worked out from the left. **An argument that is a
variable is read as the sub takes it**, after the other arguments
have run, as an operand is (see "When a variable is read"): with a sub
`set` that changes `$x`, `show($x, set())` hands `show` the new `$x`.
`show($x + 0, set())` hands it the old one, a value worked out before
`set` ran. A sub takes its arguments one at a time, a default running
when its turn comes, so a `//=` default that changes a variable is
seen by the arguments after it.

Two things perl reads another way are refused:

- **A minus hard against a one-letter name**, `-e(2)`: to perl that
  is a file test, of a file called `2`. Write `- e(2)` or `-(e(2))`.
- **A blank between a name and its bracket, first after `say` or
  `print`**, `say f (1);`: perl takes `f` for a file handle unless it
  has already seen the sub. Anywhere else the blank is fine.

`(...) x N` after `return`, as a sub's last statement or as an
argument repeats a list, as it does to perl, and is that many values.
Without the brackets, `"ab" x 3`, it is one string.

### return, and what a sub is worth

`return EXPR;` ends the call, from inside any loops and blocks, and
the call is worth EXPR. `return;` ends it with nothing to give. Either
may have an `if` or an `unless` after it:

    sub sign($n) {
        return "negative" if $n < 0;
        return "zero" unless $n;
        return "positive";
    }

`return` is a statement, and only that: perl takes `$ok and return
1;` and `my $x = return 5;`, and the language asks for the `if`. It is
not written outside a sub.

**What a call gives is a copy**: with `sub get() { return $total; }`,
`get() + step()` uses what `$total` held when `get` returned,
whatever `step` does to it afterwards.

A sub that ends without a `return` is worth its last statement, when
that is an expression: an assignment, a `++`, a call, a `my`, or a
value by itself, which is a statement in this one place:

    sub double($x) { $x * 2 }

A sub that ends in `say` or `print` is worth `true`, as in perl.

**A sub that ends any other way has no value**: in an `if` or
`unless`, a loop, a block, or a statement with a modifier, `return 1
if $x;` being one. Calling it as a statement is fine. Using its value
is a fault, `f has no value: it does not end in a return or an
expression`. (perl gives the last thing it happened to work out,
which is usually the test: `sub f($x) { if ($x) { "yes" } }` gives 0
for `f(0)`.) End the sub with a `return`.

**A sub that returns nothing**, by `return;` or an empty body, is
undef where one value is wanted: `my $v = f();`. In a list it is no
value at all, as in perl: `g(f())` calls `g` with no arguments, `say
f();` prints an empty line, and `my @r = f();` is empty. `return
undef;` is one value, an undef, everywhere.

A call hands on how it was called: `return g();`, a last statement
`g();`, the branches of `? :`, the right side of `||`, `&&`, `//`,
`and` and `or`, brackets and a unary plus all pass to `g` whether a
value, a list or nothing was wanted of the sub they are in.

### Variables in a sub

A `my` in a sub is the sub's own, and new at every call: a sub that
calls itself has its variables once for each call that is open.

A sub may also read and change **the file's variables**: those
declared by a `my` at the top level of the file, above the sub.

    my $count = 0;
    sub tick() {
        $count++;
    }

A file variable is undef from the moment the program starts, and its
`my` does not empty it. That shows only when a sub that uses the
variable is called above the `my`: after `tick(); my $count;`, with
`tick` written below, `$count` is 1. (A `my` in a block, a loop or a
sub is undef each time it is reached, as before.)

**In a row of `.`, a later piece may not call a sub that can change a
variable an earlier piece reads**: perl joins the row as one
operation and reads every piece late, so `$x . "-" . ch()` has the
`$x` that `ch` left. "Can change" means by the sub's own assignments,
or those of any sub it calls. The left side of `.=` is the first
piece. Make the call a statement of its own:

    my $c = ch();
    say $x . "-" . $c;

A `last` or `next` in a sub is for a loop of that sub.

### How deep

A sub may call itself, and subs may call each other. perl warns,
`Deep recursion`, when one sub has 100 calls of itself open at once;
the language says nothing there, and a program that goes that deep
carries one more line at its top, with the pragmas, so that perl is
as quiet:

    use v5.42;
    no warnings 'recursion';

The line changes nothing about what the program does, here or in
perl.

There is a limit all the same, and it is the implementation's, not
the language's: today the calls that are open may hold 4 MB between
them, about 3,700 calls deep for a small sub and fewer for a large
one. Past it the program stops with `fault: recursion too deep`. perl
has no such limit.

A fault names the line of the statement that was running: one in the
sub while the sub runs, and the caller's again once it has returned.

## Arrays and lists

An array is a row of values with a name:

    my @primes = (2, 3, 5, 7);
    say $primes[0];          # 2, the first
    say $primes[-1];         # 7, the last
    say scalar(@primes);     # 4, how many

`@primes` is the array, and `$primes[1]` one **element** of it. An
array's name is its own: `@x` and `$x` are two variables, and `$x[0]`
is an element of `@x`. An array may be called `@a` or `@b`, though a
variable may not be `$a` or `$b`.

`my @a;` makes an empty one. A `my` in a block, a loop or a sub makes
a new array each time it is reached.

### Lists

A **list** is values with commas between them, in brackets: `(1, 2,
3)`. It has no name, and it **flattens**: a list in a list, or an
array in a list, is its values, so `(0, (1, 2), @primes)` is seven
values in a row. `()` is the list of none. One comma may follow the
last value.

A list is a row of values, **copied as it is built**. What a list is
for:

    my @b = (1, 2, 3);          # assigned to an array
    @b = (@b, 4);               # the array's own values among them
    say "x", @b, "y";           # printed, one after another
    total(@b, 10);              # handed to a sub, as its arguments

`say` and `print` take a list, and print each value with nothing
between. `say @b;` prints `1234`.

A **range**, `1 .. 5`, is the whole numbers from one end to the other,
in a list. Each end is cut toward zero (`1.9 .. 4.1` is 1 to 4), and a
range whose first end is past its second is no values. A string for
either end is a fault: perl's range of strings (`"a" .. "e"`) is
another thing.

**`(LIST) x N`**, a list in brackets and a count, is the list N times,
where a list is wanted: `my @zeros = (0) x 10;`. Without the brackets,
or where one value is wanted, `x` repeats a string, as before.

A call of a sub in a list is its value; a sub that returned nothing
(`return;`) is no value there, so `(1, none(), 2)` is two values.

### Elements

`$a[I]` is the element at index I, counted from 0; a negative index
counts from the end, `$a[-1]` the last. The index is a whole number,
by the rule `substr` has for a position: a fraction is cut toward
zero, and an undef, a string that is no number, or a number too large
to be a whole one is a fault.

**Reading past either end gives undef**, in silence, and makes
nothing: the array is as long as it was.

**Storing past the end makes the array longer**, and the elements
between are undef:

    my @a = (1, 2);
    $a[4] = 5;               # (1, 2, undef, undef, 5)

Storing before the start (`$a[-3] = 0` in an array of two) is a
fault.

An element is assigned and worked on as a variable is: `$a[0] = 5`,
`$a[$i] += 2`, `$a[1] .= "x"`, `$a[3] //= 0`, `$a[0]++`. An operator
that reads the element and stores it (`+=`, `.=`, `||=`, `++` and the
rest) makes the element first, so `$a[9] //= 0` makes the array ten
long whatever it then stores.

The order things are worked out in is perl's. For `$a[I] = V`: V,
then I, then the store. For `$a[I] += V` and its kin: I first, then V.

`$#a` is the last index, which is one less than how many, and -1 for
an empty array.

### How many

`scalar(@a)` is how many values an array holds. And **wherever one
value is wanted, an array is that count**:

    my $n = @a;              # how many
    if (@a) { ... }          # true unless it is empty
    while (@a > 2) { ... }
    say "holds " . @a;

That goes for the left side of `||`, `&&` and `//` too: `@a || (9)`
is the count of `@a`, if it is not empty, and not `@a`.

`length(@a)` and `defined(@a)` are refused: perl warns of the first
and does not compile the second.

A list, a slice, a range and `splice` are refused where one value is
wanted: `my $x = (4, 5, 6);` gives 6 in perl, with warnings.

### List assignment

A list of variables in brackets, on the left of `=`, takes the values
of the list on the right, one each:

    my ($first, $second) = (10, 20);
    ($first, $second) = ($second, $first);     # a swap
    my ($head, @rest) = @a;

The right side is worked out first, the whole of it, which is why the
swap works. When the values run out the rest of the targets are
undef; values left over are dropped. A target may be a variable, an
element, `undef` (to skip a value), and, last, an array, which takes
every value that is left. `my ($x) = @a;` is the first element, where
`my $x = @a;` is the count.

`@a = LIST;` gives an array new values, and `my @b = @a;` copies one:
the two are then separate.

**An assignment of a list is a statement.** In perl it has a value,
the count of its right side, so that `if ((my @r = f()))` tests
whether `f` gave anything; here that is `my @r = f(); if (@r)`.

`my ($x, $y);` declares both, undef.

### push, pop, shift, unshift, splice

`push @a, LIST` adds values at the end, and `unshift @a, LIST` at the
start; each is worth the new count, and each needs a value to add.
With brackets or without: `push(@a, 1, 2)`.

`pop(@a)` takes the last value off and gives it, and `shift(@a)` the
first; from an empty array each gives undef. The brackets may be left
off only where the array ends the expression, `my $x = pop @a;`: perl
does not compile `pop @a + 1`. `shift` always names its array.

`splice(@a, OFFSET, LENGTH, LIST)` takes LENGTH values out at OFFSET,
puts LIST there, and gives what it took, as a list:

    my @a = (0, 1, 2, 3, 4, 5);
    my @gone = splice(@a, 1, 2);       # @gone is (1, 2); @a is (0, 3, 4, 5)
    splice(@a, 1, 0, 7, 8);            # nothing out, two in: (0, 7, 8, 3, 4, 5)
    splice(@a, -1);                    # the last one out

With no LENGTH, everything from OFFSET on; a negative OFFSET counts
from the end; a negative LENGTH leaves that many at the end. An
OFFSET past the end or before the start is a fault.

### Slices

`@a[1, 2]` is a **slice**: the elements at those indexes, as a list,
undef for an index past either end. The indexes are a list themselves,
so `@a[1 .. 3]` and `@a[@which]` are slices. `(LIST)[2]` and
`(LIST)[0, 2]` slice a list; a slice of a list with no values is no
values.

`@a[0]`, a slice with one index, is refused: perl warns that `$a[0]`
was meant. A slice may be assigned to, `@a[0, 1] = ("x", "y");`: that
is under "Slices", with a hash's.

### A loop over a list

    for my $x (LIST) {
        ...
    }

runs its block once for each value of the list, with `$x` that value.
`foreach` is another spelling of the same word:

    my @primes = (2, 3, 5, 7);
    my $sum = 0;
    foreach my $p (@primes) {
        $sum += $p;
    }

The list is any list: an array, several, values, a slice, a call,
`(@a, 0, @b)`. It is **worked out once, before the first time round,
and copied**. `$x` is the loop's own variable: new each time round,
gone when the loop ends, and another variable from any `$x` outside.
`last` and `next` and labels are as in any loop.

**`$x` is read-only.** In perl it is the element itself, so that `$x
*= 2` in the block rewrites the array; here it is a copy, and a
program that assigns it, steps it or appends to it is refused. Take
it into a `my` to change it, or store by index (below).

**A range alone is counted, and never built**: `for my $i (1 ..
1000000)` holds no list of a million numbers. Its ends are fixed when
the loop starts.

#### While the loop runs, its arrays are frozen

perl's loop walks the array itself: a `push` in the block makes the
loop longer, a `shift` makes it skip, a store shows up in `$x`. Here
the loop walks a copy, so those programs would print something else;
and so **every array named anywhere in the loop's list is frozen
until the loop is left**. Reading it is fine, by the block or by a
sub the block calls. Storing to an element of it, or changing its
size, by either, is a fault:

    for my $x (@a) {
        push @a, $x * 2;      # fault: an array was changed while a
    }                         # foreach is over it

The array is given back however the loop is left: at its end, by
`last`, by a `last` or `next` to a loop outside it, by `return`.

"Named anywhere" is meant: `(@a, @b)`, `@a[0, 1]`, `$a[0]`, `$#a` and
`scalar(@a)` in the list all name `@a`. So `for my $i (0 .. $#a)`
freezes `@a` too. To change an array as you go through it, take its
count first, which names nothing:

    my $n = @a;
    for my $i (0 .. $n - 1) {
        $a[$i] *= 2;
    }

or build a new array from the old one.

The same goes for a plain variable, where there is nothing to freeze:
**a loop whose block can change a variable its list names is
refused**, as the program compiles, the subs the block calls
included.

    for my $x ($lo, $hi) {
        $lo = 0;              # refused: the list names $lo
    }

That is one rule for every place the variable can stand in the list,
and it refuses `for my $i (1 .. $n) { $n-- }` too, where perl would
have agreed; `my $end = $n;` before the loop says what is meant.

**An element or a slice past either end of its array, in the loop's
list, is a fault**: perl would make the element, and the array
longer. (Read anywhere else it is undef, and makes nothing.)

A range in a loop of its own may not begin or end within 512 of the
smallest integer: perl refuses that loop, and so it is a fault.

#### What is refused

`for $x (LIST)`, with no `my`: perl lends the loop a variable from
outside and gives it its old value back after. `for my $x ()`,
which perl does not compile. `for my ($k, $v) (LIST)`, two at a time.
And `foreach (FIRST; TEST; EACH)`: to perl `foreach` and `for` are
one word, and here the loop of three parts is spelled `for`.

### `$_`, map and grep

Four constructs run a block, or one statement, once for each value of
a list, and call that value **`$_`**:

    for (LIST) { ... }            # the loop above, with $_ for its variable
    STATEMENT for LIST;           # the same for one statement
    map { ... } LIST              # a list made from a list
    grep { ... } LIST             # the values of a list that pass a test

    my @a = (3, 1, 4);
    for (@a) {
        say $_ * 2;
    }
    say "item: ", $_ for @a;
    my @doubled = map { $_ * 2 } @a;       # (6, 2, 8)
    my @big = grep { $_ > 2 } @a;          # (3, 4)

Each is the loop over a list of the section before, under another
spelling, and everything said there holds: the list is worked out
once and copied; `$_` is a copy, new each time round, and
**read-only**; every array named in the list is frozen while it runs;
a block that can change a variable the list names is refused; an
element or a slice past the end of its array, in the list, is a
fault.

**`$_` is seen in the block, or the statement, of the construct that
gives it, and nowhere else.** A sub called from the block does not
see it (hand it over: `f($_)`); outside all four there is no `$_`;
and it can not be declared. One of the four inside another has a
`$_` of its own, and the outer one is itself again after. The list of
an inner one is outside it, so it sees the outer `$_`:

    for (1, 2, 3) {
        my @upto = map { $_ * 10 } 1 .. $_;     # 1 .. $_ is the outer one
    }

`$_` is always written: `grep { defined($_) } @a`, `say $_ for @a;`.
perl's builtins that mean `$_` when given nothing are refused without
it.

#### map

`map`'s block is statements and then an expression, which is the
block's value: one value, several, or none, and `map` gives all of
them in a row.

    my @pairs = map { ($_, $_ * $_) } 1 .. 3;            # (1, 1, 2, 4, 3, 9)
    my @evens = map { $_ % 2 == 0 ? ($_) : () } @a;      # some, by a test
    my @lens = map {
        my $w = $_;
        length($w)
    } @words;

A `my` in the block is new each time round.

#### grep

`grep`'s block ends in one value, which is tested for truth, and
`grep` gives the values of the list for which it was true, each a
copy.

#### Where one value is wanted

`map` and `grep` are **how many values they give**:

    my $n = grep { $_ > 2 } @a;          # 2
    if (grep { $_ eq "x" } @names) { ... }

After `return`, though, each is a list like any other, and a call
that wants one value is the fault (above).

#### How they are written

`map` and `grep` take a block, then a list with no comma between and
no brackets round the two: `map { ... } @a`. They **take every value
to the end of the list they stand in**, as perl's do: in `(0, map {
$_ * 2 } @a, 9)` the 9 is doubled too. Brackets round the whole end
it: `(0, (map { $_ * 2 } @a), 9)`.

The statement under a `for` is what may stand before an `if`: `say`,
`print`, an assignment, a step, `push` and its kin, a call. Not
`last`, `next` or `return` (to perl they would leave the `for`'s own
loop), not a `my`, and no second modifier.

In a block:

- **no `return`**: in perl it ends the sub from a `map` block. And
  **no `last` or `next` to a loop outside the block**; one for a loop
  written inside the block is fine.
- **the block ends in an expression**, with no modifier; or in a
  `say` or a `print`, and is then worth `true`. The last statement
  may be two values joined by `or` or `and`. A list assignment has no
  value, and may not end one.
- **what comes first in it** may not be a string or a number with a
  comma after it, nor another `{`, and the block may not be empty:
  perl takes each of those for a hash, not a block. `map { ($_, 1)
  }` and `map { "x" . $_ }` are blocks.

`map` and `grep` may stand as statements, for what their blocks do.
`map EXPR, LIST`, with no block, is not in the language.

For "what a list may not do", below: a block is part of its `map` or
`grep`, so what the block changes, they change; and `grep` hands on
the things it was given, so what its list names, it names. `map`
gives copies.

### sort

`sort LIST` is the list in order, as strings are ordered (`cmp`):

    my @words = ("pear", "fig", "apple");
    say join " ", sort @words;                 # apple fig pear
    say join " ", sort 10, 9, 100;             # 10 100 9: as strings

Every value is made a string first, so an undef in the list is a
fault.

With a block, the block says the order. It is handed two of the
values, as **`$a`** and **`$b`**, and gives a number: below zero if
`$a` comes first, above if `$b` does, zero if neither.

    say join " ", sort { $a <=> $b } 10, 9, 100;            # 9 10 100
    say join " ", sort { $b <=> $a } 10, 9, 100;            # 100 10 9
    say join " ", sort { length($a) <=> length($b) or $a cmp $b } @words;
    my @top3 = (sort { $b <=> $a } @scores)[0 .. 2];

The sort is **stable**: values the block calls equal stay in the
order they were given. `reverse sort { ... } @a` is the other way
round.

`$a` and `$b` are like `$_`: copies, read-only, seen in the block
alone (not in a sub it calls: hand them over), never declared. A
`sort` inside a `sort`'s block has its own. `$a[0]` is still an
element of an array called `@a`.

The block is a block as `map`'s is: statements, and then an
expression, which is its value. No `return`, no `last` or `next` to a
loop outside it. Its value is a whole number, by the rule an index
has: a fraction is cut toward zero (so 0.5 is "equal", as in perl),
an undef or a string that is no number is a fault, and so is a number
outside 32 bits, which perl would wrap.

**The comparisons are perl's, pair for pair and in perl's order.** A
block that counts or prints, and one whose answers are no consistent
order, give here exactly what they give in perl: the runtime's sort
is perl's own merge. `sort { $n++; $a <=> $b } 5, 3, 8, 1, 9, 2, 7`
leaves 14 in `$n`, there and here.

Like `map` and `grep`, `sort` works its list out once and copies it,
freezes every array named in it while it runs, faults for an element
or a slice past the end of its array there, and is refused when its
block can change a variable its list names. It is written with no
brackets of its own, and takes everything to the end of the list it
stands in. Unlike them it is a list only: **where one value is
wanted, `sort` is refused** (perl gives undef there). After `return`
it is a list like any other.

Three things perl reads another way:

- **What comes first after `sort`** may not be a word that is not
  one of perl's own, nor a scalar: `sort by_num @a`, `sort
  f(@a)`, `sort $x, $y`. perl takes the word, with its brackets too,
  for the name of a sub to compare by, and `true` there for the
  string `true`. A `+` before it says a value is meant, and so does a
  block: `sort +f(@a)`, `sort { $a cmp $b } $x, $y`.
- **`@a = sort { ... } @a;`**, an array sorted into itself with a
  block, faults if the array holds an undef. perl sorts that in
  place, and in doing so drops any element that was never stored to,
  which is a difference between two undefs that the language does not
  keep. `my @s = sort { ... } @a; @a = @s;` says it.
- A list of one value does not run the block; but for the four blocks
  perl never runs at all, `$a <=> $b`, `$b <=> $a`, `$a cmp $b` and
  `$b cmp $a`, the one value is still looked at, as a comparison
  would look at it, since perl turns it to a number or a string
  anyway.

For "what a list may not do", below: `sort` hands on the things it
was given, so what its list names, it names.

### Arrays and subs

An array among a call's arguments flattens, like any list: with `my
@p = (3, 4);`, `area(@p)` is `area(3, 4)`. So how many arguments a
call has may only be known as the program runs, and the fault for too
few or too many comes then.

A sub may use the file's arrays, those declared at the top level
above it, and its own. A file's array is empty from the moment the
program starts, and its `my` does not empty it again (as a file's
variable).

**A last parameter may take every argument that is left**, as an
array of the sub's own:

    sub largest($first, @rest) {
        my $most = $first;
        for my $x (@rest) {
            $most = $x if $x > $most;
        }
        return $most;
    }
    say largest(3, 9, 4);        # 9

`@rest` is a copy: changing it changes nothing of the caller's. It
may be empty. `@` alone takes the arguments and names nothing. Such
a parameter is the last, and has no default. It is filled when its
turn comes, after the defaults before it have run.

### A sub that gives back a list

`return` takes a list, and so does a sub's last statement:

    sub divide($n, $d) {
        return (($n - $n % $d) / $d, $n % $d);
    }
    my ($q, $r) = divide(17, 5);         # 3 and 2

    sub evens(@v) {
        my @out;
        for my $x (@v) {
            push @out, $x if $x % 2 == 0;
        }
        return @out;
    }
    my @e = evens(1 .. 10);

A list after `return` is in brackets, unless it is one thing that is
a list already (`return @out;`, `return reverse @v;`). `return ();`
is `return;`.

**Where a list is wanted, a call is every value its sub returned**:
none, one or many. So calls go wherever a list goes: `my @r = f();`,
`(f(), g())`, `for my $x (f())`, `say f();`, `g(f())`, `(f())[0]`.
What comes back is a copy, as an array assigned is: the caller's
array and the sub's are two, and a loop over `f()` freezes nothing.

**Where one value is wanted, a sub that returns a list is a fault.**
In perl such a call gives something else each time: the count for an
array, the last for a list in brackets, a string for `reverse`. Here:

    sub all() { return @a; }
    my $n = all();           # fault: all returned a list where one
                             # value is wanted

`my ($first) = all();` takes the first, `my @r = all(); my $n = @r;`
the count, and `return scalar(@a);` returns the count. What counts is
how the `return` is written, not what it holds as the program runs:
an array, a list of two or more, a range, a slice, `(LIST) x N`,
`splice`, `reverse`, and `? :` or `|| && //` with one of those for
an arm, whichever arm is taken. `return (7);` and `return $x;` are
one value. `return f();` hands on whatever its own call wanted. And
a call for nothing, `all();` as a statement, faults for nothing.

### join and reverse

`join(SEP, LIST)` is the values of the list as one string, with SEP
between them:

    my @parts = ("a", "b", "c");
    say join(", ", @parts);          # a, b, c
    say join("", reverse(@parts));   # cba
    say join "-", 1 .. 4;            # 1-2-3-4

Each value is made a string as `.` makes one, so an undef is a fault;
SEP is one value (an array there is its count) and is made a string
even if nothing is joined. A list of none joins to `""`.

`reverse(LIST)` is the list, last first. It is a list, and only where
a list is wanted: `my $s = reverse("abc");` is refused, since perl's
`reverse` there is another function, which reverses the characters
of a string.

Both may be written without brackets, and then take everything to
the end of the list they stand in: `say join ",", reverse @a;`. With
brackets, nothing may index them: `(reverse(@a))[0]`, not
`reverse(@a)[0]`.

For "what a list may not do", below: `reverse` hands on the things
it was given, so what its list names, it names; and `join` reads its
separator last, so a later item may not change it.

### What a list may not do

perl's lists are rows of the variables themselves, not of their
values, so a change made after a list was begun shows through it: in
perl, with a sub `bump` that changes `$x`, `my @b = ($x, bump());`
has the *new* `$x`. Here a list is a row of values. So that the two
never differ:

**A later part of an expression or a list may not change what an
earlier part names.** What is named is an element, a slice, an array
or `$#a`, and a variable that is an item of a list. "Change" is by
assigning it, storing to it, or changing its size, there or in a sub
that is called, however deep. The compiler works that out over the
whole program, and refuses:

    say $a[0] + shift(@a);        # refused: shift changes @a
    my @b = ($x, bump());         # refused: bump changes $x
    push @a, $a[0], grow();       # refused, if grow changes @a

The message says to take the value into a `my` first, which says
which value is meant:

    my $first = $a[0];
    say $first + shift(@a);

`$a[0] + $a[1]`, `($x, $y) = ($y, $x)`, `@a = (@a, 1)` and `push @a,
@a` change nothing they name after naming it, and are as they look.

## Hashes

A hash is values with names: each value is stored under a **key**,
which is a string.

    my %age = (ann => 31, bob => 27, cy => 44, dee => 19);
    say $age{bob};                 # 27
    $age{eve} = 52;                # a new key
    say scalar(%age);              # 5, how many keys

`%age` is the hash, and `$age{bob}` one **element** of it. A hash's
name is its own: `%x`, `@x` and `$x` are three variables, `$x{k}` is
an element of `%x` and `$x[0]` one of `@x`.

`my %h;` makes an empty one, and a `my` in a block, a loop or a sub a
new hash each time it is reached. `my %h = LIST;` and `%h = LIST;`
fill it from a list of keys and values by turns. **A key given twice
keeps its last value. A list with an odd number of values is a
fault**: perl warns, and gives the last key no value.

### `=>`, and a word that is a string

`=>` is a comma that makes a string of the word before it. `(ann =>
31)` is `("ann", 31)`. Any word will do, one of perl's own or the name
of one of the program's subs: `(if => 1, print => 2, total => 3)` has
the keys `if`, `print` and `total`, and calls nothing.

**The word and its `=>` are on one line.** Across the end of a line
perl still makes a string of most words, and of `v65` it makes the
character `A`; that is refused. A minus before the word is refused
too: `-bar => 1` is the key `-bar` to perl, so write `"-bar"`.

What stands before `=>` and is no word is an expression like any
other: `(1 => "one", $k => 2, "two words" => 3)`.

### Elements

Between the braces is the key. **One word alone there is that
string**: `$age{bob}`, `$h{if}`, `$h{ name }`, on one line with its
braces. Anything else is an expression, worked out and **made a string
as `.` makes one**: `$h{$k}`, `$h{"two words"}`, `$h{$i + 1}`. So the
keys `1`, `1.0` and `"1"` are one key, and `true` in brackets,
`$h{(true)}`, is the key `1`. An undef for a key is a fault, where
perl warns and uses the empty string; so is a whole Num from 10^15 up,
which prints two ways.

**Reading a key that is not there gives undef**, and makes nothing.
**Storing makes the key.** Every operator that works on a variable
works on an element, and makes its key first: `$count{$word}++`,
`$h{k} += 2`, `$h{k} .= "x"`, `$h{k} //= 0`. (`$h{k} &&= 1` makes the
key and stores nothing, as in perl.)

The braces are hard against the name, `$h{k}`: perl takes a blank
there. `$h{a}{b}` and `$h{a}[0]` are for step 13, and a comma in the
braces is refused.

### exists and delete

`exists $h{k}` is true if the key is there, whatever its value: a key
may hold undef, and `exists` is how to tell that from no key.

`delete $h{k}` takes the key away, and gives the value it had, or
undef if there was none.

Both take brackets or go without. Without them, an operator that
binds tighter than a comparison may not follow, since perl would read
it into the argument: `exists $h{a} + 1` is refused, `exists($h{a}) +
1` is 1 or 2, and `exists $h{a} && exists $h{b}` reads as it looks.
Both are for a hash's element alone: perl's `exists` and `delete` of
an array's are not in the language.

### keys, values and how many

`keys %h` is the hash's keys, in a list, and `values %h` its values.
`%h` itself, where a list is wanted, is its keys and values by turns:
`my %copy = %h;`, `my @flat = %h;`, `total(%h)`.

Where one value is wanted, each of the three is **how many keys there
are**: `my $n = %h;`, `if (%h) { ... }`, `keys(%h) + 0`,
`scalar(%h)`. An empty hash is false.

`keys` and `values` take brackets or go without, by the rule `exists`
has.

**A hash keeps its keys in the order they were first stored** (D27).
A key stored again keeps its place; a key deleted and stored again is
last. `keys`, `values` and the hash in a list all go in that order.
**This is the one place a program may print what perl does not**:
perl's order is its own, and another every run. A program that is to
print the same under perl sorts:

    for my $name (sort keys %age) {
        say $name, " is ", $age{$name};
    }

### A loop over a hash

A hash may stand in the list of a `for`, a `map`, a `grep` or a
`sort`: by its `keys`, by its `values`, by itself (keys and values by
turns), by a slice or by an element.

    for my $name (sort keys %age) { say "$name is $age{$name}"; }
    my $total = 0;
    $total += $_ for values %age;
    my @adults = grep { $age{$_} >= 18 } sort keys %age;

**While a loop is over a hash's `values`, the hash itself, a slice or
an element of it, the hash is frozen**, as an array is: the block may
read it (`$h{k}`, `exists`, `keys`, how many), and a store to it, a new
key, a `delete` or an assignment to it, from the block or from a sub
the block calls, is the fault `a hash was changed while a foreach is
over it`. In perl such a loop walks the hash's own values, and a
change under it shows through, or reads what was freed. The freeze is
given back on every way out of the loop.

**A loop over `keys` freezes nothing**: the keys are copies, so this
is the loop that changes a hash as it goes.

    for my $k (sort keys %h) { delete $h{$k} if $h{$k} == 0; }

How many keys there are, `scalar(%h)` or `keys %h` where one value is
wanted, freezes nothing either; `%h` itself as the end of a range, `1
.. %h`, names the hash and does. A hash's element in a string is a
copy, and freezes nothing.

**An element or a slice in such a list, whose key is not there, is a
fault** (`a key that is not there in a foreach, where perl would make
it`): perl makes the key, with undef. So is a slice with such a key
among a call's arguments.

### Slices

`@h{K1, K2, ...}` is the values at those keys, in the order asked, in
a list; undef for a key that is not there, and no key is made.

    my ($x, $y) = @point{"x", "y"};
    my @some = @age{@names};

The `@` says a list comes out, and the braces say it is a hash:
`@h{...}` is a slice of `%h`, and `@h[...]` of the array `@h`. A slice
by one key is refused, as perl warns of it: write the element. Where
one value is wanted a slice is refused.

**A slice may be assigned to**, a hash's or an array's, as a statement:

    @h{"a", "b"} = (1, 2);
    @h{"a", "b"} = @h{"b", "a"};      # a swap
    @row[0, 1] = ("x", "y");

The right side is worked out first, then every key or index, then the
stores, a value for each in turn. **A target the list does not reach
is stored an undef**, which makes its key, or grows the array, all the
same. A slice is the one target of its assignment: beside others in
brackets, `($x, @h{...}) = ...`, it is refused, and so are `@h{...} +=
1` and its kin.

`delete @h{K1, K2}` takes each key away and gives what each held, in a
list.

### A hash as the last parameter

A sub's last parameter may be a hash, which takes the arguments that
are left as keys and values by turns:

    sub box($text, %opt) {
        my %o = (left => "[", right => "]", %opt);
        return $o{left} . $text . $o{right};
    }
    say box("a"), box("b", left => "<", right => ">");

It is a copy, filled when its turn comes. `%` alone takes them and
names nothing. **An odd number of arguments left for it is a fault**,
raised as the sub is entered, before any default runs; perl dies
there too. It has no default, and nothing follows it.

### A hash's element in a string

`"$h{name}"` and `"$h{$k}"` are the element, made a string as `.`
makes one (an undef is a fault, as everywhere). **The key is a word or
a scalar variable, hard against its braces**, and nothing else: to
perl what stands there is code, with quotes, calls and arithmetic, so
`"$h{'a b'}"`, `"$h{ a }"`, `"$h{1}"` and `"$h{$i + 1}"` are refused.
Take the value into a `my` first, or join the pieces with `.`.

After the closing brace `[`, `{`, and `->` before `[ { @ $` are
refused, since perl reads on; anything else is text: `"$h{a}::x"`,
`"$h{a}->x"`. A slice in a string, `"@h{...}"`, is refused: join it.
`"%h"` is text, as it is to perl.

### What a hash may not do

`map { $_ => 1 } @list` is refused, for the comma in the block (perl
has to guess whether those braces are a block or a hash): put the pair
in brackets, `map { ($_ => 1) } @list`.

Not in the language: `each`; `%h{...}`, a slice of keys and values;
`keys %h = N`; `length(%h)` and `defined(%h)`.

**A later part of an expression or a list may not change a hash that
an earlier part names**, as with an array: an element, `values` and
the hash itself name it, `keys` does not, and a store, a `delete` and
an assignment to the hash are changes. `say $h{a}, delete $h{a};` is
refused: take the value into a `my` first.

**The key or the index of an element that is stored to may not
change a variable that a concatenation on the right reads**: `$a[$i++]
= $i . "v";` and `$h{$k = "x"} = "$k-$k";` are refused. perl joins
such a string as it stores it, after the index is worked out, and
would read the changed variable. Take the string into a `my` first.

## Memory

A program doesn't manage memory. A string the program can no longer
reach is freed by the runtime, sooner or later; the program can't
tell when, and nothing runs when it happens. A loop that makes a
gigabyte of strings one after another, keeping none, runs in a few
megabytes.

A program that needs more memory than there is stops with the fault
`out of memory`, at the statement that asked for it.

Three environment variables change how the runtime goes about this.
They are for testing the runtime itself, and none of them changes
what a program prints, short of `out of memory`:

- `CURLY_HEAP_CAP=BYTES`: the program may hold no more than this
  much, and faults with `out of memory` if it would.
- `CURLY_GC_STRESS=N`: look for strings to free at every Nth one
  made, and not when the runtime would have chosen to. Slower.
- `CURLY_GC_POISON=1`: never use a freed string's memory again, so
  that a mistake in the runtime shows itself at once.

Each is a whole number written in digits, and 0 or nothing turns it
off. Anything else stops the program before it starts, with a message
and exit status 2.

## When a program stops

A program that reaches its end exits with status 0, having printed
what it printed.

A **fault** stops it early: whatever it had printed, then one line on
stderr,

    fault: integer overflow at hello.pl line 3.

and exit status 1. The line is the one the statement starts on. A
fault can't be caught, and nothing the program would have printed
after it is printed. What a faulting program does print is always the
beginning of what perl prints for the same file: the language stops
early, and loudly, and never says anything perl wouldn't.

A line that begins `internal:`, with exit status 2, is something else:
a mistake in the compiler or the runtime that was caught as the
program ran, and never the program's doing. It is a bug to report.
