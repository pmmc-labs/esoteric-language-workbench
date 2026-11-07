#!/usr/bin/env python3
"""Model for step 5 (lists and the core rule): tests 500 to 511.

Each test is a Ditto program and the output LANGUAGE.md defines for it,
worked out here by Python, never by running the compiler. The model is
D7's definition: every variable owns its value, so every assignment,
argument and store takes `copy.deepcopy` of what it is given, and an
update changes the variable's own copy in place. The compiler does the
opposite (shares, never writes, rebuilds the spine), so agreement is a
real check of the core rule and not the same code twice.

Python's own comparisons are not used on Ditto values: `True == 1` and
`[True] == [1]` in Python, and Ditto's `true` is not `1`. `eq`, `cmp`,
`show` and `lit` are written from LANGUAGE.md: structural equality by
type; `<` on ints, strings (byte by byte, a prefix first) and lists
(element by element with the same rules, a prefix first); the printed
form with strings bare at the top and quoted inside a list (D24). Ints
are Python ints; the programs here never overflow (faults are the
hand-written tests), and strings are ASCII so a Python `str` is a byte
string. Where a library does the work it is for the same definition:
`sorted` (stable, with `cmp` as the order), `str.split(sep)` for
`split` (pieces between non-overlapping occurrences, left to right),
`re.split` on the four whitespace bytes for `words`.

Tests 500 to 509 are fixed programs: literals and printing; indexing,
`+` and `len`; `==` and the orderings over a pool of lists; `in`; `for`
over lists; `sort`; the quicksort and insertion sort of DESIGN.md on
generated data; `split`, `join`, `words` and `slice`; path assignment
and compound assignment on paths; and the core rule's cases (`let b =
a`, an argument changed in a function, a list stored in a list, a loop
over a list it changes, a list built with `+=`). Tests 510 and 511 are
random programs: a generator writes lets, copies, slices, path updates,
appends, calls of functions that change their parameter, and loops that
change what they iterate, choosing only operations that are valid in the
state the Python side has reached, and the Python side runs them on
deep copies. Seeds are fixed, so reruns are identical.

    python3 t/models/lists.py --program literals > t/500-literals.ditto
    python3 t/models/lists.py literals > t/500-literals.expected
    python3 t/models/lists.py --program index-concat > t/501-index-concat.ditto
    python3 t/models/lists.py index-concat > t/501-index-concat.expected
    python3 t/models/lists.py --program compare > t/502-compare.ditto
    python3 t/models/lists.py compare > t/502-compare.expected
    python3 t/models/lists.py --program membership > t/503-membership.ditto
    python3 t/models/lists.py membership > t/503-membership.expected
    python3 t/models/lists.py --program for-list > t/504-for-list.ditto
    python3 t/models/lists.py for-list > t/504-for-list.expected
    python3 t/models/lists.py --program sort > t/505-sort.ditto
    python3 t/models/lists.py sort > t/505-sort.expected
    python3 t/models/lists.py --program sort-programs > t/506-sort-programs.ditto
    python3 t/models/lists.py sort-programs > t/506-sort-programs.expected
    python3 t/models/lists.py --program list-builtins > t/507-list-builtins.ditto
    python3 t/models/lists.py list-builtins > t/507-list-builtins.expected
    python3 t/models/lists.py --program path-updates > t/508-path-updates.ditto
    python3 t/models/lists.py path-updates > t/508-path-updates.expected
    python3 t/models/lists.py --program core-rule > t/509-core-rule.ditto
    python3 t/models/lists.py core-rule > t/509-core-rule.expected
    python3 t/models/lists.py --program random-a > t/510-random-a.ditto
    python3 t/models/lists.py random-a > t/510-random-a.expected
    python3 t/models/lists.py --program random-b > t/511-random-b.ditto
    python3 t/models/lists.py random-b > t/511-random-b.expected
"""
import copy
import functools
import random
import re
import sys

MAX = 2**63 - 1
MIN = -(2**63)


class Fault(Exception):
    """An operation the definition makes a fault: a model program must not
    do one, so this ends the model."""


def checked(n):
    assert MIN <= n <= MAX, 'a model program must not overflow'
    return n


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


# --- The definition: equality, order, printed form, source form -------------

def eq(a, b):
    """`==`: structural, by type; true is not 1."""
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    if isinstance(a, list) or isinstance(b, list):
        return False
    if a is None or b is None:
        return a is None and b is None
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if is_int(a) and is_int(b):
        return a == b
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    return False


def cmp(a, b):
    """-1, 0 or 1 by `<`: ints, strings, and lists of them, else a fault."""
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


def comparable(a, b):
    try:
        cmp(a, b)
        return True
    except Fault:
        return False


def cat(a, b):
    """a + b as a new list. Each side is copied on its own: copy.deepcopy of
    one structure holding the same object twice would keep them shared (it
    memoizes), and a Python value that shares is not D7's value."""
    return copy.deepcopy(a) + copy.deepcopy(b)


def contains(xs, x):
    return any(eq(x, y) for y in xs)


def sort_list(xs):
    return sorted(xs, key=functools.cmp_to_key(cmp))


ESC = {'\\': '\\\\', '"': '\\"', '\n': '\\n', '\t': '\\t', '\r': '\\r'}


def show(v, quoted=False):
    """The printed form (what `str` gives); strings are quoted inside a list."""
    if v is True: return 'true'
    if v is False: return 'false'
    if v is None: return 'nil'
    if isinstance(v, str):
        assert v.isascii()
        return '"' + ''.join(ESC.get(c, c) for c in v) + '"' if quoted else v
    if isinstance(v, list):
        return '[' + ', '.join(show(x, True) for x in v) + ']'
    return str(v)


def lit(v):
    """Ditto source for the value v. There is no negative literal, and the
    smallest int is written as a subtraction (LANGUAGE.md, Lexical)."""
    if v is True: return 'true'
    if v is False: return 'false'
    if v is None: return 'nil'
    if isinstance(v, str):
        out = ''
        for c in v:
            out += ESC.get(c, '\\{' if c == '{' else c)
        return '"' + out + '"'
    if isinstance(v, list):
        return '[' + ', '.join(lit(x) for x in v) + ']'
    if v == MIN: return '(-9223372036854775807 - 1)'
    return f'-{-v}' if v < 0 else str(v)


def trunc_div(x, y):
    q = abs(x) // abs(y)
    return q if (x < 0) == (y < 0) else -q


