"""A model of the definition under review: accept/refuse, and what an accepted program prints."""
import re

IMAX = 9223372036854775807
IMIN = -9223372036854775808

class Refused(Exception):
    pass

class Fault(Exception):
    pass

def lex(src: bytes):
    """Returns tokens: (kind, text, offset). kinds: word int ver punct"""
    for b in src:
        if not (b == 9 or b == 10 or 0x20 <= b <= 0x7E):
            raise Refused('byte %#x' % b)
    s = src.decode('ascii')
    for line in s.split('\n'):
        if line.lstrip(' \t').startswith('#!'):
            raise Refused('#! line')
    toks = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c in ' \t\n':
            i += 1
            continue
        if c == '#':
            j = s.find('\n', i)
            i = n if j < 0 else j
            continue
        if s.startswith('v5.42', i):
            j = i + 5
            if j < n and s[j] in ' \t\n;':
                toks.append(('ver', 'v5.42', i))
                i = j
                continue
            raise Refused('v5.42 not followed by blank or ;')
        if c.isalpha() or c == '_':
            m = re.compile(r'[A-Za-z_][A-Za-z0-9_]*').match(s, i)
            toks.append(('word', m.group(), i))
            i = m.end()
            continue
        if c.isdigit():
            m = re.compile(r'[0-9]+').match(s, i)
            j = m.end()
            if j < n and (s[j].isalpha() or s[j] == '_'):
                raise Refused('letter after digits')
            t = m.group()
            if len(t) > 1 and t[0] == '0':
                raise Refused('leading zero')
            if int(t) > IMAX:
                raise Refused('integer too large')
            toks.append(('int', t, i))
            i = j
            continue
        if s.startswith('++', i) or s.startswith('--', i) or s.startswith('**', i):
            raise Refused('token ' + s[i:i+2])
        if c in ';()+-*%':
            toks.append(('punct', c, i))
            i += 1
            continue
        raise Refused('character ' + repr(c))
    for k, t, o in toks:
        if k == 'word' and t not in ('use', 'say'):
            raise Refused('word ' + t)
    return s, toks

def parse(src: bytes):
    """Returns the list of expression trees, one per say. Raises Refused."""
    s, toks = lex(src)
    pos = 0
    def peek():
        return toks[pos] if pos < len(toks) else ('eof', '', len(s))
    def take(kind, text=None):
        nonlocal pos
        k, t, o = peek()
        if k != kind or (text is not None and t != text):
            raise Refused('expected %s %s, found %s %r' % (kind, text, k, t))
        pos += 1
        return (k, t, o)
    def expr():
        nonlocal pos
        l = product()
        while peek()[0] == 'punct' and peek()[1] in '+-':
            op = peek()[1]; pos += 1
            r = product()
            l = (op, l, r)
        return l
    def product():
        nonlocal pos
        l = unary()
        while peek()[0] == 'punct' and peek()[1] in '*%':
            op = peek()[1]; pos += 1
            r = unary()
            l = (op, l, r)
        return l
    def unary():
        nonlocal pos
        # iterative so that long chains of signs don't recurse
        signs = []
        while peek()[0] == 'punct' and peek()[1] in '+-':
            signs.append(peek()[1]); pos += 1
        v = primary()
        for sg in reversed(signs):
            v = ('u' + sg, v)
        return v
    def primary():
        nonlocal pos
        k, t, o = peek()
        if k == 'int':
            pos += 1
            return ('int', int(t))
        if k == 'punct' and t == '(':
            pos += 1
            e = expr()
            take('punct', ')')
            return e
        raise Refused('expected a primary, found %s %r' % (k, t))
    take('word', 'use'); take('ver'); take('punct', ';')
    out = []
    while pos < len(toks):
        sayk = take('word', 'say')
        k, t, o = peek()
        if k == 'punct' and t == '(':
            pos += 1
            e = expr()
            close = take('punct', ')')
            semi = take('punct', ';')
            after = sayk[2] + 3
            if after + 1 < len(s) and s[after] in ' \t' and s[after + 1] == '(':
                assert after + 1 == o
                if '\n' in s[o:semi[2]]:
                    raise Refused('one-blank rule')
        else:
            e = expr()
            take('punct', ';')
        out.append(e)
    return out

def ev(e):
    # iterative-safe enough: uses recursion, callers raise the limit
    k = e[0]
    if k == 'int':
        return e[1]
    if k == 'u+':
        return ev(e[1])
    if k == 'u-':
        a = ev(e[1])
        if a == IMIN:
            raise Fault('integer overflow')
        return -a
    a = ev(e[1])
    b = ev(e[2])
    if k == '+': r = a + b
    elif k == '-': r = a - b
    elif k == '*': r = a * b
    elif k == '%':
        if b == 0:
            raise Fault('modulus by zero')
        r = a % b
    if r < IMIN or r > IMAX:
        raise Fault('integer overflow')
    return r

def run(src: bytes):
    """Returns (lines, fault) for an accepted program; raises Refused."""
    trees = parse(src)
    lines = []
    for t in trees:
        try:
            lines.append(str(ev(t)))
        except Fault as f:
            return lines, str(f)
    return lines, None

def results(src: bytes):
    """Per-statement results, ignoring that a fault stops the program: int or Fault message."""
    trees = parse(src)
    out = []
    for t in trees:
        try:
            out.append(ev(t))
        except Fault as f:
            out.append(str(f))
    return out

if __name__ == '__main__':
    import sys
    sys.setrecursionlimit(1000000)
    for f in sys.argv[1:]:
        try:
            print(f, run(open(f, 'rb').read()))
        except Refused as r:
            print(f, 'REFUSED', r)
