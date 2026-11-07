#!/usr/bin/env python3
"""Model for examples/factorial.strata: 1! to 20!.

Python's math.factorial, which is exact; 20! is the largest below 2**63.

    python3 t/models/factorial.py > examples/factorial.expected
"""
import math

for n in range(1, 21):
    assert math.factorial(n) < 2**63
    print(f"{n}! = {math.factorial(n)}")
