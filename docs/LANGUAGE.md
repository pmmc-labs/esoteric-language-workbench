# Curly

The language as it is, for someone writing programs in it: every form
and builtin, in prose with examples, no tables, changed in the same
commit as the feature.

What the language is meant to become is in [`DESIGN.md`](DESIGN.md),
and [`SURFACE.md`](SURFACE.md) says, for each construct of Perl,
whether it will be in. Neither is a description of what works. This
is, and so far it is short: a program can do arithmetic and print the
answers.

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

## The text of a program

A program is written in ASCII: the printable characters, the space,
the tab and the newline. Any other character is refused wherever it
is, in a comment too: a carriage return, so a file with Windows line
endings has to be converted; any control character; any character
past ASCII, until strings arrive and bring `use utf8` with them.

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

## say

`say` prints the value of an expression and a newline.

    use v5.42;
    say 42;
    say 2 + 3 * 4;
    say(7 / 2);

prints

    42
    14
    3.5

It is the only statement there is yet, and it takes exactly one
expression, with brackets round it or without.

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
