# Referees

A second implementation of the language from the decisions, an
evaluator that prints what any program's `.expected` must be, run over
every golden test by `t/checks.py`. A program outside what it covers
exits 3 and is skipped.

- `calc.py`: the calculator, from step 0's rules and D20 to D28. It
  prints a fault's line and `exit: 1` as `t/run.sh` shows them, since the
  check compares stdout.

The builder of a step doesn't read these (`docs/PROCESS.md`, "The
referee").