def apply(op, cur, v):
    """The compound assignment `cur op= v` on ints, or `+=` on lists."""
    if isinstance(cur, list):
        assert op == '+=' and isinstance(v, list)
        return cur + copy.deepcopy(v)
    if isinstance(cur, str):
        assert op == '+='
        return cur + v
    if op == '+=': return checked(cur + v)
    if op == '-=': return checked(cur - v)
    if op == '*=': return checked(cur * v)
    q = trunc_div(cur, v)
    return q if op == '/=' else cur - q * v


# --- A program and the Python state that runs beside it ----------------------

def ix(i):
    """A path step: an int, or (source, value) for an index expression."""
    return i if isinstance(i, tuple) else (str(i), i)


class Prog:
    def __init__(self):
        self.src = []
        self.out = []
        self.vars = {}

    def line(self, *s):
        self.src.extend(s)

    def say(self, *vals):
        """The expected output of a print of these values."""
        self.out.append(' '.join(show(v) for v in vals))

    def pr(self, srcs, vals):
        self.line('print(' + ', '.join(srcs) + ')')
        self.say(*vals)

    def prlit(self, *vals):
        """print of literals: the printed form of each value."""
        self.pr([lit(v) for v in vals], vals)

    def show(self, *names):
        self.pr(list(names), [self.vars[n] for n in names])

    def program(self):
        return '\n'.join(self.src) + '\n'

    def check(self):
        """No list is reachable twice: every variable owns its whole value."""
        seen = set()

        def walk(v):
            if isinstance(v, list):
                assert id(v) not in seen, 'the model aliased a list'
                seen.add(id(v))
                for x in v:
                    walk(x)
        for v in self.vars.values():
            walk(v)

    def output(self):
        self.check()
        return ''.join(l + '\n' for l in self.out)

    # Each of these emits the statement and runs it on the Python side, where
    # a store is a deep copy (D7's definition).
    def let(self, name, v):
        self.line(f'let {name} = {lit(v)}')
        self.vars[name] = copy.deepcopy(v)
        self.check()

    def let_expr(self, name, src, v):
        self.line(f'let {name} = {src}')
        self.vars[name] = copy.deepcopy(v)
        self.check()

    def let_from(self, name, other):
        self.let_expr(name, other, self.vars[other])

    def assign(self, name, src, v):
        self.line(f'{name} = {src}')
        self.vars[name] = copy.deepcopy(v)
        self.check()

    def set(self, name, path, v, op='=', src=None):
        path = [ix(p) for p in path]
        self.line(f'{name}{"".join("[" + s + "]" for s, _ in path)} {op} {src or lit(v)}')
        box = self.vars[name]
        for _, i in path[:-1]:
            box = box[i]
        i = path[-1][1]
        assert 0 <= i < len(box), 'a model program must not fault'
        box[i] = copy.deepcopy(v) if op == '=' else apply(op, box[i], v)
        self.check()


# --- 500: literals and printing ---------------------------------------------

def literals():
    p = Prog()
    values = [
        [], [1], [1, 2, 3], [-1, 0, 1], [MAX, MIN], ['a'], ['a', 'b'], [''],
        ['a"b', 'c\\d', 'e\nf', 'g\th', 'i\rj', 'k{l}m'], [True, False, None],
        [[]], [[1], [2, [3]]], [[], [[]]], [1, 'two', [3, [4, 'five']], None, True],
        [[[[[1]]]]], ['a, b', ']', '[1]', ' ', '\'', '"'], [0, 7],
        [[1, 2], [3, 4], [5, 6]], ['x'] * 5, [None, None], [[None], [True], [False]],
        list(range(-3, 12)),
    ]
    for v in values:
        p.prlit(v)
    # Several arguments: strings are bare at the top level and quoted in a list.
    p.pr(['[1]', '"a"', '["a"]', '2'], [[1], 'a', ['a'], 2])
    p.pr(['[]', '[[]]', 'nil', '[nil]'], [[], [[]], None, [None]])
    # str, interpolation, len.
    p.line('let xs = ["a", [1, "b"], nil]')
    xs = ['a', [1, 'b'], None]
    p.pr(['str(xs)'], [show(xs)])
    p.pr(['str(xs) + "!"'], [show(xs) + '!'])
    p.pr(['len(str(xs))'], [len(show(xs))])
    p.line('print("xs = {xs}, first = {xs[0]}, second = {xs[1]}, last = {xs[2]}")')
    p.say(f'xs = {show(xs)}, first = a, second = {show(xs[1])}, last = nil')
    p.line('print("{[1, 2]}{[]}{["z"]}")')
    p.say('[1, 2][]["z"]')
    p.pr(['len(xs)', 'len([])', 'len([[], []])', 'len([1, [2, 3]])'], [3, 0, 2, 2])
    p.pr(['[1, 2] == [1, 2]', '[1, 2] != [2, 1]'], [True, True])
    return p


# --- 501: indexing, +, len ----------------------------------------------------

