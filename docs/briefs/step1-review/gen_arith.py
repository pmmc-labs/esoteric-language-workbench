"""Random accepted expressions from the grammar, model against perl, line by line."""
import random, sys, os, collections
import model, check
sys.setrecursionlimit(100000)

EDGES = []
for p in (0, 15, 16, 21, 31, 32, 42, 52, 53, 62, 63):
    for d in (-3, -2, -1, 0, 1, 2, 3):
        v = (1 << p) + d
        if 0 <= v <= model.IMAX:
            EDGES.append(v)
EDGES += [3037000499, 3037000500, 2097151, 2097152, 7, 73, 127, 337, 92737, 649657,
          1317624576693539401, 4611686018427387904, 4611686018427387903,
          9223372036854775807, 9223372036854775806, 6074000999, 1000000000000000,
          999999999999999, 9007199254740993, 18014398509481984, 1 << 61, 3, 5, 10]

def lit(rng, profile):
    r = rng.random()
    if r > 0.97: return 0
    if profile == 'small':
        return rng.choice([1, 2, 3, 5, 7, 10, 100, rng.randrange(1, 1000)])
    if profile == 'mid':
        if r < 0.5: return rng.randrange(1, 1 << rng.randrange(1, 33))
        return rng.choice([1, 2, 3, rng.randrange(1, 100)])
    # extreme
    if r < 0.45: return rng.choice(EDGES)
    if r < 0.6: return rng.randrange(1, 1 << rng.randrange(1, 64))
    if r < 0.8: return rng.choice([1, 2, 3])
    return rng.randrange(1, 20)

def primary(rng, d, profile):
    if profile == 'extreme' and rng.random() < 0.06:
        return rng.choice(['( - 9223372036854775807 - 1 )', '( -1 - 9223372036854775807 )',
                           '( -4611686018427387904 * 2 )', '( 2147483648 * -4294967296 )',
                           '( 0 * -1 )', '( - 0 )', '( 4294967296 * 2147483647 + 4294967295 )',
                           '( 7 * 1317624576693539401 )', '( - 9223372036854775807 )'])
    if d <= 0 or rng.random() < 0.45:
        return str(lit(rng, profile))
    return '( ' + expr(rng, d - 1, profile) + ' )'

def unary(rng, d, profile):
    signs = []
    while rng.random() < 0.3 and len(signs) < 4:
        signs.append(rng.choice(['-', '-', '-', '+']))
    return ' '.join(signs + [primary(rng, d, profile)])

def product(rng, d, profile):
    s = unary(rng, d, profile)
    while rng.random() < 0.4:
        s += ' ' + rng.choice(['*', '%', '%']) + ' ' + unary(rng, d, profile)
    return s

def expr(rng, d, profile):
    s = product(rng, d, profile)
    while rng.random() < 0.4:
        s += ' ' + rng.choice(['+', '-']) + ' ' + product(rng, d, profile)
    return s

def statement(rng):
    profile = rng.choice(['small', 'mid', 'extreme', 'extreme'])
    e = expr(rng, rng.randrange(0, 7), profile)
    if e.startswith('('):
        e = rng.choice(['+', '-', '(', '0 + ']) + e
        if e.startswith('(('):
            e = '( ' + e[1:] + ' )'
    return 'say ' + e + ';'

def depth(t):
    return 0 if t[0] == 'int' else 1 + max(depth(x) for x in t[1:])

def ops(t, c):
    if t[0] != 'int':
        c[t[0]] += 1
        for x in t[1:]: ops(x, c)

def one(seed, n_pure, n_mixed):
    rng = random.Random(seed)
    stats = collections.Counter()
    finds = []
    # pure file: only statements the model gives an Int for
    pure, vals = [], []
    opc = collections.Counter()
    while len(pure) < n_pure:
        st = statement(rng)
        src = ('use v5.42;\n' + st + '\n').encode()
        tr = model.parse(src)
        try:
            v = model.ev(tr[0])
        except model.Fault as f:
            stats['gen-fault ' + str(f)] += 1
            continue
        pure.append(st); vals.append(v)
        stats['pure'] += 1
        stats['pure-depth>=4'] += depth(tr[0]) >= 4
        stats['pure-neg'] += v < 0
        stats['pure-big(|v|>=2^53)'] += abs(v) >= 1 << 53
        stats['pure-IMIN'] += v == model.IMIN
        stats['pure-IMAX'] += v == model.IMAX
        stats['pure-zero'] += v == 0
        ops(tr[0], opc)
    for k, v in opc.items(): stats['op ' + k] += v
    src = ('use v5.42;\n' + '\n'.join(pure) + '\n').encode()
    rel = 't/ar_pure_%d.pl' % seed
    f = check.check(src, rel)
    assert f is not None
    if f:
        # find the lines
        rc, out, err = check.perl_run(rel)
        got = out.decode().split('\n')
        for i, v in enumerate(vals):
            if i >= len(got) or got[i] != str(v):
                finds.append(('pure-line', pure[i], str(v), got[i] if i < len(got) else None))
                if len(finds) > 5: break
        finds.append(('pure-file', rel, f))
    # mixed file: everything; perl may die on a model-fault line
    mixed = [statement(rng) for _ in range(n_mixed)]
    src = ('use v5.42;\n' + '\n'.join(mixed) + '\n').encode()
    res = model.results(src)
    rel = 't/ar_mixed_%d.pl' % seed
    todo = list(zip(mixed, res))
    rnd = 0
    while todo:
        rnd += 1
        src = ('use v5.42;\n' + '\n'.join(s for s, _ in todo) + '\n').encode()
        open(os.path.join(check.HERE, rel), 'wb').write(src)
        rc, out, err = check.perl_c(rel)
        if rc != 0 or out != b'' or err != (rel + ' syntax OK\n').encode():
            finds.append(('mixed-rule1', rel, rc, err[:300]))
        rc, out, err = check.perl_run(rel)
        got = out.decode().split('\n')
        assert got[-1] == ''
        got.pop()
        for i, g in enumerate(got):
            s, r = todo[i]
            if isinstance(r, int):
                stats['mixed-int'] += 1
                if g != str(r):
                    finds.append(('mixed-line', s, r, g))
            else:
                stats['mixed-fault-perl-printed'] += 1
                stats['mixed ' + r] += 1
        if rc == 0:
            if len(got) != len(todo):
                finds.append(('mixed-count', rel, len(got), len(todo)))
            if err != b'':
                stats['mixed-file-with-stderr'] += 1
                finds.append(('mixed-stderr-though-exit0', rel, err[:300]))
            break
        k = len(got)
        s, r = todo[k]
        stats['mixed-perl-died'] += 1
        stats['mixed-perl-died: ' + err.decode().split(' at ')[0]] += 1
        if isinstance(r, int):
            finds.append(('mixed-perl-died-on-int', s, r, err[:300]))
        else:
            stats['mixed ' + r] += 1
        todo = todo[k + 1:]
    return stats, finds

if __name__ == '__main__':
    from multiprocessing import Pool
    seeds = range(int(sys.argv[1]), int(sys.argv[2]))
    n_pure, n_mixed = int(sys.argv[3]), int(sys.argv[4])
    tot = collections.Counter(); allf = []
    with Pool(4) as p:
        for st, f in p.starmap(one, [(s, n_pure, n_mixed) for s in seeds]):
            tot.update(st); allf += f
    for k in sorted(tot): print('%-50s %d' % (k, tot[k]))
    print('FINDINGS', len(allf))
    for f in allf[:40]: print(f)
