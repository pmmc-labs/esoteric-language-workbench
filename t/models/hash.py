#!/usr/bin/env python3
"""t/1500 to t/1530: hashes (step 12a; D27, D98, D102).

The definition, which is all this file knows of the language beyond
t/models/interp.py.

  my %h;  my %h = LIST;  %h = LIST;
  $h{KEY}                      the element
  $h{KEY} = V   OP=   ++  --   stored, and worked on, as an array's is
  exists($h{KEY})  delete($h{KEY})
  keys(%h)  values(%h)  %h     lists; where one value is wanted, a count

**A hash is an array whose indexes are strings.** A key is made a string
as `.` makes one (a number as it prints, a boolean `1` or the empty
string), and an undef key is a fault. One word alone in the braces, and a
word before `=>`, is that string, whatever the word.

A list for a hash is keys and values by turns: a key given twice keeps its
last value and its first place, and **an odd number of values is a
fault**. Reading a key that is not there gives undef and makes nothing;
storing makes it; an operator that reads and stores (`+=`, `//=`, `++`)
makes it first. The orders are an array's (D80): `$h{K} = V` is V, then K,
then the store; `$h{K} OP= V` is K, the element made, then V.

`delete` gives the value that was there, or undef. Where one value is
wanted, `%h`, `keys(%h)` and `values(%h)` are how many keys there are.
After `return`, each is list-shaped (D18).

**The order** (D27) is the order keys were first stored in; a key deleted
and stored again is last. perl's is another every run, so every test here
sorts what it shows, and t/checks.py refuses one that does not: the order
itself has a test of its own kind, by hand.

This model works a program out; it does not refuse one: where a word may
stand, D76, and what `exists` may be followed by are the compiler's.

The model is Python, whose dict keeps the order of first storing. perl is
the second derivation: t/checks.py oracle holds every .expected of a test
without a `kind:` to what perl 5.42 prints, and each fault test's output
to the start of it.

1500 is the literal and its keys, 1501 elements, 1502 exists, delete, the
counts and copies. 1510 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/hash.py --program 1500 > t/1500-hash-literals-and-keys.pl
    python3 t/models/hash.py 1500 > t/1500-hash-literals-and-keys.expected
    python3 t/models/hash.py --program 1501 > t/1501-hash-elements.pl
    python3 t/models/hash.py 1501 > t/1501-hash-elements.expected
    python3 t/models/hash.py --program 1502 > t/1502-hash-exists-delete-counts.pl
    python3 t/models/hash.py 1502 > t/1502-hash-exists-delete-counts.expected
    python3 t/models/hash.py --program 1510 > t/1510-fault-hash-odd-list.pl
    python3 t/models/hash.py 1510 > t/1510-fault-hash-odd-list.expected
    python3 t/models/hash.py --program 1511 > t/1511-fault-hash-odd-list-assigned.pl
    python3 t/models/hash.py 1511 > t/1511-fault-hash-odd-list-assigned.expected
    python3 t/models/hash.py --program 1512 > t/1512-fault-hash-odd-list-of-one.pl
    python3 t/models/hash.py 1512 > t/1512-fault-hash-odd-list-of-one.expected
    python3 t/models/hash.py --program 1513 > t/1513-fault-hash-odd-list-from-an-array.pl
    python3 t/models/hash.py 1513 > t/1513-fault-hash-odd-list-from-an-array.expected
    python3 t/models/hash.py --program 1514 > t/1514-fault-hash-odd-list-from-a-hash-and-one.pl
    python3 t/models/hash.py 1514 > t/1514-fault-hash-odd-list-from-a-hash-and-one.expected
    python3 t/models/hash.py --program 1515 > t/1515-fault-hash-undef-key-read.pl
    python3 t/models/hash.py 1515 > t/1515-fault-hash-undef-key-read.expected
    python3 t/models/hash.py --program 1516 > t/1516-fault-hash-undef-key-stored.pl
    python3 t/models/hash.py 1516 > t/1516-fault-hash-undef-key-stored.expected
    python3 t/models/hash.py --program 1517 > t/1517-fault-hash-undef-key-worked-on.pl
    python3 t/models/hash.py 1517 > t/1517-fault-hash-undef-key-worked-on.expected
    python3 t/models/hash.py --program 1518 > t/1518-fault-hash-undef-key-stepped.pl
    python3 t/models/hash.py 1518 > t/1518-fault-hash-undef-key-stepped.expected
    python3 t/models/hash.py --program 1519 > t/1519-fault-hash-undef-key-exists.pl
    python3 t/models/hash.py 1519 > t/1519-fault-hash-undef-key-exists.expected
    python3 t/models/hash.py --program 1520 > t/1520-fault-hash-undef-key-deleted.pl
    python3 t/models/hash.py 1520 > t/1520-fault-hash-undef-key-deleted.expected
    python3 t/models/hash.py --program 1521 > t/1521-fault-hash-undef-key-in-a-list.pl
    python3 t/models/hash.py 1521 > t/1521-fault-hash-undef-key-in-a-list.expected
    python3 t/models/hash.py --program 1522 > t/1522-fault-hash-whole-num-key.pl
    python3 t/models/hash.py 1522 > t/1522-fault-hash-whole-num-key.expected
    python3 t/models/hash.py --program 1523 > t/1523-fault-hash-whole-num-key-read.pl
    python3 t/models/hash.py 1523 > t/1523-fault-hash-whole-num-key-read.expected
    python3 t/models/hash.py --program 1524 > t/1524-fault-hash-whole-num-key-in-a-list.pl
    python3 t/models/hash.py 1524 > t/1524-fault-hash-whole-num-key-in-a-list.expected
    python3 t/models/hash.py --program 1525 > t/1525-fault-hash-missing-as-a-number.pl
    python3 t/models/hash.py 1525 > t/1525-fault-hash-missing-as-a-number.expected
    python3 t/models/hash.py --program 1526 > t/1526-fault-hash-missing-as-a-string.pl
    python3 t/models/hash.py 1526 > t/1526-fault-hash-missing-as-a-string.expected
    python3 t/models/hash.py --program 1527 > t/1527-fault-hash-deleted-as-a-string.pl
    python3 t/models/hash.py 1527 > t/1527-fault-hash-deleted-as-a-string.expected
    python3 t/models/hash.py --program 1528 > t/1528-fault-hash-string-stepped.pl
    python3 t/models/hash.py 1528 > t/1528-fault-hash-string-stepped.expected
    python3 t/models/hash.py --program 1529 > t/1529-fault-hash-returned-for-one-value.pl
    python3 t/models/hash.py 1529 > t/1529-fault-hash-returned-for-one-value.expected
    python3 t/models/hash.py --program 1530 > t/1530-fault-hash-keys-returned-for-one-value.pl
    python3 t/models/hash.py 1530 > t/1530-fault-hash-keys-returned-for-one-value.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import list as lists
import each
import ret
import it
import sort
import interp
from var import Fault, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import SCALAR, ucall, sub, req, say_, named
from sub import ret as returns
from list import A, el, mya, seta, sayl, setel, dump, Cases, items, element
from ret import jn, rev
from it import IT, mp, gr
from sort import VA, VB, srt

ODD = 'an odd number of values for a hash'
NUM = ('<=>', VA, VB)

# The expressions: ('%', name), a hash; ('hel', name, key); ('sethel', op,
# name, key, e); ('stephel', op, before, name, key); ('exists', name, key);
# ('delete', name, key); ('keys', name); ('values', name); ('count', name),
# `scalar(keys(%name))`; and in a list,
# ('=>', word, e), a word and a value. A key is ('word', w), one word alone
# in the braces, or an expression. The statements: ('myh', name, items or
# None); ('seth', name, [items]).

def H(name):
    return ('%', name)

def W(word):
    return ('word', word)

def hel(name, key):
    return ('hel', name, W(key) if isinstance(key, str) and key.isidentifier() else key)

def sethel(name, key, e, op='='):
    return ('sethel', op, name, hel(name, key)[2], e)

def stephel(name, key, op='++', before=False):
    return ('stephel', op, before, name, hel(name, key)[2])

def myh(name, *es):
    return ('myh', name, list(es))

def seth(name, *es):
    return ('seth', name, list(es))

def pair(word, e):
    return ('=>', word, e)

class Hash:
    def __init__(self):
        self.items = {}
        self.frozen = 0

lists.LISTY = lists.LISTY + ('%', 'keys', 'values', '=>')
_shaped = ret.shaped
ret.shaped = lambda e: (isinstance(e, tuple) and e[0] in ('%', 'keys', 'values')) or _shaped(e)

def changing(h):
    if h.frozen:
        raise Fault(lists.FROZEN)
    return h

class Run(interp.Run):
    def __init__(self, statements):
        super().__init__(statements)
        # The file's hashes are there, empty, before anything runs.
        for s in statements:
            if s[0] == 'myh':
                self.scopes[0]['%' + s[1]] = Hash()

    def hash(self, name):
        for scope in reversed(self.scopes):
            if '%' + name in scope:
                return scope['%' + name]
        raise AssertionError(f'%{name} is not declared')

    def key(self, k):
        """A key, worked out: a string as `.` makes one."""
        if isinstance(k, tuple) and k[0] == 'word':
            return k[1]
        return logic.value(('.', get(self.ev(k)), ''))

    def fill(self, h, values):
        if len(values) % 2:
            raise Fault(ODD)
        new = {}
        for k, v in zip(values[::2], values[1::2]):
            new[logic.value(('.', k, ''))] = v
        changing(h).items = new

    def evl(self, e):
        kind = e[0] if isinstance(e, tuple) else None
        if kind == '%':
            return [x for pair_ in self.hash(e[1]).items.items() for x in pair_]
        if kind == 'keys':
            return list(self.hash(e[1]).items)
        if kind == 'values':
            return list(self.hash(e[1]).items.values())
        if kind == '=>':
            return [e[1]] + self.evl(e[2])
        return super().evl(e)

    def ev(self, e):
        kind = e[0] if isinstance(e, tuple) else None
        if kind not in ('%', 'keys', 'values', 'count', 'hel', 'sethel', 'stephel', 'exists', 'delete'):
            return super().ev(e)
        self.ctx = SCALAR
        h = self.hash(e[3] if kind == 'stephel' else e[2] if kind == 'sethel' else e[1])
        if kind in ('%', 'keys', 'values', 'count'):
            return len(h.items)
        if kind == 'hel':
            return h.items.get(self.key(e[2]), UNDEF)
        if kind == 'exists':
            return TRUE if self.key(e[2]) in h.items else FALSE
        if kind == 'delete':
            k = self.key(e[2])
            if k not in h.items:
                return UNDEF
            return changing(h).items.pop(k)
        if kind == 'stephel':
            _, op, before, _, key = e
            k = self.key(key)
            changing(h).items.setdefault(k, UNDEF)
            old = h.items[k]
            h.items[k] = var.step(op, old)
            return h.items[k] if before else 0 if old is UNDEF and op == '++' else old
        _, op, _, key, right = e
        if op == '=':
            r = self.ev(right)
            k = self.key(key)
            changing(h).items[k] = get(r)
            return h.items[k]
        k = self.key(key)
        changing(h).items.setdefault(k, UNDEF)
        if op in ('||=', '&&=', '//='):
            old = h.items[k]
            if old is UNDEF if op == '//=' else logic.truth(old) == (op == '&&='):
                h.items[k] = get(self.ev(right))
            return h.items[k]
        r = get(self.ev(right))
        left = h.items[k]
        if left is UNDEF and op in ('+=', '-=', '.='):
            left = '' if op == '.=' else 0
        h.items[k] = logic.value((op[:-1], left, r))
        return h.items[k]

    def run(self, s):
        if s[0] == 'myh':
            self.mark(s)
            values = None if s[2] is None else [v for item in s[2] for v in self.evl(item)]
            if self.top():
                h = self.scopes[0]['%' + s[1]]
            else:
                h = self.scopes[-1]['%' + s[1]] = Hash()
            if values is not None:
                self.fill(h, values)
        elif s[0] == 'seth':
            self.mark(s)
            self.fill(self.hash(s[1]), [v for item in s[2] for v in self.evl(item)])
        else:
            super().run(s)

# ---- as source

def key_text(k):
    return k[1] if isinstance(k, tuple) and k[0] == 'word' else text(k)

def sort_text(e, top):
    if e[1] is None and isinstance(e[3][0], tuple) and e[3][0][0] in ('keys', 'values', '%'):
        return f'(sort {items(e[3])})'
    return _sort_text(e, top)

_sort_text = var.MORE['sort']
var.MORE.update({
    '%': lambda e, top: '%' + e[1],
    'keys': lambda e, top: f'keys(%{e[1]})',
    'count': lambda e, top: f'scalar(keys(%{e[1]}))',
    'values': lambda e, top: f'values(%{e[1]})',
    '=>': lambda e, top: f'{e[1]} => {text(e[2])}',
    'hel': lambda e, top: f'${e[1]}{{{key_text(e[2])}}}',
    'exists': lambda e, top: f'exists(${e[1]}{{{key_text(e[2])}}})',
    'delete': lambda e, top: f'delete(${e[1]}{{{key_text(e[2])}}})',
    'sethel': lambda e, top: (lambda s: s if top else f'({s})')(f'${e[2]}{{{key_text(e[3])}}} {e[1]} {text(e[4], False)}'),
    'stephel': lambda e, top: (lambda s: s if top else f'({s})')(f'{e[1]}${e[3]}{{{key_text(e[4])}}}' if e[2] else f'${e[3]}{{{key_text(e[4])}}}{e[1]}'),
    'sort': sort_text,
})

_source = each.source

def source(s, depth=0):
    pad = '    ' * depth
    if s[0] == 'myh':
        return [f'{pad}my %{s[1]};' if s[2] is None else f'{pad}my %{s[1]} = ({items(s[2])});']
    if s[0] == 'seth':
        return [f'{pad}%{s[1]} = ({items(s[2])});']
    return _source(s, depth)

each.source = source
it.source = source

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

def quiet(setup, candidates):
    """The candidates that do not fault after the setup, in order."""
    return [c for c in candidates if output(setup + [c])[1] is None]

# ---- the cases

shown = var.shown

def gone(e):
    """What a delete gave, said once: it is not worked out twice."""
    return say_(('//', e, 'undef'))

def dumph(name):
    """A statement that prints a hash: its count, and each key and value,
    by key: the order a hash keeps is not perl's to agree with."""
    value = ('?:', ('call', 'defined', [('hel', name, IT)]), ('hel', name, IT), 'undef')
    return say_(join(('count', name), ':', jn(',', mp([srt([('keys', name)])], join('<', IT, '=', value, '>')))))

