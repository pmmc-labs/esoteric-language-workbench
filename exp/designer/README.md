# The designer experiment

November 2026. In every earlier round the person designed and the agents
built. The person asked: "This time I would like an agent to also design
the language, and make all the decisions", as efficiently as possible,
with the scope left to the agent. This folder records two runs. Each was
a bare cloud session given the template and a brief. It designed a
language alone and saw it built through sub-agents. There was no person
to ask in either session.

In short:

- **Run 1** built Strata, a language whose core rule is that every
  variable is a history. It came out green and cheap, and it was too
  strange to work with.
- **Run 2** was briefed for something practical. It built Ditto: value
  semantics and a lookup fallback, `a else b`. It was green, its
  examples read naturally, and it cost three times as much.
- A referee written from Ditto's documents alone agreed with 567 of its
  572 golden tests and 3,990 of 4,000 random programs. It found two gaps
  in the decisions and no compiler bugs.

## What's here

| Path | |
|---|---|
| `README.md` | This record |
| `briefs/run1-strata.md`, `briefs/run2-ditto.md` | The brief each run was given, as `docs/briefs/design-and-build.md` on its base |
| `referee/` | Ditto's referee: `referee.py`, `SILENCES.md` (the 23 places the documents left it to choose), and `tests/` (84 programs of its author's own, `sh tests/run.sh`) |
| `fuzz/` | The random-program tester: `gen.py SEED [--else]`, `fuzz.sh N START`, `one.sh`, `mix.py`, and `min/` (the minimised disagreements) |
| `refcheck.sh` | `refcheck.sh CHECKOUT REFEREE`: the referee over a checkout's golden tests |
| `results/` | The final suite run, the referee over the golden tests, both fuzz runs, and every disagreeing program with both outputs |

## The branches

None is merged into main.

| Branch | What it is |
|---|---|
| `claude/nifty-davinci-xzl3c6` | Run 1. The base `4698a43` (an orphan commit: the template as first written, `f9ada65`'s tree, plus main's `docs/PROCESS.md` and the brief), then Strata's 20 commits |
| `exp-designer-2` | Run 2. The base `e2f0e99` (the same tree with the second brief), then Ditto's 32 commits |

The bases have no history and no earlier language, so neither designer
could see the calculator.

## The setup

**Orchestration.** One Opus session per run played both the person and
the agent:

1. It wrote the whole design (decisions attributed *(designer)*) before
   any code.
2. It reread the design once, as a builder would, for silences.
3. It handed each step to one fresh sub-agent, in the foreground.
4. It reviewed each step cheaply: the suite under gcc, clang and clang's
   sanitizers, `git diff --stat`, and the builder's flags.

The brief allowed at most 10 steps, step 0 and the examples included.
To save usage, it had no referee and no reviewer agents. The compiler
was fixed at TypeScript on Node 22 emitting C, as in the earlier rounds,
so the runs stay comparable.

**What changed between the briefs.** After Strata the person asked for a
language "more practical but still creative": unusual ideas used
sparingly and only where they serve usefulness. The second brief:

- Asked that someone who writes TypeScript, Python or Go can read the
  examples at first sight. It tests each distinctive idea by whether the
  examples would be worse without it. It mentions an earlier
  too-strange run without naming it.
- Added a sixth example, built around compound data. A workaround in an
  example counts as a design problem.
- Asked the designer to write the six examples before any code, and to
  decide every error and fault per form, message and position. That was
  run 1's lesson: most builder defaults were about errors.
- Required a model for every step that computes values, the distinctive
  idea's step above all. Strata's history tests were written by hand.
- Made Sonnet the default builder. Run 1's Haiku step cost more than any
  Sonnet step.
- Allowed one step for friction the examples showed.

**The prompt**, the same for both:

    Read CLAUDE.md, then docs/briefs/design-and-build.md, and do what the
    brief says: design a language yourself, make every decision, see it
    built step by step through sub-agents, and end with EXPERIMENT.md and
    the summary it asks for. There's no one to ask in this session. Push
    to the branch you were started on.

**The referee and the fuzzer** were added to run 2 while it built, at
the person's word that usage was available. Neither existed for Strata.

- **The referee** was written by an Opus sub-agent from `DESIGN.md`,
  `DECISIONS.md` and `LANGUAGE.md` alone, as they stood at `241062c`,
  during step 7. Every decision was made up front, so the documents were
  complete by then. It never saw the compiler, the runtime, the tests or
  the models. It cost 165K tokens and 11 minutes.
- **The generator** was written by a Sonnet sub-agent from `LANGUAGE.md`.
  It treats both implementations as black boxes. It cost 139K tokens and
  15 minutes.

## Results

