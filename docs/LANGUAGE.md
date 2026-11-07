# lang

The calculator as it is, for someone writing programs in it. (In a
language started from this template, this page is the language: every
form and builtin, in prose with examples, no tables, changed in the same
commit as the feature.)

## Values

An integer: 63 bits, from -4611686018427387904 to 4611686018427387903.
Written in decimal, with a `-` for a negative. A literal past the range
is an error before the program runs.

A boolean, `#true` or `#false`, and a string, in double quotes, are the
other two kinds of value; both are below.

## Forms

A program is one expression. An expression is a value written out, an
integer, a boolean or a string, or an operator applied to its operands:

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
Arithmetic, an ordering or a bit operation on a boolean or a string
faults `not an integer`.

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

## Strings

A string is written in double quotes: `"hello"`, and `""` is the empty
one. A string is a sequence of characters, and a character is a Unicode
code point. Its length, its indexes and its order are its code points',
never the bytes or the UTF-16 units of its encoding, so `(str/len "😀")`
is `1`, and `(str/len "e\u{301}")` is `2`: the accent is a character of
its own. Nothing is normalised, so `"é"` and `"e\u{301}"` are different
strings, and `(== "é" "e\u{301}")` is `#false`.

In a literal, `\"` is a quote, `\\` a backslash, `\n` a line feed and
`\t` a tab. `\u{X}` is the code point X, written in hex with one to six
digits: `\u{41}` is `A` and `\u{1F600}` is `😀`. A tab or a carriage
return written raw stands for itself, and any other character stands for
itself too. These are errors before the program runs: a backslash before
anything else; a `\u{X}` that is empty, has more than six digits, isn't
hex, is a surrogate (D800 to DFFF) or is past 10FFFF; a line feed written
raw, which is `\n`'s job; and a string with no closing quote. A quote
ends a name or a number, so `(str/len"a")` is `(str/len "a")`. The file
is UTF-8, and one that isn't is an error before the program runs.

A string prints in double quotes, so that what prints reads back as the
same string. A `"` and a `\` have a backslash before them, a line feed is
`\n` and a tab is `\t`, and any other character below U+0020, and U+007F,
is `\u{X}` in lowercase hex. Everything else prints as itself, in UTF-8.
So `(str/char 7)` prints `"\u{7}"`, and `"é"` prints `"é"`.

Six operators take strings (`str/len`, `str/code` and `str/char` take
one operand, the others two; a different count is an error before the
program runs):

- `(str/len s)` is the number of characters of `s`.
- `(str/at s i)` is the character at index `i`, counted from 0, as a
  string of one. An index below 0 or at or past the length faults
  `bad index`.
- `(str/cat a b)` is `a` followed by `b`.
- `(str/lt a b)` is `#true` when `a` sorts before `b`. It compares
  character by character, by code point, and a string sorts before any
  longer string that begins with it: `(str/lt "\u{FFFF}" "\u{10000}")` is
  `#true`, and `(str/lt "ab" "a")` is `#false`.
- `(str/code s)` is the code point of a string of one character, as an
  integer, and faults `not a character` for any other length.
- `(str/char n)` is the string of one character with code point `n`. An
  integer that isn't a code point, a negative one, a surrogate or one past
  10FFFF, faults `not a character`.

`==` and `!=` compare two strings by their characters, and compare a
string with any other value as unequal. The other operators don't take a
string: an arithmetic operator, an ordering or a bit operation given one
faults `not an integer`. A string operator given something that isn't a
string faults `not a string`, and one given something that isn't an
integer where it wants one faults `not an integer`. Operands are checked
left to right, each for its type, and then the index or code point for
its range, so `(str/at 5 #true)` faults `not a string` and
`(str/at "ab" 7)` faults `bad index`.

## Budgets

`(within n expr)` is the value of `expr`, of whatever type, evaluated
with a budget of `n` operations. An operation is one application of an
operator, any of them, the string operators too: `(** 1 4611686018427387903)` is one,
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
out of range, a negative exponent, an operation past the budget, a
negative budget, a string index out of range, or a string operator given
a value that isn't a string or a character, ends the program:
`fault: overflow`, `fault: division by zero`, `fault: bad shift`,
`fault: bad exponent`, `fault: budget spent`, `fault: bad budget`,
`fault: bad index`, `fault: not a string` or `fault: not a character` on
stderr, and exit 1. Nothing is printed on stdout.

## Programs

The program's value is printed, followed by a newline, and the program
exits 0.
