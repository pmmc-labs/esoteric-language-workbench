#!/usr/bin/env python3
"""Model for step 3 (functions): tests 300 to 310.

Each test is a Ditto program and the output LANGUAGE.md defines for it,
worked out here by Python doing the same job natively (`math.gcd`,
`math.factorial`, `math.comb`, a Python function with the same shape),
never by running the compiler. Ints are Python ints under D14's rules:
every `+ - *` in a mirrored function goes through `checked`, or is small
enough not to need it, so a test that would overflow stops the model
instead of printing a wrong line (the faults are the hand-written 31x
tests). A call nested more than 1000 deep is a fault, so every program
here stays at or under 1000 nested calls.

Tests 300 to 307 are fixed programs: Euclid's gcd, factorial, Fibonacci,
Ackermann for small arguments, mutual recursion, a parameter reassigned
inside the function not changing the caller's variable, hoisting, and the
shapes of `return`. Test 308 makes 1000 nested calls (the most allowed),
several times, to check the depth counter comes back down. Tests 309 and
310 are random programs: a generator writes functions whose bodies hold
lets, assignments, ifs, for loops, early returns and calls to functions
written above them, and a tiny interpreter written from LANGUAGE.md's
rules (arguments evaluated left to right, then the call; a fresh frame per
call; `return` leaves the function) says what the top-level prints show.
Seeds are fixed, so reruns are identical.

    python3 t/models/functions.py --program gcd > t/300-gcd.ditto
    python3 t/models/functions.py gcd > t/300-gcd.expected
    python3 t/models/functions.py --program factorial > t/301-factorial.ditto
    python3 t/models/functions.py factorial > t/301-factorial.expected
    python3 t/models/functions.py --program fibonacci > t/302-fibonacci.ditto
    python3 t/models/functions.py fibonacci > t/302-fibonacci.expected
    python3 t/models/functions.py --program ackermann > t/303-ackermann.ditto
    python3 t/models/functions.py ackermann > t/303-ackermann.expected
    python3 t/models/functions.py --program mutual > t/304-mutual.ditto
    python3 t/models/functions.py mutual > t/304-mutual.expected
    python3 t/models/functions.py --program param-copy > t/305-param-copy.ditto
    python3 t/models/functions.py param-copy > t/305-param-copy.expected
    python3 t/models/functions.py --program hoisting > t/306-hoisting.ditto
    python3 t/models/functions.py hoisting > t/306-hoisting.expected
    python3 t/models/functions.py --program returns > t/307-returns.ditto
    python3 t/models/functions.py returns > t/307-returns.expected
    python3 t/models/functions.py --program deep > t/308-deep-ok.ditto
    python3 t/models/functions.py deep > t/308-deep-ok.expected
    python3 t/models/functions.py --program random-a > t/309-random-a.ditto
    python3 t/models/functions.py random-a > t/309-random-a.expected
    python3 t/models/functions.py --program random-b > t/310-random-b.ditto
    python3 t/models/functions.py random-b > t/310-random-b.expected
"""
import math
import random
import sys

sys.setrecursionlimit(20000)

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


def show(v):
    """The printed form of an int, bool or nil."""
    if v is None: return 'nil'
    if v is True: return 'true'
    if v is False: return 'false'
    return str(v)


def lines(out):
    return ''.join(l + '\n' for l in out)


# --- Fixed tests ------------------------------------------------------------

