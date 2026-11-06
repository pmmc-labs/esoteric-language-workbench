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

An operation's operands are evaluated left to right, and the first fault
reached in that order is the program's. Within one operation the order is:
its operands, then the budget's charge (see Budgets), then the check that
its arguments are the right type, then its own checks (overflow, division
by zero, a bad shift count, a bad exponent). So `(+ #true (/ 1 0))` is a
division by zero, the right operand's fault reached before `+` looks at
its arguments, and `(+ (/ 1 0) (/ 1 0))` is the same fault from the left
one.

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

`(within n expr)` gives `expr`'s value, with a budget of `n` operations
for everything `expr` does. `n` is an integer literal of 0 or more, written
in the source; a negative number, a name, or any other expression as `n` is
a compile error, and so is a `within` without exactly two parts.

Each performed application of an operator (`+ - * / %`, `< <= > >=`, `==
!=`, `bit/and bit/or bit/xor bit/shl bit/shr`, `**`) and each performed `if`
costs one. Literals, `#true`, `#false` and `within` itself cost nothing,
and a branch of an `if` that is not taken costs nothing. A cost is one
whatever the work: `(** 1 4611686018427387903)` costs one, and a shift costs
one whatever its count. So `(within 2 (+ (* 2 3) 4))` is `10`, two
operations in a budget of two, and `(within 1 (+ (* 2 3) 4))` faults, the
`+` being the second. `(within 0 #true)` is `#true`, and `(within 1 (if
#true 1 (/ 1 0)))` is `1`: the `if` costs one and the division is not
performed.

An operation is charged after its operands and before its type checks and
its own checks, and the one that would take the count past the budget
faults `budget spent`. So `(within 0 (/ 1 0))` is `budget spent`, and
`(within 1 (/ 1 0))` is `division by zero`; `(within 1 (+ (/ 1 0) (+ 1
2)))` is a division by zero because the left operand is reached first,
while `(within 1 (+ (+ 1 2) (/ 1 0)))` is `budget spent`, the division
being the second operation.

An operation counts against every `within` around it, so a budget holds
everything inside it, including inner budgets: `(within 2 (within 5 e))`
holds `e` to two operations, and an inner `within` can lower the limit but
never raise it. Outside any `within` nothing is counted.

## Faults

A result that doesn't fit 63 bits, a division by zero, a shift count
out of range, a negative exponent, or a spent budget ends the program:
`fault: overflow`, `fault: division by zero`, `fault: bad shift`, `fault:
bad exponent` or `fault: budget spent` on stderr, and exit 1. Nothing is
printed on stdout. A value that is not the type an operation wants is
`fault: not an integer` or `fault: not a boolean`. Where a call could fault
two ways, the order is the one under Forms.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0.
