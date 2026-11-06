# Models

A model is a small program in another language that writes a golden
test's expected output, and sometimes the test program too, from the
language's definition rather than from its implementation. Python
mostly; Java where the thing modelled was ported from Java; anything
with a trustworthy library for the subject.

A model's docstring says which test it's for, what it models and how,
and every command that regenerates a file, one a line, exactly:

    python3 t/models/thing.py --program > t/NNN-thing.lang
    python3 t/models/thing.py > t/NNN-thing.expected

`t/checks.py` reads those lines, runs each, and fails if the file
differs; `make models` writes them. A model that lists no command, or a
test that names a model that doesn't list it, fails too.

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
