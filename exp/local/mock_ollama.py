#!/usr/bin/env python3
"""A stand-in for ollama's /api/chat, to check agent.py's loop without a
model: it answers each request with the next scripted tool call, then
done. Nothing about a model is tested, only that the loop sends what
ollama expects, runs tools where it should, trims old results, survives
a 5xx and a resume, and writes its record.

    python3 exp/local/mock_ollama.py 11435 &
    python3 exp/local/agent.py --host http://localhost:11435 --model mock \\
        --repo . --brief exp/local/brief-step2.md --out /tmp/mock-run

MOCK_FAIL_AT=N makes request N answer 500 (every time, so the loop's
retries give up and the run ends with the error); a second server
without it, and agent.py --resume, continue the script where it was.
The script's position is kept in a file beside the port, so the two
servers share it.
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

SCRIPT = [
    ("read_file", {"path": "runtime/rt.h"}),
    ("run", {"command": "make test 2>&1 | tail -3"}),
    ("read_file", {"path": "t/checks.py"}),
    ("write_file", {"path": "build/mock-note.txt", "content": "the loop can write\n"}),
    ("run", {"command": "cat build/mock-note.txt; git status --short | head -3"}),
    ("read_file", {"path": "../outside"}),
    ("run", {"command": "echo still here"}),
    ("done", {"report": "Mock run: read files, ran make, wrote under build/, was refused a path outside the repository, survived a 500 and a resume."}),
]
STATE = f"/tmp/mock-ollama-{sys.argv[1]}.pos"


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        assert body.get("tools") and body.get("messages"), "agent.py sent no tools or messages"
        last = body["messages"][-1]
        assert last["role"] in ("user", "tool"), last["role"]
        n = int(open(STATE).read()) if os.path.exists(STATE) else 0
        tools = [m for m in body["messages"] if m.get("role") == "tool"]
        if n >= 5:
            # The third result (checks.py, long) is older than --keep 2 and must be a stub.
            assert any(m["content"].startswith("[") and "cut from the context" in m["content"] for m in tools), \
                "an old long result was not elided"
            assert tools[-1]["content"] and not tools[-1]["content"].startswith("[" + str(len(tools[-1]["content"]))), \
                "the newest result was elided"
        fail_at = int(os.environ.get("MOCK_FAIL_AT", "0"))
        if fail_at and n + 1 == fail_at:
            out = json.dumps({"error": "mock: server fell over"}).encode()
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return
        name, args = SCRIPT[min(n, len(SCRIPT) - 1)]
        open(STATE, "w").write(str(n + 1))
        reply = {
            "model": body["model"],
            "message": {"role": "assistant", "content": "",
                        "tool_calls": [{"function": {"name": name, "arguments": args}}]},
            "prompt_eval_count": 100 + n, "eval_count": 20, "done": True,
        }
        out = json.dumps(reply).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    if os.path.exists(STATE) and os.environ.get("MOCK_RESET", "1") == "1":
        os.remove(STATE)
    HTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()
