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

A program is one expression. An expression is an integer, or an
operator applied to two expressions:

    (+ (* 6 7) (- 10 (/ 7 2)))

`+`, `-`, `*`, `/` and `%` take exactly two arguments each. `/` divides
and truncates toward zero, and `%` is the remainder, with the dividend's
sign: `(/ -7 2)` is `-3` and `(% -7 2)` is `-1`.

`;` starts a comment, to the end of the line.

## Booleans, comparisons and `if`

`#true` and `#false` are booleans, and print as written. `<`, `<=`, `>`
and `>=` compare two integers and give a boolean; `==` and `!=` compare
any two values, and two values of different types are never equal, so
`(== #false 0)` is `#false`. All six take exactly two arguments.

`(if test then else)` has exactly three parts. It gives `then` when
`test` is `#true` and `else` when it's `#false`, and evaluates only the
one it gives. A test that isn't a boolean faults, so `(if 0 1 2)` is a
fault, not a truthy choice.

Arithmetic, or an ordering, on a boolean faults: `(+ 1 #true)` is a
fault.

## Faults

A result that doesn't fit 63 bits, or a division by zero, ends the
program: `fault: overflow` or `fault: division by zero` on stderr, and
exit 1. Nothing is printed on stdout. A boolean where an integer is
wanted ends it with `fault: not an integer`, and a non-boolean test of
an `if` with `fault: not a boolean`.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0.
