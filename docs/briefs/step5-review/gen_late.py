#!/usr/bin/env python3
"""gen_late.py SEED COUNT [--break]: random programs about late reads, assignment
as an operator, ++/--, OP=, the logical operators and builtins over variables.
Each is held to the rule by harness.py. --break makes the model read every
operand when it is reached (the checker must then go red)."""
import random, sys, collections
import model, harness
from model import lit

NAMES = ['x', 'y', 'z']
INITS = ['0', '1', '2', '3', '5', '7', '12', '"a"', '"ab"', '"7"', '"0"', '""', '"3.5"', '"10"', '1.5', '2.0', '0.5',
         'true', 'false', None, None, '"2"', '4', '9']
LITS = ['0', '1', '2', '3', '5', '"a"', '"b"', '"7"', '""', '1.5', 'true', 'false', 'undef', '"0"', '2', '2']
ARITH = ['+', '-', '*', '.', '.', '+', 'x', '/', '%', '**']
CMP = ['==', '!=', '<', '>', '<=', '>=', '<=>', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cmp']
LOG = ['&&', '||', '//', 'and', 'or']
OPASG = ['+=', '-=', '*=', '.=', 'x=', '/=', '%=', '**=', '||=', '&&=', '//=', '+=', '.=', '-=']


def var(r): return ('var', r.choice(['x', 'x', 'x', 'y', 'y', 'z']))


def gen(r, d):
    if d <= 0:
        c = r.random()
        if c < 0.6: return var(r)
        if c < 0.7: return ('paren', var(r))
        if c < 0.75: return ('uplus', var(r))
        return lit(r.choice(LITS))
    c = r.random()
    if c < 0.10: return var(r)
    if c < 0.25: return ('asg', '=', var(r), gen(r, d - 1))
    if c < 0.35: return ('asg', r.choice(OPASG), var(r), gen(r, d - 1))
    if c < 0.45: return (r.choice(['pre', 'post']), r.choice(['++', '--']), r.choice(NAMES))
    if c < 0.65:
        op = r.choice(ARITH)
        b = gen(r, d - 1)
        if op in ('x', '**') and r.random() < 0.7: b = lit(r.choice(['0', '1', '2', '3']))
        return ('bin', op, gen(r, d - 1), b)
    if c < 0.72: return ('bin', r.choice(CMP), gen(r, d - 1), gen(r, d - 1))
    if c < 0.80: return ('log', r.choice(LOG), gen(r, d - 1), gen(r, d - 1))
    if c < 0.86: return ('tern', gen(r, d - 1), gen(r, d - 1), gen(r, d - 1))
    if c < 0.89: return ('neg', gen(r, d - 1))
    if c < 0.92: return ('not', gen(r, d - 1))
    if c < 0.94: return ('fn1', r.choice(['defined', 'length', 'length', 'uc', 'ord']), gen(r, d - 1))
    if c < 0.96: return ('bin', 'xor', gen(r, d - 1), gen(r, d - 1))
    if c < 0.98: return ('paren', gen(r, d - 1))
    n = r.choice([2, 3])
    return ('fn', r.choice(['substr', 'index']), [gen(r, d - 1) for _ in range(n)])


def whole_x(e):
    """`(...) x N` as the whole of what say is given is a list to perl, and refused."""
    while e[0] == 'paren': e = e[1]
    return e[0] == 'bin' and e[1] == 'x' and e[2][0] not in ('lit', 'var', 'fn', 'fn1')


def dump(r):
    return [('say', ('tern', ('fn1', 'defined', ('var', n)), ('bin', '.', lit('"%s="' % n), ('var', n)), lit('"%s undef"' % n))) for n in NAMES]


def program(r):
    prog = [('my', n, None if (i := r.choice(INITS)) is None else lit(i)) for n in NAMES]
    for _ in range(r.choice([1, 1, 2, 3])):
        d = r.choice([1, 2, 2, 3, 3, 4])
        c = r.random()
        if c < 0.55:
            e = gen(r, d)
            if whole_x(e): continue
            prog.append(('say', e))
        elif c < 0.75: prog.append(('expr', ('asg', '=', var(r), gen(r, d))))
        elif c < 0.9: prog.append(('expr', ('asg', r.choice(OPASG), var(r), gen(r, d))))
        else: prog.append(('expr', (r.choice(['pre', 'post']), r.choice(['++', '--']), r.choice(NAMES))))
        prog += dump(r)
    return prog


BREAK_KEEP = ('var', 'asg', 'pre')


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    global BREAK_KEEP
    if '--break-all' in sys.argv: BREAK_KEEP = ()
    if '--break' in sys.argv or '--break-all' in sys.argv:
        real = model.Interp.ev
        def eager(self, e):
            v = real(self, e)
            return v if e[0] in BREAK_KEEP else model.rd(v)
        model.Interp.ev = eager
    r = random.Random(seed)
    t = harness.Tally('late reads, seed %d' % seed, 'late-%d.log' % seed)
    kinds = collections.Counter()
    skipped = 0
    for _ in range(count):
        p = program(r)
        if model.any_truth_refused(p): continue          # the proposal refuses it
        if model.any_list_refused(p): continue           # the built compiler refuses it (T104)
        if '--past' in sys.argv and (model.has_chain(p) or model.has_append_of_assigned_concat(p)):
            skipped += 1; continue                       # findings already made
        v = t.check(p)
        if v: kinds[v.split(':')[0] + (' Found =' if 'Found =' in v else '')] += 1
    t.done()
    print(dict(kinds), 'skipped as known findings:', skipped)


if __name__ == '__main__':
    main()
