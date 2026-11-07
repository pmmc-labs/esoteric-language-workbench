#!/usr/bin/env python3
"""Model for step 6 (maps): tests 600 to 611 (and 606's standard input).

Each test is a Ditto program and the output LANGUAGE.md defines for it,
worked out here by Python, never by running the compiler. A map is a
Python dict, which is insertion-ordered and keeps a key's place when its
value is replaced, as D16 and LANGUAGE.md (Assignment) say. The model is
D7's definition, as in lists.py: every variable owns its value, every
assignment, argument and store takes `copy.deepcopy` of what it is given,
and an update changes the variable's own copy in place. The compiler does
the opposite (shares, never writes, rebuilds the spine), so agreement is a
real check of the core rule and not the same code twice.

Python's own comparisons are not used on Ditto values: `True == 1` in
Python and `{"a": 1} == {"a": True}` would be wrong in Ditto. `eq`, `cmp`,
`show` and `lit` are written from LANGUAGE.md: structural equality by
type, maps equal when they have the same keys with equal values whatever
the order (D18); `<` on ints, strings and lists only; the printed form
with strings bare at the top and quoted inside a list or map, keys printed
as values are (D24). Ints are Python ints, keys are ints or ASCII strings
(no bool is ever a key, so Python's `1 == True` cannot matter), and the
programs here never overflow.

Tests 600 to 609 are fixed programs: literals and printing; lookups and
`.name` on nested values; setting keys (in place when present, at the end
when not); `==` regardless of order, `in`, `not in`; `len`, `keys`,
`remove` and `for` over keys; paths that mix indexes, keys and fields,
with compound assignment; word frequencies (with standard input); an
inventory; nested records; and the core rule's cases for maps. Tests 610
and 611 are random programs: a generator writes lets, copies, key sets,
removals, path updates, compound updates, calls that change their
parameter and loops that change what they iterate, choosing only
operations that are valid in the state the Python side has reached.
Seeds are fixed, so reruns are identical.

    python3 t/models/maps.py --program literals > t/600-literals.ditto
    python3 t/models/maps.py literals > t/600-literals.expected
    python3 t/models/maps.py --program lookups > t/601-lookups.ditto
    python3 t/models/maps.py lookups > t/601-lookups.expected
    python3 t/models/maps.py --program set-keys > t/602-set-keys.ditto
    python3 t/models/maps.py set-keys > t/602-set-keys.expected
    python3 t/models/maps.py --program equality > t/603-equality.ditto
    python3 t/models/maps.py equality > t/603-equality.expected
    python3 t/models/maps.py --program iteration > t/604-iteration.ditto
    python3 t/models/maps.py iteration > t/604-iteration.expected
    python3 t/models/maps.py --program path-updates > t/605-path-updates.ditto
    python3 t/models/maps.py path-updates > t/605-path-updates.expected
    python3 t/models/maps.py --program word-freq > t/606-word-freq.ditto
    python3 t/models/maps.py --stdin word-freq > t/606-word-freq.stdin
    python3 t/models/maps.py word-freq > t/606-word-freq.expected
    python3 t/models/maps.py --program inventory > t/607-inventory.ditto
    python3 t/models/maps.py inventory > t/607-inventory.expected
    python3 t/models/maps.py --program records > t/608-records.ditto
    python3 t/models/maps.py records > t/608-records.expected
    python3 t/models/maps.py --program core-rule > t/609-core-rule.ditto
    python3 t/models/maps.py core-rule > t/609-core-rule.expected
    python3 t/models/maps.py --program random-a > t/610-random-a.ditto
    python3 t/models/maps.py random-a > t/610-random-a.expected
    python3 t/models/maps.py --program random-b > t/611-random-b.ditto
    python3 t/models/maps.py random-b > t/611-random-b.expected
"""
import copy
import functools
import random
import re
import sys

MAX = 2**63 - 1
MIN = -(2**63)

KEYWORDS = set('and break continue else false fn for if in let nil not or return true while'.split())


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
    """`==`: structural, by type; true is not 1; maps ignore key order."""
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


def sort_list(xs):
    return sorted(xs, key=functools.cmp_to_key(cmp))


def contains(c, x):
    """`x in c` for a map (a key), a list (an element) or a string."""
    if isinstance(c, dict):
        return (is_int(x) or isinstance(x, str)) and x in c
    if isinstance(c, list):
        return any(eq(x, y) for y in c)
    return x in c


ESC = {'\\': '\\\\', '"': '\\"', '\n': '\\n', '\t': '\\t', '\r': '\\r'}


def show(v, quoted=False):
    """The printed form (what `str` gives); strings are quoted inside a list or map."""
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


def is_name(s):
    return re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', s) is not None and s not in KEYWORDS


def lit_key(k, bare=True):
    if isinstance(k, str):
        if bare and is_name(k):
            return k
        return lit(k)
    return lit(k)


