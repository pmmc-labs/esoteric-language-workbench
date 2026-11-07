### 6. Strings (to build)

Size: medium. D31 to D33 decide it; every test is written and agrees
with the referee, extended for this step. Referee: `t/referee/calc.py`,
extended for D31 to D33 before the build, by someone other than the
model's writer; wanted because what a string's length, index and order
are is where a host's own strings differ from the language's, and a
mirror of the interpreter would copy the host.

- Strings (D31): the reader takes string literals and their escapes;
  every error D31 lists is an error before running (D28), each a unit
  test in `interp/tests/`, and a position's column counts code points.
- Printing (D32).
- The six operators (D33), their faults, and `==` and `!=` on strings.
- Tests 070 to 089, written already, from `t/models/strings.py`. The step is done when they and every earlier step's pass under
  both Nodes, no file under `t/` is changed, and the documents are
  moved.
- Documents: `LANGUAGE.md` gains a section on strings (literals and
  escapes, printing, the six operators, their faults); `DESIGN.md`'s
  "What the host gives" gains its lines for strings, before the code,
  as step 0's did; this heading, the progress line, the Status.
- Leave out: string ordering with `<`, case, normalising, graphemes,
  conversions between strings and integers, any operator D33 doesn't
  name.

