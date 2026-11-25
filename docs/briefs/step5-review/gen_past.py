#!/usr/bin/env python3
"""gen_past.py SEED COUNT: pasts inside the language. A variable gets a value of
every kind and edge; then read-only statements (on it, or on a copy), then
statements of the new language (++ -- OP=), more reads, and one observation.
Each program is held to the rule against perl: a value's past showing in perl
where the model does not fault is a program that breaks it."""
import random, sys, collections
import model, harness
from model import lit

def L(text): return lit(text)
def S(text, val): return ('lit', text, 's', val)
def b(op, a, c): return ('bin', op, a, c)
def neg(a): return ('neg', a)

INT = ['0', '1', '2', '7', '10', '255', '999999999999999', '1000000000000000', '9007199254740990', '9007199254740991',
       '9007199254740992', '9007199254740993', '9007199254740994', '10000000000000000', '18014398509481984',
       '1152921504606846976', '4611686018427387904', '9223372036854775806', '9223372036854775807', '36028797018963968',
       '9007199254740996', '4503599627370496', '4503599627370497']
NUM = ['0.0', '0.5', '1.5', '3.0', '1e3', '0.1', '999999999999999.0', '1e15', '1000000000000000.5', '9007199254740991.0',
       '9007199254740992.0', '9007199254740994.0', '9007199254740996.0', '1e16', '1e19', '9.2233720368547758e18', '1.8446744073709552e19',
       '1e300', '4503599627370496.5', '0.99999999999999989', '1e-5', '1e21', '123456789012345.67', '2.5', '1e0', '7.0', '100.0',
       '9007199254740990.0', '4503599627370495.5', '2251799813685248.25', '1.7976931348623157e308', '9223372036854774784.0',
       '18014398509481984.0', '18014398509481988.0', '999999999999998.0', '1e14']
STR = ['', '0', '1', '12', '-5', '+5', ' 12', '12 ', '007', '00', '09', '0.0', '0.5', '.5', '5.', '1.5', '3.0', '-3.0', '10.00', '1e3',
       '1E3', '1e0', '0e0', '1.5e3', '1e-2', '1e15', '1e16', '1e300', '999999999999999', '1000000000000000', '9007199254740991',
       '9007199254740992', '9007199254740993', '9223372036854775807', '9223372036854775808', '-9223372036854775808',
       '18446744073709551615', '18446744073709551616', '9007199254740991.0', '9007199254740992.0', '9007199254740993.0',
       '999999999999999.0', '1000000000000000.0', '0.99999999999999995', '1.99999999999999999', '4503599627370496.5', 'abc', 'a', 'Az',
       'zz', 'a9', '12abc', '0x10', '0 but true', 'Inf', 'NaN', '-0', '-0.0', '0.', '1_000', ' ', '0 ', '1 2', '1.0e0',
       '100000000000000000000', '0.1', '3.14', '-', '+', '.', 'e5', '1e', '1e+3', '0e5', '00.5', '0.50', '99', '9', '-1', '-9007199254740992',
       '-9007199254740991', '1e15 ', '9.99e14', '1e2', '2.0', '-2.0', '+3.0', '9007199254740990', '-12', '0012', '1.0', '-1.0', 'z', 'Zz', 'a0',
       '9223372036854775806', '-9223372036854775807', '1.5 ', ' 1.5', '0e0', '.0', '-.5', '1e1', '000', '-0e0', '0.0e0', '1.0e15', '9.007199254740992e15',
       '9007199254740992e0', '12.', '+0', '+', '08', '10', '19', '199', '999', '0.9', '9.9', '-9', '-10']


