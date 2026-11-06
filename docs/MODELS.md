# Which model, for what

The process was worked out with the largest models available (Opus and
Fable, in a64-slight's case). Most of its rules exist to catch what a
model does unchecked, and those matter more as the model gets weaker,
not less. But some of the work loads capability directly, and a weaker
model given that work produces something that looks right and isn't.
This page says which is which, for choosing a session's model, a
sub-agent's, and when to change.

The one principle: **a downgrade is safe exactly where the checks are
complete.** A weak model's confident wrong answer and a strong model's
right one read the same. The suite, the models and `t/checks.py` are
what tells them apart. Where the work's result is checked by script,
the model's size is a cost question. Where it isn't (a proposal, a
model of the definition, a judgement about a design), the model's size
is the quality.

## Findings so far

Six rounds on this repo's calculator, each one or two runs per cell,
all three tiers of one model family, read by a large model. The
records are below, each with its table; this is what they add up to.

1. **Building a decided step** (design agreed, tests written): every
   tier, every time, at every effort. Six Haiku builds, five Sonnet,
   one Opus, all green under gcc, clang and the sanitizers, none
   touching a test. The downgrade is safe exactly where the checks are
   complete, and the checks were.
2. **Effort** buys verification outside the tests (a hand check of an
   expected value, a sweep, a find beside the step), not correctness
   inside them. Low effort is enough to build; high is for reviewing,
   modelling, proposing and debugging, where the agent's own checking
   is the check.
3. **Writing a model** can be delegated to medium, or small at high
   effort, when the decisions carry the traps and a referee exists.
   Every delegated model agreed with the referee. Without the referee
   the claim couldn't have been made.
4. **Thin decisions** didn't produce silent invention at either tier:
   both wrote the choice as an attributed default with its rejections
   and asked. The decision log's *(default)* is the working fallback
   for a sub-agent that can't ask.
5. **Proposing a textbook step** (arithmetic, from step 0): all three
   tiers wrote a proposal a builder took cold and built green, and all
   three converged on the semantics. The large tier alone closed the
   one silence the builders then met.
6. **Proposing a step with no textbook** (a budget, from one line):
   all three held together and built green, agreed on the hard parts,
   and differed only on choices each had flagged. Silences ran 0, 1
   and 2 by tier. The large tier found a live bug on main while
   proposing and made it the evidence for a decision; the medium tier
   left one hole on purpose, with its reason, which made its built
   language nondeterministic between compilers.

So, which model for what: build with the small tier; write models and
proposals with the medium tier when a large reader will read the
result for silences and deliberate holes before the build; keep the
large tier for that reading, for the referee's design, and for
anything where what's found beside the step matters. The person's
picks stay the source of quality: every round ended with a choice
that was theirs.

What the process gained from the rounds, beyond the model guidance:
the referee, and the cross-check between referees; a referee as a
loop; a brief that says stop or flag; a rule that a step names the
documents it moves; a history-free branch for experiments; and three
bugs the suite had never shown (an argument-order read under clang, a
negative left shift, and compiler-dependent faults on siblings), each
found by a second compiler, a sanitizer, or a proposer rather than a
test. The limits hold throughout: one run per cell, small features,
one family.

## Tiers

- **Large**: the frontier model of the day (Fable, Opus). Sustained
  reasoning across layers, holds a long context, writes a model of a
  definition rather than of the implementation.
- **Medium** (Sonnet): good at a described task; thinner proposals,
  weaker at debugging that crosses the compiler, the runtime and the
  tests at once; tends to the first fix that turns the test green.
- **Small** (Haiku): an executor. Fine with a pattern to repeat and a
  check to satisfy; shouldn't be asked to decide anything.
- **Local**: a small model, and a short context on top. Treat as small,
  with the documents cut down to what the step needs (`CLAUDE.md`
  without the Status, the step's text, the decisions it cites, and
  nothing else).

## Tasks, by what they need

**Large, and don't delegate** (tested once, on a step with textbook
semantics, where the medium and small tiers did it too; see
"Proposing a step"):

- The referee (`PROCESS.md`), when a step's proposal says one is
  wanted, and that decision itself: it's what makes a delegated model
  checkable, so it can't be delegated to the same tier.

- A proposal: options, a recommendation, what each costs. This is where
  the person's decision is only as good as what they're shown.
- Anything touching the core rule, the collector, the scheduler, the
  calling convention, or a value's encoding.
- Writing a model in `t/models/`. The failure mode is a model that
  mirrors the implementation; it's hard to see and worth nothing.
  Read every model a smaller model writes as if it were the
  implementation.
- Debugging where the symptom and the cause are in different layers
  (a wrong output from a missed root; a race shown by one scheduling
  seed), and anything a seed sweep or a replay found.
- Deciding whether a reported misbehaviour is a bug (the independent
  implementation rule).
