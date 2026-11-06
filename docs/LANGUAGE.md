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
Arithmetic, an ordering or a bit operation on a boolean faults.

## Bit operations

`bit/and`, `bit/or` and `bit/xor` on two integers, as two's complement
of any width agrees: `(bit/and -1 7)` is `7`. `(bit/shl a n)` is `a`
times 2^n and faults `overflow` when the result doesn't fit; `(bit/shr
a n)` is `a` divided by 2^n rounded toward negative infinity, so
`(bit/shr -7 1)` is `-4`. A count outside 0 to 62 faults `bad shift`.

## Exponentiation

`(** a b)` is `a` to the power `b`, both integers: `(** 2 10)` is
`1024`, `(** -3 3)` is `-27`, and `(** a 0)` is `1` for every `a`,
`(** 0 0)` too. A negative exponent faults `bad exponent`, even where
the answer would fit (`(** 1 -1)`), and a result past the range faults
`overflow`. `(** 1 4611686018427387903)` is `1` without taking long.

## Budgets

`(within n expr)` gives the value of `expr`, run with a budget of `n`
operations. An operation is one application of an operator, any of the
seventeen, however large its arguments (`(** 1 4611686018427387903)` is
one); integers, booleans, `if` and `within` itself cost nothing, so an
`if` costs its test and the branch it takes. A budget of `n` allows `n`
operations, and the next one faults `out of budget`; nothing catches it.
`(within 4 (+ (* 6 7) (- 10 (/ 7 2))))` is `49`, its four operators being
the whole budget, and with 3 it faults.

An operation is paid for after its arguments have run and before it
looks at them, so `(within 0 (/ 1 0))` is `out of budget`, the budget
having refused the division before it could fault, and `(within 1 (/ 1
0))` is `division by zero`.

`n` is any expression that gives an integer, run first and outside the
budget it sets, so its operators are paid from the budgets around it. A
negative `n` faults `bad budget`; 0 is a budget that allows nothing.
Budgets nest by the smallest: every operation is charged to every
`within` around it, so `(within 2 (within 100 e))` allows `e` two
operations, and what an inner `within` spent is still spent when it ends.
Two `within`s side by side have a budget each.

## Faults

A result that doesn't fit 63 bits, a division by zero, a shift count
out of range, a negative exponent, a spent budget, or a negative budget
ends the program: `fault: overflow`, `fault: division by zero`, `fault:
bad shift`, `fault: bad exponent`, `fault: out of budget` or `fault: bad
budget` on stderr, and exit 1. Nothing is printed on stdout.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0.