def inits():
    out = [None]
    out += [L(t) for t in INT] + [neg(L(t)) for t in INT[:19]]
    out.append(b('-', neg(L('9223372036854775807')), L('1')))
    out += [L(t) for t in NUM] + [neg(L(t)) for t in NUM[:22]]
    out += [S('"%s"' % t, t) for t in STR]
    out += [S('"12\\n"', '12\n'), S('"\\n12"', '\n12'), S('"\\t3.0"', '\t3.0')]
    out += [L('true'), L('false'), b('<', L('1'), L('2')), b('>', L('1'), L('2')), ('not', L('1')), ('not', L('0')), L('undef'),
            ('fn1', 'defined', L('undef')), ('fn1', 'length', S('"abc"', 'abc')), ('fn1', 'length', L('undef'))]
    out += [b('/', L('6'), L('2')), b('**', L('2'), L('10')), b('**', L('2'), L('53')), b('**', L('2'), L('0.5')), b('/', L('10'), L('3')),
            b('*', L('1e-200'), neg(L('1e-200'))), b('x', S('"a"', 'a'), L('3')), b('.', S('"1"', '1'), S('"2"', '2')), b('.', L('1'), L('2')),
            b('+', S('"3"', '3'), L('0')), b('+', S('"3.0"', '3.0'), L('0')), b('*', S('"3.0"', '3.0'), L('1')), b('/', L('7'), L('2')),
            b('**', L('2'), L('3')), b('%', L('10'), L('3')), ('fn', 'substr', [S('"12345"', '12345'), L('1'), L('2')]), neg(S('"12"', '12')),
            neg(S('"1.5"', '1.5')), ('fn1', 'chr', L('49')), ('fn1', 'ord', S('"1"', '1')), b('<=>', L('1'), L('2')), b('cmp', S('"a"', 'a'), S('"b"', 'b')),
            b('**', L('10'), L('15')), b('**', L('2'), L('50')), b('/', L('4000000000000000'), L('2')), b('*', L('1e15'), L('1')), b('+', L('1e15'), L('0')),
            b('/', L('18014398509481984'), L('2')), b('*', L('3'), L('0.5')), b('+', L('0.5'), L('0.5')), b('-', L('1e16'), L('1')), b('.', L('1.5'), S('""', '')),
            b('.', L('3'), S('".0"', '.0')), b('x', L('9'), L('15')), b('x', L('9'), L('16')), b('.', L('0'), L('9')), b('-', L('0.5'), L('0.5')),
            b('*', L('9007199254740992'), L('1')), b('+', L('9007199254740991'), L('1')), b('*', L('2.0'), L('4503599627370496')),
            b('**', L('2'), L('62')), b('**', L('2'), L('63')), b('**', L('3'), L('30')), b('*', L('1e10'), L('1e5'))]
    return out


def reads(v):
    z = [b('+', v, L('0')), b('.', v, S('""', '')), b('>', v, L('0.5')), neg(v), b('*', v, L('1.5')), b('%', v, L('7')), ('fn1', 'length', v),
         b('==', v, L('1')), b('eq', v, S('"a"', 'a')), ('not', v), b('x', v, L('1')), ('fn', 'substr', [S('"abc"', 'abc'), v]),
         b('*', v, L('1')), b('-', v, L('0')), b('/', v, L('1')), b('**', v, L('1')), b('<', v, L('1')), b('<=>', v, L('0')), b('lt', v, S('"b"', 'b')),
         ('fn1', 'chr', v), b('x', S('"ab"', 'ab'), v), ('fn', 'index', [S('"abc"', 'abc'), S('"b"', 'b'), v]),
         ('fn', 'substr', [S('"abcdefghij"', 'abcdefghij'), L('0'), v]), ('tern', v, L('1'), L('0')), ('log', '||', v, L('0')), ('log', '//', v, L('0')),
         ('fn1', 'defined', v), ('fn1', 'uc', v), ('fn1', 'ord', v), b('+', v, L('0.5')), b('*', v, L('1.0')), b('+', v, L('9007199254740992')),
         b('.', v, v), b('+', v, v), b('*', v, v), b('==', v, v), b('+', L('0'), v), b('*', L('1.5'), v), b('.', S('""', ''), v), b('%', L('7'), v),
         b('**', L('2'), v), b('/', L('1'), v), b('-', v, L('1')), b('+', v, L('1')), b('cmp', v, v), b('<=>', v, L('9007199254740993')),
         b('==', v, L('9007199254740992.0')), b('-', v, L('0.0')), b('+', v, S('"0"', '0')), b('+', v, S('"0.0"', '0.0')), b('*', v, S('"1.0"', '1.0')),
         b('>=', v, L('1e15')), b('!=', v, L('0')), ('fn1', 'lc', v), b('ne', v, L('0')), b('xor', v, L('1')), b('%', v, L('9007199254740993')),
         b('/', v, L('2')), b('**', v, L('2')), b('**', v, L('0.5')), b('x', v, L('0')), b('x', v, L('2'))]
    return z


