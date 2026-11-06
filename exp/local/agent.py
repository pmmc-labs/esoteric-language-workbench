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

SYSTEM = """You are an agent working alone in a code repository on the person's computer. You have four tools: read_file, write_file, run, and done. Work only through them. Read the brief that follows, do what it says in the order it says, and when you are finished, or have stopped for one of the reasons it gives, call done with your report. Do not describe what you would do; do it, one tool call at a time, and read each result before the next."""


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


def chat(host, payload):
    req = urllib.request.Request(f"{host}/api/chat", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=3600) as resp:
        return json.load(resp)


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
    a = ap.parse_args()

    repo = os.path.realpath(a.repo)
    os.makedirs(a.out, exist_ok=True)
    brief = open(a.brief, encoding="utf-8").read()
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": brief}]
    transcript = open(os.path.join(a.out, "transcript.jsonl"), "w", encoding="utf-8")
    totals = {"steps": 0, "tool_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "seconds": 0.0}
    report = None
    nudged = False
    started = time.time()

    while totals["steps"] < a.max_steps and report is None:
        payload = {"model": a.model, "messages": messages, "tools": TOOLS, "stream": False,
                   "options": {"temperature": 0, "seed": a.seed, "num_ctx": a.num_ctx}}
        if a.think != "default":
            payload["think"] = a.think == "on"
        t0 = time.time()
        try:
            reply = chat(a.host, payload)
        except Exception as e:  # the run is the record; say what ended it
            transcript.write(json.dumps({"error": str(e), "step": totals["steps"]}) + "\n")
            print(f"error from {a.host}: {e}", file=sys.stderr)
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
                                     "prompt_eval_count": reply.get("prompt_eval_count"),
                                     "eval_count": reply.get("eval_count"),
                                     "message": msg}) + "\n")
        transcript.flush()
        if not calls:
            if nudged:
                print("the model stopped calling tools; ending", file=sys.stderr)
                break
            nudged = True
            messages.append({"role": "user", "content": "Continue with a tool call, or call done with your report."})
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
                break

    totals["wall_seconds"] = round(time.time() - started, 1)
    totals["seconds"] = round(totals["seconds"], 1)
    with open(os.path.join(a.out, "report.md"), "w", encoding="utf-8") as f:
        f.write(f"# {a.model}\n\n")
        f.write("Totals: " + json.dumps(totals) + "\n\n")
        f.write("Ended by: " + ("done" if report is not None else "step limit or error") + "\n\n")
        f.write("## Report\n\n" + (report or "(none)") + "\n")
    print(json.dumps(totals), file=sys.stderr)


if __name__ == "__main__":
    main()
