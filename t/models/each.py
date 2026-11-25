#!/usr/bin/env python3
"""t/811 to t/849: foreach, and the freeze (step 9b; D17, D77, D80).

The definition, which is all this file knows of the language beyond
t/models/list.py (arrays and lists).

  for my $x (LIST) { ... }        the block once for each value of LIST
  foreach my $x (LIST) { ... }    the same, spelled out
  last;  next;  last L;  next L;  as in any loop

LIST is worked out once, before the first time round, and copied: `$x`
is a value, new each time, and read-only (the compiler refuses a program
that assigns it). A `foreach` over one range counts, and builds no list.

**Every array named anywhere in LIST is frozen while the loop runs**: a
store to an element of it, or a change of its size, by the block or by a
sub the block calls, is a fault. It may be read. The freeze is a count,
for a loop in a loop over one array, and it is given back on every way
out: the end of the list, `last`, a `last` or `next` to a loop outside,
and `return`. A range, a call and a value name no array, so `for my $i
(0 .. $#a)` leaves `@a` free to change... but for `$#a`, which names it:
the loop to change an array in is `for my $i (0 .. scalar(@a) - 1)`,
which names it too. **Naming is naming**: what does not name the array
is a count taken before the loop.

An element or a slice past either end of its array, in LIST, is a fault:
perl would make the elements (T161). And in a `foreach` over one range,
an end below -2^63 + 513 is a fault, as it is to perl (T166).

This model works a program out; it does not refuse one. D76 and D77, and
the read-only `$x`, are the compiler's.

The model is Python. perl is the second derivation: t/checks.py oracle
holds every .expected of a test without a `kind:` to what perl 5.42
prints, and each fault test's output to the start of it.

811 is a foreach over every kind of list, loops in loops, `last` and
`next`. 812 is the freeze given back, each way out. 813 is ranges walked.
820 on each fault once: every way a frozen array is changed, every shape
that names one.

Every command that writes a file, one a line (t/checks.py runs them all):

    python3 t/models/each.py --program 811 > t/811-foreach.pl
    python3 t/models/each.py 811 > t/811-foreach.expected
    python3 t/models/each.py --program 812 > t/812-freeze-given-back.pl
    python3 t/models/each.py 812 > t/812-freeze-given-back.expected
    python3 t/models/each.py --program 813 > t/813-foreach-range.pl
    python3 t/models/each.py 813 > t/813-foreach-range.expected
    python3 t/models/each.py --program 820 > t/820-fault-frozen-store.pl
    python3 t/models/each.py 820 > t/820-fault-frozen-store.expected
    python3 t/models/each.py --program 821 > t/821-fault-frozen-store-what-is-there.pl
    python3 t/models/each.py 821 > t/821-fault-frozen-store-what-is-there.expected
    python3 t/models/each.py --program 822 > t/822-fault-frozen-store-past-the-end.pl
    python3 t/models/each.py 822 > t/822-fault-frozen-store-past-the-end.expected
    python3 t/models/each.py --program 823 > t/823-fault-frozen-add-to-element.pl
    python3 t/models/each.py 823 > t/823-fault-frozen-add-to-element.expected
    python3 t/models/each.py --program 824 > t/824-fault-frozen-or-assign-element.pl
    python3 t/models/each.py 824 > t/824-fault-frozen-or-assign-element.expected
    python3 t/models/each.py --program 825 > t/825-fault-frozen-and-assign-past-the-end.pl
    python3 t/models/each.py 825 > t/825-fault-frozen-and-assign-past-the-end.expected
    python3 t/models/each.py --program 826 > t/826-fault-frozen-step-element.pl
    python3 t/models/each.py 826 > t/826-fault-frozen-step-element.expected
    python3 t/models/each.py --program 827 > t/827-fault-frozen-push.pl
    python3 t/models/each.py 827 > t/827-fault-frozen-push.expected
    python3 t/models/each.py --program 828 > t/828-fault-frozen-unshift.pl
    python3 t/models/each.py 828 > t/828-fault-frozen-unshift.expected
    python3 t/models/each.py --program 829 > t/829-fault-frozen-pop.pl
    python3 t/models/each.py 829 > t/829-fault-frozen-pop.expected
    python3 t/models/each.py --program 830 > t/830-fault-frozen-shift.pl
    python3 t/models/each.py 830 > t/830-fault-frozen-shift.expected
    python3 t/models/each.py --program 831 > t/831-fault-frozen-splice.pl
    python3 t/models/each.py 831 > t/831-fault-frozen-splice.expected
    python3 t/models/each.py --program 832 > t/832-fault-frozen-splice-nothing.pl
    python3 t/models/each.py 832 > t/832-fault-frozen-splice-nothing.expected
    python3 t/models/each.py --program 833 > t/833-fault-frozen-assign.pl
    python3 t/models/each.py 833 > t/833-fault-frozen-assign.expected
    python3 t/models/each.py --program 834 > t/834-fault-frozen-assign-itself.pl
    python3 t/models/each.py 834 > t/834-fault-frozen-assign-itself.expected
    python3 t/models/each.py --program 835 > t/835-fault-frozen-list-assign-element.pl
    python3 t/models/each.py 835 > t/835-fault-frozen-list-assign-element.expected
    python3 t/models/each.py --program 836 > t/836-fault-frozen-list-assign-array.pl
    python3 t/models/each.py 836 > t/836-fault-frozen-list-assign-array.expected
    python3 t/models/each.py --program 837 > t/837-fault-frozen-from-a-sub.pl
    python3 t/models/each.py 837 > t/837-fault-frozen-from-a-sub.expected
    python3 t/models/each.py --program 838 > t/838-fault-frozen-push-from-a-sub.pl
    python3 t/models/each.py 838 > t/838-fault-frozen-push-from-a-sub.expected
    python3 t/models/each.py --program 839 > t/839-fault-names-by-second-of-two.pl
    python3 t/models/each.py 839 > t/839-fault-names-by-second-of-two.expected
    python3 t/models/each.py --program 840 > t/840-fault-names-by-slice.pl
    python3 t/models/each.py 840 > t/840-fault-names-by-slice.expected
    python3 t/models/each.py --program 841 > t/841-fault-names-by-elements.pl
    python3 t/models/each.py 841 > t/841-fault-names-by-elements.expected
    python3 t/models/each.py --program 842 > t/842-fault-names-by-list-repeated.pl
    python3 t/models/each.py 842 > t/842-fault-names-by-list-repeated.expected
    python3 t/models/each.py --program 843 > t/843-fault-names-by-slice-of-a-list.pl
    python3 t/models/each.py 843 > t/843-fault-names-by-slice-of-a-list.expected
    python3 t/models/each.py --program 844 > t/844-fault-names-by-through-and.pl
    python3 t/models/each.py 844 > t/844-fault-names-by-through-and.expected
    python3 t/models/each.py --program 845 > t/845-fault-names-by-through-a-test.pl
    python3 t/models/each.py 845 > t/845-fault-names-by-through-a-test.expected
    python3 t/models/each.py --program 846 > t/846-fault-names-by-last-index.pl
    python3 t/models/each.py 846 > t/846-fault-names-by-last-index.expected
    python3 t/models/each.py --program 847 > t/847-fault-names-by-count.pl
    python3 t/models/each.py 847 > t/847-fault-names-by-count.expected
    python3 t/models/each.py --program 848 > t/848-fault-names-by-in-a-range.pl
    python3 t/models/each.py 848 > t/848-fault-names-by-in-a-range.expected
    python3 t/models/each.py --program 849 > t/849-fault-frozen-after-the-inner-loop.pl
    python3 t/models/each.py 849 > t/849-fault-frozen-after-the-inner-loop.expected
    python3 t/models/each.py --program 850 > t/850-fault-element-past-the-end-in-the-list.pl
    python3 t/models/each.py 850 > t/850-fault-element-past-the-end-in-the-list.expected
    python3 t/models/each.py --program 851 > t/851-fault-element-before-the-start-in-the-list.pl
    python3 t/models/each.py 851 > t/851-fault-element-before-the-start-in-the-list.expected
    python3 t/models/each.py --program 852 > t/852-fault-slice-past-the-end-in-the-list.pl
    python3 t/models/each.py 852 > t/852-fault-slice-past-the-end-in-the-list.expected
    python3 t/models/each.py --program 853 > t/853-fault-range-at-the-low-edge.pl
    python3 t/models/each.py 853 > t/853-fault-range-at-the-low-edge.expected
    python3 t/models/each.py --program 854 > t/854-fault-range-of-a-string.pl
    python3 t/models/each.py 854 > t/854-fault-range-of-a-string.expected
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import var
import loop
import list as lists
from var import Fault, MIN, MAX, UNDEF, TRUE, FALSE, get, logic, strings, text
from loop import block, do, step, set_, my, join, Jump
from sub import ABSENT, ucall, sub, req, opt, ret, say_, named, lines
from list import A, el, lst, mya, seta, sayl, setel, dump, Cases, Arr, changing, items

PAST = 'an element past the end of the array in a foreach, where perl would make it'
SLICE_PAST = 'a slice past the end of the array, where perl would make the elements'
RANGE_LOW = 'a foreach over a range that begins or ends this near the smallest integer: perl refuses it'

def names(e, into):
    """The arrays an expression names, anywhere in it."""
    if not isinstance(e, tuple):
        return into
    if e[0] in ('@', 'elem', 'last', 'scalar', 'slice', 'pop', 'shift', 'push', 'unshift', 'splice', 'setel', 'stepel'):
        into.append(e[2] if e[0] in ('setel',) else e[3] if e[0] == 'stepel' else e[1])
    for part in e[1:]:
        if isinstance(part, tuple):
            names(part, into)
        elif isinstance(part, list):
            for p in part:
                names(p, into)
    return into

# ('foreach', label, name, [items], body)
class Run(lists.Run):
    def strict(self, e):
        """The fault for an element or a slice past either end, in a
        foreach's list, through what hands a list on."""
        if not isinstance(e, tuple):
            return
        kind = e[0]
        if kind == 'elem':
            a = self.arr(e[1])
            if self.where(a, self.index(e[2])) is None:
                raise Fault(PAST)
        elif kind == 'slice':
            a = self.arr(e[1])
            for i in [self.whole_of(v) for item in e[2] for v in self.evl(item)]:
                if self.where(a, i) is None:
                    raise Fault(SLICE_PAST)
        elif kind == 'list':
            for item in e[1]:
                self.strict(item)

    def run(self, s):
        if s[0] != 'foreach':
            return super().run(s)
        _, label, name, its, body = s
        self.at = id(s)
        one_range = len(its) == 1 and isinstance(its[0], tuple) and its[0][0] == '..'
        if one_range:
            ends = []
            for end in (its[0][1], its[0][2]):
                v = get(self.ev(end))
                if strings.is_str(v):
                    raise Fault(lists.RANGE_STRING)
                ends.append(self.whole_of(v))
            if min(ends) < MIN + 513:
                raise Fault(RANGE_LOW)
            values = range(ends[0], ends[1] + 1)
        else:
            # (The cases here read nothing twice that the list's own
            # working out changes.)
            for item in its:
                self.strict(item)
            values = [v for item in its for v in self.evl(item)]
        frozen = []
        for n in dict.fromkeys(names(('list', its), [])):
            a = self.arr(n)
            a.frozen += 1
            frozen.append(a)
        self.frames.append('loop')
        try:
            for v in values:
                self.scopes.append({name: var.Place()})
                self.scopes[-1][name].value = v
                if self.round(body, label) == 'last':
                    self.scopes.pop()
                    break
                self.scopes.pop()
        finally:
            # On every way out: a `last` to an outer loop and a `return`
            # pass through here too.
            for a in frozen:
                a.frozen -= 1
        self.frames.pop()

