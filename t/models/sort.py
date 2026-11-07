#!/usr/bin/env python3
"""Model for examples/sort.strata: a sorted literal list, one per line.

Python's sorted(), ascending. The list is the one in the program: 14
numbers with duplicates (5, 12, -3) and negatives.

    python3 t/models/sort.py > examples/sort.expected
"""
DATA = [5, -3, 12, 0, 5, -8, 7, 12, 1, -3, 9, 4, 20, -1]
for v in sorted(DATA):
    print(v)
