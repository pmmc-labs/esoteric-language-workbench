#!/usr/bin/env python3
"""Consistency checks, run from anywhere (see t/README.md).

- every t/*.ditto and examples/*.ditto has an .expected, and every
  .expected and .stdin has its .ditto;
- test numbers in t/ are unique, and names are NNN-name;
- every model in t/models/*.py lists at least one command in its
  docstring (lines starting `python3 t/models/`, ending `> FILE`), and
  rerunning each reproduces FILE byte for byte.
"""
import ast
import glob
import os
import re
import shlex
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
problems = []


def check_tests():
    numbers = {}
    for d in ("t", "examples"):
        for path in sorted(glob.glob(f"{d}/*.ditto")):
            base = path[: -len(".ditto")]
            if not os.path.exists(base + ".expected"):
                problems.append(f"{path}: no .expected")
            name = os.path.basename(base)
            if d == "t":
                m = re.fullmatch(r"(\d{3})-[a-z0-9][a-z0-9-]*", name)
                if not m:
                    problems.append(f"{path}: name is not NNN-name")
                elif m.group(1) in numbers:
                    problems.append(f"{path}: number {m.group(1)} also used by {numbers[m.group(1)]}")
                else:
                    numbers[m.group(1)] = path
        for ext in (".expected", ".stdin"):
            for path in sorted(glob.glob(f"{d}/*{ext}")):
                if not os.path.exists(path[: -len(ext)] + ".ditto"):
                    problems.append(f"{path}: no .ditto")


def check_models():
    for model in sorted(glob.glob("t/models/*.py")):
        doc = ast.get_docstring(ast.parse(open(model).read())) or ""
        commands = [l.strip() for l in doc.splitlines() if l.strip().startswith("python3 t/models/")]
        if not commands:
            problems.append(f"{model}: docstring lists no `python3 t/models/...` command")
        for line in commands:
            if " > " not in line:
                problems.append(f"{model}: command does not redirect to a file: {line}")
                continue
            cmd, target = line.rsplit(" > ", 1)
            target = target.strip()
            run = subprocess.run(shlex.split(cmd), capture_output=True)
            if run.returncode != 0:
                problems.append(f"{model}: `{cmd}` failed: {run.stderr.decode()[:200]}")
            elif not os.path.exists(target):
                problems.append(f"{model}: {target} does not exist")
            elif open(target, "rb").read() != run.stdout:
                problems.append(f"{model}: rerunning `{cmd}` differs from {target}")


check_tests()
check_models()
if problems:
    for p in problems:
        print("checks:", p)
    sys.exit(1)
print("checks: ok")