| | Strata (run 1) | Ditto (run 2) |
|---|---|---|
| Core rule | every variable is a history: `x <- e` lays a value, `x@k` reads the past | every value is a value: lists and maps copied, never shared; and `a else b` on a missed lookup |
| Steps | 7 of 10 | 10 of 10, the reserve spent on in-place updates (D48) |
| Decisions | 40: 32 up front, 8 builder defaults, all kept | 48: 33 up front, 13 builder defaults, all kept, 2 at review |
| Golden tests | 90 | 572 |
| Unit tests | 37 | 174 |
| Models | 6; the history tests by hand | 9, one per computing step |
| Builders | Sonnet ×6, Haiku ×1 | Sonnet ×9; step 9 by the designer |
| Steps redone | none | none |
| Examples | 5, as asked | 6, unchanged from design time, green on first compile |
| Suite under gcc, clang, sanitized clang | green | green (my rerun: 572 each, checks ok) |
| Referee, golden tests | (none) | 567 of 572 agree |
| Random programs | (none) | 1,993 of 2,000 at step 6; 1,997 of 2,000 with `else` on the final build |
| Wall time | 56 min | 2 h 49 min |
| Session cost, as reported | $7.52 | $23.31 |
| Sub-agent tokens | ~820K | ~1.86M |
| Session | `session_017A3bHUde6RuooFzs1Hz5u8` | `session_017A3bHTuRqqVqfSwbLwqDzM` |

Whether a session's reported cost includes its sub-agents isn't known.

### What the referee found

The 10 disagreements, golden and random, come from three causes. None
is a compiler bug.

1. **Empty statements.** A lone `;` or `;;` is accepted by the compiler
   and rejected by the referee. This covers tests 005 and 234, and 4
   random programs. No decision covers it. The step 0 builder chose it
   and wrote it into a test, but never into the log. The referee listed
   it as its silence S1. *A decision that exists only in a test.*
2. **When D21's "expression statement must be a call" is checked.** This
   covers tests 150, 597 and 693. The compiler checks it in the
   resolver, after the whole file parses, so a later syntax error comes
   first. The referee checks it in the parser. D39 implies the
   compiler's order ("from the parser, before any resolver error") but
   never states it. *A decision worded too loosely.*
3. **A referee bug.** This covers 4 random programs at step 6 and 2 at
   the end. In `print(1)` followed later by `fn print() {}`, the
   compiler correctly reports `print is a builtin` at the definition.
   The referee checks the earlier call against the rejected definition.
   It is left unfixed here, so the results reproduce.

Of the referee's 23 silences, only S1 shows up in any test. The rest are
corners no test or random program reached. The random programs include
copy-then-mutate tests run against the final build, so they are
evidence, not proof, for D48's in-place updates. The designer asked for
a second reader on D48.

## What this says

- **An agent can design a language that holds together.** Both runs
  built green with nothing redone, and no builder default touched the
  semantics. A second implementation from Ditto's documents alone
  agreed on almost everything, every fault message included.
- **Taste is where it needs the person.** Left alone, the designer
  reached for a striking idea and built it faithfully into a language
  nobody would want to write in. One sentence of direction ("practical
  but still creative") produced Ditto, whose two ideas are justified by
  examples. The agent's own lists of what a person should overrule were
  sound both times: Strata's `let` sharing a past, Ditto's missing floats
  and first-class functions.
- **Up-front design costs, and pays.** Ditto's longer design phase, six
  times the tests, and a five-minute suite tripled the cost. What it
  bought: examples green on first compile, builder defaults confined to
  check order and error sites, and a referee that disagreed in two
  places.
- **The best catch was a measurement.** A builder found that a
  1,000-element sort under copy-on-every-update needed about 8 GB. The
  designer spent its reserve step on in-place updates for unshared
  values, and the sort test went from 4.1 s to 0.011 s. No example would
  have shown it.
- **The referee still earns its cost.** It cost a quarter of a step's
  budget, it was written in parallel with the build, and it found two
  holes in the decision log that the designer's own reread missed.

## The experimenter's errors

- The first base was force-pushed onto this session's branch, with the
  person's approval after the push was blocked. Later, a stop hook asked
  for the local branch, still main's history, to be pushed. Pushing it
  would have overwritten the base, so the local branch was reset to the
  remote instead.
- While Ditto was building I took its step 7, `else`, to be `if`'s
  `else` built oddly late. It is the lookup fallback.
- Strata got no referee, so the two runs aren't checked alike.

## Open, for the person

- Ditto's two gaps: whether empty statements are allowed, and D21's
  phase stated outright.
- The designers' overrule lists. Strata: D12, D14, D21, D26. Ditto: D13,
  D14, D20, D22. Also a second reading of D48's soundness argument in
  Ditto's `DESIGN.md`.
- Whether a referee becomes part of the designer brief. On this
  evidence it should.

## Running it again

A base is an orphan commit, as in `exp/interpreter/README.md`; the
brief goes in `docs/briefs/design-and-build.md`. The judge, from this
folder:

    (cd CHECKOUT && make test)
    ./refcheck.sh CHECKOUT "$PWD/referee/referee.py"
    DITTO_ROOT=CHECKOUT fuzz/fuzz.sh 2000 1
    DITTO_ROOT=CHECKOUT GEN_ARGS=--else fuzz/fuzz.sh 2000 5001
