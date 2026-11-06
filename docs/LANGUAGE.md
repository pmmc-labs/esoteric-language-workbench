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

A program is one form: an integer, or an operation. `;` starts a
comment, to the end of the line.

An operation is a list of an operator and exactly two operands,
`(op a b)`, where `op` is one of `+ - * / %` and each operand is an
integer or another operation. So `(+ 1 2)` is 3, and `(- (* 6 7) (+ 1
4))` is 37. There are no operations of one operand or of three: negation
is `(- 0 x)`, and a negative number is already an integer, `-5`. An
integer is an optional `-` and decimal digits; `+5` is not one.

`+`, `-` and `*` give the exact result of the sum, difference or
product. `/` and `%` divide and truncate toward zero, and `%` takes the
sign of the dividend, so `(/ -7 2)` is -3 and `(% -7 2)` is -1, `(/ 7
-2)` is -3 and `(% 7 -2)` is 1, and `(/ -7 -2)` is 3 and `(% -7 -2)` is
-1. For any `a` and `b`, `a` is `b * (a / b) + a % b`.

Operands are evaluated left to right, and the first fault ends the
program, so `(+ (/ 1 0) (+ 4611686018427387903 1))` is a division by
zero and the same with its operands swapped is an overflow.

A malformed program is a compile error, reported at the form at fault;
the whole program is checked before anything runs, so one with an error
anywhere in it never runs. The messages are `empty list` for `()`,
`expected an operator` where the first item of a list isn't a symbol,
`unknown operator max` for a symbol that isn't one of the five,
`- takes 2 operands` for an operator with another number of operands,
`unexpected symbol x` for a symbol where an operand or the program goes,
and `integer out of range` for a literal past the range. A list's shape
and operator are checked before its operands, and the operands left to
right; the first error is the only one reported.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0. A fault ends the program with its message on stderr and exit 1.

There are two faults. `integer overflow` is any operation whose exact
result is outside the range of an integer, an intermediate one
included: `(* (+ 4611686018427387903 1) 0)` faults though the whole
would be 0. The range is 63 bits, so `(* 2147483648 2147483648)`, which
is 2^62, faults, and so does `(* 4294967296 4294967296)`, which a 64-bit
machine would wrap to 0; `(/ -4611686018427387904 -1)` faults, and `(%
-4611686018427387904 -1)` is 0 and doesn't. `division by zero` is `/` or
`%` with a divisor of 0. A fault happens when the program runs, even in
an expression of constants, so `(/ 1 0)` compiles, and its message says
what went wrong but not where.
