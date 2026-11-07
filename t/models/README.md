# Models

A model is a small program in another language that writes a golden
test's expected output, and sometimes the test program too, from the
language's definition rather than from its implementation. Python
mostly; Java where the thing modelled was ported from Java; anything
with a trustworthy library for the subject.

A model's docstring says which test it's for, what it models and how,
and the exact commands that regenerate the files:

    python3 t/models/thing.py --program > t/NNN-thing.ditto
    python3 t/models/thing.py > t/NNN-thing.expected

Each such line starts with `python3 t/models/`, is run from the
repository root, and redirects to exactly one file; `t/checks.py` runs
them all and fails if a file differs.

Rules:

- The model computes the answer from the definition. Where it has to
  copy an implementation detail (a float printed to 17 digits, say), it
  says so and why that's the definition.
- The model is rerun when its output moves, and the file is never
  patched by hand. A test whose file was patched has no model.
- A model of scheduling is a model of the run queue, not of the
  implementation's scheduler: it says what order the definition
  permits.
- Trusted libraries, not reimplementations: Python's `struct`,
  `hashlib`, `datetime`, `fractions`; mpmath for correctly rounded
  math; a reference implementation where one exists.
