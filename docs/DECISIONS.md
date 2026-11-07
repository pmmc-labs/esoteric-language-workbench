# Decision log

What was decided, why, and what was turned down, roughly in the order it
came up. In this run there is no person: the agent is both designer and
builder (`docs/briefs/design-and-build.md`). **designer** means the
agent decided it at design time or on reviewing a step; **experimenter**
means the brief fixed it; **default** means a builder sub-agent took it
without discussion, and it stays *(default)* until the designer rules on
it at review.

An entry has: a number that's never reused, a one-line title in bold,
the attribution in italics, the reason, and `Rejected:` with each
alternative and why it lost. A decision that's later changed stays, with
a note pointing to the entry that changed it.

## Scope

**D1. Strata: a small imperative language in which every variable is a
history.** *(designer)* The name is geology: layers laid down over time,
the old ones still there to be read. One unusual idea (D7) carried far
enough to shape the whole language, on top of a deliberately ordinary
imperative core so that small programs read plainly. Rejected: a
reactive "every assignment is a permanent formula" language (cyclic
formulas for loop counters need a second kind of assignment, and
compiling it to C needs thunks everywhere); values that wear out after N
reads (fun, but FizzBuzz becomes a puzzle, against "usable"); reversed
execution order (a gimmick with nothing to carry it).

**D2. Nothing from an earlier implementation.** *(designer)* The
repository is a template; Strata starts from an empty tree.

**D3. No prelude, no `lib/`.** *(designer)* Three builtins (D21) and the
operators are the whole library; anything else is written in the
program. Rejected: a prelude in Strata (a second compilation unit and a
linking story for a language whose programs are one file).

**D4. Scale: one-file programs of up to a few hundred lines, run once to
completion.** *(designer)* No modules, no input, no performance work.

**D5. Aggressively simple; practical over pure.** *(designer)* Any
feature that adds complexity can be cut or changed.

**D6. TypeScript to C, linked with a C runtime by `cc`.**
*(experimenter)* Node 22 runs the compiler directly with type stripping,
so erasable syntax only: no enums, no parameter properties, no
namespaces. `LANG_CC` overrides the C compiler; the suite passes under
gcc, clang, and clang with `-fsanitize=undefined,address`.

## The core rule

**D7. Every name is a history. A write lays a new layer on top; `@`
reads the name as it was; nothing can change or remove the past.**
*(designer)* What it removes: rebinding (D14), shadowing, aliasing
bugs (histories are immutable and shared, D18), a separate list type
(D10), and freeing (D26). What it costs: memory grows with every write,
and lists come out newest-first. Rejected: histories that can be
rewound in place (`rewind x`), since the past changing is exactly what
the rule forbids and a rewind makes every `@` read position-dependent;
histories on only some variables (`var x` vs `hist x`), two kinds of
name for one idea; a fixed-length history (last N values), which makes
`#` meaningless and lists impossible.

## Language

**D10. Atoms are 64-bit signed integers and immutable byte strings; the
only container is the flat history of atoms.** *(designer)* A history
can't hold a history: writes take the top of their value (D12), so
nesting can't arise. Lists are histories. Rejected: floats (a printing
format and a model for every test, for no example); a boolean type
(1 and 0 do, D20); nested histories (a second level of every rule, and
the printing of trees); a character type (one-byte strings do, D21).

**D11. Every expression evaluates to a history; operators and statements
that need a value take the top.** *(designer)* One kind of expression
result, so `@` and calls compose with arithmetic: `x@1 + 1`, `f(xs@1)`.
Reading the top of an empty history faults (D23). Rejected: two kinds,
values and histories, with an explicit `top`/`all` (every arithmetic
expression grows a keyword, and the distinction is the reader's to
track).

