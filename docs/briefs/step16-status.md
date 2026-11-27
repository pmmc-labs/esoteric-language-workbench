# What CLAUDE.md's Status section should gain for step 16

Written by the session that built step 16 in a worktree beside steps 13
to 15 (branch `step16`), which was told not to edit CLAUDE.md. Paste
the paragraph below into the Status section, in its style, when the
branch is merged; the numbers of golden tests and claims are this
branch's own and move with the merge.

---

**Step 16, strings the rest, is built in three sub-steps, pulled ahead
of 13 to 15 and built beside them** (2026-11-27, by Fable 5.2, in a
worktree of its own; D120 to D131, each the recommendation by Stevan's
standing instruction; `docs/PLAN.md`, step 16, has the proposal, its
review and "16, as built"; `docs/LANGUAGE.md`, "q, qq, qw and
heredocs", "ucfirst, lcfirst and rindex", "chomp and chop", "sprintf and
printf"; T260 to T284; `briefs/claims16.py`, which `claims.py` reads).
**16a**: `q`, `qq` and `qw` with one of the four brackets hard against
the word, the string ending where perl's ends (brackets nest, a
backslash takes the next character); `qq` is double quotes whole, but a
backslash before its own bracket is refused (T278: perl takes it away
before it interpolates); **`qw` is a token the parser reads as a
bracketed list** (T260: `qw(a b)[1]` is a slice, `for my $x qw(a b)` is
refused as perl refuses it); heredocs `<<"END"`, `<<END`, `<<'END'`, each
with `~`, one on a line, nothing on that line going past its end
(T264), `'END'` keeping every backslash (T262), `~` refusing a line that
does not begin with the terminator's blanks (T263). The lexer does it
all with new functions of its own (`closing`, `body`, `quoteLike`,
`hereDoc`), calling 11a's `escape` and `variable`; the oracle check's
reading rule learned the four (fixtures both ways). **16b**:
`sprintf(FORMAT, LIST)`, a value as `join` is, and `printf(FORMAT,
LIST);`, a statement as `print` is; **the format is a string literal
with no variable in it** (D124, T22), read by `compiler/src/format.ts`;
fifteen conversions, five flags, widths, precisions and stars (D125);
**the count is checked, a fault both ways** (D126); a value past what
perl converts exactly (`%d` outside the Ints, the unsigned ones outside
-2^63 to 2^64), a negative zero, Num or string, to `%e %f %g` (T267,
T282), undef: faults (D127). `runtime/format.c` counts and then writes,
one allocation; integers by hand (macOS has no `%b`), floats through
`snprintf` but **a bare `%.0f`, which is perl's own `F0convert`**
(T280). **16c**: `ucfirst`, `lcfirst` (named unary, a first character
past ASCII a fault), `rindex` (perl adds the piece's length to the
position before clamping, T281; a sum past the Ints a fault), and
**`chomp` and `chop` as statements on one scalar variable**, built as
the variable assigned what `rt_chomp`/`rt_chop` make of it in a block of
its own, so that they are no value anywhere (D130); `chomp` leaves a
number (T279), `chop` makes the string. `runtime/strfn.c`. **The
review** (`briefs/step16-review/`, a separate Claude Code process run
from the command line, since the session had no agent tool) found five
ways to be WRONG, each answered in D131. Tests: 2600 to 2603 from
`t/models/quote.py`, 2620 to 2656 refusals (`briefs/step16a-refusals.py`);
2700 to 2703 from `t/models/fmt.py`, 2720 to 2746 faults and 2760 to
2790 refusals (`briefs/step16b-tests.py`), and the 2^31 limit from C
(`runtime/tests/format.c`); 2800 and 2801 from `t/models/strfn.py`, 2820
to 2828 faults and 2840 to 2854 refusals (`briefs/step16c-tests.py`).
Broken on purpose (`briefs/step16-mutations.py`): 77 of 83 caught the
first time, three holes closed, three breakages nothing can see. **The
census**: of the 130 probes that waited, 64 are SAME now, 7 LOUD, 30
moved to `by-design/`; 1,083 SAME, 131 LOUD, 2,019 REFUSED, 1 UNJUDGED
of 3,234 run on this branch, no WRONG. **Left as 16d** (D120): the case escapes, `substr` of four
arguments, `reverse` of a string where one value is wanted,
`__FILE__`/`__LINE__`, POD, `printf` to a handle (21), `uc`/`lc` past
ASCII. **What a merge meets**: the lexer's new branches sit before its
word branch and its operator branch, and one check at the top of its
main loop; `Token` gained `qw`; the parser gained a `qw` case in
`primary`, a `changer` case in `simple` and one refusal; `names.ts`
gained `printf`, `sprintf`, `ucfirst`, `lcfirst`, `rindex`, `chomp`,
`chop` and the `changer` kind; `checker.ts` two calls of `checkFormat`
and `sprintf` beside `join` in the contexts; `codegen.ts` two lines;
`rt.c` two `#include`s at the end, `rt.h` eight declarations.
