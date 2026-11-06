#!/usr/bin/env python3
"""A plain agent loop over ollama, for running the workbench's experiments
on a model outside the Claude family (docs/MODELS.md, "A second
family"). Nothing clever: a brief, four tools, a transcript. What it
can't do is the control: a failure here is the model's or the brief's,
not a harness's.

    python3 exp/local/agent.py --repo ../wt-local --brief exp/local/brief-step2.md \\
        --model qwen3.8:27b --out exp/local/runs/qwen-step2

Tools the model gets: read_file(path), write_file(path, content),
run(command) and done(report). Paths are under --repo and nowhere else;
commands run with --repo as their directory, through bash, with a time
limit. Temperature 0 and a fixed seed, so a run is as repeatable as the
model allows; --num-ctx is passed explicitly, since ollama's default
context is small and a brief plus a few files overflows it silently.

The context is the local tier's limit, so the loop keeps it in bounds:
a tool result older than the last --keep is cut to a stub once it's
longer than --elide characters, and the model can read the file again.
The stub says so. The transcript keeps every result in full.

A run that dies (ollama answered 5xx three times, the machine slept)
continues from its transcript with --resume: the messages are rebuilt
from --out/transcript.jsonl and the loop goes on, appending to it. The
repository's working tree is the state the model left it in.

The transcript (--out/transcript.jsonl) holds every request and reply
with ollama's own counts, and --out/report.md the model's final report
and the run's totals. Standard library only.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

TOOLS = [
    {"type": "function", "function": {
        "name": "read_file",
        "description": "Read a file in the repository. Returns its text.",
        "parameters": {"type": "object", "required": ["path"], "properties": {
            "path": {"type": "string", "description": "Path relative to the repository root."}}}}},
    {"type": "function", "function": {
        "name": "write_file",
        "description": "Write a file in the repository, replacing it if it exists. Creates directories as needed.",
        "parameters": {"type": "object", "required": ["path", "content"], "properties": {
            "path": {"type": "string", "description": "Path relative to the repository root."},
            "content": {"type": "string", "description": "The whole new contents of the file."}}}}},
    {"type": "function", "function": {
        "name": "run",
        "description": "Run a shell command in the repository root with bash. Returns stdout and stderr together and the exit status. Use it for make, git, node, ls, grep, sed and the like.",
        "parameters": {"type": "object", "required": ["command"], "properties": {
            "command": {"type": "string"}}}}},
    {"type": "function", "function": {
        "name": "done",
        "description": "Finish. Call this once, when the work is complete or you have stopped, with your final report as the brief asks for it.",
        "parameters": {"type": "object", "required": ["report"], "properties": {
            "report": {"type": "string"}}}}},
]

SYSTEM = """You are an agent working alone in a code repository on the person's computer. You have four tools: read_file, write_file, run, and done. Work only through them. Read the brief that follows, do what it says in the order it says, and when you are finished, or have stopped for one of the reasons it gives, call done with your report. Do not describe what you would do; do it, one tool call at a time, and read each result before the next. Keep each command's output short (tail, head, grep) where you can: your context is limited, and old results are cut from it."""

NUDGE = ("Your last reply was cut off before any tool call. Don't start over: take what you had decided and "
         "write it down now with a tool call, one piece at a time, then go on. Or call done with your report.")


def under(repo, path):
    full = os.path.realpath(os.path.join(repo, path))
    if full != repo and not full.startswith(repo + os.sep):
        raise ValueError(f"refused: {path} is outside the repository")
    return full


def clip(text, limit=16000):
    if len(text) <= limit:
        return text
    return text[:limit // 2] + f"\n... [{len(text) - limit} characters cut] ...\n" + text[-limit // 2:]


def call_tool(repo, name, args, timeout):
    try:
        if name == "read_file":
            with open(under(repo, args["path"]), encoding="utf-8", errors="replace") as f:
                return clip(f.read())
        if name == "write_file":
            full = under(repo, args["path"])
            os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
            with open(full, "w", encoding="utf-8") as f:
                f.write(args["content"])
            return f"wrote {len(args['content'])} characters to {args['path']}"
        if name == "run":
            r = subprocess.run(["bash", "-c", args["command"]], cwd=repo, capture_output=True,
                               text=True, errors="replace", timeout=timeout)
            out = r.stdout + r.stderr
            return clip(out) + f"\n[exit {r.returncode}]"
        if name == "done":
            return "done"
        return f"unknown tool {name}"
    except subprocess.TimeoutExpired:
        return f"[killed after {timeout}s]"
    except (KeyError, TypeError) as e:
        return f"bad arguments for {name}: {e}"
    except (OSError, ValueError) as e:
        return str(e)


def chat(host, payload, tries=3, timeout=1800):
    """One request; a 5xx or a dropped connection is retried, with the
    server's own message kept, since ollama says why in the body."""
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(f"{host}/api/chat", data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="replace")[:500]
            last = f"HTTP {e.code}: {body}"
            if e.code < 500:
                break
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            last = str(e)
        print(f"  request failed ({last}); retry {attempt + 1} of {tries - 1}" if attempt < tries - 1
              else f"  request failed ({last})", file=sys.stderr)
        time.sleep(float(os.environ.get("AGENT_RETRY_SLEEP", 10)) * (attempt + 1))
    raise RuntimeError(last)


