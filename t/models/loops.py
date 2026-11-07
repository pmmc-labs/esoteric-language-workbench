#!/usr/bin/env python3
"""Model for step 2 (variables and control flow): tests 200 to 210.

Each test is a Ditto program and the output LANGUAGE.md defines for it,
worked out here by Python doing the same job natively (a `range`, a `%`,
a `break`), never by running the compiler. Ints are Python ints under
D14's rules (a result outside 64 bits is a fault, `/` truncates, `%` takes
the dividend's sign); a program that would fault is dropped or never
written, because faults are the hand-written 21x tests.

Tests 200 to 207 are fixed algorithms (sums over ranges, Collatz lengths,
primes by trial division, branching chains, break and continue, ranges at
the ends of the int range, compound assignment). Tests 208 to 210 are
random programs: a generator writes nested lets, assignments, ifs,
whiles, fors, breaks and continues over small ints, and a tiny
interpreter written from LANGUAGE.md's statement rules (block scopes, no
shadowing, a fresh loop variable per iteration, bounds evaluated once,
loop over a snapshot) says what each prints. Seeds are fixed, so reruns
are identical.

    python3 t/models/loops.py --program sums > t/200-sums.ditto
    python3 t/models/loops.py sums > t/200-sums.expected
    python3 t/models/loops.py --program collatz > t/201-collatz.ditto
    python3 t/models/loops.py collatz > t/201-collatz.expected
    python3 t/models/loops.py --program primes > t/202-primes.ditto
    python3 t/models/loops.py primes > t/202-primes.expected
    python3 t/models/loops.py --program branching > t/203-branching.ditto
    python3 t/models/loops.py branching > t/203-branching.expected
    python3 t/models/loops.py --program break-continue > t/204-break-continue.ditto
    python3 t/models/loops.py break-continue > t/204-break-continue.expected
    python3 t/models/loops.py --program range-extremes > t/205-range-extremes.ditto
    python3 t/models/loops.py range-extremes > t/205-range-extremes.expected
    python3 t/models/loops.py --program compound > t/206-compound.ditto
    python3 t/models/loops.py compound > t/206-compound.expected
    python3 t/models/loops.py --program compound-chain > t/207-compound-chain.ditto
    python3 t/models/loops.py compound-chain > t/207-compound-chain.expected
    python3 t/models/loops.py --program random-a > t/208-random-a.ditto
    python3 t/models/loops.py random-a > t/208-random-a.expected
    python3 t/models/loops.py --program random-b > t/209-random-b.ditto
    python3 t/models/loops.py random-b > t/209-random-b.expected
    python3 t/models/loops.py --program random-c > t/210-random-c.ditto
    python3 t/models/loops.py random-c > t/210-random-c.expected
"""
import random
import sys

MAX = 2**63 - 1
MIN = -(2**63)


class Stop(Exception):
    """A fault, or a program too long: the generator drops the program."""


def checked(n):
    if not MIN <= n <= MAX:
        raise Stop('integer overflow')
    return n


def trunc_div(x, y):
    q = abs(x) // abs(y)
    return q if (x < 0) == (y < 0) else -q


def apply(op, x, y):
    """The binary operator `op` ('+', '-', '*', '/', '%') on ints, as D14."""
    if op == '+': return checked(x + y)
    if op == '-': return checked(x - y)
    if op == '*': return checked(x * y)
    if y == 0: raise Stop('division by zero')
    q = checked(trunc_div(x, y))
    return q if op == '/' else x - q * y


def lit(n):
    """Source for the int n: there is no negative literal, and the
    smallest int is written as a subtraction (LANGUAGE.md, Lexical)."""
    if n == MIN: return '(-9223372036854775807 - 1)'
    return f'-{-n}' if n < 0 else str(n)


# --- Fixed tests ------------------------------------------------------------

