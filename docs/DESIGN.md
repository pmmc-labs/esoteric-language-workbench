# Ditto design

This is the design as agreed. [`DECISIONS.md`](DECISIONS.md) has the
reasons and the alternatives that were turned down, [`PLAN.md`](PLAN.md)
the build order, and [`LANGUAGE.md`](LANGUAGE.md) every form, builtin,
error and fault in full; where this file and that one could disagree,
`LANGUAGE.md` is the spec for the language and this one for the
implementation. Nothing is **(open)**: in this run the designer made
every decision up front (D1).

## Goals

- **A small, practical, dynamically typed imperative language** for
  programs of a few hundred lines: scripts, puzzles, data wrangling,
  teaching (D1, D4).
- **Readable on sight** by someone who writes TypeScript, Python or Go:
  braces, `let`, `fn`, `if`/`while`/`for ... in`, `and`/`or`/`not`,
  string interpolation (D11).
- **Safer by default**: no aliasing (D7), no truthiness or implicit
  conversion (D10), checked integer arithmetic (D14), every fault with a
  position (D28), and expression statements that must be calls (D21).
- **Aggressively simple** (D5): six types, one compound-key type, no
  first-class functions, no floats, no garbage collector.
- **Compiled**: TypeScript on Node 22 compiles a `.ditto` file to C11,
  linked with a runtime in C by `cc` (D6).

## Non-goals

- Speed. Updates copy (D7) and maps search linearly (D27).
- Large programs: no modules, no imports, one file.
- Long-running programs: memory is never freed (D26).
- Self-hosting. Ditto has no file output and no first-class functions;
  the compiler stays in TypeScript.
- Static types. Faults are dynamic, with positions.

## The language

Values are ints, strings, bools, `nil`, lists and maps (records are
maps, `r.f` is `r["f"]`). Statements are `let`, assignment to a path
(`x`, `x[i]`, `x.f`, chained, with compound `+=` etc.), `if`/`else`,
`while`, `for` over ranges, lists, map keys and string bytes, `break`,
`continue`, `return`, and calls. Functions are top-level, hoisted, of
fixed arity, and see only their parameters and locals. Builtins:
`print str len int keys remove sort slice words split join lower upper
read fail`. Full text in `LANGUAGE.md`.

## The core rule

**Every value is a value (D7).** Lists and maps have the semantics ints
have: assignment, argument passing and storing give the receiver its
own value, and nothing anyone else does changes it. The implementation
gets this without copying on assignment: a heap object is never written
while more than one place can see it. `xs[i] = v` writes in place when
the variable `xs` is the only holder of its list (D48), and otherwise
builds a new list, which `xs` then holds alone. Updating a path
`a[i].f[j] = v` rebuilds the inner levels and sets the outermost through
the variable, in place when it can.

What it removes: aliasing bugs (the defensive copy, the default-argument
list, the loop that mutates what it iterates), cycles (so printing,
equality and ordering are simple recursions that end), and the need for
any memory management beyond allocation (no object is ever written
after it's built, so there's nothing a collector would have to track,
if one were ever added). It also decides that functions can't see
top-level variables (D13): with no globals, a function's only effect on
the world is its return value and its output.

What it costs: an update of a shared value copies it, O(n), once; after
that the variable owns the copy and updates are O(1), and appends are
amortized O(1) (D48). Nested levels below a variable are copied on each
update, O(their size). Functions that "change" something return it:
`accounts = deposit(accounts, 5)`; the parameter's first update copies.

How D48 knows a variable is the only holder: each list and map has an
`owner`, the address of the C variable holding it alone, set when an
update through that variable makes or reuses it. Every read of a
variable that could keep the value (assigning it, passing it, storing
it, returning it, iterating it, printing it) clears the owner first
(`dt_share`); only lookups that keep nothing of the container (`x[i]`,
`x.f`, `len(x)`, the right of `in`) read without clearing. An element of
a container is never owned, since whatever was stored was read that
way. So `owner == &slot` implies nothing but `slot` refers to the
object, and writing it in place can't be seen.

A proposal that touches this rule (an in-place optimization, a
reference type, a global) is recognised by it, and needs a decision.

## The second idea

**`a else b` (D20)** catches a *miss* (index out of range, missing key,
`int` of a non-number) in a lookup written in `a`, and gives `b`. It
replaces `get(k, default)`, `try/except KeyError` and `?? ` with one
operator that works for lists, maps, records and parsing, and since
which misses it catches is lexical, the compiler knows exactly where
they are and compiles each to a branch.

