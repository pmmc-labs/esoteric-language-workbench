# The process

How a language gets built here, by an agent and a person, and why each
part of it is there. The rules are short; this says what each one does
and what went wrong without it. It comes from building a64-slight.

## The two roles

**The person** owns the language: what it's for, what it isn't, taste,
and every decision about semantics. They read proposals, pick, and run
the test suite on hardware the agent doesn't have.

**The agent** owns the implementation: the compiler, the runtime, the
tests, the documents. It proposes, builds in steps, and records.

The quality of the language comes from the person's taste. The process
exists to apply that taste at the right points and nowhere else, and to
stop the agent from substituting its own.

## The loop

Every unit of work is a numbered step in `PLAN.md`, and a step goes like
this:

1. **Propose.** The agent writes what the step would do, and where it
   touches semantics, a form, a builtin, or anything marked **(open)**,
   gives options and a recommendation. A proposal is a few paragraphs
   in `PLAN.md`, or a message; the record goes in `DECISIONS.md`.
2. **Decide.** The person picks. What was picked, why, and what was
   turned down become a `Dn` entry, attributed *(User)*. A default the
   agent took without discussion is attributed *(default)* and is fair
   to revisit.
3. **Build.** In sub-steps if the step is big, each one leaving the
   suite green. The implementation changes, `LANGUAGE.md` changes with
   it, `DESIGN.md` changes if the design did.
4. **Test.** Golden tests are added for what the step did. Their
   expected output comes from somewhere other than the compiler: by
   hand, or from a model in `t/models/`.
5. **Record.** The commit subject names the step and the decision:
   `fork takes a function and its arguments (D286)`. `CLAUDE.md`'s
   Status gains a sentence. The person runs `make test` on their
   machine and reports only failures.

A step is sized to a session or two. A session that ends mid-step leaves
the suite green at the last sub-step and a Status line saying where it
stopped.

## The rules, and why

### Golden tests from an independent source

A golden test is a program and its expected output. The rule is that
expected output is **never copied from what the compiler printed**. It's
worked out by hand, or by a model: a small Python (or Java, or anything)
program that computes what the output must be from the language's
definition, and is kept in `t/models/`.

This is the rule the others lean on. An agent that writes a test by
running the compiler and saving what came out has tested nothing; it has
frozen a bug as a spec. Every failure is then a conversation about
whether the expected file or the compiler is right, and the agent will
find a reason the file should change. With the output from an
independent source, a failure is a fact.

