#!/usr/bin/env python3
"""t/410 to t/449: arrays and lists (step 9a; D76, D78 to D80).

The definition, which is all this file knows of the language beyond
t/models/sub.py (subs, and through it loops, variables, values and
operators).

  my @a;   my @a = LIST;   @a = LIST;     an array, and its own name
  (1, (2, 3), @a, 4 .. 6)                 a list: it flattens
  $a[I]                                   an element
  scalar(@a)   $#a                        how many; the last index, -1 for none
  my ($p, $q) = LIST;   ($p, $a[0], @rest) = LIST;      list assignment
  push @a, LIST   unshift   pop(@a)   shift(@a)   splice(@a, O, L, LIST)
  @a[LIST]   (LIST)[LIST]                 slices
  (LIST) x N                              a list, N times
  say LIST;                               each value, nothing between

**A list is a row of values, copied as it is built** (D76). An array in a
list is its elements; a range is its whole numbers, each end cut toward
zero; a call is its value, or nothing if the sub returned nothing (D79).
**Where one value is wanted an array is its count** (T21, T150).

An index is a whole number by `substr`'s rule. A read past either end is
undef and makes nothing. A store past the end makes the array longer, the
gap undef; before the start it is a fault.

The order (D80), which is perl's:
  $a[I] = V        V, then I, then the store
  $a[I] OP= V      I; the target is made (the array grows to hold it, or
  $a[I]++          it is the fault for before the start); then V; then
                   the element is read, worked on and stored
  (T, ...) = LIST  LIST, then every target's index, then the stores
  (LIST)[I]        I, then LIST
  @a[I]            I, then the elements

A list assignment gives each target a value, undef when they run out; an
array, the last target, takes the rest. `push` and `unshift` give the new
count; `pop` and `shift` give undef from an empty array. `splice` removes
LENGTH elements at OFFSET (to the end, with no LENGTH; a negative OFFSET
from the end; a negative LENGTH leaves that many at the end), puts LIST
there, and gives what it removed. An OFFSET past the end, or before the
start, is a fault.

A slice gives undef for an index past either end; a slice of a list with
no values is empty (T164). `(LIST) x N` goes by the count rule of `x`.

A file's array is empty as the program starts, and its `my` stores nothing
(T156).

This model works a program out; it does not refuse one. D76's refusal, of
an expression or a list in which a later part can change what an earlier
part names, is the compiler's, and no case here is such a program.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

410 is arrays made, copied, counted and indexed, at and past each end. 411
is every way an element is stored, and the order. 412 is lists: what
flattens, ranges, slices, the list repeat. 413 is list assignment. 414 is
push, pop, shift, unshift and splice at their edges. 415 is arrays and
subs: flattening into parameters and defaults, the file's arrays, a sub's
own. 416 is a count wherever one value is wanted. 417 is a value with no
past, through an element. 420 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/list.py --program 410 > t/410-arrays.pl
    python3 t/models/list.py 410 > t/410-arrays.expected
    python3 t/models/list.py --program 411 > t/411-elements.pl
    python3 t/models/list.py 411 > t/411-elements.expected
    python3 t/models/list.py --program 412 > t/412-lists.pl
    python3 t/models/list.py 412 > t/412-lists.expected
    python3 t/models/list.py --program 413 > t/413-list-assignment.pl
    python3 t/models/list.py 413 > t/413-list-assignment.expected
    python3 t/models/list.py --program 414 > t/414-push-pop-splice.pl
    python3 t/models/list.py 414 > t/414-push-pop-splice.expected
    python3 t/models/list.py --program 415 > t/415-arrays-and-subs.pl
    python3 t/models/list.py 415 > t/415-arrays-and-subs.expected
    python3 t/models/list.py --program 416 > t/416-counts.pl
    python3 t/models/list.py 416 > t/416-counts.expected
    python3 t/models/list.py --program 417 > t/417-through-an-element.pl
    python3 t/models/list.py 417 > t/417-through-an-element.expected
    python3 t/models/list.py --program 420 > t/420-fault-store-before-the-start.pl
    python3 t/models/list.py 420 > t/420-fault-store-before-the-start.expected
    python3 t/models/list.py --program 421 > t/421-fault-step-before-the-start.pl
    python3 t/models/list.py 421 > t/421-fault-step-before-the-start.expected
    python3 t/models/list.py --program 422 > t/422-fault-target-before-the-right-side.pl
    python3 t/models/list.py 422 > t/422-fault-target-before-the-right-side.expected
    python3 t/models/list.py --program 423 > t/423-fault-index-undef.pl
    python3 t/models/list.py 423 > t/423-fault-index-undef.expected
    python3 t/models/list.py --program 424 > t/424-fault-index-not-a-number.pl
    python3 t/models/list.py 424 > t/424-fault-index-not-a-number.expected
    python3 t/models/list.py --program 425 > t/425-fault-index-too-large.pl
    python3 t/models/list.py 425 > t/425-fault-index-too-large.expected
    python3 t/models/list.py --program 426 > t/426-fault-element-undef.pl
    python3 t/models/list.py 426 > t/426-fault-element-undef.expected
    python3 t/models/list.py --program 427 > t/427-fault-splice-past-the-end.pl
    python3 t/models/list.py 427 > t/427-fault-splice-past-the-end.expected
    python3 t/models/list.py --program 428 > t/428-fault-splice-before-the-start.pl
    python3 t/models/list.py 428 > t/428-fault-splice-before-the-start.expected
    python3 t/models/list.py --program 429 > t/429-fault-splice-length-too-large.pl
    python3 t/models/list.py 429 > t/429-fault-splice-length-too-large.expected
    python3 t/models/list.py --program 430 > t/430-fault-range-of-strings.pl
    python3 t/models/list.py 430 > t/430-fault-range-of-strings.expected
    python3 t/models/list.py --program 431 > t/431-fault-range-undef.pl
    python3 t/models/list.py 431 > t/431-fault-range-undef.expected
    python3 t/models/list.py --program 432 > t/432-fault-repeat-negative.pl
    python3 t/models/list.py 432 > t/432-fault-repeat-negative.expected
    python3 t/models/list.py --program 433 > t/433-fault-say-undef-in-a-list.pl
    python3 t/models/list.py 433 > t/433-fault-say-undef-in-a-list.expected
    python3 t/models/list.py --program 434 > t/434-fault-too-many-flattened.pl
    python3 t/models/list.py 434 > t/434-fault-too-many-flattened.expected
    python3 t/models/list.py --program 435 > t/435-fault-too-few-flattened.pl
    python3 t/models/list.py 435 > t/435-fault-too-few-flattened.expected
    python3 t/models/list.py --program 436 > t/436-fault-popped-undef.pl
    python3 t/models/list.py 436 > t/436-fault-popped-undef.expected
    python3 t/models/list.py --program 437 > t/437-fault-slice-index.pl
    python3 t/models/list.py 437 > t/437-fault-slice-index.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import loop
import sub as subs
from var import Fault, MIN, MAX, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import ABSENT, VOID, SCALAR, LIST, ucall, sub, req, opt, ret, say_, named, lines, source as sub_source

BEFORE = 'an element before the start of the array'
SPLICE_PAST = 'splice past the end of the array'
SPLICE_BEFORE = 'splice before the start of the array'
RANGE_STRING = 'a string as the end of a range'

class Arr:
    def __init__(self, items=()):
        self.items = list(items)

# What is a list wherever it stands, and so is flattened.
LISTY = ('@', 'list', '..', 'slice', 'lslice', 'xl', 'splice')

# The expressions: ('@', name), an array; ('elem', name, i); ('last',
# name), `$#name`; ('scalar', name); ('list', [items]); ('..', a, b);
# ('slice', name, [indexes]); ('lslice', [items], [indexes]); ('xl',
# [items], n); ('pop' or 'shift', name); ('push' or 'unshift', name,
# [items]); ('splice', name, [arguments]); ('setel', op, name, i, e);
# ('stepel', op, before, name, i). The statements: ('mya', name, items or
# None); ('seta', name, [items]); ('lassign', my, [targets], [items]) with
# a target ('$', name), ('elem', name, i), ('@', name) or None for
# `undef`; ('sayl', [items]).
class Run(subs.Program):
    def __init__(self, statements):
        super().__init__(statements)
        # The file's arrays are there, empty, before anything runs (T156).
        for s in statements:
            if s[0] == 'mya':
                self.scopes[0]['@' + s[1]] = Arr()
            if s[0] == 'lassign' and s[1]:
                for t in s[2]:
                    if t is not None and t[0] == '@':
                        self.scopes[0]['@' + t[1]] = Arr()
                    elif t is not None:
                        self.scopes[0][t[1]] = var.Place()
                        self.scopes[0][t[1]].value = UNDEF

    def arr(self, name):
        for scope in reversed(self.scopes):
            if '@' + name in scope:
                return scope['@' + name]
        raise AssertionError(f'@{name} is not declared')

    def index(self, e):
        """An index, worked out: a whole number, or a fault."""
        return self.whole_of(get(self.ev(e)))

    def where(self, a, i):
        """Where index i is in a, or None for past either end."""
        n = len(a.items)
        j = i + n if i < 0 else i
        return j if 0 <= j < n else None

    def target(self, a, i):
        """Index i of a, made: the array grows to hold it."""
        n = len(a.items)
        j = i + n if i < 0 else i
        if j < 0:
            raise Fault(BEFORE)
        a.items += [UNDEF] * (j + 1 - n)
        return j

    def evl(self, e):
        """An expression where a list is wanted: its values."""
        kind = e[0] if isinstance(e, tuple) else None
        if kind == '@':
            return list(self.arr(e[1]).items)
        if kind == 'list':
            return [v for item in e[1] for v in self.evl(item)]
        if kind == '..':
            ends = []
            for end in (e[1], e[2]):
                v = get(self.ev(end))
                if strings.is_str(v):
                    raise Fault(RANGE_STRING)
                ends.append(self.whole_of(v))
            assert ends[1] - ends[0] < 100000, 'a range too long for a test'
            return list(range(ends[0], ends[1] + 1))
        if kind == 'slice':
            indexes = [self.whole_of(v) for item in e[2] for v in self.evl(item)]
            a = self.arr(e[1])
            return [UNDEF if self.where(a, i) is None else a.items[self.where(a, i)] for i in indexes]
        if kind == 'lslice':
            indexes = [self.whole_of(v) for item in e[2] for v in self.evl(item)]
            values = [v for item in e[1] for v in self.evl(item)]
            if not values:
                return []
            a = Arr(values)
            return [UNDEF if self.where(a, i) is None else values[self.where(a, i)] for i in indexes]
        if kind == 'xl':
            values = [v for item in e[1] for v in self.evl(item)]
            n = get(self.ev(e[2]))
            return values * len(logic.value(('x', '.', n)))
        if kind == 'splice':
            return self.splice(e)
        if kind == '?:':
            return self.evl(e[2] if logic.truth(get(self.ev(e[1]))) else e[3])
        if isinstance(e, tuple) and len(e) == 3 and (kind in var.LAZY or kind == '//'):
            left = get(self.ev(e[1]))
            wanted = left is UNDEF if kind == '//' else logic.truth(left) == var.LAZY[kind]
            return self.evl(e[2]) if wanted else [left]
        if kind == '+' and len(e) == 2:
            return self.evl(e[1])
        self.ctx = LIST
        v = get(self.ev(e))
        return [] if v is ABSENT else [v]

    def whole_of(self, v):
        """A whole number by `substr`'s rule for a position."""
        n = logic.number_of(v)
        return strings.whole(n)

    def splice(self, e):
        a = self.arr(e[1])
        args = e[2]
        n = len(a.items)
        offset = self.index(args[0]) if args else 0
        length = self.index(args[1]) if len(args) > 1 else None
        new = [v for item in args[2:] for v in self.evl(item)]
        start = offset + n if offset < 0 else offset
        if start < 0:
            raise Fault(SPLICE_BEFORE)
        if start > n:
            raise Fault(SPLICE_PAST)
        if length is None:
            end = n
        elif length < 0:
            end = max(start, n + length)
        else:
            end = min(n, start + length)
        removed = a.items[start:end]
        a.items[start:end] = new
        return removed

    def ev(self, e):
        if not isinstance(e, tuple):
            return super().ev(e)
        kind = e[0]
        if kind == 'ucall':
            want, self.ctx = self.ctx, SCALAR
            results = []
            for a in e[2]:
                if isinstance(a, tuple) and a[0] in LISTY:
                    results += self.evl(a)
                    continue
                self.ctx = LIST
                r = self.ev(a)
                if r is not ABSENT:
                    results.append(r)
            value = self.call(e[1], results, want)
            self.ctx = SCALAR
            return value
        if kind not in ('@', 'elem', 'last', 'scalar', 'pop', 'shift', 'push', 'unshift', 'setel', 'stepel', 'lslice'):
            return super().ev(e)
        self.ctx = SCALAR
        if kind in ('@', 'scalar'):
            return len(self.arr(e[1]).items)
        if kind == 'last':
            return len(self.arr(e[1]).items) - 1
        if kind == 'elem':
            i = self.index(e[2])
            a = self.arr(e[1])
            return UNDEF if self.where(a, i) is None else a.items[self.where(a, i)]
        if kind == 'lslice':
            # One index, where one value is wanted: that element.
            values = self.evl(e)
            return values[0] if values else UNDEF
        if kind in ('pop', 'shift'):
            a = self.arr(e[1])
            if not a.items:
                return UNDEF
            return a.items.pop() if kind == 'pop' else a.items.pop(0)
        if kind in ('push', 'unshift'):
            new = [v for item in e[2] for v in self.evl(item)]
            a = self.arr(e[1])
            a.items[:] = a.items + new if kind == 'push' else new + a.items
            return len(a.items)
        if kind == 'stepel':
            _, op, before, name, index = e
            a = self.arr(name)
            j = self.target(a, self.index(index))
            old = a.items[j]
            a.items[j] = var.step(op, old)
            return a.items[j] if before else 0 if old is UNDEF and op == '++' else old
        _, op, name, index, right = e
        a = self.arr(name)
        if op == '=':
            r = self.ev(right)          # its calls run; a variable is read at the store
            j = self.target(a, self.index(index))
            a.items[j] = get(r)
            return a.items[j]
        j = self.target(a, self.index(index))
        if op in ('||=', '&&=', '//='):
            old = a.items[j]
            if old is UNDEF if op == '//=' else logic.truth(old) == (op == '&&='):
                a.items[j] = get(self.ev(right))
            return a.items[j]
        r = get(self.ev(right))
        left = a.items[j]
        if left is UNDEF and op in ('+=', '-=', '.='):
            left = '' if op == '.=' else 0
        a.items[j] = logic.value((op[:-1], left, r))
        return a.items[j]

    def run(self, s):
        kind = s[0]
        if kind == 'mya':
            self.mark(s)
            values = None if s[2] is None else [v for item in s[2] for v in self.evl(item)]
            if self.top():
                a = self.scopes[0]['@' + s[1]]      # its `my` stores nothing (T156)
            else:
                a = self.scopes[-1]['@' + s[1]] = Arr()
            if values is not None:
                a.items[:] = values
        elif kind == 'seta':
            self.mark(s)
            values = [v for item in s[2] for v in self.evl(item)]
            self.arr(s[1]).items[:] = values
        elif kind == 'lassign':
            self.mark(s)
            _, declares, targets, items = s
            values = [v for item in items for v in self.evl(item)]
            if declares and not self.top():
                for t in targets:
                    if t is not None and t[0] == '@':
                        self.scopes[-1]['@' + t[1]] = Arr()
                    elif t is not None:
                        self.scopes[-1][t[1]] = var.Place()
                        self.scopes[-1][t[1]].value = UNDEF
            # Every target's index, and then the stores.
            places = []
            for t in targets:
                if t is not None and t[0] == 'elem':
                    a = self.arr(t[1])
                    places.append((a, self.index(t[2])))
                else:
                    places.append(None)
            for t, place in zip(targets, places):
                if t is None:
                    values = values[1:]
                elif t[0] == '@':
                    self.arr(t[1]).items[:] = values
                    values = []
                else:
                    v = values[0] if values else UNDEF
                    values = values[1:]
                    if place is None:
                        self.place(t[1]).value = v
                    else:
                        a, i = place
                        a.items[self.target(a, i)] = v
        elif kind == 'do' and isinstance(s[1], tuple) and s[1][0] == 'splice':
            self.mark(s)
            self.splice(s[1])
        elif kind == 'sayl':
            self.mark(s)
            values = [v for item in s[1] for v in self.evl(item)]
            self.out += ''.join(logic.printed(v) for v in values) + '\n'
        else:
            super().run(s)

    def mark(self, s):
        self.at = id(s)

