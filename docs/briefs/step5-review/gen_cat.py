#!/usr/bin/env python3
"""gen_cat.py: random programs made of strings: rows of dots, `.=`, `=` and `x`
among four variables, assignments inside expressions, ternaries and logical
operators with constant and variable tests. This is where perl turns several
operations into one (multiconcat, and an assignment worked straight into its
target), and where it has been found to lose an assignment. Used through
compiler.py (kind `cat`); with the model alone: gen_cat.py SEED COUNT."""
import random, sys, collections
import model, harness
from model import lit

NAMES = ['t', 'u', 'x', 'y']
STRS = ['"a"', '"b"', '"-"', '""', '"0"', '"12"', '"ab"', '1', '2', '"<"']


def var(r): return ('var', r.choice(NAMES))


def gen(r, d):
    if d <= 0: return var(r) if r.random() < 0.7 else lit(r.choice(STRS))
    c = r.random()
    if c < 0.12: return var(r)
    if c < 0.17: return lit(r.choice(STRS))
    if c < 0.50: return ('bin', '.', gen(r, d - 1), gen(r, d - 1))
    if c < 0.62: return ('asg', '=', var(r), gen(r, d - 1))
    if c < 0.70: return ('asg', '.=', var(r), gen(r, d - 1))
    if c < 0.73: return ('asg', r.choice(['x=', '||=', '//=', '&&=']), var(r), gen(r, d - 1) if r.random() < 0.5 else lit(r.choice(['1', '2'])))
    if c < 0.78: return ('bin', 'x', gen(r, d - 1), lit(r.choice(['1', '2', '0'])))
    if c < 0.84: return ('tern', lit(r.choice(['1', '0', '"a"'])) if r.random() < 0.5 else var(r), gen(r, d - 1), gen(r, d - 1))
    if c < 0.90: return ('log', r.choice(['&&', '||', '//']), lit(r.choice(['1', '0', '""'])) if r.random() < 0.5 else var(r), gen(r, d - 1))
    if c < 0.93: return ('fn1', r.choice(['uc', 'lc', 'length']), gen(r, d - 1))
    if c < 0.96: return ('paren', gen(r, d - 1))
    if c < 0.98: return ('uplus', gen(r, d - 1))
    return ('bin', r.choice(['eq', 'ne', 'lt']), gen(r, d - 1), gen(r, d - 1))


def dump():
    return [('say', ('bin', '.', lit('"%s="' % n), ('log', '//', ('var', n), lit('"undef"')))) for n in NAMES]


def program(r):
    prog = [('my', n, None if r.random() < 0.12 else lit(r.choice(STRS))) for n in NAMES]
    for _ in range(r.choice([1, 2, 2, 3])):
        d = r.choice([1, 2, 2, 3, 3])
        c = r.random()
        if c < 0.25: prog.append(('say', gen(r, d)))
        elif c < 0.50: prog.append(('expr', ('asg', '=', var(r), gen(r, d))))
        elif c < 0.80: prog.append(('expr', ('asg', '.=', var(r), gen(r, d))))
        elif c < 0.88: prog.append(('my', 'w', gen(r, d))); prog.append(('say', ('log', '//', ('var', 'w'), lit('"w undef"')))); prog += dump(); break
        elif c < 0.94: prog.append(('mod', ('expr', ('asg', '.=', var(r), gen(r, d))), r.choice(['if', 'unless']), var(r)))
        else: prog.append(('if', [(gen(r, d), [('expr', ('asg', '.=', var(r), gen(r, d)))])], None))
        prog += dump()
    return prog


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    r = random.Random(seed)
    t = harness.Tally('strings and dots, seed %d' % seed, 'cat-%d.log' % seed)
    kinds = collections.Counter(); skipped = collections.Counter()
    for _ in range(count):
        p = program(r)
        if model.any_truth_refused(p): skipped['truth position'] += 1; continue
        if model.any_list_refused(p): skipped['list context'] += 1; continue
        if model.has_chain(p): skipped['chain of dots (finding)'] += 1; continue
        if model.has_append_of_assigned_concat(p): skipped['.= of assigned concat (finding)'] += 1; continue
        v = t.check(p)
        if v: kinds[v.split(':')[0] + (' Found =' if 'Found =' in v else '')] += 1
    t.done()
    print(dict(kinds), dict(skipped))


if __name__ == '__main__':
    main()
