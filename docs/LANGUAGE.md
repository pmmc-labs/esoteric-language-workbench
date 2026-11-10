# SMOL

The language as it is, for someone writing programs in it. Each form is
added here in the same commit that adds it.

## Values

An integer, of any size, written in decimal with a `-` directly before the
digits for a negative. A string, in double quotes; it can't contain a `"`,
and it has no escapes yet. The constants `nil`, `true` and `false`. A
function, which prints as `<function>`.

## Names

A name is a letter or `_`, then letters, digits and `_`. It may begin with
a sigil, `$`, `@` or `%`, which is part of the name: `$a` and `@a` are two
different names. `let`, `function`, `nil`, `true` and `false` are keywords
and aren't names.

## Programs

A program is statements separated by `;`, and the last may end with one.
An empty program does nothing. `//` starts a comment, which runs to the end
of the line.

## Statements

`let NAME = EXPR` binds the name for the statements after it. A later
`let` of the same name hides the earlier binding.

Any other statement is an expression.

## Expressions

A name is its value. A constant is its value.

`function (PARAMS) { BODY }` is a function. PARAMS is a list of names,
separated by commas, that are distinct; it may be empty. BODY is statements,
as in a program, and it may be empty. The function's value is the value of
the last statement of its body, if that statement is an expression. A body
with no such statement gives `nil`. A function sees the names bound where it
is written, and not the names bound after it. A parameter is an ordinary
name, so `self` is one too until methods exist.

`f(a, b)` calls `f`. The arguments are evaluated first, from left to right.
`f` must be a function, and the call must give as many arguments as `f` has
parameters.

`x.name(a, b)` calls the method `name` on `x`. No value has methods yet.

`catch(f)` is a built-in function, bound before the program starts, so a
`let` can shadow it. It calls `f` with no arguments. If that call raises a
fault, `catch` returns the fault's message as a string; otherwise it returns
`nil`. A fault in the argument itself, such as a value that isn't a function,
is not caught. `catch` takes exactly one argument.

A parameter that collects the remaining arguments into a Hash, written
`%name`, waits for Hash (step 3).

## Output

The program prints the value of its last statement, if that statement is an
expression, and then a newline. Integers print in decimal, strings in double
quotes, functions as `<function>`, and the constants as `nil`, `true` and
`false`. A program whose last statement is a `let` prints nothing. The
program then exits 0.

## Faults

A syntax error is reported as `FILE:LINE:COLUMN: MESSAGE` on stderr, and the
program exits 1. A fault is `fault: MESSAGE` on stderr, and the program exits
1; anything printed before it is kept. The faults so far are an unbound name,
a call of something that isn't a function, a call with the wrong number of
arguments, and a method call, since no value has methods yet. A fault that
`catch` takes is not a fault of the program: the program carries on after the
call to `catch`.
