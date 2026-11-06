# lang

The calculator as it is, for someone writing programs in it. (In a
language started from this template, this page is the language: every
form and builtin, in prose with examples, no tables, changed in the same
commit as the feature.)

## Values

An integer: 63 bits, from -4611686018427387904 to 4611686018427387903.
Written as an optional `-` and then one or more of the digits `0` to
`9`, and nothing else: `42`, `-7`, `007` (which is 7) and `-0` (which is
0) are integers. `+5`, `1_0`, `1.5`, `0x10`, `--1` and `-` alone are not
integers; they are symbols, and a symbol is not a value, so they are
compile errors where a value is wanted. A literal past the range is a
compile error.

Spaces, newlines, tabs and carriage returns are the only whitespace;
any other character, a no-break space say, is part of the integer or
symbol it touches.

## Forms

A program is one form: an integer, or a call. `;` starts a comment, to
the end of the line.

A call is `(op a b)`: an operator and exactly two operands, each an
integer or another call, nested as deep as you like. There are five
operators, and each one is checked as it runs (see Programs).

`(+ a b)` is the sum: `(+ 40 2)` is 42.

`(- a b)` is the first operand less the second: `(- 3 10)` is -7. There
is no one-operand `-`; to negate, subtract from zero, `(- 0 x)`.

`(* a b)` is the product: `(* -6 7)` is -42.

`(/ a b)` is the quotient, truncated toward zero: `(/ -7 2)` is -3 and
`(/ 7 -2)` is -3.

`(% a b)` is the remainder, which takes the sign of the first operand,
so that `a` is always `(/ a b)` times `b`, plus `(% a b)`: `(% -7 2)` is
-1 and `(% 7 -2)` is 1.

Both operands are always evaluated, left to right, before the operation,
and nothing is skipped or worked out ahead of time: `(* 0 (/ 1 0))` is a
division by zero, not 0.

`(- (* 3 (+ 4 5)) (/ 100 (% 17 5)))` is -23.

A malformed call is a compile error that names its place in the source:
`()` is an `empty form`; a head that is not a symbol, `(1 2)`, is
`expected an operator`; a head that is a symbol but not one of the five,
`(foo 1 2)`, is `unknown operator 'foo'`; any other count of operands,
`(+ 1)`, is `'+' takes 2 arguments, got 1`; and a symbol on its own, as
the program or as an operand, is `can't compile symbol yet`. An operator
is not a value. The whole program is checked before it runs, so a
malformed call after a faulting one is still only the compile error.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0. A fault ends the program with its message on stderr and exit 1.
There are two.

`fault: integer overflow` is any operation whose exact result is outside
the range. Nothing wraps, saturates or grows, and each operation is
checked on its own result, so `(- (+ 4611686018427387903 1) 1)` faults
though the answer would fit. A result of exactly the largest or the
smallest integer is fine: `(+ 4611686018427387902 1)` prints
4611686018427387903 and `(* -2147483648 2147483648)` prints
-4611686018427387904, but `(+ 4611686018427387903 1)` is the fault, and
so are `(- 0 -4611686018427387904)` and `(/ -4611686018427387904 -1)`,
whose results are 2^62. Only `+ - *` and `/` can leave the range;
`(% -4611686018427387904 -1)` is 0.

`fault: division by zero` is a zero second operand to `/` or `%`:
`(/ 1 0)` and `(% 1 0)`.

When two things would fault, the one that happens first is reported, and
operands happen left to right: `(+ (/ 1 0) (* 4611686018427387903
4611686018427387903))` is a division by zero, and with the operands the
other way round it is an integer overflow.
