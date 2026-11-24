#!/usr/bin/env python3
"""What perl 5.42 does with two numbers and an operator, as a model, held
to perl. Step 2's proposal (docs/PLAN.md) stands on this: it says which
results are integers and which are floats, operator by operator, and the
proposal's own rule is this one with perl's unsigned integers taken out.

It is a model of perl, not of the language, written from perl's source
(pp_add, pp_subtract, pp_multiply, pp_divide, pp_modulo, pp_pow and
pp_negate in pp.c and pp_hot.c; S_sv_2iuv_common in sv.c) and then run
against perl itself, which is the only reason to believe it:

    python3 docs/briefs/step2-perl-numbers.py          # every pair of the edges, every operator
    python3 docs/briefs/step2-perl-numbers.py --rule   # and how the proposed rule sorts them

It holds two things to perl: a model of perl's own rules (`model`), and
the rule the proposal gives the language (`language`), which is written
from the proposal's words. Where the language's rule gives a value, perl
must give that value; where it faults, perl may do anything.

A number here is an IV or UV, written ('i', n) with n from -2^63 to
2^64 - 1, or an NV, ('n', x). perl treats an NV as an integer when it is
whole and no larger than 2^53 - 1 in magnitude ("pleasable" below, after
perl's SvIV_please), and that test is the heart of every rule.

Not part of make test. t/models/num.py, written when step 2 is built,
is the model of the language; this is the evidence for its proposal.
"""

import ctypes
import math
import os
import struct
import subprocess
import sys
import tempfile

IV_MIN, IV_MAX, UV_MAX = -(2**63), 2**63 - 1, 2**64 - 1
PRESERVED = 2**53 - 1                 # sv.c: MAX_IV_PRESERVED_IN_NV
libm = ctypes.CDLL('libm.so.6' if sys.platform.startswith('linux') else 'libm.dylib')
libm.pow.restype = ctypes.c_double
libm.pow.argtypes = [ctypes.c_double, ctypes.c_double]
libm.fmod.restype = ctypes.c_double
libm.fmod.argtypes = [ctypes.c_double, ctypes.c_double]

class Dies(Exception):
    pass

def I(n):
    assert IV_MIN <= n <= UV_MAX, n
    return ('i', n)

def N(x):
    return ('n', float(x))

def nv(v):
    """SvNV: the number as a double."""
    return float(v[1])

def pleased(v):
    """The integer perl uses for this operand, or None when it uses the
    double. An IV or UV is itself; an NV counts when it is whole and at
    most 2^53 - 1 in magnitude."""
    kind, x = v
    if kind == 'i':
        return x
    if math.isfinite(x) and x == math.trunc(x) and abs(x) <= PRESERVED:
        return int(x)
    return None

def add(a, b, sign=1):
    x, y = pleased(a), pleased(b)
    if x is not None and y is not None:
        r = x + sign * y
        if IV_MIN <= r <= UV_MAX:
            return I(r)
        if r < 0 and -r <= UV_MAX:
            return N(-float(-r))        # "result valid, but out of range for IV": -(NV)result
    return N(nv(a) + sign * nv(b))

def sub(a, b):
    return add(a, b, -1)

def mul(a, b):
    x, y = pleased(a), pleased(b)
    if x is not None and y is not None:
        p = x * y
        if 0 <= p <= UV_MAX or IV_MIN <= p < 0:
            return I(p)
    return N(nv(a) * nv(b))

def div(a, b):
    x, y = pleased(a), pleased(b)
    if x is not None and y is not None:
        if y == 0:
            raise Dies('Illegal division by zero')
        # Only when the left operand is too big for a double to hold, and
        # the division is exact.
        if abs(x) >= abs(y) and abs(x) > 2**53 and abs(x) % abs(y) == 0:
            q = abs(x) // abs(y)
            if (x < 0) == (y < 0):
                return I(q)
            return I(-q) if q <= 2**63 else N(-float(q))
    if nv(b) == 0.0:
        raise Dies('Illegal division by zero')
    return N(nv(a) / nv(b))