def source(s, depth=0):
    pad = '    ' * depth
    kind = s[0]
    inner = lambda statements: [line for t in statements for line in source(t, depth + 1)]
    label = lambda name: '' if name is None else name + ': '
    if kind == 'foreach':
        return [f'{pad}{label(s[1])}for my ${s[2]} ({items(s[3])}) {{'] + inner(s[4]) + [pad + '}']
    if kind == 'sub':
        from sub import parameter
        return [f'{pad}sub {s[1]}({", ".join(parameter(p) for p in s[2])}) {{'] + inner(s[3]) + [pad + '}']
    if kind in ('while', 'until'):
        return [f'{pad}{label(s[1])}{kind} ({text(s[2])}) {{'] + inner(s[3]) + [pad + '}']
    if kind == 'for':
        return [lists.source(('for',) + tuple(s[1:5]) + ([],), depth)[0]] + inner(s[5]) + [pad + '}']
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
    return lists.source(s, depth)

def output(statements):
    r = Run(statements)
    try:
        for s in statements:
            r.run(s)
    except Fault as f:
        return r.out, str(f), r.alias.get(r.at, r.at)
    assert len(r.scopes) == 1 and r.frames == [] and r.wants == [], 'something was left open'
    return r.out, None, None

def lines_(statements, line, found):
    """sub.py's `lines`, with a foreach's block."""
    for s in statements:
        found[id(s)] = line
        kind = s[0]
        if kind in ('block', 'unless', 'while', 'until', 'for', 'sub', 'foreach'):
            line = lines_(s[-1], line + 1, found) + 1
        elif kind == 'if':
            for n, (test, body) in enumerate(s[1]):
                found[(id(s), n)] = line
                line = lines_(body, line + 1, found)
            if s[2] is not None:
                line = lines_(s[2], line + 1, found)
            line += 1
        else:
            if kind == 'mod':
                found[id(s[1])] = line
            line += 1
    return line