# Every word perl has a meaning of its own for, of a kind each.
WORDS = ['name', 'true', 'false', 'undef', 'if', 'my', 'sub', 'print', 'say', 'q', 'qq', 's', 'y', 'm', 'tr', 'x', 'and', 'or', 'not', 'lt', 'eq', 'cmp',
         'time', 'shift', 'keys', 'exists', 'delete', 'defined', 'length', 'sort', 'map', 'v65', '_x', 'a1', 'A', 'return', 'last', 'for']
# Every kind of value a key may be made from, with a string of its own.
KEYS = [0, 1, -7, 41, 2**53, 0.5, 3.0, -0.0, 1.5e300, 1e21, 0.1, 1 / 3, '', '0', 'ab', ' 3 ', '00', '3.0', '1e3', 'a b', "it's", '5', '-5', TRUE, FALSE]

def literal_cases():
    c = Cases(0)
    # A word before `=>`, and alone in braces, is its text.
    def words(f, g, G):
        h = g('h')
        s = [myh(h, *[pair(w, n) for n, w in enumerate(WORDS)]), dumph(h)]
        for w in WORDS:
            s += [say_(hel(h, w)), say_(('exists', h, W(w)))]
        s += [myh(g('e')), dumph(g('e')), ('myh', g('n'), None), dumph(g('n')),
              myh(g('one'), pair('only', 1)), dumph(g('one'))]
        return s
    c.case(words)
    # A key is a string, as `.` makes one: of every kind, as a literal's
    # item, held in a variable and worked out.
    def kinds(f, g, G):
        h, k = g('h'), g('k')
        s = [('myh', h, None), ('my', k, 0)]
        for n, v in enumerate(KEYS):
            s += [do(set_(k, v)), do(sethel(h, G('k'), n)), say_(('exists', h, ('.', G('k'), '')))]
        s += [dumph(h)]
        lit = [x for n, v in enumerate(KEYS) for x in (v, n)]
        s += [myh(g('l'), *lit), dumph(g('l')), say_(('==', ('keys', h), ('keys', g('l'))))]
        s += [myh(g('c'), ('+', 1, 1), 'two', ('.', 'a', 'b'), 'ab', ('*', 0.5, 4), 'again', ('call', 'length', ['abc']), 'three'), dumph(g('c'))]
        return s
    c.case(kinds)
    # A key given twice: the last value. A list of lists, an array, a hash.
    def lists_(f, g, G):
        h, a, o = g('h'), g('a'), g('o')
        return [myh(h, pair('a', 1), pair('b', 2), pair('a', 3), 'b', 4, pair('c', 5)), dumph(h),
                mya(a, 'p', 1, 'q', 2), myh(o, A(a)), dumph(o), seth(o, A(a), A(a)), dumph(o),
                seth(o, ('list', [pair('x', 1), ('list', [pair('y', 2)])]), pair('z', 3)), dumph(o),
                seth(o, H(h), pair('d', 6)), dumph(o), seth(o, H(o), pair('a', 9)), dumph(o), seth(o), dumph(o),
                seth(o, ('..', 1, 6)), dumph(o), seth(o, ('xl', [pair('r', 1)], 3)), dumph(o),
                seth(o, pair('u', UNDEF), pair('t', TRUE), pair('f', FALSE), pair('n', 1.5)), dumph(o)]
    c.case(lists_)
    return c.out

