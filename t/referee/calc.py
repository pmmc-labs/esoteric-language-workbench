#!/usr/bin/env python3
"""The referee: an evaluator of the calculator from its decisions (D3 to
D7, D11 to D19), on Python's unbounded integers, with the 63-bit range
and the division and shift rules applied as the decisions say. Written
from DECISIONS.md and not from the runtime, so that it is a second
implementation, and `make checks` runs it over every golden test and
fails where the two disagree. A program it doesn't cover (an operator
it has no entry for) is reported as such, exit 3, and the check skips
it; the large model extends it when a step's proposal says a referee
is wanted (docs/PROCESS.md, "The referee").

The builder of a step does not read this file: that's what makes the
referee's agreement with the builder's model worth something. The
judge runs it.

    python3 t/referee/calc.py t/010-arith.lang
"""

import sys

MIN, MAX = -(2**62), 2**62 - 1

class Fault(Exception):
    pass

def fit(n):
    if n < MIN or n > MAX:
        raise Fault('overflow')
    return n

def need_int(v):
    if isinstance(v, bool):
        raise Fault('not an integer')
    return v

def quot(a, b):
    if b == 0:
        raise Fault('division by zero')
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q

# The quotient can overflow (MIN / -1); the remainder never can, and
# D5 puts no range check on it: (% MIN -1) is 0.
def div(a, b):
    return fit(quot(a, b))

def mod(a, b):
    return a - quot(a, b) * b

def shift_count(n):
    if n < 0 or n > 62:
        raise Fault('bad shift')
    return n

BIN = {
    '+': lambda a, b: fit(need_int(a) + need_int(b)),
    '-': lambda a, b: fit(need_int(a) - need_int(b)),
    '*': lambda a, b: fit(need_int(a) * need_int(b)),
    '/': lambda a, b: div(need_int(a), need_int(b)),
    '%': lambda a, b: mod(need_int(a), need_int(b)),
    '<': lambda a, b: need_int(a) < need_int(b),
    '<=': lambda a, b: need_int(a) <= need_int(b),
    '>': lambda a, b: need_int(a) > need_int(b),
    '>=': lambda a, b: need_int(a) >= need_int(b),
    '==': lambda a, b: a == b and type(a) is type(b),
    '!=': lambda a, b: not (a == b and type(a) is type(b)),
    'bit/and': lambda a, b: need_int(a) & need_int(b),
    'bit/or': lambda a, b: need_int(a) | need_int(b),
    'bit/xor': lambda a, b: need_int(a) ^ need_int(b),
    'bit/shl': lambda a, b: fit(need_int(a) << shift_count(need_int(b))),
    'bit/shr': lambda a, b: need_int(a) >> shift_count(need_int(b)),
    '**': lambda a, b: power(need_int(a), need_int(b)),
}

# D19: a negative exponent faults; 0 ** 0 is 1 as Python's is.
def power(a, b):
    if b < 0:
        raise Fault('bad exponent')
    if b > 64 and abs(a) >= 2:
        raise Fault('overflow')
    return fit(a ** b)

# The reader: integers, symbols, lists; ; comments.
def read(src):
    toks, i = [], 0
    while i < len(src):
        c = src[i]
        if c.isspace():
            i += 1
        elif c == ';':
            while i < len(src) and src[i] != '\n':
                i += 1
        elif c in '()':
            toks.append(c); i += 1
        else:
            j = i
            while j < len(src) and not src[j].isspace() and src[j] not in '();':
                j += 1
            toks.append(src[i:j]); i = j
    def form(k):
        t = toks[k]
        if t == '(':
            items, k = [], k + 1
            while toks[k] != ')':
                item, k = form(k)
                items.append(item)
            return items, k + 1
        d = t[1:] if t.startswith('-') else t
        return (int(t) if d.isdigit() else t), k + 1
    forms, k = [], 0
    while k < len(toks):
        f, k = form(k)
        forms.append(f)
    return forms

def ev(f):
    if isinstance(f, int):
        return f
    if f == '#true':
        return True
    if f == '#false':
        return False
    head, *args = f
    if head == 'if':
        t = ev(args[0])
        if not isinstance(t, bool):
            raise Fault('not a boolean')
        return ev(args[1]) if t else ev(args[2])
    # Arguments left to right; which fault wins when both would is open.
    return BIN[head](ev(args[0]), ev(args[1]))

def show(v):
    return '#true' if v is True else '#false' if v is False else str(v)

if __name__ == '__main__':
    src = open(sys.argv[1]).read()
    forms = read(src)
    assert len(forms) == 1
    try:
        print(show(ev(forms[0])))
    except Fault as e:
        print(f'fault: {e}')
        print('exit: 1')
    except KeyError as e:
        print(f'referee: no entry for {e}', file=sys.stderr)
        sys.exit(3)