def items(es):
    return ', '.join(element(e) for e in es)

def element(e):
    """An item of a list, as source: a list operator's own brackets do."""
    return text(e, isinstance(e, tuple) and e[0] in ('ucall', 'elem', '@', 'last', 'scalar', 'list', 'slice', 'lslice', 'pop', 'shift', 'push', 'unshift', 'splice', 'call', '$'))

MORE = {
    '@': lambda e, top: '@' + e[1],
    'elem': lambda e, top: f'${e[1]}[{text(e[2])}]',
    'last': lambda e, top: '$#' + e[1],
    'scalar': lambda e, top: f'scalar(@{e[1]})',
    'list': lambda e, top: f'({items(e[1])})',
    '..': lambda e, top: (lambda s: s if top else f'({s})')(f'{text(e[1], False)} .. {text(e[2], False)}'),
    'slice': lambda e, top: f'@{e[1]}[{items(e[2])}]',
    'lslice': lambda e, top: f'({items(e[1])})[{items(e[2])}]',
    'xl': lambda e, top: (lambda s: s if top else f'({s})')(f'({items(e[1])}) x {text(e[2], False)}'),
    'pop': lambda e, top: f'pop(@{e[1]})',
    'shift': lambda e, top: f'shift(@{e[1]})',
    'push': lambda e, top: f'push(@{e[1]}, {items(e[2])})',
    'unshift': lambda e, top: f'unshift(@{e[1]}, {items(e[2])})',
    'splice': lambda e, top: f'splice(@{e[1]}{"".join(", " + element(a) for a in e[2])})',
    'setel': lambda e, top: (lambda s: s if top else f'({s})')(f'${e[2]}[{text(e[3])}] {e[1]} {text(e[4], False)}'),
    'stepel': lambda e, top: (lambda s: s if top else f'({s})')(f'{e[1]}${e[3]}[{text(e[4])}]' if e[2] else f'${e[3]}[{text(e[4])}]{e[1]}'),
    'ucall': lambda e, top: f'{e[1]}({items(e[2])})',
}
var.MORE.update(MORE)