- A review of a step's diff against its decisions, when one is wanted.

**Medium, with the step written first:**

- A plan step whose design is agreed, whose tests are named, and whose
  expected outputs exist or come from a model already written.
- A new form or builtin that mirrors an existing one (a sixth operator
  beside five; a `bytes/` function beside its `str/` twin).
- Porting an example, under "examples bend to the language": the agent
  must stop and report when the port wants a feature, not add one.
- `LANGUAGE.md` and guide prose for a feature that's landed.
- A prelude function with a sig and tests given.
- A unit test for a stated case.

**Small, where a check says when it's done:**

- Reruns and sweeps: `make models`, a seed sweep, the suite under a
  stress knob, and a report of what failed.
- A rename or a mechanical edit across files, with the rule that each
  replacement is asserted (the script does the work; the model writes
  the script and reads its output).
- Expected output by hand for a test whose output is obvious, with the
  rule that it's worked out from the program, not run.
- Searching: where a name is used, which tests cover a form, what a
  decision says.
- Formatting, and the Status paragraph's wording from a list of what
  landed.

## When to escalate

Stop and hand up (or, in a session, say so and wait) at any of these.
Each is a point where a smaller model will press on and be wrong:

- The fix you're drawn to is editing an `.expected` file, or a model.
- Two attempts and the suite is still red for the same test.
- The step needs a decision that isn't in `DECISIONS.md`, or meets an
  **(open)** item.
- The change touches the core rule or any layer listed under large.
- A model and the compiler disagree and you can't say which is right
  from the definition. (In this repo's own step 1 the model was wrong.
  It happens both ways.)
- The diff has grown past what the step describes.
- A port needs a feature, or a test needs a special case in the
  compiler to pass.
- A seed sweep, a replay or a stress knob fails and the plain run
  passes.
- You're about to add a flag, an environment variable or a knob.

## When a downgrade is safe

- The step's text names the files, the tests and where their expected
  output comes from, and the design is a `Dn` already.
- A step of the same shape has been done before and can be read as the
  pattern.
- The change is additive: no existing test's expected output moves.
- Nothing marked (open) is in reach.
- The result is checked by `make test` with nothing left to judgement.

If all five hold, medium does it; if the step is a repeat of one just
done, small does it. If any fails, large.

## Per session

