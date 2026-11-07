# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. In this run there is no separate person: the agent is both
designer and builder (`docs/briefs/design-and-build.md`). **designer**
means the designer decided it, up front or at a step's review;
**default** means a builder took it without discussion, and it stands
until the designer's review keeps it (then it's marked *(designer,
kept)*) or changes it. Defaults are fair to revisit.

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics, the reason, and `Rejected:` with each
alternative and why it lost. A decision that's later changed stays,
with a note pointing to the entry that changed it; the new entry says
what it retires.

Sections group entries by subject, not by time; a new entry goes in the
section it belongs to. Number by time.

## Scope

**D1. Ditto: a small, practical, dynamically typed imperative language,
designed in full before any code.** *(designer)* The brief asks for a
language someone who writes TypeScript, Python or Go can read at once
and write in the same day, with creativity spent on making ordinary
programs better. With no person to consult, deciding everything up
front (every form, builtin, error message and position) is what keeps
builders from inventing. Rejected: a language around one striking idea
(the brief's warning: the last one was too strange to use); designing
step by step (builders would fill the silences).

**D2. Nothing is kept from before.** *(designer)* The repository is the
template; there's no earlier implementation.

**D3. The runtime is C and holds every builtin; there's no prelude in
Ditto.** *(designer)* Without first-class functions (D22) a prelude
could only hold plain functions over lists and strings, which are
shorter and faster in C, and a prelude would cost a step. Rejected: a
prelude in Ditto (a step for little), builtins as generated C (harder to
test than a C file).

**D4. Scale: programs of a few hundred lines over data in the
thousands.** *(designer)* This licenses O(n) updates (D7) and linear map
lookup (D27). Rejected: designing for large data (would need in-place
updates and hashing, both machinery).

**D5. Aggressively simple; practical over pure.** *(designer)* Any
feature that adds complexity can be cut or changed.

**D6. TypeScript on Node 22 compiles to C11, linked with a C runtime by
`cc`.** *(designer; fixed by the brief)* `LANG_CC` overrides the C
compiler; the suite passes under gcc, clang, and clang with
`-fsanitize=undefined,address`.

## The core rule

**D7. Every value is a value.** *(designer)* Lists and maps behave as
ints do: assigning, passing or storing one gives the receiver its own
value, which no one else can change. Implemented by never writing a heap
object after it's built: `xs[i] = v` builds a new list (sharing the
elements) and stores it in `xs`; a path update `a[i].f = v` rebuilds the
spine. It removes aliasing bugs, makes cycles impossible (printing and
equality are plain recursions), and needs no memory management. It
costs an O(n) copy per update and means functions return what they
change. It earns its place in the ledger example (step 8): a batch of
transfers applied to a copy that is simply dropped on failure, which in
TypeScript needs a deep clone nobody remembers to write. Rejected:
reference semantics (the aliasing bugs this exists to remove);
copy-on-write with reference counts (in-place when unique: a count on
every value and every assignment, machinery the D4 scale doesn't need);
immutable values without update syntax (`xs = set(xs, i, v)` everywhere
reads badly to the audience); ownership and borrowing in the style of
Hylo or Rust (a checker and rules the audience doesn't know).

## Language

**D10. Dynamic types, strictly: no truthiness, no implicit conversion.**
*(designer)* `if`, `while`, `and`, `or`, `not` take bools; `+` doesn't
mix types; every type error is a fault with a position. Static types
would need a checker step the budget doesn't have. Rejected: static
types (budget); truthiness (`if xs` hides the empty/nil distinction
and is a classic bug); implicit int-to-string in `+` (interpolation does
it explicitly).

**D11. Braces and newlines, Go-shaped.** *(designer)* `if cond { }`
without parentheses, braces required, newline ends a statement, `;`
for several on a line, `//` comments, `else` allowed on the line after
`}`. Newlines don't end a statement inside `( )`, `[ ]`, a map literal,
or after a binary operator, `else`, `,`, `=` or a compound assignment.
Rejected: indentation (fragile in a lexer, and in pasted code); required
semicolons (noise); Go's rule that `else` must follow `}` on its line
(an error the reader doesn't need).

**D12. `let` declares; no shadowing; block scope.** *(designer)*
Assignment to an undeclared name is an error, so a typo can't create a
variable. No shadowing at all, so a name means one thing within a
function. Rejected: Python's implicit declaration (typos);
`const`/`let` split (with value semantics a variable is the only thing
that can change, and `const` would be a second keyword for little).

**D13. Functions are top-level, hoisted, fixed arity, not values, and
see only their parameters and their own variables.** *(designer)* The
last part follows from D7: with no globals, nothing reaches a function
but its arguments, and nothing leaves it but its result and its output.
Rejected: globals readable from functions (a constant passed as an
argument is one more word; a global changed under a function is what D7
removes); nested functions and closures (see D22).

**D14. Ints only: 64-bit, checked, truncating division.** *(designer)*
Overflow and division by zero fault; `/` truncates and `%` follows the
dividend's sign, as in C, Go and TypeScript's `Math.trunc`.
`MIN / -1` overflows; `MIN % -1` is 0. Rejected: floats (a printing
format, a model of it, and a second numeric type to mix, for programs
the examples don't need); bignums (machinery); Python's floor division
(surprises the TypeScript and Go readers).

**D15. Strings are immutable bytes, with `{expr}` interpolation.**
*(designer)* Indexing and `for` give one-byte strings; `len` is bytes.
Interpolation is the only conversion to text, and makes `print` lines
read like the output. `\{` and `\}` escape braces. Rejected: characters
as a type (one more type, and Unicode semantics); code points (UTF-8
decoding for little gain in small programs); `${}` (noisier).

**D16. Lists and maps; maps are records.** *(designer)* One keyed
type: insertion-ordered maps with int or string keys, and `m.f` is
`m["f"]`. A map literal's bare name key is that string. Keys in a
literal must be distinct (a compile error). Rejected: a separate record
or struct type (a second type to explain, and its literal would collide
with the map's); tuples (lists do); bool or list keys (equality on keys
stays simple).

**D17. Operators: Python's words, C's symbols, no chained
comparisons.** *(designer)* `and or not in not in` as words; `== != <
<= > >= + - * / %` as symbols; `+` also joins strings and lists;
compound assignment `+= -= *= /= %=`. `a < b < c` is a compile error
rather than either meaning. Precedence in `LANGUAGE.md`. Rejected:
`&& || !` (two spellings of the same thing); `**`, bit operators,
`++` (no example needs them).

**D18. Equality is structural and never faults; ordering is for ints,
strings and lists.** *(designer)* With D7 there's no identity to
compare, so `==` compares values; different types are unequal; maps are
equal regardless of key order. `<` on lists is lexicographic, so a list
of `[score, name]` pairs sorts naturally. Rejected: ordering maps or
bools (no natural order); `==` faulting on mixed types (`x == nil` must
work).

**D19. `for` walks ranges, lists, map keys and string bytes, over a
snapshot.** *(designer)* `a..b` is half-open and `a..=b` inclusive, as
in Rust, and exist only in a `for` header, so they need no value
representation. The iterated value is evaluated once, and by D7 the loop
sees it as it was. Rejected: ranges as values (a type for one use);
inclusive `..` (half-open is what indexing wants); C-style three-part
`for` (the range covers it).

**D20. `a else b`: the fallback for a lookup that misses.** *(designer)*
The second idea. A miss is an index out of range, a missing key, or
`int` of a non-number; `else` catches the misses of the lookups written
in its left operand, lexically, and nothing else. It binds tighter than
any binary operator so it attaches to the operand next to it:
`counts[w] else 0 + 1`. A left operand with no lookup is a compile
error. It earns its place in the word count (`counts[w] else 0`), the
route finder (`roads[here] else []`) and input parsing
(`int(s) else 0`); without it each needs an `if ... in ...` and a second
lookup. Rejected: exceptions with `try`/`catch` (a runtime mechanism,
and they catch more than was meant); lookups returning `nil` on a miss
(nil spreads until something far away faults); `get(m, k, default)`
(one builtin per container, and nothing for parsing); catching misses
dynamically inside called functions (a function's internal bug would be
silently defaulted, and it needs `setjmp`).

**D21. An expression statement must be a call.** *(designer)* Catches
`x == 1` written for `x = 1`, and lookups written for their fault.
Rejected: any expression (silent no-ops).

**D22. Builtins: `print str len int keys remove sort slice words split
join lower upper read fail`; no first-class functions.** *(designer)*
The set the six examples and ordinary scripts need. One calling syntax,
`f(x)`. Appending is `xs += [x]`. Rejected: method syntax `xs.len()`
(two ways to call, and `.` already means field); `push` (`+=` does it);
first-class functions, lambdas and `sort` by key (closures are a step of
their own and every example reads well without them; a list of
`[key, value]` pairs sorts by key); `type(x)` (no example needs it;
dynamic checks are the runtime's job); `min`, `max`, `abs`, `range`
(one-liners in Ditto).

**D23. `nil` is a value.** *(designer)* What a function returns
without `return`, and a literal for "nothing yet". It has no operations
but `==`, `!=` and printing. Rejected: no nil at all (functions would
need a return value always, and "not found" would need a sentinel).

**D24. Printed form: strings bare at the top, quoted inside
containers.** *(designer)* `print("a")` prints `a`, `print(["a"])`
prints `["a"]`, so a list of strings is unambiguous. Inside quotes,
`\\ \" \n \t \r` are escaped and other bytes are raw. Map keys print as
values do (`{"qty": 3, 7: true}`). Rejected: printing record keys bare
(`{qty: 3}`: prettier, but a second rule); escaping every non-printable
byte (UTF-8 text should print as itself).

**D25. Input is `read()`, all of standard input as one string.**
*(designer)* The one input a script needs; `split(read(), "\n")` gives
lines. Rejected: line-at-a-time input (a second builtin and an
end-of-input value); command-line arguments (no example needs them).

**D34. A call's arguments may end with a comma.** *(default; designer, kept)*
`LANGUAGE.md` allows it for lists and maps only and is silent on calls;
Go and TypeScript allow it, and a call broken over several lines reads
better with it. `print(,)` is still an error. Rejected: forbidding it
(one more thing to trip over for the audience).

**D35. Lexer details the spec left open.** *(default; designer, kept)* A bare `}` in a
string is an ordinary byte (only `{` starts interpolation). A backslash
at the end of a line is `unterminated string`. A string that runs off
the line inside an interpolation makes that interpolation
`unterminated interpolation`, at its `{`, rather than a second
`unterminated string`. An interpolation holding only spaces is
`empty interpolation`. Leading zeros in an integer are allowed
(`007` is 7). A run of newlines (with comments and blank lines) is one
newline token, and none comes before the first token. Rejected:
rejecting a bare `}` (Python's f-strings do; not worth a rule here),
leading-zero errors (octal confusion doesn't arise: there is no octal).

## Values and memory

**D26. A value is a 16-byte tagged struct passed by value; heap
objects are immutable; memory is never freed.** *(designer)* A bump
allocator over large chunks kept on a global list (so LeakSanitizer
sees them reachable). Rejected: pointer tagging (undefined-behaviour
traps under the sanitizers for little gain); a collector or reference
counts (D4: programs end before memory matters).

**D27. Maps are arrays of keys and values in insertion order, searched
linearly.** *(designer)* An update copies the map anyway (D7), so a hash
table wouldn't change the order of the cost. Rejected: hash tables
(machinery, and order would need a second array anyway).

## Runtime

**D28. A fault prints `path:line:col: fault: message` and exits 1;
calls nest at most 1000 deep.** *(designer)* Standard output is flushed
first, so a test sees output and fault in order. The position is the
operator, `[`, `.`, builtin name or condition per `LANGUAGE.md`.
A depth counter in every function makes deep recursion a fault, not a
crash, and 1000 (Python's limit) fits in the default stack even under
AddressSanitizer. Rejected: stack traces (one line is enough at this
scale); a larger limit (risks the C stack under the sanitizers before
the counter trips).

## Compiler

**D29. Four passes of pure functions over plain data; the first error
stops compilation, printed `path:line:col: error: message`, exit 2.**
*(designer)* Lexer, parser, resolver, codegen; AST nodes are objects
with `kind` and `pos`; no classes. Exit 2 keeps compile errors apart
from faults (1) in a golden test's `exit:` line. Rejected: error
recovery (one error at a time is enough for small programs).

**D30. Generated C computes every subexpression into a temporary, in
source order; standard C11 only.** *(designer)* C doesn't order a call's
arguments; nesting runtime calls in generated C would make Ditto's
evaluation order the C compiler's choice (PROCESS.md tells how that bit
before). `and`, `or`, `else`, `break`, `continue` are `if` and `goto`.
Rejected: GNU statement expressions (an extension, and still unordered
arguments); nested calls (above).

**D31. The command line: `bin/ditto build FILE -o EXE`,
`bin/ditto run FILE`, `bin/ditto c FILE`.** *(designer)* `build`
writes the C next to the executable as `EXE.c` and compiles it with
`$LANG_CC` (default `cc`) and
`-std=c11 -O1 $LANG_CFLAGS` with `runtime/ditto.c`; `run` builds into
`build/run/` and runs with the program's standard input and output;
`c` prints the C. Exit 2 for a compile error or bad usage, 3 if the C
compiler fails (always a compiler bug), otherwise `run` exits with the
program's status.

**D36. Parser errors at step 0.** *(default; designer, kept)* A statement that doesn't
start with a name is `expected a statement, found Y`; a name must be
followed by `(`, an argument by `,` or `)`, and a finished statement by a
newline, `;` or the end of the file (`expected newline, found Y`). A
file ending inside a call is `expected ')', found end of file`, at the
position after the last byte. These are the `expected X, found Y`
sites `DESIGN.md` leaves to the builder.

**D38. Step 1 details the spec left open.** *(default; designer, kept)* Parentheses
leave no node in the AST, so `(print(1))` is a call and an allowed
statement. Until variables arrive (step 2) a name in an expression can
only start a call, so `print(print)` is `expected '(', found ')'`. A
statement starting with anything that can start an expression is parsed
as one, so `42` is `expression statement must be a call` (test 027
changed from step 0's `expected a statement, found '42'`); only a token
that can't start an expression (`else`, `}`) is `expected a statement`.
The newline rule is as written: a newline is skipped after a binary
operator but not after a prefix `-` or `not`. In an arithmetic or
comparison operator a type fault is reported before `division by zero`
or `integer overflow`, and both operands are evaluated before either is
checked. `and`/`or` check the left operand before evaluating the right
and the right one after; both fault `cannot use and on T` with that
operand's type. Rejected: a paren node to forbid `(f())` as a statement
(machinery for a harmless case); reporting `comparisons do not chain` in
the resolver (the parser knows at once).

**D39. Step 2 details the spec left open.** *(default; designer, kept)* Parsing: the
target of `=` or a compound operator is parsed as an expression first, so
`cannot assign to this` (at the statement's first token) comes from the
parser, before any resolver error; a parenthesized name is still a name
(D38), so `(x) = 1` assigns. A bare name on its own line is
`expression statement must be a call` (test 025 changed from step 0's
`expected '(', found newline`). A bare `{ }` is not a statement
(`expected a statement, found '{'`). `else` may start the line after a
`}` only when nothing but that newline (and blank lines or comments)
separates them. The new `expected X` sites: `a name` (after `let`, after
`for`), `'='` (after `let x`), `'in'`, `'{'` (before every block,
including after `else`, which takes `{` or `if`), `'}'` (a block that
reaches the end of the file), and `a statement` for a keyword that can't
start one, `fn` and `return` included until step 3. `..` and `..=` are
tokens of the `for` header only, so elsewhere they are whatever the
surrounding rule expected (`print(1..2)` is `expected ')', found '..'`).
Scopes: the loop variable lives in the same scope as the body's own
variables, so `for i in ... { let i = 1 }` is `i is already declared`; in
`let x = ...` the name is checked before the value is resolved (leftmost
error first, and `let x = x + 1` is `unknown variable x` only when no `x`
is declared); in an assignment the target is resolved before the value.
`let print = 1` is allowed (variables and functions have separate
namespaces). A builtin's name used as a value is already
`functions are not values` (step 3 adds user functions to it). Rejected:
reporting `cannot assign to this` in the resolver (the parser knows at
once, as with `comparisons do not chain`); a block statement (a second
use of `{` that step 6's map literals would have to disambiguate).

**D40. Evaluation order of `for` headers.** *(default; designer, kept)* Both range
bounds are evaluated, left to right, and then checked, the low bound
first: `for i in nil..1 / 0` is `division by zero`, not
`range bounds must be ints, got nil`, as D38 does for an operator's two
operands. `for x in e` evaluates `e` once and then asks it for its
length, so `cannot iterate over T` points at `e`'s first token and comes
after any fault inside `e`. Codegen walks a range with an inclusive
`int64_t` counter that advances only after testing `k < hi`, so a range
ending at the largest int neither overflows nor loops forever; a
`for` over a collection walks it by index through `dt_iter_len` and
`dt_iter_item`, which steps 4 to 6 fill in (until then every value
faults). Rejected: checking each bound as it is evaluated (the order
would depend on which is bad); `k <= hi` with `k++` (undefined behaviour
at the largest int).

**D41. Step 3 details the spec left open.** *(default; designer, kept)* Parsing: a
parameter list is like an argument list (D34): it may break across
lines and end with a comma, and the body's `{` must be on the line of the
`)`. `fn` met anywhere but the program's own statements is
`functions are defined at the top level` at the keyword, from the parser
and before anything after it is read (so it comes before any resolver
error, like `cannot assign to this`). A `return` is bare when the next
token is a newline, `;`, `}` or the end of the file; otherwise an
expression follows. Resolving: errors still come in source order across
functions and top-level code, with the arity checked before the
arguments are resolved (`f(1, y, 3)` for a two-parameter `f` is the arity
error, not `unknown variable y`). `x is a top-level variable; ...` is said
for a name not declared in the function that is declared by any `let` or
`for` in the top level's own code, at any depth of blocks and above or
below the function; a name used inside a function that is declared
nowhere is `unknown variable`. A builtin's name is reserved only once the
builtin exists (`print` now), so `fn len` is allowed until step 4 adds
`len`; no test defines one. A parameter may have a builtin's or another
function's name (separate namespaces, D39). Depth: only calls of user
functions count; a call enters after its arguments are evaluated and
leaves when it returns, and the 1001st nested one faults at its name (the
top level is depth 0, so `f(999)` below makes exactly 1000). Codegen: a
function is a non-static C function `f_NAME` over `Value` parameters,
prototyped before any definition, with the call bracketed by `dt_enter`
and `dt_leave`; its parameters are the C parameters themselves, which is
the copy the core rule asks for since values are immutable. The generated
file turns off `-Winfinite-recursion` with a pragma, because gcc and
clang report a function that always calls itself, which in Ditto is a
valid program that faults at the depth limit. Rejected: checking depth
inside every function (an extra statement in each body for the same
effect); `static` functions with `__attribute__((unused))` (an
extension, D30); reserving all fifteen builtin names now (a function
could not be called `len` yet `len(x)` would still be `unknown function`
until step 4); reporting `functions are defined at the top level` from
the resolver (the parser knows at once).

**D42. Step 4 details the spec left open.** *(default; designer, kept)* Parsing: `in` and
`not in` are comparisons, so a newline after them is skipped like after
any binary operator and they don't chain (the error points at the second
operator, the `not` of a `not in`). A `x not in c` that faults says
`cannot use in on T and U`, at the `not`: it is `not (x in c)`, so the
operator that failed is `in`. Each `{expr}` of a string is parsed on its
own and must be used up by the expression: `"{1 2}"` is
`expected '}', found '2'`, and `"{1 +}"` is
`expected an expression, found '}'`, pointing at the closing brace (the
lexer records where it was). An index `x[i]` is parsed after any primary
(a call, a parenthesized expression, a string literal) and binds tighter
than prefix minus; `.name` is not parsed until step 6, so a `.` after an
expression is an ordinary `expected newline, found '.'`. A string is no
longer `expected an expression` as a call argument (test 024 now has two
strings side by side: `expected ')', found string`). Runtime: an index
checks the container's type (`cannot index int`), then the index's
(`string index must be an int, got bool`), then the range, so the miss is
the last thing that can happen; a builtin checks its arguments left to
right (`slice` the value, then `from`, then `to`) and the range last.
`fail` writes a string's bytes as they are (NULs and all) and any other
value as `str` gives it. `len` already answers for lists and maps, which
no program can make yet. Shape for step 7: every lookup is a runtime
function that returns whether it hit (`dt_try_index`, `dt_try_int`) and
faults only for what `else` must not catch; `dt_index` and `dt_b_int` are
those plus the fault for a miss, so the `else` branch needs no new runtime
support. Codegen: a string literal is built once, in a `static Value`
cached at its first use, so a literal in a loop allocates once;
interpolation computes every part in order into temporaries and joins
them with `dt_interp`. Rejected: parsing `.name` now to give
`cannot use .name on string` (a form no test of this step can use);
`setjmp` for misses (D20 rejects it); building each literal on every
evaluation (allocation per iteration for no gain).

**D43. Step 5 details the spec left open.** *(default; designer, kept)* Sorting: `sort`
is a stable merge sort that puts the right item first only when it is
strictly less than the left one, so the pair it compares is always
(later, earlier) and an uncomparable pair faults as `later < earlier`
would: `sort([1, "a"])` is `cannot use < on string and int`, and a list
of fewer than two elements never faults. Ordering a pair of lists compares
the items one by one with `<`'s own rules, so `[nil] <= [nil]` is
`cannot use <= on nil and nil` (an item pair is not tested for `==`
first), with the operator the program wrote. Builtin checks go left to
right, each argument whole before the next: `split` the string, then the
separator, then `split: empty separator`; `join` the list and then every
one of its items (the item's type is named), then the separator. `join`
accepts an empty separator; `split` and `words` pieces are new strings.
The set of an assignment checks the container's type first (`cannot assign
into T`, so a string indexed by a bad key says that), then the key's type,
then its range. Parsing: the target of an assignment is parsed as an
expression and then read back as a name with index steps, so `(xs)[0] = 1`
assigns (as `(x) = 1` does, D39) and a list literal, a call, a string or an
operator at the root is `cannot assign to this` at the statement's first
token; a `[` at the start of a line starts a statement, so `xs` newline
`[0] = 1` is two statements. A list literal's items are any expressions;
a missing comma is `expected ']', found '2'`. Codegen: an indexed
assignment computes the keys, then (compound only) the current value by the
lookups an expression would make, then the right-hand side and the
operator; `store` then looks up every step but the last, sets the last with
`dt_set_index` and sets each level back into the one above, innermost
first; for a compound assignment the lookups run twice, which only costs
time since they cannot fail the second time. Every update copies the list
it changes and memory is never freed (D26), so the tests keep lists
small (a swap in an insertion sort of 30 items is two 480-byte copies).
`==` on two maps stays false until step 6, since no map can be made yet.
Rejected: insertion sort or a different comparison order for `sort` (the
(later, earlier) rule is what any stable algorithm that tests `later <
earlier` does, and the model needs a pair it can state); testing `==`
before `<` inside lists (a second rule); a store that mutates a list nobody
else holds (D7 rejects it); evaluating a compound assignment's path once
and keeping the containers (a second code path for the same result).

**D44. Step 6 details the spec left open.** *(default; designer, kept)*
Parsing: a map key is judged by its first tokens: a name (the string it
spells; a keyword is not a name), a string without interpolation, an int
literal, or `-` followed by an int literal; anything else is `map key must
be a name, a string or an int` at that token (so `{[1]: 2}`, `{(1): 2}`,
`{-a: 1}`, `{, a: 1}` and the second comma of `{a: 1,, b: 2}`), and a good
key not followed by `:` is the ordinary `expected ':', found '+'` (so
`{1 + 2: 3}` and `{f(): 1}` point at the `+` and the `(`). Newlines are
ignored anywhere between a map literal's braces, which the parser does since
the lexer cannot tell a map's `{` from a block's. A `{` is a map literal
wherever an expression starts, including after `if`, `while` and `in`, so
`while {` is now a map as a condition (test 270 now uses `while )`); a `{`
at the start of a statement is still `expected a statement, found '{'`,
which is what a stray block gets. A `.` must follow its operand on the same
line (`m` newline `.a` is `expected a statement, found '.'`), and a field
name is a name, not a keyword (`expected a name, found 'in'`). Checks: a
lookup or set checks the container's type first, then the key's
(`map key must be an int or a string, got list`), then the miss; a literal's
keys are compared in the resolver in source order, each key before its own
value, so `{a: x, a: 1}` is `unknown variable x` and `{a: 1, a: x}` is
`duplicate key "a"`; a duplicate key is shown as a key is printed (`"a"`,
`3`, `-3`, quotes and escapes as D24), and `007` and `7` are the same key.
Faults: the `.name` of `cannot use .name on list` is the field as written,
so `xs.count` is `cannot use .count on list`; setting through a `.name` on a
list says that too, and on any other non-map `cannot assign into T`, while
`[` on a map accepts any int or string key. `keys` and `remove` expect `a map`
for their first argument, and `remove(m, k)` with a `k` that cannot be a key
(a list, say) is the same map, as `k in m` is false for it. Runtime: maps
are immutable like lists (D7), `dt_set_index` and `dt_set_field` copy the
two arrays and replace in place or append, `==` looks each key of one up in
the other, `for` walks `keys` by index over the snapshot, and a map is
`{"a": 1, 3: "x"}` with keys printed as values are (D24). The lookups keep
the try shape of step 4: `dt_try_index` and `dt_try_field` report a miss,
`dt_index` and `dt_field` fault on it. Rejected: key expressions in
brackets, `{[k]: v}`, as in JavaScript (D16 keeps the literal to constants,
and `m[k] = v` covers the rest); a hash index (D27); `.name` on a list as a
miss (a wrong type is a fault `else` must not catch); a separate message for
`m.name` on a missing key (`missing key "name"` is what `m["name"]` says).

**D46. Step 7 details the spec left open.** *(default; designer, kept)* Which lookups make
a left operand acceptable: any index, field or call of `int` written
anywhere in it counts, including one inside a nested `else`'s left operand
(which catches it itself), so `(xs[i] else 0) else 1` compiles, pointless as
the outer `else` is; a user function's call does not count, whatever its
body holds. Order of errors: the left operand is resolved first, then
`else needs a lookup...` is checked (at the `else`), then the right operand
is resolved, so `z else 1` is `unknown variable z` and `1 else z` is the
`else` error. Which `else` catches a miss: the innermost one whose *left*
operand it is written in; a lookup in an `else`'s right operand belongs to
the `else`s around it, so `(a[0] else b[1]) else 2` catches the miss of
`b[1]` with the outer one. Parsing: the right operand is a prefix-minus
expression (`xs[9] else -1` works, `xs[9] else not b` is `expected an
expression, found 'not'`); a newline after `else` is skipped like one after
any binary operator, and one before it ends the statement (`else` there is
`expected a statement, found 'else'`); a statement that is an `else`
expression is `expression statement must be a call`, and one as an
assignment's target is `cannot assign to this`. Code: a lookup in a left
operand is the `dt_try_` form with `goto missN` on a false return, `missN:`
starts the right operand, `doneN:` follows it (labels numbered with the
temporaries; D30), and a function body is compiled with no labels, so
nothing in it is caught; the `missN:` label is written only if some lookup
jumps to it, since an unused label is a warning and D37 makes warnings
errors. The runtime needed no change. Rejected: counting
only lookups no inner `else` catches (a second kind of lookup to track, for
a case no one writes).

## Project

**D47. Step 8 details the spec left open.** *(default; designer, kept)* The examples are
DESIGN.md's six programs unchanged, each with one leading `//` comment of
what it shows, named `fizzbuzz`, `recursion`, `sorting`, `wordcount`,
`routes` and `ledger`. The word count's standard input is a passage of 303
words of plain prose written for it (apostrophes, a capital at the start of
sentences, `--` and quotation marks, so `clean` drops, lowercases and
sometimes empties a word); the model holds the passage and writes the
`.stdin` file, so the program and the model read the same text. The model's
`print` of an interpolated list or map uses the same printed form as `str`
(D24). No example needed a change to the language (D9). Rejected: a model
that reads `wordcount.stdin` back (the file would then be the only
definition of the input, with nothing for `checks.py` to regenerate).

**D45. The runtime is compiled once per C compiler, flags and source,
and cached as `build/rt/HASH.o`.** *(designer, at step 6's review)*
`make test` had grown past six minutes, a third of it compiling
`ditto.c` for each of 1500 builds. The object is written under a
temporary name and renamed, so parallel builds share it safely.
Rejected: a Makefile rule for the object (the driver is what `run` and
the tests both use).

**D8. Golden tests' expected output comes from an independent source,
never from the compiler.** *(designer)* See `t/README.md`.

**D9. Examples bend to the language.** *(designer)* When a port needs a
feature, the example changes or is left out. Rejected: adding to the
language to make a port pass.

**D32. No referee; a model per step.** *(designer)* Each step's
computed outputs come from a Python model in `t/models/` that generates
the test programs and their expected output from the definition. A
referee interpreter would be larger than the compiler's first steps.
Rejected: a referee in `t/referee/` (cost, in a run measured on cost).

**D33. Tests: `t/NNN-name.ditto` with `.expected` and an optional
`.stdin`; step k numbers its tests k00 to k99.** *(designer)* A test's
standard input is `NNN-name.stdin` if it exists, otherwise empty.
`make test` runs the unit tests, the golden tests (in `t/` and
`examples/`) under `cc`, under `clang`, and under clang with
`-fsanitize=undefined,address`, and `t/checks.py`. Rejected: header
comments for stdin (escapes in a comment are harder to read than a
file).

**D37. The golden runs compile with `-Wall -Wextra -Werror` under `cc`
and clang; `t/run.sh` fails loudly if it can't run.** *(default; designer, kept)* The
generated C and the runtime are meant to be warning-free, and a warning
under one compiler is a portability bug under the other. The runner
treats anything but "some test failed" from `xargs` as a runner failure,
not a pass. Rejected: warnings off (D30's ordering bugs hide behind
them); `-Werror` under the sanitizer run (the flags there are the
sanitizer's, per D6).
