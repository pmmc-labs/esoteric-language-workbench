#!/usr/bin/env python3
"""t/020-compare: the six comparisons (D12) over every pair of the edge
values, each counted with an if (D13), so one program checks them all
and the booleans never print: for each operator, the number of pairs
that hold, and the six counts packed as a base-100 number, `<` the
lowest pair of digits. Python's comparisons on integers are the
definition; the operators' names are the language's.

    python3 t/models/compare.py --program > t/020-compare.lang
    python3 t/models/compare.py > t/020-compare.expected
"""

import operator
import sys

MIN, MAX = -(2**62), 2**62 - 1
VALUES = [0, 1, -1, 7, -7, MAX, MIN, 3, -3]
OPS = [('<', operator.lt), ('<=', operator.le), ('>', operator.gt), ('>=', operator.ge), ('==', operator.eq), ('!=', operator.ne)]

def count(fn):
    return sum(1 for a in VALUES for b in VALUES if fn(a, b))

def counted(op):
    terms = [f'(if ({op} {a} {b}) 1 0)' for a in VALUES for b in VALUES]
    acc = terms[0]
    for t in terms[1:]:
        acc = f'(+ {acc} {t})'
    return acc

def program():
    acc = counted(OPS[-1][0])
    for op, _ in reversed(OPS[:-1]):
        acc = f'(+ (* {acc} 100) {counted(op)})'
    return '\n'.join([
        '; Every comparison over every pair of edge values, each counted with an',
        '; if, the six counts packed in base 100, < lowest. Expected output and',
        '; this program from t/models/compare.py.',
        acc,
    ]) + '\n'

def expected():
    n = 0
    for _, fn in reversed(OPS):
        n = n * 100 + count(fn)
    return f'{n}\n'

if __name__ == '__main__':
    sys.stdout.write(program() if '--program' in sys.argv else expected())