Each step in `PLAN.md` carries a **Size** line, set when the step is
written (by a large model, since writing the step is itself a large
task: it's the proposal). A session's first move after reading
`CLAUDE.md` is to compare the step's size with its own model and say
so: "this step is marked medium; I'm larger than it needs" is a reason
to pick a cheaper session next time, and "marked large; I'm Sonnet" is
a reason to stop before building and ask. The Status paragraph can say
what the last step was built with, so a pattern shows.

## Sub-agents

The lead is large: it holds the step, the decisions and the judgement.
It delegates:

- To medium: independent sub-steps whose tests are already written,
  in parallel, each with the files it may touch named. The lead reads
  the diffs, not the summaries.
- To small: sweeps, searches, reruns and reports. A report is data; the
  lead checks anything surprising before acting on it.
- Never: the proposal, a model, the decision log entry, or a fix to
  something a sub-agent reported broken and the lead hasn't seen fail.

A sub-agent returns a summary, and summaries hide what went wrong. The
lead's check is the suite, not the summary. A sub-agent that reports
"all tests pass" after editing an `.expected` has done the one thing the
process forbids, and only `make checks` or a read of the diff catches
it. Ask for the diff.

## What happened, once

Step 2 of this repo's calculator, marked medium, with D11 to D14
decided and tests 020 to 024 written and red, was built cold by Sonnet
and by Haiku, each in a worktree from the same commit, with the same
brief: read CLAUDE.md, the step and its decisions, build, report. One
run each, so this is a record, not a measurement.

| | Sonnet | Haiku |
|---|---|---|
| Green under gcc, clang and the sanitizers, nothing under `t/` touched | yes | yes |
| Lines changed | 75 | 121 |
| Tool calls, time | 11, 1.2 min | 31, 3.4 min |
| Docs moved (the step didn't say to) | no, and said so | yes |
| Uncertainties reported | 3, all real | 7, all real |

Both runtimes were right, and alike: the tag check as a statement
before the operation (both had read the clang lesson in CLAUDE.md),
`if` as a special form on a runtime test, equality by bits with a
comment saying why that's D12. Both chose codegen over the reader for
`#true` and said so.

Haiku found a bug outside the step that Sonnet and the step's author
had missed: the operator table was a plain object looked up with `in`,
so `toString` was an operator and `(toString 1 2)` emitted JavaScript's
function source into the C. It fixed it, said in the commit that the
fix was outside the step, and added a test. It also saw that the step
touched a value's encoding, which this page lists under large, said so,
and built anyway with the reason that D14 fixed the bits: the right
call, made for the right reason, and reported for the person to check.
And it raised two design questions a large model should have raised in
the proposal: which fault reports when both arguments of a call fault,
and that bitwise `==` won't survive heap values.

Sonnet, in an earlier launch that handed it the wrong repository by
mistake, read the plan, found no such step, listed what it had
checked, built nothing and asked. That's the escalation behaviour
above, unprompted.

What this says against the tiers above: on a step with the design
decided and the tests written, the small tier was not merely adequate
but found more; the cost was three times the tool calls and a wider
diff to read. The claim that held is the principle at the top: the
downgrade was safe because the checks were complete. The claim that
didn't is "small shouldn't be asked to decide anything": it decided
well twice, and the difference was that it reported each decision.
Two things the experiment can't say: how either does when the model
in `t/models/` isn't written yet, and how either does on a step that
goes wrong.

## Effort

Effort is a second axis, separate from size: size is what the model
can see, effort is how long it looks. The two split the escalation
signals above. Raise effort first when the symptom is that the agent
isn't verifying: a fix that turned one test green and broke nothing it
ran, a diff not read back, a report thinner than the work. Raise size
when the symptom is that it doesn't see it: a wrong model of the
definition, a design question not raised, a bug it can't place across
layers. Effort won't supply what a model doesn't know; size won't make
it check.

### What happened, once more

The same step 2, built cold by Haiku three times from the same commit:
at low effort, at the default, and at high. One run each.

| | Low | Default | High |
|---|---|---|---|
| Green under gcc, clang and the sanitizers, nothing under `t/` touched | yes | yes | yes |
| Lines changed | 89 | 121 | 110 |
| Tool calls, time | 16, 1.6 min | 31, 3.4 min | 48, 3.5 min |
| Tokens | 100K | 152K | 151K |
| The `toString` bug outside the step | missed, and copied the pattern into its new constants table | found and fixed, saying so | found, left out of the step, recommended a fix |
| Checked 020's expected value by hand from the definition | no | no | yes |
| Checked the fault-order question under both compilers before raising it | no | no | yes |
| Uncertainties reported | 6, all real | 7, all real | 7, all real |

All three runtimes were correct, and the low-effort one the most
careful about the clang lesson, reading each operand into its own
statement. What effort bought was not correctness, which the tests
held at every level, but verification outside the tests: the hand
check of an expected value, the compiler-by-compiler check of a
question before raising it, and the find outside the step. High and
default cost the same tokens; high spent them on half again as many
tool calls, which is where the checking shows. Low cost two thirds and
was blind to what the step didn't name.

### Guidance

- **Building a step whose checks are complete**: low effort is enough
  for correctness, and the cheapest. What it loses is anything the step
  didn't name, so a diff built at low effort wants a read by someone
  who will see what's beside it.
- **Reviewing a diff, writing a model, a proposal, a debug**: high.
  These are the tasks where the agent's own checking is the check, and
  high effort is more checking.
- **Sweeps, searches, reports**: low.
- A step's `Size` line stays; add an `Effort` line only where it isn't
  the default, which is for the tasks under high above.
- Small model at high effort against medium model at default: on this
  step, the small model at high found more and cost less. That's one
  comparison on one step, with the design decided and the tests
  written; it says nothing about a step where they aren't.

## Writing a model, delegated

The page above says a model is large work and not to delegate it,
because the failure mode, a model that mirrors the implementation, is
quiet. That was tested on step 3, bit operations, with D15 to D17
decided and nothing else: no model, no tests. The step told the
builder to write `t/models/bits.py` and its tests first, from the
definition, then the code. Sonnet at default effort and Haiku at high
each did it cold from the same commit. One run each.

The judge was a referee written beforehand and kept out of the repo:
an evaluator of the whole calculator in Python, from the decisions,
checked against the thirteen existing tests before it judged anyone.
It disagreed with one, and the referee was wrong (it range-checked a
quotient on the way to a remainder, which D5 doesn't), which is the
check a referee needs too. The decisions were written with the traps
a mirror of C falls into: a shift count checked rather than masked, a
left shift that faults rather than wraps, and a right shift that
rounds toward negative infinity where division truncates.

| | Sonnet | Haiku, high |
|---|---|---|
| Model from the definition, not the runtime | yes | yes |
| Expected outputs agree with the referee | 11 of 11 | 7 of 7 |
| Green under gcc, clang and the sanitizers | yes | yes |
| Tool calls, tokens, time | 12, 95K, 2.0 min | 43, 172K, 5.8 min |
| Edge values, shift counts | 11 values, 7 counts | 13 values, every count |
| Model and tests committed red before the code | no, one commit | yes, two commits |
| Hit clang's 256-bracket limit on a linear fold, fixed in the model | yes | yes |
| Noticed the same limit applies to a user's program | no | yes, and left it for a decision |

Both models were real: Python's unbounded integers, the right shift
as floor division rather than `>>`, the left as multiplication with
the range checked after, the count checked first. Neither borrowed
from `rt.c`. Both runtimes avoided the two undefined-C traps, by
different routes (complement and shift back; divide and correct). Both
ran their tests red before building, as the step asked. Both raised
the open question the decisions leave, which fault reports when a call
could fault two ways, and neither decided it.

So, against the page's own claim: a model can be delegated to the
medium tier, and to the small tier at high effort, when the decisions
are written with the traps in them and a referee exists. The
condition is the point. The decisions did the large work (saying what
a shift by 63 does, and that `bit/shr` isn't `/`), and the referee
made the result checkable. Without the first, a model has nothing to
compute from but the code; without the second, a mirror passes. What
remains large is writing the decisions that way, and the referee.

What the experiment can't say: how either does when the decisions are
thin, which is the usual case before a step is proposed, and that's
where a mirror would come from.

## Thin decisions

The step 3 result rested on decisions written with the traps in them.
Step 4 took that away: exponentiation, with one line of decision,
D18, "`(** a b)`, a to the power b, on two integers", and a step that
named the model and the done condition and nothing else. What D18
leaves open is real: a negative exponent, zero to the zero, overflow,
a huge exponent with a base of 0, 1 or -1 where a naive loop never
ends. Under the working rules the move is to stop at "the step needs a
decision that isn't in `DECISIONS.md`". Sonnet at default and Haiku
at high, cold, one run each.

| | Sonnet | Haiku, high |
|---|---|---|
| Noticed the gaps | all | all |
| Decided silently | no | no |
| Wrote the choice as a `Dn` marked default, with rejections, and asked for it to be confirmed | yes, D19 | yes, D19 |
| The choices | negative exponent faults `bad exponent`; `0 ** 0` is 1; overflow by D4 | the same |
| Model from the stated definition; expected outputs agree with the referee | 6 of 6 | 4 of 4 |
| Green under gcc, clang and the sanitizers | yes | yes |
| Tool calls, tokens, time | 14, 99K, 1.9 min | 45, 184K, 12.5 min |
| Beyond the step | a test that a huge exponent doesn't hang | a 7,000-case sweep of the runtime against the model under UBSan, not committed |
| Misreads | called itself the large tier | none |

Neither stopped, and neither could: a subagent has no one to ask.
What both did instead is the process's own fallback, the *(default)*
attribution in `DECISIONS.md`: decide, write it down as a default with
the reasons and what was rejected, and put it first in the report for
the person to confirm or change. Both chose the same answers, by the
same analogy (D16's rejection of a masked shift count), without
seeing each other. Both ran their tests red before building. Both
wrote the runtime by squaring, so a huge exponent takes 62 steps, and
both argued in a comment why an intermediate overflow implies the
result's.

So on thin decisions the risk this page feared, a silent invention,
didn't happen at either tier, and what happened instead was the right
fallback. Two things to hold onto. First, a default that's been built
on is harder to revisit than one that's only proposed, since tests
now encode it; the person's confirmation of D19 is a real step, not a
formality, and the brief should say which the agent is to do, stop or
default, since in a session with a person it should stop. Second,
this was a decision with an obvious best answer by analogy to one
already in the log. A thin decision with no neighbour to reason from
is the case that's still untested.

## Proposing a step

The large work itself, tested once: the repo as it stood at step 0,
with the process as it is now and every record of steps 1 to 4 cut
(the branch `exp-step0`), given to Opus, Sonnet and Haiku, each at
high effort, cold, with one task: propose the next step and don't
build it. The deliverable was what `PROCESS.md` calls large work: the
decisions marked default with their rejections and the traps decided,
the step's text with its Referee and Size lines, the referee if
wanted, and a brief a builder could be handed. Then each proposal went,
unchanged, to the builder its own Size line asked for. One run per
cell. The reader of all of it was Fable at low effort.

A flaw in the setup, found by the proposers: the branch kept its git
history, and all three looked at `git log`. The commit subjects named
the four steps and that overflow was checked at run time. The step
choice was obvious from D1 anyway; the traps, the referee, the tests
and the brief were theirs. Opus noticed the history, refused to read
it, and forbade its builder to. `exp-step0-clean` has no history, for
next time.

### The proposals

| | Opus | Sonnet | Haiku |
|---|---|---|---|
| Tokens, tool calls, time | 136K, 19, 7.2 min | 132K, 23, 5.9 min | 170K, 24, 6.1 min |
| The step | five operators | five operators | four, `%` left out with a reason |
| Decisions | 6 | 8 | 9, numbered from D20 around the history |
| Traps decided (division rule, zero divisor, min / -1, overflow at 63 bits, evaluation order) | all | all | all |
| Compile errors with messages and positions decided | yes | yes | yes |
| The order of compile errors within one form decided | yes (D13: shape, then operator, then operands) | no | no |
| The integer literal's rule a decision of its own, with the warning that a model's `int()` takes more | folded into D13 | yes (D9) | `+5` only (D22) |
| Straight-line C, a temporary per operand, settling C's argument order and clang's bracket limit at once | yes | yes | yes |
| Tests planned, and where their outputs come from | 17: 2 by hand, 15 from a model | 29: 26 worked by hand in the step text, 3 from a model | 16, all from a model |
| Referee | written; cross-checked against C with a 128-bit range on 51,000 pairs | written, iterative, so 1,000-deep programs work | written; self-checked on 30 cases |
| Size line | medium, effort high, with the argument | medium, with the argument | large, saying it wasn't a large-model proposal |
| The brief's gate | stop if the builder is smaller than the Size | the same, and "decide nothing; stop" | the same, and stop unless the person has picked the decisions |
| Forbids the builder the git history | yes | no | no |
| Referee survives 1,000-deep programs | no, recursive | yes, a loop, because its own tests go that deep | no, recursive |

All three referees agree with each other and with this repo's on every
trap. All three decided the same semantics, by the same reasoning,
differing in the fault's name and in whether `%` came now. Read closely
(at high effort, after the first write-up at low), the three differ in
more than length:

- **Opus** decided the one thing the other two left: the order in which
  a form's errors are reported. Both other builders hit exactly that
  silence and decided it themselves. Its test 012 weights the four sign
  cases of division so that a floored one shows in a single number, one
  test for the trap. Its rejections are argued to the point where the
  reader can see why: variadic `+` is "four decisions for a shorthand".
- **Sonnet** made the integer literal's rule a decision, with the
  warning a model needs about Python's `int()`, which the others left
  to an aside. Its D14, with the depth its tests reach and where Node's
  stack gives out, is the most concrete. Its weak spot is the generated
  test `mixed`: the step said "about 300 operations, a generator written
  out", and left the rest to the builder, who then chose a seed by
  taste and rejected one whose value came out 0. The content of a
  golden test came from the builder's judgement, which is the thing a
  model exists to remove; the referee covered it, but a proposal fixes
  the generator or drops the test. Its D15 keeps `can't compile symbol
  yet` as a permanent message.
- **Haiku**'s reason for leaving `%` out doesn't hold: the rule it says
  `%` would need, the dividend's sign, is a line, and its D24 already
  took the harder half of the same decision. Its sixteen programs are
  the best-chosen set of the three (`mul-wraps` for the 64-bit wrap,
  three orderings for the fault order), and all of their expected
  outputs come from the model, so the person has nothing to read by
  eye. Numbering from D20 around the history was reasonable and leaves
  a note in the log that refers to history the log otherwise doesn't.

Two complaints the builders made were not the proposers' errors: "the
thirty commands" for fifteen tests was right, two a test, and the
builder miscounted; and the wrong paths in Haiku's brief came from the
experiment's own setup, the brief written in one worktree and built in
another.

### The builds

Every proposal first went to Haiku at high effort, as the earlier rounds
had, and all three Haiku builders stopped at the brief's gate without
building: each read its tier, read the Size line, and reported. In the
earlier rounds, on briefs this repo's author wrote, Haiku flagged the
mismatch and built, correctly every time. The difference is the
briefs: three proposers, independently, turned CLAUDE.md's "say so and
escalate rather than press on" into a hard stop, and the builder
obeyed. Three stopped runs cost 260K tokens and built nothing. Then
each proposal went to the builder its Size line named, Haiku's after
the person accepted D20 to D28 as proposed, since its gate required it.

| | Opus's, built by Sonnet | Sonnet's, built by Sonnet | Haiku's, built by Opus |
|---|---|---|---|
| Green under gcc, clang and the sanitizers | yes | yes | yes |
| Golden tests | 19 | 31 | 18 |
| Builder's model agrees with the proposer's referee | 19 of 19 | 31 of 31 | 18 of 18 |
| Decisions the builder found missing | none | none | none |
| Silences the builder filled and reported | none | three orderings among compile errors; how the random tree is drawn | the order of errors within one form |
| Tokens, tool calls, time | 112K, 19, 2.9 min | 131K, 31, 7.7 min | 125K, 28, 5.1 min |

No builder had to decide a semantic. What was left to them was the
order of compile errors, which Opus alone had decided, and the
construction of a generated test, which Sonnet's step had left open.
Sonnet's builder decided both and reported them, against its own
brief's "decide nothing; stop": the flag-and-build fallback won over
the brief's words, which is what this page now says it should as a
sub-agent, and the brief should have said.

### What this says

On this step, every tier wrote a proposal a builder could take cold,
with the traps decided before the builder met them. Most of the
differences were in thoroughness: Sonnet's step text, with its 26
hand-worked outputs, was the one to hand over; Opus's referee was the
most verified; Haiku's was the most careful about what it wasn't
entitled to decide, and the only one that made the person's picks a
gate. One difference was in kind, and it went the way the tiers
predict: the one silence a builder had to fill, Opus had closed and
the others hadn't. That's small on this step, where the silence was
the order of error messages. On a step whose silences are semantics,
it's the whole job. Against this page's claim that proposals are large work and not
to delegate: on a step with textbook semantics, that was too strong.
Integer arithmetic has a right answer every tier knows, and no
proposal had to invent. Whether that holds for a step whose semantics
are the language's own, with no textbook to reason from, is the case
that's still untested, and it's the case the claim was about.

The finding that wasn't looked for: the briefs. A rule written as
"flag and escalate" in CLAUDE.md became "stop" in three briefs, and a
small builder stopped three times on steps it had built correctly
before. A brief should say which it means. For a sub-agent with no one
to ask, flag and proceed is the cheaper default, since the suite and
the referee catch what a smaller builder gets wrong; stop is for a
session where a person can answer.

Two small things the round found. A referee is as deep as its
proposer's tests: this repo's and two of the three proposers' were
recursive and fail past about 1,000 levels, and would have failed
Sonnet's tests; only Sonnet's, whose plan said its tests nest 1,000
deep, was a loop. This repo's is a loop now, and `PROCESS.md` says a
referee is written as one. And `make hooks` in a worktree writes the
hook into the main checkout's git directory, which every builder
reported as a write it was told not to make.

## The untested case, run

The round above was repeated on a step with no textbook: a budget,
`(within n expr)`, one line of decision from the person (D20) on the
calculator as it stood after step 4, on an orphan branch with no
history (`exp-step5`). Opus, Sonnet and Haiku, each at high effort,
cold, proposed it: decisions, step text, referee, brief, no build. Then
Sonnet at high effort built all three, since every Size line said
medium for the build and one builder for all keeps the builder out of
the comparison. One run per cell, read at high effort.

What D20 leaves open, and nothing in the repo answered: what counts as
an operation, how `**` counts when the runtime loops for it, what a
budget inside a budget means, a budget of zero, the branch an `if`
doesn't take, a fault inside a budget, what `n` may be, the fault's
name. None of that was in the branch; the proposers found the questions
themselves.

### The proposals

| | Opus | Sonnet | Haiku |
|---|---|---|---|
| Tokens, tool calls, time | 205K, 47, 23.6 min | 195K, 39, 14.5 min | 208K, 32, 8.4 min |
| What an operation is | the seventeen operators; `if`, `within` and atoms free; `**` one | the same | the seventeen, and each `if` taken, one each |
| The charge | after the operands, before the operator's own checks | the same | the same |
| Nesting | every budget in force, the lowest governs, the inner's unused part dropped | the same | the same |
| `n` | any expression, evaluated outside its own budget; a boolean `not an integer`, a negative `bad budget` | the same | a literal, 0 or more; else a compile error |
| The order of a call's operands | decided, left to right, with the evidence that gcc and clang disagree on main today | left unspecified, named as a step of its own, and tests with two faulting siblings forbidden | decided, left to right, and the order of one operator's own checks too |
| The generated C | C's comma operator with two temporaries where both operands are lists; nothing else changes | a static C function per `within`, no sequencing of operands | straight-line statements, a temporary per operand, which retires the bracket limit |
| The fault's name | `budget spent`, `bad budget` | `out of budget`, `bad budget` | `budget spent` |
| Tests | 20, all by hand; every operator once in one program | 22, all by hand; checked in a prototype against eight deliberately wrong runtimes | 13 by hand and one from a model the builder writes |
| The referee checked against | a prototype on 1,200 random programs under gcc and clang | the prototype and the eight mutants | its author, on 30 cases |
| Size | medium | medium | large for the model, medium for the build |

The three agree on the parts that were hardest to see: where the
charge falls, which decides `(within 0 (/ 1 0))`; that every budget in
force applies; that `**` is one operation however it's computed; that
a budget of zero allows a program with no operations. They split on
three choices, and each proposer flagged its own choice as the one the
person should look at: whether an `if` costs, whether `n` is a literal,
and what the fault is called.

The one real divergence is the order of operands. Opus found, while
proposing, that the language on main is already nondeterministic:
`(+ (/ 1 0) (+ #true 1))` faults `not an integer` under gcc and
`division by zero` under clang, and no test had noticed because none
had two faulting siblings. It decided the order and wrote the bug into
D25 as the reason. Haiku decided the order too, from the general
lesson in CLAUDE.md. Sonnet saw it, judged the codegen rewrite a step
of its own, and forbade tests that would expose it. Under a budget that
isn't a corner: in Sonnet's built language `(within 1 (+ (* 2 3) (/ 1
0)))` faults `division by zero` under gcc and `out of budget` under
clang, and the suite passes under both.

### The builds and the cross-check

| | Opus's | Sonnet's | Haiku's |
|---|---|---|---|
| Green under gcc, clang and the sanitizers | 46 tests | 48 tests | 40 tests |
| Builder's tokens, tool calls, time | 111K, 18, 3.5 min | 119K, 24, 4.0 min | 138K, 33, 6.4 min |
| Silences or errors the builder met | none | one error: D27 claimed its lifted functions reported compile errors in reading order, and they didn't; the builder fixed it and reported it | two silences: a budget literal past the integer range, decided and reported; when an `if` is charged relative to its test, decided without noticing it was open |
| gcc and clang agree on the built language | yes | no | yes |

Each proposal's referee was then run over every build's tests, with
the two fault names treated as one. Opus's and Sonnet's agree on all 94
of each other's tests. Both differ from Haiku's on one test, the one
that charges an `if`. Haiku's differs from theirs on seven each, every
one a test that charges an `if` or computes `n`. Three derivations of
semantics nobody had written down, and nothing hidden between them:
every disagreement is one of the three flagged choices.

### What this says

The prediction was that on a step with no textbook, the silences a
builder has to fill would separate the tiers, and the large tier's
decisions would hold together where the others' left holes. The
gradient is there and it runs the predicted way: no silence in Opus's,
one wrong claim in Sonnet's, two silences in Haiku's. It's smaller than
predicted, since all three held together and all three built green.
The one hole that matters, the order, was Sonnet's, and it wasn't an
oversight: it was weighed, named, and left, with the reason that the
fix was a rewrite. That is a judgement a person can overrule in a
minute, and it's exactly the judgement the proposal exists to put in
front of them. What the large tier did that the others didn't was find
the live bug on main and make it the evidence for the decision.

So the claim at the top of this page survives, narrower. Proposing a
step whose semantics are the language's own can be delegated to the
medium tier, and the small tier's was buildable too; the result will
hold together and build. What the large tier adds is in what's left
open and in what it finds beside the step, and that's what a large
reader of a delegated proposal looks for before the build: the
silences, the holes left on purpose, and whether the reasons for them
hold. The reading is the large work. Writing the referee held at every
tier, and the cross-check between referees is what made the
convergence a fact rather than an impression; it costs minutes and
should follow every round of this kind.

Limits: one run per cell; a small feature with few interactions; and
three tiers of one family, whose agreement may be shared training as
much as reasoning. A feature with more surface, or a second family,
would test both.

## A second family

Every round above is one model family, and the convergence between its
tiers may be shared training as much as reasoning. The same rounds on
a model served by ollama on a laptop, through a plain loop of our own
so a failure is the model's or the brief's (`exp/local/`, its README),
are the test of that, and of this page's claim about the local tier:
that context, not reasoning, is its limit, and the documents are cut
to the step. The record of each run is in `exp/local/runs/`.

### Round 1: building step 2

`qwen3.8:27b` on an M2 Max with 32 GB, through `exp/local/agent.py`,
from the commit the Claude builders had, with a brief of 1,300 tokens
standing in for CLAUDE.md, the plan and the decisions
(`exp/local/brief-step2.md`). One run.

| | qwen3.8:27b, local | Sonnet | Haiku, high |
|---|---|---|---|
| Green under gcc, clang and the sanitizers, nothing under `t/` touched | yes | yes | yes |
| Lines changed | 78 | 75 | 110 |
| Tool calls, model turns | 21, 13 | 11 | 48 |
| Wall time | 14.4 min | 1.2 min | 3.5 min |
| Tokens | 296K prompt (the context resent each turn, 23K on average), 9K output, 15K characters of thinking | 122K | 151K |
| Uncertainties reported | 3, all real: equality by bits, the `if` message's wording, parenthesising the branches | 3 | 7 |
| Found the `toString` bug beside the step | no | no | yes |

The diff reads like the better Claude builds: the tag check as a
statement before the operation, `if` as a special form on a runtime
test with its branches parenthesised, equality by bits with the
argument why written in the comment, every comment citing its
decision. It read the three files and the tests first, ran the
baseline, wrote the runtime, then the compiler, appended the unit test
with a heredoc rather than rewriting the test file, ran all three
checks, confirmed nothing under `t/` moved, committed with the right
subject, and stopped. The three uncertainties it reported are the same
three the Claude builders reported on the same step.

Two things to hold against it. It rewrote `rt.c`, `rt.h` and
`codegen.ts` whole with `write_file`, since the loop has no edit tool,
and reproduced the untouched parts exactly; on a longer file that
would have been the risk. And the brief said nothing about tiers, so
the size check never came up: the local tier was told only the step.

What this says: the process carried, on a decided step with complete
checks, to a model that shares no training with the family the rounds
were built on, at a quarter the size of the smallest tier tried and at
no cost in tokens. The convergence inside the family on this kind of
step was not only shared training. And the prediction about the local
tier held in its first half: the documents cut to the step were
enough, and the context never overflowed. Rounds 2 and 3, the model
and the proposal, are where the other half is tested.

### Round 2: writing the model for step 3

`exp/local/brief-step3.md`, from the commit where step 3 has its
decisions and nothing else (`936aec3`): the model first, committed
red, then the build. The same model and machine; a brief of 1,800
tokens, with the rules for a model and D15 to D17, and the instruction
not to read the runtime's bit code for the answer. One run, in two
pieces: the first attempt died at step 8 when ollama ran out of GPU
memory (the server was set to a 64K context and the prompt had reached
51K tokens), and the run was resumed from its transcript with the loop
trimming old results and no longer resending the model's thinking.

| | qwen3.8:27b, local | Sonnet | Haiku, high |
|---|---|---|---|
| Model from the definition, not the runtime | yes | yes | yes |
| Expected outputs agree with the referee | 6 of 6 | 11 of 11 | 7 of 7 |
| Green under gcc, clang and the sanitizers; nothing existing under `t/` changed | yes | yes | yes |
| Model and tests committed red before the code | yes | no | yes |
| Tool calls, model turns | 46, 37 | 12 | 43 |
| Model time | 50 min | 2.0 min | 5.8 min |
| Edge values, shift counts | 9 values, 6 counts | 11 values, 7 counts | 13 values, every count |
| Hit clang's bracket limit and folded as a tree | folded as a tree from the start, told to by the brief | yes, found it | yes, found it |

The model is what the brief asked for: Python's integers, `&`, `|` and
`^` as they are, the left shift as multiplication with the range
checked after, the right shift as floor division with the comment that
it rounds the other way from `/`, the count checked first; the faults
written by hand with a note that the model has no booleans, as Sonnet's
had. The referee agrees with every file it wrote.

Two things in the transcript are worth more than the table. First, the
model's first fold computed the sum of the terms reduced once at the
end, and the program it emitted reduced at every node; with the
language's signed remainder those differ, and the compiler's output
disagreed with the expected file. The model-writer worked out that the
model had misread its own program and changed the model's arithmetic,
not the expected file: the compiler was the signal, the program's text
the authority, and the referee the confirmation. That is the same
shape as this repo's own step 1, where the compiler found the model's
fold overflowing. Second, its floor division took three attempts: the
first negated the dividend and the sanitizer caught the overflow at the
minimum, the second was off by one and a test caught it, the third was
right. Each wrong attempt was caught by a check the process had put
there, and the report says so in order.

It also edited the source files in place this time, with anchored
Python scripts, rather than rewriting them whole as in round 1; the
brief's line about context may have done that. The context estimate
stayed between 6K and 12K tokens for thirty turns after the resume.

What this says: writing a model from decisions with the traps in them
carried to the second family too, with the referee agreeing on every
output, and the one correction the model-writer made was the right
kind. The cost was time, fifty minutes of model time against two for
Sonnet, and a run that needed the harness to keep its context in
bounds, which is the local tier's limit as this page predicted it.

### Round 3: proposing a step

`exp/local/brief-propose.md`, from `exp-step0-clean`: the repo at
step 0 with no history, D1 and D2, and a brief that says what a
proposal is, since the local tier doesn't read `PROCESS.md`.

The first attempt failed, and the failure is the finding this round was
most likely to give. The model spent nineteen turns reading: every
document, every source file, the test runner, the checks, and then the
same files again, since the loop had cut them from its context after
four newer results and it went back for what it had lost. On the
twentieth turn it generated for an hour without a tool call, the same
text over and over (the speculative decoder's acceptance rate was 99%,
which is what repetition looks like), until the request timed out, with
the machine swapping. A build needs the step and three files in view; a
proposal needs the decisions, the plan, the code and the test
conventions all at once, and a 27B model with a 24K context couldn't
hold them, which is what this page's "Local" tier said: the limit is
context, not reasoning. The loop was changed to cut results only when
the context is actually near its budget and to cap a reply's length,
and the round is to be rerun; the first run's transcript is kept
(`exp/local/runs/qwen-propose-1`).

## What to expect, by tier, on this process

- **Large**: the process as written. The person's time goes to
  proposals.
- **Medium**: works, with smaller steps, and the person reading every
  model and every proposal closely. Native code and runtime work are
  where it strains; keep the compiler emitting C longer.
- **Small**: as the builder of steps a large model wrote, with the
  checks installed as hooks. Not alone.
- **Local**: the same, with the documents cut to the step and the
  steps cut to an hour. The limit is context more than reasoning: a
  model that has lost the rules by the middle of a session is a model
  without the process.
