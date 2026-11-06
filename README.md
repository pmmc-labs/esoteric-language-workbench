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

## What's here

| Path | |
|---|---|
| `CLAUDE.md` | The agent's standing instructions, as a template. Fill the brackets, keep the rules. |
| `docs/PROCESS.md` | The method: the rules, why each one is there, what a session looks like, and what each party does. Read this first. |
| `docs/DESIGN.md` | Skeleton: the language and implementation as agreed, with **(open)** marking what isn't. |
| `docs/DECISIONS.md` | Skeleton: numbered decisions, who made each, why, and what was turned down. |
| `docs/PLAN.md` | Skeleton: numbered steps, each one feature, each ending green with tests added. |
| `docs/LANGUAGE.md` | Skeleton: the language as it is, for someone writing programs in it. |
| `t/README.md` | The golden-test discipline: expected output from an independent source, never from the implementation. |
| `t/models/README.md` | Models: small programs in another language that write expected outputs, rerun and never patched. `t/models/arith.py` is a worked one. |
| `t/checks.py` | The mechanical checks: models rerun and compared, tests paired, commits naming their decision. |
| `docs/MODELS.md` | Which tasks need which size of model, when to escalate, when a smaller one is safe. |
| `bin/`, `compiler/`, `runtime/`, `t/run.sh`, `Makefile` | Steps 0 and 1, worked: a calculator, the smallest end-to-end compiler, its runner and its tests. |

## Using it

1. Copy the tree into a new repo (or use it as a GitHub template).
2. Fill `CLAUDE.md`'s brackets: the language's name, the host language,
   the toolchain, the commands.
3. Write `docs/DESIGN.md`'s goals and the first decisions in
   `docs/DECISIONS.md` (D1 to D10 or so are the scope: what it's for,
   what's cut, what's borrowed). These are the person's, not the agent's.
4. Steps 0 and 1 are built: a TypeScript compiler that Node runs as it
   is, integer arithmetic compiled to C and linked with a C runtime,
   `t/run.sh`, a `Makefile`, golden tests from a model, and the checks.
   `make test` should pass; `make hooks` installs the commit check.
   Rename `lang`, `langc` and `.lang` to the language's own, keep or
   replace the calculator's decisions (D1 to D7), keep D8 to D10.
5. Propose the next step. From then on the loop in `docs/PROCESS.md`
   runs.
