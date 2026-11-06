#!/usr/bin/env python3
"""The referee for the calculator: an evaluator written from the
decisions (D1 to D4, D8 to D15 in docs/DECISIONS.md), not from the
runtime or the compiler. Given a program, it prints what the golden
test's .expected must be: the value and a newline, or, for a fault, its
message and `exit: 1` (D3), each with a newline.

    python3 t/referee/calc.py t/NNN-name.lang

Exit 0 with the output on stdout; exit 3 with the reason on stderr when
the program is outside what a golden test can be, which is a program the
compiler must refuse (D4, D15). t/checks.py skips those.

It is deliberately slow and plain: Python's unbounded integers, the 63-bit
range checked after every operation (D10), division written out so that it
truncates (D11) and doesn't borrow Python's floor, and nothing recursive,
so a deeply nested program is no harder than a flat one (D12, D14).

The builder of a step doesn't read this file (CLAUDE.md): a model that
agrees with it agrees by a second derivation.
"""

import sys

INT_MIN = -(2 ** 62)
INT_MAX = 2 ** 62 - 1
# The reader's whitespace and delimiters (D9): nothing else separates atoms,
# so a no-break space or a form feed is part of a symbol.
SPACE = ' \n\t\r'
DELIM = SPACE + '();'
DIGITS = '0123456789'


class Outside(Exception):
    """The program is one the compiler must refuse."""


def tokens(text):
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in SPACE:
            i += 1
        elif c == ';':
            while i < n and text[i] != '\n':
                i += 1
        elif c in '()':
            yield c
            i += 1
        else:
            j = i
            while j < n and text[j] not in DELIM:
                j += 1
            yield text[i:j]
            i = j


def atom(tok):
    """An integer is an optional '-' and then one or more of 0-9, and
    nothing else (D9): not Python's int(), which takes '+5', '1_0' and
    other scripts' digits."""
    digits = tok[1:] if tok[0] == '-' else tok
    if digits and all(ch in DIGITS for ch in digits):
        v = int(tok)
        if not INT_MIN <= v <= INT_MAX:
            raise Outside(f'integer out of range: {tok}')
        return ('int', v)
    return ('sym', tok)


def parse(text):
    """The top-level forms, as ('int', n), ('sym', s) or ('list', [forms])."""
    stack = [[]]
    for t in tokens(text):
        if t == '(':
            stack.append([])
        elif t == ')':
            if len(stack) == 1:
                raise Outside("unexpected ')'")
            items = stack.pop()
            stack[-1].append(('list', items))
        else:
            stack[-1].append(atom(t))
    if len(stack) != 1:
        raise Outside("missing ')'")
    return stack[0]


OPS = {'+', '-', '*', '/', '%'}


def check(form):
    """The compile errors of D15, over the whole program before anything
    runs: a malformed form anywhere, reached or not, means no output."""
    todo = [form]
    while todo:
        kind, v = todo.pop()
        if kind == 'int':
            continue
        if kind == 'sym':
            raise Outside(f"can't compile symbol yet: {v}")
        if not v:
            raise Outside('empty form')
        hk, hv = v[0]
        if hk != 'sym':
            raise Outside('expected an operator')
        if hv not in OPS:
            raise Outside(f"unknown operator '{hv}'")
        if len(v) != 3:
            raise Outside(f"'{hv}' takes 2 arguments, got {len(v) - 1}")
        todo.extend(v[1:])


class Fault(Exception):
    pass


def apply(op, a, b):
    if op == '+':
        r = a + b
    elif op == '-':
        r = a - b
    elif op == '*':
        r = a * b
    else:
        if b == 0:
            raise Fault('division by zero')
        q = abs(a) // abs(b)          # truncation toward zero (D11)
        if (a < 0) != (b < 0):
            q = -q
        r = q if op == '/' else a - b * q
    if not INT_MIN <= r <= INT_MAX:
        raise Fault('integer overflow')
    return r


def evaluate(form):
    """Left operand, then right, then the operation (D12); the first fault
    to happen is the one reported. An explicit stack of (form, operands
    so far), so depth is not a limit."""
    values = []
    todo = [(form, False)]
    while todo:
        (kind, v), done = todo.pop()
        if kind == 'int':
            values.append(v)
        elif done:
            b = values.pop()
            a = values.pop()
            values.append(apply(v[0][1], a, b))
        else:
            todo.append(((kind, v), True))
            todo.append((v[2], False))      # popped second
            todo.append((v[1], False))      # popped first
    return values[0]


def main(argv):
    if len(argv) != 2:
        sys.exit('usage: calc.py file.lang')
    try:
        forms = parse(open(argv[1], encoding='utf-8', newline='').read())
        if len(forms) != 1:
            raise Outside('a program is one form')
        check(forms[0])
    except Outside as e:
        print(f'outside the referee: {e}', file=sys.stderr)
        return 3
    try:
        sys.stdout.write(f'{evaluate(forms[0])}\n')
    except Fault as f:
        sys.stdout.write(f'fault: {f}\nexit: 1\n')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