def target(t):
    return 'undef' if t is None else text(t)

def source(s, depth=0):
    pad = '    ' * depth
    kind = s[0]
    inner = lambda statements: [line for t in statements for line in source(t, depth + 1)]
    label = lambda name: '' if name is None else name + ': '
    if kind == 'mya':
        return [f'{pad}my @{s[1]};' if s[2] is None else f'{pad}my @{s[1]} = ({items(s[2])});']
    if kind == 'seta':
        return [f'{pad}@{s[1]} = ({items(s[2])});']
    if kind == 'lassign':
        return [f'{pad}{"my " if s[1] else ""}({", ".join(target(t) for t in s[2])}) = ({items(s[3])});']
    if kind == 'sayl':
        return [f'{pad}say({items(s[1])});']
    # The statements that hold statements, laid out here so that those
    # inside them are.
    if kind == 'sub':
        return [f'{pad}sub {s[1]}({", ".join(subs.parameter(p) for p in s[2])}) {{'] + inner(s[3]) + [pad + '}']
    if kind in ('while', 'until'):
        return [f'{pad}{label(s[1])}{kind} ({text(s[2])}) {{'] + inner(s[3]) + [pad + '}']
    if kind == 'for':
        return [sub_source(('for',) + tuple(s[1:5]) + ([],), depth)[0]] + inner(s[5]) + [pad + '}']
    if kind == 'block':
        return [pad + '{'] + inner(s[1]) + [pad + '}']
    if kind == 'if':
        out = []
        for n, (test, statements) in enumerate(s[1]):
            out += [f'{pad}{"if" if n == 0 else "} elsif"} ({text(test)}) {{'] + inner(statements)
        if s[2] is not None:
            out += [pad + '} else {'] + inner(s[2])
        return out + [pad + '}']
    if kind == 'unless':
        return [f'{pad}unless ({text(s[1])}) {{'] + inner(s[2]) + [pad + '}']
    if kind == 'mod':
        return [source(s[1], depth)[0][:-1] + f' {s[2]} {text(s[3])};']
    return sub_source(s, depth)

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

