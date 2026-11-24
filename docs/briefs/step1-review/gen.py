# Candidate programs with the reviewer's model's verdict on each, as JSON lines.
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.setrecursionlimit(100000)
OUT = os.path.join(HERE, '..', '..', '..', 'build', 'step1-review')
os.makedirs(OUT, exist_ok=True)
import model
def verdict(s):
    try:
        lines, fault = model.run(s.encode())
        return {'s': s, 'ok': True, 'lines': lines, 'fault': fault}
    except model.Refused as r:
        return {'s': s, 'ok': False}
def exhaustive(alpha, n):
    for k in range(1, n + 1):
        for combo in itertools.product(alpha, repeat=k):
            yield 'use v5.42;\nsay' + ''.join(combo) + ';'
sets = {'A': ([' ', '\t', '\n', '(', ')', '+', '-', '*', '%', '1', ';', '#\n', 'say'], 5),
        'B': ([' ', '\n', '(', ')', '+', '-', '%', '1', '0'], 6),
        'C': ([' ', '\n', '(', ')', '-', '1', ';', 'say', '#\n', '--', '**', '2 '], 5)}
with open(os.path.join(OUT, 'cands.jsonl'), 'w') as f:
    n = ok = 0
    for name, (alpha, depth) in sets.items():
        for s in exhaustive(alpha, depth):
            v = verdict(s); n += 1; ok += v['ok']
            f.write(json.dumps(v) + '\n')
    print('candidates', n, 'accepted by the model', ok)
