#!/usr/bin/env python3
"""Model for step 1 (expressions on ints, bools and nil): tests 100 to 108.

It writes test programs of many `print` lines and their expected output
from LANGUAGE.md's definition: Python ints for 64-bit ints with a range
check (overflow is a fault, never a wrap), truncating `/` and sign-of-
dividend `%` (D14), `==` structural across types (D18), `and`/`or`
short-circuiting and requiring bools (D10). The values are tagged tuples,
so Python's `True == 1` can't leak in. An expression that would fault
is dropped from the generated programs (a fault ends a program, so those
are the hand-written 11x tests). Randomness is a fixed seed, so reruns
are identical; the printer parenthesizes by the precedence table only
where needed, so a wrong precedence in the compiler changes the output.

    python3 t/models/ints.py --program add-sub > t/100-add-sub.ditto
    python3 t/models/ints.py add-sub > t/100-add-sub.expected
    python3 t/models/ints.py --program mul > t/101-mul.ditto
    python3 t/models/ints.py mul > t/101-mul.expected
    python3 t/models/ints.py --program div-mod > t/102-div-mod.ditto
    python3 t/models/ints.py div-mod > t/102-div-mod.expected
    python3 t/models/ints.py --program neg-not > t/103-neg-not.ditto
    python3 t/models/ints.py neg-not > t/103-neg-not.expected
    python3 t/models/ints.py --program compare > t/104-compare.ditto
    python3 t/models/ints.py compare > t/104-compare.expected
    python3 t/models/ints.py --program equality > t/105-equality.ditto
    python3 t/models/ints.py equality > t/105-equality.expected
    python3 t/models/ints.py --program precedence > t/106-precedence.ditto
    python3 t/models/ints.py precedence > t/106-precedence.expected
    python3 t/models/ints.py --program logic > t/107-logic.ditto
    python3 t/models/ints.py logic > t/107-logic.expected
    python3 t/models/ints.py --program short-circuit > t/108-short-circuit.ditto
    python3 t/models/ints.py short-circuit > t/108-short-circuit.expected
"""
import random
import sys

MAX = 2**63 - 1
MIN = -(2**63)


class Fault(Exception):
    pass


# Expressions: ('int', n) n >= 0, ('bool', b), ('nil',), ('neg', e),
# ('not', e), (op, l, r) for the binary operators.
def lit(n): return ('int', n)
def neg(e): return ('neg', e)
def b(op, l, r): return (op, l, r)

TRUE, FALSE, NIL = ('bool', True), ('bool', False), ('nil',)
EDGE = [lit(0), lit(1), neg(lit(1)), lit(7), neg(lit(7)), lit(MAX), neg(lit(MAX)),
        b('-', neg(lit(MAX)), lit(1))]            # the last is MIN
ARITH = ['+', '-', '*', '/', '%']
ORDER = ['<', '<=', '>', '>=']
EQ = ['==', '!=']


def typename(v): return v[0]


def trunc_div(x, y):
    q = abs(x) // abs(y)
    return q if (x < 0) == (y < 0) else -q


def checked(n):
    if not MIN <= n <= MAX:
        raise Fault('integer overflow')
    return n


def ev(e):
    """Value of e as a tagged tuple; raises Fault."""
    k = e[0]
    if k in ('int', 'bool'): return e
    if k == 'nil': return e
    if k == 'neg':
        v = ev(e[1])
        if v[0] != 'int': raise Fault('type')
        return ('int', checked(-v[1]))
    if k == 'not':
        v = ev(e[1])
        if v[0] != 'bool': raise Fault('type')
        return ('bool', not v[1])
    if k in ('and', 'or'):
        l = ev(e[1])
        if l[0] != 'bool': raise Fault('type')
        if (k == 'and') == (not l[1]):   # decided by the left operand
            return l
        r = ev(e[2])
        if r[0] != 'bool': raise Fault('type')
        return r
    l, r = ev(e[1]), ev(e[2])
    if k == '==': return ('bool', l == r)
    if k == '!=': return ('bool', l != r)
    if l[0] != 'int' or r[0] != 'int': raise Fault('type')
    x, y = l[1], r[1]
    if k == '+': return ('int', checked(x + y))
    if k == '-': return ('int', checked(x - y))
    if k == '*': return ('int', checked(x * y))
    if k in ('/', '%'):
        if y == 0: raise Fault('division by zero')
        q = checked(trunc_div(x, y))
        return ('int', q if k == '/' else x - q * y)
    if k == '<': return ('bool', x < y)
    if k == '<=': return ('bool', x <= y)
    if k == '>': return ('bool', x > y)
    if k == '>=': return ('bool', x >= y)
    raise AssertionError(k)


def show(v):
    if v[0] == 'int': return str(v[1])
    if v[0] == 'bool': return 'true' if v[1] else 'false'
    return 'nil'


# Precedence levels of LANGUAGE.md, loosest first (else and in come later).
LEVEL = {'or': 1, 'and': 2, 'not': 3, '==': 4, '!=': 4, '<': 4, '<=': 4, '>': 4, '>=': 4,
         '+': 5, '-': 5, '*': 6, '/': 6, '%': 6, 'neg': 8}


def level(e):
    return 10 if e[0] in ('int', 'bool', 'nil') else LEVEL[e[0]]