# ---- the cases. As in sub.py: a case is statements at the top level, and
# every name in it ends in the case's number.

shown = var.shown
P, Q, R, I = (('$', name) for name in 'pqri')

def A(name):
    return ('@', name)

def el(name, i):
    return ('elem', name, i)

def lst(*es):
    return ('list', list(es))

def mya(name, *es):
    return ('mya', name, list(es))

def seta(name, *es):
    return ('seta', name, list(es))

def sayl(*es):
    return ('sayl', list(es))

def setel(name, i, e, op='='):
    return ('setel', op, name, i, e)

def dump(name):
    """A statement that prints an array: its count, and each element."""
    v = ('$', 'dump_i')
    piece = ('?:', ('call', 'defined', [el(name, v)]), join('<', el(name, v), '>'), '<undef>')
    return block(('my', 'dump_i', 0), ('my', 'dump_s', ''),
                 ('while', None, ('<', v, A(name)), [do(set_('dump_s', piece, '.=')), do(step('dump_i'))]),
                 say_(join(('scalar', name), ':', ('$', 'dump_s'))))

VALUES = [0, 1, -7, 0.5, 3.0, '', '0', 'ab', ' 3 ', TRUE, FALSE, UNDEF]

class Cases:
    def __init__(self, first):
        self.k = first
        self.out = []

    def case(self, make):
        self.k += 1
        self.out.append(make(*named(self.k)))

def array_cases():
    c = Cases(0)
    # Made, with each kind of value; copied; an empty one; one value.
    c.case(lambda f, g, G: [mya(g('a'), *VALUES), dump(g('a')), mya(g('b'), A(g('a'))), do(setel(g('b'), 0, 9)), dump(g('b')), say_(el(g('a'), 0)),
                            ('mya', g('e'), None), dump(g('e')), mya(g('one'), 5), dump(g('one')), mya(g('none')), dump(g('none')),
                            seta(g('a'), 1, 2), dump(g('a')), seta(g('a')), dump(g('a')), seta(g('a'), UNDEF), dump(g('a')),
                            mya(g('t'), 1, 2, 3), seta(g('t'), A(g('t')), 4), dump(g('t')), seta(g('t'), A(g('t')), A(g('t'))), dump(g('t'))])
    # Indexes: at each end, past each, negative, fractional, strings,
    # booleans; and a read makes nothing.
    def indexes(f, g, G):
        a = g('a')
        s = [mya(a, 10, 20, 30)]
        for i in (0, 1, 2, 3, 4, -1, -2, -3, -4, -5, 1.9, -1.9, 0.5, -0.5, '2', ' 1 ', '-1', TRUE, FALSE, 1e0, MAX, MIN, 2**31, -2**31, 2**40):
            s.append(shown(el(a, i)))
        s += [dump(a), say_(('last', a)), say_(('scalar', a)), ('mya', g('e'), None), say_(('last', g('e'))), shown(el(g('e'), 0)), shown(el(g('e'), -1)), dump(g('e'))]
        s += [('my', g('i'), 1), say_(el(a, G('i'))), say_(el(a, ('+', G('i'), 1))), say_(el(a, ('last', a))), say_(el(a, ('-', A(a), 1))), shown(el(a, A(a))),
              say_(el(a, ('-', el(a, 0), 9)))]
        return s
    c.case(indexes)
    return c.out