def element_cases():
    c = Cases(0)
    VALUES = [0, 1, -7, 0.5, 3.0, '', '0', 'ab', '00', ' 3 ', TRUE, FALSE, UNDEF]
    # Reading: what is there, what is not, and nothing is made.
    def reading(f, g, G):
        h, k = g('h'), g('k')
        s = [myh(h, *[x for n, v in enumerate(VALUES) for x in (f'k{n}', v)]), dumph(h)]
        for n in range(len(VALUES)):
            s += [shown(hel(h, f'k{n}')), shown(('hel', h, f'k{n}')), say_(('call', 'defined', [hel(h, f'k{n}')]))]
        s += [shown(hel(h, 'nope')), say_(('call', 'defined', [hel(h, 'nope')])), shown(('//', hel(h, 'nope'), 'dflt')),
              ('my', k, 'k1'), shown(hel(h, G('k'))), shown(hel(h, ('.', 'k', 2))), shown(hel(h, ('.', G('k'), 0))),
              ('my', g('v'), hel(h, 'zz')), sayl(hel(h, 'k1'), hel(h, 'k7'), hel(h, 'k1')), dumph(h)]
        return s
    c.case(reading)
    # Storing, and every operator that reads and stores, on what is there
    # and on what is not.
    def storing(f, g, G):
        h = g('h')
        s = [myh(h, pair('n', 5), pair('s', 'ab'), pair('u', UNDEF), pair('z', 0), pair('e', ''))]
        tries = []
        for key in ('n', 's', 'u', 'z', 'e', 'new'):
            for op, v in (('=', 7), ('+=', 2), ('-=', 2), ('*=', 3), ('.=', 'x'), ('x=', 2), ('//=', 9), ('||=', 8), ('&&=', 6), ('**=', 2), ('/=', 2), ('%=', 3)):
                tries.append(block(myh('t', H(h)), say_(sethel('t', key if key != 'new' else f'new{len(tries)}', v, op)), dumph('t')))
            for op in ('++', '--'):
                for before in (True, False):
                    tries.append(block(myh('t', H(h)), say_(stephel('t', key, op, before)), dumph('t')))
        return s + quiet(s, tries) + [dumph(h)]
    c.case(storing)
    # The orders (D80): the value, then the key, then the store; for an
    # operator that reads, the key first.
    def orders(f, g, G):
        h, i = g('h'), g('i')
        return [('myh', h, None), ('my', i, 'a'),
                do(sethel(h, G('i'), set_(i, 'b'))), dumph(h), say_(G('i')),
                seth(h), do(set_(i, 'a')), do(sethel(h, G('i'), set_(i, 'b'), '.=')), dumph(h),
                seth(h, pair('a', 1)), do(set_(i, 'a')), do(sethel(h, G('i'), set_(i, 5), '+=')), dumph(h),
                seth(h), do(sethel(h, 'p', sethel(h, 'q', 4))), dumph(h),
                seth(h, pair('n', 1)), do(sethel(h, 'm', ('+', hel(h, 'n'), 1))), do(sethel(h, 'n', ('+', hel(h, 'm'), hel(h, 'n')))), dumph(h)]
    c.case(orders)
    return c.out

