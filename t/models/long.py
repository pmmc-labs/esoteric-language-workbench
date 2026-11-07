#!/usr/bin/env python3
"""Model for golden test 211-long-history: a history of ten thousand writes.

The program is `let x = 0` followed by 10000 lines `x <- x + 1`, then prints
of x's depth, its top, and layers read back with `@`. This is far more than
one arena chunk holds, so it proves chunks chain (D26) and that `@` walks
a long history. The expected output is computed from a Python list standing
for the history, newest last: `#x` is its length, `x@k` has top
list[len - 1 - k].

    python3 t/models/long.py --program > t/211-long-history.strata
    python3 t/models/long.py > t/211-long-history.expected
"""
import sys

N = 10000
PROBES = [0, 1, 2, 4999, 5000, 9998, 9999, 10000]  # k for `x@k`; 10000 is the oldest

hist = [0]
for _ in range(N):
    hist.append(hist[-1] + 1)

if "--program" in sys.argv:
    out = ["let x = 0"] + ["x <- x + 1"] * N + ["print #x", "print x"]
    for k in PROBES:
        out += [f"print #x@{k}", f"print x@{k}"] if k < len(hist) else []
    sys.stdout.write("\n".join(out) + "\n")
else:
    out = [len(hist), hist[-1]]
    for k in PROBES:
        if k < len(hist):
            out += [len(hist) - k, hist[len(hist) - 1 - k]]
    sys.stdout.write("".join(f"{v}\n" for v in out))
