# [name]

A cleaned-up Perl 5 with a runtime of its own. A program it accepts is
Perl 5.42 once its annotations are erased, and prints what perl prints
unless it stops loudly first; what Perl has that the language cuts is a
compile error or a fault, never a different meaning. The compiler is
TypeScript run by Node as it is, and emits C that links with a C
runtime. It has no name yet: the driver is `langc`, and a program is a
`.pl` file.

## Status

**Nothing is built.** 2026-11-24: the design was proposed from a
reading of Chalk, perl5-son, Opal and Allium
([`docs/BACKGROUND.md`](docs/BACKGROUND.md)). Stevan decided the scope
(D1), the core rule (D2), the compiler's shape (D3), Chalk's subset as
the start (D4), which of Perl 6's promises are planned (D5) and that
there is no Sea of Nodes (D6); D7 to D9 are the workbench's process
rules. D10 to D31 are defaults, every one open, listed at the end of
[`docs/DESIGN.md`](docs/DESIGN.md). [`docs/PLAN.md`](docs/PLAN.md) has
steps 0 (`say 42;`, and the oracle check) and 1 (integer arithmetic)
proposed in full and steps 2 to 30 in outline. The first draft was
reviewed adversarially against perl 5.38.2, which refuted four of its
claims about perl and found about twenty ways to be WRONG; D10, D14,
D15, D17, D18, D21 and D23 were rewritten, and
[`docs/TRAPS.md`](docs/TRAPS.md) keeps the fifty programs (T1 to
T50), by step. Known unfinished: D23, where perl's numbers carry
history. **Next:** Stevan settles the open questions steps 0 and 1
cite (D10, D12, D13, D15, D16, D21, D23, D25, D28 to D31), then step
0. Not agreed: the name; whether perigrin's
probes may be imported (D11).

## Read first, in this order

1. [`docs/LANGUAGE.md`](docs/LANGUAGE.md): the language as it is, for
   someone writing programs in it.
2. [`docs/DESIGN.md`](docs/DESIGN.md): the language and implementation
   as agreed. **(open)** marks proposals that haven't been confirmed.
3. [`docs/SURFACE.md`](docs/SURFACE.md): Perl, construct by construct:
   in, a fault, later, or cut.
4. [`docs/PLAN.md`](docs/PLAN.md): the build order.
   [`docs/TRAPS.md`](docs/TRAPS.md): for the step in hand, the
   programs where the obvious implementation is WRONG.
5. [`docs/DECISIONS.md`](docs/DECISIONS.md): why, and what was turned
   down. Check it before "improving" something; it may have been
   decided against.
6. [`docs/BACKGROUND.md`](docs/BACKGROUND.md): the four projects this
   learned from, and what is parked. Optional.

The process is the workbench's: `docs/PROCESS.md` and `docs/MODELS.md`
in `pmmc-labs/esoteric-language-workbench`.

## Working rules

- **The core rule (D2) is the design.** Before accepting a construct,
  ask what perl does with it. If the language would do anything else,
  it refuses or faults. A change that gives a Perl program a new
  meaning is a proposal that says so in its first line.
- **Never WRONG.** A program that runs, doesn't fault, and prints what
  perl doesn't is a bug, whatever else is true. Fix it by agreeing
  with perl, or faulting, or refusing, in that order of preference. A
  refusal has a message that names what was refused.
- **Aggressively simple.** When a feature needs machinery, say so and
  offer to cut it. Cutting is always allowed here.
- **Propose before building** any change to semantics, a construct
  moved between In, Fault, Later and Cut in `SURFACE.md`, a builtin,
  or anything marked (open). Give options and a recommendation. Record
  the outcome in `docs/DECISIONS.md` (who decided, why, what was
  rejected) and update `docs/DESIGN.md` and `docs/SURFACE.md`.
- **perl is the oracle, and memory isn't.** Never write what perl does
  from memory, in a test, a decision or a document: run perl 5.42 and
  paste. (perl5-son recorded being wrong from memory twice in one fix;
  this design's first draft had `2 ** 62` as an exact integer, and
  perl prints `4.61168601842739e+18`.)