def t_sums():
    cases = [(0, 0), (0, 1), (1, 10), (10, 1), (-5, 5), (5, 5), (-3, -1), (-1, -3),
             (0, 100), (1, 1000), (-100, 100), (7, 8), (3, 0)]
    src = ['let lo = 0', 'let hi = 0', 'let s = 0', 'let count = 0']
    out = []
    for lo, hi in cases:
        for incl in (False, True):
            src += [f'lo = {lit(lo)}', f'hi = {lit(hi)}', 's = 0', 'count = 0',
                    f'for i in lo..{"=" if incl else ""}hi {{', '  s += i', '  count += 1', '}',
                    'print(lo, hi, count, s)']
            r = range(lo, hi + (1 if incl else 0))
            out.append(f'{lo} {hi} {len(r)} {sum(r)}')
    # The bounds are evaluated once: changing n in the body changes nothing.
    src += ['let n = 3', 's = 0', 'for i in 0..n {', '  n += 1', '  s += i', '}', 'print(n, s)']
    n, s = 3, 0
    for i in range(0, n):
        n += 1
        s += i
    out.append(f'{n} {s}')
    # Bounds are expressions, left then right.
    src += ['for i in 2 * 3 - 5..(4 + 4) / 2 {', '  print(i)', '}']
    out += [str(i) for i in range(2 * 3 - 5, (4 + 4) // 2)]
    return '\n'.join(src) + '\n', ''.join(l + '\n' for l in out)


def t_collatz():
    src = '''for n in 1..=60 {
  let x = n
  let steps = 0
  let peak = x
  while x != 1 {
    if x % 2 == 0 {
      x /= 2
    } else {
      x = 3 * x + 1
    }
    steps += 1
    if x > peak { peak = x }
  }
  print(n, steps, peak)
}
let big = 837799
let steps = 0
while big != 1 {
  if big % 2 == 0 { big = big / 2 } else { big = big * 3 + 1 }
  steps += 1
}
print(steps)
'''
    out = []
    for n in range(1, 61):
        x, steps, peak = n, 0, n
        while x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            steps += 1
            peak = max(peak, x)
        out.append(f'{n} {steps} {peak}')
    x, steps = 837799, 0
    while x != 1:
        x = x // 2 if x % 2 == 0 else 3 * x + 1
        steps += 1
    out.append(str(steps))
    return src, ''.join(l + '\n' for l in out)


def t_primes():
    src = '''let count = 0
for n in 2..=200 {
  let prime = true
  let d = 2
  while d * d <= n {
    if n % d == 0 {
      prime = false
      break
    }
    d += 1
  }
  if prime {
    count += 1
    print(n)
  }
}
print(count)
let last = 0
let gaps = 0
for n in 3..=200 {
  let prime = true
  for d in 2..n {
    if d * d > n { break }
    if n % d == 0 { prime = false; break }
  }
  if not prime { continue }
  if n - last == 2 { gaps += 1 }
  last = n
}
print(gaps)
'''
    def is_prime(n):
        return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))
    ps = [n for n in range(2, 201) if is_prime(n)]
    out = [str(p) for p in ps] + [str(len(ps))]
    # Twin-prime pairs among 3..=200 (consecutive primes two apart).
    odd = [p for p in ps if p >= 3]
    out.append(str(sum(1 for a, b in zip(odd, odd[1:]) if b - a == 2)))
    return src, ''.join(l + '\n' for l in out)


def t_branching():
    rules = [(15, 1500), (7, 700), (5, 500), (3, 300)]
    # Layouts of one chain: braces on the same line, `else` on the next
    # line, and one-line blocks.
    lines = ['for n in 1..=105 {',
             '  if n % 15 == 0 {', '    print(n, 1500)',
             '  } else if n % 7 == 0 {', '    print(n, 700)',
             '  }', '  else if n % 5 == 0 { print(n, 500) }',
             '  else if n % 3 == 0 { print(n, 300) } else {', '    print(n, 0)', '  }',
             '}']
    out = []
    for n in range(1, 106):
        tag = next((t for d, t in rules if n % d == 0), 0)
        out.append(f'{n} {tag}')
    # A second chain on values, with nesting and a condition on a variable.
    lines += ['let hits = 0', 'for a in -4..=4 {', '  for b in -4..=4 {',
              '    if a < 0 {', '      if b < 0 { hits += 1 } else { hits += 10 }',
              '    } else if a == 0 {', '      hits += 100',
              '    } else {', '      if b < 0 or b > 2 { hits += 1000 }', '    }', '  }', '}', 'print(hits)']
    hits = 0
    for a in range(-4, 5):
        for b in range(-4, 5):
            if a < 0:
                hits += 1 if b < 0 else 10
            elif a == 0:
                hits += 100
            else:
                if b < 0 or b > 2:
                    hits += 1000
    out.append(str(hits))
    return '\n'.join(lines) + '\n', ''.join(l + '\n' for l in out)


