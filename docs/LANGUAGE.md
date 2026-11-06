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

`#true` and `#false`. `<`, `<=`, `>` and `>=` compare two integers and
give a boolean; `==` and `!=` compare any two values. `(if test then
else)` gives `then` when `test` is `#true` and `else` when it's
`#false`, evaluating only that one; anything else as the test faults.
Arithmetic, an ordering, a bit operation or `**` on a boolean faults.

## Bit operations

`bit/and`, `bit/or` and `bit/xor` on two integers, as two's complement
of any width agrees: `(bit/and -1 7)` is `7`. `(bit/shl a n)` is `a`
times 2^n and faults `overflow` when the result doesn't fit; `(bit/shr
a n)` is `a` divided by 2^n rounded toward negative infinity, so
`(bit/shr -7 1)` is `-4`. A count outside 0 to 62 faults `bad shift`.

## Exponentiation

`(** a b)` is `a` to the power `b`, on two integers: `(** 2 10)` is `1024`,
`(** -3 3)` is `-27`, and `(** 0 0)` is `1`. A negative exponent faults
`bad exponent`, and a result that doesn't fit 63 bits faults `overflow`,
as `(** 2 62)` does.

## Faults

A result that doesn't fit 63 bits, a division by zero, a shift count out
of range, or a negative exponent ends the program: `fault: overflow`,
`fault: division by zero`, `fault: bad shift` or `fault: bad exponent` on
stderr, and exit 1. Nothing is printed on stdout.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0.