def size(messages):
    """A rough token count of what's sent, four characters a token."""
    return sum(len(json.dumps(m)) for m in messages) // 4


def trimmed(messages, keep, elide, budget):
    """The messages as sent. A thinking model's reasoning is never resent
    (it filled the context in round 2). Tool results are cut to a stub
    only while the whole is over `budget` tokens, oldest long result
    first, and never the newest `keep`: round 3's first run cut results
    the model still needed and it read the same files over and over."""
    out = []
    for i, m in enumerate(messages):
        # A thinking model's reasoning is dropped once it led to tool calls:
        # done with, and resending it filled the context in round 2. A reply
        # with no tool call was a thought cut off (round 3: the whole design
        # of a step, twice, each time from the start), and that one is kept
        # so the next turn continues it rather than beginning again.
        if m.get("role") == "assistant" and m.get("thinking") and m.get("tool_calls"):
            m = {k: v for k, v in m.items() if k != "thinking"}
        out.append(dict(m))
    tool_at = [i for i, m in enumerate(out) if m.get("role") == "tool"]
    cuttable = tool_at[:-keep] if keep else tool_at
    for i in cuttable:
        if size(out) <= budget:
            break
        if len(out[i].get("content", "")) > elide:
            out[i]["content"] = (f"[{len(out[i]['content'])} characters, cut from the context to save room; "
                                 f"read the file or run the command again if you need it]")
    return out


