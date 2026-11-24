#!/usr/bin/env python3
"""Part A: random expressions over the whole grammar, as text, so that the
model's parse (levels 1 to 6) is held against perl's as well as its values.
usage: a4_random.py SEED COUNT [options...]"""
import sys, random
from harness import *
from pools import *
seed, count = int(sys.argv[1]), int(sys.argv[2])
NL = 'nl' in sys.argv
for k in sys.argv[3:]:
    if k != 'nl': model.OPT[k] = True
R = random.Random(seed)
S = numstrings(full=False)
S = [s for s in S if len(s) < 45 and '3037000' not in s]
NICE_S = ['abc', 'Ab', '', ' ', 'a b', 'x', 'hello world', '12', '3', '1.5', '2.0', '1e3', '-4', '0', '007', ' 5 ', '65', '0.5', '10', '-1.0', '+7', 'aXb', '(', ')', '#', "it's", '5e0', '00', '-0', '.5', 'e', '9']
NICE_N = ['0', '1', '2', '3', '5', '10', '65', '100', '0.5', '1.5', '2.0', '1e3', '3.0', '0.1', '7', '255', '2.5', '1e15', '0x10', '0b11', '0o17', '1_000', '.5', '1.0']
N = [n for n in numbers() if '3037000500' not in n]
UN = ['length', 'uc', 'lc', 'ord', 'chr']
def lit():
    r = R.random()
    if r < 0.30: return R.choice(NICE_N)
    if r < 0.60:
        s = R.choice(NICE_S)
        if R.random() < 0.3 and "'" not in s and '\\' not in s: return "'" + s + "'"
        return q(s)
    if r < 0.75: return q(R.choice(S))
    if r < 0.90: return R.choice(N)
    return R.choice(['"\\x{E9}"', '"\\x{100}a"', '"a\\x{10FFFF}"', '"\\xFF"', '"\\0"', '"\\n"', '"A\\tb"', '9007199254740993', '4611686018427387904', '1e16', '"1e15"', '"9007199254740992"', '18014398509481984'])
def ws():
    r = R.random()
    if NL and r < 0.25: return R.choice(['\n', ' \n', '\n ', ' # c\n', '\t', '\n\n', ' # ) x . (\n', '\n# "\n'])
    return ' ' if r < 0.8 else '' if r < 0.95 else '  '
def expr(d):
    if d <= 0 or R.random() < 0.12: return lit()
    r = R.random()
    if r < 0.50:
        op = R.choice(['+', '-', '*', '/', '%', '**', '.', '.', '.', 'x', 'x', '+', '*'])
        return expr(d - 1) + ws() + op + ws() + expr(d - 1)
    if r < 0.60: return '(' + expr(d - 1) + ')'
    if r < 0.67: return R.choice(['-', '-', '+', '- ']) + expr(d - 1)
    if r < 0.77: return R.choice(UN) + R.choice(['', '', ' ']) + '(' + expr(d - 1) + ')'
    if r < 0.89: return R.choice(UN) + (ws() if NL else R.choice([' ', ' ', ''])) + expr(d - 1)
    if r < 0.95:
        a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.6 else [])
        return 'substr' + R.choice(['', '', ' ']) + '(' + ', '.join(a) + ')'
    a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.5 else [])
    return 'index' + R.choice(['', '', ' ']) + '(' + ','.join(a) + ')'
stmts = []
for _ in range(count):
    e = expr(R.choice([1, 2, 2, 3]))
    r = R.random()
    if r < 0.7: stmts.append('say %s;' % e)
    elif r < 0.8: stmts.append('say(%s);' % e)
    elif r < 0.9: stmts.append('print %s;' % e)
    else: stmts.append('print(%s);' % e)
print(len(stmts), 'statements, seed', seed)
st, f = check_statements(HO, stmts)
import pickle
pickle.dump(f, open('out_a4_%d%s.pkl' % (seed, 'nl' if NL else ''), 'wb'))
show(f, 4)