def element_cases():
    c = Cases(100)
    # A store at each end and past it; the gap is undef; a negative index.
    def stores(f, g, G):
        a = g('a')
        s = [mya(a, 1, 2, 3)]
        for i, v in ((0, 'z'), (2, 'l'), (3, 'n'), (6, 'far'), (-1, 'm1'), (-7, 'first'), (1.9, 'frac'), ('2', 'str')):
            s += [do(setel(a, i, v)), dump(a)]
        s += [('mya', g('e'), None), do(setel(g('e'), 2, 1)), dump(g('e')), ('mya', g('z'), None), do(setel(g('z'), 0, UNDEF)), dump(g('z'))]
        return s
    c.case(stores)
    # Every assigning operator and step on an element; on one that is
    # undef; on one past the end, which is made.
    def works(f, g, G):
        a = g('a')
        s = [mya(a, 5, 'ab', 0, UNDEF)]
        for op, i, v in (('+=', 0, 2), ('-=', 0, 1), ('*=', 0, 3), ('/=', 0, 2), ('%=', 0, 5), ('**=', 0, 2), ('.=', 1, 'c'), ('x=', 1, 2),
                         ('||=', 2, 'was false'), ('||=', 2, 'not now'), ('&&=', 2, 'was true'), ('//=', 3, 'was undef'), ('//=', 3, 'not now'),
                         ('+=', 5, 1), ('.=', 6, 's'), ('-=', 7, 1), ('//=', 9, 'made'), ('&&=', 11, 'not stored'), ('||=', 12, 'stored')):
            s += [do(setel(a, i, v, op)), dump(a)]
        for op in ('++', '--'):
            for before in (True, False):
                s += [say_(('stepel', op, before, a, 0)), do(('stepel', op, before, a, 14)), dump(a)]
        return s
    c.case(works)
    # The order: `=` works out its right side, then its index; the others
    # their index first. And an element is a value where it stands.
    def order(f, g, G):
        a, i = g('a'), g('i')
        Iv = G('i')
        return [mya(a, 1, 2, 3), ('my', i, 0),
                do(setel(a, Iv, set_(i, 2))), dump(a), say_(Iv),
                seta(a, 1, 2, 3), do(set_(i, 0)), do(setel(a, Iv, set_(i, 2), '+=')), dump(a),
                seta(a, 1, 2, 3), do(set_(i, 0)), do(setel(a, Iv, set_(i, 2), '.=')), dump(a),
                seta(a, 0, 2, 3), do(set_(i, 0)), do(setel(a, Iv, set_(i, 2), '||=')), dump(a),
                seta(a, 7, 7, 7), do(set_(i, 0)), do(setel(a, step(i), Iv)), dump(a),
                seta(a, 10, 20, 30), do(set_(i, 0)), say_(('+', el(a, step(i)), el(a, step(i)))), say_(Iv),
                do(set_(i, 0)), do(setel(a, Iv, el(a, step(i, '++', True)))), dump(a),
                do(set_(i, 1)), do(setel(a, Iv, ('+', el(a, ('-', Iv, 1)), el(a, Iv)))), dump(a),
                do(setel(a, 0, el(a, 2))), do(setel(a, A(a), 'at the count')), dump(a),
                ('my', g('v'), setel(a, 1, 'value of a store')), say_(G('v')), ('my', g('w'), setel(a, 0, 5, '+=')), say_(G('w'))]
    c.case(order)
    return c.out

def list_cases():
    c = Cases(200)
    # What flattens: lists in lists, arrays, empty ones, a comma after
    # the last.
    def flat(f, g, G):
        a, b, e = g('a'), g('b'), g('e')
        return [mya(a, 1, 2), mya(b, 'x'), ('mya', e, None),
                mya(g('c'), 0, lst(1, lst(2, 3)), A(a), A(e), A(b), lst(), 9), dump(g('c')),
                mya(g('d'), lst(lst(lst(7)))), dump(g('d')), mya(g('h'), A(e), A(e)), dump(g('h')),
                sayl(1, 2, 3), sayl(A(a)), sayl('x', A(a), 'y'), sayl(A(e)), sayl(A(a), A(a)), sayl(lst(A(a), 5), ':', ('scalar', a)),
                sayl(el(a, 0), '-', el(a, 1))]
    c.case(flat)
    # Ranges: each end at each kind of whole and fractional number, a
    # boolean; nothing when the first is past the second.
    def ranges(f, g, G):
        r = g('r')
        s = [('mya', r, None), ('my', g('n'), 3)]
        for lo, hi in ((1, 5), (3, 1), (0, 0), (-2, 2), (1.9, 4.1), (-1.9, 1.9), (FALSE, TRUE), (1, G('n')), (('-', G('n'), 1), ('*', G('n'), 2)),
                       (MAX - 1, MAX), (MIN, MIN + 1), (5, 4), (2.0, 4.0), (-0.0, 1)):
            s += [seta(r, ('..', lo, hi)), dump(r)]
        s += [seta(r, 0, ('..', 2, 3), ('..', 7, 8)), dump(r), sayl(('..', 1, 9)), seta(r, ('..', 1, A(r))), dump(r), seta(r, ('..', 0, ('last', r))), dump(r)]
        return s
    c.case(ranges)
    # Slices of an array and of a list: in order, repeated, negative, past
    # either end, by an array and a range of indexes; an empty list's is
    # empty.
    def slices(f, g, G):
        a, s_, i, e = g('a'), g('s'), g('i'), g('e')
        s = [mya(a, 10, 20, 30, 40), ('mya', s_, None), mya(i, 0, 2), ('mya', e, None)]
        for idx in ([1, 2], [('..', 1, 3)], [-1, 0], [5, 1], [A(i)], [0, 0, 0], [-5, -4], [3, 2, 1, 0], [A(e)], [1.9, '2'], [A(i), ('..', 0, 1)], [lst(0)], [0, lst(1, 2)]):
            s += [seta(s_, ('slice', a, idx)), dump(s_)]
        for its, idx in (([10, 20, 30], [1]), ([10, 20, 30], [0, 2]), ([A(a), 9], [4]), ([('..', 1, 5)], [-1]), ([A(a)], [9, 10]), ([A(a)], [1, 9]),
                         ([A(e)], [0, 1]), ([A(e)], [0]), ([], [0, 1]), ([1, 2, 3], [5, 6]), ([1, 2, 3], [5]), ([A(a)], [A(i)])):
            s += [seta(s_, ('lslice', its, idx)), dump(s_)]
        s += [say_(('lslice', [10, 20, 30], [1])), say_(('+', ('lslice', [A(a)], [-1]), 1)), shown(('lslice', [A(e)], [0])), shown(('lslice', [A(a)], [9]))]
        return s
    c.case(slices)
    # A list, N times.
    def repeats(f, g, G):
        r, a = g('r'), g('a')
        s = [('mya', r, None), mya(a, 1, 2)]
        for its, n in (([0], 3), ([1, 2], 2), ([A(a)], 2), (['a'], 0), ([A(a), 'x'], 1), ([], 3), ([5], 2.9), ([5], '2'), ([5], TRUE), ([5], FALSE), ([('..', 1, 3)], 2)):
            s += [seta(r, ('xl', its, n)), dump(r)]
        s += [seta(r, ('x', 'ab', 2)), dump(r), sayl(('xl', ['-'], 5)), seta(r, ('xl', [0], A(a))), dump(r)]
        return s
    c.case(repeats)
    return c.out

