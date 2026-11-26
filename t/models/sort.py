#!/usr/bin/env python3
"""t/1200 to t/1249: sort (step 10c; D82, D83, D84, D87).

The definition, which is all this file knows of the language beyond
t/models/it.py (`$_`, map, grep) and t/models/merge.py (perl's merge).

  sort LIST                   by string, as `cmp` orders
  sort { ...; EXPR } LIST     by the block: `$a` and `$b` are two of the
                              values, and EXPR below zero, zero or above
                              says which comes first

**Which pairs are compared, and in what order, is perl's**: the merge of
t/models/merge.py, which is perl's own, asked for a pair at a time. So a
block that counts or prints, and one that is no consistent order, show
here what they show there (D82). The sort is stable.

The list is worked out once and copied, as a `map`'s is; every array
named in it is frozen while the sort runs; an element or a slice past the
end of its array in it is a fault (T188). `$a` and `$b` are values, new
for each comparison, read-only.

**The block's value** is a whole number by the rule an index has (a
fraction is cut toward zero, an undef or a string that is no number is a
fault), and a fault outside 32 bits, where perl wraps it (T173).

**With no block every value is made a string before anything is
compared**, so an undef is a fault whatever the list holds. With a block
a list of none or of one runs it not at all; but for the four blocks
perl throws away, `$a <=> $b`, `$b <=> $a`, `$a cmp $b` and `$b cmp $a`,
a lone value is compared with itself, since perl turns it to a number or
a string all the same (T190).

**`@a = sort { ... } @a;` with an undef in `@a` is a fault** (T187): perl
sorts that in place and drops an element that was never stored, which is
a past of the array's that is not kept.

After `return`, a sort is list-shaped (D18). (Where one value is wanted
the compiler refuses it: D84.)

This model works a program out; it does not refuse one.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

1200 is sorts of every kind, in every place. 1201 is the order of the
comparisons, by blocks that log them. 1210 on each fault once.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/sort.py --program 1200 > t/1200-sort.pl
    python3 t/models/sort.py 1200 > t/1200-sort.expected
    python3 t/models/sort.py --program 1201 > t/1201-sort-order.pl
    python3 t/models/sort.py 1201 > t/1201-sort-order.expected
    python3 t/models/sort.py --program 1210 > t/1210-fault-frozen-sort-store.pl
    python3 t/models/sort.py 1210 > t/1210-fault-frozen-sort-store.expected
    python3 t/models/sort.py --program 1211 > t/1211-fault-frozen-sort-push.pl
    python3 t/models/sort.py 1211 > t/1211-fault-frozen-sort-push.expected
    python3 t/models/sort.py --program 1212 > t/1212-fault-frozen-sort-assign.pl
    python3 t/models/sort.py 1212 > t/1212-fault-frozen-sort-assign.expected
    python3 t/models/sort.py --program 1213 > t/1213-fault-frozen-sort-from-a-sub.pl
    python3 t/models/sort.py 1213 > t/1213-fault-frozen-sort-from-a-sub.expected
    python3 t/models/sort.py --program 1214 > t/1214-fault-given-back-after-a-sort.pl
    python3 t/models/sort.py 1214 > t/1214-fault-given-back-after-a-sort.expected
    python3 t/models/sort.py --program 1215 > t/1215-fault-sort-names-by-second-of-two.pl
    python3 t/models/sort.py 1215 > t/1215-fault-sort-names-by-second-of-two.expected
    python3 t/models/sort.py --program 1216 > t/1216-fault-sort-names-by-slice.pl
    python3 t/models/sort.py 1216 > t/1216-fault-sort-names-by-slice.expected
    python3 t/models/sort.py --program 1217 > t/1217-fault-sort-names-by-reverse.pl
    python3 t/models/sort.py 1217 > t/1217-fault-sort-names-by-reverse.expected
    python3 t/models/sort.py --program 1218 > t/1218-fault-sort-names-by-a-map-of-it.pl
    python3 t/models/sort.py 1218 > t/1218-fault-sort-names-by-a-map-of-it.expected
    python3 t/models/sort.py --program 1219 > t/1219-fault-element-past-the-end-in-a-sort.pl
    python3 t/models/sort.py 1219 > t/1219-fault-element-past-the-end-in-a-sort.expected
    python3 t/models/sort.py --program 1220 > t/1220-fault-slice-past-the-end-in-a-sort.pl
    python3 t/models/sort.py 1220 > t/1220-fault-slice-past-the-end-in-a-sort.expected
    python3 t/models/sort.py --program 1221 > t/1221-fault-slice-past-the-end-in-a-sort-with-no-block.pl
    python3 t/models/sort.py 1221 > t/1221-fault-slice-past-the-end-in-a-sort-with-no-block.expected
    python3 t/models/sort.py --program 1222 > t/1222-fault-sort-block-gives-undef.pl
    python3 t/models/sort.py 1222 > t/1222-fault-sort-block-gives-undef.expected
    python3 t/models/sort.py --program 1223 > t/1223-fault-sort-block-gives-a-string-that-is-no-number.pl
    python3 t/models/sort.py 1223 > t/1223-fault-sort-block-gives-a-string-that-is-no-number.expected
    python3 t/models/sort.py --program 1224 > t/1224-fault-sort-block-gives-past-32-bits.pl
    python3 t/models/sort.py 1224 > t/1224-fault-sort-block-gives-past-32-bits.expected
    python3 t/models/sort.py --program 1225 > t/1225-fault-sort-block-gives-below-32-bits.pl
    python3 t/models/sort.py 1225 > t/1225-fault-sort-block-gives-below-32-bits.expected
    python3 t/models/sort.py --program 1226 > t/1226-fault-sort-block-gives-a-number-outside-the-integers.pl
    python3 t/models/sort.py 1226 > t/1226-fault-sort-block-gives-a-number-outside-the-integers.expected
    python3 t/models/sort.py --program 1227 > t/1227-fault-sort-of-an-undef.pl
    python3 t/models/sort.py 1227 > t/1227-fault-sort-of-an-undef.expected
    python3 t/models/sort.py --program 1228 > t/1228-fault-sort-of-one-undef.pl
    python3 t/models/sort.py 1228 > t/1228-fault-sort-of-one-undef.expected
    python3 t/models/sort.py --program 1229 > t/1229-fault-sort-of-one-string-by-number.pl
    python3 t/models/sort.py 1229 > t/1229-fault-sort-of-one-string-by-number.expected
    python3 t/models/sort.py --program 1230 > t/1230-fault-sort-of-one-undef-by-string.pl
    python3 t/models/sort.py 1230 > t/1230-fault-sort-of-one-undef-by-string.expected
    python3 t/models/sort.py --program 1231 > t/1231-fault-sort-of-strings-by-number.pl
    python3 t/models/sort.py 1231 > t/1231-fault-sort-of-strings-by-number.expected
    python3 t/models/sort.py --program 1232 > t/1232-fault-undef-in-an-array-sorted-in-place.pl
    python3 t/models/sort.py 1232 > t/1232-fault-undef-in-an-array-sorted-in-place.expected
    python3 t/models/sort.py --program 1233 > t/1233-fault-undef-in-an-array-sorted-in-place-through-brackets.pl
    python3 t/models/sort.py 1233 > t/1233-fault-undef-in-an-array-sorted-in-place-through-brackets.expected
    python3 t/models/sort.py --program 1234 > t/1234-fault-sort-returned-for-one-value.pl
    python3 t/models/sort.py 1234 > t/1234-fault-sort-returned-for-one-value.expected
    python3 t/models/sort.py --program 1235 > t/1235-fault-in-a-sort-block.pl
    python3 t/models/sort.py 1235 > t/1235-fault-in-a-sort-block.expected
"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import loop
import list as lists
import each
import ret
import it
import merge
from var import Fault, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join
from sub import SCALAR, ucall, sub, req, opt, say_, named
from sub import ret as returns
from list import A, el, lst, mya, seta, sayl, setel, dump, Cases, Arr, items, element
from each import each as over
from ret import jn, rev, slurp
from it import IT, forit, formod, mp, gr

WIDE = "a sort block's value is outside 32 bits, where perl wraps it"
IN_PLACE = 'an undef in an array sorted in place: perl drops an element that was never stored'
VA, VB = ('$', 'a'), ('$', 'b')

lists.LISTY = lists.LISTY + ('sort',)
_shaped = ret.shaped
ret.shaped = lambda e: (isinstance(e, tuple) and e[0] == 'sort') or _shaped(e)

def srt(its, *body):
    """sort: with a block, its statements, the last an expression; with
    none, by string."""
    return ('sort', list(body[:-1]), body[-1], list(its)) if body else ('sort', None, None, list(its))

def thrown_away(e):
    """Whether a block is one of the four perl compares without (T190)."""
    return e[1] == [] and e[2] in (('<=>', VA, VB), ('<=>', VB, VA), ('cmp', VA, VB), ('cmp', VB, VA))

def bare(e):
    """An item behind brackets of its own."""
    while isinstance(e, tuple) and e[0] == 'list' and len(e[1]) == 1:
        e = e[1][0]
    return e

class Run(it.Run):
    def sorter(self, e):
        _, body, last, its = e
        for item in its:
            self.strict(item)
        values = [v for item in its for v in self.evl(item)]
        frozen = [self.arr(n) for n in dict.fromkeys(each.names(('list', its), []))]
        for a in frozen:
            a.frozen += 1
        at = self.at
        try:
            if body is None:
                for v in values:
                    logic.value(('.', v, ''))
                compare = lambda x, y: logic.value(('cmp', x, y))
            else:
                def compare(x, y):
                    self.scopes.append({'a': var.Place(), 'b': var.Place()})
                    self.scopes[-1]['a'].value = x
                    self.scopes[-1]['b'].value = y
                    try:
                        for s in body:
                            self.run(s)
                        self.at = at
                        n = self.whole_of(get(self.ev(last)))
                    finally:
                        self.scopes.pop()
                    if not -2 ** 31 <= n < 2 ** 31:
                        raise Fault(WIDE)
                    return n
                if len(values) == 1 and thrown_away(e):
                    compare(values[0], values[0])
            asking = merge.merge(len(values))
            try:
                pair = next(asking)
                while True:
                    pair = asking.send(compare(values[pair[0]], values[pair[1]]))
            except StopIteration as done:
                return [values[i] for i in done.value]
        finally:
            for a in frozen:
                a.frozen -= 1

    def evl(self, e):
        if isinstance(e, tuple) and e[0] == 'sort':
            return self.sorter(e)
        return super().evl(e)

    def run(self, s):
        if s[0] == 'seta' and len(s[2]) == 1:
            e = bare(s[2][0])
            if isinstance(e, tuple) and e[0] == 'sort' and e[1] is not None and len(e[3]) == 1 and bare(e[3][0]) == ('@', s[1]):
                # In place, to perl (T187).
                self.at = id(s)
                if any(v is UNDEF for v in self.arr(s[1]).items):
                    raise Fault(IN_PLACE)
        super().run(s)

# ---- as source

def sort_text(e, top):
    if e[1] is None:
        first = e[3][0]
        assert not isinstance(first, tuple) or first[0] in ('@', 'slice', 'map', 'grep', 'sort', 'reverse', 'join'), 'perl would take a word or a bracket first after sort another way'
        return f'(sort {items(e[3])})'
    return f'(sort {{ {it.inline(e[1])}{text(e[2])} }} ({items(e[3])}))'

var.MORE['sort'] = sort_text
_blocks = it.blocks

def blocks(e, line, found):
    """it.py's `blocks`, with a sort's."""
    if isinstance(e, tuple) and e[0] == 'sort' and e[1] is not None:
        for s in e[1] + [e[2]]:
            found[id(s)] = line
    _blocks(e, line, found)

it.blocks = blocks
source = it.source

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

# ---- the cases

shown = var.shown
P, Q, X = (('$', n) for n in 'pqx')
NUM = ('<=>', VA, VB)
DOWN = ('<=>', VB, VA)
STR = ('cmp', VA, VB)

def sort_cases():
    c = Cases(0)
    # By string, with no block; and the four blocks perl throws away.
    def plain(f, g, G):
        n, w, e, r = g('n'), g('w'), g('e'), g('r')
        s = [mya(n, 10, 9, 2, 33, 100, 1, 21, 2), mya(w, 'pear', 'Fig', 'apple', 'fig', '', 'Apple', 'b', 'a10', 'a9'), ('mya', e, None), ('mya', r, None),
             mya(g('m'), 3, 1.5, '2', TRUE, FALSE, -7, 0.25, '10', 1e3)]
        for its in ([A(n)], [A(w)], [A(e)], [A(g('m'))], [A(n), A(w)], [7], [3, 1, 2], ['b', 'a'], [('slice', n, [0, 1, 2])], [0, ('..', 8, 12)], [rev(A(n))]):
            s += [seta(r, srt(its)), dump(r)]
        for b in (NUM, DOWN, STR, ('cmp', VB, VA)):
            s += [seta(r, srt([A(n)], b)), dump(r), seta(r, srt([A(e)], b)), dump(r), seta(r, srt([42], b)), dump(r)]
        s += [seta(r, srt([A(w)], STR)), dump(r), seta(r, srt([A(g('m'))], NUM)), dump(r), seta(r, srt([A(g('m'))], DOWN)), dump(r),
              seta(r, rev(srt([A(n)], NUM))), dump(r), seta(r, rev(srt([A(w)]))), dump(r)]
        return s
    c.case(plain)
    # Blocks: by a key, by two, stable, with statements and a my, calling
    # a sub, with a map or a sort inside, by arithmetic, by a test, and
    # ones that are no order.
    def blocks_(f, g, G):
        w, n, r = g('w'), g('n'), g('r')
        ln = lambda v: ('call', 'length', [v])
        return [mya(w, 'pear', 'fig', 'apple', 'kiwi', 'date', 'plum', 'a', 'bb', 'cc', 'ddd', 'ee', 'f'), mya(n, 5, 3, 8, 1, 9, 2, 7), ('mya', r, None),
                sub(f('len'), [req('p')], returns(ln(P))), sub(f('by'), [req('p'), req('q')], returns(('<=>', P, Q))),
                seta(r, srt([A(w)], ('<=>', ln(VA), ln(VB)))), dump(r),
                seta(r, srt([A(w)], ('or', ('<=>', ln(VA), ln(VB)), ('cmp', VA, VB)))), dump(r),
                seta(r, srt([A(w)], ('||', ('<=>', ln(VB), ln(VA)), ('cmp', VB, VA)))), dump(r),
                seta(r, srt([A(w)], ('<=>', ucall(f('len'), VA), ucall(f('len'), VB)))), dump(r),
                seta(r, srt([A(n)], ucall(f('by'), VA, VB))), dump(r),
                seta(r, srt([A(n)], ('-', VA, VB))), dump(r), seta(r, srt([A(n)], ('-', VB, VA))), dump(r),
                seta(r, srt([A(n)], ('my', 'x', ('%', VA, 3)), ('my', 'y', ('%', VB, 3)), ('<=>', ('$', 'x'), ('$', 'y')))), dump(r),
                seta(r, srt([A(n)], ('?:', ('<', VA, VB), -1, ('?:', ('>', VA, VB), 1, 0)))), dump(r),
                seta(r, srt([A(n)], ('<=>', ('scalar', n), 0))), dump(r),
                seta(r, srt([A(n)], 0)), dump(r), seta(r, srt([A(n)], 1)), dump(r), seta(r, srt([A(n)], -1)), dump(r),
                seta(r, srt([A(n)], ('/', ('-', VA, VB), 4))), dump(r), seta(r, srt([A(n)], ('*', ('-', VA, VB), 0.5))), dump(r),
                seta(r, srt([A(n)], ('>', VA, VB))), dump(r), seta(r, srt([A(n)], '1')), dump(r), seta(r, srt([A(n)], TRUE)), dump(r), seta(r, srt([A(n)], FALSE)), dump(r),
                seta(r, srt([A(n)], 2147483647)), dump(r), seta(r, srt([A(n)], -2147483648)), dump(r),
                # A sort in a sort's block, a map in one, and a sort in a
                # map's: each has its own `$a`, `$b` and `$_`.
                seta(r, srt([A(n)], ('mya', 't', [srt([VA, VB], DOWN)]), ('<=>', el('t', 0), VA))), dump(r),
                seta(r, srt([A(n)], ('<=>', mp([VA], ('%', IT, 4)), mp([VB], ('%', IT, 4))))), dump(r),
                seta(r, mp([A(n)], ('mya', 't', [srt([IT, 5, 1], NUM)]), el('t', 1))), dump(r),
                seta(r, srt([mp([A(n)], ('*', IT, IT))], DOWN)), dump(r), seta(r, srt([gr([A(n)], ('>', IT, 2))], NUM)), dump(r),
                seta(r, mp([srt([A(n)], NUM)], ('+', IT, 1))), dump(r), seta(r, gr([srt([A(w)])], ('>', ln(IT), 2))), dump(r),
                # The array is as it was, and may be read from the block.
                seta(r, srt([A(n)], ('<=>', ('+', VA, el(n, 0)), ('+', VB, el(n, 0))))), dump(r), dump(n)]
    c.case(blocks_)
    # Every place a list is wanted; in place; in subs.
    def places(f, g, G):
        n, r = g('n'), g('r')
        S = lambda: srt([A(n)], NUM)
        return [mya(n, 5, 3, 8, 1), ('mya', r, None),
                sub(f('sorted'), [slurp('v')], returns(srt([A('v')], NUM))),
                sub(f('last'), [slurp('v')], do(srt([A('v')], DOWN))),
                sub(f('cnt'), [slurp('v')], returns(jn(',', ('scalar', 'v'), A('v')))),
                sub(f('smallest'), [slurp('v')], ('lassign', True, [('$', 'first')], [srt([A('v')], NUM)]), returns(('$', 'first'))),
                sayl(S()), say_(jn(',', S())), say_(ucall(f('cnt'), S(), 0)), over('x', [S()], sayl('x', X)), forit([S()], sayl('i', IT)), formod(say_(IT), S()),
                ('lassign', True, [('$', g('x')), ('$', g('y'))], [S()]), say_(join(G('x'), G('y'))),
                sayl(('lslice', [S()], [0, -1])), sayl(('xl', [S()], 2)), do(('push', r, [S()])), dump(r),
                seta(r, ucall(f('sorted'), A(n), 4)), dump(r), seta(r, ucall(f('last'), 2, 9)), dump(r), say_(ucall(f('smallest'), A(n))),
                # In place, and through brackets; then the array is its own
                # again.
                seta(n, srt([A(n)], NUM)), dump(n), seta(n, srt([lst(A(n))], DOWN)), dump(n), seta(n, lst(srt([A(n)], STR))), dump(n),
                seta(n, srt([A(n)])), dump(n), seta(n, rev(srt([A(n)], NUM))), dump(n), seta(n, srt([A(n), 0], NUM)), dump(n),
                do(('push', n, [6])), do(setel(n, 0, 99)), dump(n),
                # An undef that the block takes, where it is not in place.
                seta(r, srt([3, UNDEF, 1], ('<=>', ('//', VA, 0), ('//', VB, 0)))), dump(r),
                seta(n, 3, UNDEF, 1), seta(r, srt([A(n)], ('<=>', ('//', VA, 0), ('//', VB, 0)))), dump(r),
                seta(n, rev(srt([A(n)], ('<=>', ('//', VA, 0), ('//', VB, 0))))), dump(n)]
    c.case(places)
    return c.out

def order_cases():
    """The comparisons themselves: blocks that log each pair, over lists
    that take every path of the merge. perl's order, or these differ."""
    c = Cases(100)
    r_ = random.Random(10)
    made = [[5, 3, 8, 1, 9, 2, 7], [1, 2, 3, 4, 5, 6, 7], [7, 6, 5, 4, 3, 2, 1], [2, 1], [1, 2], [4, 4, 4, 4, 4], [3, 1, 2]]
    made += [[r_.randrange(50) for _ in range(n)] for n in (9, 17, 24, 33)]
    made += [list(range(20)) + [3, 2, 1], list(range(30, 8, -1)) + [50, 51], [1] * 9 + [0] * 9 + [1] * 5,
             [r_.randrange(3) for _ in range(40)], list(range(18)) + list(range(18)), list(range(40, 0, -1)),
             # a long run and one more: the one is picked up into the run
             list(range(19)), list(range(21, 0, -1)), list(range(17)) + [5]]
    def logged(f, g, G):
        v, r, log, n = g('v'), g('r'), g('log'), g('n')
        note = do(set_(log, join(VA, ',', VB, ' '), '.='))
        s = [('mya', v, None), ('mya', r, None), ('my', log, ''), ('my', n, 0)]
        for values in made:
            for how in (NUM, DOWN, ('<=>', ('%', VA, 5), ('%', VB, 5)), ('-', ('%', ('+', ('*', VA, 7), ('*', VB, 13)), 3), 1)):
                s += [seta(v, *values), do(set_(log, '')), seta(r, srt([A(v)], note, how)), say_(G('log')), say_(jn(' ', A(r)))]
        # Counted, and nothing else; in place and into another array and
        # under reverse: the same comparisons.
        for values in made[:6]:
            s += [seta(v, *values), do(set_(n, 0)), seta(r, srt([A(v)], do(step(n)), NUM)), say_(G('n')),
                  do(set_(log, '')), seta(v, srt([A(v)], note, DOWN)), say_(G('log')),
                  do(set_(log, '')), seta(r, rev(srt([A(v)], note, NUM))), say_(G('log')), say_(jn(' ', A(r)))]
        # A list of none and of one: the block is not run.
        s += [do(set_(n, 0)), seta(r, srt([lst()], do(step(n)), NUM)), seta(r, srt([7], do(step(n)), NUM)), say_(G('n'))]
        return s
    c.case(logged)
    return c.out