def resume(path, messages):
    """Rebuild the conversation from a transcript, and the totals."""
    totals = {"steps": 0, "tool_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "seconds": 0.0}
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            if "message" in d:
                messages.append(d["message"])
                totals["steps"] = d["step"]
                totals["prompt_tokens"] += d.get("prompt_eval_count") or 0
                totals["output_tokens"] += d.get("eval_count") or 0
                totals["seconds"] += d.get("seconds") or 0
            elif "tool" in d:
                messages.append({"role": "tool", "content": d["result"], "tool_name": d["tool"]})
                totals["tool_calls"] += 1
            elif "nudge" in d:
                messages.append({"role": "user", "content": NUDGE})
    # A run cut off between a reply and its tool results leaves that step
    # unanswered: drop it, and the model decides it again. What its tools
    # did before the cut stays in the tree, where the model will see it.
    last = max((i for i, m in enumerate(messages) if m.get("role") == "assistant"), default=None)
    if last is not None:
        calls = len(messages[last].get("tool_calls") or [])
        answered = sum(1 for m in messages[last + 1:] if m.get("role") == "tool")
        if calls and answered < calls:
            del messages[last:]
            totals["steps"] -= 1
            totals["tool_calls"] -= answered
            print(f"dropped an unfinished step ({answered} of {calls} tool results recorded)", file=sys.stderr)
    return totals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--host", default="http://localhost:11434")
    ap.add_argument("--max-steps", type=int, default=80)
    ap.add_argument("--num-ctx", type=int, default=32768)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=600, help="seconds a command may run")
    ap.add_argument("--think", choices=["on", "off", "default"], default="default")
    ap.add_argument("--keep", type=int, default=4, help="tool results never cut, the newest")
    ap.add_argument("--elide", type=int, default=1200, help="a result shorter than this is never cut")
    ap.add_argument("--budget", type=float, default=0.6, help="cut old results only past this share of --num-ctx")
    ap.add_argument("--num-predict", type=int, default=8192, help="the most tokens one reply may have; a model in a loop is cut there")
    ap.add_argument("--request-timeout", type=int, default=1800, help="seconds one request may take")
    ap.add_argument("--resume", action="store_true", help="continue from --out/transcript.jsonl")
    a = ap.parse_args()

    repo = os.path.realpath(a.repo)
    os.makedirs(a.out, exist_ok=True)
    brief = open(a.brief, encoding="utf-8").read()
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": brief}]
    tpath = os.path.join(a.out, "transcript.jsonl")
    if a.resume:
        totals = resume(tpath, messages)
        print(f"resumed at step {totals['steps']}, {totals['tool_calls']} tool calls so far", file=sys.stderr)
        transcript = open(tpath, "a", encoding="utf-8")
        transcript.write(json.dumps({"resumed": True, "at": totals["steps"]}) + "\n")
    else:
        totals = {"steps": 0, "tool_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "seconds": 0.0}
        transcript = open(tpath, "w", encoding="utf-8")
    report = None
    nudged = False
    ended = "step limit"
    started = time.time()

    while totals["steps"] < a.max_steps and report is None:
        sent = trimmed(messages, a.keep, a.elide, int(a.num_ctx * a.budget))
        est = size(sent)
        if est > a.num_ctx * 0.8:
            print(f"  context estimate {est} tokens, near --num-ctx {a.num_ctx}", file=sys.stderr)
        payload = {"model": a.model, "messages": sent, "tools": TOOLS, "stream": False,
                   "options": {"temperature": 0, "seed": a.seed, "num_ctx": a.num_ctx,
                               "num_predict": a.num_predict}}
        if a.think != "default":
            payload["think"] = a.think == "on"
        t0 = time.time()
        try:
            reply = chat(a.host, payload, timeout=a.request_timeout)
        except RuntimeError as e:
            transcript.write(json.dumps({"error": str(e), "step": totals["steps"]}) + "\n")
            print(f"error from {a.host}: {e}\nrerun with --resume to continue from here", file=sys.stderr)
            ended = f"error: {e}"
            break
        dt = time.time() - t0
        totals["steps"] += 1
        totals["prompt_tokens"] += reply.get("prompt_eval_count", 0)
        totals["output_tokens"] += reply.get("eval_count", 0)
        totals["seconds"] += dt
        msg = reply.get("message", {})
        messages.append(msg)
        calls = msg.get("tool_calls") or []
        transcript.write(json.dumps({"step": totals["steps"], "seconds": round(dt, 1),
                                     "context_estimate": est,
                                     "prompt_eval_count": reply.get("prompt_eval_count"),
                                     "eval_count": reply.get("eval_count"),
                                     "message": msg}) + "\n")
        transcript.flush()
        if reply.get("done_reason") == "length":
            print(f"  the reply hit --num-predict {a.num_predict}; the model may be looping", file=sys.stderr)
        if not calls:
            if nudged:
                print("the model stopped calling tools; ending", file=sys.stderr)
                ended = "no tool call twice"
                break
            nudged = True
            messages.append({"role": "user", "content": NUDGE})
            transcript.write(json.dumps({"nudge": True, "step": totals["steps"]}) + "\n")
            continue
        for call in calls:
            fn = call.get("function", {})
            name, args = fn.get("name"), fn.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"_raw": args}
            totals["tool_calls"] += 1
            result = call_tool(repo, name, args, a.timeout)
            shown = args if name != "write_file" else {"path": args.get("path"), "chars": len(args.get("content", ""))}
            print(f"[{totals['steps']}] {name} {json.dumps(shown)[:160]}", file=sys.stderr)
            transcript.write(json.dumps({"step": totals["steps"], "tool": name, "args": args, "result": result}) + "\n")
            transcript.flush()
            messages.append({"role": "tool", "content": result, "tool_name": name})
            if name == "done":
                report = args.get("report", "")
                ended = "done"
                break

    totals["wall_seconds"] = round(time.time() - started, 1)
    totals["seconds"] = round(totals["seconds"], 1)
    with open(os.path.join(a.out, "report.md"), "w", encoding="utf-8") as f:
        f.write(f"# {a.model}\n\n")
        f.write("Totals: " + json.dumps(totals) + "\n\n")
        f.write("Ended by: " + ended + "\n\n")
        f.write("## Report\n\n" + (report or "(none)") + "\n")
    print(json.dumps(totals), file=sys.stderr)


if __name__ == "__main__":
    main()
