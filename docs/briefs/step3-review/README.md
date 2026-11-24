# The review of step 3's definition

A reader that had not seen the builder's model or the evidence for the
proposal was given the proposed definition of step 3 as prose, perl
5.42, and one instruction: find a program the definition accepts that
runs, doesn't fault, and differs from perl; and refute the claim that
a value's past never shows where the definition doesn't fault. What it
found is in [`../../TRAPS.md`](../../TRAPS.md), T100 to T103, and in
`../../PLAN.md` under step 3.

| File | |
|---|---|
| `model.py` | The reviewer's model of the definition: a parser and an evaluator, written from the prose. `OPT` holds the readings it took of what the prose left open, the amendments its findings asked for (`amend_*`), and three ways to break the model on purpose (`mut_*`) |
| `pools.py` | Its values: 1,681 strings that are numbers or nearly, and the numbers at the edges |
| `harness.py` | Its checker: a program against perl, by the three rules, bytes against bytes |
| `a4_random.py` | Its generator of random statements over the whole grammar, as it ran it against perl |
| `compiler.py` | The builder's: the same generator, with the reviewer's model deciding which statements print, and the compiler and perl run on them. `python3 docs/briefs/step3-review/compiler.py SEED COUNT [nl]` |

The first three are as the reviewer left them, paths and all: `harness.py`
writes its programs under a `t/` beside itself. The rest of what it
wrote (the other generators, the search of pasts, its logs) was in its
own scratch directory and is not kept; its report has the counts.