def text(e, need=0, rng=None):
    """Source for e, parenthesized only where `need` (the level the
    context requires) demands it; with rng, sometimes where it doesn't."""
    k = e[0]
    if k == 'int': s = str(e[1])
    elif k == 'bool': s = 'true' if e[1] else 'false'
    elif k == 'nil': s = 'nil'
    elif k == 'neg': s = '-' + text(e[1], 9, rng)       # operand: an atom
    elif k == 'not': s = 'not ' + text(e[1], 3, rng)
    elif LEVEL[k] == 4:                                  # comparisons don't chain
        s = f'{text(e[1], 5, rng)} {k} {text(e[2], 5, rng)}'
    else:                                                # left associative
        L = LEVEL[k]
        s = f'{text(e[1], L, rng)} {k} {text(e[2], L + 1, rng)}'
    if level(e) < need or (rng is not None and k not in ('int', 'bool', 'nil') and rng.random() < 0.1):
        s = f'({s})'
    return s


def line(e, rng=None):
    return f'print({text(e, 0, rng)})'


def tidy(exprs):
    """The expressions that don't fault, with their printed values."""
    out = []
    for e in exprs:
        try:
            out.append((e, show(ev(e))))
        except Fault:
            pass
    return out


# Generators ---------------------------------------------------------------

def gen_int(rng, d):
    if d == 0 or rng.random() < 0.25:
        return rng.choice(EDGE) if rng.random() < 0.6 else lit(rng.randrange(0, 30))
    if rng.random() < 0.15:
        return neg(gen_int(rng, d - 1))
    return b(rng.choice(ARITH), gen_int(rng, d - 1), gen_int(rng, d - 1))


def gen_any(rng, d):
    r = rng.random()
    if r < 0.6: return gen_int(rng, d)
    if r < 0.8: return gen_bool(rng, d)
    return NIL


def gen_bool(rng, d):
    if d == 0 or rng.random() < 0.2:
        return rng.choice([TRUE, FALSE])
    r = rng.random()
    if r < 0.15: return ('not', gen_bool(rng, d - 1))
    if r < 0.4: return b(rng.choice(['and', 'or']), gen_bool(rng, d - 1), gen_bool(rng, d - 1))
    if r < 0.8: return b(rng.choice(ORDER), gen_int(rng, d - 1), gen_int(rng, d - 1))
    return b(rng.choice(EQ), gen_any(rng, d - 1), gen_any(rng, d - 1))


def generate(rng, gen, depth, n):
    out = []
    while len(out) < n:
        out += tidy([gen(rng, depth)])
    return out


# The tests ----------------------------------------------------------------

def pairs(ops, pool=EDGE):
    return [b(op, x, y) for op in ops for x in pool for y in pool]


def t_add_sub(): return tidy(pairs(['+', '-']))
def t_mul(): return tidy(pairs(['*']))
def t_div_mod(): return tidy(pairs(['/', '%']))
def t_neg_not():
    return tidy([neg(x) for x in EDGE] + [neg(neg(x)) for x in EDGE]
                + [('not', TRUE), ('not', FALSE), ('not', ('not', TRUE)), ('not', ('not', FALSE)),
                   neg(neg(neg(lit(5))))])
def t_compare(): return tidy(pairs(ORDER + EQ))
def t_equality():
    pool = [NIL, TRUE, FALSE, lit(0), lit(1), neg(lit(1)), lit(MAX)]
    return tidy(pairs(EQ, pool))
def t_precedence(): return generate(random.Random(106), gen_any, 4, 220)
def t_logic():
    rng = random.Random(107)
    simple = [b(op, x, y) for op in ('and', 'or') for x in (TRUE, FALSE) for y in (TRUE, FALSE)]
    simple += [('not', b(op, x, y)) for op in ('and', 'or') for x in (TRUE, FALSE) for y in (TRUE, FALSE)]
    simple += [b('or', FALSE, b('and', TRUE, TRUE)), b('or', TRUE, b('and', FALSE, TRUE)),
               b('and', ('not', FALSE), ('not', ('not', TRUE)))]
    return tidy(simple) + generate(rng, gen_bool, 4, 120)


def t_short_circuit():
    risky = [b('==', b('/', lit(1), lit(0)), lit(0)),                  # division by zero
             b('>', b('+', lit(MAX), lit(1)), lit(0)),                 # overflow
             b('<', b('-', NIL, lit(1)), lit(0)),                      # type error
             lit(1),                                                   # not a bool
             b('and', lit(1), TRUE),
             ('not', lit(3))]
    out = []
    for r in risky:
        out += [b('and', FALSE, r), b('or', TRUE, r),
                b('and', FALSE, b('and', TRUE, r)), b('or', TRUE, b('or', FALSE, r)),
                b('or', b('and', FALSE, r), TRUE), ('not', b('and', FALSE, r)),
                b('and', b('or', TRUE, TRUE), b('or', TRUE, r))]
    return tidy(out)


TESTS = {
    'add-sub': t_add_sub, 'mul': t_mul, 'div-mod': t_div_mod, 'neg-not': t_neg_not,
    'compare': t_compare, 'equality': t_equality, 'precedence': t_precedence,
    'logic': t_logic, 'short-circuit': t_short_circuit,
}


def main(argv):
    program = '--program' in argv
    names = [a for a in argv if not a.startswith('--')]
    if len(names) != 1 or names[0] not in TESTS:
        sys.exit('usage: ints.py [--program] ' + '|'.join(TESTS))
    items = TESTS[names[0]]()
    # One printer rng per test, independent of the generators' rng.
    prng = random.Random(names[0]) if names[0] == 'precedence' else None
    if program:
        sys.stdout.write(''.join(line(e, prng) + '\n' for e, _ in items))
    else:
        sys.stdout.write(''.join(v + '\n' for _, v in items))


main(sys.argv[1:])