def assign_cases():
    c = Cases(300)
    def shapes(f, g, G):
        p, q, r, a = g('p'), g('q'), g('r'), g('a')
        show = lambda: say_(join(logic.shown(G('p')), ' ', logic.shown(G('q')), ' ', logic.shown(G('r'))))
        s = [('lassign', True, [('$', p), ('$', q), ('$', r)], [1, 2, 3]), show()]
        for its in ([1, 2], [1], [], [1, 2, 3, 4], [lst(7, 8), 9], [('..', 4, 9)]):
            s += [('lassign', False, [('$', p), ('$', q), ('$', r)], its), show()]
        s += [mya(a, 'x', 'y', 'z', 'w'),
              ('lassign', False, [('$', p), ('$', q), ('$', r)], [A(a)]), show(),
              ('lassign', False, [('$', p), None, ('$', r)], [A(a)]), show(),
              ('lassign', False, [None, None, ('$', r)], [1, 2]), show(),
              ('lassign', False, [('$', p)], [A(a)]), show(),
              ('lassign', False, [('$', p), A(a)], [1, 2, 3]), show(), dump(a),
              ('lassign', False, [('$', p), A(a)], [1]), show(), dump(a),
              ('lassign', False, [A(a)], [5, 6]), dump(a),
              ('lassign', True, [('$', g('m')), A(g('rest'))], [A(a), 7]), say_(G('m')), dump(g('rest')),
              ('lassign', True, [('$', g('only'))], [9]), say_(G('only')),
              ('lassign', True, [None, ('$', g('second'))], [1, 2]), say_(G('second')),
              ('lassign', True, [('$', g('u')), ('$', g('w'))], []), shown(G('u'))]
        return s
    c.case(shapes)
    # The right side is worked out first: swaps, of variables and of
    # elements, a rotation, an array among its own values.
    def swaps(f, g, G):
        p, q, a = g('p'), g('q'), g('a')
        return [('lassign', True, [('$', p), ('$', q)], [1, 2]),
                ('lassign', False, [('$', p), ('$', q)], [G('q'), G('p')]), say_(join(G('p'), ' ', G('q'))),
                ('lassign', False, [('$', p), ('$', q)], [G('q'), ('+', G('p'), G('q'))]), say_(join(G('p'), ' ', G('q'))),
                mya(a, 1, 2, 3),
                ('lassign', False, [el(a, 0), el(a, 2)], [el(a, 2), el(a, 0)]), dump(a),
                ('lassign', False, [el(a, 0), el(a, 1), el(a, 2)], [el(a, 1), el(a, 2), el(a, 0)]), dump(a),
                ('lassign', False, [('$', p), A(a)], [A(a), G('p')]), say_(G('p')), dump(a),
                ('lassign', False, [el(a, 0), A(a)], [9, 8, 7]), dump(a),
                ('lassign', False, [el(a, 5), ('$', p)], [1]), dump(a), shown(G('p')),
                ('lassign', False, [el(a, -1), el(a, 0)], ['last', 'first']), dump(a),
                seta(a, ('slice', a, [1, 0])), dump(a)]
    c.case(swaps)
    # Every target's index before any store.
    def indexes(f, g, G):
        a, i = g('a'), g('i')
        return [mya(a, 1, 2, 3), ('my', i, 0),
                ('lassign', False, [('$', i), el(a, G('i'))], [1, 5]), dump(a), say_(G('i')),
                seta(a, 1, 2, 3), do(set_(i, 0)),
                ('lassign', False, [el(a, G('i')), ('$', i)], [5, 1]), dump(a), say_(G('i')),
                seta(a, 1, 2, 3), do(set_(i, 0)),
                ('lassign', False, [el(a, step(i)), el(a, step(i))], ['x', 'y']), dump(a)]
    c.case(indexes)
    return c.out

def builtin_cases():
    c = Cases(400)
    def pushes(f, g, G):
        a, b = g('a'), g('b')
        return [('mya', a, None), say_(('push', a, [1, 2])), say_(('push', a, [3])), dump(a),
                say_(('pop', a)), say_(('shift', a)), dump(a), say_(('pop', a)), shown(('pop', a)), shown(('shift', a)), dump(a),
                say_(('unshift', a, [5, 6])), dump(a), mya(b, 7, 8), do(('push', a, [A(b), 9])), dump(a),
                do(('push', a, [A(a)])), dump(a), do(('unshift', a, [A(b), lst(0, 0)])), dump(a),
                say_(('-', ('pop', a), ('pop', a))), say_(('.', ('shift', a), ('shift', a))), dump(a),
                do(('push', a, [('..', 1, 3), ('xl', ['r'], 2), ('slice', b, [1, 0])])), dump(a),
                do(('push', a, [lst()])), dump(a),
                do(('push', a, [UNDEF])), dump(a), do(('push', a, [('scalar', a)])), dump(a),
                ('my', g('n'), ('+', ('push', a, [0]), 1)), say_(G('n')),
                ('while', None, A(a), [do(('pop', a))]), dump(a),
                do(('push', a, [1, 2, 3])), do(('push', a, [('shift', a)])), dump(a), do(('unshift', a, [('pop', a)])), dump(a)]
    c.case(pushes)
    def splices(f, g, G):
        a, r = g('a'), g('r')
        s = [('mya', a, None), ('mya', r, None)]
        for args in ([1, 2], [2], [1, 0, 7, 8], [-1], [0, -1], [], [0], [6], [6, 0], [3, 1], [0, 99], [1, -9], [-6, 2], [2, 2, 'x'], [2, 0, lst(1, 2), 'y'],
                     [1.9, 1.9], ['1', '2'], [0, 0], [-2, -1, 'z'], [5, 1, 'at the end'], [0, 6, lst()], [TRUE, TRUE]):
            s += [seta(a, 0, 1, 2, 3, 4, 5), seta(r, ('splice', a, args)), dump(r), dump(a)]
        s += [seta(a, 1, 2, 3), do(('splice', a, [1, 1])), dump(a), seta(a, 1, 2, 3), seta(r, ('splice', a, [0, 1, A(a)])), dump(a),
              seta(a, 1, 2, 3), sayl(('splice', a, [0, 2])), dump(a), ('mya', g('e'), None), seta(r, ('splice', g('e'), [])), dump(r), seta(r, ('splice', g('e'), [0, 0, 1])), dump(g('e'))]
        return s
    c.case(splices)
    return c.out

