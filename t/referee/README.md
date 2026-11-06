# Referees

A second implementation of the language from the decisions, an
evaluator that prints what any program's `.expected` must be, run over
every golden test by `t/checks.py`: it must print the `.expected`, or
exit 3 to say the program is outside what it covers (a program the
compiler must refuse, say), which is skipped. The builder of a step
doesn't read these files (`docs/PROCESS.md`, "The referee"), but runs
`make checks` for their verdicts.

- `calc.py`: the calculator, from D1 to D4 and D8 to D15, written with
  step 1's proposal. A step that adds a form extends it before the
  step's builder starts.