- **A proposal for a large step is reviewed adversarially before
  it's built**: a reader who didn't write it, given the proposal and
  perl, asked to find a program that would run, not fault, and differ.
  What it finds goes into `docs/TRAPS.md` with the program and perl's
  output, and into the step as a test.
- **Expected output never comes from the compiler** (D7). A `same`
  test's comes from perl; a `fault` or `refused` test's is worked out
  by hand; a model writes the edges. When a model's output moves,
  rerun the model; don't patch the file.
- **Make a check fail on purpose before trusting it.** A new check,
  a new kind of test, a new script: break what it guards and see it
  go red. (perl5-son's harness once reported 986 of 986 clean when
  857 were, because a loop ate its own input.)
- **Tests run programs.** A check that reads the tree or the C and
  never runs the binary proves nothing about what a program prints.
- Keep a working compiler with passing tests at the end of every step
  (Ghuloum). Each step adds golden tests.
- **Examples bend to the language** (D8). A port of a Perl program
  will want something that was cut; change the port.
- When a construct or builtin is added or changes, update
  `docs/LANGUAGE.md` (no tables there) and its row in
  `docs/SURFACE.md`.
- When editing with scripts, assert that each replacement matched.
- Test timing uses a virtual clock; real time is never used in tests.
- Update the Status section above as steps land. It is the only
  handoff: there is no `docs/plans/`, and a plan that isn't a step in
  `PLAN.md` or a `Dn` doesn't exist.
- A commit that touches the implementation names its decision or plan
  step in the subject (D9; `make hooks` installs the check).
- At the start of a step, compare the step's **Size** line with your
  own model, by the workbench's `docs/MODELS.md`, and say so if they
  don't match.

## Code style

- TypeScript that Node runs as it is: only erasable syntax (no enums,
  no parameter properties, no namespaces).
- The compiler is plain functions over plain data: tree nodes are
  objects with a `kind`, lists are arrays, and nothing is mutated
  after the pass that made it. One file per pass. No class
  hierarchies. (If the compiler is ever ported to the language, this
  is the shape that ports; nothing depends on that.)
- **One table of names** (`compiler/src/names.ts`): keywords, builtins,
  their argument shapes and contexts. No pass switches on a source
  string that isn't in it.
- An error is a diagnostic with a position, raised where it's found.
  It is never a node in the tree.
- The generated C is one statement per operation, each result in a
  temporary (D31). C doesn't order a call's arguments: never pass a
  variable and a call that sets it in the same argument list, and
  never two arguments that can fault. The cloud machine's `cc` is gcc
  and the Mac's is clang: run the suite under both, and `make
  sanitize`, before calling a runtime change done. A left shift of a
  negative value is undefined before C23. (All three are the
  workbench's findings, each from a bug.)
- The runtime has no global state: one context, first argument of
  everything (D28).
- Every runtime operator checks its operands' tags and faults by name.
  No operator trusts the compiler until types (step 26) give it a
  reason to.
- Comments explain why, not what.

## Toolchain

- Node 22.18 or later, and a C compiler as `cc`; clang as well.
- **perl 5.42**, as `LANG_PERL` (default `perl`). The checks fail
  without it; they don't skip. [How it's installed on the cloud
  machine, whose own perl is 5.38.2: step 0 writes this.]
- Python 3 for `t/checks.py` and the models.
- `t/run.sh t/000-say.pl` checks the setup; it should end
  `1 tests, 0 failed`.

## Layout

[As built; `docs/PLAN.md` has it as planned. Step 0 writes this.]

## Commands

[The workbench's: `make test`, `make unit`, `make golden`, `make
checks`, `make check`, `make golden-clang`, `make sanitize`, `make
models`, `make commits`, `make hooks`; and `make doctor`, `make
oracle` (writes each `same` and `dies` test's `.expected` from perl),
`make census` from step 11. Step 0 writes this as it stands.]

A compiled program prints to stdout and exits 0. A fault is `fault:
MESSAGE at FILE line N.` on stderr and exit 1, after whatever stdout
had. An uncaught `die` is its message on stderr and exit 255. The
golden tests check stdout and stderr together, plus `exit: N` when the
status isn't 0.
