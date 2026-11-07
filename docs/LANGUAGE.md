# Strata

The language as it is, for someone writing programs in it. This file
describes the whole language as designed before the build; the Status
in `CLAUDE.md` and the progress line of [`PLAN.md`](PLAN.md) say which
steps have landed. A step that changes anything here changes this file
in the same commit.

A Strata program is a file of statements and function definitions. Its
one idea: **every variable is a history**. Writing to a variable lays a
new value on top of the old ones; the old ones stay, and `@` reads them.

```
let x = 1
x <- 2
x <- 3
print x        ; 3
print x@1      ; 2, x as it was one write ago
print #x       ; 3, the number of writes x has seen
```

## Lexical matters

Source is bytes. Spaces, tabs, carriage returns and newlines separate
tokens and are otherwise ignored; a statement may span lines and several
may share one. `;` starts a comment that runs to the end of the line.

Names are a letter or `_` followed by letters, digits and `_`. These are
keywords and can't be names: `fn let if else while return print write
and or not`. Integer literals are decimal digits, at most
9223372036854775807. String literals are in double quotes, on one line,
with the escapes `\n`, `\t`, `\"` and `\\`. Tokens are read longest
first, so `<-`, `<=`, `>=` and `!=` are always one token: `a<-1` is a
write, not `a < -1`. A `!` not followed by `=` is an unexpected
character.

Errors before running are reported as `error at L:C: message`, with the
1-based line and byte column, and the compiler exits 2. Only the first
is reported.

## Values

There are two kinds of atom: **numbers**, 64-bit signed integers, and
**strings**, immutable sequences of bytes.

A **history** is a stack of atoms, newest on top, possibly empty. It is
the only container: a list is a history. **Every expression evaluates
to a history.** A literal `7` is a history of one layer. An operator
takes the **top** of each operand and makes a new one-layer history. A
name evaluates to the variable's whole history. Reading the top of an
empty history is a fault, `empty history`.

Histories are never changed, only extended, so they are shared freely:
giving a history a second name, passing it to a function or returning it
copies nothing and can't affect anyone else's.

## Statements

### let

```
let name = expression
```

Declares `name` and gives it the whole history of the expression. So
`let y = x` gives `y` all of `x`'s past, and `let y = x + 0` gives `y`
one layer. A name can be declared once in a function (or in the main
program): declaring a name that is already visible, a parameter or an
earlier `let` in this or an enclosing block, is an error, `x is already
declared`. A `let` is visible from the statement after it to the end of
its block. A `let` in a loop body makes a fresh variable each time
round.

### <- (write)

```
name <- expression
```

Lays the top of the expression on the variable's history. The variable
must be declared (`unknown variable x`). There is no other way to change
a variable, and no way to remove or replace what it has held.

```
let total = 0
total <- total + 5
total <- total + 7
print total      ; 12
print total@2    ; 0
```

### print and write

```
print expression
write expression
```

Print the top of the expression: a number in decimal (with `-` if
negative), a string as its bytes. `print` adds a newline, `write`
doesn't.

### if

```
if condition { ... }
if condition { ... } else { ... }
if condition { ... } else if condition { ... } else { ... }
```

A condition is the top of its expression, which must be a number
(`expected a number, got a string`); zero is false, anything else true.

### while

```
while condition { ... }
```

Runs the block while the condition is true, testing before each round.
There is no `for`, `break` or `continue`.

### return

```
return expression
```

Ends the function, its result being the whole history of the
expression. Outside a function it's an error, `return outside a
function`. A function that ends without `return` returns the empty
history.

### Calls as statements

```
name(arguments)
```

Calls a function and discards its result. No other expression can stand
as a statement.

## Expressions

From loosest to tightest:

1. `a or b`
2. `a and b`
3. `not a`
4. `a = b`, `a != b`, `a < b`, `a <= b`, `a > b`, `a >= b`: at most one
   per level, so `a < b < c` is an error (`expected statement, found
   '<'`, at the second operator); write `a < b and b < c`.
5. `a + b`, `a - b`, left to right.
6. `a * b`, `a / b`, `a % b`, left to right.
7. `-a`, `#a`.
8. `a@k`, left to right.

Primaries: integer and string literals, names, calls `f(a, b)`, history
literals `[a, b, c]`, and `( expression )`.