**D12. `let x = e` names the whole history of `e`; `x <- e` lays the top
of `e` on `x`.** *(designer)* `let` is where a name gets its past,
`<-` is how it grows. So `let y = x` gives `y` all of `x`'s past (shared,
not copied), and `let y = x + 0` gives `y` one layer. `x <- e` with `e`
empty faults. Rejected: `let` laying only the top (then a function's
returned list can't be named); `<-` laying the whole of `e` on top
(nesting by concatenation: `x <- x` would double `x`, surprising for
the commonest form).

**D13. `#e` is the depth; `e@k` is `e` with its top `k` layers removed,
for `0 <= k <= #e`.** *(designer)* `@` returning a history (a suffix)
rather than an atom makes one operator serve as both "the value k writes
ago" and "the list below the top", which is what recursion on lists
needs. `k = #e` gives the empty history; `k` outside the range faults
with `@ out of range (index K, depth D)`. Its right operand is a primary
(`x@1`, `x@i`, `x@(i + 1)`); `@` chains left (`x@1@1` is `x@2`).
Rejected: `@` returning an atom plus a separate "rest" operator (two
operators for one idea); negative `k` counting from the oldest layer (a
second indexing convention; `x@(#x - 1)` reads the oldest).

**D14. No form replaces a variable's history; a name is declared once
per function.** *(designer)* The core rule made total: a variable only
grows. `let` of a name already visible in the function (a parameter, or
any enclosing or earlier `let` in scope) is a compile error, `x is
already declared`. `let` inside a loop body declares a fresh variable
each time it runs. Rejected: `x = e` rebinding (rewrites the past);
shadowing in inner blocks (a name would then have two pasts, and `@`
on it would depend on scope).

**D15. A history literal `[a, b, c]` is the history written in that
order: `a` oldest, `c` the top.** *(designer)* Reads as a sequence of
writes, so `let x = [1, 2]` and `let x = [1]` then `x <- 2` agree. Each
element contributes its top; an empty element faults at `[`. `[]` is
the empty history. Rejected: newest first (reads backwards against the
source).

**D16. Syntax: braces for blocks, newlines insignificant, `;` comments
to end of line.** *(designer)* Every statement starts with a keyword or
a name, and no expression continues with a name, so statements need no
terminator. `;` matches the golden-test header convention
(`t/README.md`). Expression statements are calls only. Rejected:
significant newlines (lexer state for no gain); `#` comments (`#` is
depth); `--` comments (collides with `a--b`).

**D17. Control: `if`/`else if`/`else` and `while`. No `for`, no
`break`.** *(designer)* `while` with a counter covers every example.
Rejected: `for i in a..b` (a second loop form whose counter would grow a
history like any other: no gain over `while`); `break`/`continue` (use
a condition or a function's `return`).

**D18. Functions: top level only, hoisted, not values; they see only
their parameters and their own locals; arguments are passed as whole
histories; a function's result is the history `return` names, or `[]`
if it ends without one.** *(designer)* Passing histories lets a callee
read the caller's past (`trend(x)` can look at `x@1`), and writing to a
parameter grows the callee's copy, invisible to the caller, because
histories are immutable and shared. Top-level `let`s are the main
program's locals, invisible to functions. Function names and variable
names are separate namespaces (a call looks up functions, a bare name
looks up variables). Defining a builtin's name is an error. Rejected:
globals (a second kind of variable, and shared mutable state the core
rule otherwise avoids); closures and first-class functions (a heap
object and a calling convention for no example); passing only the top
(throws away the feature).

**D19. Integers are 64-bit, checked.** *(designer)* `+ - *`, prefix `-`
and `/` fault with `integer overflow` when the result doesn't fit.
`/` truncates toward zero and `%` has the dividend's sign (C's and
Java's); both fault with `division by zero` on 0, and both fault with
`integer overflow` for the minimum integer by -1 (so `%` agrees with
`/`). An integer literal over 9223372036854775807 is a compile error,
`integer literal out of range`; so the minimum integer can't be written
as a literal, only computed. Rejected: wrapping (silent wrong answers);
bignums (an allocator and a model's worth of work for no example);
floor division (Python's; less familiar to C-family readers).

**D20. Conditions are numbers: zero is false, anything else true.
Comparisons, `and`, `or`, `not` yield 1 or 0; `and` and `or`
short-circuit.** *(designer)* A string as a condition, or as an operand
of `and`/`or`/`not`, faults `expected a number, got a string`. Rejected:
a boolean atom (D10); `and`/`or` returning an operand (needs truthiness
for strings, or a type rule for the result).

**D21. Strings are immutable byte strings. `+` concatenates, comparisons
are bytewise, and three builtins do the rest: `len(s)`, `at(s, i)`,
`str(n)`.** *(designer)* `len` is the byte count; `at(s, i)` is the
one-byte string at 0-based `i`, faulting `index out of range (index I,
length N)`; `str(n)` is the decimal form of a number. `+` and the six
comparisons need both sides the same kind, else `mismatched types:
number and string` (kinds in operand order). `- * / %`, prefix `-`, an
`@` index, `at`'s index and `str`'s argument need a number, else
`expected a number, got a string`; `len` and `at`'s first argument need
a string, else `expected a string, got a number`. Literals: `"..."` with
escapes `\n \t \" \\`; any other escape is a compile error, `unknown
escape \c`; a newline or end of file before the closing quote is
`unterminated string`. Rejected: strings as histories of characters
(tempting for the core rule, but then a string is a container, printing
needs a rule for histories, and `+` on histories needs a meaning);
character codes (`ord`/`chr`; no example needs them); `num(s)` (no
input to parse).

**D22. `print e` prints the top of `e` and a newline; `write e` prints it
without one.** *(designer)* Numbers in decimal with a leading `-` when
negative, strings as their bytes. An empty `e` faults. Rejected:
printing a whole history (needs a format, and nesting rules, for what a
four-line loop does); `print` with several arguments (`+` and `str`).

**D23. A fault flushes stdout, prints `fault at L:C: message` to stderr,
and exits 1.** *(designer)* `L:C` is the 1-based line and byte column of
the operation that needed the value: the operator token for operators
(`+`, `@`, `and`, prefix `-`...), the keyword for `print`, `write`,
`if`, `while`, the `<-` token for a write, the `[` for a history
literal, the name for a builtin call or for the call that exceeds the
depth limit. The messages, the whole list: `empty history`, `@ out of
range (index K, depth D)`, `integer overflow`, `division by zero`,
`expected a number, got a string`, `expected a string, got a number`,
`mismatched types: number and string` (or `string and number`), `index
out of range (index I, length N)`, `recursion too deep`, `out of memory`
(the last with no position: `fault: out of memory`). Rejected: a stack
trace (the position is enough at this scale); exit codes per fault
(nothing reads them).

**D24. A compile error prints `error at L:C: message` to stderr and
exits 2; only the first error is reported; no binary is written.**
*(designer)* No file name, so expected outputs don't depend on the path
a test was run by. Messages: `unexpected character 'c'`, `unterminated
string`, `unknown escape \c`, `integer literal out of range`, `expected
THING, found TOKEN` for every parse error, `unknown variable x`, `x is
already declared`, `unknown function f`, `f is already defined`, `f is
a builtin`, `f takes N arguments, given M` (`1 argument` when N is 1),
`return outside a function`. Rejected: several errors per run (recovery
is machinery); warnings (nothing to warn about yet).

**D25. Evaluation is left to right: operands, arguments, list
elements, the `@` base before its index.** *(designer)* The compiler
puts every subexpression in a fresh C temporary in source order, so C's
unspecified argument order can't leak into behaviour
(`docs/PROCESS.md`, "The person's machine"). `and`/`or` evaluate their
right side only when needed. Rejected: C expressions nested directly
(the gcc/clang argument-order bug the process doc records).

**D27. Calls nest at most 10000 deep; the call that would be the
10001st active one faults `recursion too deep` at its name.**
*(designer)* A counter, not a guard page: portable, and it fires before
the sanitizers' larger frames overflow the C stack. Rejected: no limit
(a segfault is not a fault message); a limit from an environment
variable (no test needs it).

**D28. No input: no stdin, arguments, environment, clock or random
numbers.** *(designer)* Programs are closed, so every run is
deterministic and the template's virtual clock, seeds and record/replay
have nothing to do. Rejected: reading stdin (would want `num`, line
splitting, end-of-input rules; no example needs it).

## Values and memory

**D26. Memory is never freed: layers and strings come from an arena of
1 MiB chunks, chained from a global.** *(designer)* The core rule means
nothing is ever overwritten, so a collector would only find dead loop
temporaries; at D4's scale that's affordable. Chaining the chunks from a
global keeps LeakSanitizer quiet. A request the allocator can't meet
faults `fault: out of memory`. Rejected: reference counting (every
temporary needs a release, in generated code); a collector (roots in C
locals need a shadow stack).

## Compiler

**D29. The compiler is pure functions over plain-object ASTs, no
classes; one file per pass: lexer, parser, resolve, codegen, errors,
main.** *(designer)* Nodes are tagged unions (`{k: "bin", op, l, r,
line, col}`); environments are arrays or maps passed down, not mutated
across passes. 2-space indent. Errors are thrown as a plain object and
caught once in `main.ts`. Rejected: classes and visitors (the shape
that makes a later self-host a rewrite).

**D30. The driver: `bin/strata build FILE -o OUT` (exit 0, or 2 on a
compile error) and `bin/strata run FILE` (compile to `build/`, run,
pass the program's exit code through).** *(designer)* `bin/strata` is a
shell script calling `node compiler/src/main.ts` for C, then
`${LANG_CC:-cc} -std=c11 -O1 $LANG_CFLAGS` with the runtime. C11 with
no extensions so gcc and clang accept the same code. The C compiler runs
with `-w`: its warnings on generated code would land in a golden test's
output. If `cc` itself fails, that's a compiler bug: the driver prints
`internal error: cc failed` with cc's output and exits 3. Rejected: GNU
statement expressions (codegen with temporaries doesn't need them).

## Project

**D8. Golden tests' expected output comes from an independent source,
never from the compiler.** *(experimenter)* See `t/README.md`. By hand
for a few obvious lines; from a Python model in `t/models/` for anything
with arithmetic edge cases or more than a screen of output.

**D9. Examples bend to the language.** *(experimenter)* When a port
needs a feature, the example changes or is left out. Rejected: adding
to the language to make a port pass.

**D31. Golden tests are numbered by step: step n's are `n00` up
(`t/000-...` for step 0, `t/100-...` for step 1).** *(designer)* A test's
number says which step brought it. Examples in `examples/` are named,
not numbered. Source files end `.strata`.

**D32. Each step's tests and models are committed red before its code,
in their own commit; the code commit makes them green.** *(experimenter)*

## Step 0 defaults

**D33. A parse error is `expected THING, found TOKEN`, where THING is
`statement` or `expression` and TOKEN is the offending token's source
text in single quotes, or `end of file`, at that token's position (the
end of file is the line and column just past the last byte).**
*(default)* D24 fixes the shape but not the words. Naming the grammar
class rather than the one form that happens to be legal in step 0
(`integer`) means the messages in tests `004` and later don't change as
forms arrive. Rejected: `expected integer` (stale at step 1); quoting
token kinds (`found name`) rather than text (says less); a list of
every token that could have appeared (machinery).

**D34. Lexer details D24 leaves open.** *(default)* The source is read
as latin1, one character per byte, so columns are byte columns. All of
the file is lexed before parsing, so a lexical error anywhere is
reported ahead of an earlier parse error. An unterminated string is
reported at its opening quote; an unknown escape at its backslash. A
byte that is not printable ASCII is shown as `\xHH` in `unexpected
character`. `integer literal out of range` is checked in the lexer
(from step 0, though PLAN.md lists it under step 1), at the literal's
first digit. Rejected: lexing on demand (a streaming lexer for a
first-error rule that costs nothing now); decoding UTF-8 (columns
would stop being bytes); leaving the range check to step 1 (the
lexical-error unit tests of step 0 want all four of D24's).

**D35. The runtime's shape for step 0.** *(default)* `strata.h` defines
the atom (`is_str` and a union of `int64_t` and a string pointer), the
layer `{atom, below, depth}` and `strata_hist` as a `const` pointer to
a layer, NULL for empty. Generated code is one `int main(void)` of
temporaries and `strata_*` calls, each taking the source `L, C` it can
fault at; `strata_print` takes a history and prints its top (faulting
`empty history` on NULL) so `print` is already D22. The compiler writes
`OUT.c` next to the binary and `bin/strata` keeps it. Arena requests
larger than a chunk get a chunk of their own. Rejected: a `main`
that calls generated `strata_main` (nothing needs the split yet);
deleting the C file (a failing sanitizer run is easier to read with it).
