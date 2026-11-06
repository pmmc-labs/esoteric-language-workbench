#!/usr/bin/env python3
"""The calculator's referee: an evaluator written from docs/DECISIONS.md
(step 0's literals and output, and D20 to D28), not from compiler/ or
runtime/. `make checks` runs it over every golden test.

  python3 -I t/referee/calc.py PROGRAM.lang

It prints what the program's .expected must be, the way t/run.sh
compares it: the value and a newline; or, on a fault, the fault line
and `exit: 1` (run.sh puts stderr and stdout together, and so does this).
Exit 3 means the program is outside what this covers: a compile error
(those are unit tests, D4, so no golden test has one), or a form the
decisions don't mention.

Python's integers are unbounded, so an operation's exact result is
computed and then range-checked, which is D26 with no wrap to worry about.
Division is truncation toward zero (D24), not Python's //.
"""

import re
import sys

OUTSIDE = 3
INT_MIN = -(2 ** 62)
INT_MAX = 2 ** 62 - 1
OPS = ('+', '-', '*', '/')


class Outside(Exception):
    """A compile error, or a form the decisions don't cover."""


class Fault(Exception):
    """A run-time fault; its text is the message after `fault: `."""


def tokens(src):
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in ' \n\t\r':
            i += 1
        elif c == ';':
            while i < n and src[i] != '\n':
                i += 1
        elif c in '()':
            out.append(c)
            i += 1
        else:
            j = i
            while j < n and src[j] not in ' \n\t\r();':
                j += 1
            out.append(src[i:j])
            i = j
    return out


def parse(toks, i):
    t = toks[i]
    if t == '(':
        items, i = [], i + 1
        while True:
            if i >= len(toks):
                raise Outside()                 # missing ')'
            if toks[i] == ')':
                return ('list', items), i + 1
            f, i = parse(toks, i)
            items.append(f)
    if t == ')':
        raise Outside()
    # D22: an integer is an optional '-' and digits; `+5` and a lone `-` are symbols.
    if re.fullmatch(r'-?[0-9]+', t):
        return ('int', int(t)), i + 1
    return ('sym', t), i + 1


def program(src):
    toks = tokens(src)
    forms, i = [], 0
    while i < len(toks):
        f, i = parse(toks, i)
        forms.append(f)
    return forms


def check(f):
    """D21: every compile error, found before anything runs."""
    if f[0] == 'int':
        if not INT_MIN <= f[1] <= INT_MAX:
            raise Outside()
    elif f[0] == 'sym':
        raise Outside()                         # a symbol is not a value
    else:
        items = f[1]
        if not items or items[0][0] != 'sym' or items[0][1] not in OPS:
            raise Outside()
        if len(items) != 3:                    # D20: two operands
            raise Outside()
        for x in items[1:]:
            check(x)


def ev(f):
    if f[0] == 'int':
        return f[1]
    items = f[1]
    op = items[0][1]
    a = ev(items[1])                            # D27: left to right,
    b = ev(items[2])                            # then the operator's own fault
    if op == '+':
        r = a + b
    elif op == '-':
        r = a - b
    elif op == '*':
        r = a * b
    else:
        if b == 0:
            raise Fault('division by zero')     # D24
        q = abs(a) // abs(b)                    # D24: truncation toward zero
        r = q if (a < 0) == (b < 0) else -q
    if not INT_MIN <= r <= INT_MAX:             # D23, D25
        raise Fault('integer overflow')
    return r


def main(path):
    with open(path, encoding='utf-8') as fh:
        src = fh.read()
    try:
        forms = program(src)
        if len(forms) != 1:                     # a program is one form (step 0)
            raise Outside()
        check(forms[0])
    except Outside:
        return OUTSIDE
    try:
        value = ev(forms[0])
    except Fault as e:
        sys.stdout.write(f'fault: {e}\nexit: 1\n')
        return 0
    sys.stdout.write(f'{value}\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
