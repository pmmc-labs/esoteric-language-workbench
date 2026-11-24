**D31. Strings: a third type of value, a sequence of Unicode scalar
values, written `"..."`.** *(Default, Claude's, written for the
interpreter experiments the person asked for, to check what is
particular to an interpreter; fair to revisit.)* A string's length,
indexes and order are its code points', never its encoding's: `"😀"`
is one long, `"e\u{301}"` (an `e` and a combining accent) two, and
nothing is normalised, so `(== "é" "e\u{301}")` is `#false`. In a
literal, `\"`, `\\`, `\n` and `\t` are themselves, and `\u{X}` is the
code point X, one to six hex digits; any other character stands for
itself. Each of these is an error before running (D28): a literal with
no closing `"`; a newline inside a literal (write `\n`); a backslash
before anything else; a `\u{X}` that is empty, longer than six digits,
not hex, a surrogate (D800 to DFFF) or past 10FFFF. A tab or a
carriage return inside a literal stands for itself; only a line feed
is refused. The source is UTF-8, and a file that isn't valid UTF-8 is
an error before running. White space is a space, a tab, a line feed or
a carriage return, and nothing else: not U+00A0, not a form feed, not
U+FEFF, so a file that begins with a byte order mark begins with an
unknown name. A `"` ends a name or an integer as a bracket does, so
`(str/len"a")` reads as `(str/len "a")` and `"a""b"` as two literals.
Integers are still ASCII digits.
A position's column (D28) counts code points from 1, so on a line
after `"😀"` a form's column is the same whatever the encoding takes
for it. Rejected: UTF-16 code units, JavaScript's (a character past
U+FFFF would count two and could be cut in half); bytes, UTF-8's
(every character past ASCII would count more than one); grapheme
clusters (they need the Unicode tables, and change with Unicode's
versions); normalising (the same).

**D32. A string prints in double quotes: `"` and `\` with a backslash
before them, a newline as `\n`, a tab as `\t`, any other code point
below U+0020 and U+007F as `\u{X}` (lowercase hex, no leading zeros),
and every other code point as itself, in UTF-8: the C1 controls (U+0080
to U+009F), U+2028 and U+2029 too.** *(Default, Claude's,
as D31.)* So what a string prints reads back as the same string:
`(str/char 7)` prints `"\u{7}"`, and `"é"` prints `"é"`. stdout is
UTF-8. Rejected: printing a string bare (the value `"#true"` and the
value `#true` would print alike); JSON's escapes (`\u0007`, and
surrogate pairs past U+FFFF, which aren't this language's escapes);
escaping everything past ASCII (unreadable for a person, and the
tests would say nothing about printing UTF-8).

**D33. Six string operators: `(str/len s)`, `(str/at s i)`, `(str/cat
a b)`, `(str/lt a b)`, `(str/code s)` and `(str/char n)`.** *(Default,
Claude's, as D31.)* `str/len` is the number of code points.
`str/at` is the code point at index `i`, from 0, as a string of one;
an index outside 0 to one less than the length faults `bad index`.
`str/cat` is `a` followed by `b`. `str/lt` is `#true` when `a` sorts
before `b`, comparing code point by code point, and a string before any
longer one it begins: so `(str/lt "\u{FFFF}" "\u{10000}")` is `#true`.
`str/code` is the code point of a string of one, as an integer; a
string of any other length faults `not a character`. `str/char` is the
string of one for a scalar value; an integer that isn't one (negative,
a surrogate, past 10FFFF) faults `not a character`. `str/len`,
`str/code` and `str/char` take one operand and the others two, which
amends D3 for these six: a different count is an error before running,
`str/len takes 1 argument, not 2`. An operand where a string is wanted
that isn't one faults `not a string`; `str/at`'s index and `str/char`'s
operand, where an integer is wanted, fault `not an integer`. Operands
are checked left to right, each for its type, and then the index or
code point for its range, so `(str/at 5 #true)` faults `not a string`
and `(str/at "ab" 7)` `bad index`. Each of the six is one operation for
a budget (D21), charged after its operands and before its checks (D22).
The seventeen operators given a string fault `not an integer`, as they
do a boolean (D11), except `==` and `!=`, which compare two strings by
their code points (D12). Rejected: `str/len` as two operands, to keep
D3 whole (a second operand with no meaning); ordering strings with `<`
and the rest (D12 keeps them to integers, and a separate name says
which order); comparing by UTF-16 code units, JavaScript's `<` (it puts
`"\u{10000}"` before `"\u{FFFF}"`).