def index_concat():
    p = Prog()
    p.let('xs', [10, 20, 30, 40])
    xs = p.vars['xs']
    p.pr(['xs[0]', 'xs[3]', 'xs[1 + 1]', 'xs[len(xs) - 1]', 'xs[xs[0] / 10]'], [xs[0], xs[3], xs[2], xs[3], xs[1]])
    p.pr(['-xs[0]', 'xs[0] + 1', 'xs[1] * 2 - xs[0]', '-xs[0] * 2'], [-10, 11, 30, -20])
    p.let('g', [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    g = p.vars['g']
    p.pr(['g[1]', 'g[1][2]', 'g[2][0] + g[0][2]', 'g[g[0][0]][g[0][1]]'], [g[1], g[1][2], g[2][0] + g[0][2], g[1][2]])
    p.line('for i in 0..3 {', '  print(g[i][0], g[i][1], g[i][2], g[0][i], g[1][i], g[2][i])', '}')
    for i in range(3):
        p.say(g[i][0], g[i][1], g[i][2], g[0][i], g[1][i], g[2][i])
    p.let('s', ['ab', 'cd'])
    p.pr(['s[0][1]', 's[1][0] + s[0][0]', 'len(s[1])', 's[1]'], ['b', 'ca', 2, 'cd'])
    p.pr(['[10, 20, 30][1]', '[[1, 2], [3]][0][1]', '[[1, 2], [3]][1][0]', '["x", "y"][1]', '(xs + [50])[4]'], [20, 2, 3, 'y', 50])
    # A call's result can be indexed, and an index can be a call.
    p.line('fn pick(ys, i) {', '  return ys[i]', '}', 'fn pair(a, b) {', '  return [a, b]', '}')
    p.pr(['pick(xs, 2)', 'pair(1, 2)[1]', 'pair("a", [3])[1]', 'xs[pick([0, 3], 1)]'], [30, 2, [3], 40])
    # +
    cases = [([], []), ([], [1]), ([1], []), ([1, 2], [3]), ([[1]], [[2]]), (['a'], ['b', 'c']), ([None], [True, 1]),
             ([[]], [[], []]), ([1, [2]], [[3], 4])]
    for a, b in cases:
        p.pr([lit(a) + ' + ' + lit(b)], [a + b])
    p.pr(['[1] + [2] + [3] + [4]', '([1] + [2]) + ([3] + [4])', '[[1]] + [[2]] + [[3]]'], [[1, 2, 3, 4], [1, 2, 3, 4], [[1], [2], [3]]])
    p.pr(['len(xs + xs)', 'len([] + [])', 'len(g + g)', 'xs + xs'], [8, 0, 6, xs + xs])
    p.pr(['xs', 'g'], [xs, g])  # + changed neither
    # Building with += and +.
    p.line('let r = []', 'for i in 0..10 {', '  r += [i * i]', '}', 'print(r, len(r))')
    r = [i * i for i in range(10)]
    p.say(r, len(r))
    p.line('r += r', 'print(r)')
    r = r + r
    p.say(r)
    p.line('let evens = []', 'let odds = []', 'for i in 0..11 {',
           '  if i % 2 == 0 { evens += [i] } else { odds += [i] }', '}',
           'print(evens, odds, evens + odds)')
    ev = [i for i in range(11) if i % 2 == 0]
    od = [i for i in range(11) if i % 2 != 0]
    p.say(ev, od, ev + od)
    p.line('let nest = []', 'for i in 0..4 {', '  let row = []', '  for j in 0..i {', '    row += [j]', '  }',
           '  nest += [row]', '}', 'print(nest)')
    p.say([[j for j in range(i)] for i in range(4)])
    return p


# --- 502: == and the orderings -------------------------------------------------

def compare():
    p = Prog()
    ints = [[], [1], [1, 2], [1, 3], [2], [1, 2, 3], [-1], [MAX], [MIN], [0, 0], [1, 1, 1], [-5, 5]]
    strs = [[''], ['a'], ['a', 'b'], ['ab'], ['b'], ['A'], ['a', ''], ['a', 'a'], ['abc', 'b']]
    nested = [[[]], [[1]], [[1], [2]], [[1, 2]], [[1], []], [[2]], [[1, 1]], [[], []], [[[1]]], [[1], 2]]
    mixed = [[None], [True], [False], [1, 'a'], ['1'], [1, '1'], [[1], 'a'], [None, None], [True, 1]]
    def both(a, b):
        srcs = [f'{lit(a)} == {lit(b)}', f'{lit(a)} != {lit(b)}']
        vals = [eq(a, b), not eq(a, b)]
        if comparable(a, b):
            c = cmp(a, b)
            for op, r in (('<', c < 0), ('<=', c <= 0), ('>', c > 0), ('>=', c >= 0)):
                srcs.append(f'{lit(a)} {op} {lit(b)}')
                vals.append(r)
        p.pr(srcs, vals)

    for pool in (ints, strs, nested):
        for a in pool:
            for b in pool:
                both(a, b)
    # == on anything: mixed types, true is not 1, nil only equals nil.
    for a in ints[:4] + strs[:3] + nested[:3] + mixed:
        for b in mixed:
            p.pr([f'{lit(a)} == {lit(b)}', f'{lit(a)} != {lit(b)}'], [eq(a, b), not eq(a, b)])
    # A list is never equal to a non-list.
    for other in (1, 'a', True, None):
        p.pr([f'[] == {lit(other)}', f'{lit(other)} == []', f'[{lit(other)}] == {lit(other)}'],
             [False, False, False])
    # Variables, and a copy that is equal until it is changed.
    p.let('a', [[1, 2], [3]])
    p.let_from('b', 'a')
    p.pr(['a == b', 'a < b', 'a <= b'], [True, False, True])
    p.set('b', [0, 1], 9)
    p.pr(['a == b', 'a < b', 'a > b'], [False, True, False])
    p.set('b', [0, 1], 2)
    p.set('b', [1], [3, 0])
    p.pr(['a == b', 'a < b', 'a > b'], [False, True, False])
    return p


# --- 503: in -------------------------------------------------------------------

def membership():
    p = Prog()
    xs = [1, 2, '1', 'a', '', None, True, False, [], [1], [1, 2], [[1]], ['a'], [None], [True], [1, 'a']]
    cs = [[], [1], [1, 2, 3], ['a', 'b'], [[1], [2]], [None], [True], [1, '1'], [[]], [[], 1], [False, 0],
          [[1, 2], ['a']], [[[1]]]]
    for c in cs:
        for x in xs:
            p.pr([f'{lit(x)} in {lit(c)}', f'{lit(x)} not in {lit(c)}'], [contains(c, x), not contains(c, x)])
    p.let('items', [[1, 2], [3, 4], [5]])
    items = p.vars['items']
    p.pr(['[3, 4] in items', '3 in items', '[5] in items', '[] in items', '3 in items[1]', '5 not in items[1]'],
         [True, False, True, False, True, True])
    p.line('let hits = 0', 'for i in 0..6 {', '  if i in items[1] or [i] in items { hits += 1 }', '}', 'print(hits)')
    hits = sum(1 for i in range(6) if contains(items[1], i) or contains(items, [i]))
    p.say(hits)
    p.line('let uniq = []', 'for x in [3, 1, 3, 2, 1, 2, 5, 3] {', '  if x not in uniq { uniq += [x] }', '}', 'print(uniq)')
    uniq = []
    for x in [3, 1, 3, 2, 1, 2, 5, 3]:
        if not contains(uniq, x): uniq.append(x)
    p.say(uniq)
    return p


# --- 504: for over a list ----------------------------------------------------------

def for_list():
    p = Prog()
    p.line('let xs = [3, 1, 4, 1, 5, 9, 2, 6]', 'let total = 0', 'for x in xs { total += x }', 'print(total)')
    xs = [3, 1, 4, 1, 5, 9, 2, 6]
    p.say(sum(xs))
    p.line('let seen = []', 'for x in xs {', '  if x not in seen { seen += [x] }', '}', 'print(seen, len(seen))')
    seen = []
    for x in xs:
        if x not in seen: seen.append(x)
    p.say(seen, len(seen))
    # The loop walks the list as it was when it started.
    p.line('for x in xs {', '  xs += [x * 10]', '}', 'print(xs, len(xs))')
    for x in list(xs):
        xs = xs + [x * 10]
    p.say(xs, len(xs))
    p.line('let n = 0', 'for x in xs {', '  xs = [n]', '  n += 1', '}', 'print(xs, n)')
    n = 0
    for x in list(xs):
        xs = [n]
        n += 1
    p.say(xs, n)
    p.line('let ys = [1, 2, 3]', 'for y in ys {', '  y = y * 100', '  print(y)', '}', 'print(ys)')
    ys = [1, 2, 3]
    for y in ys:
        p.say(y * 100)
    p.say(ys)
    p.line('for i in 0..len(ys) {', '  ys[i] = ys[i] * 2', '}', 'print(ys)')
    ys = [y * 2 for y in ys]
    p.say(ys)
    p.line('for y in ys {', '  ys[0] += 1', '  print(y, ys)', '}')
    for y in list(ys):
        ys[0] += 1
        p.say(y, ys)
    # Nested lists.
    p.line('let g = [[1, 2], [3, 4], [5, 6]]', 'let sums = []', 'for row in g {', '  let s = 0',
           '  for v in row { s += v }', '  sums += [s]', '}', 'print(sums)')
    g = [[1, 2], [3, 4], [5, 6]]
    p.say([sum(r) for r in g])
    p.line('for row in g {', '  row += [0]', '  row[0] = 99', '}', 'print(g)')
    p.say(g)
    p.line('let flat = []', 'for row in g {', '  for v in row { flat += [v] }', '}', 'print(flat)')
    p.say([v for r in g for v in r])
    # Literals, calls, empty lists, lists of strings.
    p.line('for w in ["a", "b", "c"] { print(w) }')
    for w in 'abc': p.say(w)
    p.line('fn evens(n) {', '  let out = []', '  for i in 0..n {', '    if i % 2 == 0 { out += [i] }', '  }',
           '  return out', '}', 'for e in evens(10) { print(e) }')
    for e in range(0, 10, 2): p.say(e)
    p.line('for x in [] { print("never") }', 'for x in [[]] { print("once", x) }')
    p.say('once', [])
    p.line('let zs = [1, 2, 3]', 'for z in zs {', '  zs = []', '  print(z)', '}', 'print(zs)')
    p.say(1); p.say(2); p.say(3); p.say([])
    # break and continue.
    p.line('let tail = []', 'for v in [4, 8, 15, 16, 23, 42] {', '  if v % 2 == 1 { continue }',
           '  if v > 20 { break }', '  tail += [v]', '}', 'print(tail)')
    p.say([4, 8, 16])
    # The loop variable is fresh each pass and the name is free afterwards.
    p.line('for q in [1, 2] { }', 'let q = []', 'print(q)')
    p.say([])
    # Strings inside lists are walked as strings.
    p.line('for s in ["ab", "c"] {', '  for c in s { print(c, s) }', '}')
    for s in ['ab', 'c']:
        for c in s: p.say(c, s)
    return p


# --- 505: sort ------------------------------------------------------------------

def sort():
    p = Prog()

    def srt(v, name=None):
        s = sort_list(v)
        p.pr([f'sort({lit(v)})'], [s])

    srt([])
    srt([1])
    srt([2, 1])
    srt([1, 2])
    srt([5, 3, 8, 1, 9, 2, 8])
    srt([0, -1, 1, MAX, MIN, -7, 7])
    srt([3, 3, 3])
    srt(list(range(10, 0, -1)))
    srt(['pear', 'apple', 'fig', '', 'Apple', 'app', 'apple pie', 'b', 'a'])
    srt([['b', 2], ['a', 9], ['a', 1], ['c', 0]])
    srt([[3, 'c'], [1, 'z'], [3, 'a'], [2, 'm'], [1, 'a']])
    srt([[2], [1, 2], [], [1], [1, 1], [1, 0]])
    srt([[[2]], [[1], [5]], [[1]], [[]], []])
    srt([['x', 'y'], ['x'], ['w', 'z', 'q'], ['x', '']])
    rng = random.Random(505)
    big = [rng.randint(-1000, 1000) for _ in range(150)]
    srt(big)
    # sort returns a new list; the original is as it was.
    p.let('data', [31, 4, 15, 9, 26, 5, 35, 8, 97, 93, 2, 38, 46, 26, 43])
    data = p.vars['data']
    p.pr(['sort(data)', 'data'], [sort_list(data), data])
    p.let_expr('sorted_data', 'sort(data)', sort_list(data))
    p.pr(['sorted_data == data', 'sort(sorted_data) == sorted_data', 'len(sorted_data) == len(data)'], [False, True, True])
    p.set('sorted_data', [0], 1000)
    p.pr(['data[0]', 'sorted_data[0]'], [31, 1000])
    # sort of sort, and of a list built in a loop.
    p.line('let squares = []', 'for i in 0..12 {', '  squares += [(i * 7 % 12 - 5) * (i * 7 % 12 - 5)]', '}',
           'print(squares)', 'print(sort(squares))')
    sq = [((i * 7 % 12) - 5) ** 2 for i in range(12)]
    p.say(sq)
    p.say(sort_list(sq))
    # Words and their lengths as sortable pairs.
    p.line('let pairs = []', 'for w in words("the quick brown fox jumps over the lazy dog") {',
           '  pairs += [[len(w), w]]', '}', 'print(sort(pairs))')
    ws = 'the quick brown fox jumps over the lazy dog'.split()
    p.say(sort_list([[len(w), w] for w in ws]))
    # Sorting a list of lists leaves the inner lists as they were.
    p.let('rows', [[3, 1], [1, 2], [2, 0]])
    rows = p.vars['rows']
    p.let_expr('ordered', 'sort(rows)', sort_list(rows))
    p.set('ordered', [0, 1], 99)
    p.pr(['rows', 'ordered'], [rows, p.vars['ordered']])
    return p


# --- 506: quicksort and insertion sort (DESIGN.md example 3) ----------------------

SORT_FNS = '''fn quicksort(xs) {
  if len(xs) < 2 { return xs }
  let pivot = xs[0]
  let smaller = []
  let larger = []
  for i in 1..len(xs) {
    if xs[i] < pivot { smaller += [xs[i]] } else { larger += [xs[i]] }
  }
  return quicksort(smaller) + [pivot] + quicksort(larger)
}

fn insertion_sort(xs) {
  for i in 1..len(xs) {
    let j = i
    while j > 0 and xs[j - 1] > xs[j] {
      let t = xs[j]; xs[j] = xs[j - 1]; xs[j - 1] = t
      j -= 1
    }
  }
  return xs
}
'''


def sort_programs():
    p = Prog()
    p.line(SORT_FNS)
    rng = random.Random(506)
    datasets = [
        [31, 4, 15, 9, 26, 5, 35, 8, 97, 93, 2, 38, 46, 26, 43],
        [],
        [7],
        list(range(20, 0, -1)),
        [4] * 10,
        [rng.randint(-50, 50) for _ in range(30)],
        [rng.randint(0, 5) for _ in range(25)],
        ['pear', 'apple', 'fig', 'apple', 'kiwi', 'banana'],
        [[2, 'b'], [1, 'z'], [2, 'a'], [1, 'a']],
    ]
    for k, d in enumerate(datasets):
        name = f'data{k}'
        p.let(name, d)
        s = sort_list(d)
        p.pr([f'quicksort({name})', f'insertion_sort({name})', name],
             [s, s, d])
        p.pr([f'sort({name}) == quicksort({name})', f'insertion_sort({name}) == sort({name})', f'len({name})'],
             [True, True, len(d)])
    return p


# --- 507: split, join, words, slice -----------------------------------------------

def list_builtins():
    p = Prog()
    splits = [('a,b,c', ','), ('a,,b', ','), ('', ','), (',', ','), (',a,', ','), ('abc', ','), ('abc', 'abc'),
              ('aaa', 'aa'), ('a--b--c', '--'), ('a b  c', ' '), ('line1\nline2\n', '\n'), ('a\tb', '\t'),
              ('x', 'x'), ('xx', 'x'), ('abab', 'ab'), ('ab', 'abc'), ('a, b, c', ', '), ('one', ' '),
              ('{}', '{'), ('a"b"c', '"'), ('aXbxc', 'x'), ('...', '.')]
    for s, sep in splits:
        parts = s.split(sep)
        p.pr([f'split({lit(s)}, {lit(sep)})', f'len(split({lit(s)}, {lit(sep)}))'], [parts, len(parts)])
    joins = [([], ','), (['a'], ','), (['a', 'b', 'c'], ','), (['a', '', 'b'], ', '), (['', ''], '-'), (['ab', 'cd'], ''),
             ([''], 'x'), (['x', 'y'], '\n'), (['1', '2'], ' + ')]
    for xs, sep in joins:
        p.pr([f'join({lit(xs)}, {lit(sep)})'], [sep.join(xs)])
    texts = ['', ' ', 'a', '  hello   world  ', 'a\tb\nc\rd e', '\n\n', 'one,two three', 'x  \t \n y', ' lead', 'trail ',
             'tabs\t\tand\r\nlines']
    for t in texts:
        ws = [w for w in re.split(r'[ \t\n\r]+', t) if w != '']
        p.pr([f'words({lit(t)})', f'len(words({lit(t)}))'], [ws, len(ws)])
    # Round trips.
    p.line('let csv = "name,qty,price"', 'let cells = split(csv, ",")', 'print(cells, join(cells, ",") == csv)')
    cells = 'name,qty,price'.split(',')
    p.say(cells, True)
    p.line('print(join(words("  the   quick brown  "), " "))')
    p.say('the quick brown')
    p.line('let lines = split("1 2\\n3 4 5\\n\\n6", "\\n")', 'for line in lines {', '  print(len(words(line)), words(line))', '}')
    for line in '1 2\n3 4 5\n\n6'.split('\n'):
        w = line.split()
        p.say(len(w), w)
    p.line('let total = 0', 'for w in words("10 20 30 -5") { total += int(w) }', 'print(total)')
    p.say(55)
    # slice on lists.
    p.let('xs', [10, 20, 30, 40, 50])
    xs = p.vars['xs']
    for a, b in [(0, 5), (0, 0), (5, 5), (1, 3), (2, 3), (0, 1), (4, 5), (3, 3)]:
        p.pr([f'slice(xs, {a}, {b})', f'len(slice(xs, {a}, {b}))'], [xs[a:b], len(xs[a:b])])
    p.pr(['slice([], 0, 0)', 'slice([[1], [2, 3], []], 1, 3)', 'slice(["a", "b"], 1, 2)', 'slice(xs, 1, 4) + slice(xs, 0, 1)'],
         [[], [[2, 3], []], ['b'], [20, 30, 40, 10]])
    p.pr(['slice(xs, 0, len(xs)) == xs', 'slice(slice(xs, 1, 5), 1, 3)'], [True, [30, 40]])
    p.let_expr('part', 'slice(xs, 1, 3)', xs[1:3])
    p.set('part', [0], 0)
    p.pr(['xs', 'part'], [xs, p.vars['part']])
    p.line('let g = [[1, 2], [3, 4]]', 'let top = slice(g, 0, 1)', 'top[0][0] = 9', 'print(g, top)')
    p.say([[1, 2], [3, 4]], [[9, 2]])
    # Chunks of a list, and a window.
    p.line('let chunks = []', 'let at = 0', 'while at < len(xs) {', '  let end = at + 2',
           '  if end > len(xs) { end = len(xs) }', '  chunks += [slice(xs, at, end)]', '  at = end', '}', 'print(chunks)')
    p.say([xs[i:i + 2] for i in range(0, len(xs), 2)])
    return p


# --- 508: path assignment -------------------------------------------------------

def path_updates():
    p = Prog()
    p.let('g', [[0] * 4 for _ in range(4)])
    for i in range(4):
        p.set('g', [i, i], 1)
    p.show('g')
    p.set('g', [0, 3], 7)
    p.set('g', [3, 0], 5, '+=')
    p.set('g', [3, 0], 5, '*=')
    p.set('g', [3, 0], 3, '-=')
    p.set('g', [3, 0], 4, '/=')
    p.set('g', [3, 0], 3, '%=')
    p.show('g')
    p.line('for i in 0..4 {', '  for j in 0..4 {', '    g[i][j] += i * j', '  }', '}')
    for i in range(4):
        for j in range(4):
            p.vars['g'][i][j] += i * j
    p.show('g')
    p.set('g', [1], [9], '+=')
    p.set('g', [("len(g) - 1", 3), ("len(g) - 1", 3)], 42)
    p.set('g', [("1 + 1", 2), ("g[0][3] - 6", 1)], -1, '+=')
    p.show('g')
    p.pr(['len(g[1])', 'len(g[0])', 'g[1][4]'], [5, 4, 9])
    # Swap rows through a temporary: values, not references.
    p.let_expr('tmp', 'g[0]', p.vars['g'][0])
    g = p.vars['g']
    p.line('g[0] = g[1]')
    g[0] = copy.deepcopy(g[1])
    p.line('g[1] = tmp')
    g[1] = copy.deepcopy(p.vars['tmp'])
    p.set('g', [0, 0], 100)
    p.show('g', 'tmp')
    # Three deep and four deep.
    p.let('cube', [[[0, 0], [0, 0]], [[0, 0], [0, 0]]])
    for a in range(2):
        for b in range(2):
            for c in range(2):
                p.set('cube', [a, b, c], a * 4 + b * 2 + c)
    p.show('cube')
    p.set('cube', [1, 0], [8, 9, 10])
    p.set('cube', [1, 0, 2], 5, '*=')
    p.set('cube', [0], [[]], '+=')
    p.show('cube')
    p.let('deep', [[[[1]]]])
    p.set('deep', [0, 0, 0, 0], 2, '+=')
    p.set('deep', [0, 0, 0], [3], '+=')
    p.show('deep')
    # Strings in lists, and appending to an inner list.
    p.let('names', ['ann', 'bob', 'cy'])
    p.set('names', [1], '!', '+=')
    p.set('names', [2], 'rus', '+=')
    p.set('names', [0], 'Ann')
    p.show('names')
    p.let('groups', [[], [], []])
    for k in range(10):
        p.line(f'groups[{k} % 3] += [{k}]')
        p.vars['groups'][k % 3].append(k)
    p.show('groups')
    # Transpose built with += on paths.
    p.line('let m = [[1, 2, 3], [4, 5, 6]]', 'let tr = []',
           'for j in 0..3 {', '  tr += [[]]', '  for i in 0..2 {', '    tr[j] += [m[i][j]]', '  }', '}', 'print(tr, m)')
    m = [[1, 2, 3], [4, 5, 6]]
    p.say([[m[i][j] for i in range(2)] for j in range(3)], m)
    # Index expressions are evaluated before the right-hand side, once.
    p.line('let k = 0', 'let ws = [10, 20, 30]', 'ws[k] = k + 5', 'ws[k + 1] += k + 5', 'k = 2', 'ws[k] -= k', 'print(ws, k)')
    p.say([5, 25, 28], 2)
    # Updating an element of an element that is shared with a variable.
    p.let('row', [1, 2, 3])
    p.line('let table = [row, row]')
    p.vars['table'] = [copy.deepcopy(p.vars['row']), copy.deepcopy(p.vars['row'])]
    p.set('table', [0, 0], 99)
    p.set('row', [2], 0)
    p.show('table', 'row')
    # Booleans, nil and strings as elements; the whole element replaced by another type.
    p.let('mix', [1, 'a', True, None, [1]])
    p.set('mix', [0], 'zero')
    p.set('mix', [1], [1, 2])
    p.set('mix', [3], False)
    p.set('mix', [4, 0], None)
    p.show('mix')
    # A loop that updates what it iterates by index.
    p.line('let acc = [1, 1, 1, 1, 1, 1]', 'for i in 2..len(acc) {', '  acc[i] = acc[i - 1] + acc[i - 2]', '}', 'print(acc)')
    acc = [1] * 6
    for i in range(2, 6):
        acc[i] = acc[i - 1] + acc[i - 2]
    p.say(acc)
    return p


# --- 509: the core rule -------------------------------------------------------------

def core_rule():
    p = Prog()
    # let b = a, then change b; then change a.
    p.let('a', [1, 2, 3])
    p.let_from('b', 'a')
    p.set('b', [0], 99)
    p.show('a', 'b')
    p.set('a', [2], -3)
    p.show('a', 'b')
    p.assign('b', 'a', p.vars['a'])
    p.set('a', [1], 5, '+=')
    p.show('a', 'b')
    p.line('b += [4]')
    p.vars['b'] = cat(p.vars['b'], [4])
    p.show('a', 'b')
    p.pr(['a == b', 'a == slice(b, 0, 3)'], [eq(p.vars['a'], p.vars['b']), eq(p.vars['a'], p.vars['b'][:3])])
    # An argument changed inside a function: the caller's is untouched.
    p.line('fn bump(xs) {', '  xs[0] = 100', '  xs += [200]', '  return xs', '}',
           'fn scratch(xs) {', '  xs[0] += 1', '}')
    p.let('c', [1, 2])
    arg = copy.deepcopy(p.vars['c']); arg[0] = 100; arg = arg + [200]
    p.let_expr('d', 'bump(c)', arg)
    p.show('c', 'd')
    p.line('scratch(c)')
    p.show('c')
    p.pr(['bump(c)', 'c'], [arg, p.vars['c']])
    # A function returning its parameter gives a value; changing the result does not change the original.
    p.line('fn same(xs) {', '  return xs', '}')
    p.let_expr('e', 'same(c)', p.vars['c'])
    p.set('e', [0], -1)
    p.show('c', 'e')
    # A list stored in a list: the store takes the value at that moment.
    p.let('inner', [1, 2])
    dup = copy.deepcopy
    p.let_expr('outer', '[inner, inner, [inner]]', [dup(p.vars['inner']), dup(p.vars['inner']), [dup(p.vars['inner'])]])
    p.set('inner', [0], 50)
    p.show('inner', 'outer')
    p.set('outer', [0, 1], 60)
    p.set('outer', [2, 0, 0], 70)
    p.show('inner', 'outer')
    p.line('outer[1] = inner')
    p.vars['outer'][1] = copy.deepcopy(p.vars['inner'])
    p.set('inner', [1], 0)
    p.show('inner', 'outer')
    p.let_expr('row', 'outer[0]', p.vars['outer'][0])
    p.set('row', [0], 0)
    p.show('row', 'outer')
    p.let_expr('twice', 'outer + outer', cat(p.vars['outer'], p.vars['outer']))
    p.set('twice', [0, 0], 1)
    p.set('twice', [3, 0], 2)
    p.show('outer', 'twice')
    # A function that stores its parameter in a list, then changes the parameter.
    p.line('fn wrap(xs) {', '  let box = [xs]', '  xs[0] = 0', '  box += [xs]', '  return box', '}')
    p.let('w', [5, 6])
    wr = [[5, 6], [0, 6]]
    p.let_expr('boxed', 'wrap(w)', wr)
    p.show('w', 'boxed')
    # A loop over a list that changes it sees the list as it was.
    p.let('items', [1, 2, 3])
    p.line('let visits = []', 'for it in items {', '  items += [it * 10]', '  items[0] += 1', '  visits += [it]', '}', 'print(items, visits)')
    it = list(p.vars['items']); items = list(it); visits = []
    for x in it:
        items = items + [x * 10]
        items[0] += 1
        visits.append(x)
    p.say(items, visits)
    p.vars['items'] = items
    p.line('for it in items {', '  items = []', '}', 'print(items)')
    p.say([])
    p.let('grid', [[1, 2], [3, 4]])
    p.line('let seen_rows = []', 'for r in grid {', '  grid[1][0] = 0', '  seen_rows += [r]', '}', 'print(seen_rows, grid)')
    sr = [[1, 2], [3, 4]]
    p.say(sr, [[1, 2], [0, 4]])
    # A list built with += in a loop; the copies taken on the way stay as they were.
    p.line('let acc = []', 'let snaps = []', 'for i in 0..5 {', '  acc += [i]', '  snaps += [acc]', '}', 'print(acc)', 'print(snaps)')
    acc = []; snaps = []
    for i in range(5):
        acc = acc + [i]
        snaps = snaps + [copy.deepcopy(acc)]
    p.say(acc)
    p.say(snaps)
    p.line('snaps[2][0] = 99', 'print(snaps[2], snaps[3], acc)')
    snaps[2][0] = 99
    p.say(snaps[2], snaps[3], acc)
    # swap and rotate through functions that return what they change.
    p.line('fn swap(xs, i, j) {', '  let t = xs[i]', '  xs[i] = xs[j]', '  xs[j] = t', '  return xs', '}',
           'fn rotate(xs) {', '  return slice(xs, 1, len(xs)) + [xs[0]]', '}')
    p.let('s', ['a', 'b', 'c', 'd'])
    p.let_expr('s2', 'swap(s, 0, 3)', ['d', 'b', 'c', 'a'])
    p.let_expr('s3', 'rotate(s2)', ['b', 'c', 'a', 'd'])
    p.show('s', 's2', 's3')
    p.line('s = swap(s, 1, 2)')
    p.vars['s'] = ['a', 'c', 'b', 'd']
    p.show('s')
    # Self assignment and doubling.
    p.line('s = s', 's = s + s', 's[0] = "z"', 'print(s)')
    p.say(['z', 'c', 'b', 'd', 'a', 'c', 'b', 'd'])
    # Nested containers: a copy of a nested list is deep.
    p.let('n1', [[1, [2]], [[3]]])
    p.let_from('n2', 'n1')
    p.set('n2', [0, 1, 0], 20)
    p.set('n2', [1, 0, 0], 30)
    p.show('n1', 'n2')
    p.pr(['n1 == n2', 'n1[0][0] == n2[0][0]', 'n1[0][1] == n2[0][1]'], [False, True, False])
    # Parameters are copies of copies: a function that passes its list on.
    p.line('fn outerfn(xs) {', '  xs[0] = "outer"', '  return innerfn(xs) + xs', '}',
           'fn innerfn(xs) {', '  xs[0] = "inner"', '  xs += ["x"]', '  return xs', '}')
    p.let('base', ['b', 'c'])
    p.let_expr('res', 'outerfn(base)', ['inner', 'c', 'x', 'outer', 'c'])
    p.show('base', 'res')
    return p


# --- 510, 511: random programs -------------------------------------------------------

def touch1(xs):
    xs = copy.deepcopy(xs)
    xs[0] = 77
    xs.append(5)
    return len(xs)


def touch2(xs):
    xs = copy.deepcopy(xs)
    xs[0][0] = 99
    xs[0] = xs[0] + [1]
    xs = xs + [[2]]
    return xs


def random_prog(seed, steps):
    """Kinds: L1 is a list of ints, L2 a list of lists of ints, I an int."""
    rng = random.Random(seed)
    p = Prog()
    kinds = {}
    p.line('fn touch1(xs) {', '  xs[0] = 77', '  xs += [5]', '  return len(xs)', '}',
           'fn touch2(xs) {', '  xs[0][0] = 99', '  xs[0] += [1]', '  xs += [[2]]', '  return xs', '}',
           'fn first(xs) {', '  return xs[0]', '}')
    counter = [0]

    def fresh():
        counter[0] += 1
        return f'v{counter[0]}'

    def value(kind):
        if kind == 'I': return rng.randint(-9, 9)
        if kind == 'L1': return [rng.randint(-9, 9) for _ in range(rng.randint(1, 5))]
        return [[rng.randint(0, 3) for _ in range(rng.randint(1, 3))] for _ in range(rng.randint(1, 3))]

    def names(kind, pred=lambda v: True):
        return [n for n, k in kinds.items() if k == kind and pred(p.vars[n])]

    def pick(kind, pred=lambda v: True):
        c = names(kind, pred)
        return rng.choice(c) if c else None

    def idx(n_len, base_src):
        i = rng.randrange(n_len)
        if i == n_len - 1 and rng.random() < 0.5:
            return (f'len({base_src}) - 1', i)
        return (str(i), i)

    def declare(kind, name, src, v):
        p.let_expr(name, src, v)
        kinds[name] = kind

    def op_let():
        kind = rng.choice(['L1', 'L1', 'L2', 'I'])
        v = value(kind)
        n = fresh()
        p.let(n, v)
        kinds[n] = kind

    def op_copy():
        kind = rng.choice(['L1', 'L2'])
        a = pick(kind)
        if a is None: return
        n = fresh()
        declare(kind, n, a, p.vars[a])

    def op_slice():
        kind = rng.choice(['L1', 'L2'])
        a = pick(kind)
        if a is None: return
        v = p.vars[a]
        lo = rng.randint(0, len(v)); hi = rng.randint(lo, len(v))
        if hi == lo: return  # keep the lists non-empty
        n = fresh()
        declare(kind, n, f'slice({a}, {lo}, {hi})', v[lo:hi])

    def op_concat():
        kind = rng.choice(['L1', 'L2'])
        a, b = pick(kind), pick(kind)
        if a is None or len(p.vars[a]) + len(p.vars[b]) > 10: return
        n = fresh()
        declare(kind, n, f'{a} + {b}', cat(p.vars[a], p.vars[b]))

    def op_assign():
        kind = rng.choice(['L1', 'L2'])
        a, b = pick(kind), pick(kind)
        if a is None: return
        if rng.random() < 0.6:
            p.assign(a, b, p.vars[b])
        else:
            if len(p.vars[a]) + len(p.vars[b]) > 10: return
            p.assign(a, f'{a} + {b}', cat(p.vars[a], p.vars[b]))

    def op_set_l1():
        a = pick('L1')
        if a is None: return
        i = idx(len(p.vars[a]), a)
        p.set(a, [i], rng.randint(-9, 9))

    def op_set_l2():
        a = pick('L2', lambda v: any(len(r) > 0 for r in v))
        if a is None: return
        v = p.vars[a]
        i = rng.choice([k for k, r in enumerate(v) if len(r) > 0])
        j = rng.randrange(len(v[i]))
        p.set(a, [i, j], rng.randint(0, 9))

    def op_set_row():
        # a[i] = b[j]: the row is a value, so later changes to either stay apart
        a, b = pick('L2'), pick('L2')
        if a is None: return
        i, j = rng.randrange(len(p.vars[a])), rng.randrange(len(p.vars[b]))
        p.set(a, [i], p.vars[b][j], src=f'{b}[{j}]')

    def op_compound1():
        a = pick('L1')
        if a is None: return
        i = idx(len(p.vars[a]), a)
        cur = p.vars[a][i[1]]
        op = rng.choice(['+=', '-=', '*='])
        k = rng.randint(1, 4)
        if op == '*=' and abs(cur) > 10**6: return
        p.set(a, [i], k, op)

    def op_compound2():
        a = pick('L2')
        if a is None: return
        i = rng.randrange(len(p.vars[a]))
        if rng.random() < 0.5:
            if len(p.vars[a][i]) > 6: return
            p.set(a, [i], [rng.randint(0, 3)], '+=')
        else:
            if not p.vars[a][i]: return
            j = rng.randrange(len(p.vars[a][i]))
            p.set(a, [i, j], rng.randint(1, 4), rng.choice(['+=', '-=']))

    def op_append():
        kind = rng.choice(['L1', 'L2'])
        a = pick(kind)
        if a is None or len(p.vars[a]) >= 8: return
        v = [rng.randint(-9, 9)] if kind == 'L1' else [[rng.randint(0, 3)]]
        p.line(f'{a} += {lit(v)}')
        p.vars[a] = cat(p.vars[a], v)

    def op_int():
        a = pick('I')
        if a is None: return
        k = rng.randint(1, 5)
        op = rng.choice(['+=', '-=', '*='])
        if op == '*=' and abs(p.vars[a]) > 10**6: return
        p.line(f'{a} {op} {k}')
        p.vars[a] = apply(op, p.vars[a], k)

    def op_touch1():
        a = pick('L1')
        if a is None: return
        if rng.random() < 0.5:
            p.pr([f'touch1({a})', a], [touch1(p.vars[a]), p.vars[a]])
        else:
            n = fresh()
            declare('I', n, f'touch1({a})', touch1(p.vars[a]))

    def op_touch2():
        a = pick('L2', lambda v: len(v[0]) > 0 and len(v) < 8)
        if a is None: return
        if rng.random() < 0.5:
            p.pr([f'touch2({a})', a], [touch2(p.vars[a]), p.vars[a]])
        else:
            n = fresh()
            declare('L2', n, f'touch2({a})', touch2(p.vars[a]))

    def op_row_out():
        # let r = a[i]; change r; a does not change
        a = pick('L2')
        if a is None: return
        i = rng.randrange(len(p.vars[a]))
        n = fresh()
        declare('L1', n, f'{a}[{i}]', p.vars[a][i])
        p.set(n, [0], 55)
        p.show(a, n)

    def op_loop_grow():
        a = pick('L1', lambda v: len(v) <= 4)
        if a is None: return
        x = fresh()
        p.line(f'for {x} in {a} {{', f'  {a} += [{x}]', '}')
        p.vars[a] = cat(p.vars[a], p.vars[a])

    def op_loop_rows():
        a, b = pick('L2'), pick('L1')
        if a is None or b is None or len(p.vars[a]) + len(p.vars[b]) > 9: return
        x = fresh()
        p.line(f'for {x} in {a} {{', f'  {x} += [0]', f'  {x}[0] = 1', f'  {b} += [len({x})]', '}')
        for r in p.vars[a]:
            p.vars[b] = p.vars[b] + [len(r) + 1]

    def op_eq():
        kind = rng.choice(['L1', 'L2'])
        a, b = pick(kind), pick(kind)
        if a is None: return
        p.pr([f'{a} == {b}', f'{a} < {b}', f'len({a})'], [eq(p.vars[a], p.vars[b]), cmp(p.vars[a], p.vars[b]) < 0, len(p.vars[a])])

    def op_first():
        a = pick('L2', lambda v: len(v) > 0)
        if a is None: return
        p.pr([f'first({a})', f'{a}'], [p.vars[a][0], p.vars[a]])

    def op_show():
        if kinds:
            p.show(rng.choice(sorted(kinds)))

    ops = [op_let, op_copy, op_copy, op_slice, op_concat, op_assign, op_set_l1, op_set_l1, op_set_l2, op_set_l2,
           op_set_row, op_compound1, op_compound2, op_append, op_int, op_touch1, op_touch2, op_row_out,
           op_loop_grow, op_loop_rows, op_eq, op_first, op_show, op_show]
    for _ in range(4):
        op_let()
    for _ in range(steps):
        rng.choice(ops)()
    for n in kinds:
        p.show(n)
    return p


TESTS = {
    'literals': ('500-literals', literals),
    'index-concat': ('501-index-concat', index_concat),
    'compare': ('502-compare', compare),
    'membership': ('503-membership', membership),
    'for-list': ('504-for-list', for_list),
    'sort': ('505-sort', sort),
    'sort-programs': ('506-sort-programs', sort_programs),
    'list-builtins': ('507-list-builtins', list_builtins),
    'path-updates': ('508-path-updates', path_updates),
    'core-rule': ('509-core-rule', core_rule),
    'random-a': ('510-random-a', lambda: random_prog(510, 70)),
    'random-b': ('511-random-b', lambda: random_prog(511, 90)),
}


def main(argv):
    mode = 'expected'
    if argv and argv[0] == '--program':
        mode = 'program'
        argv = argv[1:]
    if len(argv) != 1 or argv[0] not in TESTS:
        sys.exit('usage: lists.py [--program] ' + '|'.join(TESTS))
    p = TESTS[argv[0]][1]()
    sys.stdout.write(p.program() if mode == 'program' else p.output())


if __name__ == '__main__':
    main(sys.argv[1:])
