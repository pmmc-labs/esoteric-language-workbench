# Brief: design a language, then build it

This repository is a template for building a language with an agent as
the builder and a person as the designer (`docs/PROCESS.md`). In this
session there is no person. **You are both.** You design the language,
make every decision, and see it built. There is no one to ask: never stop
to ask, decide and record.

## What to make

An original language of your own design, in the spirit of the repository's
name: it has one unusual idea at its core (the template's "core rule",
D7), the thing that makes it worth existing. But it must be **usable**:
someone should be able to write ordinary small programs in it. Don't
recreate an existing esoteric language; borrowing ideas is fine and goes
in `docs/BACKGROUND.md`.

Usable means, and the build is done when, `examples/` holds at least
these, each a golden test with a `.expected`:

1. FizzBuzz, 1 to 100.
2. A recursive function (factorial or Fibonacci).
3. Sorting a list of numbers.
4. Something on text (reverse a word, count letters, or similar).
5. A program that shows off the core rule.

Examples bend to the language, but these five must be writable in it.

## Fixed, not yours to decide

These are the experimenter's, so the run stays comparable and cheap:

- The compiler is TypeScript run by Node 22 as it is (erasable syntax
  only: no enums, no parameter properties), compiling to C, linked with a
  runtime in C by `cc`. `LANG_CC` overrides the C compiler.
- It must pass under gcc (`cc` here) and clang, and under clang's
  `-fsanitize=undefined,address`. Both are installed.
- Golden tests' expected output comes from an independent source: by
  hand, or a model in `t/models/` (Python), rerun and never patched
  (`t/README.md`). Each step's tests are committed red before its code.
- Ghuloum: the suite is green at the end of every step.
- **Budget:** at most 10 steps in `docs/PLAN.md`, step 0 (the scaffold)
  and the examples included. Size the language to fit. Memory may be
  never freed if you decide so; aggressively simple wins.

Everything else is yours: the name, the syntax, the semantics, the
runtime, errors, the core rule.

## How to work, for economy

Usage is the cost being measured: spend it where it buys quality.

1. **Design first, all of it, yourself.** Read `CLAUDE.md` and
   `docs/PROCESS.md`, then fill `CLAUDE.md`'s brackets, write
   `docs/DESIGN.md`, `docs/DECISIONS.md` (D1 on; attribute each one
   *(designer)*, with its reason and `Rejected:`), `docs/PLAN.md` (each
   step with what it adds, its tests, what it leaves out, and a **Size**
   line: small, medium or large), and a first `docs/LANGUAGE.md`. Decide
   the whole language now, so no builder has to invent. Then reread it
   once, as a builder would, for silences: what a program could do that
   no decision answers (evaluation order, every fault and its message,
   printing, edge values, what an error before running looks like).
   Close them. Commit `Design: ...` before any code.
2. **Delegate each step** to one sub-agent (Agent tool, a fresh agent, not
   a fork), with `model: "sonnet"` for medium steps and `"haiku"` for
   small ones; keep large work (a design question, a hard runtime
   mechanism) for yourself. The sub-agent writes the step's model and
   tests, commits them red, builds the step, and commits it green. Its
   brief is short: the step number, the files to read, the commands, and
   "no one to ask: write any default as a *(default)* decision and flag
   it in your report". Don't paste documents into briefs; point at them.
   Run sub-agents one at a time, in the foreground.
3. **Review cheaply.** After each step: the suite under gcc, clang and the
   sanitizers, `git diff --stat`, and read only what looks wrong or what
   the report flags. Decide each flagged default (keep it as
   *(designer)*, or change it and say so). Don't spawn reviewers. No
   referee in this run.
4. **When something fails twice,** cut or simplify it with a decision
   rather than retrying. Don't search the web.
5. Commit each step as it lands; the subject names its step or decision.
   Update `CLAUDE.md`'s Status as steps land. Push the branch after each
   step.

## At the end

Write `EXPERIMENT.md` at the root, short:

- The language in a paragraph, and its core rule in a sentence.
- Steps, decisions (how many; which were hard), golden tests, examples.
- Per step: who built it (you or which sub-agent model), what it flagged,
  and anything you had to redo.
- Usage as far as you can see it (sub-agent tokens and time from their
  results).
- What you'd do differently, and what you'd want a person to overrule.

Then push, and end with a three-line summary.
