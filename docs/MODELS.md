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

**Large, and don't delegate:**

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
