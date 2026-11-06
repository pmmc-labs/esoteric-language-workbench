# Referees

A second implementation of the language from the decisions, an
evaluator that prints what any program's `.expected` must be, run over
every golden test by `t/checks.py` (`docs/PROCESS.md`, "The referee").

- `calc.py`: the calculator, from D3, D4 and D8 to D13, written with
  step 1's proposal. A program outside it (a form no decision has
  given it, a compile error, a header) exits 3 and is skipped.