def whole_cases():
    c = Cases(0)
    def exists_delete(f, g, G):
        h, k = g('h'), g('k')
        return [myh(h, pair('a', 1), pair('u', UNDEF), pair('z', 0), pair('e', ''), 1, 'one'), ('my', k, 'a'),
                say_(('exists', h, W('a'))), say_(('exists', h, W('u'))), say_(('exists', h, W('nope'))), say_(('exists', h, G('k'))),
                say_(('exists', h, 1)), say_(('exists', h, ('.', G('k'), 'x'))), say_(('!', ('exists', h, W('nope')))),
                say_(('?:', ('exists', h, W('z')), 'has z', 'no z')), say_(('&&', ('exists', h, W('a')), ('exists', h, W('e')))),
                ('if', [(('exists', h, W('nope')), [say_('wrong')]), (('exists', h, W('u')), [say_('u is there')])], None), dumph(h),
                gone(('delete', h, W('a'))), gone(('delete', h, W('a'))), gone(('delete', h, W('u'))), gone(('delete', h, W('nope'))),
                say_(('exists', h, W('a'))), dumph(h), ('my', g('d'), ('delete', h, 1)), say_(G('d')), do(('delete', h, W('z'))), dumph(h),
                do(sethel(h, 'a', 'back')), say_(('+', ('call', 'length', [('delete', h, W('a'))]), 1)), dumph(h),
                do(('delete', h, W('e'))), dumph(h), gone(('delete', h, W('e')))]
    c.case(exists_delete)
    def counts(f, g, G):
        h, e, n = g('h'), g('e'), g('n')
        return [myh(h, pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4)), ('myh', e, None),
                say_(('+', ('keys', h), 0)), ('my', n, H(h)), say_(G('n')), ('my', g('m'), ('keys', h)), say_(G('m')),
                ('my', g('z'), H(e)), say_(G('z')),
                ('if', [(H(h), [say_('some')])], [say_('none')]), ('if', [(H(e), [say_('some')])], [say_('none')]),
                ('if', [(('keys', e), [say_('keys')])], [say_('no keys')]), ('if', [(('values', h), [say_('values')])], None),
                say_(('+', ('keys', h), ('values', h))), say_(('==', ('keys', h), 4)), say_(('.', 'n', ('keys', h))),
                do(('delete', h, W('a'))), ('my', g('after'), H(h)), say_(G('after')),
                do(sethel(h, 'a', 9)), do(sethel(h, 'a', 10)), ('my', g('again'), H(h)), say_(G('again')),
                say_(jn(',', srt([('keys', h)]))), say_(jn(',', srt([('values', h)], NUM))), say_(jn(',', srt([H(h)]))),
                say_(jn(',', rev(srt([('keys', h)])))), say_(jn(',', mp([srt([('keys', h)])], ('x', IT, 2))))]
    c.case(counts)
    def copies(f, g, G):
        h, o, a = g('h'), g('o'), g('a')
        return [myh(h, pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4)), myh(o, H(h)), do(sethel(o, 'a', 9)), do(sethel(o, 'z', 0)),
                do(('delete', o, W('b'))), dumph(h), dumph(o), seth(o, H(h)), dumph(o), seth(h, H(h)), dumph(h),
                seth(h, H(h), pair('e', 5)), dumph(h), seth(h, pair('first', 0), H(h)), dumph(h),
                ('mya', a, [srt([H(h)])]), say_(('scalar', a)), ('mya', g('k'), [srt([('keys', h)])]), dump(g('k')),
                ('mya', g('v'), [srt([('values', h)], NUM)]), dump(g('v')),
                sub(f('size'), [req('n')], returns(('*', D('n'), 2))), say_(ucall(f('size'), ('+', ('keys', h), 0))), say_(ucall(f('size'), ('+', H(h), 0))),
                sub(f('made'), [], myh('t', pair('p', 1), pair('q', 2)), returns(H('t'))), myh(g('r'), ucall(f('made'))), dumph(g('r')),
                sub(f('twice'), [], myh('t', pair('p', 1)), do(sethel('t', 'q', 2)), returns(('keys', 't'))),
                ('mya', g('tw'), [ucall(f('twice'))]), say_(jn(',', srt([A(g('tw'))]))),
                block(myh('t', pair('in', 1)), dumph('t'), block(myh('t', pair('deeper', 2)), dumph('t')), dumph('t')),
                ('my', g('i'), 0), ('while', None, ('<', G('i'), 3), [myh('t', pair('k', G('i'))), do(sethel('t', ('.', 'x', G('i')), 1)), dumph('t'), do(step(g('i')))])]
    c.case(copies)
    return c.out