# ---- the cases

shown = var.shown
X, Y, I = ('$', 'x'), ('$', 'y'), ('$', 'i')

def each(name, its, *body, label=None):
    return ('foreach', label, name, list(its), list(body))

def pr(*es):
    """print each, and a blank: a loop's values on one line."""
    return ('sayl', list(es))

def foreach_cases():
    c = Cases(0)
    def kinds(f, g, G):
        a, e, b, line = g('a'), g('e'), g('b'), g('line')
        L = G('line')
        add = lambda v: do(set_(line, join('<', v, '>'), '.='))
        def walk(*its):
            return [do(set_(line, '')), each('x', its, add(('?:', ('call', 'defined', [X]), X, 'undef'))), say_(L)]
        s = [mya(a, 1, 2, 3), ('mya', e, None), mya(b, 'p', 'q'), ('my', line, ''), sub(f('none'), [], ret()), sub(f('five'), [], ret(5))]
        for its in ([A(a)], [1, 2, 3], [A(a), A(b)], [A(e)], [A(e), A(e)], [lst()], [A(a), 9, A(e), 'z'], [('slice', a, [2, 0])], [('lslice', [A(a), 7], [3, 0])],
                    [('xl', [A(a)], 2)], [el(a, 0), el(a, 2)], [ucall(f('five')), ucall(f('none')), ucall(f('five'))], [ucall(f('none'))], [('scalar', a)],
                    [('..', 1, 4), 9], [0, ('..', 2, 3)], [('?:', A(a), A(b), A(e))], [('||', A(e), A(b))], [('||', A(a), A(b))], [UNDEF, 0, ''], [lst(1, lst(2, lst(3)))],
                    [('last', a)], [('+', A(a), 1)]):
            s += walk(*its)
        return s
    c.case(kinds)
    # Loops in loops, over one array and over two; `last` and `next`, to
    # the inner and to the outer; a foreach in a while and a while in a
    # foreach.
    def nested(f, g, G):
        a, b, line = g('a'), g('b'), g('line')
        L = G('line')
        add = lambda *vs: do(set_(line, join(*vs, ' '), '.='))
        return [mya(a, 1, 2, 3), mya(b, 10, 20), ('my', line, ''),
                each('x', [A(a)], each('y', [A(a)], add(X, Y))), say_(L), do(set_(line, '')),
                each('x', [A(a)], each('y', [A(b)], ('mod', ('next', None), 'if', ('==', Y, 10)), add(X, Y))), say_(L), do(set_(line, '')),
                each('x', [A(a)], each('y', [A(a)], ('mod', ('next', 'OUT'), 'if', ('>', Y, X)), ('mod', ('last', 'OUT'), 'if', ('==', X, 3)), add(X, Y)), label='OUT'), say_(L), do(set_(line, '')),
                each('x', [A(a)], ('mod', ('last', None), 'if', ('==', X, 2)), add(X)), say_(L), do(set_(line, '')),
                each('x', [A(a)], ('mod', ('next', None), 'if', ('==', X, 2)), add(X)), say_(L), do(set_(line, '')),
                ('my', g('k'), 0), ('while', None, ('<', G('k'), 2), [each('x', [A(b)], add(G('k'), X)), do(step(g('k')))]), say_(L), do(set_(line, '')),
                each('x', [A(b)], ('my', 'n', 0), ('while', None, ('<', ('$', 'n'), 2), [add(X, ('$', 'n')), do(step('n'))])), say_(L), do(set_(line, '')),
                each('x', [A(a)], ('for', None, [my('j', 0)], ('<', ('$', 'j'), X), [step('j')], [add(X, ('$', 'j'))])), say_(L), do(set_(line, '')),
                # `$x` is the loop's own, and gone after; a variable of
                # its name outside is another.
                ('my', 'x', 'outer'), each('x', [A(b)], add(X)), say_(join(L, X)), do(set_(line, '')),
                # A copy: changing a copy of it changes nothing.
                each('x', [A(a)], ('my', 'c', X), do(set_('c', 10, '*=')), add(('$', 'c'))), say_(L), dump(a), do(set_(line, '')),
                # Read while the loop is over it, and another array changed.
                each('x', [A(a)], do(('push', b, [('*', X, el(a, 0))])), add(('scalar', a), ('last', a), el(a, -1))), say_(L), dump(b)]
    c.case(nested)
    # In subs: a `return` from inside one loop and from inside two; the
    # file's array walked by a sub; a sub called from the block that reads
    # the array.
    def in_subs(f, g, G):
        a = g('a')
        return [mya(a, 4, 8, 15, 16),
                sub(f('find'), [req('w')], each('x', [A(a)], ('mod', ret(X), 'if', ('>', X, ('$', 'w')))), ret(-1)),
                sub(f('pair'), [req('w')], each('x', [A(a)], each('y', [A(a)], ('mod', ret(join(X, '+', Y)), 'if', ('==', ('+', X, Y), ('$', 'w'))))), ret('none')),
                sub(f('total'), [], ('my', 't', 0), each('x', [A(a)], do(set_('t', X, '+='))), ret(('$', 't'))),
                sub(f('first'), [], ret(el(a, 0))),
                say_(ucall(f('find'), 5)), say_(ucall(f('find'), 100)), say_(ucall(f('pair'), 23)), say_(ucall(f('pair'), 7)), say_(ucall(f('total'))),
                each('x', [A(a)], say_(('+', X, ucall(f('first'))))),
                each('x', [ucall(f('total')), ucall(f('find'), 8)], say_(X))]
    c.case(in_subs)
    return c.out