def t_break_continue():
    src = '''for a in 1..=12 {
  for b in 1..=12 {
    if b < a { continue }
    if a * b > 40 { break }
    if (a + b) % 2 == 1 { continue }
    print(a, b)
  }
}
let n = 0
let total = 0
while true {
  n += 1
  if n % 2 == 0 { continue }
  if total > 100 { break }
  total += n
}
print(n, total)
let i = 0
let skipped = 0
while i < 20 {
  i += 1
  if i % 3 == 0 {
    skipped += 1
    continue
  }
  if i > 14 { break }
  print(i)
}
print(i, skipped)
let outer = 0
let inner = 0
for x in 0..5 {
  outer += 1
  for y in 0..5 {
    if y == 3 { break }
    inner += 1
  }
  if x == 3 { break }
}
print(outer, inner)
for k in 1..=5 {
  while true {
    if k % 2 == 0 { break }
    print(k)
    break
  }
}
'''
    out = []
    for a in range(1, 13):
        for b in range(1, 13):
            if b < a: continue
            if a * b > 40: break
            if (a + b) % 2 == 1: continue
            out.append(f'{a} {b}')
    n = total = 0
    while True:
        n += 1
        if n % 2 == 0: continue
        if total > 100: break
        total += n
    out.append(f'{n} {total}')
    i = skipped = 0
    while i < 20:
        i += 1
        if i % 3 == 0:
            skipped += 1
            continue
        if i > 14: break
        out.append(str(i))
    out.append(f'{i} {skipped}')
    outer = inner = 0
    for x in range(0, 5):
        outer += 1
        for y in range(0, 5):
            if y == 3: break
            inner += 1
        if x == 3: break
    out.append(f'{outer} {inner}')
    for k in range(1, 6):
        while True:
            if k % 2 == 0: break
            out.append(str(k))
            break
    return src, ''.join(l + '\n' for l in out)


def t_range_extremes():
    cases = [(MAX - 2, MAX, True), (MAX - 2, MAX, False), (MAX, MAX, True), (MAX, MAX, False),
             (MAX - 1, MAX, True), (MAX, MAX - 1, True), (MIN, MIN + 2, False), (MIN, MIN + 2, True),
             (MIN, MIN, True), (MIN, MIN, False), (MAX, MIN, True), (MAX, MIN, False),
             (MIN + 1, MIN, False), (-1, 1, True), (MIN, MIN + 1, True)]
    src, out = [], []
    for lo, hi, incl in cases:
        src += [f'let count = 0', ] if not src else []
        src += ['count = 0', f'for i in {lit(lo)}..{"=" if incl else ""}{lit(hi)} {{', '  print(i)',
                '  count += 1', '}', 'print(count)']
        r = range(lo, hi + (1 if incl else 0))
        out += [str(i) for i in r] + [str(len(r))]
    return '\n'.join(src) + '\n', ''.join(l + '\n' for l in out)


EDGE = [0, 1, -1, 7, -7, 2, 3, MAX, -MAX, MIN, MAX - 1, MIN + 1]
OPS = ['+', '-', '*', '/', '%']


def t_compound():
    src = ['let x = 0']
    out = []
    for op in OPS:
        for a in EDGE:
            for b in EDGE:
                try:
                    v = apply(op, a, b)
                except Stop:
                    continue
                src += [f'x = {lit(a)}', f'x {op}= {lit(b)}', 'print(x)']
                out.append(str(v))
    # The right side sees the variable's old value, and `x op= x` is fine.
    src += ['x = 6', 'x += x', 'x *= x', 'x -= x + 1', 'x %= 5', 'print(x)']
    x = 6; x += x; x *= x; x -= x + 1; x = apply('%', x, 5)
    out.append(str(x))
    return '\n'.join(src) + '\n', ''.join(l + '\n' for l in out)