SAME = {'1200': ('sort', sort_cases), '1201': ('sort-order', order_cases)}

def faults():
    out = {}
    n = [1210]
    def fault(name, subs_, near, far):
        out[str(n[0])] = ('fault-' + name, subs_, near, far)
        n[0] += 1
    a3 = lambda: mya('a', 3, 1, 2)
    R = lambda e: ('mya', 'r', [e])
    # The array, changed while it is sorted: by the block, and by a sub
    # the block calls.
    for name, change in (('store', do(setel('a', 0, 9))), ('push', do(('push', 'a', [4]))), ('assign', seta('a', 7))):
        fault('frozen-sort-' + name, [], block(a3(), R(srt([A('a')], NUM))), block(a3(), R(srt([A('a')], change, NUM))))
    fault('frozen-sort-from-a-sub', [mya('a', 3, 1, 2), sub('poke', [], do(setel('a', 2, 30)), returns(0))], block(R(srt([A('a')], NUM))), block(R(srt([A('a')], do(ucall('poke')), NUM))))
    store = do(setel('a', 0, 9))
    fault('given-back-after-a-sort', [], block(a3(), R(srt([A('a')], NUM)), store, dump('a')), block(a3(), R(srt([A('a')], store, NUM))))
    for name, its in (('second-of-two', [A('b'), A('a')]), ('slice', [('slice', 'a', [0, 1])]), ('reverse', [rev(A('a'))]), ('a-map-of-it', [mp([A('a')], IT)])):
        fault('sort-names-by-' + name, [], block(a3(), mya('b', 7), R(srt(its, NUM))), block(a3(), mya('b', 7), R(srt(its, store, NUM))))
    # Past the end, in a sort's list (T188): with a block and with none.
    und = ('<=>', ('//', VA, 0), ('//', VB, 0))
    fault('element-past-the-end-in-a-sort', [], block(a3(), R(srt([el('a', 2), 5], und))), block(a3(), R(srt([el('a', 3), 5], und))))
    fault('slice-past-the-end-in-a-sort', [], block(a3(), R(srt([('slice', 'a', [0, 2])], und))), block(a3(), R(srt([('slice', 'a', [0, 3])], und))))
    fault('slice-past-the-end-in-a-sort-with-no-block', [], block(a3(), R(srt([('slice', 'a', [0, 2])]))), block(a3(), R(srt([('slice', 'a', [0, 3])]))))
    # The block's value.
    for name, near, far in (('undef', 0, UNDEF), ('a-string-that-is-no-number', '0', 'abc'), ('past-32-bits', 2147483647, 2147483648), ('below-32-bits', -2147483648, -2147483649),
                            ('a-number-outside-the-integers', 1e9, 1e30)):
        fault('sort-block-gives-' + name, [], block(a3(), R(srt([A('a')], near))), block(a3(), R(srt([A('a')], far))))
    # With no block every value is made a string first: an undef, among
    # others and alone.
    fault('sort-of-an-undef', [], block(mya('u', 'b', '', 'a'), R(srt([A('u')]))), block(mya('u', 'b', UNDEF, 'a'), R(srt([A('u')]))))
    fault('sort-of-one-undef', [], block(mya('u', ''), R(srt([A('u')]))), block(mya('u', UNDEF), R(srt([A('u')]))))
    # A lone value, under a block perl throws away (T190); and under
    # another, which is not run.
    fault('sort-of-one-string-by-number', [], block(mya('u', 'abc'), R(srt([A('u')], ('+', NUM, 0)))), block(mya('u', 'abc'), R(srt([A('u')], NUM))))
    fault('sort-of-one-undef-by-string', [], block(mya('u', UNDEF), R(srt([A('u')], ('.', STR, '')))), block(mya('u', UNDEF), R(srt([A('u')], ('cmp', VB, VA)))))
    # Two values that the comparison faults on.
    fault('sort-of-strings-by-number', [], block(mya('u', '10', '9'), R(srt([A('u')], NUM))), block(mya('u', '10', 'x'), R(srt([A('u')], NUM))))
    # In place (T187).
    fault('undef-in-an-array-sorted-in-place', [], block(mya('u', 3, UNDEF, 1), R(srt([A('u')], und)), seta('u', rev(srt([A('u')], und))), dump('u')), block(mya('u', 3, UNDEF, 1), seta('u', srt([A('u')], und))))
    fault('undef-in-an-array-sorted-in-place-through-brackets', [], block(mya('u', 3, 1), seta('u', lst(srt([lst(A('u'))], und))), dump('u')), block(mya('u', 3, UNDEF), seta('u', lst(srt([lst(A('u'))], und)))))
    # D18.
    fault('sort-returned-for-one-value', [mya('a', 3, 1, 2), sub('f', [], returns(srt([A('a')], NUM)))], sayl(ucall('f')), ('my', 'x', ucall('f')))
    # A fault in a block, on its statement's line.
    fault('in-a-sort-block', [], block(a3(), R(srt([A('a')], ('my', 't', ('/', 6, VA)), NUM))), block(mya('a', 3, 0, 2), R(srt([A('a')], ('my', 't', ('/', 6, VA)), NUM))))
    return out

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/sort.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/sort.py {n} > t/{n}-{name}.expected\n'
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
    model = ['model: t/models/sort.py']
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
