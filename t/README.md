# Golden tests

`NNN-name.smol` is a program and `NNN-name.expected` is what it must
print: stdout and stderr together, in order, plus a last line `exit: N`
when the exit status isn't 0. Numbers are never reused. `run.sh` runs one
through the interpreter and diffs.

No header lines are read yet. A test that needs standard input, arguments
or an environment brings its own header with the feature that needs it.

## Where expected output comes from

**Never from the compiler.** It's worked out by hand, or by a model in
`models/`. Running the interpreter and saving what it printed freezes a
bug as the spec, and every later failure becomes an argument about which
side is wrong.

By hand is fine when the output is obvious: a few lines a person can
check by reading the program. Anything with arithmetic edge cases,
floating point, hashing, dates, scheduling order, encodings or more than
a screen of output comes from a model.

When a change moves an output a model wrote, **rerun the model**. Don't
patch the file. `make checks` reruns every model and fails on a file
that differs, so a patch doesn't survive `make test`.

## The referee

`referee/` will hold a second implementation of the language, written from
the decisions, that prints what any program's `.expected` must be. None
yet: the first step whose proposal says `Referee: ...` writes one.
`make checks` runs every referee over every test. It is what a model
written by someone else is judged against, so the builder of a step
doesn't read it (`docs/PROCESS.md`, "The referee").

## Determinism

None of the knobs exist yet: no clock, no seed, no heap cap. `run.sh` sets
each one when the interpreter gains it. A test runs the same way every
time or it isn't a test.

## Kinds of test

- `t/`: the golden tests. Each plan step adds some.
- `compiler/tests/`: unit tests, for what a golden test can't reach: the
  reader's positions, the messages of syntax errors, the evaluator's
  internals.
