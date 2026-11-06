#!/usr/bin/env python3
"""A model of step 1's arithmetic (docs/DECISIONS.md D8, D10, D11, D12),
for golden tests 028, 029 and 030. It writes both the programs and what
they must print, from the definition: not from the compiler, and not
from the runtime's code.

    python3 t/models/arith.py deep-left --program > t/028-deep-left.lang
    python3 t/models/arith.py deep-left > t/028-deep-left.expected
    python3 t/models/arith.py deep-right --program > t/029-deep-right.lang
    python3 t/models/arith.py deep-right > t/029-deep-right.expected
    python3 t/models/arith.py mixed --program > t/030-mixed.lang
    python3 t/models/arith.py mixed > t/030-mixed.expected

How, and what it does not copy:

- Integers are Python's, which are exact, so "the exact result is out of
  range" (D10) is a comparison with the range, made at every node by
  `apply`, the one place an operation is defined. Nothing is checked once
  at the end.
- `/` and `%` are written out from D11, with magnitudes and signs:
  truncate toward zero, and the remainder takes the dividend's sign. They
  are not Python's `//` and `%`, which floor, and `a = (a / b) * b + a % b`
  is asserted for every division made.
- A literal is written by `str` of an integer, never read back with
  `int()` (D9).
- Evaluation is left operand, then right, then the operation (D12), so
  the first fault is the one raised; the generator of `mixed` redraws any
  operation that would fault, so the program has a value.
- The random choices of `mixed` come from a linear congruential
  generator written out below, since Python's `random` stream is not part
  of the definition.
"""

import sys

sys.setrecursionlimit(20000)

INT_MIN = -(2 ** 62)
INT_MAX = 2 ** 62 - 1


class Fault(Exception):
    """A run-time fault; the message is what the program prints (D3)."""


def sign(n):
    return (n > 0) - (n < 0)


def truncated_quotient(a, b):
    """D11: toward zero. Divide the magnitudes, then give the quotient
    the sign the operands' signs make."""
    q = abs(a) // abs(b)
    return -q if sign(a) * sign(b) < 0 else q


def truncated_remainder(a, b):
    """D11: the sign of the dividend."""
    r = abs(a) % abs(b)
    return -r if a < 0 else r


def apply(op, a, b):
    """One operation on two integers in range: the exact result if it is
    in range, else the fault D10 or D11 names."""
    if op == '+':
        r = a + b
    elif op == '-':
        r = a - b
    elif op == '*':
        r = a * b
    elif op == '/' or op == '%':
        if b == 0:
            raise Fault('division by zero')
        q = truncated_quotient(a, b)
        m = truncated_remainder(a, b)
        assert a == q * b + m, (a, b, q, m)
        r = q if op == '/' else m
    else:
        raise AssertionError(op)
    if r < INT_MIN or r > INT_MAX:
        raise Fault('integer overflow')
    return r


# A tree is ('lit', n) or (op, left, right).

def lit(n):
    assert INT_MIN <= n <= INT_MAX
    return ('lit', n)


def call(op, left, right):
    return (op, left, right)


def evaluate(tree):
    """Left, then right, then the operation; every node is range-checked
    by apply, and every literal here."""
    if tree[0] == 'lit':
        assert INT_MIN <= tree[1] <= INT_MAX
        return tree[1]
    op, left, right = tree
    a = evaluate(left)
    b = evaluate(right)
    return apply(op, a, b)


def show(tree):
    if tree[0] == 'lit':
        return str(tree[1])
    return '(%s %s %s)' % (tree[0], show(tree[1]), show(tree[2]))


def deep_left():
    # (+ (+ (+ 0 1) 2) 3) carried to 1000: 1000 lists, the first around 0 and 1.
    tree = call('+', lit(0), lit(1))
    for k in range(2, 1001):
        tree = call('+', tree, lit(k))
    return tree


def deep_right():
    # (- 1 (- 2 (- 3 ... (- 999 1000)))): 999 lists.
    tree = call('-', lit(999), lit(1000))
    for k in range(998, 0, -1):
        tree = call('-', lit(k), tree)
    return tree


class Lcg:
    """x' = (1103515245 x + 12345) mod 2^31, taking the bits above the
    low 16, which are the better ones."""

    def __init__(self, seed):
        self.x = seed

    def below(self, n):
        self.x = (1103515245 * self.x + 12345) % 2 ** 31
        return (self.x >> 16) % n


def mixed():
    """About 300 operations over all five operators, operands from -50
    to 50. Start with a pool of 301 literals; repeatedly draw two of
    them in order and an operator, replace them by that call if it does
    not fault (else draw again). One item is left: the program. The seed
    is the first of several tried that satisfy the assertions at the end,
    which say what the test must exercise."""
    rng = Lcg(7)
    operators = ['+', '-', '*', '*', '/', '%']  # `*` twice: it is what grows the values
    pool = []
    for _ in range(301):
        n = rng.below(101) - 50
        pool.append((lit(n), n))
    seen = set()          # (operator, sign of dividend, sign of divisor) for / and %
    biggest = 0           # the largest magnitude of any node
    biggest_product = 0   # and of any product
    count = {op: 0 for op in '+-*/%'}
    while len(pool) > 1:
        # Half the time the left operand is the newest call, so that
        # chains form and the values compound.
        i = len(pool) - 1 if rng.below(2) == 0 else rng.below(len(pool))
        j = rng.below(len(pool) - 1)
        if j >= i:
            j += 1
        op = operators[rng.below(len(operators))]
        (left, a), (right, b) = pool[i], pool[j]
        try:
            r = apply(op, a, b)
        except Fault:
            continue
        pool = [p for k, p in enumerate(pool) if k != i and k != j]
        pool.append((call(op, left, right), r))
        count[op] += 1
        biggest = max(biggest, abs(r))
        if op == '*':
            biggest_product = max(biggest_product, abs(r))
        if op in '/%':
            seen.add((op, sign(a), sign(b)))
    tree = pool[0][0]
    # What the test is for, so a change to the generator can't quietly
    # make it weaker.
    assert sum(count.values()) == 300, count
    assert all(count[op] > 0 for op in count), count
    for op in '/%':
        for sa in (-1, 1):
            for sb in (-1, 1):
                assert (op, sa, sb) in seen, (op, sa, sb)
    assert biggest > 2 ** 40, biggest
    assert biggest_product > 2 ** 40, biggest_product
    assert abs(pool[0][1]) > 2 ** 32, pool[0][1]  # the program's value is not a lucky 0
    return tree


TESTS = {'deep-left': deep_left, 'deep-right': deep_right, 'mixed': mixed}


def main(argv):
    args = [a for a in argv if a != '--program']
    if len(args) != 1 or args[0] not in TESTS:
        sys.exit('usage: arith.py (%s) [--program]' % ' | '.join(TESTS))
    tree = TESTS[args[0]]()
    value = evaluate(tree)
    if '--program' in argv:
        print('; Written by t/models/arith.py %s (step 1); do not edit.' % args[0])
        print(show(tree))
    else:
        print(value)


main(sys.argv[1:])
