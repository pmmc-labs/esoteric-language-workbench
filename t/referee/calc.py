#!/usr/bin/env python3
"""The calculator's referee: an evaluator written from the decisions,
not from the compiler or the runtime, that prints what a program's
.expected must be.

    python3 t/referee/calc.py t/NNN-name.lang

It prints the value and a newline, or, for a fault, `fault: MESSAGE`
and `exit: 1` on lines of their own (stdout and stderr together, as
t/run.sh compares them), and exits 0. A program it doesn't cover (a
form no decision has given it yet, a compile error, or a test header
that sets input, arguments or the environment) exits 3, with the
reason on stderr, and `make checks` skips it.

What it follows, and where each rule comes from:

  LANGUAGE.md   a literal is an optional `-` and decimal digits; `;`
                comments to the end of a line; a program is one form;
                the value is printed with a newline.
  D3            a fault: its message, then `exit: 1`; stdout is empty,
                since nothing is printed before the value.
  D4, D13       a literal out of 63 bits, or a malformed expression,
                anywhere in the program, is a compile error: found
                before anything runs, so never a fault (here, exit 3).
  D8            (op a b) with op one of + - * / % and two operands.
  D9            each operation's exact result; outside 63 bits, the
                fault `integer overflow`, intermediate results too.
  D10           / truncates toward zero, % takes the dividend's sign;
                a zero divisor is `division by zero`. Python's // and
                % floor, so truncation is worked on the magnitudes.
  D11           operands left to right; the first fault ends it.
  D12           every operation at run time; no positions in a fault.

The builder of a step doesn't read this file (docs/PROCESS.md, "The
referee"): it's what their model is checked against.
"""

import re
import sys

LO, HI = -(2 ** 62), 2 ** 62 - 1
SPACE = ' \t\n\r'               # what the language counts as whitespace
LITERAL = re.compile(r'-?[0-9]+', re.ASCII)
OPERATORS = ('+', '-', '*', '/', '%')
HEADERS = re.compile(r'^; (stdin|args|env):', re.M)


class Outside(Exception):
    """A program this referee doesn't cover, or one that doesn't compile."""


class Fault(Exception):
    """A fault at run time (D3, D12): the message, without a position."""


class Symbol(str):
    """A symbol, kept apart from integers and lists."""


def tokens(text):
    out, i = [], 0
    while i < len(text):
        c = text[i]
        if c in SPACE:
            i += 1
        elif c == ';':
            while i < len(text) and text[i] != '\n':
                i += 1
        elif c in '()':
            out.append(c)
            i += 1
        else:
            j = i
            while j < len(text) and text[j] not in SPACE and text[j] not in '();':
                j += 1
            out.append(text[i:j])
            i = j
    return out


def parse(toks):
    """Every top-level form: an int, a Symbol, or a list of forms."""
    forms, stack = [], [[]]
    for t in toks:
        if t == '(':
            stack.append([])
        elif t == ')':
            if len(stack) == 1:
                raise Outside("unexpected ')'")
            done = stack.pop()
            stack[-1].append(done)
        else:
            stack[-1].append(int(t) if LITERAL.fullmatch(t) else Symbol(t))
    if len(stack) != 1:
        raise Outside("missing ')'")
    return stack[0]


def check(form):
    """D13's checks, in its order, over the whole program before it runs."""
    if isinstance(form, Symbol):
        raise Outside(f'unexpected symbol {form}')
    if isinstance(form, int):
        if not LO <= form <= HI:
            raise Outside('integer out of range')
        return
    if not form:
        raise Outside('empty list')
    head = form[0]
    if not isinstance(head, Symbol):
        raise Outside('expected an operator')
    if head not in OPERATORS:
        raise Outside(f'unknown operator {head} (not a form this referee covers)')
    if len(form) != 3:
        raise Outside(f'{head} takes 2 operands')
    for operand in form[1:]:
        check(operand)


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
        q = abs(a) // abs(b)                    # magnitudes: truncation, not floor
        if (a < 0) != (b < 0):
            q = -q
        r = q if op == '/' else a - b * q
    if not LO <= r <= HI:
        raise Fault('integer overflow')
    return r


def evaluate(form):
    if isinstance(form, int):
        return form
    op, left, right = form
    a = evaluate(left)                          # D11: left first
    b = evaluate(right)
    return apply(op, a, b)


def main(argv):
    if len(argv) != 1:
        sys.exit(__doc__)
    text = open(argv[0], encoding='utf-8').read()
    try:
        if HEADERS.search(text):
            raise Outside('a header this referee doesn\'t model')
        forms = parse(tokens(text))
        if len(forms) != 1:
            raise Outside('a program is one form')
        check(forms[0])
    except Outside as e:
        print(f'{argv[0]}: outside the referee: {e}', file=sys.stderr)
        sys.exit(3)
    sys.setrecursionlimit(10000)
    try:
        sys.stdout.write(f'{evaluate(forms[0])}\n')
    except Fault as e:
        sys.stdout.write(f'fault: {e}\nexit: 1\n')


if __name__ == '__main__':
    main(sys.argv[1:])