D = lambda n: ('$', n)

SAME = {'1500': ('hash-literals-and-keys', literal_cases), '1501': ('hash-elements', element_cases), '1502': ('hash-exists-delete-counts', whole_cases)}

def faults():
    out = {}
    n = [1510]
    def fault(name, near, far, subs_=()):
        out[str(n[0])] = ('fault-hash-' + name, list(subs_), near, far)
        n[0] += 1
    h4 = lambda: myh('h', pair('a', 1), pair('b', 2), pair('c', 3), pair('d', 4))
    # An odd list for a hash.
    fault('odd-list', block(myh('h', 1, 2), dumph('h')), block(myh('h', 1, 2, 3), dumph('h')))
    fault('odd-list-assigned', block(h4(), seth('h', pair('a', 1), pair('b', 2)), dumph('h')), block(h4(), seth('h', pair('a', 1), 'b'), dumph('h')))
    fault('odd-list-of-one', block(('myh', 'h', None), seth('h'), dumph('h')), block(('myh', 'h', None), seth('h', 'a'), dumph('h')))
    fault('odd-list-from-an-array', block(mya('a', 1, 2), myh('h', A('a')), dumph('h')), block(mya('a', 1, 2, 3), myh('h', A('a')), dumph('h')))
    fault('odd-list-from-a-hash-and-one', block(h4(), myh('g', H('h'), 'e', 5), dumph('g')), block(h4(), myh('g', H('h'), 'e'), dumph('g')))
    # An undef key.
    both = lambda make, good, bad: (block(h4(), *good, make()), block(h4(), *bad, make()))
    fault('undef-key-read', *both(lambda: shown(hel('h', D('k'))), [('my', 'k', '')], [('my', 'k', None)]))
    fault('undef-key-stored', *both(lambda: do(sethel('h', D('k'), 1)), [('my', 'k', 0)], [('my', 'k', None)]))
    fault('undef-key-worked-on', *both(lambda: do(sethel('h', D('k'), 1, '+=')), [('my', 'k', FALSE)], [('my', 'k', None)]))
    fault('undef-key-stepped', *both(lambda: do(stephel('h', D('k'))), [('my', 'k', 'a')], [('my', 'k', None)]))
    fault('undef-key-exists', *both(lambda: say_(('exists', 'h', D('k'))), [('my', 'k', 'a')], [('my', 'k', None)]))
    fault('undef-key-deleted', *both(lambda: do(('delete', 'h', D('k'))), [('my', 'k', 'a')], [('my', 'k', None)]))
    fault('undef-key-in-a-list', block(myh('g', '', 1), dumph('g')), block(myh('g', UNDEF, 1), dumph('g')))
    # D36: a whole Num from 10^15 is no string, so no key.
    fault('whole-num-key', *both(lambda: do(sethel('h', D('k'), 1)), [('my', 'k', 999999999999999.0)], [('my', 'k', 1e15)]))
    fault('whole-num-key-read', *both(lambda: shown(hel('h', D('k'))), [('my', 'k', 1e16)], [('my', 'k', 2.0**53 - 1)]))
    fault('whole-num-key-in-a-list', block(myh('g', 0.5, 1), dumph('g')), block(myh('g', 1e15, 1), dumph('g')))
    # What is not there is undef, and an undef is no number and no string.
    fault('missing-as-a-number', block(h4(), say_(('+', hel('h', 'a'), 1))), block(h4(), say_(('+', hel('h', 'nope'), 1))))
    fault('missing-as-a-string', block(h4(), say_(('.', hel('h', 'a'), '!'))), block(h4(), say_(('.', hel('h', 'nope'), '!'))))
    fault('deleted-as-a-string', block(h4(), say_(('.', ('delete', 'h', W('a')), '!'))), block(h4(), do(('delete', 'h', W('a'))), say_(('.', ('delete', 'h', W('a')), '!'))))
    # An operator that reads and stores makes the key, and then faults.
    fault('string-stepped', block(h4(), do(sethel('h', 'a', 2, '*=')), dumph('h')), block(h4(), do(sethel('h', 'a', 'x')), do(sethel('h', 'a', 2, '*=')), dumph('h')))
    # D18: a hash after return, reached for one value.
    fault('returned-for-one-value', block(('mya', 'r', [ucall('f')]), say_(('scalar', 'r'))), ('my', 'x', ucall('f')), [myh('g', pair('a', 1)), sub('f', [], returns(H('g')))])
    fault('keys-returned-for-one-value', block(('mya', 'r', [ucall('f')]), say_(('scalar', 'r'))), ('my', 'x', ucall('f')), [myh('g', pair('a', 1)), sub('f', [], returns(('keys', 'g')))])
    return out

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/hash.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/hash.py {n} > t/{n}-{name}.expected\n'
                   for n, name in sorted([(n, SAME[n][0]) for n in SAME] + [(n, FAULTS[n][0]) for n in FAULTS]))

def program(statements, header):
    text_lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in text_lines)

def main(argv):
    sys.setrecursionlimit(20000)
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/hash.py']
    if number in SAME:
        cases = SAME[number][1]()
        for c in cases:
            assert output(c)[1] is None, (number, output(c)[1], output(c)[0][-200:])
        statements = [s for c in cases for s in c]
        out.write((program(statements, model) if want_program else output(statements)[0]).encode())
        return
    name, the_subs, near, far = FAULTS[number]
    path = f't/{number}-{name}.pl'
    header = ['kind: fault'] + model
    statements = the_subs + [('say', 1), near, far, ('say', 2)]
    if want_program:
        out.write(program(statements, header).encode())
        return
    printed, fault, at = output(statements)
    assert fault is not None and output(the_subs + [('say', 1), near])[1] is None, (number, printed, fault)
    found = {}
    it.lines_(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])
