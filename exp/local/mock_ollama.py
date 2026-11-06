#!/usr/bin/env python3
"""A stand-in for ollama's /api/chat, to check agent.py's loop without a
model: it answers each request with the next scripted tool call, then
done. Nothing about a model is tested, only that the loop sends what
ollama expects, runs tools where it should, and writes its record.

    python3 exp/local/mock_ollama.py 11435 &
    python3 exp/local/agent.py --host http://localhost:11435 --model mock \\
        --repo . --brief exp/local/brief-step2.md --out /tmp/mock-run
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

SCRIPT = [
    ("read_file", {"path": "runtime/rt.h"}),
    ("run", {"command": "make test 2>&1 | tail -3"}),
    ("write_file", {"path": "build/mock-note.txt", "content": "the loop can write\n"}),
    ("run", {"command": "cat build/mock-note.txt; git status --short | head -3"}),
    ("read_file", {"path": "../outside"}),
    ("done", {"report": "Mock run: read a file, ran make, wrote under build/, was refused a path outside the repository."}),
]


class Handler(BaseHTTPRequestHandler):
    n = 0

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        assert body.get("tools") and body.get("messages"), "agent.py sent no tools or messages"
        last = body["messages"][-1]
        assert last["role"] in ("user", "tool"), last["role"]
        name, args = SCRIPT[min(Handler.n, len(SCRIPT) - 1)]
        Handler.n += 1
        reply = {
            "model": body["model"],
            "message": {"role": "assistant", "content": "",
                        "tool_calls": [{"function": {"name": name, "arguments": args}}]},
            "prompt_eval_count": 100 + Handler.n, "eval_count": 20, "done": True,
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
    HTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()
