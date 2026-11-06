# Brief: step 1, arithmetic

You are building step 1 of [`PLAN.md`](PLAN.md): the calculator's five
operators, `+ - * / %`, with their two faults. The design is decided:
D8 to D13 in [`DECISIONS.md`](DECISIONS.md). Your job is to build it
as written, with its tests and the model that writes their expected
output, and to report. It isn't to redesign it: where a decision
reads as a default, it's a default you build on as written.

## First

The step's **Size** line says medium, **Effort** high. Compare it with
your own model, by [`MODELS.md`](MODELS.md), and say so in your first
message. If you're small, stop there and say so; this step has a model
to write.

## Read, in this order

1. [`CLAUDE.md`](../CLAUDE.md), all of it. Its working rules bind you,
   and its code style has two lessons this step meets head on: C
   doesn't order a call's arguments, and a left shift of a negative
   value is undefined.
2. [`LANGUAGE.md`](LANGUAGE.md).
3. [`PLAN.md`](PLAN.md): step 0, then step 1, which is the
   specification: the files, the tests, where each expected output
   comes from, and what's left out.
4. [`DECISIONS.md`](DECISIONS.md), all of it (it's short); D3, D4, D5
   and D8 to D13 are the ones you build to.
5. [`t/README.md`](../t/README.md) and
   [`t/models/README.md`](../t/models/README.md): where expected output
   comes from, and the shape of a model's docstring.
6. [`MODELS.md`](MODELS.md), "When to escalate".
7. The code: `bin/langc.ts`, `compiler/src/`, `compiler/tests/`,
   `runtime/`, `t/run.sh`, and `t/checks.py` (to know what it checks).

**Don't read `t/referee/`**, in the tree or in git (`git show`, `git
log -p` and the like), and don't read earlier versions of this repo's
`compiler/`, `runtime/`, `t/models/` or `t/referee/` in its history:
the workbench has been built past this point before and reset. The
referee is what your model is checked against, and agreement means
something only if your model was worked out from the decisions alone.

## Do, in this order

1. **The tests, before the compiler.** Write 010 and 011 by hand,
   expected output worked out from the program. Then the model,
   `t/models/arith.py`, from D8 to D12 and step 1's text: it writes
   the programs and the expected outputs of 012 to 026, its docstring
   lists the thirty commands one a line, exactly as
   `t/models/README.md` shows them, and each program it writes carries
   a comment naming `t/models/arith.py` and the decision it checks.
   `make models` writes the files; never write or patch one by hand.
   Then `make checks`: it must end `all: 0 failed`, with the referee
   line `1 referees, 19 tests agree, 0 outside them`. `make golden`
   fails the new tests at this point, as it should.

   If the referee disagrees with a test, work out from the decisions
   which side is wrong, without reading the referee. If it's your
   model, fix the model and rerun it. If the decisions say the
   referee is wrong, or don't say, stop and report: the test, what
   each side prints, and the decision's words.
2. **The runtime** (`runtime/rt.h`, `runtime/rt.c`): the five checked
   operations and their faults, D9 and D10. Overflow is out of 63
   bits, not 64; tests 019, 020 and 021 are there for the ways that
   goes wrong.
3. **The codegen** (`compiler/src/codegen.ts`): the whole program
   checked first, in D13's order with its messages, then compiled,
   with operands sequenced left to right in the C (D11; tests 024 and
   025). No constant folding (D12). Keep the compiler's shape: pure
   functions over the forms, as `codegen.ts` and `reader.ts` are.
4. **The unit tests** in `compiler/tests/codegen.test.ts`, as step 1
   lists them; replace step 0's tests only where D13 changes what
   they check.
5. **Green:** `make test`, then `make golden-clang` and `make
   sanitize` (clang is installed; the sanitizer runtime may not be,
   and if it isn't, say so rather than skip silently), and `make
   check` (`npm install` once; if the network won't allow it, say
   so).
6. **The documents**, as step 1 lists them: `LANGUAGE.md`,
   `DESIGN.md`'s "The language", step 1 marked (done) with the
   progress line in `PLAN.md`, `CLAUDE.md`'s Status.
7. **Commit**, after `make hooks`, on this branch, one commit whose
   subject names the step and the decisions, as `Step 1: arithmetic,
   + - * / % and their faults, tests 010 to 026 (D8 to D13)`. Don't
   push.

## Don't touch

- `t/referee/`, `t/checks.py`, `t/run.sh`, the `Makefile`.
- Tests 000 and 001 and their expected outputs.
- `docs/DECISIONS.md`, `docs/PROCESS.md`, `docs/MODELS.md`, this
  brief. A decision you need that isn't in the log is a reason to stop
  and ask, not an entry to write.
- `compiler/src/reader.ts`: the step needs no change to it. If you
  find it does, say why before changing it.
- Any `.expected` the model writes, by hand, ever.

And don't add to the language: no operator beyond the five, no
variadic or unary form, no folding, no flag, no environment variable.
`MODELS.md`'s escalation list applies as written; the ones nearest
this step are the fix you're drawn to being an edit to an `.expected`
or the model to make a test pass, two attempts with the same test
still red, and a diff past the files step 1 names.

## Report

In this order, briefly:

1. Your model, and how it compares with the step's size.
2. The commit's hash and subject, and the files it changes.
3. The last lines of `make test`, including the referee's line, and
   of `make golden-clang`, `make sanitize` and `make check`, or why
   one wasn't run.
4. Every disagreement between your model and the referee, and how the
   decisions settled it.
5. Anything you did differently from step 1's text, and every point
   where you were unsure, with what you chose.

The lead reads the diff, not the summary, so the report doesn't need
to describe the code.
