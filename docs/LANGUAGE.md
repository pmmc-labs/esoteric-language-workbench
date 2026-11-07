# Ditto

Ditto is a small language for everyday programs, in a syntax a
TypeScript, Python or Go programmer can read on sight. It has one rule
that sets it apart: **every value is a value**. Assigning a list or a
map, passing it to a function, or storing it in another one gives a
copy, as numbers and strings already do everywhere. Nothing you hold
changes because someone else changed theirs. Its second idea is small:
`a else b`, which gives `b` when a lookup written in `a` finds nothing.

This document is the language as designed, every form and builtin, with
the exact message and position of every error and fault. It was written
before the compiler; each section says which plan step builds it
(`PLAN.md`). Until that step lands, the section is the spec.

## Programs

A program is one file, `name.ditto`, of UTF-8 or plain ASCII text. It
holds top-level statements and function definitions, in any order. The
statements run from top to bottom; functions are defined before anything
runs, so a function can be called above the place it's written.

```
print("hello, world")
```

A program ends when its last top-level statement has run, with exit
status 0. A **fault** (a runtime error) ends it at once with exit status
1, after printing one line on standard error:

```
examples/bank.ditto:12:21: fault: missing key "dave"
```

The path is the one the compiler was given, then the line and the column
(both from 1, columns in bytes) of the place the fault points at; each
form below says which place that is. Everything the program printed
before the fault comes out first.

A **compile error** stops the compiler before anything runs, with exit
status 2 and one line on standard error, in the same shape:

```
t/301-arity.ditto:4:3: error: add takes 2 arguments, got 3
```

Only the first error is reported. (Step 0, D28, D29.)

## Lexical structure

`//` starts a comment that runs to the end of the line. Spaces, tabs and
carriage returns separate tokens. Any other byte outside a string or
comment that isn't part of a token is the compile error
`unexpected character 'c'`, or `unexpected byte 0xNN` (two upper-case
hex digits) if it isn't printable ASCII, pointing at it.

A **newline** ends a statement, except where the statement can't have
ended: inside `( )` or `[ ]`, inside a map literal's `{ }`, and after a
binary operator, `else`, a comma, `=` or a compound assignment. `;` also
ends a statement, so `{ let t = a; a = b; b = t }` fits on one line. A
`}` ends the statement before it.

**Names** are ASCII letters, digits and `_`, not starting with a digit.
These are keywords and can't be names: `and break continue else false fn
for if in let nil not or return true while`.

**Integers** are decimal digits, with `_` allowed between digits
(`1_000_000`); leading zeros are allowed and mean nothing (`007` is 7).
A literal that starts with a digit and goes on with a
letter or `_` in the wrong place (`12ab`, `1_`, `1__0`) is
`malformed number`; one above 9223372036854775807 is
`integer literal too large`. Both point at the literal's first byte.
There is no negative literal: `-5` is unary minus applied to `5`, so the
smallest int is written `-9223372036854775807 - 1`.

**Strings** are in double quotes, on one line. The escapes are `\n`,
`\t`, `\r`, `\\`, `\"`, `\{` and `\}`; any other is
`unknown escape '\q'` at the backslash. A newline or end of file before
the closing quote is `unterminated string`, at the opening quote. Bytes
other than these pass through as they are, so a string can hold UTF-8;
that includes a bare `}`, which only means something inside an
interpolation. A backslash at the end of a line is `unterminated string`.

Inside a string, `{expr}` is **interpolation**: the expression is
evaluated and its printed form (as `str` gives it) put in its place.
The expression can be anything, including strings and nested
interpolation: `"total: {len(xs)} items, first {xs[0]}"`. `{}` with
nothing in it is `empty interpolation`, at the `{`; an interpolation that
reaches the end of the line (even inside a string written in it) is
`unterminated interpolation`, at the `{` (D35).
Parts are evaluated left to right. (Step 4, D15.)

## Values

There are six types, named as faults name them:

- `int`: a 64-bit signed integer. Arithmetic that would leave the range
  faults; it never wraps.
- `string`: an immutable sequence of bytes.
- `bool`: `true` or `false`.
- `nil`: the one value `nil`, which a function returns when it returns
  nothing.
- `list`: an ordered sequence of values, `[1, "two", [3]]`.
- `map`: keys to values, keys being ints or strings, kept in the order
  the keys were first added. `{name: "pen", qty: 3}`. A map is also how
  Ditto spells a record.

There are no floats and no first-class functions. (D10, D14, D16.)

### Every value is a value (the core rule)

Lists and maps behave like ints. `let b = a` gives `b` its own value;
changing `b` afterwards never changes `a`. A function gets its own copy
of each argument, and can change it freely; the caller's is untouched,
and the only way a function affects its caller is by returning a value.
Putting a list into a map puts in its value at that moment.

