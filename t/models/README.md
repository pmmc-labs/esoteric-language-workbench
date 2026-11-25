# Models

A model is a small program in another language that writes a golden
test's expected output, and sometimes the test program too, from the
language's definition rather than from its implementation. Python
mostly; Java where the thing modelled was ported from Java; anything
with a trustworthy library for the subject.

A model's docstring says which test it's for, what it models and how,
and every command that regenerates a file, one a line, exactly:

    python3 t/models/thing.py --program > t/NNN-thing.pl
    python3 t/models/thing.py > t/NNN-thing.expected

`t/checks.py` reads those lines, runs each, and fails if the file
differs; `make models` writes them. A model that lists no command, or a
test that names a model that doesn't list it, fails too. `arith.py` is
the worked example: copy its shape.

`arith.py` is step 1's Ints; `num.py` is step 2's Nums and the rule
for which kind an answer is (D35, D45); `str.py` is step 3's strings,
and imports `num.py` for its numbers; `bool.py` is step 4's booleans,
undef, comparisons and logic, and imports both. `str.py` lists its commands in
its docstring and checks the list against its own table of tests as
it starts: `python3 t/models/str.py --commands` prints the list when
a test is added.

Keep a program a model writes to about three thousand statements, and
write several if there are more: a C compiler takes more than
proportionally longer over one long run of statements.

In this language a model is half of a pair. The other half is perl:
the oracle check (`t/checks.py oracle`) runs the model's program under
perl 5.42 and holds its `.expected` to what perl prints. Two
derivations, neither of them the compiler's; when they disagree,
neither file is patched, and the disagreement is reported.

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