def sub_cases():
    c = Cases(500)
    # An array flattens into the parameters, with what is beside it; too
    # few are made up by defaults.
    def flatten(f, g, G):
        a, e = g('a'), g('e')
        three = sub(f('three'), [req('p'), req('q'), req('r')], ret(join(P, Q, R)))
        cnt = sub(f('cnt'), [opt('p', '-'), opt('q', '-'), opt('r', '-')], ret(join(logic.shown(P), logic.shown(Q), logic.shown(R))))
        none = sub(f('none'), [], ret())
        return [three, cnt, none, mya(a, 1, 2), ('mya', e, None),
                say_(ucall(f('three'), A(a), 3)), say_(ucall(f('three'), 0, A(a))), say_(ucall(f('three'), A(e), 1, A(a))),
                say_(ucall(f('cnt'), A(e))), say_(ucall(f('cnt'), A(a))), say_(ucall(f('cnt'), A(a), 9)),
                say_(ucall(f('cnt'), ('lslice', [A(a)], [0]))), say_(ucall(f('cnt'), ('lslice', [A(e)], [0]))), say_(ucall(f('cnt'), lst())),
                say_(ucall(f('cnt'), lst(), 1)), say_(ucall(f('cnt'), ('..', 1, 3))), say_(ucall(f('cnt'), ('slice', a, [1, 0]))), say_(ucall(f('cnt'), ('xl', ['r'], 2))),
                say_(ucall(f('cnt'), el(a, 0), el(a, 5))), say_(ucall(f('cnt'), ('scalar', a), ('last', a))), say_(ucall(f('cnt'), ucall(f('none')), A(a))),
                say_(ucall(f('cnt'), UNDEF, A(e), UNDEF)),
                # No value in a list (D79).
                mya(g('c'), ucall(f('none'))), dump(g('c')), mya(g('d'), 1, ucall(f('none')), 2), dump(g('d')),
                ('lassign', True, [('$', g('y')), ('$', g('z'))], [ucall(f('none')), 7]), say_(G('y')), shown(G('z')),
                do(('push', a, [ucall(f('none'))])), dump(a), sayl('[', ucall(f('none')), ']'),
                mya(g('one'), ucall(f('three'), 1, 2, 3)), dump(g('one')), mya(g('two'), ucall(f('three'), 1, 2, 3), ucall(f('cnt'))), dump(g('two'))]
    c.case(flatten)
    # The file's arrays, from subs; a sub's own, new at each call; a call
    # before the `my` (T156).
    def files(f, g, G):
        a, b, m = g('a'), g('b'), g('m')
        return [do(ucall(f('fill'))), ('mya', a, None), dump(a), mya(b, 9), dump(b),
                do(ucall(f('fill'))), ('lassign', True, [('$', g('n')), A(m)], []), dump(m),
                sub(f('fill'), [], do(('push', a, [1, 2])), do(('push', b, [3])), do(('push', m, [4]))),
                sub(f('own'), [req('p')], ('mya', 'mine', None), do(('push', 'mine', [P])), ('mod', do(ucall(f('own'), ('-', P, 1))), 'if', ('>', P, 0)),
                    do(('push', 'mine', ['after'])), say_(join(('scalar', 'mine'), ':', el('mine', 0), el('mine', 1)))),
                do(ucall(f('own'), 2)),
                sub(f('total'), [], ('my', 't', 0), ('my', 'i', 0), ('while', None, ('<', ('$', 'i'), A(a)), [do(set_('t', el(a, ('$', 'i')), '+=')), do(step('i'))]), ret(('$', 't'))),
                say_(ucall(f('total'))), do(setel(a, 0, 100)), say_(ucall(f('total'))),
                sub(f('set'), [req('p'), req('q')], do(setel(a, P, Q))), do(ucall(f('set'), 5, 1)), dump(a),
                sub(f('len'), [], ret(('scalar', a))), say_(ucall(f('len')))]
    c.case(files)
    return c.out

def count_cases():
    c = Cases(600)
    def counts(f, g, G):
        a, e, n = g('a'), g('e'), g('n')
        Aa, Ae = A(a), A(e)
        s = [mya(a, 4, 5, 6), ('mya', e, None), ('my', n, Aa), say_(G('n')), do(set_(n, Ae)), say_(G('n'))]
        for x in (('.', 'x', Aa), ('-', Aa), ('+', Aa, 1), ('*', Aa, 2), ('**', Aa, 2), ('%', Aa, 2), ('call', 'uc', [Aa]), ('==', Aa, 3), ('<', Aa, 5), ('!', Aa), ('!', Ae),
                  ('?:', Aa, 'some', 'none'), ('?:', Ae, 'some', 'none'), ('x', '-', Aa), ('x', Aa, 2), ('.', Aa, ''), ('.', Aa, Ae), ('==', Aa, Ae), ('-', Aa, 1),
                  ('||', Ae, 7), ('&&', Aa, 't'), ('//', Aa, 1), ('call', 'substr', ['abcdef', Aa]), ('+', ('last', a), 1), ('-', ('scalar', a), ('last', a)),
                  ('<=>', Aa, Ae), ('eq', Aa, '3'), ('+', ('+', Aa), 0)):
            s.append(shown(x))
        s += [do(set_(n, 0)), do(set_(n, Aa, '+=')), do(set_(n, Aa, '.=')), say_(G('n')), do(set_(n, ('?:', Aa, Aa, 0))), say_(G('n')),
              ('if', [(Aa, [say_('if')])], None), ('unless', Ae, [say_('unless')]), ('mod', say_('mod'), 'if', ('>', Aa, 2)),
              ('while', None, ('>', Aa, 1), [do(('pop', a))]), dump(a), ('until', None, ('>=', Aa, 3), [do(('push', a, [0]))]), dump(a),
              # `@a || LIST` is the count (T150), and `@e || LIST` the list.
              mya(g('f'), ('||', Aa, lst(9))), dump(g('f')), mya(g('d'), ('||', Ae, lst(1, 2))), dump(g('d')),
              mya(g('h'), ('?:', Aa, Aa, Ae)), dump(g('h')), mya(g('k'), ('&&', Aa, Ae)), dump(g('k')), mya(g('m'), ('&&', Aa, lst(1, 2))), dump(g('m')),
              say_(el(a, ('-', Aa, 1))), ('lassign', True, [('$', g('first'))], [Aa]), say_(G('first')),
              mya(g('idx'), 1), say_(el(a, A(g('idx'))))]
        return s
    c.case(counts)
    return c.out

