# Golden tests

`NNN-name.ext` is a program and `NNN-name.expected` is what it must
print: stdout and stderr together, in order, plus a last line `exit: N`
when the exit status isn't 0. Numbers are never reused. `run.sh`
compiles one, runs it with the environment every test assumes (the
virtual clock, a fixed seed and epoch, the heap cap, the collector's
poison), and diffs.

Header lines a test may carry, as comments at the top:

- `; stdin: bytes` (printf `%b` escapes), the test's standard input.
- `; args: words`, its arguments.
- `; env: NAME=value ...`, its environment.
- `; warns: L:C ...`, the checker warnings it expects, if there's a
  checker; any other warning fails.

A test that writes files writes under `build/t/`.

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

A test runs the same way every time or it isn't a test. `run.sh` sets
what makes that so, and the runtime provides it:

- A virtual clock, which moves only when nothing can run.
- A fixed random seed and a fixed epoch for the time of day.
- A scheduling seed, for sweeps that look for races.
- Record and replay of everything that comes in from the world.
- A collector stress knob and poisoned frees, for the collector's own
  tests.

## Kinds of test

- `t/`: the golden tests. Each plan step adds some.
- `examples/`: programs, each with a `.expected` a golden test too.
- `docs/guide/code/`: the guide's programs, golden tests, and a check
  that each code block in a page matches its file.
- `compiler/tests/`: unit tests per pass, for what a golden test can't
  reach (the reader's positions, error messages).
- `t/types/`: the checker's warnings, if there's a checker.
- `t/replay.sh`: checks that need more than one run (record then
  replay; the same program under several scheduling seeds).
- `t/live.py`: what a golden test can't see: real time, real memory
  limits, signals, a terminal, a real network. Few, and each one named
  for the bug it guards.