def t_compound_chain():
    rng = random.Random(207)
    src = ['let x = 1', 'let y = -3', 'print(x, y)']
    out = ['1 -3']
    vals = {'x': 1, 'y': -3}
    while len(src) < 400:
        name = rng.choice('xy')
        op = rng.choice(OPS)
        if rng.random() < 0.3:
            rhs_src, rhs = ('y' if name == 'x' else 'x'), vals['y' if name == 'x' else 'x']
        else:
            rhs = rng.choice([-9, -2, -1, 1, 2, 3, 5, 10, 1000, 123456789])
            rhs_src = lit(rhs)
        try:
            v = apply(op, vals[name], rhs)
        except Stop:
            continue
        vals[name] = v
        src += [f'{name} {op}= {rhs_src}', 'print(x, y)']
        out.append(f'{vals["x"]} {vals["y"]}')
    return '\n'.join(src) + '\n', ''.join(l + '\n' for l in out)


# --- Random programs --------------------------------------------------------
#
# Expressions: ('n', k), ('v', name), (op, l, r).  Conditions: ('cmp', op, l,
# r), ('and' | 'or', c, c), ('not', c).  Statements: ('let', name, e),
# ('set', name, op, e), ('print', [e]), ('if', cond, then, else_or_None),
# ('while', cond, body), ('for', var, lo, hi, inclusive, body), ('break',),
# ('continue',).

POOL = list('abcdefghijk')
CMPS = ['==', '!=', '<', '<=', '>', '>=']


def gen_expr(rng, visible, d):
    if d == 0 or rng.random() < 0.35:
        if visible and rng.random() < 0.6:
            return ('v', rng.choice(visible))
        return ('n', rng.randrange(-5, 13))
    op = rng.choice(['+', '+', '-', '-', '*', '/', '%'])
    if op in ('*', '/', '%'):
        return (op, gen_expr(rng, visible, d - 1), ('n', rng.choice([-3, -2, 1, 2, 3, 4, 5, 7])))
    return (op, gen_expr(rng, visible, d - 1), gen_expr(rng, visible, d - 1))


def gen_cond(rng, visible, d):
    r = rng.random()
    if d == 0 or r < 0.55:
        return ('cmp', rng.choice(CMPS), gen_expr(rng, visible, 1), gen_expr(rng, visible, 1))
    if r < 0.7: return ('not', gen_cond(rng, visible, d - 1))
    return (rng.choice(['and', 'or']), gen_cond(rng, visible, d - 1), gen_cond(rng, visible, d - 1))


def gen_block(rng, visible, protected, in_loop, depth, n):
    """n statements; names declared here are visible to the ones after."""
    visible = list(visible)
    out = []
    for _ in range(n):
        for s in gen_stmt(rng, visible, protected, in_loop, depth):
            out.append(s)
            if s[0] == 'let': visible.append(s[1])
    return out


def fresh(rng, visible):
    free = [n for n in POOL if n not in visible]
    return rng.choice(free) if free else None


def gen_stmt(rng, visible, protected, in_loop, depth):
    r = rng.random()
    assignable = [v for v in visible if v not in protected]
    if r < 0.20:
        name = fresh(rng, visible)
        if name: return [('let', name, gen_expr(rng, visible, 2))]
    elif r < 0.45:
        if assignable:
            op = rng.choice(['=', '+=', '-=', '*=', '/=', '%='])
            if op in ('*=', '/=', '%='):
                e = ('n', rng.choice([-3, -2, 1, 2, 3, 5, 7]))
            else:
                e = gen_expr(rng, visible, 2)
            return [('set', rng.choice(assignable), op, e)]
    elif r < 0.62:
        return [('print', [gen_expr(rng, visible, 2) for _ in range(rng.randrange(1, 4))])]
    elif r < 0.78 and depth < 3:
        then = gen_block(rng, visible, protected, in_loop, depth + 1, rng.randrange(1, 4))
        els = None
        if rng.random() < 0.6:
            if rng.random() < 0.4:
                els = gen_stmt_if(rng, visible, protected, in_loop, depth + 1)
            else:
                els = gen_block(rng, visible, protected, in_loop, depth + 1, rng.randrange(1, 3))
        return [('if', gen_cond(rng, visible, 2), then, els)]
    elif r < 0.84 and depth < 3:
        w = fresh(rng, visible)
        if w:
            body = gen_block(rng, visible + [w], protected | {w}, True, depth + 1, rng.randrange(1, 4))
            return [('let', w, ('n', 0)),
                    ('while', ('cmp', '<', ('v', w), ('n', rng.randrange(1, 6))),
                     [('set', w, '+=', ('n', 1))] + body)]
    elif r < 0.93 and depth < 3:
        var = fresh(rng, visible)
        if var:
            lo, hi = gen_expr(rng, visible, 1), gen_expr(rng, visible, 1)
            body = gen_block(rng, visible + [var], protected, True, depth + 1, rng.randrange(1, 4))
            return [('for', var, lo, hi, rng.random() < 0.5, body)]
    elif in_loop and r < 0.97:
        return [('break',)] if rng.random() < 0.5 else [('continue',)]
    return [('print', [gen_expr(rng, visible, 1)])]