def steps(v, r):
    n = v[1]
    one = [('post', '++', n), ('pre', '++', n), ('post', '--', n), ('pre', '--', n)]
    rhs = [L('1'), L('0'), L('1.5'), S('"1"', '1'), S('"1.0"', '1.0'), L('2'), L('0.5'), S('"3.0"', '3.0'), L('7'), L('1.0'), S('""', ''), S('"0"', '0'),
           L('9007199254740992'), L('9007199254740991'), L('1e16'), L('10000000000000000'), v, L('true'), L('false'), neg(L('1')), L('1e15'),
           S('"1e3"', '1e3'), L('3'), L('0.0'), S('"abc"', 'abc'), L('9223372036854775807'), neg(L('0.5'))]
    ops = ['+=', '-=', '*=', '/=', '%=', '**=', '.=', 'x=', '||=', '&&=', '//=']
    c = r.random()
    if c < 0.5: return ('expr', r.choice(one))
    if c < 0.93:
        op = r.choice(ops)
        e = r.choice(rhs)
        if op == 'x=' and r.random() < 0.8: e = r.choice([L('1'), L('2'), L('0'), L('3')])
        if op == '**=' and r.random() < 0.8: e = r.choice([L('1'), L('2'), L('0'), L('0.5')])
        return ('expr', ('asg', op, v, e))
    if c < 0.97: return ('expr', ('asg', '=', v, r.choice([v, b('+', v, L('0')), b('.', v, S('""', '')), neg(v), b('*', v, L('1'))])))
    return ('expr', ('asg', r.choice(['+=', '.=', '-=']), v, r.choice(one)))


def observations(v):
    n = v[1]
    return [
        [('say', v)],
        [('say', b('+', v, L('1')))], [('say', b('*', v, L('3')))], [('say', b('-', v, L('1')))], [('say', b('/', v, L('2')))], [('say', b('%', v, L('5')))],
        [('say', b('.', v, S('"|"', '|')))], [('say', ('fn1', 'length', v))], [('say', ('tern', b('==', v, L('1')), S('"eq"', 'eq'), S('"ne"', 'ne')))],
        [('say', b('+', v, L('0.5')))], [('say', b('*', v, L('1.5')))], [('say', b('+', v, L('9007199254740992')))], [('say', b('-', v, L('9007199254740993')))],
        [('say', neg(v))], [('say', b('x', v, L('2')))], [('say', b('**', v, L('2')))], [('say', b('<=>', v, L('9007199254740993')))],
        [('say', ('tern', v, S('"t"', 't'), S('"f"', 'f')))], [('say', ('tern', ('fn1', 'defined', v), S('"d"', 'd'), S('"u"', 'u')))],
        [('expr', ('post', '++', n)), ('say', v)], [('expr', ('post', '--', n)), ('say', v)], [('expr', ('pre', '++', n)), ('say', b('+', v, L('0')))],
        [('say', ('fn', 'substr', [S('"abcdefghijklmnop"', 'abcdefghijklmnop'), v]))], [('say', ('fn1', 'chr', v))],
        [('say', b('+', b('+', v, L('0')), ('pre', '++', n)))], [('say', b('.', v, ('post', '++', n)))], [('say', b('.', neg(v), ('asg', '+=', v, L('1'))))],
        [('say', ('post', '++', n)), ('say', v)], [('say', ('post', '--', n)), ('say', v)], [('say', ('pre', '++', n))], [('say', ('pre', '--', n))],
        [('say', b('+', v, S('"1.0"', '1.0')))], [('say', b('*', v, L('1.0')))], [('say', b('==', v, L('9007199254740992.0')))], [('say', b('eq', v, L('1')))],
        [('say', b('+', v, L('1e15')))], [('say', b('*', v, v))], [('say', b('+', v, v))], [('say', b('.', v, v))], [('say', b('-', v, L('0.5')))],
        [('say', b('+', v, L('10000000000000000')))], [('say', b('*', v, L('10000000000000000')))], [('say', b('-', L('0'), v))], [('say', b('%', v, L('1000000')))],
        [('expr', ('asg', '+=', v, L('0'))), ('say', v)], [('expr', ('asg', '.=', v, S('""', ''))), ('say', v)], [('expr', ('asg', '*=', v, L('1'))), ('say', v)],
        [('expr', ('asg', '-=', v, L('1'))), ('say', v)], [('expr', ('asg', '+=', v, L('1'))), ('say', v)],
    ]