def t_gcd():
    src = '''// Euclid's algorithm, by loop and by recursion.
fn gcd(a, b) {
  while b != 0 {
    let t = b
    b = a % b
    a = t
  }
  return a
}

fn gcd_rec(a, b) {
  if b == 0 { return a }
  return gcd_rec(b, a % b)
}

fn lcm(a, b) {
  return a / gcd(a, b) * b
}

'''
    pairs = [(12, 18), (18, 12), (0, 5), (5, 0), (1, 1), (17, 5), (100, 75), (1071, 462),
             (7, 7), (1, 1000), (2**40, 6**20), (123456789, 987654321), (MAX, 3), (MAX, MAX),
             (MAX, MAX - 1), (46368, 28657), (360, 84), (1000000007, 998244353)]
    src_lines, out = [], []
    for a, b in pairs:
        src_lines.append(f'print({a}, {b}, gcd({a}, {b}), gcd_rec({a}, {b}))')
        out.append(f'{a} {b} {math.gcd(a, b)} {math.gcd(a, b)}')
    src_lines.append('')
    for a, b in [(12, 18), (4, 6), (21, 6), (1, 9), (8, 9), (1000, 1500), (123456, 7890)]:
        src_lines.append(f'print(lcm({a}, {b}))')
        out.append(str(math.lcm(a, b)))
    # Arguments are expressions, evaluated before the call.
    src_lines += ['', 'print(gcd(2 * 3 * 7, 7 * 5 * 3), gcd_rec(gcd(48, 36), gcd(90, 60)))']
    out.append(f'{math.gcd(2 * 3 * 7, 7 * 5 * 3)} {math.gcd(math.gcd(48, 36), math.gcd(90, 60))}')
    return src + '\n'.join(src_lines) + '\n', lines(out)


def t_factorial():
    src = '''fn fact(n) {
  if n == 0 { return 1 }
  return n * fact(n - 1)
}

fn fact_loop(n) {
  let r = 1
  for i in 2..=n { r *= i }
  return r
}

fn binomial(n, k) {
  return fact(n) / (fact(k) * fact(n - k))
}

for n in 0..=20 {
  print(n, fact(n), fact_loop(n))
}

for n in 0..=8 {
  for k in 0..=n {
    print(n, k, binomial(n, k))
  }
}
print(binomial(20, 10), binomial(20, 1), binomial(15, 7))
'''
    out = []
    for n in range(21):
        out.append(f'{n} {math.factorial(n)} {math.factorial(n)}')
    for n in range(9):
        for k in range(n + 1):
            out.append(f'{n} {k} {math.comb(n, k)}')
    out.append(f'{math.comb(20, 10)} {math.comb(20, 1)} {math.comb(15, 7)}')
    return src, lines(out)


