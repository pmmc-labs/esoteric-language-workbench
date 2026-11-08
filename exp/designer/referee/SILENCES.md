# Silences

These are the places where `docs/LANGUAGE.md`, `docs/DESIGN.md` and `docs/DECISIONS.md`
are silent or ambiguous. For each one: what the documents leave open, what
`referee.py` does, and why. `S<n>` tags in the code mark where each choice is made.
If the referee and the compiler disagree on one of these, the documents don't decide
it. The disagreement isn't a bug in either until the designer rules.

**S1. Empty statements.** The docs say `;` ends a statement, but not whether `;;`, a
leading `;`, or `{ ; }` is allowed. *Chosen:* `;` is accepted only after a
statement. Anywhere else it is `expected a statement, found ';'`. *Why:* the docs
describe `;` as a terminator, and D36 says a statement starting with a token that
can't begin one is `expected a statement`.

**S2. How an unknown escape shows a byte that isn't printable.** The docs give
`unknown escape '\q'` but don't say how a control byte or a UTF-8 byte after `\` is
shown. *Chosen:* the raw byte goes between the quotes. *Why:* this is the simplest
option, and the docs leave non-ASCII bytes raw everywhere else.

**S3. `//` inside an interpolation.** *Chosen:* the comment runs to the end of the
line, so the interpolation is `unterminated interpolation`, at its `{`. *Why:* a
comment runs to the end of the line, and an interpolation that reaches the end of
the line is unterminated (D35).

**S4. What counts as a call.** *Chosen:* only a name followed directly by `(`. So
`(f)(x)` and `xs[0](1)` are not calls: `(print)(1)` on its own line is
`expression statement must be a call`. A parenthesized call, `(print(1))`, is
still a call (D38). *Why:* functions are not values (D13), so only a name can be
called.

**S5. A newline after `..` or `..=` in a `for` header.** *Chosen:* it is skipped, as
after a binary operator. *Why:* the range operator works like a binary operator.

**S6. Which error comes first when an expression statement is followed by junk.**
For example `x y`. *Chosen:* the expression-statement check runs before the
terminator check, so it is `expression statement must be a call` at `x`, not
`expected newline, found 'y'`. *Why:* D39 reports a bare name on its own line as the
expression-statement error, and this reports the leftmost problem.

**S7. A newline between a statement's `else` and its `{` or `if`.** *Chosen:* it is
skipped. *Why:* D11 and LANGUAGE.md list "after `else`" among the places where a
newline doesn't end a statement, without limiting it to expressions. A newline
before the block of `if`, `while`, `for` or `fn` is still `expected '{', found
newline`.

**S8. A name that is both a function and a top-level variable, used inside a
function where it isn't local.** *Chosen:* `functions are not values`. That check
comes before the top-level-variable message. *Why:* this is an arbitrary order. It
is rare.

**S9. Assigning to a function's name when no variable has that name.** For example
`f = 1`. *Chosen:* the same check as a read, giving `functions are not values`
(or `unknown variable`). *Why:* one lookup routine. LANGUAGE.md says "reading or
assigning" for `unknown variable`.

**S10. The order of a `for` loop variable's duplicate check and errors in the
header's expressions.** *Chosen:* the duplicate-name check comes first, then the
iterable or bounds are resolved, then the variable is declared. *Why:* source order
(the name comes before the expression). D39 does the same for `let`.

**S11. Which operator a compound-assignment fault names.** LANGUAGE.md says
`+=` and the others apply "the operator ... as in an expression", with faults
pointing at the `+=`. *Chosen:* the message names the bare operator, as in
`cannot use + on string and int`, at the `+=`. *Why:* this is "as in an
expression", with only the position changed.

**S12. The exact sort algorithm.** D43 fixes the stable merge sort, which puts the
right item first only when it is strictly less, so the pair compared is (later,
earlier). It doesn't fix the split, which decides which uncomparable pair is
reported first (`sort([1, "a", nil])` and similar). *Chosen:* a top-down merge sort
whose left half is the first `len // 2` items, with left recursion first.
*Why:* this is the textbook form, and it matches the documented
`sort([1, "a"])` example.

**S13. `not` as the operand of a tighter operator.** For example `1 == not x` or
`1 + not x`. *Chosen:* `expected an expression, found 'not'`. *Why:* the precedence
table puts `not` at level 3, so a comparison or arithmetic operand can't start with
it. `not not x` is fine.

**S14. Bad usage or an unreadable file.** *Chosen:* a plain message and exit 2,
the same as the compiler's bad usage (D31). *Why:* the docs don't give a message.

**S15. Which bytes are "printable ASCII" for `unexpected character`.**
*Chosen:* 0x21 to 0x7E. Space never reaches this check. DEL, control bytes
(including VT and FF) and every byte from 0x80 up are `unexpected byte 0xNN`. A
non-ASCII byte right after a name ends the name and is itself the error. *Why:*
these are the usual definitions.

**S16. Newlines "anywhere between" a map literal's braces.** *Chosen:* this is taken
literally. Every newline token is ignored while parsing the literal, including
inside a value's expression, so `{a: 1` newline `+ 2}` is `{"a": 3}` and `-`
newline `3` is a key. *Why:* this follows the wording of D44.

**S17. Lex errors and parse errors.** *Chosen:* the whole file is lexed before
parsing, so a lexer error anywhere is reported before a parse error earlier in the
file. Likewise all parse errors come before any resolver error. *Why:* DESIGN.md
describes these as separate passes.

**S18. When `else needs a lookup` is checked relative to errors in its operands.**
*Chosen:* the left operand is resolved first, then the lookup check runs (at
`else`), then the right operand is resolved. *Why:* this gives source order.

**S19. A `}` of an interpolation and the lexer's bracket stack.** Newlines are
dropped inside `( )` and `[ ]` but kept directly inside `{`. *Chosen:* the lexer
keeps a stack of `( [ {` and drops a newline only when the innermost open bracket
is `(` or `[`. A stray closer with nothing open is ignored. Interpolation braces
never touch the stack, because an interpolation can't hold a newline. *Why:* this
is the plain reading of DESIGN.md's lexer description.

**S20. `int` and leading zeros or `-0`.** *Chosen:* `int("007")` is 7,
`int("-0")` is 0, and `int("-9223372036854775808")` is the smallest int. *Why:*
the docs say "an optional `-` and one or more decimal digits, in range". They don't
forbid leading zeros.

**S21. Assigning to a `for` loop variable inside the body.** *Chosen:* this doesn't
change the iteration. The range walks its own counter and the next round rebinds
the variable. *Why:* "declared fresh in each iteration" and D40's counter.

**S22. Arity wording for zero.** *Chosen:* `read takes 0 arguments, got 1`. *Why:*
the docs only special-case one (`1 argument`).

**S23. A builtin's name with a variable of the same name in scope, called.** For
example `let print = 1` then `print(print)`. *Chosen:* the call goes to the builtin
and the argument is the variable. A variable's name used as a callee is
`unknown function x`. *Why:* D39 says variables and functions are separate
namespaces.
