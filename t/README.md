# Golden tests

`NNN-name.ditto` is a program and `NNN-name.expected` is what it must
print: stdout and stderr together, in order, plus a last line `exit: N`
when the exit status isn't 0. Numbers are never reused. `run.sh`
compiles one, runs it with `NNN-name.stdin` as its standard input if
that file exists (otherwise empty input), and diffs. Step k numbers its
tests k00 to k99 (D33). A compile error's output is the compiler's
standard error and `exit: 2`.

## Where expected output comes from

**Never from the compiler.** It's worked out by hand, or by a model in
`models/`. Running the compiler and saving what it printed freezes a bug
as the spec, and every later failure becomes an argument about which
side is wrong.

By hand is fine when the output is obvious: a few lines a person can
check by reading the program. Anything with arithmetic edge cases,
floating point, hashing, dates, scheduling order, encodings or more than
a screen of output comes from a model.

When a change moves an output a model wrote, **rerun the model**. Don't
patch the file.

## Determinism

Ditto has no clock, randomness, concurrency or environment, so a
program's only input is its standard input, and every run is the same.

## Kinds of test

- `t/`: the golden tests. Each plan step adds some.
- `examples/`: programs, each with a `.expected` a golden test too.
- `compiler/tests/`: unit tests per pass (`node --test`), for what a
  golden test can't reach (the lexer's positions, token streams).
- `t/checks.py`: every test has its `.expected`, and every model's
  files regenerate unchanged.