```
let a = [1, 2, 3]
let b = a
b[0] = 99
print(a, b)          // [1, 2, 3] [99, 2, 3]
```

It follows that a value can never contain itself, so printing and
comparing always end; that a loop over a list sees the list as it was
when the loop started; and that a function can't be given anything to
change behind the caller's back. Under the hood, values are never
changed in place: an update builds a new value (sharing what it can) and
stores it in the variable. That makes updating an element cost a copy of
the list or map it's in, which is fine at the size Ditto is for (D4,
D7).

## Variables

`let name = expr` declares a variable in the current block and gives it
a value. Every variable is declared before use; there's no declaration
without a value (`let x = nil` if there's nothing yet).

- Reading or assigning a name that isn't declared in an enclosing block
  of the same function (or of the top level) is `unknown variable x`, at
  the name.
- Inside a function, a name that is only a top-level variable is
  `x is a top-level variable; functions see only their parameters and their own variables`.
- A name that is a function, used as a value, is
  `functions are not values`.
- Declaring a name that is already declared in this block or any
  enclosing one is `x is already declared`, at the new name. There's no
  shadowing; two sibling blocks can each have their own `x`.
- The new variable is in scope after its `let`, so `let x = x + 1` with
  no earlier `x` is `unknown variable x`.
- A loop variable belongs to the loop's block: `let` of the same name in
  the body is `x is already declared`, and the name is free again after
  the loop.

(Step 2, D12, D13.)

### Assignment

```
x = expr
xs[i] = expr
accounts[name].balance = expr
counts[w] += 1
```

The target is a variable followed by any number of `[index]` and
`.field` steps. Anything else on the left of `=` (`f(x) = 1`, `1 = 2`)
is `cannot assign to this`, at the target's first token.

`x = e` evaluates `e` and stores it in `x`. A target with steps updates
the value inside the variable and stores the whole new value back:

1. the index expressions, left to right;
2. the right-hand side;
3. the path: each step but the last is looked up as in an expression,
   and faults as one would;
4. the last step is set: a list index must be in range (setting doesn't
   grow a list; `xs += [v]` does); a map key is replaced in place if
   present, added at the end if not.

Setting a step on something that isn't a list or a map faults:
`cannot assign into string` (or whichever type) at the step's `[` or
`.`. The compound assignments `+= -= *= /= %=` do the same, except that
after step 1 the current value at the full path is read (faulting as a
lookup would), then the right-hand side is evaluated, then the operator
is applied as in an expression, with its faults pointing at the `+=`.

## Expressions

Evaluation is left to right throughout: operands, arguments, list and
map elements, interpolation parts.

From loosest to tightest:

1. `or`
2. `and`
3. `not` (prefix)
4. `==` `!=` `<` `<=` `>` `>=` `in` `not in`, which don't chain:
   `a < b < c` is `comparisons do not chain`, at the second operator
5. `+` `-`
6. `*` `/` `%`
7. `else`
8. `-` (prefix)
9. calls `f(...)`, indexing `x[i]`, fields `x.name`
10. literals, names, `( expr )`

Binary operators at levels 1, 2, 5, 6 and 7 associate to the left.

### Literals

`42`, `"text"`, `true`, `false`, `nil`, lists `[a, b, c]`, maps
`{key: value, ...}`. Lists and maps may break across lines and may end
with a comma.

A map key is a name (meaning that string: `{qty: 3}` is
`{"qty": 3}`), a string literal without interpolation, or an int
literal, optionally with a leading `-`. Anything else is
`map key must be a name, a string or an int`, at the key. The same key
twice in one literal is `duplicate key "qty"` (or `duplicate key 3`), at
the second. `{}` is the empty map.

### Arithmetic

`+ - * / %` take ints. `/` truncates toward zero and `%` takes the sign
of its left operand, as in C, Go and TypeScript, so
`-7 / 2 == -3` and `-7 % 2 == -1`. Faults, each at the operator:

- `integer overflow`, when the result doesn't fit; this includes
  `-x` for the smallest int and `(-9223372036854775807 - 1) / -1`.
  (`(-9223372036854775807 - 1) % -1` is `0`.)
- `division by zero`, for `/` and `%`.
- `cannot use - on string and int` (with the operator and the two
  types), when an operand isn't an int; for prefix minus,
  `cannot use - on string`.

`+` also joins two strings or two lists: `"ab" + "c"`, `[1] + [2, 3]`.
Any other pair is `cannot use + on string and int`. To put a number in a
string, interpolate it: `"n = {n}"`.

### Comparison

`==` and `!=` take any two values and never fault. Values of different
types are never equal. Lists are equal when they have equal elements in
the same order; maps when they have the same keys with equal values,
whatever their order.

`< <= > >=` compare two ints, two strings (byte by byte; a prefix comes
first), or two lists (element by element with these same rules; a
prefix comes first). Any other pair, including two list elements met on
the way, is `cannot use < on int and string`, at the operator.

`x in c` is `true` when:

- `c` is a map and `x` is one of its keys (an `x` that can't be a key is
  simply not in it);
- `c` is a list and an element is `==` to `x`;
- `c` is a string and `x` is a string that occurs in it (`""` is in any
  string).

Anything else is `cannot use in on int and int`, at `in`. `x not in c`
is `not (x in c)`, with faults at `not`.

### Logic

`and`, `or` and `not` take bools; `and` and `or` short-circuit, so the
right operand is evaluated only when it decides. A non-bool operand is
`cannot use and on int` (with the operator and the operand's type), at
the operator. There's no truthiness anywhere: `if` and `while` take
bools too.

### Indexing and fields

`xs[i]` is the element at `i`, from 0, of a list, or the one-byte string
at `i` of a string. `m[k]` is the value at key `k` of a map. `m.name` is
`m["name"]`. Faults, at the `[` or the `.`:

- `index 5 out of range (length 3)` for a list or string, including any
  negative index;
- `missing key "qty"` or `missing key 7`, for a map;
- `list index must be an int, got string` (or string index);
- `map key must be an int or a string, got list`;
- `cannot index int` for `[` on anything else, and
  `cannot use .name on list` for `.` on anything but a map.

The first two are **misses**, which `else` can catch.

### `else`: the fallback for a lookup

`a else b` is `a`, unless a lookup written in `a` misses, in which case
it's `b`:

```
counts[w] = counts[w] else 0 + 1     // (counts[w] else 0) + 1
let port = int(text) else 8080
for road in roads[here] else [] { ... }
```

A lookup is an index `x[i]`, a field `x.name`, or a call to the builtin
`int`. A miss is an index out of range, a missing key, or `int` given a
string that isn't a number. `b` is evaluated only after a miss.

What is caught is decided by where the code is written: a miss in any
lookup written inside `a`, including in its index expressions and
interpolations, is caught, and nothing else is. A miss inside a function
that `a` calls faults as usual, and so does every other fault in `a`.
A left operand with no lookup written in it is
`else needs a lookup on its left: an index, a field or int()`, at
`else`.

`else` binds tighter than any binary operator and looser than prefix
minus, so it attaches to the operand next to it, and associates to the
left: `a else b else c` tries `a`, then `b`, then gives `c`.
(Step 7, D20.)

### Calls

`f(a, b)` calls the function or builtin `f`. The argument list may break
across lines and may end with a comma (D34). Arguments are evaluated
left to right, then the call is made. Each function and most builtins
take a fixed number of arguments; another number is
`f takes 2 arguments, got 3` (`1 argument` when it's one), at the name.
A name that isn't a function or builtin is `unknown function f`.

A call nested more than 1000 deep faults:
`stack overflow (more than 1000 nested calls)`, at the call's name. Only
calls of functions you define count, and the top level isn't one:
`down(999)` for a `down` that calls itself until `n` is 0 makes 1000
nested calls and succeeds; `down(1000)` makes a 1001st and faults.
Arguments are evaluated before the depth is counted. (Step 3, D28, D41.)

## Statements

### Expression statements

A call on its own line runs it and drops its result. Any other
expression on its own is `expression statement must be a call`, at its
first token, which catches `x == 1` written for `x = 1`. A call in
parentheses is still a call (D38).

### `if`

```
if n % 15 == 0 {
  print("FizzBuzz")
} else if n % 3 == 0 {
  print("Fizz")
} else {
  print(n)
}
```

No parentheses are needed around the condition; braces are required.
`else` may be on the line after the `}`, and `else if` chains as often as
needed. A block is not a statement of its own: `{` starts one only after
a condition, `else`, or a loop header. The condition must be a bool,
or the fault is `condition must be a bool, got int`, at the condition's
first token. Each block is a scope. (Step 2.)

### `while`

`while cond { ... }` runs the block while `cond` is `true`, with the
same condition fault as `if`. (Step 2.)

### `for`

```
for i in 1..=100 { ... }     // 1 to 100
for i in 0..len(xs) { ... }  // 0 to len(xs) - 1
for x in xs { ... }          // each element
for k in m { ... }           // each key, in order
for c in s { ... }           // each byte, as a one-byte string
```

`a..b` and `a..=b` exist only here, in a `for` header: from `a` up to
but not including `b`, or up to and including `b`. Both bounds are
evaluated once, before the loop, left then right, and then both
checked, the left first: they must be ints
(`range bounds must be ints, got string`, at the first token of the bad
bound). When `a` is past the end there are no iterations.

For a list, map or string, the expression is evaluated once and the loop
walks that value; changing the variable it came from inside the loop
doesn't change what the loop sees (the core rule). Anything else is
`cannot iterate over int`, at the expression's first token.

The loop variable is declared fresh in each iteration, in the loop's
scope, and can be assigned like any variable. (Steps 2, 4, 5, 6.)

### `break` and `continue`

Leave the innermost loop, or go to its next iteration. Outside a loop:
`break outside a loop`, `continue outside a loop`, at the keyword.

### Functions and `return`

```
fn gcd(a, b) {
  while b != 0 {
    let t = b
    b = a % b
    a = t
  }
  return a
}
```

`fn` defines a function, at the top level only (anywhere else:
`functions are defined at the top level`, at `fn`). Parameters are
variables of the function, each a copy of its argument. A function sees
its parameters, its own variables and every function, and nothing else:
not the top level's variables (the core rule, D13).

`return expr` ends the function with that value; `return` alone, or
reaching the end, returns `nil`. `return` at the top level is
`return outside a function`.

Compile errors, at the name: `duplicate function f`,
`print is a builtin` (defining a builtin's name), and, at the second
one, `x is already declared` for a repeated parameter (a `let` or `for`
in the body that reuses a parameter's name is the same error). A parameter list
may break across lines and end with a comma, like an argument list, and
the body's `{` is on the line of the `)`. A bare `return` is one followed
by a newline, `;` or `}`. A name in a function that is declared there
nowhere is `unknown variable`, unless the top level's code declares it
anywhere (a `let` or `for` at any depth, above or below the function),
which is the longer message under Variables. A function can have the
name of a variable, its own or the top level's: they are separate names.
(Step 3, D41.)

## Builtins

Builtins are called like functions. A builtin given an argument of the
wrong type faults, at its name, with `name: expected T, got U`, where `T`
is given with each builtin below.

**`print(a, b, ...)`** writes the printed form of each argument,
separated by single spaces, then a newline, to standard output. Any
number of arguments, none included. Returns `nil`.

**`str(x)`** is the printed form of `x` as a string. Strings are
themselves at the top level, and in double quotes inside a list or map,
with `\\`, `\"`, `\n`, `\t` and `\r` escaped and every other byte as it
is. Ints are decimal. `true`, `false`, `nil`. Lists are
`[1, "a", [2]]` and `[]`; maps `{"name": "pen", 3: true}` and `{}`, in
key order. So `print(["a"])` prints `["a"]` and `print("a")` prints `a`.

**`len(x)`**: the number of bytes in a string, elements in a list, or
keys in a map. Expects `a string, list or map`.

**`int(s)`**: the int that the string `s` spells: an optional `-` and
one or more decimal digits, nothing else (no `+`, spaces or `_`), in
range. Otherwise it misses, with the fault `not a number: "12x"` (the
string printed as in a list), at `int`, which `else` can catch.
Expects `a string`.

**`keys(m)`**: the keys of a map, as a list, in order. Expects `a map`.

**`remove(m, k)`**: the map `m` without the key `k`; the same map if
`k` isn't in it. Expects `a map`.

**`sort(xs)`**: the elements of the list in ascending order, by `<`;
equal elements keep their order. A pair that `<` can't compare faults
as `<` would, at `sort`: `cannot use < on int and string`. Expects
`a list`.

**`slice(x, from, to)`**: the elements (or bytes) of a list (or string)
from index `from` up to but not including `to`. Unless
`0 <= from <= to <= len(x)`, it faults with
`slice 2..9 out of range (length 3)`, at `slice`. Expects
`a list or string`, then `an int` for each bound.

**`words(s)`**: the pieces of `s` between runs of spaces, tabs,
newlines and carriage returns, as a list of strings, with no empty
pieces. Expects `a string`.

**`split(s, sep)`**: the pieces of `s` between occurrences of `sep`,
empty ones included: `split("a,,b", ",")` is `["a", "", "b"]`. An empty
`sep` faults with `split: empty separator`. Expects `a string` for
both.

**`join(xs, sep)`**: the strings of `xs` with `sep` between them.
Expects `a list of strings` (an element that isn't a string faults with
`join: expected a list of strings, got int`, the element's type) and
`a string`.

**`lower(s)`, `upper(s)`**: `s` with ASCII letters changed case, other
bytes as they are. Expects `a string`.

**`read()`**: everything left on standard input, as a string; `""` once
it's all read.

**`fail(msg)`**: faults with `msg` as the message (a string, or
the printed form of anything else), at `fail`. Never returns.

(Builtins arrive with the step for their types: `print` in step 0 and 1,
`str`, `len`, `int`, `lower`, `upper`, `slice` on strings, `read` and
`fail` in step 4, `words`, `split`, `join`, `sort` and `slice` on lists
in step 5, `keys` and `remove` in step 6.)
