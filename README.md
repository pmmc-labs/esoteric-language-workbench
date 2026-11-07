# esoteric-language-workbench

A template for building a programming language with an AI agent as the
builder and a person as the designer. It captures the process that built
[a64-slight](https://github.com/pmmc-labs/a64-slight): a Lisp on an actor
runtime, compiled to native AArch64 and x86-64, in 310 commits over four
weeks, with 340 golden tests, a decision log of 290 entries and a type
checker, two targets and a replayable runtime, all of it green at every
step.

The process is the product here. Nothing in this repo is specific to
Lisps, actors or native code.

**This branch, `interpreter`,** is the workbench for an interpreter
rather than a compiler (`docs/DECISIONS.md`, D28 and D29;
`docs/PROCESS.md`, "An interpreter instead of a compiler"): the
calculator's decisions, golden tests, models and referee, its compiler
and runtime taken out, to be built again as a tree-walker in
TypeScript on Node. main has the compiler.

## What's here

| Path | |
|---|---|
| `CLAUDE.md` | The agent's standing instructions, as a template. Fill the brackets, keep the rules. |
| `docs/PROCESS.md` | The method: the rules, why each one is there, what a session looks like, and what each party does. Read this first. |
| `docs/REPORT.md` | What the workbench found: the process, who can do which part of it, and the limits, on one page. |
| `docs/briefs/decisions-browser.md` | The brief for a hyperlinked, graphed browser for a decision log, a64-slight's first. |
| `tools/decisions/` | That browser: a log read into JSON, and one HTML page of it, hyperlinked, graphed and as an arc map. `make decisions` builds this log's and a64-slight's. |
| `docs/DESIGN.md` | Skeleton: the language and implementation as agreed, with **(open)** marking what isn't. |
| `docs/DECISIONS.md` | Skeleton: numbered decisions, who made each, why, and what was turned down. |
| `docs/PLAN.md` | Skeleton: numbered steps, each one feature, each ending green with tests added. |
| `docs/LANGUAGE.md` | Skeleton: the language as it is, for someone writing programs in it. |
| `t/README.md` | The golden-test discipline: expected output from an independent source, never from the implementation. |
| `t/models/README.md` | Models: small programs in another language that write expected outputs, rerun and never patched. `t/models/arith.py` is a worked one. |
| `t/checks.py` | The mechanical checks: models rerun and compared, tests paired, the referee agreeing with every test, commits naming their decision. |
| `t/referee/` | The referee: a second implementation from the decisions, which a delegated model is judged against. |
| `docs/MODELS.md` | Which tasks need which size of model, when to escalate, when a smaller one is safe. |
| `t/run.sh`, `Makefile` | The runner, which runs each golden test through `bin/lang.ts`, and the targets. The interpreter itself is built from step 0 (`docs/PLAN.md`). |

## Using it

1. Copy the tree into a new repo (or use it as a GitHub template).
2. Fill `CLAUDE.md`'s brackets: the language's name, the host language,
   the toolchain, the commands.
3. Write `docs/DESIGN.md`'s goals and the first decisions in
   `docs/DECISIONS.md` (D1 to D10 or so are the scope: what it's for,
   what's cut, what's borrowed). These are the person's, not the agent's.
4. On this branch nothing is built: `docs/PLAN.md`'s steps 0 to 5
   build the interpreter against golden tests that already exist, and
   `make test` passes once step 5 is done. `make hooks` installs the
   commit check. Rename `lang` and `.lang` to the language's own, keep
   or replace the calculator's decisions, keep D8 to D10, D28 and D29.
5. Propose the next step. From then on the loop in `docs/PROCESS.md`
   runs.
