# A second family: running the experiments on a local model

`docs/MODELS.md`'s rounds all used one model family. These files run the
same rounds on a model served by ollama on a laptop, with a plain loop
as the harness (`agent.py`), so that a failure is the model's or the
brief's and not a harness's.

## What's here

- `agent.py`: the loop. A brief, four tools (`read_file`, `write_file`,
  `run`, `done`), temperature 0, a fixed seed, an explicit context size,
  a transcript of every exchange and a report with the totals.
- `brief-step2.md`: round 1, building step 2 from its red tests, cut to
  what a 32K context can hold: the rules, the step, D11 to D14, the
  commands, the report. It stands in for CLAUDE.md, PLAN.md and
  DECISIONS.md, which `docs/MODELS.md`'s "Local" tier says to cut.
- `mock_ollama.py`: a scripted stand-in for `/api/chat`, to check the
  loop without a model.
- `runs/`: each run's `transcript.jsonl` and `report.md`, committed, as
  the record.

## Running round 1 on the laptop

Needs: ollama with the model pulled, Node 22.18 or later, a C compiler
as `cc` and `clang` (Xcode's is both), Python 3.

```
cd esoteric-language-workbench
git worktree add -b local-MODEL-step2 ../wt-local d5a0f3a     # step 2 written, tests red
python3 exp/local/agent.py --repo ../wt-local --brief exp/local/brief-step2.md \
    --model qwen3.8:27b --out exp/local/runs/MODEL-step2
```

`d5a0f3a` is the commit the Claude builders started from. The agent
prints each tool call to stderr as it goes, and the totals at the end.
`--num-ctx` defaults to 32768; if the model won't load at that size,
try 16384 and say so in the record. `--think on|off` sets ollama's
thinking switch for models that have one; the default leaves it to the
model. `--max-steps` (80) ends a run that doesn't call `done`.

Then judge it the way every round was judged, in the worktree:

```
cd ../wt-local
make test; make golden-clang; make sanitize
git status --short          # nothing under t/ should have changed
git diff --stat d5a0f3a
```

Commit and push the worktree's branch, and commit the run directory on
main, so the diff and the transcript can be read. The transcript is
the model's record; `report.md` is its own account of the run.

## Rounds 2 and 3

Writing the model for step 3 from D15 to D17 (the referee judges it),
and proposing step 1 from step 0 (`exp-step0-clean`), each with a brief
of its own, once round 1 has been run and read.