def mod(a, b):
    use_double = dright_valid = False
    left = right = 0
    dleft = dright = 0.0
    y = pleased(b)
    if y is not None:
        right_neg, right = y < 0, abs(y)
    else:
        dright = nv(b)
        right_neg = dright < 0
        if right_neg:                   # not abs(): a negative zero stays one
            dright = -dright
        if dright < 2.0**64:
            right, dright_valid = int(dright), True
        else:
            use_double = True
    x = pleased(a)
    if not use_double and x is not None:
        left_neg, left = x < 0, abs(x)
    else:
        dleft = nv(a)
        left_neg = dleft < 0
        if left_neg:
            dleft = -dleft
        if not use_double:
            if dleft < 2.0**64:
                left = int(dleft)
            else:
                dleft = math.floor(dleft + 0.5) if math.isfinite(dleft) else dleft
                use_double = True
                dright = math.floor(dright + 0.5) if dright_valid else float(right)
    if use_double:
        if dright == 0.0:
            raise Dies('Illegal modulus zero')
        dans = libm.fmod(dleft, dright)
        if left_neg != right_neg and dans:
            dans = dright - dans
        return N(-dans if right_neg else dans)
    if right == 0:
        raise Dies('Illegal modulus zero')
    ans = left % right
    if left_neg != right_neg and ans:
        ans = right - ans
    if right_neg:
        return I(-ans) if ans <= 2**63 else N(-float(ans))
    return I(ans)

def power(a, b):
    x, y = pleased(a), pleased(b)
    if x is not None and y is not None and y >= 0:
        base, positive = abs(x), x >= 0
        if base & (base - 1) == 0:
            # A power of two (or 0, or 1) to a whole power: by squaring, in
            # doubles, which is exact until it overflows.
            result, b2, p = 1.0, float(base) if positive else -float(base), y
            if p & 1:
                result *= b2
            p >>= 1
            while p:
                b2 *= b2
                if p & 1:
                    result *= b2
                p >>= 1
            return N(result)
        # "result will definitely fit in UV": the bits of the base times
        # the power, in a UV, which wraps (so a vast power gets in too).
        if (y * base.bit_length()) % 2**64 <= 64:
            result = pow(base, y, 2**64)
            if positive or y % 2 == 0:
                return I(result)
            return I(-result) if result <= 2**63 else N(-float(result))
    return N(libm.pow(nv(a), nv(b)))

def neg(a):
    kind, x = a
    if kind == 'n':
        return N(-x)
    if x > IV_MAX:                      # a UV
        return I(-x) if x <= 2**63 else N(-float(x))
    return I(-x)

OPS = {'+': add, '-': sub, '*': mul, '/': div, '%': mod, '**': power}

def model(op, a, b=None):
    try:
        return neg(a) if op == 'neg' else OPS[op](a, b)
    except Dies as d:
        return ('dies', str(d))

# ---- the values