def given_back_cases():
    """After each way out of a loop over an array, the array can be
    changed again."""
    c = Cases(100)
    def ways(f, g, G):
        a = g('a')
        change = lambda: [do(('push', a, [0])), do(setel(a, 0, ('+', el(a, 0), 1))), dump(a)]
        s = [mya(a, 1, 2, 3)]
        s += [each('x', [A(a)], ('my', 'c', X))] + change()
        s += [each('x', [A(a)], ('mod', ('last', None), 'if', ('==', X, 2)))] + change()
        s += [each('x', [A(a)], each('y', [A(a)], ('mod', ('last', 'OUT'), 'if', ('==', Y, 2))), label='OUT')] + change()
        s += [each('x', [A(a)], each('y', [A(a)], ('mod', ('next', 'OUT'), 'if', ('==', Y, 2))), label='OUT')] + change()
        s += [('my', g('k'), 0), ('while', 'W', ('<', step(g('k')), 2), [each('x', [A(a)], ('mod', ('next', 'W'), 'if', TRUE))])] + change()
        s += [sub(f('one'), [], each('x', [A(a)], ret(X)), ret(0)), sub(f('two'), [], each('x', [A(a)], each('y', [A(a)], ret(Y))), ret(0)),
              say_(ucall(f('one')))] + change() + [say_(ucall(f('two')))] + change()
        # A loop in a loop over one array: the inner one ending leaves it
        # frozen, and the outer one ending frees it.
        s += [each('x', [el(a, 0)], each('y', [A(a)], ('my', 'c', Y)), each('y', [('slice', a, [0, 1])], ('my', 'c', Y)))] + change()
        # A sub that walks the array, called while nothing else does.
        s += [sub(f('walk'), [], ('my', 'n', 0), each('x', [A(a)], do(step('n'))), ret(('$', 'n'))), say_(ucall(f('walk')))] + change()
        # The count before the loop names nothing: the array may change.
        s += [('my', g('n'), ('scalar', a)), each('i', [('..', 0, ('-', G('n'), 1))], do(setel(a, I, 2, '*='))), dump(a)]
        return s
    c.case(ways)
    return c.out

