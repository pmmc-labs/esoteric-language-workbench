#!/usr/bin/env python3
"""gen_alias.py: the target of an assignment among its own operands, every
operator and builtin, exhaustively: `$x = A op B`, `$x op= A`, `my $w = ...`,
with A and B from $x, $y, ($x), a literal. perl computes into the target
directly (TARGMY, padsv_store); the model does not know that."""
import itertools, collections
import model, harness
from model import lit

x, y = ('var', 'x'), ('var', 'y')
ATOMS = [x, y, ('paren', x), lit('2'), lit('"ab"'), ('uplus', y)]
BIN = ['+', '-', '*', '/', '%', '**', '.', 'x', '==', '!=', '<', '>', '<=', '>=', '<=>', 'eq', 'ne', 'lt', 'gt', 'le', 'ge', 'cmp', 'xor']
LOG = ['&&', '||', '//']
OPASG = ['+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//=']
INITS = [('3', '2'), ('"ab"', '2'), ('2', '"abc"'), ('1.5', '3'), ('"12"', '"3"'), (None, '1'), ('0', None), ('true', '"1"')]


def exprs():
    for a, b in itertools.product(ATOMS, ATOMS):
        for op in BIN: yield ('bin', op, a, b)
        for op in LOG: yield ('log', op, a, b)
        yield ('fn', 'substr', [a, b])
        yield ('fn', 'index', [a, b])
        yield ('tern', a, b, a)
    for a in ATOMS:
        yield ('neg', a); yield ('not', a); yield ('fn1', 'length', a); yield ('fn1', 'uc', a); yield ('fn1', 'defined', a)
        yield ('fn1', 'ord', a); yield ('fn1', 'chr', a); yield ('fn1', 'lc', a)
        yield ('fn', 'substr', [a, lit('0'), lit('1')]); yield ('fn', 'substr', [a, a, a]); yield ('fn', 'index', [a, a, a])
        yield ('bin', '.', a, ('bin', '.', a, a)); yield ('bin', '+', a, ('bin', '*', a, a))


def main():
    t = harness.Tally('the target among its operands', 'alias.log')
    kinds = collections.Counter(); skipped = collections.Counter()
    tail = [('say', ('log', '//', x, lit('"x undef"'))), ('say', ('log', '//', y, lit('"y undef"')))]
    n = [0]
    for e in exprs():
        bodies = [[('expr', ('asg', '=', x, e))], [('expr', ('asg', '=', y, e))], [('my', 'w', e), ('say', ('log', '//', ('var', 'w'), lit('"u"')))],
                  [('say', ('asg', '=', x, e))], [('expr', ('asg', '=', x, ('asg', '=', y, e)))]]
        bodies += [[('expr', ('asg', op, x, e))] for op in OPASG]
        bodies += [[('say', ('asg', op, x, e))] for op in ('+=', '.=', 'x=')]
        for body in bodies:
            n[0] += 1
            for ix, iy in [INITS[(n[0] + k) % len(INITS)] for k in range(3)]:
                p = [('my', 'x', None if ix is None else lit(ix)), ('my', 'y', None if iy is None else lit(iy))] + body + tail
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