## Values and memory

A value is a 16-byte struct passed by value in C:

```c
typedef enum { T_NIL, T_BOOL, T_INT, T_STR, T_LIST, T_MAP } Tag;  // C, not TS
typedef struct Value { uint8_t tag; union { int64_t i; bool b;
  struct Str *s; struct List *l; struct Map *m; }; } Value;
```

`Str` is a length and bytes; `List` a length and an array of `Value`;
`Map` a length and arrays of keys and values in insertion order, looked
up by linear search with `==` on keys (D27). Strings are immutable; lists
and maps carry a capacity and an `owner` (D48) and are written only by
an update through their owning variable. Memory comes from a bump allocator over large
`malloc`ed chunks kept on a global list, and is never freed (D26); the
chunks stay reachable, so LeakSanitizer stays quiet.

## The runtime

`runtime/ditto.h` and `runtime/ditto.c`: value constructors, the
operators with their checks, indexing and setting, equality and
ordering, printing, the builtins, iteration helpers, the fault function,
the call-depth counter and the allocator. A fault flushes standard
output, writes `path:line:col: fault: message` to standard error, and
exits 1. Runtime functions that can fault take the position as two
`int` arguments (line, column); the path is a global the generated
`main` sets.

There is no prelude written in Ditto: every builtin is C (D3).

## The compiler

`compiler/src/`, run directly by Node 22 (type stripping; `.ts`
imports; erasable syntax only, so no enums and no parameter
properties):

- `lexer.ts`: bytes to tokens with line and column; newline tokens,
  dropped inside `( )` and `[ ]`; strings with interpolation become one
  token holding literal parts and the token lists of each `{...}`.
- `parser.ts`: tokens to an AST of plain objects with a `kind` and a
  `pos`. Precedence climbing per `LANGUAGE.md`'s table. The parser skips
  newlines after a binary operator, `else`, `,`, `=`, a compound
  assignment and inside map literals, and before an `else` that follows
  an `if` block.
- `resolve.ts`: scopes and names (D12, D13), arity, `break`/`continue`/
  `return` placement, `else` needing a lookup, duplicate keys and
  functions. Annotates each variable use with its C name.
- `codegen.ts`: AST to C. Every subexpression is computed into a fresh
  temporary, in source order, so C's unspecified argument order never
  shows (D30). Short-circuit logic, `else` and loops are `if` and
  `goto`. Standard C11, no extensions.
- `errors.ts`: the compile error type and its formatting.
- `main.ts`: the command line (D31).

The compiler is pure functions over plain data, discriminated unions
with a `kind` string, no classes (D29). It stops at the first error.

## Errors and faults

Every message and the position it points at is in `LANGUAGE.md`, beside
its form; the builder doesn't invent them. Two formats:

```
path:line:col: error: message      (compiler, exit 2)
path:line:col: fault: message      (program, exit 1)
```

Parser errors not listed there take the shape
`expected X, found Y`, where `Y` is `end of file`, `newline`, `string`,
or the token's text in single quotes (`'}'`, `'else'`, `'count'`,
`'42'`), and `X` is what the parser wanted: `an expression`, `'{'`,
`')'`, `a name`, `newline` (after a complete statement), and so on.
That shape is the decision; the builder picks `X` per site and records
nothing.

## The six examples, as designed

Written before any code to test the design; they are the programs
`examples/` will hold (step 8). Each read naturally on the first
attempt, except the word count, which first needed a sort by key: it
now prints counts in first-seen order and finds the top with a loop,
and that turned out clearer than the sorted version.

### 1. FizzBuzz

```
for i in 1..=100 {
  if i % 15 == 0 {
    print("FizzBuzz")
  } else if i % 3 == 0 {
    print("Fizz")
  } else if i % 5 == 0 {
    print("Buzz")
  } else {
    print(i)
  }
}
```

### 2. Recursion

```
fn fact(n) {
  if n == 0 { return 1 }
  return n * fact(n - 1)
}

fn fib(n) {
  if n < 2 { return n }
  return fib(n - 1) + fib(n - 2)
}

for n in 0..=20 {
  print("{n}! = {fact(n)}, fib({n}) = {fib(n)}")
}
```

### 3. Sorting