def range_cases():
    c = Cases(200)
    def ranges(f, g, G):
        line, n = g('line'), g('n')
        L = G('line')
        s = [('my', line, ''), ('my', n, 3), sub(f('limit'), [], ret(G('n')))]
        for lo, hi in ((1, 5), (3, 1), (0, 0), (-2, 2), (1.9, 4.1), (-1.9, 1.9), (FALSE, TRUE), (1, G('n')), (('-', G('n'), 1), ('*', G('n'), 2)),
                       (MAX - 2, MAX), (MIN + 513, MIN + 514), (5, 4), (-0.0, 1)):
            s += [do(set_(line, '')), each('i', [('..', lo, hi)], do(set_(line, join(I, ' '), '.='))), say_(L)]
        # The ends are fixed when the loop starts (the end is a call's
        # value: a loop whose block changes a variable its list names is
        # refused, D77); `last` and `next`.
        s += [do(set_(line, '')), each('i', [('..', 1, ucall(f('limit')))], do(set_(n, 10)), do(set_(line, I, '.='))), say_(L),
              do(set_(line, '')), each('i', [('..', 1, 9)], ('mod', ('next', None), 'if', ('%', I, 2)), ('mod', ('last', None), 'if', ('>', I, 6)), do(set_(line, I, '.='))), say_(L),
              ('my', g('c'), 0), each('i', [('..', 1, 200000)], do(step(g('c')))), say_(G('c')),
              # More values than an array may hold: a range is counted, and never built.
              do(set_(line, '')), each('i', [('..', 1, 5000000000)], ('mod', ('last', None), 'if', ('==', I, 4)), do(set_(line, I, '.='))), say_(L),
              do(set_(line, '')), each('i', [('..', 1, 3)], each('j', [('..', I, 3)], do(set_(line, join(I, ('$', 'j'), ' '), '.=')))), say_(L)]
        return s
    c.case(ranges)
    return c.out

