#!/usr/bin/env python3
"""Mechanical checks, run from anywhere; exit 1 on any mismatch.

1. Every .strata in t/ and examples/ has a .expected, and every .expected
   has a .strata.
2. Every model's docstring commands (lines starting `python3 t/models/`,
   of the form `COMMAND > FILE`) are rerun and compared with FILE, so a
   hand-patched expected file is caught.
"""
import ast
import glob
import os
import subprocess
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
bad = []

for d in ("t", "examples"):
    srcs = {p[: -len(".strata")] for p in glob.glob(f"{d}/*.strata")}
    exps = {p[: -len(".expected")] for p in glob.glob(f"{d}/*.expected")}
    bad += [f"{p}.strata has no .expected" for p in sorted(srcs - exps)]
    bad += [f"{p}.expected has no .strata" for p in sorted(exps - srcs)]

for model in sorted(glob.glob("t/models/*.py")):
    doc = ast.get_docstring(ast.parse(open(model).read())) or ""
    for line in doc.splitlines():
        line = line.strip()
        if not line.startswith("python3 t/models/"):
            continue
        cmd, sep, target = line.partition(" > ")
        if not sep:
            bad.append(f"{model}: no '> FILE' in: {line}")
            continue
        r = subprocess.run(cmd, shell=True, capture_output=True)
        if r.returncode != 0:
            bad.append(f"{model}: `{cmd}` failed: {r.stderr.decode()[:200]}")
        elif r.stdout != open(target.strip(), "rb").read():
            bad.append(f"{model}: output of `{cmd}` differs from {target.strip()}")

for b in bad:
    print("check failed:", b, file=sys.stderr)
sys.exit(1 if bad else 0)
