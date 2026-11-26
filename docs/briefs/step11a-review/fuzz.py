#!/usr/bin/env python3
"""Holds model.py to perl 5.42: for every string the model ACCEPTS and gives a
value for, perl must print that value, exit 0, and say nothing on stderr.

    python3 fuzz.py exhaustive [--zero]     every shape, every suffix of 0 to 2
                                            printable characters, and every
                                            one-character prefix
    python3 fuzz.py random N SEED [--zero]  N random strings over a nasty alphabet
    python3 fuzz.py index [--zero]          every index and slice body of up
                                            to 4 tokens

--zero makes the model refuse a leading zero in an index (finding W1), so
that the rest can be seen.  CURLY_PERL names perl (default
/opt/perl-5.42/bin/perl).  Work files go to $REVIEW_TMP (default: a
directory under the scratchpad given in FINDINGS.md, or ./tmp).
Differences are printed, and written to fuzz-<mode>.diff beside this file.
"""

import itertools
import os
import random
import subprocess
import sys
from multiprocessing import Pool

import model

PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
TMP = os.environ.get('REVIEW_TMP', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp'))

# What the program declares.  $x and @x both, $i and @i both, @a with no $a
# (the language has no `my $a`), $y with no @y, @z with no $z.
ENV = {
    '$x': 'X', '$y': 'Y', '$i': 1, '$j': 2, '$x_': 'U', '$xx': 'W', '$x1': 'V',
    '@x': ['k', 'l', 'm'], '@a': ['p', 'q', 'r', 's'], '@i': ['e', 'f'], '@z': ['g'],
}
SCALARS = [k[1:] for k in ENV if k[0] == '$']
ARRAYS = [k[1:] for k in ENV if k[0] == '@']

HEADER = 'use v5.42;\n' + ''.join(
    ('my %s = %s;\n' % (k, repr(v) if isinstance(v, int) else '"%s"' % v)) if k[0] == '$'
    else 'my %s = (%s);\n' % (k, ', '.join('"%s"' % e for e in v))
    for k, v in ENV.items())


def run_one(args):
    n, body = args
    path = os.path.join(TMP, 'f%d-%d.pl' % (os.getpid(), n))
    with open(path, 'w') as f:
        f.write(HEADER + 'print "' + body + '";\n')
    try:
        r = subprocess.run([PERL, path], capture_output=True, timeout=10)
        res = (r.returncode, r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace'))
    except subprocess.TimeoutExpired:
        res = (-1, '', 'TIMEOUT')
    os.unlink(path)
    return body, res


def check(bodies, tag, opts):
    os.makedirs(TMP, exist_ok=True)
    accepted = []
    refused = faults = 0
    for b in bodies:
        kind, got = model.lex(b, SCALARS, ARRAYS, opts)
        if kind == 'refused':
            refused += 1
            continue
        v = model.value(got, ENV)
        if isinstance(v, tuple):
            faults += 1
            continue
        accepted.append((b, v))
    want = dict(accepted)
    diffs = []
    with Pool(4) as pool:
        for body, (code, out, err) in pool.imap_unordered(run_one, list(enumerate(want)), chunksize=64):
            if code != 0 or err != '' or out != want[body]:
                diffs.append((body, want[body], code, out, err.strip().split('\n')[0]))
    diffs.sort()
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'fuzz-%s.diff' % tag), 'w') as f:
        for d in diffs:
            f.write('string %r\n  model %r\n  perl  exit %d, %r\n  err   %s\n' % d)
    print('%s: %d strings, %d refused by the model, %d faults by the model, '
          '%d accepted and run under perl, %d differ' %
          (tag, len(bodies), refused, faults, len(want), len(diffs)))
    for d in diffs[:60]:
        print('  %r: model %r, perl exit %d %r %s' % d)
    return diffs


SHAPES = ['$x', '${x}', '$y', '@a', '@{a}', '@x', '$a[0]', '$a[-1]', '$a[$i]', '$x[1]',
          '@a[0,1]', '@a[0 .. 1]', '@a[$i, 2]', '$#a', '$#{a}', '$#x']
PRINT = [chr(c) for c in range(32, 127) if chr(c) != '"']


def exhaustive():
    out = []
    for s in SHAPES:
        out.append(s)
        for a in PRINT:
            out.append(s + a)
            out.append(a + s)
            for b in PRINT:
                out.append(s + a + b)
                out.append(a + s + b)
        for t in ['->[0]', '->{a}', '->@*', '->$*', '->$#*', '->@[0]', '->%*', '->&*', '->**', '->(1)',
                  '::y', ':::', ':y', "'y", '-->', '->-', '\\->[0]', '-\\>[0]', '\\::', '\\[0]', '\\{a}',
                  ' [0]', ' {a}', '\n[0]', '\t[0]', '.[0]', '}[0]', ']{a}']:
            out.append(s + t)
    return out


ALPHA = list('$@#{}[]():-><\'\\.,_ax01 ^*&%!~+=;?/|`i') + ['->', '::', '..', '$#', '${', '@{', '$x', '@a',
        '$a[', '@a[', '$i', '$x[', '@x[', '${x}', '@{a}', '$#a', '$#{a}', ']', '}', '0', '1', ', ', ' .. ',
        '-1', '\\', '\n', '\t', '$y', '@z', '$xx', '$x1', '$x_', '_', '$j', '@i']


def rand(n, seed):
    r = random.Random(seed)
    out = set()
    while len(out) < n:
        k = r.randint(1, 9)
        s = ''.join(r.choice(ALPHA) for _ in range(k))
        if s.endswith('\\') and not s.endswith('\\\\'):
            s += r.choice('[{:-$@ ')
        out.add(s)
    return sorted(out)


ITOK = ['0', '1', '2', '-1', '-', '00', '01', '010', '3', '9', '$i', '$j', '$x', '$y', ' ', '  ', '\t', ',', '..',
        '...', '.', '$', '_', '1_0', '+', '$#a', '$i[0]', '@x', '1.0', '1e0', '0x1', '$ i', '${i}', '-0', '--1']


def index():
    out = []
    for k in range(0, 5):
        for toks in itertools.product(ITOK, repeat=k):
            if k == 4 and not ({',', '..'} & set(toks)):
                continue
            b = ''.join(toks)
            out.append('<$a[' + b + ']>')
            out.append('<@a[' + b + ']>')
    return sorted(set(out))


def main():
    args = [a for a in sys.argv[1:] if a != '--zero']
    opts = model.Opts
    if '--zero' in sys.argv:
        opts.refuse_leading_zero = True
    mode = args[0]
    if mode == 'exhaustive':
        check(exhaustive(), 'exhaustive', opts)
    elif mode == 'random':
        check(rand(int(args[1]), int(args[2])), 'random-%s' % args[2], opts)
    elif mode == 'index':
        check(index(), 'index', opts)


if __name__ == '__main__':
    main()
