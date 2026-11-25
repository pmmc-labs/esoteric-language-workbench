#!/usr/bin/env python3
"""gen_past_ex.py [PART/OF]: not a sample: every initial value x every single
read-only statement (and none) x each of ++ and -- (as a statement) x five
observations, each program held to the rule. The values, reads and
observations are gen_past.py's."""
import sys, collections
import model, harness

import gen_past
ns = vars(gen_past)
L, S, b = ns['L'], ns['S'], ns['b']


def main():
    part, of = 0, 1
    for a in sys.argv[1:]:
        if '/' in a: part, of = map(int, a.split('/'))
    x = ('var', 'x')
    t = harness.Tally('every value x every read x ++/--, part %d of %d' % (part, of), 'pastex-%d.log' % part)
    kinds = collections.Counter()
    obs = [[('say', x)], [('say', b('+', x, L('1')))], [('say', b('.', x, S('"|"', '|')))], [('say', b('*', x, L('10000000000000000')))],
           [('expr', ('post', '++', 'x')), ('say', b('-', x, L('0.5')))]]
    n = 0
    for init in ns['inits']():
        for rd in [None] + ns['reads'](x):
            for step in (('post', '++', 'x'), ('post', '--', 'x')):
                for o in obs:
                    n += 1
                    if n % of != part: continue
                    p = [('my', 'x', init)] + ([] if rd is None else [('my', 't1', rd)]) + [('expr', step)] + o
                    v = t.check(p)
                    if v:
                        key = v.split(':')[0]
                        for w in ('Lost precision',):
                            if w in v: key += ' [' + w + ']'
                        kinds[key] += 1
    t.done()
    print(dict(kinds))


if __name__ == '__main__':
    main()
