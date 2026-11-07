#!/usr/bin/env python3
"""Model for step 7 (`else`, D20): tests 700 to 709 (and the standard input
of 704 and 706).

Each test is a Ditto program and the output LANGUAGE.md defines for it,
worked out here by Python, never by running the compiler. The model keeps
a tree for each expression. `render` writes the tree as Ditto source with
the precedence table of LANGUAGE.md (so a tree for `m["z"] else 0 + 1`
needs no parentheses and one for `m["z"] else (0 + 1)` has them), and `ev`
evaluates the tree: a lookup that finds nothing raises `Miss`, a wrong type
raises `Fault`, and `else` is a Python `try` around its left operand.
That is the lexical rule for these programs because none of the trees here
calls a function that looks something up; the programs where a miss
happens in a called function are faults and written by hand. A call of the
function `note` prints, so the order and the laziness of evaluation show.
The tests that print the same tree twice print its minimal source and its
fully parenthesised source, which must agree.

Tests 700 to 703 are fixed expressions: every lookup (list, string, map,
`.name`, `int`) hitting and missing; chains `a else b else c`; precedence
against every operator, minimal and fully parenthesised; laziness, order
of evaluation, and lookups inside arguments, index expressions, list and
map literals and interpolations. Test 704 counts words (`counts[w] else 0
+ 1`) from standard input, 705 finds routes (`roads[here] else []`), 706
parses `key=value` lines from standard input (`int(value) else value`),
707 uses `else` in every statement position. Tests 708 and 709 are random
expressions over lists, maps, strings and `int`, with `else` nested
anywhere, chosen so that no miss escapes and nothing overflows. Seeds are
fixed, so reruns are identical.

    python3 t/models/fallback.py --program lookups > t/700-lookups.ditto
    python3 t/models/fallback.py lookups > t/700-lookups.expected
    python3 t/models/fallback.py --program chains > t/701-chains.ditto
    python3 t/models/fallback.py chains > t/701-chains.expected
    python3 t/models/fallback.py --program precedence > t/702-precedence.ditto
    python3 t/models/fallback.py precedence > t/702-precedence.expected
    python3 t/models/fallback.py --program lexical > t/703-lexical.ditto
    python3 t/models/fallback.py lexical > t/703-lexical.expected
    python3 t/models/fallback.py --program word-count > t/704-word-count.ditto
    python3 t/models/fallback.py --stdin word-count > t/704-word-count.stdin
    python3 t/models/fallback.py word-count > t/704-word-count.expected
    python3 t/models/fallback.py --program routes > t/705-routes.ditto
    python3 t/models/fallback.py routes > t/705-routes.expected
    python3 t/models/fallback.py --program config > t/706-config.ditto
    python3 t/models/fallback.py --stdin config > t/706-config.stdin
    python3 t/models/fallback.py config > t/706-config.expected
    python3 t/models/fallback.py --program statements > t/707-statements.ditto
    python3 t/models/fallback.py statements > t/707-statements.expected
    python3 t/models/fallback.py --program random-a > t/708-random-a.ditto
    python3 t/models/fallback.py random-a > t/708-random-a.expected
    python3 t/models/fallback.py --program random-b > t/709-random-b.ditto
    python3 t/models/fallback.py random-b > t/709-random-b.expected
"""
import functools
import random
import re
import sys

MAX = 2**63 - 1
MIN = -(2**63)


class Miss(Exception):
    """A lookup found nothing: what `else` catches."""


class Fault(Exception):
    """Anything else the definition makes a fault: a model program must not
    do one, so this ends the model (or, in the random tests, the tree)."""


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def checked(n):
    if not MIN <= n <= MAX:
        raise Fault('integer overflow')
    return n


# --- The definition: equality, order, printed form, source form -------------