def lit(v, bare=True):
    """Ditto source for the value v. There is no negative literal, and the
    smallest int is written as a subtraction (LANGUAGE.md, Lexical). A key
    that is a name is written bare unless bare is false."""
    if v is True: return 'true'
    if v is False: return 'false'
    if v is None: return 'nil'
    if isinstance(v, str):
        out = ''
        for c in v:
            out += ESC.get(c, '\\{' if c == '{' else c)
        return '"' + out + '"'
    if isinstance(v, list):
        return '[' + ', '.join(lit(x, bare) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ', '.join(f'{lit_key(k, bare)}: {lit(x, bare)}' for k, x in v.items()) + '}'
    if v == MIN: return '(-9223372036854775807 - 1)'
    return f'-{-v}' if v < 0 else str(v)


def trunc_div(x, y):
    q = abs(x) // abs(y)
    return q if (x < 0) == (y < 0) else -q


def apply(op, cur, v):
    """The compound assignment `cur op= v` on ints, strings and lists."""
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

def I(i):
    """A path step `[i]` for a literal int or string key."""
    return (f'[{lit(i)}]', i)


def E(src, i):
    """A path step `[src]` whose expression has the value i."""
    return (f'[{src}]', i)


def F(name):
    """A path step `.name`: the key is the string name."""
    return (f'.{name}', name)


def step(s):
    if isinstance(s, tuple):
        return s
    return I(s)


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
        """No list or map is reachable twice: every variable owns its whole value."""
        seen = set()

        def walk(v):
            if isinstance(v, (list, dict)):
                assert id(v) not in seen, 'the model aliased a container'
                seen.add(id(v))
                for x in (v.values() if isinstance(v, dict) else v):
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
        """`name<path> op= v`. Every step but the last must be present; the
        last is set (a map key is added at the end if absent, a list index
        must be in range); a compound operator reads the current value, which
        must be present."""
        path = [step(s) for s in path]
        self.line(f'{name}{"".join(s for s, _ in path)} {op} {src or lit(v)}')
        box = self.vars[name]
        for _, k in path[:-1]:
            if isinstance(box, dict):
                assert k in box, 'a model program must not fault'
            else:
                assert 0 <= k < len(box), 'a model program must not fault'
            box = box[k]
        k = path[-1][1]
        if isinstance(box, dict):
            assert op == '=' or k in box, 'a model program must not fault'
            box[k] = copy.deepcopy(v) if op == '=' else apply(op, box[k], v)
        else:
            assert 0 <= k < len(box), 'a model program must not fault'
            box[k] = copy.deepcopy(v) if op == '=' else apply(op, box[k], v)
        self.check()


# --- 600: literals and printing ---------------------------------------------

def literals():
    p = Prog()
    values = [
        {}, {'a': 1}, {'a': 1, 'b': 2}, {'b': 2, 'a': 1}, {'name': 'pen', 'qty': 3},
        {1: 'x'}, {1: 'x', 2: 'y'}, {2: 'y', 1: 'x'}, {-1: 'neg', 0: 'zero', 1: 'one'}, {7: 7},
        {MAX: 1, 5: 2}, {'a': None, 'b': True, 'c': False}, {'k': []}, {'k': {}}, {'k': [{}]},
        {'a': {'b': {'c': {'d': 1}}}}, {'xs': [1, 2, 3], 'm': {'y': 'z'}},
        {'a b': 1, '': 2, 'with"quote': 3, 'back\\slash': 4, 'nl\nx': 5, 'tab\tx': 6, 'cr\rx': 7},
        {'in': 1, 'nil': 2, 'if': 3}, {'3': 'string three', 3: 'int three'},
        {'s': 'a"b', 't': 'c\\d', 'u': 'e\nf', 'v': 'k{l}m'},
        {'a': 1, 'b': {'a': 2}, 'c': [{'a': 3}, {'a': 4}]},
        {1: {2: {3: 'deep'}}}, {'only': {'one': {}}},
        {'z': 1, 'y': 2, 'x': 3, 'w': 4, 'v': 5, 'u': 6},
    ]
    for v in values:
        p.prlit(v)
    # The same literals with every name key spelled as a string.
    for v in values[:6] + values[11:13] + values[15:17]:
        p.pr([lit(v, bare=False)], [v])
    # Several arguments: strings are bare at the top level and quoted in a map.
    p.pr(['{a: "x"}', '"x"', '["x"]', '{}'], [{'a': 'x'}, 'x', ['x'], {}])
    # Int key spellings: underscores, leading zeros, a leading minus.
    p.pr(['{1_000: "a", 007: "b", -0012: "c", 0: "d"}'], [{1000: 'a', 7: 'b', -12: 'c', 0: 'd'}])
    # A trailing comma, and a literal broken across lines.
    p.pr(['{a: 1, b: 2,}', '{a: 1,}', '{x: [1, 2,],}'], [{'a': 1, 'b': 2}, {'a': 1}, {'x': [1, 2]}])
    p.line('let layout = {',
           '  first: 1,',
           '  "second": 2,',
           '  3: "third",',
           '',
           '  fourth: {',
           '    inner: [',
           '      1,',
           '      2,',
           '    ],',
           '  },',
           '}',
           'print(layout)')
    p.say({'first': 1, 'second': 2, 3: 'third', 'fourth': {'inner': [1, 2]}})
    p.line('print({', '  a:', '    1 +', '    2', '  ,', '  b : 4 }', ')')
    p.say({'a': 3, 'b': 4})
    # Values are any expressions, evaluated in order.
    p.line('fn tick(n) {', '  print("tick", n)', '  return n * 10', '}',
           'let ordered = {c: tick(1), a: tick(2), b: tick(3)}', 'print(ordered)')
    p.say('tick', 1); p.say('tick', 2); p.say('tick', 3)
    p.say({'c': 10, 'a': 20, 'b': 30})
    p.pr(['{n: 1 + 2 * 3, s: "a" + "b", l: [1] + [2], b: 1 < 2, m: {x: 1}}'],
         [{'n': 7, 's': 'ab', 'l': [1, 2], 'b': True, 'm': {'x': 1}}])
    # str, interpolation, len.
    p.line('let m = {"a": "x", b: [1, "y"], c: nil}')
    m = {'a': 'x', 'b': [1, 'y'], 'c': None}
    p.pr(['str(m)'], [show(m)])
    p.pr(['str(m) + "!"', 'len(str(m))'], [show(m) + '!', len(show(m))])
    p.line('print("m = {m}, a = {m.a}, b = {m.b}, c = {m.c}")')
    p.say(f'm = {show(m)}, a = x, b = {show(m["b"])}, c = nil')
    p.line('print("{{}}{{a: 1}}{{1: "one"}}")')
    p.say('{}{"a": 1}{1: "one"}')
    p.pr(['len(m)', 'len({})', 'len({a: {b: 1, c: 2}})', 'len({1: 1, 2: 2, 3: 3})'], [3, 0, 1, 3])
    p.pr(['{} == {}', '{a: 1} != {a: 2}', '{} != []', '{} != nil'], [True, True, True, True])
    return p


# --- 601: lookups and fields -------------------------------------------------

def lookups():
    p = Prog()
    p.let('m', {'name': 'pen', 'qty': 3, 'tags': ['red', 'blue'], 'dims': {'w': 4, 'h': 9}, 1: 'one', -2: 'minus two', '': 'empty'})
    m = p.vars['m']
    p.pr(['m["name"]', 'm.name', 'm["qty"]', 'm.qty', 'm[1]', 'm[-2]', 'm[""]'],
         [m['name'], m['name'], 3, 3, 'one', 'minus two', 'empty'])
    p.pr(['m.tags', 'm.tags[1]', 'm.dims', 'm.dims.w', 'm["dims"]["h"]', 'm.dims["w"] * m.dims.h', 'len(m.tags)'],
         [m['tags'], 'blue', m['dims'], 4, 9, 36, 2])
    # Keys that are computed.
    p.line('let k = "qty"', 'let n = 1')
    p.pr(['m[k]', 'm["q" + "ty"]', 'm[n]', 'm[n - 3]', 'm[len("ab") - 4]', 'm[slice("x", 0, 0)]'],
         [3, 3, 'one', 'minus two', 'minus two', 'empty'])
    # Int keys and string keys with the same spelling are different keys.
    p.let('both', {1: 'int one', '1': 'string one', 2: 'int two'})
    p.pr(['both[1]', 'both["1"]', 'both[2]', 'both[str(1)]', 'both[int("2")]'], ['int one', 'string one', 'int two', 'string one', 'int two'])
    # Fields of records inside lists, and lists inside records.
    p.let('rows', [{'id': 1, 'tags': ['a']}, {'id': 2, 'tags': ['b', 'c']}, {'id': 3, 'tags': []}])
    rows = p.vars['rows']
    p.pr(['rows[0].id', 'rows[1].tags[1]', 'rows[2].tags', 'rows[len(rows) - 1].id', 'rows[rows[0].id].id'],
         [1, 'c', [], 3, 2])
    p.line('let total = 0', 'for r in rows {', '  total += r.id * len(r.tags)', '}', 'print(total)')
    p.say(sum(r['id'] * len(r['tags']) for r in rows))
    # Fields of calls, parenthesized values and literals.
    p.line('fn point(x, y) {', '  return {x: x, y: y}', '}', 'fn pick(r, k) {', '  return r[k]', '}',
           'fn getx(r) {', '  return r.x', '}')
    p.pr(['point(3, 4).x', 'point(3, 4).y + 1', 'pick(point(5, 6), "y")', 'getx({x: "ex", y: 0})', '(point(1, 2)).x',
          '{a: {b: 7}}.a.b', '{a: [10, 20]}.a[1]', '{1: "i"}[1]', '{x: 1}["x"] + {x: 2}.x'],
         [3, 5, 6, 'ex', 1, 7, 20, 'i', 3])
    # A field binds tighter than prefix minus, and indexes and fields chain.
    p.let('d', {'a': 5, 'b': {'c': [{'e': 2}]}})
    p.pr(['-d.a', '-d.a * 2', 'd.b.c[0].e', 'd["b"].c[0]["e"]', '-d.b.c[0].e + d.a'], [-5, -10, 2, 2, 3])
    # A map value taken out is a value of its own.
    p.let_expr('inner', 'd.b', p.vars['d']['b'])
    p.set('inner', [F('c')], [], '=')
    p.pr(['d', 'inner'], [p.vars['d'], p.vars['inner']])
    # The same name as a variable, a function, a builtin: a field is only a key.
    p.line('let len2 = {len: 1, print: 2, str: 3, keys: 4, remove: 5, in2: 6}',
           'print(len2.len, len2.print, len2.str, len2.keys, len2.remove)')
    p.say(1, 2, 3, 4, 5)
    p.line('let name = "name"', 'let rec = {name: "the name key", other: name}', 'print(rec.name, rec.other, rec[name])')
    p.say('the name key', 'name', 'the name key')
    # Fields in interpolation.
    p.line('print("{rows[1].id}:{rows[1].tags[0]}:{point(1, 2).y}:{d.b.c[0].e}")')
    p.say('2:b:2:2')
    return p


# --- 602: setting keys ----------------------------------------------------------

def set_keys():
    p = Prog()
    p.let('m', {})
    p.show('m')
    p.set('m', ['b'], 1)
    p.set('m', ['a'], 2)
    p.show('m')
    p.set('m', ['b'], 10)          # in place: b keeps its place
    p.show('m')
    p.set('m', ['c'], 3)           # at the end
    p.set('m', [F('d')], 4)
    p.set('m', [F('a')], 20)
    p.show('m')
    p.line('print(keys(m), len(m))')
    p.say(list(p.vars['m']), len(p.vars['m']))
    p.set('m', [5], 'five')
    p.set('m', [-5], 'minus')
    p.set('m', [0], 'zero')
    p.set('m', [5], 'FIVE')
    p.set('m', ['5'], 'str five')
    p.show('m')
    p.line('print(m[5], m["5"], m[-5], m[0])')
    p.say('FIVE', 'str five', 'minus', 'zero')
    # Computed keys, each evaluated once, before the right-hand side.
    p.line('fn k(s) {', '  print("key", s)', '  return s', '}', 'fn v(n) {', '  print("value", n)', '  return n', '}')
    p.line('let o = {}', 'o[k("x")] = v(1)', 'o[k("y")] = v(2)', 'o[k("x")] = v(3)', 'print(o)')
    p.say('key', 'x'); p.say('value', 1); p.say('key', 'y'); p.say('value', 2); p.say('key', 'x'); p.say('value', 3)
    p.say({'x': 3, 'y': 2})
    # A counter per word.
    p.line('let counts = {}', 'for w in ["b", "a", "b", "c", "a", "b"] {', '  if w in counts {',
           '    counts[w] += 1', '  } else {', '    counts[w] = 1', '  }', '}', 'print(counts)')
    c = {}
    for w in ['b', 'a', 'b', 'c', 'a', 'b']:
        c[w] = c[w] + 1 if w in c else 1
    p.say(c)
    # Setting a key to every type of value, and replacing a value by another type.
    p.let('t', {'v': 1})
    for val in ['text', None, True, False, [1, 2], {'n': {}}, -7, '', []]:
        p.set('t', ['v'], val)
        p.show('t')
    p.set('t', ['w'], 0)
    p.set('t', ['w'], 5, '+=')
    p.set('t', ['w'], 2, '*=')
    p.set('t', ['w'], 3, '-=')
    p.set('t', ['w'], 4, '/=')
    p.set('t', ['w'], 2, '%=')
    p.show('t')
    p.set('t', ['s'], 'ab')
    p.set('t', ['s'], 'cd', '+=')
    p.set('t', ['l'], [1])
    p.set('t', ['l'], [2, 3], '+=')
    p.show('t')
    # Many keys: order is the order of first insertion.
    p.line('let wide = {}', 'for i in 0..20 {', '  wide[i * 7 % 20] = i', '}', 'print(wide)')
    wide = {}
    for i in range(20):
        wide[i * 7 % 20] = i
    p.say(wide)
    p.line('for i in 0..20 {', '  wide[19 - i] = wide[i * 7 % 20] + 100', '}', 'print(wide)')
    for i in range(20):
        wide[19 - i] = wide[i * 7 % 20] + 100
    p.say(wide)
    # A key set to a map or list and set again: values, not references.
    p.line('let a = {x: 1}', 'let b = {}', 'b["first"] = a', 'a.x = 2', 'b["second"] = a', 'print(a, b)')
    p.say({'x': 2}, {'first': {'x': 1}, 'second': {'x': 2}})
    return p


# --- 603: == regardless of order, in ------------------------------------------------

def equality():
    p = Prog()
    pool = [
        {}, {'a': 1}, {'a': 2}, {'a': 1, 'b': 2}, {'b': 2, 'a': 1}, {'a': 1, 'b': 3}, {'a': 1, 'b': 2, 'c': 3},
        {'c': 3, 'b': 2, 'a': 1}, {1: 'x'}, {'1': 'x'}, {1: 'x', 2: 'y'}, {2: 'y', 1: 'x'}, {1: 'x', 2: 'z'},
        {'a': [1, 2]}, {'a': [2, 1]}, {'a': {'b': 1}}, {'a': {'b': 2}}, {'a': {'b': 1, 'c': 2}}, {'a': {'c': 2, 'b': 1}},
        {'a': None}, {'a': True}, {'a': False}, {'a': 0}, {'a': ''}, {'a': []}, {'a': {}},
        {'x': {'y': {'z': 1, 'w': 2}, 'v': [{'u': 1, 't': 2}]}}, {'x': {'v': [{'t': 2, 'u': 1}], 'y': {'w': 2, 'z': 1}}},
    ]
    for a in pool:
        for b in pool:
            p.pr([f'{lit(a)} == {lit(b)}', f'{lit(a)} != {lit(b)}'], [eq(a, b), not eq(a, b)])
    others = [[], [1], 1, 'a', True, False, None, '', 0]
    for a in pool[:5] + pool[13:14]:
        for o in others:
            p.pr([f'{lit(a)} == {lit(o)}', f'{lit(o)} != {lit(a)}'], [False, True])
    # Equality inside lists, and of lists of maps in different orders.
    ls = [[{'a': 1, 'b': 2}], [{'b': 2, 'a': 1}], [{'a': 1}, {'b': 2}], [{'b': 2}, {'a': 1}], [{}], [[]], [{'a': [{'b': 1}]}], [{'a': [{'b': 1}]}]]
    for a in ls:
        for b in ls:
            p.pr([f'{lit(a)} == {lit(b)}'], [eq(a, b)])
    # A map built in a different order equals the other.
    p.line('let m1 = {}', 'let m2 = {}', 'for k in ["p", "q", "r"] { m1[k] = len(k) }',
           'for k in ["r", "q", "p"] { m2[k] = len(k) }', 'print(m1 == m2, keys(m1), keys(m2))')
    p.say(True, ['p', 'q', 'r'], ['r', 'q', 'p'])
    p.line('m2.q = 5', 'print(m1 == m2)', 'm2.q = 1', 'print(m1 == m2)', 'm2 = remove(m2, "p")', 'print(m1 == m2)', 'm2.p = 1', 'print(m1 == m2, keys(m2))')
    p.say(False); p.say(True); p.say(False); p.say(True, ['r', 'q', 'p'])
    # in and not in.
    maps = [{}, {'a': 1}, {'a': 1, 'b': None}, {1: 'x', '1': 'y'}, {-1: 0, 0: 0}, {'': 1}, {'a b': 1}, {'a': {'b': 1}}]
    xs = ['a', 'b', '', 'a b', '1', 1, 2, -1, 0, None, True, False, [], [1], {}, {'a': 1}]
    for c in maps:
        for x in xs:
            p.pr([f'{lit(x)} in {lit(c)}', f'{lit(x)} not in {lit(c)}'], [contains(c, x), not contains(c, x)])
    # in looks at keys, not values; a key with a nil value is still a key.
    p.let('m', {'k': None, 'v': 'k', 3: 4})
    p.pr(['"k" in m', 'nil in m', '4 in m', '3 in m', '"v" in m', 'm.v in m', 'm.k in m'], [True, False, False, True, True, True, False])
    p.line('if "k" in m and m.k == nil { print("nil value") }')
    p.say('nil value')
    # Other comparisons of maps are faults (see the fault tests); == never is.
    p.pr(['m == m', 'm == {k: nil, v: "k", 3: 4}', 'm == {3: 4, v: "k", k: nil}', 'm != {3: 4}'], [True, True, True, True])
    return p


# --- 604: len, keys, remove, for -----------------------------------------------------

def iteration():
    p = Prog()
    p.let('m', {'one': 1, 'two': 2, 'three': 3, 4: 'four', -5: 'minus five'})
    m = p.vars['m']
    p.pr(['len(m)', 'keys(m)', 'len(keys(m))', 'keys({})', 'keys({a: 1})'], [5, list(m), 5, [], ['a']])
    p.line('for k in m {', '  print(k, m[k])', '}')
    for k in m:
        p.say(k, m[k])
    p.line('let ks = []', 'for k in m { ks += [k] }', 'print(ks == keys(m), ks)')
    p.say(True, list(m))
    # for over keys is over a snapshot: changing the map in the loop is not seen.
    p.line('let seen = []', 'for k in m {', '  seen += [k]', '  m["extra"] = 0', '  m.one += 1', '}', 'print(seen)', 'print(m)')
    seen = list(m)
    for _ in seen:
        m['extra'] = 0
        m['one'] += 1
    p.say(seen)
    p.say(m)
    p.line('for k in m {', '  m = {}', '}', 'print(m, len(m))')
    p.vars['m'] = {}
    p.say({}, 0)
    p.line('for k in {} { print("never") }', 'for k in {a: 1} { print("once", k) }')
    p.say('once', 'a')
    p.line('for k in {x: 1, y: 2} {', '  for j in {p: 1, q: 2} { print(k, j) }', '}')
    for k in 'xy':
        for j in 'pq':
            p.say(k, j)
    p.line('let n = 0', 'for k in {a: 1, b: 2, c: 3} {', '  if k == "b" { continue }', '  n += 1', '}', 'print(n)')
    p.say(2)
    p.line('for k in {a: 1, b: 2, c: 3} {', '  if k == "b" { break }', '  print(k)', '}')
    p.say('a')
    p.line('for k in {a: 1} { k = k + "!"', '  print(k) }')
    p.say('a!')
    # The loop variable is a copy of the key.
    p.line('let src = {k1: [1], k2: [2]}', 'let total = 0', 'for k in src {', '  for x in src[k] { total += x }', '}', 'print(total)')
    p.say(3)
    # remove: a new map; the original is as it was; absent keys change nothing.
    p.let('inv', {'a': 1, 'b': 2, 'c': 3, 'd': 4})
    inv = p.vars['inv']
    p.pr(['remove(inv, "b")', 'inv', 'remove(inv, "z")', 'remove(inv, 1)', 'remove(inv, "a") == remove(inv, "a")'],
         [{'a': 1, 'c': 3, 'd': 4}, inv, inv, inv, True])
    p.pr(['remove(remove(inv, "a"), "d")', 'remove(remove(remove(remove(inv, "a"), "b"), "c"), "d")', 'remove({}, "x")', 'len(remove(inv, "c"))'],
         [{'b': 2, 'c': 3}, {}, {}, 3])
    p.pr(['remove(inv, [1])', 'remove(inv, {})', 'remove(inv, nil)', 'remove(inv, true)'], [inv, inv, inv, inv])
    p.line('let gone = remove(inv, "a")', 'gone.a = 100', 'print(gone, inv)')
    p.say({'b': 2, 'c': 3, 'd': 4, 'a': 100}, inv)
    p.line('let ks2 = keys(inv)', 'ks2 += ["z"]', 'print(ks2, inv)')
    p.say(list(inv) + ['z'], inv)
    p.line('inv = remove(inv, "c")', 'inv.c = 33', 'print(inv)')
    del inv['c']; inv['c'] = 33
    p.say(inv)
    # Removing while walking the keys.
    p.line('let all = {a: 1, b: 2, c: 3, d: 4, e: 5}', 'for k in keys(all) {', '  if all[k] % 2 == 0 { all = remove(all, k) }', '}', 'print(all)')
    p.say({'a': 1, 'c': 3, 'e': 5})
    # Keys are strings and ints in order; sort them when they are alike.
    p.line('let sq = {}', 'for i in 0..8 {', '  sq[(i * 5) % 8] = i * i', '}', 'print(keys(sq), sort(keys(sq)))')
    sq = {}
    for i in range(8): sq[(i * 5) % 8] = i * i
    p.say(list(sq), sort_list(list(sq)))
    p.line('for k in sort(keys(sq)) { print(k, sq[k]) }')
    for k in sort_list(list(sq)): p.say(k, sq[k])
    return p


# --- 605: paths that mix indexes, keys and fields ---------------------------------------

def path_updates():
    p = Prog()
    p.let('db', {'users': [{'name': 'ann', 'tags': ['a'], 'stats': {'n': 1}}, {'name': 'bob', 'tags': [], 'stats': {'n': 2}}], 'count': 2})
    p.show('db')
    p.set('db', [F('users'), 0, F('name')], 'Ann')
    p.set('db', ['users', 1, 'name'], 'Bob', '+=')
    p.set('db', [F('users'), 0, F('tags')], ['b'], '+=')
    p.set('db', [F('users'), 1, F('tags'), ], ['x', 'y'], '+=')
    p.set('db', [F('users'), 1, F('tags'), 1], 'z')
    p.set('db', [F('users'), 0, F('stats'), F('n')], 5, '+=')
    p.set('db', [F('users'), E('1', 1), F('stats'), E('"n"', 'n')], 3, '*=')
    p.set('db', [F('users'), 0, F('stats'), F('extra')], True)
    p.set('db', [F('count')], 1, '+=')
    p.set('db', [F('users')], [{'name': 'cy'}], '+=')
    p.set('db', [F('users'), 2, F('tags')], [])
    p.set('db', [F('meta')], {'v': 1})
    p.set('db', [F('meta'), F('w')], {'v': 2})
    p.set('db', [F('meta'), F('w'), F('v')], 2, '*=')
    p.show('db')
    db = p.vars['db']
    p.pr(['db.users[1].tags', 'db.users[0].stats', 'db.meta.w.v', 'len(db.users)', 'db["users"][2]["name"]'],
         [db['users'][1]['tags'], db['users'][0]['stats'], db['meta']['w']['v'], len(db['users']), db['users'][2]['name']])
    # A map of lists of maps, with computed steps.
    p.line('let g = {}', 'for i in 0..3 {', '  g[i] = []', '  for j in 0..3 {', '    g[i] += [{pos: i * 3 + j, v: 0}]', '  }', '}')
    g = {i: [{'pos': i * 3 + j, 'v': 0} for j in range(3)] for i in range(3)}
    p.vars['g'] = g
    p.line('for i in 0..3 {', '  for j in 0..3 {', '    g[i][j].v += i * j + g[i][j].pos', '  }', '}')
    for i in range(3):
        for j in range(3):
            g[i][j]['v'] += i * j + g[i][j]['pos']
    p.show('g')
    p.line('g[1][2] = g[2][1]', 'g[2][1].v = -1', 'g[0][0] = {pos: -1}', 'g[3] = [g[1][2], g[0][0]]')
    g[1][2] = copy.deepcopy(g[2][1])
    g[2][1]['v'] = -1
    g[0][0] = {'pos': -1}
    g[3] = [copy.deepcopy(g[1][2]), copy.deepcopy(g[0][0])]
    p.show('g')
    p.set('g', [3, 1, F('pos')], 10, '*=')
    p.show('g')
    # Compound assignment on every operator.
    p.let('c', {'n': 100, 's': 'ab', 'l': [1], 'k': {'n': 7}})
    for op, val in [('+=', 5), ('-=', 3), ('*=', 4), ('/=', 7), ('%=', 5), ('/=', -2), ('*=', -3), ('%=', 4)]:
        p.set('c', [F('n')], val, op)
    p.set('c', [F('s')], 'cd', '+=')
    p.set('c', [F('l')], [2], '+=')
    p.set('c', [F('k'), F('n')], 3, '-=')
    p.show('c')
    # Keys are evaluated left to right, then the current value, then the right-hand side.
    p.line('fn say(n) {', '  print("say", n)', '  return n', '}',
           'fn key(s) {', '  print("key", s)', '  return s', '}',
           'let o = {a: {b: 1}, c: 2}', 'o[key("a")][key("b")] += say(10)', 'print(o)')
    p.say('key', 'a'); p.say('key', 'b'); p.say('say', 10)
    p.say({'a': {'b': 11}, 'c': 2})
    p.line('o[key("c")] = say(5) + o.c', 'print(o)')
    p.say('key', 'c'); p.say('say', 5)
    p.say({'a': {'b': 11}, 'c': 7})
    # A path in a function: the parameter is changed, the caller's is not.
    p.line('fn bump(r) {', '  r.n += 1', '  r.log = [r.n]', '  r.sub.deep = "d"', '  return r', '}',
           'let rec = {n: 0, sub: {}}', 'let bumped = bump(rec)', 'print(rec, bumped)')
    p.say({'n': 0, 'sub': {}}, {'n': 1, 'sub': {'deep': 'd'}, 'log': [1]})
    return p


# --- 606: word frequencies (standard input) -----------------------------------------------

WORD_TEXT = '''the quick brown fox jumps over the lazy dog
The dog barks; the fox runs away
a quick brown dog and a lazy fox
  jumps   over   it all
the end of the story is the end
'''


def word_freq_words():
    return [w for w in re.split(r'[ \t\n\r]+', WORD_TEXT) if w != '']


def word_freq():
    p = Prog()
    p.line('let counts = {}', 'let order = []',
           'for w in words(lower(read())) {',
           '  if w in counts {',
           '    counts[w] += 1',
           '  } else {',
           '    counts[w] = 1',
           '    order += [w]',
           '  }',
           '}',
           'print(len(counts), "distinct words in order:", order)',
           'let pairs = []',
           'for w in counts { pairs += [[-counts[w], w]] }',
           'for pair in sort(pairs) {',
           '  print("{pair[1]}: {-pair[0]}")',
           '}',
           'let best = sort(pairs)[0]',
           'print("most common:", best[1], -best[0])',
           'let by_len = {}',
           'for w in order {',
           '  if len(w) in by_len {',
           '    by_len[len(w)] += [w]',
           '  } else {',
           '    by_len[len(w)] = [w]',
           '  }',
           '}',
           'for n in sort(keys(by_len)) { print(n, by_len[n]) }',
           'print(counts == counts, counts.the, "dog" in counts, "cat" in counts)')
    words = [w.lower() for w in word_freq_words()]
    counts, order = {}, []
    for w in words:
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1
            order.append(w)
    p.say(len(counts), 'distinct words in order:', order)
    pairs = [[-counts[w], w] for w in counts]
    for pair in sort_list(pairs):
        p.say(f'{pair[1]}: {-pair[0]}')
    best = sort_list(pairs)[0]
    p.say('most common:', best[1], -best[0])
    by_len = {}
    for w in order:
        by_len.setdefault(len(w), []).append(w)
    for n in sort_list(list(by_len)):
        p.say(n, by_len[n])
    p.say(True, counts['the'], True, False)
    return p


# --- 607: inventory ------------------------------------------------------------------------

def inventory():
    p = Prog()
    p.line('fn add_item(inv, name, qty, price) {',
           '  if name in inv {',
           '    inv[name].qty += qty',
           '    inv[name].price = price',
           '  } else {',
           '    inv[name] = {qty: qty, price: price}',
           '  }',
           '  return inv',
           '}',
           'fn take(inv, name, qty) {',
           '  if name not in inv { return inv }',
           '  inv[name].qty -= qty',
           '  if inv[name].qty <= 0 { inv = remove(inv, name) }',
           '  return inv',
           '}',
           'fn value(inv) {',
           '  let total = 0',
           '  for name in inv { total += inv[name].qty * inv[name].price }',
           '  return total',
           '}')
    inv = {}

    def add_item(inv, name, qty, price):
        inv = copy.deepcopy(inv)
        if name in inv:
            inv[name]['qty'] += qty
            inv[name]['price'] = price
        else:
            inv[name] = {'qty': qty, 'price': price}
        return inv

    def take(inv, name, qty):
        inv = copy.deepcopy(inv)
        if name not in inv:
            return inv
        inv[name]['qty'] -= qty
        if inv[name]['qty'] <= 0:
            del inv[name]
        return inv

    def value(inv):
        return sum(r['qty'] * r['price'] for r in inv.values())

    p.line('let inv = {}')
    p.vars['inv'] = {}
    steps = [('add', 'pen', 10, 2), ('add', 'ink', 3, 15), ('add', 'pad', 5, 4), ('take', 'pen', 4), ('add', 'pen', 6, 3),
             ('take', 'ink', 5), ('take', 'cap', 1), ('add', 'cap', 1, 9), ('take', 'pad', 2), ('add', 'ink', 7, 14),
             ('take', 'cap', 1), ('take', 'pad', 3), ('add', 'pad', 1, 5)]
    for st in steps:
        if st[0] == 'add':
            _, name, qty, price = st
            p.line(f'inv = add_item(inv, {lit(name)}, {qty}, {price})')
            inv = add_item(inv, name, qty, price)
        else:
            _, name, qty = st
            p.line(f'inv = take(inv, {lit(name)}, {qty})')
            inv = take(inv, name, qty)
        p.vars['inv'] = copy.deepcopy(inv)
        p.pr(['inv', 'value(inv)', 'len(inv)'], [inv, value(inv), len(inv)])
    # A snapshot taken before a batch is the old inventory after it.
    p.line('let before = inv', 'let after = take(add_item(inv, "pen", 100, 1), "ink", 1)', 'print(before == inv, after == inv, value(before), value(after))')
    after = take(add_item(inv, 'pen', 100, 1), 'ink', 1)
    p.say(True, eq(after, inv), value(inv), value(after))
    p.line('print(inv)')
    p.say(inv)
    # Report in name order.
    p.line('for name in sort(keys(inv)) {', '  let r = inv[name]', '  print("{name}: {r.qty} at {r.price} = {r.qty * r.price}")', '}')
    for name in sort_list(list(inv)):
        r = inv[name]
        p.say(f'{name}: {r["qty"]} at {r["price"]} = {r["qty"] * r["price"]}')
    return p


# --- 608: nested records --------------------------------------------------------------------

def records():
    p = Prog()
    p.let('company', {
        'name': 'Acme',
        'staff': [
            {'name': 'Ann', 'role': 'dev', 'langs': ['c', 'py'], 'addr': {'city': 'Oslo', 'zip': 150}},
            {'name': 'Bob', 'role': 'ops', 'langs': [], 'addr': {'city': 'Rome', 'zip': 100}},
            {'name': 'Cy', 'role': 'dev', 'langs': ['ts'], 'addr': {'city': 'Oslo', 'zip': 151}},
        ],
        'depts': {'dev': {'head': 'Ann', 'size': 2}, 'ops': {'head': 'Bob', 'size': 1}},
    })
    co = p.vars['company']
    p.show('company')
    p.line('for s in company.staff {', '  print(s.name, s.role, len(s.langs), s.addr.city, s.addr.zip)', '}')
    for s in co['staff']:
        p.say(s['name'], s['role'], len(s['langs']), s['addr']['city'], s['addr']['zip'])
    p.line('let cities = {}', 'for s in company.staff {',
           '  if s.addr.city in cities {', '    cities[s.addr.city] += [s.name]', '  } else {', '    cities[s.addr.city] = [s.name]', '  }', '}',
           'print(cities)')
    cities = {}
    for s in co['staff']:
        cities.setdefault(s['addr']['city'], []).append(s['name'])
    p.say(cities)
    p.line('for d in company.depts {', '  print(d, company.depts[d].head, company.depts[d].size)', '}')
    for d in co['depts']:
        p.say(d, co['depts'][d]['head'], co['depts'][d]['size'])
    p.set('company', [F('staff'), 1, F('role')], 'dev')
    p.set('company', [F('depts'), 'dev', F('size')], 1, '+=')
    p.set('company', [F('depts'), 'ops', F('size')], 1, '-=')
    p.set('company', [F('staff'), 1, F('langs')], ['sh'], '+=')
    p.set('company', [F('staff'), 2, F('addr'), F('city')], 'Bergen')
    p.set('company', [F('staff'), 0, F('addr'), F('zip')], 1, '+=')
    p.set('company', [F('depts'), 'hr'], {'head': 'Dee', 'size': 0})
    p.show('company')
    # Records are values: a copy of a record in a list, then a change to the original.
    p.line('let first = company.staff[0]', 'company.staff[0].name = "Anna"', 'print(first.name, company.staff[0].name)')
    p.say('Ann', 'Anna')
    p.vars['company']['staff'][0]['name'] = 'Anna'
    p.line('let swap = company.staff[1]', 'company.staff[1] = company.staff[2]', 'company.staff[2] = swap',
           'print(company.staff[1].name, company.staff[2].name)')
    p.say('Cy', 'Bob')
    st = p.vars['company']['staff']
    st[1], st[2] = st[2], st[1]
    # A function that builds records and one that updates them.
    p.line('fn person(name, role) {', '  return {name: name, role: role, langs: []}', '}',
           'fn learn(p, lang) {', '  p.langs += [lang]', '  return p', '}')
    p.line('let dee = learn(learn(person("Dee", "hr"), "go"), "rs")', 'print(dee)')
    p.say({'name': 'Dee', 'role': 'hr', 'langs': ['go', 'rs']})
    p.line('let team = [person("x", "a"), person("y", "b")]', 'team[1] = learn(team[1], "ml")', 'print(team)')
    p.say([{'name': 'x', 'role': 'a', 'langs': []}, {'name': 'y', 'role': 'b', 'langs': ['ml']}])
    st = p.vars['company']['staff']
    for i, a in ((1, {'zip': st[1]['addr']['zip'], 'city': st[1]['addr']['city']}), (2, {'zip': st[2]['addr']['zip'], 'city': st[2]['addr']['city']})):
        z = {'zip': a['zip']}
        p.pr([f'company.staff[{i}].addr == {lit(a)}', f'company.staff[{i}].addr == {lit(z)}', f'company.staff[{i}].addr == {lit({"city": a["city"], "zip": a["zip"]})}'],
             [eq(st[i]['addr'], a), eq(st[i]['addr'], z), True])
    # Records in a map keyed by int.
    p.line('let byid = {}', 'for i in 0..4 {', '  byid[100 + i] = {id: 100 + i, sq: i * i}', '}', 'byid[102].sq += 1', 'print(byid)')
    byid = {100 + i: {'id': 100 + i, 'sq': i * i} for i in range(4)}
    byid[102]['sq'] += 1
    p.say(byid)
    return p


# --- 609: the core rule for maps ------------------------------------------------------------

def core_rule():
    p = Prog()
    dup = copy.deepcopy
    # let b = a, then change b; then change a.
    p.let('a', {'x': 1, 'y': 2})
    p.let_from('b', 'a')
    p.set('b', [F('x')], 99)
    p.show('a', 'b')
    p.set('a', [F('y')], -2)
    p.set('a', [F('z')], 3)
    p.show('a', 'b')
    p.set('b', ['new'], 'n')
    p.show('a', 'b')
    p.assign('b', 'a', p.vars['a'])
    p.set('a', [F('x')], 5, '+=')
    p.show('a', 'b')
    p.pr(['a == b', 'a != b'], [False, True])
    # A map as an argument changed inside a function: the caller's is untouched.
    p.line('fn bump(m) {', '  m.x = 100', '  m.added = true', '  m = remove(m, "y")', '  return m', '}',
           'fn scratch(m) {', '  m.x += 1', '}')
    p.let('c', {'x': 1, 'y': 2})
    arg = {'x': 100, 'added': True}
    p.let_expr('d', 'bump(c)', arg)
    p.show('c', 'd')
    p.line('scratch(c)')
    p.show('c')
    p.pr(['bump(c)', 'c'], [arg, p.vars['c']])
    # A function returning its parameter gives a value.
    p.line('fn same(m) {', '  return m', '}')
    p.let_expr('e', 'same(c)', p.vars['c'])
    p.set('e', [F('x')], -1)
    p.show('c', 'e')
    # A map stored in a map or list takes the value at that moment.
    p.let('inner', {'n': 1})
    p.let_expr('outer', '{one: inner, two: inner, three: [inner]}', {'one': dup(p.vars['inner']), 'two': dup(p.vars['inner']), 'three': [dup(p.vars['inner'])]})
    p.set('inner', [F('n')], 50)
    p.show('inner', 'outer')
    p.set('outer', [F('one'), F('n')], 60)
    p.set('outer', [F('three'), 0, F('n')], 70)
    p.show('inner', 'outer')
    p.line('outer.two = inner')
    p.vars['outer']['two'] = dup(p.vars['inner'])
    p.set('inner', [F('n')], 0)
    p.show('inner', 'outer')
    p.let_expr('row', 'outer.one', p.vars['outer']['one'])
    p.set('row', [F('n')], -60)
    p.show('row', 'outer')
    # A map in a list: the list is copied with the map in it.
    p.let('ms', [{'k': 1}, {'k': 2}])
    p.let_from('ms2', 'ms')
    p.set('ms2', [0, F('k')], 10)
    p.set('ms', [1, F('k')], 20)
    p.show('ms', 'ms2')
    p.let_expr('both', 'ms + ms2', cat_list(p.vars['ms'], p.vars['ms2']))
    p.set('both', [0, F('k')], 0)
    p.set('both', [2, F('k')], 0)
    p.show('ms', 'ms2', 'both')
    # A function that stores its parameter in a map, then changes the parameter.
    p.line('fn wrap(m) {', '  let box = {first: m}', '  m.v = 0', '  box.second = m', '  return box', '}')
    p.let('w', {'v': 5})
    p.let_expr('boxed', 'wrap(w)', {'first': {'v': 5}, 'second': {'v': 0}})
    p.show('w', 'boxed')
    # A loop over a map that changes it sees the map as it was.
    p.let('items', {'a': 1, 'b': 2, 'c': 3})
    p.line('let visits = []', 'for k in items {', '  items[k + "!"] = items[k] * 10', '  items.a += 1', '  visits += [k]', '}', 'print(items, visits)')
    items = dup(p.vars['items']); visits = []
    for k in list(items):
        items[k + '!'] = items[k] * 10
        items['a'] += 1
        visits.append(k)
    p.say(items, visits)
    p.vars['items'] = items
    p.line('for k in items { items = {} }', 'print(items)')
    p.say({})
    p.vars['items'] = {}
    # Snapshots taken in a loop stay as they were.
    p.line('let acc = {}', 'let snaps = []', 'for i in 0..4 {', '  acc[i] = i * i', '  snaps += [acc]', '}', 'print(acc)', 'print(snaps)')
    acc = {}; snaps = []
    for i in range(4):
        acc[i] = i * i
        snaps.append(dup(acc))
    p.say(acc)
    p.say(snaps)
    p.line('snaps[1][0] = 99', 'print(snaps[1], snaps[2], acc)')
    snaps[1][0] = 99
    p.say(snaps[1], snaps[2], acc)
    # keys() is a list of its own, remove() a map of its own.
    p.let('src', {'p': 1, 'q': 2})
    p.line('let ks = keys(src)', 'ks += ["r"]', 'ks[0] = "changed"', 'let rm = remove(src, "p")', 'rm.s = 3', 'print(src, ks, rm)')
    p.say({'p': 1, 'q': 2}, ['changed', 'q', 'r'], {'q': 2, 's': 3})
    # Self assignment, and a map that contains a copy of itself.
    p.let('me', {'n': 1})
    p.set('me', [F('me')], p.vars['me'], src='me')
    p.set('me', [F('me'), F('me')], p.vars['me'], src='me')
    p.set('me', [F('n')], 2)
    p.show('me')
    p.let('t', {'n': 1})
    p.set('t', [F('again')], p.vars['t'], src='t')
    p.assign('t', '{outer: t}', {'outer': p.vars['t']})
    p.set('t', [F('outer'), F('n')], 9)
    p.show('t')
    # Deep copies are deep.
    p.let('n1', {'a': {'b': [{'c': 1}]}})
    p.let_from('n2', 'n1')
    p.set('n2', [F('a'), F('b'), 0, F('c')], 20)
    p.show('n1', 'n2')
    p.pr(['n1 == n2', 'n1.a.b == n2.a.b', 'n1.a == {b: [{c: 1}]}'], [False, False, True])
    # A parameter passed on twice.
    p.line('fn outerfn(m) {', '  m.who = "outer"', '  return [innerfn(m), m]', '}',
           'fn innerfn(m) {', '  m.who = "inner"', '  m.extra = 1', '  return m', '}')
    p.let('base', {'v': 0})
    p.let_expr('res', 'outerfn(base)', [{'v': 0, 'who': 'inner', 'extra': 1}, {'v': 0, 'who': 'outer'}])
    p.show('base', 'res')
    return p


def cat_list(a, b):
    return copy.deepcopy(a) + copy.deepcopy(b)


# --- 610, 611: random programs --------------------------------------------------------------

WORDS = ['a', 'b', 'c', 'd', 'e', 'x', 'y', 'qty', 'name', 'id']


def touch_m(m):
    m = copy.deepcopy(m)
    m['touched'] = len(m)
    if 'a' in m:
        m['a'] += 1
    return m


def touch_n(n):
    n = copy.deepcopy(n)
    n['t'] = n.get('t', []) + [7]
    for k in list(n):
        if k != 't' and len(n[k]) < 4:
            n[k] = n[k] + [1]
    return n


def random_prog(seed, steps):
    """Kinds: M a map of word to int, N a map of word to list of ints, R a
    list of maps of word to int, I an int, K a map of int to string."""
    rng = random.Random(seed)
    p = Prog()
    kinds = {}
    p.line('fn touch_m(m) {', '  m.touched = len(m)', '  if "a" in m { m.a += 1 }', '  return m', '}',
           'fn touch_n(n) {', '  if "t" in n { n.t += [7] } else { n.t = [7] }',
           '  for k in keys(n) {', '    if k != "t" and len(n[k]) < 4 { n[k] += [1] }', '  }', '  return n', '}',
           'fn total(m) {', '  let s = 0', '  for k in m { s += m[k] }', '  return s', '}')
    counter = [0]

    def fresh():
        counter[0] += 1
        return f'v{counter[0]}'

    def words(n):
        return rng.sample(WORDS, n)

    def value(kind):
        if kind == 'I': return rng.randint(-9, 9)
        if kind == 'M': return {w: rng.randint(-9, 9) for w in words(rng.randint(1, 4))}
        if kind == 'N': return {w: [rng.randint(0, 9) for _ in range(rng.randint(0, 3))] for w in words(rng.randint(1, 3))}
        if kind == 'R': return [{w: rng.randint(0, 9) for w in words(rng.randint(1, 2))} for _ in range(rng.randint(1, 3))]
        ks = rng.sample(range(-3, 6), rng.randint(1, 4))
        return {k: rng.choice(['p', 'q', 'rr', '']) for k in ks}

    def names(kind, pred=lambda v: True):
        return [n for n, k in kinds.items() if k == kind and pred(p.vars[n])]

    def pick(kind, pred=lambda v: True):
        c = names(kind, pred)
        return rng.choice(c) if c else None

    def declare(kind, name, src, v):
        p.let_expr(name, src, v)
        kinds[name] = kind

    def op_let():
        kind = rng.choice(['M', 'M', 'N', 'R', 'I', 'K'])
        v = value(kind)
        n = fresh()
        p.let(n, v)
        kinds[n] = kind

    def op_copy():
        kind = rng.choice(['M', 'N', 'R', 'K'])
        a = pick(kind)
        if a is None: return
        declare(kind, fresh(), a, p.vars[a])

    def op_assign():
        kind = rng.choice(['M', 'N', 'K'])
        a, b = pick(kind), pick(kind)
        if a is None: return
        p.assign(a, b, p.vars[b])

    def op_set_new():
        a = pick('M')
        if a is None: return
        w = rng.choice(WORDS)
        if rng.random() < 0.5:
            p.set(a, [F(w)], rng.randint(-9, 9))
        else:
            p.set(a, [w], rng.randint(-9, 9))

    def op_set_k():
        a = pick('K')
        if a is None: return
        k = rng.randint(-3, 6)
        p.set(a, [k], rng.choice(['p', 'q', 'rr', 'z']))

    def op_compound():
        a = pick('M', lambda v: len(v) > 0)
        if a is None: return
        w = rng.choice(list(p.vars[a]))
        op = rng.choice(['+=', '-=', '*='])
        k = rng.randint(1, 4)
        if op == '*=' and abs(p.vars[a][w]) > 10**6: return
        p.set(a, [F(w) if rng.random() < 0.5 else w], k, op)

    def op_remove():
        a = pick('M', lambda v: len(v) > 1)
        if a is None: return
        w = rng.choice(list(p.vars[a]) + ['zz'])
        p.assign(a, f'remove({a}, "{w}")', {k: v for k, v in p.vars[a].items() if k != w})

    def op_n_append():
        a = pick('N', lambda v: len(v) > 0)
        if a is None: return
        w = rng.choice(list(p.vars[a]))
        if len(p.vars[a][w]) >= 6: return
        p.set(a, [F(w)], [rng.randint(0, 9)], '+=')

    def op_n_set():
        a = pick('N', lambda v: any(len(x) > 0 for x in v.values()))
        if a is None: return
        w = rng.choice([k for k, x in p.vars[a].items() if len(x) > 0])
        i = rng.randrange(len(p.vars[a][w]))
        p.set(a, [F(w), i], rng.randint(0, 9), rng.choice(['=', '+=']))

    def op_n_new():
        a = pick('N', lambda v: len(v) < 6)
        if a is None: return
        w = rng.choice(WORDS)
        p.set(a, [w], [rng.randint(0, 9) for _ in range(rng.randint(0, 2))])

    def op_r_set():
        a = pick('R')
        if a is None: return
        i = rng.randrange(len(p.vars[a]))
        w = rng.choice(WORDS)
        p.set(a, [i, F(w)], rng.randint(0, 9))

    def op_r_compound():
        a = pick('R', lambda v: any(len(r) > 0 for r in v))
        if a is None: return
        i = rng.choice([k for k, r in enumerate(p.vars[a]) if len(r) > 0])
        w = rng.choice(list(p.vars[a][i]))
        p.set(a, [i, F(w)], rng.randint(1, 4), rng.choice(['+=', '-=']))

    def op_r_move():
        # a[i] = m: the record is a value; later changes to either stay apart
        a, m = pick('R'), pick('M')
        if a is None or m is None: return
        i = rng.randrange(len(p.vars[a]))
        p.set(a, [i], p.vars[m], src=m)

    def op_r_append():
        a, m = pick('R', lambda v: len(v) < 6), pick('M')
        if a is None or m is None: return
        p.line(f'{a} += [{m}]')
        p.vars[a] = p.vars[a] + [copy.deepcopy(p.vars[m])]

    def op_int():
        a = pick('I')
        if a is None: return
        k = rng.randint(1, 5)
        op = rng.choice(['+=', '-=', '*='])
        if op == '*=' and abs(p.vars[a]) > 10**6: return
        p.line(f'{a} {op} {k}')
        p.vars[a] = apply(op, p.vars[a], k)

    def op_touch_m():
        a = pick('M')
        if a is None: return
        if rng.random() < 0.5:
            p.pr([f'touch_m({a})', a], [touch_m(p.vars[a]), p.vars[a]])
        else:
            declare('M', fresh(), f'touch_m({a})', touch_m(p.vars[a]))

    def op_touch_n():
        a = pick('N')
        if a is None: return
        if rng.random() < 0.5:
            p.pr([f'touch_n({a})', a], [touch_n(p.vars[a]), p.vars[a]])
        else:
            declare('N', fresh(), f'touch_n({a})', touch_n(p.vars[a]))

    def op_total():
        a = pick('M')
        if a is None: return
        p.pr([f'total({a})', f'len({a})', f'keys({a})'], [sum(p.vars[a].values()), len(p.vars[a]), list(p.vars[a])])

    def op_row_out():
        # let r = a.k; change r; a does not change
        a = pick('N', lambda v: len(v) > 0)
        if a is None: return
        w = rng.choice(list(p.vars[a]))
        n = fresh()
        declare('L', n, f'{a}.{w}', p.vars[a][w])
        p.line(f'{n} += [0]')
        p.vars[n] = p.vars[n] + [0]
        p.show(a, n)

    def op_loop_keys():
        a = pick('M', lambda v: len(v) <= 3)
        if a is None: return
        k = fresh()
        p.line(f'for {k} in {a} {{', f'  {a}[{k} + "!"] = len({a})', f'  {a}.a = 1', '}')
        m = p.vars[a]
        for key in list(m):
            m[key + '!'] = len(m)
            m['a'] = 1
        p.check()

    def op_loop_total():
        a = pick('M')
        if a is None: return
        s = fresh()
        p.line(f'let {s} = 0', f'for k in {a} {{', f'  {s} += {a}[k] * 2', f'  {a}[k] = 0', '}', f'print({s}, {a})')
        m = p.vars[a]
        t = sum(v * 2 for v in m.values())
        for key in list(m):
            m[key] = 0
        p.say(t, m)
        # `s` and `k` are in scope here and nowhere else; the program is
        # straight-line, so a fresh `s` each time is enough (k is the loop's own).

    def op_eq():
        kind = rng.choice(['M', 'N', 'K'])
        a, b = pick(kind), pick(kind)
        if a is None: return
        key = rng.randint(-3, 6) if kind == 'K' else rng.choice(WORDS)
        p.pr([f'{a} == {b}', f'{lit(key)} in {a}', f'len({a})'],
             [eq(p.vars[a], p.vars[b]), contains(p.vars[a], key), len(p.vars[a])])

    def op_show():
        if kinds:
            p.show(rng.choice(sorted(kinds)))

    ops = [op_let, op_copy, op_copy, op_assign, op_set_new, op_set_new, op_set_k, op_compound, op_compound, op_remove,
           op_n_append, op_n_set, op_n_new, op_r_set, op_r_compound, op_r_move, op_r_append, op_int, op_touch_m,
           op_touch_n, op_total, op_row_out, op_loop_keys, op_loop_total, op_eq, op_show, op_show]
    for _ in range(5):
        op_let()
    for _ in range(steps):
        rng.choice(ops)()
    for n in kinds:
        p.show(n)
    return p


# --- The command line ----------------------------------------------------------------------

TESTS = {
    'literals': ('600-literals', literals),
    'lookups': ('601-lookups', lookups),
    'set-keys': ('602-set-keys', set_keys),
    'equality': ('603-equality', equality),
    'iteration': ('604-iteration', iteration),
    'path-updates': ('605-path-updates', path_updates),
    'word-freq': ('606-word-freq', word_freq),
    'inventory': ('607-inventory', inventory),
    'records': ('608-records', records),
    'core-rule': ('609-core-rule', core_rule),
    'random-a': ('610-random-a', lambda: random_prog(610, 70)),
    'random-b': ('611-random-b', lambda: random_prog(611, 90)),
}


def main(argv):
    mode = 'expected'
    if argv and argv[0] in ('--program', '--stdin'):
        mode = argv[0][2:]
        argv = argv[1:]
    if len(argv) != 1 or argv[0] not in TESTS or (mode == 'stdin' and argv[0] != 'word-freq'):
        sys.exit('usage: maps.py [--program] ' + '|'.join(TESTS) + '\n       maps.py --stdin word-freq')
    p = TESTS[argv[0]][1]()
    if mode == 'stdin':
        sys.stdout.write(WORD_TEXT)
    else:
        sys.stdout.write(p.program() if mode == 'program' else p.output())


if __name__ == '__main__':
    main(sys.argv[1:])