def through_cases():
    """sub.py's `through`, with each operand kept in an element and read
    back, popped and shifted."""
    out = []
    V, W = ('$', 'v'), ('$', 'w')
    ops = [(op, V, W) for op in ('+', '-', '*', '/', '%', '**', '.', 'x', '==', '<', '<=>', 'eq', 'lt', 'cmp', '&&', '||', '//')]
    ops += [('-', V), ('!', V), ('call', 'length', [V]), ('call', 'uc', [V]), ('?:', V, W, V), ('call', 'index', [V, W])]
    for n, e in enumerate(ops):
        f, g, G = named(700 + n)
        a = g('a')
        quiet = [pair for pair in loop.PAIRS if output([('block', [('my', 'v', pair[0]), ('my', 'w', pair[1]), shown(e)])])[1] is None]
        pairs = quiet[::max(1, len(quiet) // 8)][:8]
        case = [('mya', a, None)]
        for x, y in pairs:
            case.append(('block', [seta(a, x, y), ('my', 'v', el(a, 0)), ('my', 'w', el(a, 1)), shown(e),
                                   do(('push', a, [x, y])), do(set_('w', ('pop', a))), do(set_('v', ('pop', a))), shown(e),
                                   ('lassign', False, [('$', 'v'), ('$', 'w')], [('slice', a, [0, 1])]), shown(e)]))
        out.append(case)
    return out

SAME = {'410': ('arrays', array_cases), '411': ('elements', element_cases), '412': ('lists', list_cases), '413': ('list-assignment', assign_cases),
        '414': ('push-pop-splice', builtin_cases), '415': ('arrays-and-subs', sub_cases), '416': ('counts', count_cases), '417': ('through-an-element', through_cases)}

# number: (name, the subs, a near case that prints, the one that faults)
def faults():
    a3 = mya('a', 1, 2, 3)
    loud = sub('loud', [req('p')], say_(P), ret(P))
    two = sub('two', [req('p'), req('q')], ret(join(P, ',', Q)))
    return {
        '420': ('fault-store-before-the-start', [], block(a3, do(setel('a', -3, 'first')), say_(el('a', 0))), block(a3, do(setel('a', -4, 'x')))),
        '421': ('fault-step-before-the-start', [], block(a3, do(('stepel', '++', False, 'a', -3)), shown(el('a', -4))), block(a3, do(('stepel', '++', False, 'a', -4)))),
        # An assigning operator makes its target before its right side
        # runs: the fault comes first, and `loud` is not heard (T160).
        '422': ('fault-target-before-the-right-side', [loud], block(a3, do(setel('a', 0, ucall('loud', 'heard'), '.=')), say_(el('a', 0))),
                block(a3, do(setel('a', -4, ucall('loud', 'not heard'), '.=')))),
        '423': ('fault-index-undef', [], block(a3, ('my', 'u', 1), say_(el('a', ('$', 'u')))), block(a3, ('my', 'u', None), say_(el('a', ('$', 'u'))))),
        # (By a variable: perl warns as it compiles of an index written as
        # a string that is no number, and that is a refusal.)
        '424': ('fault-index-not-a-number', [], block(a3, ('my', 'i', '2'), say_(el('a', ('$', 'i')))), block(a3, ('my', 'i', 'x'), say_(el('a', ('$', 'i'))))),
        '425': ('fault-index-too-large', [], block(a3, shown(el('a', MAX))), block(a3, shown(el('a', 1e30)))),
        '426': ('fault-element-undef', [], block(a3, say_(('+', el('a', 2), 1))), block(a3, say_(('+', el('a', 3), 1)))),
        '427': ('fault-splice-past-the-end', [], block(a3, do(('splice', 'a', [3, 0, 9])), say_(el('a', 3))), block(a3, do(('splice', 'a', [4, 0, 9])))),
        '428': ('fault-splice-before-the-start', [], block(a3, do(('splice', 'a', [-3, 1])), say_(el('a', 0))), block(a3, do(('splice', 'a', [-4, 1])))),
        '429': ('fault-splice-length-too-large', [], block(a3, do(('splice', 'a', [0, MAX])), say_(('scalar', 'a'))), block(a3, do(('splice', 'a', [0, 1e30])))),
        '430': ('fault-range-of-strings', [], block(('mya', 'r', [('..', 1, 3)]), say_(('scalar', 'r'))), block(('mya', 'r', [('..', '1', '3')]))),
        '431': ('fault-range-undef', [], block(('my', 'u', 2), ('mya', 'r', [('..', 1, ('$', 'u'))]), say_(('scalar', 'r'))), block(('my', 'u', None), ('mya', 'r', [('..', 1, ('$', 'u'))]))),
        '432': ('fault-repeat-negative', [], block(('mya', 'r', [('xl', [1, 2], 0)]), say_(('scalar', 'r'))), block(('mya', 'r', [('xl', [1, 2], -1)]))),
        '433': ('fault-say-undef-in-a-list', [], block(a3, sayl(A('a'), '!')), block(a3, do(setel('a', 4, 5)), sayl('before', A('a')))),
        '434': ('fault-too-many-flattened', [two, loud], block(mya('a', 1, 2), say_(ucall('two', A('a')))), block(a3, say_(ucall('two', ucall('loud', 'ran'), A('a'))))),
        '435': ('fault-too-few-flattened', [two], block(mya('a', 1), say_(ucall('two', A('a'), 2))), block(('mya', 'a', None), say_(ucall('two', A('a'), 2)))),
        '436': ('fault-popped-undef', [], block(mya('a', 1), say_(('+', ('pop', 'a'), 1))), block(mya('a', 1), do(('pop', 'a')), say_(('+', ('pop', 'a'), 1)))),
        '437': ('fault-slice-index', [], block(a3, mya('s', ('slice', 'a', [0, '1'])), say_(('scalar', 's'))), block(a3, mya('s', ('slice', 'a', [0, 'one'])))),
    }

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/list.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/list.py {n} > t/{n}-{name}.expected\n'
                   for n, name in sorted([(n, SAME[n][0]) for n in SAME] + [(n, FAULTS[n][0]) for n in FAULTS]))

def program(statements, header):
    text_lines = [line for s in statements for line in source(s)]
    return ''.join(f'# {h}\n' for h in header) + 'use v5.42;\n' + strings.OPEN + ''.join(line + '\n' for line in text_lines)

def main(argv):
    sys.setrecursionlimit(20000)
    if argv == ['--commands']:
        sys.stdout.write(commands())
        return
    assert commands() in __doc__, 'the commands in the docstring are not the tests: python3 t/models/list.py --commands'
    want_program = argv[0] == '--program'
    number = argv[-1]
    out = sys.stdout.buffer
    model = ['model: t/models/list.py']
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
    lines(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])
