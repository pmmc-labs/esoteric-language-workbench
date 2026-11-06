# Brief: build step 5, a budget (`within`)

You are the builder of step 5 of the calculator. The proposal is done and
is what you build; you are not asked to propose or to change it. Work only
in the worktree you were started in.

## Read, in this order

1. `CLAUDE.md`, all of it, and follow its "Read first" order and its
   working rules.
2. `docs/PLAN.md`, step 5 and the Progress line. It lists the files, the
   unit tests, and all 22 golden tests with their programs and their
   expected output. That list is the spec for the tests.
3. `docs/DECISIONS.md`: D20 (the person's) and D21 to D27 (the defaults
   that complete it), and the entries they lean on: D3, D6, D13, D17, D19.
4. `docs/MODELS.md`, "Tiers" and "When to escalate" only.

Do not read `t/referee/`: it is the second implementation your tests are
checked against, and agreement means nothing if you copied from it.

## Size

The step is marked **medium**. Compare it with your own model first
(`docs/MODELS.md`) and say what you found, in the first line of your
report.

- Smaller than medium (Haiku, say), as a sub-agent with no one to ask:
  **build, and flag the mismatch first in the report.** The decisions are
  written, the tests are given and the referee is complete, so a mistake
  shows as a red check. Do not stop for this alone.
- The same or larger: build, and say so.
- In a session with a person: stop and ask.

## What to do, in this order

1. `make test` on the untouched worktree. It should be green.
2. Write tests 050 to 071 from the step's list: each program preceded by
   one `;` comment line (what it checks, the decision; do not name a file
   under `t/models/` in it), and its `.expected` exactly as listed (the
   value and a newline, or `fault: ...` and `exit: 1`). Check that each
   fails, and that each fails because `within` is not an operator and for
   no other reason. Commit them red (a commit of tests only needs no
   decision in its subject).
3. The runtime (`runtime/rt.h`, `runtime/rt.c`) as D27 says: the count, the
   limit, `charge()` as the first statement of each of the seventeen
   operator functions (check the count with grep: 17), `rt_within`. The
   existing tests stay green; commit, with `step 5` or `D27` in the subject.
4. The compiler (`compiler/src/codegen.ts`) as D26 and D27 say, and the
   unit tests the step lists in `compiler/tests/codegen.test.ts`. The new
   golden tests go green. Commit, with `step 5` or `D26` in the subject.
5. Run `make test`, `LANG_CC=clang make test` (or `make golden-clang`) and
   `make sanitize`, and `make check` if `npm install` works here. Any that
   cannot run, say so, and why.
6. Move the documents the step lists: `docs/LANGUAGE.md`, step 5's heading
   and the Progress line in `docs/PLAN.md`, and `CLAUDE.md`'s Status
   (including **Next**, and what model built this and at what Size). A
   step is not done until they are moved.

## What not to touch

`t/referee/`; any existing test, `.expected` file or model; the text of D1
to D27 (if you must decide something, add an entry after D27, below);
`docs/DESIGN.md` (still the template); `docs/MODELS.md`; `docs/PROCESS.md`.
No flag, environment variable or knob. Leave out what the step lists under
"Leave out", and report, don't add, if something seems to need it.

Do not run `make hooks`: in a worktree it writes into the main checkout's
git directory, which is not yours. Name `step 5` or a `Dn` in the subject
of each commit that touches `compiler/`, `runtime/`, `lib/` or `bin/`,
and do not push.

Keep scratch files in a directory you create with `mktemp -d`, not a
fixed name: the scratch directory may be shared with other sessions.

## When something is wrong or missing

- A test red for a reason you cannot trace to your code, or `make checks`
  saying the referee and a `.expected` disagree: the fix is never to edit
  an `.expected` or a model. Stop at that point and report both sides, with
  the program and what each says; the decisions say which is right and the
  referee is not yours to read.
- A question the decisions do not answer: take the smallest reading that
  fits D20 to D27, add it after D27 as a numbered entry marked *(Default)*
  with its reasons and what you rejected, and put it first in your report
  for the person to confirm. In a session with a person, ask instead.
- Two attempts at one failure and still red, or a diff growing past what
  the step lists: stop and report.
- Anything wrong outside the step that you notice: report it, do not fix it.

## Report

First lines: your model against the Size, and any default you added.
Then: what landed, by file; the commits; the last lines of `make test`,
the clang run and `make sanitize`; the number of tests and whether the
referee agreed with them (`make checks` prints it); every point where you
were unsure, each with what you did; anything noticed outside the step.