def gen_stmt_if(rng, visible, protected, in_loop, depth):
    then = gen_block(rng, visible, protected, in_loop, depth + 1, rng.randrange(1, 3))
    els = None
    if depth < 3 and rng.random() < 0.5:
        els = gen_block(rng, visible, protected, in_loop, depth + 1, 1)
    return [('if', gen_cond(rng, visible, 1), then, els)]


class Break(Exception): pass
class Continue(Exception): pass


class Interp:
    """LANGUAGE.md's rules for blocks, lets, assignment, if, while, for."""

    def __init__(self):
        self.scopes = [{}]
        self.out = []
        self.steps = 0

    def tick(self):
        self.steps += 1
        if self.steps > 4000 or len(self.out) > 200:
            raise Stop('too long')

    def lookup(self, name):
        for s in reversed(self.scopes):
            if name in s: return s
        raise AssertionError(f'unknown variable {name}')

    def expr(self, e):
        if e[0] == 'n': return e[1]
        if e[0] == 'v': return self.lookup(e[1])[e[1]]
        return apply(e[0], self.expr(e[1]), self.expr(e[2]))

    def cond(self, c):
        k = c[0]
        if k == 'cmp':
            x, y = self.expr(c[2]), self.expr(c[3])
            return {'==': x == y, '!=': x != y, '<': x < y, '<=': x <= y, '>': x > y, '>=': x >= y}[c[1]]
        if k == 'not': return not self.cond(c[1])
        l = self.cond(c[1])
        if k == 'and': return l and self.cond(c[2])
        return l or self.cond(c[2])

    def block(self, stmts, first=None):
        self.scopes.append({} if first is None else dict(first))
        try:
            for s in stmts: self.stmt(s)
        finally:
            self.scopes.pop()

    def stmt(self, s):
        self.tick()
        k = s[0]
        if k == 'let':
            assert all(s[1] not in sc for sc in self.scopes), 'already declared'
            v = self.expr(s[2])
            self.scopes[-1][s[1]] = v
        elif k == 'set':
            cur = self.lookup(s[1])
            if s[2] == '=':
                v = self.expr(s[3])
            else:
                v = apply(s[2][0], cur[s[1]], self.expr(s[3]))
            cur[s[1]] = v
        elif k == 'print':
            self.out.append(' '.join(str(self.expr(e)) for e in s[1]))
        elif k == 'if':
            if self.cond(s[1]): self.block(s[2])
            elif s[3] is not None: self.block(s[3])
        elif k == 'while':
            while self.cond(s[1]):
                self.tick()
                try: self.block(s[2])
                except Continue: pass
                except Break: break
        elif k == 'for':
            lo, hi = self.expr(s[2]), self.expr(s[3])      # both, once, left to right
            for i in range(lo, hi + (1 if s[4] else 0)):
                self.tick()
                try: self.block(s[5], {s[1]: i})            # a fresh variable each time
                except Continue: pass
                except Break: break
        elif k == 'break': raise Break
        elif k == 'continue': raise Continue
        else: raise AssertionError(k)


def etext(e, top=False):
    if e[0] == 'n': return lit(e[1])
    if e[0] == 'v': return e[1]
    s = f'{etext(e[1])} {e[0]} {etext(e[2])}'
    return s if top else f'({s})'


def ctext(c, top=False):
    k = c[0]
    if k == 'cmp': s = f'{etext(c[2])} {c[1]} {etext(c[3])}'
    elif k == 'not': return f'not ({ctext(c[1], True)})'
    else: s = f'({ctext(c[1], True)}) {k} ({ctext(c[2], True)})'
    return s