SAME = {'811': ('foreach', foreach_cases), '812': ('freeze-given-back', given_back_cases), '813': ('foreach-range', range_cases)}

def faults():
    out = {}
    n = [820]
    def fault(name, subs_, near, far):
        out[str(n[0])] = ('fault-' + name, subs_, near, far)
        n[0] += 1
    a3 = lambda: mya('a', 1, 2, 3)
    over = lambda its, *body: each('x', its, *body)
    quiet = say_(X)
    # T131: perl carries on where this faults, and a loop over an array
    # that grows each time round never ends. Every change is followed by
    # a `last`.
    stop = ('last', None)
    # Every way an array is changed, while a loop is over it: each in a
    # loop that reads, and then in one that changes.
    ways = [
        ('store', do(setel('a', 0, 9))),
        ('store-what-is-there', do(setel('a', 0, el('a', 0)))),
        ('store-past-the-end', do(setel('a', 5, 9))),
        ('add-to-element', do(setel('a', 1, 1, '+='))),
        ('or-assign-element', do(setel('a', 1, 1, '||='))),
        ('and-assign-past-the-end', do(setel('a', 5, 1, '&&='))),
        ('step-element', do(('stepel', '++', False, 'a', 0))),
        ('push', do(('push', 'a', [4]))),
        ('unshift', do(('unshift', 'a', [0]))),
        ('pop', do(('pop', 'a'))),
        ('shift', do(('shift', 'a'))),
        ('splice', do(('splice', 'a', [0, 1]))),
        ('splice-nothing', do(('splice', 'a', [0, 0]))),
        ('assign', seta('a', 7, 8)),
        ('assign-itself', seta('a', A('a'))),
        ('list-assign-element', ('lassign', False, [el('a', 0), ('$', 'x2')], [5, 6])),
        ('list-assign-array', ('lassign', False, [('$', 'x2'), A('a')], [5, 6])),
    ]
    for name, change in ways:
        fault('frozen-' + name, [], block(a3(), ('my', 'x2', 0), over([A('a')], quiet)), block(a3(), ('my', 'x2', 0), over([A('a')], quiet, change, stop)))
    # From a sub the block calls.
    poke = sub('poke', [], do(setel('a', 2, 30)), ret(0))
    grow = sub('grow', [], do(('push', 'a', [9])), ret(0))
    return_ = lambda: None
    fault('frozen-from-a-sub', [mya('a', 1, 2, 3), poke], over([A('a')], quiet), over([A('a')], quiet, do(ucall('poke')), stop))
    fault('frozen-push-from-a-sub', [mya('a', 1, 2, 3), grow], over([A('a')], quiet), over([A('a')], quiet, do(ucall('grow')), stop))
    # Every shape that names the array freezes it.
    store = do(setel('a', 0, 9))
    for name, its in (('second-of-two', [A('b'), A('a')]), ('slice', [('slice', 'a', [0, 1])]), ('elements', [el('a', 1), el('a', 2)]), ('list-repeated', [('xl', [A('a')], 2)]),
                      ('slice-of-a-list', [('lslice', [A('a')], [0, 1])]), ('through-and', [('&&', A('b'), A('a'))]), ('through-a-test', [('?:', 1, A('a'), A('b'))]),
                      ('last-index', [('last', 'a')]), ('count', [('scalar', 'a')]), ('in-a-range', [('..', 0, ('last', 'a')), 9])):
        fault('names-by-' + name, [], block(a3(), mya('b', 7), over(its, quiet)), block(a3(), mya('b', 7), over(its, quiet, store)))
    # A loop in a loop over one array: when the inner one ends the array
    # is frozen still.
    fault('frozen-after-the-inner-loop', [], block(a3(), over([A('a')], each('y', [A('a')], say_(Y)))), block(a3(), over([A('a')], each('y', [A('a')], say_(Y)), store)))
    # Past the end, in the list (T161), and the low edge of a range (T166).
    fault('element-past-the-end-in-the-list', [], block(a3(), over([el('a', 2)], quiet)), block(a3(), over([el('a', 3)], quiet)))
    fault('element-before-the-start-in-the-list', [], block(a3(), over([el('a', -3)], quiet)), block(a3(), over([el('a', -4)], quiet)))
    fault('slice-past-the-end-in-the-list', [], block(a3(), over([('slice', 'a', [0, 2])], quiet)), block(a3(), over([('slice', 'a', [0, 3])], quiet)))
    fault('range-at-the-low-edge', [], block(over([('..', MIN + 513, MIN + 514)], quiet)), block(over([('..', MIN + 512, MIN + 514)], quiet)))
    fault('range-of-a-string', [], block(over([('..', 1, 2)], quiet)), block(over([('..', 1, '2')], quiet)))
    return out

FAULTS = faults()

def commands():
    return ''.join(f'    python3 t/models/each.py --program {n} > t/{n}-{name}.pl\n'
                   f'    python3 t/models/each.py {n} > t/{n}-{name}.expected\n'
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
    model = ['model: t/models/each.py']
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
    lines_(statements, len(header) + 3, found)
    out.write(f'{printed}fault: {fault} at {path} line {found[at]}.\nexit: 1\n'.encode())

if __name__ == '__main__':
    main(sys.argv[1:])