def eq(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return len(a) == len(b) and all(k in b and eq(v, b[k]) for k, v in a.items())
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    if isinstance(a, (list, dict)) or isinstance(b, (list, dict)):
        return False
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if is_int(a) and is_int(b):
        return a == b
    return isinstance(a, str) and isinstance(b, str) and a == b


def cmp(a, b):
    if is_int(a) and is_int(b):
        return (a > b) - (a < b)
    if isinstance(a, str) and isinstance(b, str):
        x, y = a.encode(), b.encode()
        return (x > y) - (x < y)
    if isinstance(a, list) and isinstance(b, list):
        for x, y in zip(a, b):
            c = cmp(x, y)
            if c != 0:
                return c
        return (len(a) > len(b)) - (len(a) < len(b))
    raise Fault('cannot compare')


def sort_list(xs):
    return sorted(xs, key=functools.cmp_to_key(cmp))


ESC = {'\\': '\\\\', '"': '\\"', '\n': '\\n', '\t': '\\t', '\r': '\\r'}


def show(v, quoted=False):
    if v is True: return 'true'
    if v is False: return 'false'
    if v is None: return 'nil'
    if isinstance(v, str):
        assert v.isascii()
        return '"' + ''.join(ESC.get(c, c) for c in v) + '"' if quoted else v
    if isinstance(v, list):
        return '[' + ', '.join(show(x, True) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ', '.join(show(k, True) + ': ' + show(x, True) for k, x in v.items()) + '}'
    return str(v)


KEYWORDS = set('and break continue else false fn for if in let nil not or return true while'.split())


def is_name(s):
    return re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', s) is not None and s not in KEYWORDS


def lit(v):
    """Ditto source for the value v (no negative literal: `-5` is a prefix
    minus on 5, which is how LANGUAGE.md writes one)."""
    if v is True: return 'true'
    if v is False: return 'false'
    if v is None: return 'nil'
    if isinstance(v, str):
        return '"' + ''.join(ESC.get(c, '\\{' if c == '{' else c) for c in v) + '"'
    if isinstance(v, list):
        return '[' + ', '.join(lit(x) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ', '.join(
            f'{k if isinstance(k, str) and is_name(k) else lit(k)}: {lit(x)}' for k, x in v.items()) + '}'
    assert v != MIN
    return f'-{-v}' if v < 0 else str(v)


def trunc_div(x, y):
    q = abs(x) // abs(y)
    return q if (x < 0) == (y < 0) else -q


# --- Expression trees --------------------------------------------------------
# ('int', n) ('str', s) ('bool', b) ('nil',) ('list', [node]) ('map', [(key, node)])
# ('var', name) ('ix', c, i) ('fld', c, name) ('toint', e) ('else', l, r)
# ('bin', op, l, r) ('logic', op, l, r) ('neg', e) ('interp', [str | node])
# ('call', name, [node])

def lift(x):
    if isinstance(x, tuple):
        return x
    if x is None: return ('nil',)
    if isinstance(x, bool): return ('bool', x)
    if is_int(x): return ('int', x)
    if isinstance(x, str): return ('str', x)
    if isinstance(x, list): return ('list', [lift(y) for y in x])
    if isinstance(x, dict): return ('map', [(k, lift(y)) for k, y in x.items()])
    raise AssertionError(x)


def V(name): return ('var', name)
def X(c, i): return ('ix', lift(c), lift(i))
def F(c, name): return ('fld', lift(c), name)
def I(e): return ('toint', lift(e))
def E(l, r, *more):
    node = ('else', lift(l), lift(r))
    for m in more:
        node = ('else', node, lift(m))
    return node
def B(op, l, r): return ('bin', op, lift(l), lift(r))
def L(op, l, r): return ('logic', op, lift(l), lift(r))
def N(e): return ('neg', lift(e))
def S(*parts): return ('interp', [p if isinstance(p, str) else lift(p) for p in parts])
def C(name, *args): return ('call', name, [lift(a) for a in args])
def ML(*items): return ('list', [lift(a) for a in items])
def MM(**items): return ('map', [(k, lift(v)) for k, v in items.items()])


def prec(n):
    k = n[0]
    if k == 'int': return 8 if n[1] < 0 else 9
    if k == 'bin': return {'==': 4, '<': 4, '+': 5, '-': 5, '*': 6, '/': 6, '%': 6}[n[1]]
    if k == 'logic': return 1 if n[1] == 'or' else 2
    if k == 'else': return 7
    if k == 'neg': return 8
    return 9


def render(n, need=0, full=False):
    """Source for n where an operand of precedence `need` is expected; with
    `full`, every operator expression is parenthesised."""
    s = raw(n, full)
    if prec(n) < need or (full and prec(n) < 9 and need > 0):
        return '(' + s + ')'
    return s


def raw(n, full):
    k = n[0]
    if k == 'int': return f'-{-n[1]}' if n[1] < 0 else str(n[1])
    if k == 'str': return lit(n[1])
    if k == 'bool': return lit(n[1])
    if k == 'nil': return 'nil'
    if k == 'var': return n[1]
    if k == 'list': return '[' + ', '.join(render(x, 0, full) for x in n[1]) + ']'
    if k == 'map':
        return '{' + ', '.join(f'{key if is_name(key) else lit(key)}: {render(x, 0, full)}' for key, x in n[1]) + '}'
    if k == 'ix': return f'{render(n[1], 9, full)}[{render(n[2], 0, full)}]'
    if k == 'fld': return f'{render(n[1], 9, full)}.{n[2]}'
    if k == 'toint': return f'int({render(n[1], 0, full)})'
    if k == 'call': return f'{n[1]}(' + ', '.join(render(a, 0, full) for a in n[2]) + ')'
    if k == 'neg':
        inner = render(n[1], 8, full)
        return '-(' + inner + ')' if inner.startswith('-') else '-' + inner
    if k == 'else': return f'{render(n[1], 7, full)} else {render(n[2], 8, full)}'
    if k in ('bin', 'logic'):
        p = prec(n)
        lo = p + 1 if p == 4 else p
        return f'{render(n[2], lo, full)} {n[1]} {render(n[3], p + 1, full)}'
    if k == 'interp':
        out = ''
        for part in n[1]:
            if isinstance(part, str):
                out += ''.join(ESC.get(c, '\\{' if c == '{' else c) for c in part)
            else:
                out += '{' + render(part, 0, full) + '}'
        return '"' + out + '"'
    raise AssertionError(k)


def has_lookup(n):
    k = n[0]
    if k in ('ix', 'fld', 'toint'):
        return True
    if k in ('int', 'str', 'bool', 'nil', 'var'):
        return False
    if k == 'list': return any(has_lookup(x) for x in n[1])
    if k == 'map': return any(has_lookup(x) for _, x in n[1])
    if k == 'call': return any(has_lookup(x) for x in n[2])
    if k == 'neg': return has_lookup(n[1])
    if k == 'interp': return any(has_lookup(p) for p in n[1] if not isinstance(p, str))
    if k == 'else': return has_lookup(n[1]) or has_lookup(n[2])
    return has_lookup(n[2]) or has_lookup(n[3])


def lookup_index(c, i):
    if isinstance(c, (list, str)):
        if not is_int(i): raise Fault('index must be an int')
        if i < 0 or i >= len(c): raise Miss()
        return c[i]
    if isinstance(c, dict):
        if not (is_int(i) or isinstance(i, str)): raise Fault('bad key')
        if i not in c: raise Miss()
        return c[i]
    raise Fault('cannot index')


def to_int(s):
    if not isinstance(s, str): raise Fault('int: expected a string')
    if re.fullmatch(r'-?[0-9]+', s) is None: raise Miss()
    n = int(s)
    if not MIN <= n <= MAX: raise Miss()
    return n


def ev(n, env, log):
    k = n[0]
    if k in ('int', 'str', 'bool'): return n[1]
    if k == 'nil': return None
    if k == 'var': return env[n[1]]
    if k == 'list': return [ev(x, env, log) for x in n[1]]
    if k == 'map':
        out = {}
        for key, x in n[1]:
            out[key] = ev(x, env, log)
        return out
    if k == 'ix':
        c = ev(n[1], env, log)
        return lookup_index(c, ev(n[2], env, log))
    if k == 'fld':
        c = ev(n[1], env, log)
        if not isinstance(c, dict): raise Fault('cannot use .name')
        if n[2] not in c: raise Miss()
        return c[n[2]]
    if k == 'toint': return to_int(ev(n[1], env, log))
    if k == 'neg':
        v = ev(n[1], env, log)
        if not is_int(v): raise Fault('neg')
        return checked(-v)
    if k == 'else':
        try:
            return ev(n[1], env, log)
        except Miss:
            return ev(n[2], env, log)
    if k == 'call':
        args = [ev(a, env, log) for a in n[2]]
        assert n[1] == 'note' and len(args) == 1
        log.append('note ' + show(args[0]))
        return args[0]
    if k == 'interp':
        return ''.join(p if isinstance(p, str) else show(ev(p, env, log)) for p in n[1])
    if k == 'logic':
        a = ev(n[2], env, log)
        if not isinstance(a, bool): raise Fault('and/or')
        if (n[1] == 'and') != a: return a
        b = ev(n[3], env, log)
        if not isinstance(b, bool): raise Fault('and/or')
        return b
    if k == 'bin':
        a = ev(n[2], env, log)
        b = ev(n[3], env, log)
        op = n[1]
        if op == '==': return eq(a, b)
        if op == '<': return cmp(a, b) < 0
        if op == '+' and isinstance(a, (str, list)) and type(a) is type(b): return a + b
        if not (is_int(a) and is_int(b)): raise Fault('type')
        if op == '+': return checked(a + b)
        if op == '-': return checked(a - b)
        if op == '*': return checked(a * b)
        if b == 0: raise Fault('division by zero')
        q = trunc_div(a, b)
        return checked(q) if op == '/' else a - q * b
    raise AssertionError(k)


class Prog:
    def __init__(self):
        self.src = []
        self.out = []
        self.env = {}

    def line(self, *s):
        self.src.extend(s)

    def let(self, name, v):
        self.line(f'let {name} = {lit(v)}')
        self.env[name] = v

    def say(self, *vals):
        self.out.append(' '.join(show(v) for v in vals))

    def case(self, node, both=False):
        """print(node), and with `both` print(node) again fully parenthesised."""
        for full in ((False, True) if both else (False,)):
            log = []
            v = ev(node, self.env, log)
            self.line(f'print({render(node, 0, full)})')
            self.out.extend(log)
            self.say(v)

    def program(self):
        return '\n'.join(self.src) + '\n'

    def output(self):
        return ''.join(l + '\n' for l in self.out)


# --- 700: every lookup, hitting and missing ---------------------------------

def env_basic(p):
    p.let('xs', [10, 20, 30])
    p.let('s', 'abc')
    p.let('m', {'a': 1, 'b': 2, 'two words': 3, 7: 'seven', 'e': [], -1: 'minus'})
    p.let('deep', {'list': [1, [2, 3]], 'rec': {'k': 'v'}, 'nothing': None})
    p.let('n1', '42')
    p.let('bad', '4x')
    p.let('neg', '-17')
    p.let('empty', '')
    p.let('big', '9223372036854775808')
    p.let('lo', '-9223372036854775808')
    p.let('toolo', '-9223372036854775809')


def lookups():
    p = Prog()
    env_basic(p)
    for i in [0, 1, 2, 3, 4, -1, -3, 1000]:
        p.case(E(X(V('xs'), i), 'none'))
    for i in [0, 2, 3, -1]:
        p.case(E(X(V('s'), i), 'none'))
    for k in ['a', 'b', 'z', '', 'two words', 7, 8, -1, 0]:
        p.case(E(X(V('m'), k), 'none'))
    for name in ['a', 'b', 'e', 'z', 'two']:
        p.case(E(F(V('m'), name), 'none'))
    p.case(E(F(F(V('deep'), 'rec'), 'k'), 'none'))
    p.case(E(F(F(V('deep'), 'rec'), 'q'), 'none'))
    p.case(E(F(F(V('deep'), 'nope'), 'k'), 'none'))
    p.case(E(X(F(V('deep'), 'list'), 1), 'none'))
    p.case(E(X(X(F(V('deep'), 'list'), 1), 0), 'none'))
    p.case(E(X(X(F(V('deep'), 'list'), 1), 5), 'none'))
    p.case(E(X(X(F(V('deep'), 'list'), 9), 0), 'none'))
    p.case(E(F(V('deep'), 'nothing'), 'default'))
    for v in ['n1', 'bad', 'neg', 'empty', 'big', 'lo', 'toolo']:
        p.case(E(I(V(v)), 'not a number'))
    for t in ['0', '-0', '007', '+5', ' 5', '5 ', '0x10', '-', '--1', '1_000', '1.5', '9223372036854775807']:
        p.case(E(I(t), -1))
    for d in [None, True, 'text', [1, 'two'], {'k': 'v'}, [], {}]:
        p.case(E(X(V('xs'), 9), d))
    return p


# --- 701: chains --------------------------------------------------------------

def chains():
    p = Prog()
    env_basic(p)
    xs, m = V('xs'), V('m')
    for a, b, c in [(0, 1, 2), (7, 1, 2), (7, 8, 2), (7, 8, 9), (7, 1, 9)]:
        p.case(E(X(xs, a), X(xs, b), X(xs, c), 'last'), both=True)
    p.case(E(F(m, 'z'), F(m, 'y'), F(m, 'b'), 0), both=True)
    p.case(E(F(m, 'z'), F(m, 'y'), F(m, 'x'), 0), both=True)
    p.case(E(X(xs, 5), E(X(xs, 6), 3)), both=True)             # a else (b else c)
    p.case(E(X(xs, 5), E(X(xs, 1), 3)), both=True)
    p.case(E(E(X(xs, 5), F(m, 'z')), 4), both=True)            # the inner default misses
    p.case(E(E(X(xs, 5), F(m, 'a')), 4), both=True)
    p.case(E(E(X(xs, 0), F(m, 'z')), 4), both=True)
    p.case(E(I('x'), I('y'), I('37'), 0), both=True)
    p.case(E(I('x'), I('y'), I('z'), 0), both=True)
    p.case(E(X(xs, 3), X(m, 'a'), 99), both=True)
    # the default is itself a lookup, deep in a record
    p.case(E(F(F(V('deep'), 'no'), 'k'), F(F(V('deep'), 'rec'), 'k'), 'none'), both=True)
    p.case(E(X(X(F(V('deep'), 'list'), 1), 7), X(X(F(V('deep'), 'list'), 1), 1), -1), both=True)
    return p


# --- 702: precedence ----------------------------------------------------------

def precedence():
    p = Prog()
    env_basic(p)
    xs, m = V('xs'), V('m')
    miss, hit = X(xs, 9), X(xs, 1)
    for op in ['+', '-', '*', '/', '%', '==', '<']:
        for lhs in (miss, hit):
            p.case(B(op, E(lhs, 7), 3), both=True)          # (lhs else 7) op 3
            p.case(B(op, 30, E(lhs, 7)), both=True)         # 30 op (lhs else 7)
            p.case(B(op, E(lhs, 7), E(X(xs, 8), 2)), both=True)
    p.case(B('+', E(miss, 0), 1), both=True)
    p.case(B('+', E(hit, 0), 1), both=True)
    p.case(E(miss, B('+', 0, 1)), both=True)                   # else (0 + 1)
    p.case(B('*', 2, E(miss, 5)), both=True)
    p.case(E(B('*', 2, miss), 5), both=True)                  # (2 * xs[9]) else 5
    p.case(E(B('+', X(xs, 0), miss), 5), both=True)           # the miss is the right operand of +
    p.case(E(N(miss), 5), both=True)                          # (-xs[9]) else 5
    p.case(E(N(hit), 5), both=True)
    p.case(N(E(miss, 5)), both=True)                          # -(xs[9] else 5)
    p.case(E(miss, N(5)), both=True)                          # else -5
    p.case(N(E(miss, N(5))), both=True)
    p.case(B('-', E(miss, 1), E(X(xs, 7), 2), ), both=True)
    p.case(B('-', B('-', 10, E(miss, 1)), E(X(xs, 7), 2)), both=True)
    p.case(L('and', B('==', X(xs, 0), 10), E(F(m, 'z'), False)), both=True)
    p.case(L('or', B('==', E(miss, 0), 0), E(F(m, 'z'), False)), both=True)
    p.case(L('and', E(F(m, 'z'), False), True), both=True)
    p.case(L('or', E(F(m, 'z'), True), False), both=True)
    p.case(B('<', E(miss, 100), 5), both=True)
    p.case(B('==', E(F(m, 'z'), None), None), both=True)
    p.case(B('+', E(X('abc', 5), 'x'), 'y'), both=True)
    p.case(B('+', E(X(V('s'), 5), 'x'), E(X(V('s'), 1), 'y')), both=True)
    p.case(B('+', ML(1), E(F(m, 'e'), ML(2))), both=True)
    p.case(B('+', ML(1), E(F(m, 'zz'), ML(2))), both=True)
    return p


# --- 703: what is caught, order, laziness ------------------------------------

NOTE = ['fn note(x) {', '  print("note", x)', '  return x', '}']


def lexical():
    p = Prog()
    p.line(*NOTE)
    env_basic(p)
    xs, m = V('xs'), V('m')
    p.case(E(X(xs, 0), C('note', 'default')))                  # right side never runs
    p.case(E(X(xs, 9), C('note', 'default')))
    p.case(E(X(xs, 0), X(xs, 99)))                             # a right side that would miss
    p.case(E(X(xs, C('note', 5)), C('note', 0)))               # index, then default
    p.case(E(X(xs, C('note', 1)), C('note', 0)))
    p.case(E(C('note', X(xs, 9)), 7))                          # the lookup is written in the left: caught, note never runs
    p.case(E(C('note', X(xs, 0)), 7))
    p.case(E(B('+', C('note', 1), X(xs, C('note', 9))), C('note', 2)))
    p.case(E(B('+', C('note', X(xs, 9)), C('note', 1)), C('note', 2)))   # note(1) never runs
    p.case(E(X(xs, X(m, 'z')), -1))                            # a miss inside an index expression
    p.case(E(X(xs, X(m, 'b')), -1))
    p.case(E(X(xs, X(xs, X(xs, 0))), -1))                      # xs[xs[xs[0]]]: xs[10] misses
    p.case(E(X(xs, X(xs, X(xs, 7))), -1))
    p.case(E(X(V('s'), I('2')), 'none'))
    p.case(E(X(V('s'), I('two')), 'none'))
    p.case(E(S('{', X(xs, 9), '}'), 'none'))                  # interpolation
    p.case(E(S('v=', X(xs, 0), '!'), 'none'))
    p.case(E(S('v=', X(xs, 9), '!'), 'none'))
    p.case(E(S('a', X(xs, 0), 'b', X(m, 'z'), 'c'), 'none'))
    p.case(E(S('a', X(xs, 0), 'b', E(X(m, 'z'), 'q'), 'c'), 'none'))   # caught inside the braces
    p.case(E(S('n=', I(S(X(xs, 0))), '.'), 'none'))
    p.case(E(S('n=', I(S(F(m, 'a'), 'x')), '.'), 'none'))      # int("1x") misses
    p.case(E(S(S(X(xs, 5))), 'outer'))                         # nested interpolation
    p.case(E(ML(X(xs, 0), X(xs, 9)), ML()))                     # list literal items
    p.case(E(ML(X(xs, 0), X(xs, 1)), ML()))
    p.case(E(MM(a=X(xs, 0), b=F(m, 'z')), MM()))               # map literal values
    p.case(E(MM(a=X(xs, 0), b=F(m, 'b')), MM()))
    p.case(E(X(ML(1, 2, 3), 5), 0))                            # a lookup on a literal
    p.case(E(F(MM(a=1), 'a'), 0))
    p.case(E(F(MM(a=1), 'b'), 0))
    p.case(X(E(X(xs, 9), ML(4, 5)), 1))                        # else inside a lookup's target
    p.case(X(ML(4, 5, 6), E(X(xs, 9), 2)))                     # else inside a lookup's index
    p.case(E(X(X(ML(ML(1), ML(2, 3)), E(X(xs, 7), 1)), E(F(m, 'q'), 1)), -1))
    p.case(E(X(xs, E(F(m, 'q'), 1)), 0))
    p.case(E(X(xs, E(F(m, 'q'), 9)), 0))
    p.case(B('+', E(X(xs, 0), 0), E(C('note', X(xs, 9)), 1)), both=True)
    return p


# --- 704: word count ---------------------------------------------------------

WORD_TEXT = '''the quick brown fox jumps over the lazy dog
The dog barks; the fox runs away. THE END
fox fox fox
'''


def word_count():
    p = Prog()
    p.line('let counts = {}',
           'let order = []',
           'for w in words(lower(read())) {',
           '  counts[w] = counts[w] else 0 + 1',
           '  if counts[w] == 1 { order += [w] }',
           '}',
           'for w in order { print("{w}: {counts[w]}") }',
           'print(counts.the else 0, counts.zebra else 0, counts["fox"] else -1)',
           'print("{counts.dog else 0} dogs, {counts.cat else 0} cats")')
    counts, order = {}, []
    for w in WORD_TEXT.lower().split():
        counts[w] = counts.get(w, 0) + 1
        if counts[w] == 1:
            order.append(w)
    for w in order:
        p.say(f'{w}: {counts[w]}')
    p.say(counts.get('the', 0), counts.get('zebra', 0), counts.get('fox', -1))
    p.say(f"{counts.get('dog', 0)} dogs, {counts.get('cat', 0)} cats")
    return p


# --- 705: route finding ------------------------------------------------------

ROADS = {
    'home': ['bakery', 'park'], 'bakery': ['home', 'market', 'school'],
    'park': ['home', 'lake'], 'market': ['bakery', 'station'],
    'school': ['bakery', 'station'], 'lake': ['park'], 'station': ['market', 'school'],
    'island': [],
}
GOALS = [('home', 'station'), ('lake', 'school'), ('home', 'home'), ('park', 'market'), ('home', 'nowhere'),
         ('nowhere', 'home')]


def route(roads, start, goal):
    came = {start: start}
    queue, nxt = [start], 0
    while nxt < len(queue):
        here = queue[nxt]
        nxt += 1
        if here == goal:
            path = [goal]
            while path[0] != start:
                path = [came[path[0]]] + path
            return path
        for road in roads.get(here, []):
            if road not in came:
                came[road] = here
                queue.append(road)
    return None


def routes():
    p = Prog()
    p.line('fn route(roads, start, goal) {',
           '  let came_from = {}',
           '  came_from[start] = start',
           '  let queue = [start]',
           '  let next = 0',
           '  while next < len(queue) {',
           '    let here = queue[next]',
           '    next += 1',
           '    if here == goal {',
           '      let path = [goal]',
           '      while path[0] != start {',
           '        path = [came_from[path[0]]] + path',
           '      }',
           '      return path',
           '    }',
           '    for road in roads[here] else [] {',
           '      if road not in came_from {',
           '        came_from[road] = here',
           '        queue += [road]',
           '      }',
           '    }',
           '  }',
           '  return nil',
           '}')
    p.let('roads', ROADS)
    for a, b in GOALS:
        p.line(f'print({lit(a)}, {lit(b)}, route(roads, {lit(a)}, {lit(b)}))')
        p.say(a, b, route(ROADS, a, b))
    p.line('print(roads.island else "none", roads.sea else "none", len(roads["bakery"] else []))')
    p.say(ROADS['island'], 'none', 3)
    return p


# --- 706: configuration lines -------------------------------------------------

CONFIG_TEXT = '''port=8080
host=example.org
retries=x3
depth=-12
verbose
name=a=b

timeout=
big=99999999999999999999
'''


def config():
    p = Prog()
    p.line('let raw = {}',
           'let settings = {}',
           'let bare = []',
           'for line in split(read(), "\\n") {',
           '  if line == "" { continue }',
           '  let parts = split(line, "=")',
           '  let value = parts[1] else ""',
           '  if len(parts) == 1 { bare += [parts[0]] }',
           '  raw[parts[0]] = value',
           '  settings[parts[0]] = int(value) else value',
           '}',
           'print(settings)',
           'print(bare)',
           'let port = int(raw.port else "") else 80',
           'let retries = int(raw.retries else "") else 3',
           'let workers = int(raw.workers else "") else 4',
           'print(port, retries, workers)',
           'print(settings.depth else 0, settings.nothing else 0, settings["host"] else "-")')
    raw, settings, bare = {}, {}, []
    for line in CONFIG_TEXT.split('\n'):
        if line == '':
            continue
        parts = line.split('=')
        value = parts[1] if len(parts) > 1 else ''
        if len(parts) == 1:
            bare.append(parts[0])
        raw[parts[0]] = value
        try:
            settings[parts[0]] = to_int(value)
        except Miss:
            settings[parts[0]] = value
    p.say(settings)
    p.say(bare)

    def number(key, d):
        try:
            return to_int(raw[key] if key in raw else '')
        except Miss:
            return d
    p.say(number('port', 80), number('retries', 3), number('workers', 4))
    p.say(settings.get('depth', 0), settings.get('nothing', 0), settings.get('host', '-'))
    return p


# --- 707: else in every statement position -----------------------------------

def statements():
    p = Prog()
    p.line('fn first_word(line) {',
           '  return words(line)[0] else ""',
           '}',
           'fn lookup(table, key) {',
           '  return table[key] else nil',
           '}',
           'fn digits(text) {',
           '  let n = int(text) else -1',
           '  return n',
           '}',
           'let table = {a: 1, b: 2, c: 3}',
           'print(lookup(table, "a"), lookup(table, "zz"), lookup(table, "c"))',
           'print("[" + first_word("hello world") + "]", "[" + first_word("   ") + "]")',
           'print(digits("12"), digits("x"), digits(""), digits("-5"))',
           'let total = 0',
           'for k in ["a", "x", "b", "q", "c"] {',
           '  total += table[k] else 100',
           '}',
           'print(total)',
           'let xs = [3, 2, 1]',
           'let i = 0',
           'let sum = 0',
           'while xs[i] else 0 > 0 {',
           '  sum += xs[i]',
           '  i += 1',
           '}',
           'print(i, sum)',
           'let flags = {on: true}',
           'if flags.on else false {',
           '  print("on")',
           '}',
           'if flags.off else false {',
           '  print("off")',
           '} else {',
           '  print("not off")',
           '}',
           'let pos = {at: 1}',
           'xs[pos.at else 0] = 99',
           'xs[pos.nowhere else 2] = 77',
           'print(xs)',
           'let grid = [[1, 2], [3, 4]]',
           'grid[grid[1][5] else 0][pos.at else 0] += 10',
           'print(grid)',
           'let words2 = {}',
           'for w in ["a", "b", "a"] {',
           '  words2[w] = (words2[w] else []) + [len(words2[w] else [])]',
           '}',
           'print(words2)',
           'let found = nil',
           'for k in keys(table) {',
           '  if table[k] else 0 >= 2 { found = k; break }',
           '}',
           'print(found)',
           'let lists = {a: [1, 2]}',
           'for x in lists.d else [7, 8] { print(x) }',
           'for x in lists.a else [0] { print(x) }')
    table = {'a': 1, 'b': 2, 'c': 3}
    p.say(1, None, 3)
    p.say('[hello]', '[]')
    p.say(12, -1, -1, -5)
    p.say(sum(table.get(k, 100) for k in ['a', 'x', 'b', 'q', 'c']))
    xs = [3, 2, 1]
    i = s = 0
    while (xs[i] if i < len(xs) else 0) > 0:
        s += xs[i]
        i += 1
    p.say(i, s)
    p.say('on')
    p.say('not off')
    xs[1] = 99
    xs[2] = 77
    p.say(xs)
    grid = [[1, 2], [3, 4]]
    grid[0][1] += 10
    p.say(grid)
    w2 = {}
    for w in ['a', 'b', 'a']:
        w2[w] = w2.get(w, []) + [len(w2.get(w, []))]
    p.say(w2)
    found = None
    for k in table:
        if table.get(k, 0) >= 2:
            found = k
            break
    p.say(found)
    p.say(7)
    p.say(8)
    p.say(1)
    p.say(2)
    return p


# --- 708, 709: random expressions --------------------------------------------

RANDOM_ENV = {
    'xs': [4, -3, 0, 12, 7, 1, 25, -8],
    'mi': {0: 5, 3: -2, -1: 9, 10: 1, 42: 6},
    'rec': {'a': 3, 'b': -4, 'c': 0, 'd': 11},
    'strs': ['12', 'x', '-4', '', '99z', '7', '0', '-'],
}


def gen_with_lookup(rng, gen, depth, fallback):
    for _ in range(6):
        t = gen(rng, depth)
        if has_lookup(t):
            return t
    return fallback


def gen_int(rng, depth):
    """An int-valued tree, which may miss or fault; the caller keeps only
    the ones that evaluate."""
    r = rng.random()
    if depth <= 0 or r < 0.12:
        return ('int', rng.randint(-3, 12))
    if r < 0.30:
        return ('ix', V('xs'), gen_int(rng, depth - 1))
    if r < 0.42:
        return ('ix', V('mi'), gen_int(rng, depth - 1))
    if r < 0.50:
        return ('fld', V('rec'), rng.choice(['a', 'b', 'c', 'd', 'e', 'f']))
    if r < 0.56:
        return ('ix', V('rec'), ('str', rng.choice(['a', 'b', 'zz'])))
    if r < 0.66:
        return ('toint', gen_str(rng, depth - 1))
    if r < 0.86:
        return ('else', gen_with_lookup(rng, gen_int, depth - 1, ('ix', V('xs'), ('int', rng.randint(-2, 10)))),
                gen_int(rng, depth - 1))
    if r < 0.95:
        return ('bin', rng.choice(['+', '-', '*', '/', '%']), gen_int(rng, depth - 1), gen_int(rng, depth - 1))
    return ('neg', gen_int(rng, depth - 1))


def gen_str(rng, depth):
    r = rng.random()
    if depth <= 0 or r < 0.25:
        return ('str', rng.choice(['5', 'x', '-3', '08', '', '1 ']))
    if r < 0.60:
        return ('ix', V('strs'), gen_int(rng, depth - 1))
    if r < 0.85:
        return ('interp', [gen_int(rng, depth - 1)])
    if r < 0.95:
        return ('interp', [gen_int(rng, depth - 1), rng.choice(['x', '0', '.'])])
    return ('else', gen_with_lookup(rng, gen_str, depth - 1, ('ix', V('strs'), ('int', rng.randint(-2, 9)))),
            gen_str(rng, depth - 1))


def random_prog(seed, count):
    rng = random.Random(seed)
    p = Prog()
    for name, v in RANDOM_ENV.items():
        p.let(name, v)
    kept = hits = 0
    while kept < count:
        node = gen_int(rng, rng.choice([2, 3, 4, 5]))
        if rng.random() < 0.2:
            node = ('bin', '<', node, gen_int(rng, 2))
        if not has_lookup(node):
            continue
        try:
            log = []
            v = ev(node, p.env, log)
        except (Miss, Fault):
            continue
        if is_int(v) and abs(v) > 10**9:
            continue
        both = rng.random() < 0.3
        for full in ((False, True) if both else (False,)):
            p.line(f'print({render(node, 0, full)})')
            p.say(v)
        kept += 1
    return p


TESTS = {
    'lookups': (700, lookups), 'chains': (701, chains), 'precedence': (702, precedence),
    'lexical': (703, lexical), 'word-count': (704, word_count), 'routes': (705, routes),
    'config': (706, config), 'statements': (707, statements),
    'random-a': (708, lambda: random_prog(7001, 70)), 'random-b': (709, lambda: random_prog(7002, 70)),
}


def main(argv):
    mode = 'expected'
    if argv and argv[0] in ('--program', '--stdin'):
        mode = argv[0][2:]
        argv = argv[1:]
    stdin_texts = {'word-count': WORD_TEXT, 'config': CONFIG_TEXT}
    if len(argv) != 1 or argv[0] not in TESTS or (mode == 'stdin' and argv[0] not in stdin_texts):
        sys.exit('usage: fallback.py [--program] ' + '|'.join(TESTS) + '\n       fallback.py --stdin word-count|config')
    if mode == 'stdin':
        sys.stdout.write(stdin_texts[argv[0]])
        return
    p = TESTS[argv[0]][1]()
    sys.stdout.write(p.program() if mode == 'program' else p.output())


if __name__ == '__main__':
    main(sys.argv[1:])
