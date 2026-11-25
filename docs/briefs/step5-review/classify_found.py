#!/usr/bin/env python3
"""classify_found.py SEED COUNT: regenerate gen_struct's programs (no perl) and
hold perl's "Found = in conditional" to a rule: perl warns exactly when a truth
position holds, behind brackets, unary plus and at most one `!`/`not`, a plain
`=` whose right side perl folds to a constant. Reads struct-SEED.log for the
programs perl warned on."""
import os
import sys, random, re
import model, harness

import gen_struct
ns = vars(gen_struct)


def strip(e):
    while e[0] in ('paren', 'uplus'): e = e[1]
    return e


def const_truth(e):
    """None if perl does not fold e; else its truth (roughly: literals only)."""
    e = strip(e)
    if e[0] == 'lit':
        if e[2] == 'u': return None        # undef is an op, not a constant
        if e[2] == 'i' or e[2] == 'n': return e[3] != 0
        if e[2] == 's': return e[3] not in ('', '0')
        return bool(e[3])
    return None


def fold(e):
    """What perl leaves of e after folding constant conditions: e itself, or the operand taken."""
    e = strip(e)
    if e[0] == 'log':
        t = const_truth(fold(e[2])) if fold(e[2])[0] == 'lit' else None
        if t is None: return e
        if e[1] in ('&&', 'and'): return fold(e[3]) if t else fold(e[2])
        if e[1] in ('||', 'or'): return fold(e[2]) if t else fold(e[3])
        return fold(e[2])                  # a defined constant // anything
    if e[0] == 'tern':
        t = const_truth(fold(e[1])) if fold(e[1])[0] == 'lit' else None
        if t is None: return e
        return fold(e[2]) if t else fold(e[3])
    return e


def is_const(e):
    e = fold(e)
    if e[0] == 'lit': return e[2] != 'u'
    if e[0] in ('neg', 'not'): return is_const(e[1])
    if e[0] == 'bin': return is_const(e[2]) and is_const(e[3])
    if e[0] == 'fn1' and e[1] != 'defined': return is_const(e[2])
    return False


def warns_here(e):
    e = fold(e)
    if e[0] in ('not', 'lnot'): e = fold(e[1])
    return e[0] == 'asg' and e[1] == '=' and is_const(e[3])


def warns(x):
    if isinstance(x, list): return any(warns(y) for y in x)
    if not isinstance(x, tuple) or not x: return False
    k = x[0]
    if k == 'if': return any(warns_here(c) or warns(c) or warns(b) for c, b in x[1]) or (x[2] is not None and warns(x[2]))
    if k == 'unless': return warns_here(x[1]) or warns(x[1]) or warns(x[2])
    if k == 'mod': return warns_here(x[3]) or warns(x[3]) or warns(x[1])
    if k == 'tern' and const_truth(fold(x[1])) is None and warns_here(x[1]): return True
    if k == 'log' and warns_here(x[2]): return True
    return any(warns(y) for y in x[1:] if isinstance(y, (tuple, list)))


seed, count = int(sys.argv[1]), int(sys.argv[2])
warned = set()
for blk in open(os.path.join(harness.HERE, 'struct-%d.log' % seed)).read().split('----\n')[1:]:
    s, _, v = blk.partition('## ')
    if 'Found =' in v: warned.add(s)
r = random.Random(seed)
both = only_perl = only_rule = neither = 0
for _ in range(count):
    p = ns['program'](r)
    if model.any_truth_refused(p) or model.any_list_refused(p) or model.has_chain(p) or model.has_append_of_assigned_concat(p): continue
    s = model.source(p)
    w, pw = warns(p), s in warned
    if w and pw: both += 1
    elif pw:
        only_perl += 1
        if only_perl <= 3: print('PERL WARNS, THE RULE DOES NOT:\n' + s)
    elif w:
        only_rule += 1
        if only_rule <= 3: print('THE RULE SAYS PERL WARNS, IT DID NOT:\n' + s)
    else: neither += 1
print('perl warns and the rule says so: %d; perl only: %d; the rule only: %d; neither: %d' % (both, only_perl, only_rule, neither))
