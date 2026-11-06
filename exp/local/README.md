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
try 16384 and say so in the record. The loop keeps the context in
bounds by cutting old long tool results to a stub (`--keep`, `--elide`);
the transcript keeps them whole. A run that dies, on a 5xx ollama
answers three times or anything else, says so and stops; `--resume`
with the same `--out` rebuilds the conversation from the transcript and
goes on, the worktree being as the model left it. Ollama's own reason
for a 5xx is in its log, on a Mac `~/.ollama/logs/server.log`; the
usual ones are the context filling up and a tool call the server
couldn't parse. `--think on|off` sets ollama's
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

## Round 2: writing the model for step 3, then building it

The commit `936aec3` has step 3's decisions (D15 to D17) and no model
and no tests; the brief asks for the model first, committed red, then
the build.

```
git worktree add -b local-MODEL-step3 ../wt-local3 936aec3
python3 exp/local/agent.py --repo ../wt-local3 --brief exp/local/brief-step3.md \
    --model qwen3.8:27b --out exp/local/runs/MODEL-step3
```

Judge as before, plus the referee: on main, `python3 t/referee/calc.py`
over each new `t/03*.lang` must print its `.expected`. Push the branch
and commit the run directory on main.

## Round 3

Proposing step 1 from step 0 (`exp-step0-clean`), with a brief of its
own, once rounds 1 and 2 have been read.
