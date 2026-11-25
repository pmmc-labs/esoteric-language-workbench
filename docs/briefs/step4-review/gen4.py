#!/usr/bin/env python3
"""Part A: random statements over the whole step-4 grammar, as text.
usage: gen4.py SEED COUNT [nl] [tight] [OPT4KEY=VALUE ...]"""
import sys, random, pickle
import model4
from h4 import *
from pools import q

seed, count = int(sys.argv[1]), int(sys.argv[2])
NL = 'nl' in sys.argv
TIGHT = 'tight' in sys.argv
HEAVY = 'heavy' in sys.argv
for k in sys.argv[3:]:
    if '=' in k:
        a, b = k.split('=')
        model4.OPT4[a] = {'True': True, 'False': False}.get(b, b)
R = random.Random(seed)
NUM = ['0', '1', '2', '3', '5', '10', '0.5', '1.5', '2.0', '1e3', '.5', '0x10', '7', '0.0', '1.0', '100', '9007199254740993', '1e16', '4', '-1']
STR = ['a', 'abc', '', '0', '1', '2', '10', '0.0', '00', ' ', 'b', 'A', '1.5', '-1', '3.0', '1e3', 'ab', '0E0', ' 1', '9', '1 ', '-0', 'B', 'aa', '2.50', '0x1']
UN = ['length', 'uc', 'lc', 'ord', 'chr', 'defined', 'defined', 'length']
BIN = (['+', '-', '*', '/', '%', '**', '.', '.', 'x'] +
       ['<', '>', '<=', '>=', 'lt', 'gt', 'le', 'ge'] * 2 +
       ['==', '!=', '<=>', 'eq', 'ne', 'cmp'] * 3 +
       ['&&', '||', '//'] * 5 + ['and', 'or', 'xor'] * 3)


def lit():
    r = R.random()
    if r < 0.30:
        return R.choice(NUM)
    if r < 0.55:
        s = R.choice(STR)
        if R.random() < 0.3:
            return "'" + s + "'"
        return q(s)
    if r < 0.70:
        return 'true'
    if r < 0.85:
        return 'false'
    if r < 0.93:
        return 'undef'
    return '(undef)'


def ws(word=False):
    r = R.random()
    if NL and r < 0.2:
        return R.choice(['\n', ' \n', '\n ', ' # c\n', '\t', '\n\n', ' # ) x . ( ? : //\n', '\n# "\n'])
    if TIGHT:
        return ' ' if r < 0.5 else ''
    if word:
        return ' ' if r < 0.93 else '' if r < 0.97 else '  '
    return ' ' if r < 0.75 else '' if r < 0.95 else '  '


def count_expr(d):
    r = R.random()
    if r < 0.5:
        return R.choice(['0', '1', '2', '3', 'true', 'false', '"2"', '2.5', '(1+1)', '!0', '!1'])
    if r < 0.7:
        return '(' + expr(0) + ')'
    return R.choice(['not ', '!', 'length ', 'defined ', 'length(', 'defined(']) .rstrip('(') + '(' + expr(d - 1) + ')'


def heavy(d):
    r = R.random()
    if r < 0.30:
        op = R.choice(['&&', '||', '//', 'and', 'or', 'xor', '==', '<', 'lt', 'eq', '<=>', 'cmp', '.', 'x', '+', '**', '!=', 'ne', '>=', '-', '*'])
        if op == 'x':
            return expr(d - 1) + ws(True) + 'x' + ws(True) + count_expr(d)
        return expr(d - 1) + ws(op.isalpha()) + op + ws(op.isalpha()) + expr(d - 1)
    if r < 0.45:
        return R.choice(['not ', 'not ', 'not(', 'not (', 'not\n', 'not', 'not  (', 'not#\n(', 'not !', 'not -', 'not +(', '! not ', '- not ', 'not not ']) + expr(d - 1)
    if r < 0.52:
        return R.choice(['not(', 'not (', '!(', '-(', '+(', '(']) + expr(d - 1) + ')'
    if r < 0.70:
        return expr(d - 1) + ws() + '?' + ws() + expr(d - 1) + ws() + ':' + ws() + expr(d - 1)
    if r < 0.82:
        return R.choice(['defined', 'defined', 'length', 'ord', 'chr', 'uc', 'lc']) + R.choice([' ', ' ', '', '(', ' (', '\n', ' !', ' -', ' +', ' not ', ' - ', '  -', '\t-', ' !!']) + expr(d - 1)
    if r < 0.90:
        return R.choice(['!', '-', '+', '! ', '- ', '!!', '-!', '!-', '+!', '!+', '- -', '! !']) + expr(d - 1)
    a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.6 else [])
    return R.choice(['substr', 'index']) + R.choice(['', '', ' ']) + '(' + ', '.join(a) + ')'


def expr(d):
    if d <= 0 or R.random() < 0.12:
        return lit()
    if HEAVY:
        return heavy(d)
    r = R.random()
    if r < 0.52:
        op = R.choice(BIN)
        w = op.isalpha()
        if op == 'x':
            return expr(d - 1) + ws(True) + 'x' + ws(True) + count_expr(d)
        return expr(d - 1) + ws(w) + op + ws(w) + expr(d - 1)
    if r < 0.60:
        return '(' + ws() + expr(d - 1) + ws() + ')'
    if r < 0.70:
        return R.choice(['-', '!', '!', '!', '+', '- ', '! ', '!!']) + expr(d - 1)
    if r < 0.78:
        return R.choice(['not ', 'not ', 'not(', 'not (', 'not\n', 'not']) + expr(d - 1) + ('' if R.random() < 0.5 else '') 
    if r < 0.80:
        return R.choice(['not(', 'not (']) + expr(d - 1) + ')'
    if r < 0.88:
        return expr(d - 1) + ws() + '?' + ws() + expr(d - 1) + ws() + ':' + ws() + expr(d - 1)
    if r < 0.92:
        return R.choice(UN) + R.choice(['', '', ' ']) + '(' + expr(d - 1) + ')'
    if r < 0.97:
        return R.choice(UN) + (ws(True) if NL else R.choice([' ', ' ', ''])) + expr(d - 1)
    if r < 0.99:
        a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.6 else [])
        return 'substr' + R.choice(['', '', ' ']) + '(' + ', '.join(a) + ')'
    a = [expr(d - 1), expr(d - 1)] + ([expr(d - 1)] if R.random() < 0.5 else [])
    return 'index' + R.choice(['', '', ' ']) + '(' + ','.join(a) + ')'


def gen(count):
    stmts = []
    for _ in range(count):
        e = expr(R.choice([1, 2, 2, 3, 3, 4]))
        r = R.random()
        if r < 0.35:
            stmts.append('say %s;' % e)
        elif r < 0.85:
            stmts.append('say(%s);' % e)
        elif r < 0.9:
            stmts.append('print %s;' % e)
        elif r < 0.95:
            stmts.append('print(%s);' % e)
        else:
            stmts.append('say (%s);' % e)
    return stmts


if __name__ == '__main__':
    stmts = gen(count)
    print(len(stmts), 'statements, seed', seed)
    st, f = check_statements(HO, stmts)
    pickle.dump(f, open('out_gen4_%d%s%s%s.pkl' % (seed, 'nl' if NL else '', 't' if TIGHT else '', 'h' if HEAVY else ''), 'wb'))
    show(f, 6)