def ints():
    out = {0, 1, 2, 3, 7, 10, 15, 16, 20, 32, 33, 40, 63, 64}
    for p in (31, 32, 52, 53, 62):
        out |= {2**p - 1, 2**p, 2**p + 1}
    out |= {3037000499, 3037000500, 10**15, 10**15 + 1, 10**16, 10**18, IV_MAX - 1, IV_MAX, IV_MAX // 3}
    out |= {-v for v in out}
    out |= {IV_MIN, IV_MIN + 1}
    return [I(v) for v in sorted(out)]

def nums():
    out = [0.0, -0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.7, 10.0, 16.0, 0.1, 1e-5, 1e3, 4294967295.0, 4294967296.0,
           999999999999999.0, 1e15, 2e15, 2.0**52, 2.0**53 - 1, 2.0**53, 2.0**53 + 2, 1e16, 2.0**62, 2.0**63 - 1024,
           2.0**63, 2.0**63 + 2048, 1e19, 1.8e19, 2.0**64, 1e20, 1e300, 5e-324, 1.7976931348623157e308]
    out += [-v for v in out if v != 0.0]
    out += [math.inf, -math.inf, math.nan]
    return [N(v) for v in out]

def perl_source(v):
    """The value as Perl that makes exactly it: an integer literal, or a
    double from its eight bytes (a new one each time, so that no value
    carries a past)."""
    kind, x = v
    if kind == 'i':
        return f'(-{-x})' if x < 0 else str(x)
    return f'n("{struct.pack(">d", x).hex()}")'

def shown(r):
    """A result as perl and the model both write it down."""
    kind, x = r
    if kind == 'dies':
        return f'dies {x}'
    if kind == 'i':
        return f'{"U" if x > IV_MAX else "I"} {x}'
    return f'N {struct.pack(">d", x).hex() if not math.isnan(x) else "nan"}'

PRELUDE = r'''use v5.42;
no warnings;
use B ();
sub n($hex) { return unpack "d>", pack "H16", $hex }
sub show($r) {
    my $f = B::svref_2object(\$r)->FLAGS;
    return "N " . ($r != $r ? "nan" : unpack "H16", pack "d>", $r) if !($f & B::SVf_IOK);
    return (($f & B::SVf_IVisUV) && $r > 9223372036854775807 ? "U " : "I ") . $r;
}
sub attempt($code) { my $r = eval { $code->() }; return defined $r ? show($r) : "dies " . ($@ =~ s/ at .*//sr); }
'''

def cases():
    vals = ints() + nums()
    out = [('neg', a, None) for a in vals]
    for op in OPS:
        for a in vals:
            for b in vals:
                out.append((op, a, b))
    return out

def ask_perl(cs):
    perl = os.environ.get('CURLY_PERL', 'perl')
    lines = [PRELUDE]
    for op, a, b in cs:
        expr = f'-{perl_source(a)}' if op == 'neg' else f'{perl_source(a)} {op} {perl_source(b)}'
        lines.append(f'say attempt(sub {{ {expr} }});')
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, 'numbers.pl')
        open(path, 'w').write('\n'.join(lines) + '\n')
        r = subprocess.run([perl, path], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    return r.stdout.split('\n')[:-1]

# ---- the language's rule, as the proposal has it

# Written from the proposal's words and not from perl's code: Python's
# integers and floats, and one question, `integral`. Where it gives a
# value, perl must give the same value of the same kind; where it faults,
# perl may do as it likes (D12). main() checks exactly that.

INT_MIN, INT_MAX = IV_MIN, IV_MAX

class Fault(Exception):
    pass

def window(x):
    """A whole float perl prints one way before it has been used as an
    integer and another way after: 1e15 to 2^53 - 1 in magnitude."""
    return x == math.trunc(x) and 10**15 <= abs(x) <= PRESERVED

def integral(v):
    """The whole number an operand stands for, or None: an Int, or a Num
    that is whole and below 2^53 in magnitude."""
    kind, x = v
    if kind == 'i':
        return x
    return int(x) if x == math.trunc(x) and abs(x) < 2**53 else None

def Int(n):
    if not INT_MIN <= n <= INT_MAX:
        raise Fault('integer overflow')
    return ('i', n)

def Num(x):
    if math.isinf(x):
        raise Fault('float overflow')
    if math.isnan(x):
        raise Fault('not a number')
    return ('n', x)

def language(op, a, b=None):
    """The proposed rule. Operands are Ints and finite Nums."""
    if op == 'neg':
        return Int(-a[1]) if a[0] == 'i' else Num(-a[1])
    x, y = integral(a), integral(b)
    fa, fb = float(a[1]), float(b[1])
    both_ints = a[0] == 'i' and b[0] == 'i'
    if op in ('+', '-', '*') and x is not None and y is not None:
        # The amendment step 3 proposes (PLAN.md, Q7; T92): an Int of 2^53
        # or more that a double holds exactly has two answers with a whole
        # Num, by whether the Int has been used as a float. Only a past
        # shows it, so step3-strings-as-numbers.py is where it is checked.
        for whole, other in ((a, b), (b, a)):
            if whole[0] == 'i' and abs(whole[1]) >= 2**53 and float(whole[1]) == whole[1] and other[0] == 'n':
                raise Fault('a whole number this large with a float has two answers in perl')
    if op in ('+', '-'):
        if x is not None and y is not None:
            return Int(x + y if op == '+' else x - y)       # exact, or a fault
        return Num(fa + fb if op == '+' else fa - fb)
    if op == '*':
        if x is not None and y is not None:
            p = x * y
            if INT_MIN <= p <= INT_MAX:
                return ('i', p)
            # Two Ints overflow (D23). So does anything perl would hold as
            # an unsigned integer, 2^63 to 2^64 - 1. Past that, with a Num
            # in it, the product is a Num.
            if both_ints or 2**63 <= p <= UV_MAX:
                raise Fault('integer overflow')
        return Num(fa * fb)
    if op == '/':
        if fb == 0.0:
            raise Fault('division by zero')
        # Exact, when the left operand is an Int too large for a Num to
        # hold and the right divides it.
        if a[0] == 'i' and abs(a[1]) > 2**53 and y is not None and a[1] % y == 0:
            return Int(a[1] // y)
        return Num(fa / fb)
    if op == '%':
        # Each operand cut down to its whole part, which must be an Int.
        cut = []
        for kind, v in (a, b):
            t = v if kind == 'i' else math.trunc(v)
            if not INT_MIN <= t <= INT_MAX:
                raise Fault('modulus of a number outside the integers')
            cut.append(t)
        if cut[1] == 0:
            raise Fault('modulus by zero')
        return ('i', cut[0] % cut[1])
    if op == '**':
        if x is not None and y is not None and y >= 0:
            if abs(x) & (abs(x) - 1) == 0:
                # 0, 1 and the powers of two: always a Num, and exact.
                try:
                    return Num(float(x) ** y if y < 2000 else (0.0 if x == 0 else float(x) ** (y % 2) if abs(x) == 1 else math.inf))
                except OverflowError:
                    raise Fault('float overflow')
            if y * abs(x).bit_length() <= 64:
                return Int(x ** y)                           # exact, or a fault
        return Num(libm.pow(fa, fb))
    raise AssertionError(op)

def finite(v):
    return v[0] == 'i' and v[1] <= IV_MAX or v[0] == 'n' and math.isfinite(v[1])

def main(argv):
    cs = cases()
    got = ask_perl(cs)
    assert len(got) == len(cs), (len(got), len(cs))
    wrong = disagree = 0
    sorts = {}
    for (op, a, b), g in zip(cs, got):
        m = model(op, a, b)
        if shown(m) != g:
            wrong += 1
            if wrong <= 20:
                print(f'DIFFERS {op} {a} {b}: the model of perl {shown(m)}, perl {g}')
        # The language has no unsigned integers, infinities or NaNs, so
        # the rule is only asked about operands it could be given.
        if not finite(a) or b is not None and not finite(b):
            continue
        try:
            r = language(op, a, b)
            what = 'an Int' if r[0] == 'i' else 'a Num, whole and 1e15 to 2^53: faults when printed' if window(r[1]) else 'a Num'
            if shown(r) != g:
                disagree += 1
                if disagree <= 20:
                    print(f'WRONG {op} {a} {b}: the rule {shown(r)}, perl {g}')
        except Fault as f:
            what = f'fault: {f}'
        sorts.setdefault(op, {}).setdefault(what, []).append(g)
    print(f'{len(cs)} operations over {len(ints())} integers and {len(nums())} floats: the model of perl differs from perl on {wrong}')
    print(f'the proposed rule gives a value perl does not on {disagree}')
    if '--rule' in argv:
        for op in sorts:
            print(f'{op}:')
            for what, gs in sorted(sorts[op].items()):
                print(f'    {len(gs):6}  {what}')
    return 1 if wrong or disagree else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
