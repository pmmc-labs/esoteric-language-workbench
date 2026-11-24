# What the workbench found

November 2026. The workbench began as the process that built
a64-slight, extracted into a template, and became a set of experiments
on who can do which parts of that process: three tiers of one model
family, three effort levels, and a second family on a laptop. Every
round was run on a small calculator language built for the purpose,
and judged by the same machinery the process uses for real work: the
suite under gcc, clang and the sanitizers, a referee, and a read of the
diff. The records, with their tables, are in `MODELS.md`; this is what
they add up to, and what they don't.

## The process

Eight things made a64-slight work, in the order they mattered:

1. Golden tests whose expected output never comes from the compiler,
   but from a model of the definition, rerun and never patched.
2. Ghuloum's rule: the compiler works at the end of every step, and
   every step adds tests.
3. A decision log that says who decided, why, and what was rejected.
4. Propose before building anything that touches semantics.
5. Examples bend to the language, not the other way round.
6. The person's machine as a second oracle, and a second compiler and
   a sanitizer as two more.
7. A status paragraph as the handoff between sessions, and decision
   numbers threading commits, design, plan and tests together.
8. Determinism in the runtime from the start, so a failure is a fact.

The workbench added four: the referee, a second implementation of the
language from the decisions, run over every test and cross-checked
between proposals; mechanical checks for the rules that can be
mechanical (models rerun, tests paired, commits naming their decision);
a step that names the documents it moves; and briefs that say whether
a smaller builder stops or builds and flags.

## Who can do what

The rounds, each one or two runs per cell, on steps with the checks
complete unless said otherwise:

| Task | Opus | Sonnet | Haiku | qwen3.8:27b, local |
|---|---|---|---|---|
| Build a decided step | yes | yes, every time | yes, every time, at every effort | yes |
| Write a model from decisions with the traps in them | not tried | yes, referee agrees | yes at high effort, referee agrees | yes, referee agrees |
| Fill a thin decision | not tried | writes a default, flags it, builds | the same, the same default | not tried |
| Propose a step with a textbook (arithmetic) | yes; the only one to close the silence builders then met | yes; the most complete text | yes; the most careful about what it may decide | could not hold the design long enough to write it |
| Propose a step with no textbook (a budget) | yes; found a live bug and made it evidence | yes; left one hole on purpose, which made the built language compiler-dependent | yes; two small silences | not tried |

Every build at every tier was green under all three compilers'
builds and touched no test. Every delegated model agreed with the
referee. No tier invented silently when a decision was thin. On the
two proposal rounds, all three Claude tiers produced designs that held
together and built; the silences a builder then had to fill ran 0, 1
and 2 by tier, and the one hole that mattered was a judgement left on
purpose rather than an oversight.

The second family confirmed the two cheaper claims and refused the
third: a 27B model with a 24K context built a step and wrote a model
as well as the smallest Claude tier, at no cost in tokens and ten to
twenty times the wall time, and could not propose a step. It reasoned
the proposal out, correctly, thirty thousand characters of it, and
couldn't hold the result long enough to emit it. That is the local
tier's limit as `MODELS.md` had predicted it: context, not reasoning,
and context meaning the working memory for a design, not the files it
reads. Whether writing as it decides would get it through is untested;
the laptop had reached its limit.

## So, which model for what

- **Build** with the small tier, at low effort if someone reads the
  diff. The checks carry it.
- **Write models and proposals** with the medium tier, on condition
  that a large reader reads the result before the build for the
  silences and the holes left on purpose. The reading is the large
  work.
- **Keep the large tier** for that reading, for the referee's design,
  for decisions with no neighbour in the log to reason from, and for
  what it finds beside the step: twice in these rounds a live bug on
  main that no test had shown.
- **Effort** buys verification outside the tests, not correctness
  inside them: low to build, high to review, model, propose or debug.
- **A local model** builds and writes models from a brief cut to the
  step. It doesn't propose, at this size, this way.
- **The person's picks** stay the source of quality. Every round ended
  with a choice that was theirs, and the one hole in a built language
  was a choice a person would have overruled in a minute.

## What was found along the way

Three bugs the suite had never shown, each found by something other
than a test: an argument-order read under clang, found by the person's
machine; a negative left shift, found by the sanitizer on its first
run; and faults on sibling operands that differed between gcc and
clang, found by a proposer. A referee that was wrong on its first run,
and two of three proposers' referees that would have failed another
proposer's tests, since each was as deep as its author's tests. Three
briefs that turned a flag into a stop, and three small builders that
obeyed. A history leak in an experiment branch, found by the
proposers. And a harness that had to learn, one failure at a time, to
retry, resume, trim its context, cap a reply and carry a cut-off
thought.

## Limits

One or two runs per cell, so these are records and not measurements.
Small features on a toy language, with few interactions. Three tiers
of one family, and one model of a second. The reader of every round
was a large model of the same family as the three tiers, at low effort
for the first rounds and high for the rest. A longer language, a step
with more surface, a second family's larger model, or a second reader
would test any of these, and the branches and transcripts are kept for
whoever runs them.