def program(r, INITS):
    x, u = ('var', 'x'), ('var', 'u')
    prog = [('my', 'x', r.choice(INITS))]
    tn = [0]
    have_u = [False]
    def which():
        return u if have_u[0] and r.random() < 0.6 else x
    def some_reads(k):
        for _ in range(k):
            if not have_u[0] and r.random() < 0.12:
                prog.append(('my', 'u', x)); have_u[0] = True; continue
            tn[0] += 1
            prog.append(('my', 't%d' % tn[0], r.choice(reads(which()))))
    some_reads(r.choice([0, 0, 1, 1, 1, 2, 2, 3]))
    for _ in range(r.choice([1, 1, 1, 2, 2, 3])):
        prog.append(steps(which(), r))
        some_reads(r.choice([0, 0, 0, 1, 1, 2]))
    v = which()
    if r.random() < 0.2:
        # the value an expression of the new language yields, kept in a variable of its own
        n = v[1]
        e = r.choice([('post', '++', n), ('post', '--', n), ('pre', '++', n), ('pre', '--', n), ('asg', '+=', v, L('0')), ('asg', '.=', v, S('""', '')),
                      ('asg', '||=', v, L('5')), ('asg', '=', v, v), ('log', '||', v, L('0')), ('uplus', v), ('tern', L('1'), v, L('0')),
                      ('asg', '-=', v, L('1')), ('asg', '*=', v, L('1')), ('asg', 'x=', v, L('1'))])
        prog.append(('my', 'w', e))
        some_reads(r.choice([0, 0, 1]))
        if r.random() < 0.7: v = ('var', 'w')
        if r.random() < 0.5: prog.append(steps(v, r))
    if r.random() < 0.3: prog.append(('say', ('tern', ('fn1', 'defined', v), S('"d"', 'd'), S('"u"', 'u'))))
    prog += r.choice(observations(v))
    if r.random() < 0.4: prog += r.choice(observations(v))
    return prog


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    if '--break' in sys.argv:
        # the checker must go red: a string's step without the proposal's leading-zero fault
        bytes_isdigit = bytes.isdigit
        real = model.step
        def broken(v, sign):
            if v.tag == model.T_STR and sign == 1:
                b = model.as_bytes(v)
                if len(b) > 1 and b.isdigit() and b[:1] == b'0': return model.N(model.numeric(v)[1] + 1)
            return real(v, sign)
        model.step = broken
    r = random.Random(seed)
    INITS = inits()
    t = harness.Tally('pasts, seed %d' % seed, 'past-%d.log' % seed)
    kinds = collections.Counter(); skipped = 0
    for _ in range(count):
        p = program(r, INITS)
        if model.any_truth_refused(p) or model.any_list_refused(p): skipped += 1; continue
        v = t.check(p)
        if v:
            key = v.split(':')[0]
            for w in ('Lost precision', 'Found =', 'uninitialized', "isn't numeric", 'Non-finite', 'Negative repeat'):
                if w in v: key += ' [' + w + ']'
            kinds[key] += 1
    t.done()
    print(dict(kinds), 'skipped', skipped)


if __name__ == '__main__':
    main()
