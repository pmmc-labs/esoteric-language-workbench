# The compiler's output against the reviewer's model: batches of programs
# that don't fault, and faulting ones one at a time.
import sys, json, random, subprocess, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.setrecursionlimit(100000)
import model, gen_arith
ROOT = os.path.join(HERE, '..', '..', '..')
os.chdir(os.path.join(ROOT, 'build', 'step1-review'))
def compiled(src, name):
    open(f'{name}.pl', 'w').write(src)
    c = subprocess.run(['node', f'{ROOT}/bin/curlyc.ts', '-o', name, f'{name}.pl'], capture_output=True, text=True)
    if c.returncode != 0:
        return None, c.stderr, None
    r = subprocess.run([f'./{name}'], capture_output=True, text=True)
    return r.stdout, r.stderr, r.returncode
bad = 0
def batch(stmts_and_lines, label):
    global bad
    n = 0
    for k in range(0, len(stmts_and_lines), 1500):
        part = stmts_and_lines[k:k + 1500]
        src = 'use v5.42;\n' + '\n'.join(s for s, _ in part) + '\n'
        want = ''.join(l + '\n' for _, ls in part for l in ls)
        out, err, status = compiled(src, 'b')
        n += len(part)
        if out != want or status != 0:
            bad += 1
            print('DIFFERS', label, k, (err or '')[:200])
            got = (out or '').split('\n'); w = want.split('\n')
            for i, (a, b) in enumerate(zip(got, w)):
                if a != b: print('  first difference at line', i, repr(a), repr(b)); break
    print(label, n, 'programs in batches')
def singly(progs, label):
    global bad
    for s, lines, fault in progs:
        out, err, status = compiled(s, 'f')
        want = ''.join(l + '\n' for l in lines)
        if out != want or status != 1 or not err.startswith(f'fault: {fault} at f.pl line '):
            bad += 1; print('DIFFERS', label, repr(s), repr(out), repr(err), status, 'want', repr(want), fault)
    print(label, len(progs), 'faulting programs, one at a time')
rng = random.Random(1)
ok, faulting = [], []
for line in open('cands.jsonl'):
    v = json.loads(line)
    if not v['ok']: continue
    if v['fault'] is None: ok.append((v['s'][len('use v5.42;\n'):], v['lines']))
    else: faulting.append((v['s'], v['lines'], v['fault']))
batch(ok, 'exhaustive')
singly(rng.sample(faulting, min(120, len(faulting))), 'exhaustive')
# random arithmetic, the reviewer's generator
good, faults = [], []
for profile in ('small', 'mid', 'extreme', 'extreme', 'extreme'):
    for _ in range(6000):
        e = gen_arith.expr(rng, rng.randrange(0, 7), profile)
        s = f'say({e});'
        r = model.results(('use v5.42;\n' + s).encode())[0]
        if isinstance(r, int): good.append((s, [str(r)]))
        else: faults.append(('use v5.42;\nsay(1);\n' + s + '\nsay(2);\n', ['1'], r))
batch(good, 'random arithmetic')
singly(rng.sample(faults, 120), 'random arithmetic')
print('faulting kinds:', {k: sum(1 for f in faults if f[2] == k) for k in set(f[2] for f in faults)})
print('differences:', bad)
sys.exit(1 if bad else 0)
