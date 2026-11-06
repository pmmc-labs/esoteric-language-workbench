# lang

The calculator as it is, for someone writing programs in it. (In a
language started from this template, this page is the language: every
form and builtin, in prose with examples, no tables, changed in the same
commit as the feature.)

## Values

An integer: 63 bits, from -4611686018427387904 to 4611686018427387903.
Written in decimal, with a `-` for a negative. A literal past the range
is a compile error.

## Forms

A program is one integer. `;` starts a comment, to the end of the line.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0. A fault ends the program with its message on stderr and exit 1;
nothing faults yet.
