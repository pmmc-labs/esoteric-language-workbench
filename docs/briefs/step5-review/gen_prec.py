#!/usr/bin/env python3
"""gen_prec.py SEED COUNT [--break]: gen_late's random trees, printed with the
fewest brackets (minshow.py). --break prints `=` as if it bound tighter than
`? :` (the checker must go red)."""
import random, sys, collections
import model, harness, minshow

import gen_late
ns = vars(gen_late)


def any_list_refused(p):
    return any(s[0] in ('say', 'print') and minshow.list_refused(s[1]) for s in p)


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    if '--break' in sys.argv: minshow.level = (lambda real: lambda e: 6 if e[0] == 'asg' else real(e))(minshow.level)
    r = random.Random(seed)
    t = harness.Tally('precedence, fewest brackets, seed %d' % seed, 'prec-%d.log' % seed)
    kinds = collections.Counter(); skipped = collections.Counter()
    for _ in range(count):
        p = ns['program'](r)
        if model.any_truth_refused(p): skipped['truth position'] += 1; continue
        if any_list_refused(p): skipped['list context'] += 1; continue
        if model.has_chain(p): skipped['chain of dots (finding)'] += 1; continue
        if model.has_append_of_assigned_concat(p): skipped['.= of assigned concat (finding)'] += 1; continue
        v = t.check(p, minshow.source(p))
        if v: kinds[v.split(':')[0] + (' Found =' if 'Found =' in v else '')] += 1
    t.done()
    print(dict(kinds), dict(skipped))


if __name__ == '__main__':
    main()
