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

Evaluation is left to right: an operator's left operand completely, then
its right, then the operator; an `if`'s test, then one branch; a
`within`'s budget, then its body. The first fault in that order ends the
program, so `(+ (/ 1 0) (+ #true 1))` faults `division by zero`.

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

`(within n expr)` is the value of `expr`, of whatever type, evaluated
with a budget of `n` operations. An operation is one application of an
operator, any of the seventeen: `(** 1 4611686018427387903)` is one,
however large the exponent. Literals, `if` and `within` cost nothing,
and a branch of an `if` that isn't taken isn't evaluated, so costs
nothing. Operations are counted as they run, and an operator is charged
after its operands have been evaluated and before it checks anything:

    (within 3 (+ (* 2 3) (- 10 4)))    ; 12, three operations
    (within 2 (+ (* 2 3) (- 10 4)))    ; fault: budget spent
    (within 1 (+ (/ 1 0) 2))           ; fault: division by zero
    (within 0 (/ 1 0))                 ; fault: budget spent

A budget of `n` allows `n` operations; the one that would be the next
faults `budget spent` instead of running. Nothing catches it. A
budget of 0 allows an expression with no operations: `(within 0 42)`.

Budgets nest, and every budget in force applies: an operation is
charged to all of them, so an inner `within` can't give more than the
outer has left. `(within 1 (within 5 (+ (+ 1 2) 3)))` faults, and so
does `(within 5 (within 1 (+ (+ 1 2) 3)))`. When an inner `within`
ends, what it didn't use is dropped and the outer has paid for what it
did: `(within 3 (+ (within 5 (+ (+ 1 2) 3)) 4))` is `10`, and with 2
outside it faults. Outside every `within` nothing is counted.

The budget is any expression, evaluated first and not under the budget
it sets: its operations are charged to the budgets around the `within`.
`(within 2 (within (+ 1 1) (* 3 4)))` is `12`, and with 1 outside it
faults. The budget must be an integer, else `not an integer`, and not
negative, else `bad budget`, either before the body runs:
`(within -1 (/ 1 0))` faults `bad budget`.

## Faults

A result that doesn't fit 63 bits, a division by zero, a shift count
out of range, a negative exponent, an operation past the budget, or a
negative budget ends the program: `fault: overflow`, `fault: division
by zero`, `fault: bad shift`, `fault: bad exponent`, `fault: budget
spent` or `fault: bad budget` on stderr, and exit 1. Nothing is printed
on stdout.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0.