`not` is a prefix form at its own level: `not a = b` is `not (a = b)`,
`not not a` is allowed, and `a and not b` is fine, but `1 + not 2` is a
parse error; write `1 + (not 2)`. A missing `)` is `expected ')', found
...`.

Operands are evaluated left to right, all of them, except that `and` and
`or` evaluate their right side only if needed.

### Arithmetic

`+ - * / %` on numbers, and prefix `-`. A result that doesn't fit in 64
bits is a fault, `integer overflow`. `/` truncates toward zero; `%` has
the sign of its left operand, so `-7 / 2` is `-3` and `-7 % 2` is `-1`.
Dividing by zero is a fault, `division by zero`; dividing the smallest
number by `-1`, with `/` or `%`, is `integer overflow`. An operand that
is a string is a fault, `expected a number, got a string`, except that
`+` on two strings concatenates them; `+` on a number and a string is a
fault, `mismatched types: number and string` (the kinds in operand
order).

### Comparisons

The six comparisons give 1 or 0. Two numbers compare as numbers; two
strings compare bytewise, a prefix before anything longer
(`"ab" < "abc"`). A number and a string is a fault, `mismatched types:
...` as for `+`.

### Logic

`and`, `or` and `not` take numbers and give 1 or 0. `a and b` doesn't
evaluate `b` if `a` is false; `a or b` doesn't if `a` is true.

### Depth: #

`#e` is the number of layers in `e`'s history: how many times a variable
has been written, counting its `let`'s layers.

### The past: @

`e@k` is `e` as it was `k` writes ago: its history with the top `k`
layers removed. `k` is a primary: a literal, a name, a call or a
parenthesised expression (`x@(i + 1)`). `e@0` is `e`; `e@(#e)` is the
empty history; any other `k` outside `0` to `#e` is a fault, `@ out of
range (index K, depth D)`.

Because `e@k` is a history, it's both an old value and a list:

```
let fib = [0, 1]
let n = 0
while n < 8 {
  fib <- fib + fib@1      ; the newest plus the one before it
  n <- n + 1
}
print fib                  ; 34

fn sum(xs) {
  if #xs = 0 { return 0 }
  return xs + sum(xs@1)    ; the top plus the sum of the rest
}
print sum([1, 2, 3, 4])    ; 10
```

### History literals

`[a, b, c]` is the history you'd get by writing `a`, then `b`, then `c`:
`c` is the top and `a` the oldest. Each element contributes its top.
`[]` is the empty history.

## Functions

```
fn name(param, param) {
  ...
}
```

Functions are defined at top level, before or after their use; they
can't nest. A call `name(a, b)` evaluates its arguments left to right
and binds each parameter to the whole history of its argument. A
function sees only its parameters and its own `let`s, not the main
program's. Writing to a parameter extends the function's own history;
the caller's variable is unchanged:

```
fn bump(x) {
  x <- x + 1
  return x
}
let a = 5
let b = bump(a)
print a      ; 5
print b      ; 6
print b@1    ; 5, b's history is a's, plus one layer
```

Calls nest at most 10000 deep; the call beyond that is a fault,
`recursion too deep`. Errors: `unknown function f`, `f is already
defined`, `f is a builtin` (defining `len`, `at` or `str`), `f takes N
arguments, given M`.

## Builtins

`len(s)` is the number of bytes in the string `s`.

`at(s, i)` is the one-byte string at position `i` of `s`, counting from
0. Outside `0` to `len(s) - 1` it's a fault, `index out of range (index
I, length N)`.

`str(n)` is the decimal string of the number `n`.

`len` and `at`'s first argument must be strings (`expected a string, got
a number`); `at`'s index and `str`'s argument must be numbers.

## Programs

The program's statements run top to bottom. It prints only through
`print` and `write`, and reads nothing: no input, arguments, clock or
randomness. It exits 0 when the last statement finishes.

A **fault** stops the program: what was printed so far is flushed, then
`fault at L:C: message` goes to stderr and the exit code is 1. `L:C` is
where the failing operation is written: the operator, the keyword
(`print`, `if`, ...), the `<-`, the `[` of a history literal, or the
name of a builtin or of the call that went too deep. The faults are:
`empty history`, `@ out of range (index K, depth D)`, `integer
overflow`, `division by zero`, `expected a number, got a string`,
`expected a string, got a number`, `mismatched types: A and B`, `index
out of range (index I, length N)`, `recursion too deep`, and `out of
memory` (printed as `fault: out of memory`, with no position).

Memory is never freed.
