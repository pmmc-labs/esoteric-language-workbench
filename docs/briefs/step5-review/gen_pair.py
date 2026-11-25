#!/usr/bin/env python3
"""gen_pair.py SEED COUNT: the claim itself, on pairs. A base program (a value, then
statements of the new language, then observations) and the same program with
read-only statements inserted (before the steps, between them, on the variable
or with a copy taken after the reads). perl runs both. Where perl's outputs
differ, the model must fault in both programs at or before the first byte that
differs; otherwise the pair is a counterexample. A variant whose inserted read
itself faults in the model is counted apart: that read is not one the language
lets a program make."""
import os
import random, sys, collections
import model, harness

import gen_past
ns = vars(gen_past)
inits, reads, steps, observations = ns['inits'], ns['reads'], ns['steps'], ns['observations']


def common(a, b):
    n = 0
    while n < len(a) and n < len(b) and a[n] == b[n]: n += 1
    return n


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    if '--break' in sys.argv:
        # the check must go red: no fault for printing a whole float from 10^15 to 2^53 (D36 undone
        # for values that came out of -- only), so a value's past shows
        real = model.step
        def broken(v, sign):
            out = real(v, sign)
            if sign == -1 and out.tag == model.T_NUM:
                d = model.as_num(out)
                if d == int(d) and 1e15 <= abs(d) < model.TWO53: return model.I(int(d))
            return out
        model.step = broken
    r = random.Random(seed)
    INITS = inits()
    x, u = ('var', 'x'), ('var', 'u')
    tally = collections.Counter()
    log = open(os.path.join(harness.HERE, 'pair-%d.log' % seed), 'w')
    for _ in range(count):
        init = r.choice(INITS)
        copy = r.random() < 0.3
        v = u if copy else x
        head = [('my', 'x', init)]
        s1 = [steps(v, r) for _ in range(r.choice([1, 1, 2]))]
        s2 = [steps(v, r) for _ in range(r.choice([0, 0, 1]))]
        obs = r.choice(observations(v)) + (r.choice(observations(v)) if r.random() < 0.3 else [])
        tn = [0]
        def rs(k, w):
            out = []
            for _ in range(k):
                tn[0] += 1
                out.append(('my', 't%d' % tn[0], r.choice(reads(w))))
            return out
        r1 = rs(r.choice([1, 1, 2, 3]), x)
        r2 = rs(r.choice([0, 0, 1, 2]), v) if s2 else []
        cp = [('my', 'u', x)] if copy else []
        base = head + cp + s1 + s2 + obs
        var = head + r1 + cp + s1 + r2 + s2 + obs
        if model.any_truth_refused(var) or model.any_list_refused(var): continue
        bout, berr, bexit = harness.perl(model.source(base))
        vout, verr, vexit = harness.perl(model.source(var))
        tally['pairs'] += 1
        if bout == vout:
            tally['perl prints the same'] += 1
            continue
        tally['perl prints differently'] += 1
        c = common(bout, vout)
        mb, fb = model.run(base)
        mv, fv = model.run(var)
        ok = fb is not None and fv is not None and len(mb) <= c and len(mv) <= c
        if ok:
            tally['... and the model faults in both, in time'] += 1
            continue
        # does an inserted read fault by itself?
        _, f1 = model.run(head + r1)
        _, f2 = model.run(head + r1 + cp + s1 + r2) if fv is not None else (None, None)
        _, f2b = model.run(head + r1 + cp + s1)
        if f1 is not None or (f2 is not None and f2b is None):
            tally['... and an inserted read faults in the model (not a read the language allows)'] += 1
            continue
        tally['COUNTEREXAMPLE'] += 1
        log.write('==== base\n%s-- perl %r stderr %r\n-- model %r fault %r\n==== with reads\n%s-- perl %r stderr %r\n-- model %r fault %r\n\n' % (
            model.source(base), bout, berr, mb, fb, model.source(var), vout, verr, mv, fv))
        log.flush()
    for k, n in tally.items(): print('%7d  %s' % (n, k))


if __name__ == '__main__':
    main()
