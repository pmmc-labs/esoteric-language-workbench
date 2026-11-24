# Curly

The language as it is, for someone writing programs in it: every form
and builtin, in prose with examples, no tables, changed in the same
commit as the feature.

What the language is meant to become is in [`DESIGN.md`](DESIGN.md),
and [`SURFACE.md`](SURFACE.md) says, for each construct of Perl,
whether it will be in. Neither is a description of what works. This
is, and so far it is short: a program can do arithmetic, build
strings, and print.

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

Two more lines may follow it, in either order, each once, before
anything else:

    use utf8;
    use open ':std', ':encoding(UTF-8)';

The first lets the program's text hold characters past ASCII, and the
second lets the program print them; each is described where it
matters, below. They are written exactly so (either kind of quote will
do), and no other `use` is in the language.

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

Every statement ends with a semicolon, the last one too, and there is
no empty statement: `;;` is refused.

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

They are the only statements there are yet, and each takes exactly one
expression, with brackets round it or without: `say "a", "b";` waits
for lists. Neither has a value, so neither can stand inside an
expression. What is said of `say` below goes for `print` too.

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
one blank between them, `say (1 + 2);`, the statement has to end on
that line, bracket, semicolon and all: perl looks along the line for
them and warns when they aren't there, and a program perl warns about
is refused.

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

**A `$` or an `@` in double quotes must have its backslash**: `"cost:
\$5"`, `"me\@example.com"`. To perl those begin a variable, and
putting a variable's value into a string comes later.

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

One spelling is refused: a sign after the name must have a blank
before it and none after, `length -5`. perl warns that `length - 5`
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
to be an Int is a fault.

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
