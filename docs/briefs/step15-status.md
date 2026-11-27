# What CLAUDE.md's Status section should gain for step 15

Written by the session that built step 15 in a tree of its own (branch
`step15`), which was told not to edit CLAUDE.md; to be merged into the
Status section by hand, in its style.

---

**Step 15, `die`, `try`, `catch`, is built** (2026-11-27, pulled ahead
of 13 and 14, which were built in another tree at the same time; D140
to D151, the builder's recommendations under Stevan's standing
instruction; `docs/PLAN.md`, step 15, has the proposal, its review and
"15, as built"; `docs/LANGUAGE.md`, "die, try and catch"; T300 to T320;
83 rows of `claims.py`, 941 in all). **`die LIST`** makes perl's message
byte for byte (the values joined with nothing between, `Died` when
empty, ` at FILE line N.` when it does not end in a newline, N by D34)
and throws it; uncaught, it is written to stderr after stdout and the
exit is 255 (D12), a test of kind `dies`. It is a list operator and a
value anywhere but tested or first (D146: perl warns), and `$x or die
...;` is refused as D56 refuses every statement joined by a word
operator. **`try BLOCK catch ($e) BLOCK`**, a statement; `return`,
`last` and `next` in either block do what they do anywhere; a die in a
catch goes out one; **a fault is never caught** (D13); a sub that ends
in a `try` has no value (D18, T65). `...` is `die "Unimplemented"`
(D145). `finally` and `defer` are refused until step 21 (D144); a `#
line N` comment is refused (D147). **The review found three WRONGs**:
perl names a line of its lexer's choosing for a statement over several
lines and the last statement run for a `while`'s test (T316, T317), so
a `die` or `warn` whose message is not written to end in a newline is
refused there (D150); and perl exits with `$!`, ERANGE, after a string
read as a number or a `**` underflowed (T319), so an uncaught `die`
after one faults (D151). **15b**: `warn LIST` (its value `true`), `say
STDERR LIST;` and `print STDERR LIST;`; **`t/run.sh` keeps stdout and
stderr apart, stdout first**, and a test that writes to stderr and ends
normally is of the new kind **`warns`** (D149); for `dies` and `warns`
the oracle runs perl once more with `t/oracle/Warned.pm`, which marks
every warning not from the program's own `warn`, which closes the hole
"The checks themselves" kept for step 15; a fault test's stderr before
its fault must be the start of perl's. **In the runtime**
(`runtime/unwind.c`) unwinding is `setjmp` and `longjmp` (D141): a `try`
notes the frames, the depth, the sorts and how many freezes are held
(the freezes are now also a stack in the context, kept by `rt_freeze`
and `rt_thaw`), and a `die` puts each back; the thrown value goes
through the context, never a C local; the generated code's list of
what every way out does (`open`) closes a `try` for `return`, `last`
and `next`. **A merge with 13 must decide what `die $ref` throws**: the
runtime faults on a value that is not a scalar until then (D142).
Tests: 3000 to 3004 by hand, 3010 to 3016 from `t/models/die.py`, 3050
to 3065 `dies`, 3080 to 3095 faults, 3100 to 3148 refusals from
`briefs/step15-refusals.py`, 3200 to 3203 `warns`, and
`runtime/tests/unwind.c`; 1,350 golden tests and 149 unit tests.
Broken on purpose (`briefs/step15-mutations.py`): 52 of 58 caught the
first time, five holes closed, one breakage nothing can see. Green
under gcc, clang, and UBSan with ASan. The reviewer was an independent
session given only the proposal and perl; its report is summarised in
`PLAN.md`, "What the review found" (the session that built the step had
no way to save the report as a file). The census: of the 19 probes that waited for step 15, 17 use `eval`, which D20 cut, and moved to `by-design/` (2,334 there now, with the one below); `warn` alone came through (`io8`), and one that printed to `STDERR` (`bl-h2`), which had waited for step 21; `rl-q5`, the one probe with a `try`, is refused for its `no warnings;`. One probe with a `# line` directive is refused by design now (D147). **1,021 SAME, 124 LOUD, 1 UNJUDGED, no WRONG**, and no probe left SAME.
