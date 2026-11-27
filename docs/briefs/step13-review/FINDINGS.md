# Review of step 13's proposal: references and nested data

By a reader who did not write the proposal (a sub-agent, 2026-11-27),
with perl 5.42.0 run plain. 315 programs in the `.t` files here, each
with perl's output in the `.out` beside it; `sh run-all.sh` reruns
them, `probe.py` runs one file, `curly-now.sh` runs 8 programs under
perl and the compiler as it was. The reviewer's report was handed
back as text and is summarized here by the lead; the programs and
perl's outputs are the reviewer's own files.

Three ways to be WRONG, one unclear place where one guess is WRONG,
three shapes perl refuses and the proposal took, five gaps. What was
done about each: `docs/PLAN.md`, step 13, "What the review found",
and D114. The traps are T249 to T256 in `docs/TRAPS.md`, each with a
row in `claims.py`.

- **W1** (`viv.t`, `loopvar.t`, `order.t`): a store that makes a hop
  assigns whatever held the undef; perl reads that late (T249), and
  through a loop variable the made array lands in the list (T250).
- **W2** (`freed.t`, `freed2.t`): `map`, `grep`, `sort`, and a `for`
  over more than one array, walk values perl has freed when the
  block drops the last reference (T251).
- **W3** (`viv.t`): storing through an undef that is no variable or
  element dies in perl (T252).
- **U1** (`strings2.t`, `strings3.t`): what follows `${ EXPR }` and
  the postfix forms in a string (T253).
- **P1 to P3** (`parse*.t`): `{` first in `say(`, `{` first in a
  dereference's braces, a word alone in any brace form (T254).
- **G1 to G5**: the order of making (agrees with perl; `order.t`),
  a file variable's cell (T255, `filevar.t`), `defined` of a whole
  container (T256), a number first in a statement's `{`, slices
  through a reference among a call's arguments.
- **What stood**: D109 for names (`concat.t`, `interp.t`,
  `aassign.t`), the in-place sort (`sort.t`), D112 (`scalar.t`),
  13c's cells, D113 where a value may begin, 13d's chains
  (`strings.t`), and all 18 of the proposal's claims.
