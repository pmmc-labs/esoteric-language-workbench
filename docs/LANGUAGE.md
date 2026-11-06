# lang

The calculator as it is, for someone writing programs in it. (In a
language started from this template, this page is the language: every
form and builtin, in prose with examples, no tables, changed in the same
commit as the feature.)

## Values

An integer: 63 bits, from -4611686018427387904 to 4611686018427387903.
Written in decimal, with a `-` for a negative. A literal past the range
is a compile error. A `+` doesn't start a literal: `+5` is a symbol, and
a symbol isn't a value, so it's a compile error too.

## Forms

A program is one expression: an integer, or a form. `;` starts a
comment, to the end of the line.

A form is an operator and two operands in parentheses, `(op a b)`. The
operators are `+`, `-`, `*` and `/`, and an operand is an integer or
another form:

    (+ 2 3)                 ; 5
    (- 2 7)                 ; -5
    (* (+ 1 2) (- 10 4))    ; 18

Each operator takes exactly two operands. There's no `(+ 1 2 3)`: write
`(+ (+ 1 2) 3)`. There's no one-operand `-` either: a negative literal
is `-5`, and a form is negated by taking it from 0, `(- 0 (* 2 3))`.

`/` truncates toward zero, so `(/ -7 2)` and `(/ 7 -2)` are both -3, and
`(/ 7 2)` is 3. There's no remainder operator.

These are compile errors, and the program doesn't run:

- `+ takes two operands`, for `(+ 1)` or `(+ 1 2 3)`, at the form's `(`.
  The message names the operator.
- `unknown operator: foo`, for `(foo 1 2)`, at the `(`.
- `a form must start with an operator`, for `()` or `(1 2)`, at the `(`.
- `a symbol is not a value: x`, for a symbol where a value goes, as in
  `x` or `(+ 1 x)`, at the symbol.
- `integer out of range`, for a literal past 63 bits, at the literal.

The whole program is checked before it runs, and the first error from
the left is the one reported. So `(+ (/ 1 0) 4611686018427387904)` is a
compile error, not a division by zero.

## Faults

A fault happens as the program runs. Nothing is worked out at compile
time, so `(/ 1 0)` compiles, and faults when it runs.

- `fault: integer overflow`: an operator's result is outside the 63-bit
  range. `(+ 4611686018427387903 1)` faults, and so does
  `(* 4294967296 4294967296)`, whose value, 2^64, is far past the range,
  though a 64-bit machine would wrap it to 0. `(/ -4611686018427387904 -1)`
  is an overflow too: its value, 2^62, is one past the largest integer.
- `fault: division by zero`: the divisor of `/` is 0.

Operands are worked out left to right, the left one first, and then the
operator. The first fault in that order is the one reported:

    (+ (/ 1 0) (+ 4611686018427387903 1))   ; division by zero, the left one
    (+ (+ 4611686018427387903 1) (/ 1 0))   ; integer overflow, the left one
    (+ 4611686018427387903 (/ 1 0))         ; division by zero: the right
                                            ; operand faults before the + can

## Programs

The program's value is printed, followed by a newline, and the program
exits 0. A fault ends the program with its message on stderr and exit 1.