```
fn quicksort(xs) {
  if len(xs) < 2 { return xs }
  let pivot = xs[0]
  let smaller = []
  let larger = []
  for i in 1..len(xs) {
    if xs[i] < pivot { smaller += [xs[i]] } else { larger += [xs[i]] }
  }
  return quicksort(smaller) + [pivot] + quicksort(larger)
}

fn insertion_sort(xs) {
  for i in 1..len(xs) {
    let j = i
    while j > 0 and xs[j - 1] > xs[j] {
      let t = xs[j]; xs[j] = xs[j - 1]; xs[j - 1] = t
      j -= 1
    }
  }
  return xs
}

let data = [31, 4, 15, 9, 26, 5, 35, 8, 97, 93, 2, 38, 46, 26, 43]
print(quicksort(data))
print(insertion_sort(data))
print(data)                      // untouched: each function sorted a copy
print(sort(data) == quicksort(data))
```

### 4. Word count

```
fn clean(word) {
  let out = ""
  for c in lower(word) {
    if c >= "a" and c <= "z" or c == "'" { out += c }
  }
  return out
}

let counts = {}
let total = 0
for raw in words(read()) {
  let w = clean(raw)
  if w != "" {
    counts[w] = (counts[w] else 0) + 1
    total += 1
  }
}

let best = ""
for w in counts {
  if best == "" or counts[w] > counts[best] { best = w }
}
print("{total} words, {len(counts)} different")
print("most common: \"{best}\", {counts[best]} times")
for w in counts {
  if counts[w] > 1 { print("{w}: {counts[w]}") }
}
```

### 5. Route finding (compound data)

```
fn route(roads, start, goal) {
  let came_from = {}
  came_from[start] = start
  let queue = [start]
  let next = 0
  while next < len(queue) {
    let here = queue[next]
    next += 1
    if here == goal {
      let path = [goal]
      while path[0] != start {
        path = [came_from[path[0]]] + path
      }
      return path
    }
    for road in roads[here] else [] {
      if road not in came_from {
        came_from[road] = here
        queue += [road]
      }
    }
  }
  return nil
}

let roads = {
  home: ["bakery", "park"],
  bakery: ["home", "market", "school"],
  park: ["home", "lake"],
  market: ["bakery", "station"],
  school: ["bakery", "station"],
  lake: ["park"],
  station: ["market", "school"],
}
print(route(roads, "home", "station"))
print(route(roads, "lake", "school"))
print(route(roads, "home", "airport"))
```

### 6. All-or-nothing transfers (the core rule)

```
// apply() works on its own copy of the accounts, so a batch that fails
// halfway leaves the caller's accounts exactly as they were.
fn apply(accounts, batch) {
  for t in batch {
    if t.from not in accounts or t.to not in accounts {
      return {ok: false, why: "no account for {t}"}
    }
    if accounts[t.from].balance < t.amount {
      return {ok: false, why: "{t.from} has only {accounts[t.from].balance}"}
    }
    accounts[t.from].balance -= t.amount
    accounts[t.to].balance += t.amount
    accounts[t.from].log += ["-{t.amount} to {t.to}"]
    accounts[t.to].log += ["+{t.amount} from {t.from}"]
  }
  return {ok: true, accounts: accounts}
}

let accounts = {
  alice: {balance: 100, log: []},
  bob: {balance: 50, log: []},
  carol: {balance: 0, log: []},
}
let opening = accounts
let batches = [
  [{from: "alice", to: "bob", amount: 30}, {from: "bob", to: "carol", amount: 60}],
  [{from: "carol", to: "alice", amount: 10}, {from: "carol", to: "bob", amount: 90}],
  [{from: "bob", to: "dave", amount: 5}],
]
for batch in batches {
  let result = apply(accounts, batch)
  if result.ok {
    accounts = result.accounts
    print("applied {len(batch)} transfers")
  } else {
    print("rejected: {result.why}")
  }
}
for name in accounts {
  print("{name}: {accounts[name].balance} {accounts[name].log}")
}
print("opening: {opening}")
```

In TypeScript, the second batch would have left carol 10 poorer and
alice 10 richer with nothing logged as applied, unless `apply` began
with a deep clone; in Ditto the failed batch can't leak, and `opening`
is still the opening balances at the end, with no copy written anywhere.

## Open questions

None. Defaults a builder takes are recorded as *(default)* in
`DECISIONS.md` and decided at review.