Its corollary: when a change legitimately moves an output a model wrote,
**rerun the model, don't patch the file**. A patched file and a stale
model disagree at the next change, and then nobody knows which is right.
(a64-slight's D287 found three files that had been patched.)

Independent sources that worked: Python's `float`, `struct`, `hashlib`,
`datetime` and `fractions`; mpmath for a libm; Java's own `SplittableRandom`
for a PRNG ported from it; a model of the run queue for output that
depends on scheduling; a reference implementation of an algorithm
(SimPy's bank, the JSONTestSuite); the language's own earlier
interpreter, if it has one, for the surface that's kept.

### A working compiler at the end of every step

Ghuloum's rule (*An Incremental Approach to Compiler Construction*): the
first step compiles one integer literal to a binary that prints it, and
every step after adds one feature, with the suite passing at the end. No
step is "the parser" or "the backend"; every step goes end to end.

What it buys: no long broken stretch. A session can end anywhere. A
regression is found within the step that caused it, by the test the
step before added. And the test suite grows at the rate the language
does, so there's never a "write the tests" phase that doesn't happen.

### The decision log

`DECISIONS.md` is numbered, attributed, and keeps what was rejected. An
entry is: what was decided, *(User)* or *(default)*, why, and
"Rejected: ..." with the alternatives and the reason each lost.
Decisions are revised, not deleted: a later entry says "retires D8", and
D8 stays, with a note pointing forward.

What it buys: a new session doesn't re-propose what was turned down.
Instructions in `CLAUDE.md` say to check the log before improving
anything. The attribution matters: an agent given "the user decided X"
holds to X; given "X was decided" it will argue with it. The rejections
matter as much as the decisions: the reason selective receive was
rejected is what stops it coming back under another name.

The log also gives the commits, the design doc, the plan and the tests a
shared index. `D286` appears in the commit subject, in `DESIGN.md`, in
the test's comment and in `CLAUDE.md`'s Status, so any one of them leads
to the rest.

### Propose before building

Semantics, forms, builtins, the core rule, and anything marked (open):
options and a recommendation first, then the person picks. Everything
else (the implementation of what's agreed, bug fixes, tests, docs) the
agent just does.

The line is drawn where taste lives. An agent asked about everything
stalls; an agent asked about nothing builds a language nobody wanted.
Semantics is where a wrong default costs the most to undo, because
programs and tests get written against it.

A proposal that's been agreed is also where the plan comes from: the
proposal names its steps, and they go into `PLAN.md` as written.

### Examples bend to the language

When an example program needs something the language doesn't have,
change the example or drop it. Never add to the language to make an
example pass.

This is "aggressively simple" made operational. The easy move, for an
agent, is always to add: a builtin, a special case, a flag. Every port
of an existing program will want something. This rule makes the
addition a proposal (above) rather than a side effect of a port, and
most of the time the example is better for the change.

### An independent implementation before calling it a bug

A reported misbehavior is checked against something else that computes
the same thing before the code is changed. The agent's reading of the
spec is not that something else.

### Determinism, from the start

Tests are only facts if a run is reproducible. a64-slight built the
knobs early and never regretted it:

- A **virtual clock** (`SLIGHT_CLOCK=virtual`): time starts at 0 and
  moves only when nothing can run, straight to the next timer. Every
  test runs on it; real time never appears in a test.
- A **seeded scheduler** (`SLIGHT_SCHED=n`): processes run in an order
  from a seed, so a race is found by sweeping seeds.
- **Record and replay**: everything that comes in from the world is
  written to a file, and a run can be replayed from it exactly.
- **Collector stress and poison**: a collection at every nth call, and
  freed memory filled with garbage, so a missed root fails now and not
  in a month.
- A fixed **seed** for random numbers, and a fixed epoch for the time of
  day, set by the test runner.

For a language without processes most of these collapse to the first and
last. Build what applies before the second step needs it.

### The referee

A referee is a second implementation of the language, small and slow,
written from the decisions and not from the runtime: an evaluator in
Python that takes any program and prints what the `.expected` must be.
It lives in `t/referee/`, and `make checks` runs it over every golden
test, so the suite and the referee are held to agree, and a test that
isn't covered yet is skipped until the referee grows.

It exists for one thing: to make a model written by someone else
checkable. A model that mirrors the implementation passes every test;
against a referee it either agrees or it doesn't, and the decisions say
which is wrong. This repo's third and fourth experiments
(`MODELS.md`) rested on it: without the referee, "the smaller model
wrote a real model" would have been a judgement; with it, a diff. It
also does what "verify a reported misbehaviour against an independent
implementation" asks for, every time, mechanically.

The large model decides when one is needed, at proposal time: the
step's text says `Referee: extend t/referee/NAME.py to cover this` or
`Referee: none`, with the reason. It's wanted when the model is to be
delegated, when the semantics have traps a mirror would copy, or when
expected outputs aren't checkable by eye. It isn't wanted for a step
whose tests are a few lines by hand, or whose output is a direct read
of the definition. Writing the referee is large work, and it's written
or extended before the step is handed to a builder.

And one rule of shape: a referee's reader and evaluator are loops with
a stack of their own, not recursive functions. A program nests as deep
as a test wants, and a referee that recurses is as deep as its own
author's tests happened to go; this repo's failed past a thousand
levels the first time a builder's tests went deeper.

Two rules keep it honest. The builder of a step doesn't read the
referee, so that agreement means two derivations and not one copied.
And the referee is checked against the suite before it judges: this
repo's was wrong once on its first run, range-checking a quotient on
the way to a remainder, and the suite showed it.

### Mechanical checks, where a rule can be one

A rule an agent has to remember is a rule a weaker agent, or a long
session, will forget. Where a rule can be checked by a script, it is,
and the script is in `make test`:

- **Models**: every file a model writes is regenerated and compared.
  A patched `.expected` fails; so does a model changed without a rerun.
  The convention that makes this possible is that a model's docstring
  lists every command that writes a file, one a line.
- **Tests**: every test has its `.expected`, and a test that names a
  model names one that lists it.
- **Commits**: a commit that touches the implementation names a `Dn`
  or a plan step in its subject, checked over a range, or by a
  commit-msg hook as you commit.
- **Referee**: every referee agrees with every golden test it covers.

`t/checks.py` has them. What can't be checked by script (that an
expected output written by hand was in fact worked out by hand, that a
proposal was read) stays a rule, and is the person's to watch.

### The documents, and what each is for

- `LANGUAGE.md`: the language as it is, for a user. Every form, every
  builtin, no tables. Changed in the same commit as the feature.
- `DESIGN.md`: the language and implementation as agreed. Marks
  **(open)** what's a default not yet confirmed. Short; the reasons
  are in the log.
- `PLAN.md`: numbered steps, each one feature, with a progress line at
  the top. Proposals that have been agreed live here as their steps;
  proposals not yet agreed live here marked as such.
- `DECISIONS.md`: above.
- `CLAUDE.md`: the agent's standing orders and the Status paragraph.
  The Status is the handoff: dense, with `Dn`s and test numbers.
- `BACKGROUND.md`: prior art, what was borrowed, what's parked (other
  targets, other ideas). Where things go so they stop coming up.
- `briefs/`: the brief each step was built from, where one was written
  for a builder other than the proposer; `5-budget.md` is the worked
  example.
- The guide (`docs/guide/`): for learning the language. Its code blocks
  are golden tests, checked against the files they came from, so the
  guide can't drift.
- `MODELS.md`: which tasks need which size of model, when to escalate,
  when a smaller one is safe, for choosing a session's model and a
  sub-agent's.

### The person's machine

The agent develops where it can (a cloud x86 box, with the native
target cross-compiled and run under an emulator). The person runs the
suite on the real hardware after every step and reports only failures.
This is a second oracle the agent can't talk its way around, and it's
where every platform difference was found (macOS's linker, Rosetta's
floats, a loopback race).

It found one in this repo's own step 1, on the first run. The runtime's
arithmetic was written `checked(r, __builtin_add_overflow(a, b, &r))`.
C doesn't order a call's arguments: gcc, the cloud machine's `cc`,
happened to set `r` first and the suite passed; clang on the M2 read
`r` before it was set, and three tests printed `0` where they should
have faulted. Nothing on the cloud side would have shown it, since the
agent had run the suite only under the compiler that hid it. What
followed is the shape every such find should take:

1. Reproduce where the agent is, before changing anything (`LANG_CC=clang`
   on the cloud machine failed the same three tests).
2. Fix the cause, not the symptom (the flag computed in a statement of
   its own; not a `volatile`, not a reordering that happens to work).
3. Record the lesson where the next session will read it (CLAUDE.md's
   code style: never pass a variable and a call that sets it in one
   argument list), naming the symptom, so it's recognised and not just
   obeyed.
4. Make the check mechanical where it can be (`make golden-clang`, the
   suite under the other compiler, so the cloud side runs both; and
   `make sanitize`, which would have caught the read on Linux, and on
   its first run caught a second thing: a left shift of a negative
   value, undefined C that every compiler happens to do right).
5. Name the finder in the commit (D4's subject says "Found by Stevan's
   make test"), since who found what is part of the record.

## What a session looks like

1. Read `CLAUDE.md`. Its Status says where things are.
2. Read the plan's next step, and the decisions it cites.
3. If the step needs a decision, propose and stop. The person's reply
   starts the next session, or the same one.
4. Build in sub-steps, `make test` after each.
5. Write the tests, from a model where the output isn't obvious.
6. Update `LANGUAGE.md`, `DESIGN.md` if needed, `DECISIONS.md`, the
   plan's progress line, `CLAUDE.md`'s Status.
7. Commit with the `Dn` in the subject. Report what landed, what
   failed, what's next.

## What didn't matter as much

Commit message format beyond the `Dn`. Branch discipline (one branch, a
PR every few dozen decisions, worked fine). Formal specification; the
golden tests are the spec. Code review by another model; the tests
caught more than the reviews did, and a review's findings were only
worth anything once each was turned into a test (a64-slight's
`docs/review-2026-11-02-plan.md` did exactly that).

## Signs it's working

The suite grows every commit. A session can start cold and be
productive in minutes. A question "why does it do X" has a `Dn` answer.
Nothing in the language is there because an example wanted it. The
person spends their time on proposals, not on debugging.
