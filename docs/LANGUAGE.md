# Curly

The language as it is, for someone writing programs in it: every form
and builtin, in prose with examples, no tables, changed in the same
commit as the feature.

What the language is meant to become is in [`DESIGN.md`](DESIGN.md),
and [`SURFACE.md`](SURFACE.md) says, for each construct of Perl,
whether it will be in. Neither is a description of what works. This
is, and so far it is short: a program can print whole numbers.

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
left out, and it must be `v5.42` exactly. It appears once.

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

One comment is refused: a first line that starts `#!`. perl reads
switches from that line (`#!/usr/bin/perl -n` wraps the whole program
in a loop over its input), and the language has no switches. A `#!`
anywhere but the first line is an ordinary comment.

## Statements

Every statement ends with a semicolon, the last one too, and there is
no empty statement: `;;` is refused.

## say

`say` prints an integer and a newline.

    use v5.42;
    say 42;
    say 0;
    say 9223372036854775807;

prints

    42
    0
    9223372036854775807

That is the only statement there is yet, and it takes exactly one
integer, written without brackets: `say(42);` waits for the next step.

## Integers

An integer is written in decimal digits, from `0` to
`9223372036854775807`, which is 2^63 - 1, the largest there is.
Anything larger is refused: perl would carry on with a kind of number
the language doesn't have.

A number may not start with a zero unless it is `0` itself. perl reads
`010` as octal, 8, and `08` as a mistake; here both are refused until
octal is in.

No other way of writing a number is in yet: no minus sign, no `1_000`,
no `0x10`, no `1.5`, no `1e3`. Each is refused where it stands.

## When a program stops

A program that reaches its end exits with status 0, having printed
what it printed.

Nothing in the language can fail at run time yet. When something can,
the program will stop there with a **fault**: whatever it had printed,
then one line on stderr, `fault: MESSAGE at FILE line N.`, and exit
status 1. A fault can't be caught.
