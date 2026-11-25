# The review of step 4's definition

As step 3's ([`../step3-review/`](../step3-review/README.md)): a reader
with the proposal's words and perl, who extended the step 3 reviewer's
model. What it found is in [`../../TRAPS.md`](../../TRAPS.md), T115, and
in `../../PLAN.md` under step 4.

| File | |
|---|---|
| `model4.py` | The reviewer's model of step 4, on `../step3-review/model.py`. `OPT4` holds its readings, the amendments its findings asked for, and three ways to break the model on purpose |
| `h4.py` | The step 3 harness pointed at it |
| `gen4.py` | Its generator of random statements over the whole grammar |
| `compiler.py` | The builder's: the reviewer's generator and model, and the compiler and perl run on what they draw. `python3 docs/briefs/step4-review/compiler.py SEED COUNT [nl] [tight] [heavy]` |

The rest of what it wrote (its search of pasts, by states: 18 million
looks; its logs) was in its own scratch directory and is not kept; its
report has the counts.