def t_fibonacci():
    src = '''fn fib(n) {
  if n < 2 { return n }
  return fib(n - 1) + fib(n - 2)
}

fn fib_iter(n) {
  let a = 0
  let b = 1
  for i in 0..n {
    let t = a + b
    a = b
    b = t
  }
  return a
}

// Carries the last two values along, so it is one call per step.
fn fib_acc(n, a, b) {
  if n == 0 { return a }
  return fib_acc(n - 1, b, a + b)
}

for n in 0..=20 {
  print(n, fib(n), fib_iter(n), fib_acc(n, 0, 1))
}
for n in 85..=91 {
  print(n, fib_iter(n), fib_acc(n, 0, 1))
}
print(fib(24) == fib_iter(24), fib(10) + fib(11) == fib(12), fib(12) - fib(11) == fib(10))
'''
    def fib(n):
        return n if n < 2 else checked(fib(n - 1) + fib(n - 2))

    def fib_iter(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, checked(a + b)
        return a

    def fib_acc(n, a, b):
        return a if n == 0 else fib_acc(n - 1, b, checked(a + b))

    out = [f'{n} {fib(n)} {fib_iter(n)} {fib_acc(n, 0, 1)}' for n in range(21)]
    out += [f'{n} {fib_iter(n)} {fib_acc(n, 0, 1)}' for n in range(85, 92)]
    out.append(' '.join(show(x) for x in (
        fib(24) == fib_iter(24), fib(10) + fib(11) == fib(12), fib(12) - fib(11) == fib(10))))
    return src, lines(out)


def t_ackermann():
    src = '''fn ack(m, n) {
  if m == 0 { return n + 1 }
  if n == 0 { return ack(m - 1, 1) }
  return ack(m - 1, ack(m, n - 1))
}

for m in 0..=3 {
  for n in 0..=5 {
    print(m, n, ack(m, n))
  }
}
print(ack(2, 20), ack(3, 6))
'''
    # The deepest nesting for these arguments is 511, under the limit of 1000.
    def ack(m, n):
        if m == 0: return n + 1
        if n == 0: return ack(m - 1, 1)
        return ack(m - 1, ack(m, n - 1))

    out = [f'{m} {n} {ack(m, n)}' for m in range(4) for n in range(6)]
    out.append(f'{ack(2, 20)} {ack(3, 6)}')
    return src, lines(out)


def t_mutual():
    src = '''fn is_even(n) {
  if n == 0 { return true }
  return is_odd(n - 1)
}

fn is_odd(n) {
  if n == 0 { return false }
  return is_even(n - 1)
}

// Hofstadter's Female and Male sequences.
fn female(n) {
  if n == 0 { return 1 }
  return n - male(female(n - 1))
}

fn male(n) {
  if n == 0 { return 0 }
  return n - female(male(n - 1))
}

for n in 0..=12 {
  print(n, is_even(n), is_odd(n))
}
print(is_even(100), is_odd(101), is_even(555), is_odd(556))
for n in 0..=40 {
  print(n, female(n), male(n))
}
'''
    def female(n): return 1 if n == 0 else n - male(female(n - 1))
    def male(n): return 0 if n == 0 else n - female(male(n - 1))

    out = [f'{n} {show(n % 2 == 0)} {show(n % 2 == 1)}' for n in range(13)]
    out.append(' '.join(show(x) for x in (100 % 2 == 0, 101 % 2 == 1, 555 % 2 == 0, 556 % 2 == 1)))
    out += [f'{n} {female(n)} {male(n)}' for n in range(41)]
    return src, lines(out)


def t_param_copy():
    src = '''// A parameter is a variable of the function: assigning to it changes
// nothing in the caller, even when the caller's variable has the same name.
fn bump(n) {
  n += 1
  n = n * 2
  return n
}

fn clobber(n) {
  n = 0
  return n
}

fn relay(n) {
  let z = clobber(n)
  return n * 10 + z
}

fn swap_score(a, b) {
  let t = a
  a = b
  b = t
  return a * 100 + b
}

fn count_down(n) {
  let steps = 0
  while n > 0 {
    n -= 1
    steps += 1
  }
  return steps
}

// Each recursive call has its own n: it is still the same n when the call
// returns.
fn rebuild(n) {
  if n < 10 { return n }
  let head = rebuild(n / 10)
  return head * 10 + n % 10
}

let n = 5
let m = bump(n)
print(n, m)
print(bump(n), bump(bump(n)), n)

let a = 3
let b = 4
print(swap_score(a, b), a, b)
print(swap_score(b, a), a, b)

n = 7
print(relay(n), n)
print(count_down(n), n)
print(count_down(0), count_down(-3))
for i in 1..=3 {
  print(i, bump(i), i)
}
print(rebuild(0), rebuild(7), rebuild(1234567), rebuild(9223372036854775807))
'''
    def bump(n):
        n += 1
        n = n * 2
        return n

    def clobber(n):
        n = 0
        return n

    def relay(n):
        z = clobber(n)
        return n * 10 + z

    def swap_score(a, b):
        a, b = b, a
        return a * 100 + b

    def count_down(n):
        steps = 0
        while n > 0:
            n -= 1
            steps += 1
        return steps

    def rebuild(n):
        if n < 10: return n
        head = rebuild(n // 10)
        return head * 10 + n % 10

    out = []
    n = 5
    m = bump(n)
    out.append(f'{n} {m}')
    out.append(f'{bump(n)} {bump(bump(n))} {n}')
    a, b = 3, 4
    out.append(f'{swap_score(a, b)} {a} {b}')
    out.append(f'{swap_score(b, a)} {a} {b}')
    n = 7
    out.append(f'{relay(n)} {n}')
    out.append(f'{count_down(n)} {n}')
    out.append(f'{count_down(0)} {count_down(-3)}')
    for i in range(1, 4):
        out.append(f'{i} {bump(i)} {i}')
    out.append(f'{rebuild(0)} {rebuild(7)} {rebuild(1234567)} {rebuild(MAX)}')
    return src, lines(out)


def t_hoisting():
    src = '''// Functions are defined before anything runs, so a call can be written
// above the function, and a function can call one written below it.
print(triple(4), add_all(1, 2, 3))
print(from_below(5))

fn from_below(n) {
  return twice(n) + thrice(n)
}

fn twice(n) { return 2 * n }

print(twice(thrice(2)))
let result = triple(triple(2))
print(result)

fn triple(n) { return 3 * n }
fn thrice(n) { return triple(n) }

fn add_all(a, b, c) { return a + b + c }
fn no_params() { return 42 }

print(no_params(), no_params() + 1)
for i in 1..=3 {
  print(twice(i), thrice(i))
}
'''
    triple = lambda n: 3 * n
    twice = lambda n: 2 * n
    thrice = lambda n: triple(n)
    out = [f'{triple(4)} {1 + 2 + 3}', str(twice(5) + thrice(5)), str(twice(thrice(2))),
           str(triple(triple(2))), '42 43']
    out += [f'{twice(i)} {thrice(i)}' for i in range(1, 4)]
    return src, lines(out)


def t_returns():
    src = '''fn nothing() {
}

fn bare() {
  return
}

fn falls_off() {
  let x = 1
  x += 1
}

fn semi(n) {
  if n > 0 { return; }
  return n
}

fn sign(n) {
  if n < 0 {
    return -1
  } else if n > 0 {
    return 1
  }
  return 0
}

// Returns from inside a loop, and from inside two.
fn first_multiple(k, limit) {
  for i in 1..=limit {
    if i % k == 0 { return i }
  }
  return nil
}

fn find_pair(target) {
  for a in 1..=20 {
    for b in a..=20 {
      if a * b == target { return a * 100 + b }
    }
  }
  return -1
}

fn jump_to_multiple(n) {
  while true {
    n += 7
    if n % 5 == 0 { return n }
  }
}

fn is_prime(n) {
  if n < 2 { return false }
  let d = 2
  while d * d <= n {
    if n % d == 0 { return false }
    d += 1
  }
  return true
}

fn count_primes(limit) {
  let count = 0
  for n in 2..=limit {
    if is_prime(n) { count += 1 }
  }
  return count
}

// The value of a call that returned nothing is nil.
fn passes_nil() {
  return nothing()
}

print(nothing(), bare(), falls_off(), passes_nil())
print(nothing() == nil, bare() != nil, falls_off() == bare())
print(semi(1), semi(0), semi(-4))
print(sign(-9), sign(0), sign(12))
print(first_multiple(7, 100), first_multiple(7, 6), first_multiple(1, 5))
print(find_pair(36), find_pair(91), find_pair(97), find_pair(400))
print(jump_to_multiple(1), jump_to_multiple(5), jump_to_multiple(-2))
print(is_prime(1), is_prime(2), is_prime(91), is_prime(97))
print(count_primes(100), count_primes(1000))
nothing()
bare()
print(sign(sign(5) - 3))
'''
    def first_multiple(k, limit):
        for i in range(1, limit + 1):
            if i % k == 0: return i
        return None

    def find_pair(target):
        for a in range(1, 21):
            for b in range(a, 21):
                if a * b == target: return a * 100 + b
        return -1

    def jump(n):
        while True:
            n += 7
            if n % 5 == 0: return n

    def is_prime(n):
        if n < 2: return False
        d = 2
        while d * d <= n:
            if n % d == 0: return False
            d += 1
        return True

    def sign(n): return -1 if n < 0 else 1 if n > 0 else 0

    def semi(n):
        if n > 0: return None
        return n

    def count_primes(limit): return sum(1 for n in range(2, limit + 1) if is_prime(n))

    nothing = bare = falls_off = lambda: None
    out = [' '.join(show(f()) for f in (nothing, bare, falls_off, lambda: nothing())),
           ' '.join(show(x) for x in (nothing() is None, bare() is not None, falls_off() is bare())),
           ' '.join(show(semi(n)) for n in (1, 0, -4)),
           ' '.join(show(sign(n)) for n in (-9, 0, 12)),
           ' '.join(show(first_multiple(*a)) for a in ((7, 100), (7, 6), (1, 5))),
           ' '.join(show(find_pair(t)) for t in (36, 91, 97, 400)),
           ' '.join(show(jump(n)) for n in (1, 5, -2)),
           ' '.join(show(is_prime(n)) for n in (1, 2, 91, 97)),
           f'{count_primes(100)} {count_primes(1000)}',
           show(sign(sign(5) - 3))]
    return src, lines(out)


def t_deep():
    src = '''// 1000 nested calls is the most a program may make: depth(999) is the call
// for 999, 998, ... 0.
fn depth(n) {
  if n == 0 { return 0 }
  return 1 + depth(n - 1)
}

fn ping(n) {
  if n == 0 { return 0 }
  return pong(n - 1) + 1
}

fn pong(n) {
  if n == 0 { return 0 }
  return ping(n - 1) + 1
}

fn sum_to(n) {
  if n == 0 { return 0 }
  return n + sum_to(n - 1)
}

print(depth(999))
print(depth(999), depth(998) + depth(1))
for i in 1..=5 {
  print(i, depth(999) - 999 + i)
}
print(ping(999), pong(999), ping(500) + pong(500))
print(sum_to(999))
print(depth(depth(500)))
print(depth(10 + depth(200)))
'''
    def depth(n): return 0 if n == 0 else 1 + depth(n - 1)
    def sum_to(n): return 0 if n == 0 else n + sum_to(n - 1)
    def ping(n): return 0 if n == 0 else pong(n - 1) + 1
    def pong(n): return 0 if n == 0 else ping(n - 1) + 1

    out = [str(depth(999)), f'{depth(999)} {depth(998) + depth(1)}']
    out += [f'{i} {depth(999) - 999 + i}' for i in range(1, 6)]
    out.append(f'{ping(999)} {pong(999)} {ping(500) + pong(500)}')
    out.append(str(sum_to(999)))
    out.append(str(depth(depth(500))))
    out.append(str(depth(10 + depth(200))))
    return src, lines(out)


# --- Random programs --------------------------------------------------------
#
# Expressions: ('n', k), ('v', name), ('neg', e), (op, l, r) for op in
# + - * / %, ('call', fname, [args]).  Conditions: ('cmp', op, l, r),
# ('and' | 'or', c, c), ('not', c).  Statements: ('let', name, e),
# ('set', name, e), ('if', cond, then, else_or_None), ('for', var, hi,
# body), ('return', e).  Variables are declared only at the top of a
# function body, so scopes never need tracking; loop variables are
# unique and read-only; blocks inside ifs and fors hold only returns,
# assignments and one more if.

CMPS = ['==', '!=', '<', '<=', '>', '>=']


def gen_expr(rng, vars_, fns, d):
    r = rng.random()
    if d <= 0 or r < 0.25:
        if vars_ and rng.random() < 0.65:
            return ('v', rng.choice(vars_))
        return ('n', rng.choice([0, 1, 2, 3, 5, 7, 9, 10, -1, -4, 100]))
    if fns and r < 0.5:
        name, arity = rng.choice(fns)
        return ('call', name, [gen_expr(rng, vars_, fns, d - 1) for _ in range(arity)])
    if r < 0.58:
        return ('neg', gen_expr(rng, vars_, fns, d - 1))
    op = rng.choice(['+', '+', '-', '-', '*', '/', '%'])
    left = gen_expr(rng, vars_, fns, d - 1)
    if op in '/%':
        # A literal divisor, so the program doesn't fault for dividing by zero.
        return (op, left, ('n', rng.choice([1, 2, 3, 4, 7, -2, -5])))
    return (op, left, gen_expr(rng, vars_, fns, d - 1))


def gen_cond(rng, vars_, fns, d):
    r = rng.random()
    if d > 0 and r < 0.2:
        return (rng.choice(['and', 'or']), gen_cond(rng, vars_, fns, d - 1), gen_cond(rng, vars_, fns, d - 1))
    if d > 0 and r < 0.3:
        return ('not', gen_cond(rng, vars_, fns, d - 1))
    return ('cmp', rng.choice(CMPS), gen_expr(rng, vars_, fns, 1), gen_expr(rng, vars_, fns, 1))


def gen_fn(rng, idx, fns):
    name = f'f{idx}'
    params = [f'p{k}' for k in range(rng.choice([0, 1, 1, 2, 2, 3]))]
    vars_ = list(params)
    body = []
    for k in range(rng.choice([0, 1, 2])):
        body.append(('let', f'v{k}', gen_expr(rng, vars_, fns, 3)))
        vars_.append(f'v{k}')
    assignable = list(vars_)
    loops = 0
    for _ in range(rng.choice([1, 2, 3])):
        r = rng.random()
        if r < 0.4:
            then = [('return', gen_expr(rng, vars_, fns, 2))]
            orelse = None
            if assignable and rng.random() < 0.4:
                orelse = [('set', rng.choice(assignable), gen_expr(rng, vars_, fns, 2))]
            body.append(('if', gen_cond(rng, vars_, fns, 1), then, orelse))
        elif r < 0.75 and assignable:
            loops += 1
            var = f'i{loops}'
            inner = vars_ + [var]
            stmts = [('set', rng.choice(assignable), gen_expr(rng, inner, fns, 2))]
            if rng.random() < 0.4:
                stmts.append(('if', gen_cond(rng, inner, fns, 0),
                              [('return', gen_expr(rng, inner, fns, 1))], None))
            body.append(('for', var, rng.choice([0, 1, 3, 6]), stmts))
        elif assignable:
            body.append(('set', rng.choice(assignable), gen_expr(rng, vars_, fns, 3)))
    body.append(('return', gen_expr(rng, vars_, fns, 3)))
    return {'name': name, 'params': params, 'body': body}


class Interp:
    BUDGET = 30000

    def __init__(self, fns):
        self.fns = {f['name']: f for f in fns}
        self.steps = 0

    def tick(self):
        self.steps += 1
        if self.steps > self.BUDGET: raise Stop('too long')

    def expr(self, env, e):
        self.tick()
        k = e[0]
        if k == 'n': return e[1]
        if k == 'v': return env[e[1]]
        if k == 'neg': return checked(-self.expr(env, e[1]))
        if k == 'call':
            args = [self.expr(env, a) for a in e[2]]
            return self.call(e[1], args)
        l = self.expr(env, e[1])
        r = self.expr(env, e[2])
        return apply(k, l, r)

    def cond(self, env, c):
        k = c[0]
        if k == 'cmp':
            l = self.expr(env, c[2])
            r = self.expr(env, c[3])
            return {'==': l == r, '!=': l != r, '<': l < r, '<=': l <= r, '>': l > r, '>=': l >= r}[c[1]]
        if k == 'not': return not self.cond(env, c[1])
        left = self.cond(env, c[1])
        if k == 'and': return self.cond(env, c[2]) if left else False
        return True if left else self.cond(env, c[2])

    def block(self, env, stmts):
        """Runs statements; returns ('ret', value) when a return happened."""
        for s in stmts:
            self.tick()
            k = s[0]
            if k == 'let' or k == 'set':
                env[s[1]] = self.expr(env, s[2])
            elif k == 'return':
                return ('ret', self.expr(env, s[1]))
            elif k == 'if':
                branch = s[2] if self.cond(env, s[1]) else s[3]
                if branch is not None:
                    r = self.block(env, branch)
                    if r: return r
            elif k == 'for':
                for i in range(s[2]):
                    env[s[1]] = i
                    r = self.block(env, s[3])
                    if r: return r
                env.pop(s[1], None)
        return None

    def call(self, name, args):
        f = self.fns[name]
        env = dict(zip(f['params'], args))
        return self.block(env, f['body'])[1]


def etext(e, top=False):
    k = e[0]
    if k == 'n': return lit(e[1])
    if k == 'v': return e[1]
    if k == 'call': return f'{e[1]}({", ".join(etext(a, True) for a in e[2])})'
    if k == 'neg': return '-' + etext(e[1])
    t = f'{etext(e[1])} {k} {etext(e[2])}'
    return t if top else f'({t})'


def ctext(c, top=False):
    k = c[0]
    if k == 'cmp':
        t = f'{etext(c[2])} {c[1]} {etext(c[3])}'
        return t if top else f'({t})'
    if k == 'not': return f'not {ctext(c[1])}'
    t = f'{ctext(c[1])} {k} {ctext(c[2])}'
    return t if top else f'({t})'


def stext(s, ind):
    pad = '  ' * ind
    k = s[0]
    if k == 'let': return [f'{pad}let {s[1]} = {etext(s[2], True)}']
    if k == 'set': return [f'{pad}{s[1]} = {etext(s[2], True)}']
    if k == 'return': return [f'{pad}return {etext(s[1], True)}']
    if k == 'if':
        out = [f'{pad}if {ctext(s[1], True)} {{'] + [l for x in s[2] for l in stext(x, ind + 1)]
        if s[3] is None: return out + [f'{pad}}}']
        return out + [f'{pad}}} else {{'] + [l for x in s[3] for l in stext(x, ind + 1)] + [f'{pad}}}']
    if k == 'for':
        return [f'{pad}for {s[1]} in 0..{s[2]} {{'] + [l for x in s[3] for l in stext(x, ind + 1)] + [f'{pad}}}']


def ftext(f):
    out = [f'fn {f["name"]}({", ".join(f["params"])}) {{']
    for s in f['body']:
        out += stext(s, 1)
    return out + ['}', '']


def t_random(name):
    seed = 0
    while True:
        seed += 1
        rng = random.Random(f'{name}-{seed}')
        fns = []
        sigs = []
        for idx in range(rng.choice([5, 6, 7])):
            f = gen_fn(rng, idx, sigs)
            fns.append(f)
            sigs.append((f['name'], len(f['params'])))
        calls = []
        for _ in range(14):
            fname, arity = rng.choice(sigs)
            calls.append(('call', fname, [('n', rng.choice([-7, -3, -1, 0, 1, 2, 3, 5, 8, 12, 50]))
                                           for _ in range(arity)]))
        for _ in range(4):
            calls.append(gen_expr(rng, [], sigs, 3))
        it = Interp(fns)
        try:
            out = [str(it.expr({}, c)) for c in calls]
        except Stop:
            continue
        # Interesting enough: a spread of values, not all the same.
        if len(set(out)) < 8: continue
        prog = [l for f in fns for l in ftext(f)]
        prog += [f'print({etext(c, True)})' for c in calls]
        return '\n'.join(prog) + '\n', lines(out)


TESTS = {
    'gcd': t_gcd, 'factorial': t_factorial, 'fibonacci': t_fibonacci, 'ackermann': t_ackermann,
    'mutual': t_mutual, 'param-copy': t_param_copy, 'hoisting': t_hoisting,
    'returns': t_returns, 'deep': t_deep,
    'random-a': lambda: t_random('a'), 'random-b': lambda: t_random('b'),
}


def main(argv):
    program = '--program' in argv
    names = [a for a in argv if not a.startswith('--')]
    if len(names) != 1 or names[0] not in TESTS:
        sys.exit('usage: functions.py [--program] ' + '|'.join(TESTS))
    src, expected = TESTS[names[0]]()
    sys.stdout.write(src if program else expected)


main(sys.argv[1:])