def is_simple(s): return s[0] in ('let', 'set', 'print', 'break', 'continue')


def stext(s):
    k = s[0]
    if k == 'let': return f'let {s[1]} = {etext(s[2], True)}'
    if k == 'set': return f'{s[1]} {s[2]} {etext(s[3], True)}'
    if k == 'print': return 'print(' + ', '.join(etext(e, True) for e in s[1]) + ')'
    return k


class Printer:
    def __init__(self, rng): self.rng = rng

    def stmts(self, stmts, ind):
        lines, i = [], 0
        while i < len(stmts):
            s = stmts[i]
            # Sometimes two simple statements share a line, joined by `;`.
            if (is_simple(s) and i + 1 < len(stmts) and is_simple(stmts[i + 1])
                    and self.rng.random() < 0.2):
                lines.append(f'{ind}{stext(s)}; {stext(stmts[i + 1])}')
                i += 2
                continue
            lines += self.stmt(s, ind)
            i += 1
        return lines

    def stmt(self, s, ind, prefix=None):
        k = s[0]
        if is_simple(s): return [ind + stext(s)]
        if k == 'if': return self.if_(s, ind, ind)
        if k == 'while':
            return self.loop(f'{ind}while {ctext(s[1])}', s[2], ind)
        lo, hi = etext(s[2], True), etext(s[3], True)
        return self.loop(f'{ind}for {s[1]} in {lo}..{"=" if s[4] else ""}{hi}', s[5], ind)

    def loop(self, head, body, ind):
        if len(body) == 1 and is_simple(body[0]) and self.rng.random() < 0.3:
            return [f'{head} {{ {stext(body[0])} }}']
        return [head + ' {'] + self.stmts(body, ind + '  ') + [ind + '}']

    def if_(self, s, ind, prefix):
        _, cond, then, els = s
        if els is None and len(then) == 1 and is_simple(then[0]) and self.rng.random() < 0.3:
            return [f'{prefix}if {ctext(cond)} {{ {stext(then[0])} }}']
        out = [f'{prefix}if {ctext(cond)} {{'] + self.stmts(then, ind + '  ')
        if els is None: return out + [ind + '}']
        next_line = self.rng.random() < 0.4          # `else` on the line after the `}`
        if len(els) == 1 and els[0][0] == 'if' and self.rng.random() < 0.7:
            if next_line: return out + [ind + '}'] + self.if_(els[0], ind, ind + 'else ')
            return out + self.if_(els[0], ind, ind + '} else ')
        if next_line: out += [ind + '}', ind + 'else {']
        else: out.append(ind + '} else {')
        return out + self.stmts(els, ind + '  ') + [ind + '}']


def t_random(name):
    seed = 0
    while True:
        seed += 1
        rng = random.Random(f'{name}-{seed}')
        prog = []
        visible = []
        for _ in range(11):
            for s in gen_stmt(rng, visible, set(), False, 0):
                prog.append(s)
                if s[0] == 'let': visible.append(s[1])
        names = [s[1] for s in prog if s[0] == 'let']
        if not names: continue
        prog.append(('print', [('v', n) for n in names]))
        it = Interp()
        try:
            for s in prog: it.stmt(s)
        except Stop:
            continue
        if not 15 <= len(it.out) <= 150: continue
        lines = Printer(random.Random(f'{name}-print-{seed}')).stmts(prog, '')
        return '\n'.join(lines) + '\n', ''.join(l + '\n' for l in it.out)


TESTS = {
    'sums': t_sums, 'collatz': t_collatz, 'primes': t_primes, 'branching': t_branching,
    'break-continue': t_break_continue, 'range-extremes': t_range_extremes,
    'compound': t_compound, 'compound-chain': t_compound_chain,
    'random-a': lambda: t_random('a'), 'random-b': lambda: t_random('b'),
    'random-c': lambda: t_random('c'),
}


def main(argv):
    program = '--program' in argv
    names = [a for a in argv if not a.startswith('--')]
    if len(names) != 1 or names[0] not in TESTS:
        sys.exit('usage: loops.py [--program] ' + '|'.join(TESTS))
    src, expected = TESTS[names[0]]()
    sys.stdout.write(src if program else expected)


main(sys.argv[1:])
