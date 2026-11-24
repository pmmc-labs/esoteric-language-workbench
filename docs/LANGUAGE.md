# Curly

The language as it is, for someone writing programs in it: every form
and builtin, in prose with examples, no tables, changed in the same
commit as the feature.

What the language is meant to become is in [`DESIGN.md`](DESIGN.md),
and [`SURFACE.md`](SURFACE.md) says, for each construct of Perl,
whether it will be in. Neither is a description of what works. This
is, and so far it is short: a program can do arithmetic on whole
numbers and print the answers.

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
    say(-7 % 3);

prints

    42
    14
    2

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

## Integers

An integer is a whole number from -9223372036854775808 to
9223372036854775807, which are -2^63 and 2^63 - 1.

One is written in decimal digits, from `0` to `9223372036854775807`.
Anything larger is refused: perl would carry on with a kind of number
the language doesn't have. There is no negative literal: `-5` is a
minus applied to `5`. So the smallest integer can't be written
directly, its digits being one past the largest; write
`-9223372036854775807 - 1`.

A number may not start with a zero unless it is `0` itself. perl reads
`010` as octal, 8, and `08` as a mistake; here both are refused until
octal is in.

No other way of writing a number is in yet: no `1_000`, no `0x10`, no
`1.5`, no `1e3`. Each is refused where it stands.

## Arithmetic

`+`, `-` and `*` add, subtract and multiply, and a `-` before an
expression negates it. The answer is exact, or the program stops:
when it would be past either end of the integers, that is a fault,
`integer overflow`. (perl would go on, with an unsigned integer or a
rounded one.)

    say 9223372036854775806 + 1;     # 9223372036854775807
    say 9223372036854775807 + 1;     # fault: integer overflow

`%` is the remainder, and it takes the sign of its right operand, as
perl's does and C's doesn't:

    say 7 % 3;       # 1
    say -7 % 3;      # 2
    say 7 % -3;      # -2
    say -7 % -3;     # -1

A remainder by zero is a fault, `modulus by zero`.

A `+` before an expression does nothing to it.

Operators group as in perl. A minus or plus sign before an expression
binds tightest; then `*` and `%`; then `+` and `-`. Operators of the
same level group from the left, so `2 - 3 - 4` is -5 and `2 * 7 % 3`
is 2. Brackets group as you'd expect.

    say 2 + 3 * 4;       # 14
    say (2 + 3) * 4;     # refused: see say
    say((2 + 3) * 4);    # 20
    say -2 * -3;         # 6
    say - -5;            # 5

Two minus signs with nothing between them, `--5`, are one thing to
perl, a decrement, and are refused; so are `++` and `**`, each until
its step. The operands of an operator are worked out from left to
right, so of two faults in one expression, the left one is the one
that happens.

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
