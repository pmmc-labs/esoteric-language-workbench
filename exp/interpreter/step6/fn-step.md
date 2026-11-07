### 6. Functions, tail calls and depth (to build)

Size: medium. D31 to D34 decide it; every test is written and agrees
with the referee, extended for this step. Referee: `t/referee/calc.py`,
extended for D31 to D34 before the build, by someone other than the
model's writer; wanted because the depth's edge and the charge's order
are traps a mirror of the interpreter would copy.

- Definitions and calls (D31): the reader and checker take a program of
  definitions and then one expression; every error D31 lists is an
  error before running (D28), each a unit test in `interp/tests/`.
- Calls (D32): arguments left to right, the charge, the depth's check,
  the body.
- Tail calls (D33): a call in tail position runs in constant space.
- Depth (D34): 10,000 calls in progress, the next faulting `stack`,
  the same under both Nodes.
- Tests 070 to 089, written already, from `t/models/fn.py`.
  The step is done when they and every earlier step's pass under both
  Nodes, no file under `t/` is changed, and the documents are moved.
- Documents: `LANGUAGE.md` gains a section on functions (definitions,
  calls, tail calls, the depth, the errors before running, `stack`
  among the faults); `DESIGN.md`'s "What the host gives" gains its
  lines for calls, tail calls and depth, before the code, as step 0's
  did; this heading, the progress line, the Status.
- Leave out: functions as values, `lambda`, closures, local
  definitions, `let`, any loop form but a function that calls itself.

