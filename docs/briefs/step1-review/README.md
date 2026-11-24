# The review of step 1's language, and what it left behind

Step 1's definition (integer arithmetic) was given to a reviewer with
perl 5.42 and one instruction: find a program the definition accepts
that perl treats otherwise. It found none, over about 1.2 million
`say` statements and half a million programs. These are its tools, as
it wrote them, and three scripts that turn them on the compiler. A
record, like `../arith-review.py`: nothing in `make test` runs them,
and nobody keeps the model up with the language. Start from them when
a later step wants the same.

- `model.py`: the reviewer's own implementation of the definition, in
  Python: which files are accepted, what each prints, where it faults.
  Written from the definition's text, without sight of the compiler.
- `check.py`, `gen_arith.py`: how it held the model to perl, and its
  generator of random expressions. (`check.py` expects a `t/`
  directory beside it to write programs into.)

The model is a second implementation of the step's language that the
builder didn't write, which is what the workbench calls a referee. So
the compiler was run against it:

    python3 docs/briefs/step1-review/gen.py       # 1,271,555 programs and the model's verdict on each
    node docs/briefs/step1-review/accept.ts       # does the compiler accept the same ones?
    python3 docs/briefs/step1-review/values.py    # and print the same, and fault the same?

`gen.py` writes every string of up to five or six fragments after
`say` (blanks, newlines, brackets, operators, `1`, `0`, `;`, `say`, a
comment, `--`, `**`) to `build/step1-review/`. On 2026-11-24 the
compiler and the model agreed on all of it: the same 20,304 programs
accepted of 1,271,555; the same output for the 19,288 of those that
don't fault and for 19,164 random expressions; the same fault for 240
programs that do. Each script was failed on purpose first: with the
one-blank rule off, 88 programs differ; with `x % -1` made 1, 26
batches do.
