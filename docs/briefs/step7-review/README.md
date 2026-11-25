# The review of step 7's proposal, the collector

2026-11-25, by a reader who didn't write the proposal
(`docs/PLAN.md`, "7. The collector"), before anything was built. The
question was the rule for a large step: a sequence of operations that
frees a string still in use, or keeps garbage without bound, under the
design as proposed.

**No program was found that frees a string in use.** The rule held on
every golden test of steps 0 to 6, run on a prototype of the design
with a collection at every allocation. What was found is in the test
plan and in four sentences of the proposal that today's code doesn't
bear out; the findings are in the report that went back to the builder,
and the numbers behind them are here.

## What is here

- `gen.ts`: the generated C of every golden test that compiles, the
  driver's first half and no more.
- `proto.py`: the prototype. It patches a **copy** of `runtime/rt.c` and
  `rt.h` (each patch asserts that it matched; nothing in `runtime/` is
  touched) so that a number as a string is on the C stack, there is a
  collection before every allocation, and a string nothing reaches is
  poisoned, marked dead and never handed out again. It rewrites each
  test's generated C two ways and runs both:
  - **scoped**: every `rt_value` local registers itself as a root for
    as long as its C block is open. Fewer roots than the proposal has,
    so a program right here is right there.
  - **frame**: the proposal's layout, by macros: no `rt_value` locals;
    a variable is the slot of its depth among the variables in scope, a
    temporary is the slot after the variables with its number in its
    statement, shared by every statement, never cleared; every slot is
    a root, stale or not.
  Then the mutations, each by an environment variable the copy reads:
  a root not looked at (all, the variables, the temporaries, the last
  slot of each kind, the first), a collection at every 2nd, 3rd and
  10th allocation, the dead-string check in `to_str` alone as the
  proposal words it, the operands checked again after the allocation,
  which the proposal doesn't have, a `my` that leaves its slot as it
  found it, and a frame whose temporaries begin on its deepest variable.
- `report.txt`: what `proto.py` printed, 275 tests each way.
- `shapes.py`: every line of that C against the shapes the proposal's
  third place needs (a call's result is stored before anything else
  runs; an argument is never a call's result; a pointer points at a
  temporary or a variable). 653,853 lines, none of another shape.
- `probes/`: five programs, each with perl's answer in the report.
  `last-slot.pl`, `truth-of-the-dead.pl`, `number-of-the-dead.pl` and
  `length-of-the-dead.pl` are each a mutation that a test should see
  and no golden test does; `kept.pl` ends holding 900,000 bytes that
  nothing in the program can reach.

## To run it again

From the repository's root, with `WORK` a directory outside it:

    node docs/briefs/step7-review/gen.ts WORK/c
    python3 docs/briefs/step7-review/proto.py WORK              # a minute and a half
    python3 docs/briefs/step7-review/shapes.py WORK/c
    python3 docs/briefs/step7-review/proto.py WORK probe docs/briefs/step7-review/probes/last-slot.pl RT7_SKIP=lasttemp

Every run is under `timeout 10` and keeps a megabyte of what a program
prints: a mutation can make a loop run for ever.

## The numbers

Of 275 tests that compile, 105 allocate at all once a conversion
doesn't. Under the frame, with a collection at every allocation:

| What the collector doesn't look at | Tests that turn red |
|---|---|
| nothing (the design as proposed) | 0 |
| every root | 78 |
| every temporary | 76 |
| every variable | 13 |
| the first variable's slot | 8 |
| the last variable's slot | 1 (538) |
| the last temporary's slot | 0 |

Of the 78, 70 turn red with no `internal:` line: the program ran on
with a poisoned string and printed it. With the operands checked again
after the allocation, all 78 say `internal:`. With every root missed
and a collection at every 2nd, 3rd and 10th allocation, 64, 52 and 31
turn red. A `my` that doesn't make its slot undef turns 6 red (504,
562, 700, 702, 730, 741). All 275 runs take between 0.8 and 0.9
seconds, collecting at every allocation or never: the largest frame
has thirty slots.

## What it doesn't show

There is no heap cap in the prototype and no ordinary policy, so
nothing here measures either. The frame is one static array, not a
frame linked from the context, and there is one function: nothing here
exercises a chain of frames. The state is global, which the real
runtime's may not be (D28).
