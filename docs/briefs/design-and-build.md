# Brief: design a language, then build it

This repository is a template for building a language with an agent as
the builder and a person as the designer (`docs/PROCESS.md`). In this
session there is no person. **You are both.** You design the language,
make every decision, and see it built. There is no one to ask: never stop
to ask, decide and record.

## What to make

A **practical** language of your own design that is still creative. The
repository's name is ironic: this is a platform for experimenting with
languages, not for oddities. Someone who writes TypeScript, Python or Go
should be able to read your examples at first sight and write a program
the same day.

Creativity goes into making ordinary programs better: clearer, shorter,
safer, or easier to get right. One or two distinctive ideas are welcome
where they serve that, and they go in the template's "core rule" (D7).
Use unusual ideas sparingly. An earlier run built its whole language
around one striking idea, and the result was too strange to work with:
every example had to work around it. A good test for an idea is whether
the examples would be worse without it. Don't recreate an existing
language. Borrowing ideas is fine, and they go in `docs/BACKGROUND.md`.

Usable means, and the build is done when, `examples/` holds at least
these, each a golden test with a `.expected`:

1. FizzBuzz, 1 to 100.
2. A recursive function (factorial or Fibonacci).
3. Sorting a list of numbers.
4. Something on text: count the words in a passage, or something
   similar.
5. A program built around compound data: records, maps, or whatever the
   language has, such as a small inventory, a graph search, or a bank
   ledger.
6. A program that shows off the distinctive idea, in a task where it
   earns its place.

Examples bend to the language, but these six must read naturally in it.
If one needs a workaround, treat that as a design problem rather than an
example problem.

## Fixed, not yours to decide

These are the experimenter's, so the run stays comparable and cheap:

- The compiler is TypeScript run by Node 22 as it is (erasable syntax
  only: no enums, no parameter properties), compiling to C, linked with a
  runtime in C by `cc`. `LANG_CC` overrides the C compiler.
- It must pass under gcc (`cc` here) and clang, and under clang's
  `-fsanitize=undefined,address`. Both are installed.
- Golden tests' expected output comes from an independent source: a
  model in `t/models/` (Python), rerun and never patched, or by hand
  (`t/README.md`).
  - Every step whose tests compute values, the distinctive idea's step
    above all, gets a model. Hand-written expectations are for faults,
    errors and short programs only.
  - Each step's tests are committed red before its code.
- Ghuloum: the suite is green at the end of every step.
- **Budget:** at most 10 steps in `docs/PLAN.md`, step 0 (the scaffold)
  and the examples included. Size the language to fit. Memory may be
  never freed if you decide so; aggressively simple wins.

Everything else is yours: the name, the syntax, the semantics, the
runtime, errors, input, the distinctive idea.

## How to work, for economy

Usage is the cost being measured: spend it where it buys quality.

1. **Design first, all of it, yourself.**
   - Read `CLAUDE.md` and `docs/PROCESS.md`, then write the design:
     - fill `CLAUDE.md`'s brackets;
     - `docs/DESIGN.md`;
     - `docs/DECISIONS.md`, D1 on, each attributed *(designer)*, with
       its reason and `Rejected:`;
     - `docs/PLAN.md`, each step with what it adds, its tests, what it
       leaves out, and a **Size** line (small, medium or large);
     - a first `docs/LANGUAGE.md`.
   - Decide the whole language now, so no builder has to invent. That
     includes, per form, every error and fault: its message and the
     position it points at. An earlier run's builders spent most of
     their defaults on exactly that.
   - Before any code, write the six examples in the designed language,
     in `docs/DESIGN.md` or a scratch file. Fix the design wherever they
     read awkwardly.
   - Then reread everything once, as a builder would, looking for
     silences: what a program could do that no decision answers. Think
     of evaluation order, printing, edge values, and what an error before
     running looks like. Close them.
   - Commit `Design: ...` before any code.
2. **Delegate each step** to one sub-agent: the Agent tool, a fresh agent
   rather than a fork, with `model: "sonnet"`.
   - An earlier run found Haiku cost more than Sonnet even on its
     smallest step, so use Haiku only for pure repetition.
   - Keep large work (a design question, a hard runtime mechanism) for
     yourself.
   - The sub-agent writes the step's model and tests, commits them red,
     builds the step, and commits it green.
   - Its brief is short: the step number, the files to read, the
     commands, and "no one to ask: write any default as a *(default)*
     decision and flag it in your report". Don't paste documents into
     briefs; point at them.
   - Run sub-agents one at a time, in the foreground.
3. **Review cheaply.** After each step:
   - Run the suite under gcc, clang and the sanitizers, check
     `git diff --stat`, and read only what looks wrong or what the
     report flags.
   - Decide each flagged default: keep it as *(designer)*, or change it
     and say so.
   - Don't spawn reviewers. No referee in this run.
4. **When something fails twice,** cut or simplify it with a decision
   rather than retrying. Don't search the web.
5. **Commit each step as it lands**, with a subject that names its step
   or decision. Update `CLAUDE.md`'s Status as steps land, and push the
   branch after each step.
6. **If the examples show friction,** and the budget has steps left,
   you may spend one step removing it, by decision.

## At the end

Write `EXPERIMENT.md` at the root, short:

- The language in a paragraph, and its distinctive idea or ideas in a
  sentence each, with why each earns its place.
- Steps, decisions (how many; which were hard), golden tests, models,
  and examples.
- Per step: who built it (you or which sub-agent model), what it flagged,
  and anything you had to redo.
- Usage as far as you can see it (sub-agent tokens and time from their
  results).
- Where it's still awkward to write in, what you'd do differently, and
  what you'd want a person to overrule.

Then push, and end with a three-line summary.
