#!/usr/bin/env python3
"""gen_struct.py SEED COUNT [--break]: blocks, if/elsif/else, unless, statement
modifiers, and where a `my` is visible: shadowing in nested blocks, a `my` in a
condition (seen in the chain's later conditions and blocks, not in the rest of
its own condition, not after the chain), `my $x = $x`. Values are small
integers, so little faults. --break makes a condition's `my` visible at once."""
import random, sys, collections
import model, harness
from model import lit

NAMES = ['x', 'y', 'z', 'n', 'm']


class G:
    def __init__(self, r):
        self.r = r
        self.scopes = [set()]

    def visible(self):
        out = set()
        for s in self.scopes: out |= s
        return sorted(out)

    def atom(self):
        vis = self.visible()
        if vis and self.r.random() < 0.7: return ('var', self.r.choice(vis))
        return lit(self.r.choice(['0', '1', '2', '3', '5', '7']))

    def expr(self, d=2):
        r = self.r
        if d <= 0: return self.atom()
        c = r.random()
        vis = self.visible()
        if c < 0.3: return self.atom()
        if c < 0.55: return ('bin', r.choice(['+', '-', '*', '.', '+']), self.expr(d - 1), self.expr(d - 1))
        if c < 0.65: return ('bin', r.choice(['==', '<', '>', '!=', 'eq']), self.expr(d - 1), self.expr(d - 1))
        if c < 0.72: return ('log', r.choice(['&&', '||', '//']), self.expr(d - 1), self.expr(d - 1))
        if c < 0.78: return ('tern', self.expr(d - 1), self.expr(d - 1), self.expr(d - 1))
        if c < 0.82: return ('not', self.expr(d - 1))
        if vis and c < 0.90: return ('asg', r.choice(['=', '+=', '-=', '.=', '||=', '*=']), ('var', r.choice(vis)), self.expr(d - 1))
        if vis and c < 0.96: return (r.choice(['pre', 'post']), r.choice(['++', '--']), r.choice(vis))
        return self.atom()

    def cond(self, chain):
        """A condition; `chain` is the chain's scope (a set) or None for a modifier."""
        r = self.r
        if chain is None or r.random() < 0.55:
            e = self.expr(2)
            return ('bin', '>', e, lit(r.choice(['0', '2', '5']))) if r.random() < 0.5 else e
        fresh = [n for n in NAMES if n not in chain]
        if not fresh: return self.expr(2)
        n = r.choice(fresh)
        rhs = self.expr(1)
        if not model.has_var(rhs): rhs = ('bin', '+', rhs, ('var', self.visible()[0])) if self.visible() else None
        if rhs is None: return self.expr(2)
        decl = ('asg', '=', ('my', n), rhs)
        c = r.random()
        # the rest of the condition is made while the new name is not yet visible
        if c < 0.3: e = ('bin', r.choice(['>', '<', '==']), decl, self.expr(1))
        elif c < 0.5: e = ('bin', '>', ('bin', r.choice(['+', '*', '.']), decl, self.expr(1)), lit('3'))
        elif c < 0.6: e = ('bin', '>', ('bin', r.choice(['+', '-']), self.expr(1), decl), lit('3'))
        elif c < 0.7: e = ('not', decl)
        elif c < 0.8: e = ('log', r.choice(['&&', '||', 'and', 'or']), ('bin', '>', decl, lit('2')), self.expr(1))
        elif c < 0.9: e = ('tern', ('bin', '>', decl, lit('2')), self.expr(1), self.expr(1))
        else: e = decl
        chain.add(n)
        self.pending.append(n)
        return e

    def simple(self):
        r = self.r
        c = r.random()
        vis = self.visible()
        if c < 0.5 or not vis: return ('say', ('bin', '.', lit('"s%d:"' % r.randrange(100)), self.expr(2)))
        if c < 0.8: return ('expr', ('asg', r.choice(['=', '+=', '-=', '.=', '||=', '*=', '&&=', '//=']), ('var', r.choice(vis)), self.expr(2)))
        return ('expr', (r.choice(['pre', 'post']), r.choice(['++', '--']), r.choice(vis)))

    def body(self, depth):
        self.scopes.append(set())
        out = [self.stmt(depth) for _ in range(self.r.choice([1, 1, 2, 3]))]
        self.scopes.pop()
        return out

    def stmt(self, depth):
        r = self.r
        c = r.random()
        if c < 0.25 or not self.visible():
            fresh = [n for n in NAMES if n not in self.scopes[-1]]
            if fresh:
                n = r.choice(fresh)
                e = self.expr(2) if r.random() < 0.85 else None
                self.scopes[-1].add(n)            # after its initializer was made: not visible there
                return ('my', n, e)
        if c < 0.5 or depth <= 0: return self.simple()
        if c < 0.6: return ('block', self.body(depth - 1))
        if c < 0.85:
            chain = set()
            self.scopes.append(chain)
            arms = []
            for _ in range(r.choice([1, 1, 2, 3])):
                self.pending = []
                seen = set(chain)
                # names declared in this condition are out of sight until it is done
                cnd = None
                saved = set(chain)
                cnd = self.make_cond(chain)
                arms.append((cnd, self.body(depth - 1)))
            els = self.body(depth - 1) if r.random() < 0.5 else None
            self.scopes.pop()
            return ('if', arms, els)
        if c < 0.92:
            chain = set()
            self.scopes.append(chain)
            cnd = self.make_cond(chain)
            b = self.body(depth - 1)
            self.scopes.pop()
            return ('unless', cnd, b)
        return ('mod', self.simple(), r.choice(['if', 'unless']), self.cond(None))

    def make_cond(self, chain):
        """Make a condition whose own `my` is not visible inside it."""
        hidden = set(chain)
        self.pending = []
        # generate with the chain scope as it was; cond() adds the name to `chain`
        # only after it has made the rest, but nested expr() calls come first
        work = set(chain)
        self.scopes[-1] = work_view = set(chain)
        e = self.cond(work_view)
        # cond() added the new name to work_view after generating: make it real
        chain |= work_view
        self.scopes[-1] = chain
        return e


def ok(e, in_my_cond=False):
    return True


def program(r):
    g = G(r)
    prog = [g.stmt(3) for _ in range(r.choice([3, 4, 5, 6]))]
    prog += [('say', ('bin', '.', lit('"end %s="' % n), ('log', '//', ('var', n), lit('"u"')))) for n in sorted(g.scopes[0])]
    return prog


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    if '--break' in sys.argv:
        def target(self, t):
            if t[0] == 'var': return self.lookup(t[1])
            cell = model.Cell(t[1], model.U())
            self.scopes[-1][t[1]] = cell          # visible at once: not what perl does
            return cell
        model.Interp.target = target
    r = random.Random(seed)
    t = harness.Tally('structure and scope, seed %d' % seed, 'struct-%d.log' % seed)
    kinds = collections.Counter(); skipped = collections.Counter()
    for _ in range(count):
        p = program(r)
        if model.any_truth_refused(p): skipped['truth position'] += 1; continue
        if model.any_list_refused(p): skipped['list context'] += 1; continue
        if model.has_chain(p): skipped['chain of dots (finding)'] += 1; continue
        if model.has_append_of_assigned_concat(p): skipped['.= of assigned concat (finding)'] += 1; continue
        v = t.check(p)
        if v: kinds[v.split(':')[0] + (' Found =' if 'Found =' in v else '') + (' masks' if 'masks' in v else '')] += 1
    t.done()
    print(dict(kinds), dict(skipped))


if __name__ == '__main__':
    main()
