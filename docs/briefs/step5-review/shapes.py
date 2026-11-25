#!/usr/bin/env python3
"""shapes.py FILE...: programs written by hand, one to a paragraph ('---' between
them, 'use v5.42;' put first), each given to the compiler and, if it is
accepted, to perl. Prints the ones that are WRONG: accepted, run without a
fault, and not what perl prints or something perl complains of; or faulted
after printing what perl doesn't begin with. -v prints every verdict."""
import os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
PERL = os.environ.get('CURLY_PERL', 'perl')
ENV = dict(os.environ, PERL_HASH_SEED='1')
work = tempfile.mkdtemp(prefix='step5-shapes-')


def run(args, **kw):
    return subprocess.run(args, capture_output=True, stdin=subprocess.DEVNULL, timeout=60, **kw)


def verdict(src):
    path = os.path.join(work, 'x.pl')
    open(path, 'w').write(src)
    c = run(['node', os.path.join(ROOT, 'bin', 'curlyc.ts'), '-o', os.path.join(work, 'x'), path])
    if c.returncode == 1: return 'refused', c.stderr.decode().strip().split(': ', 1)[-1][:110]
    if c.returncode != 0: return 'WRONG', 'the compiler breaks: ' + c.stderr.decode()[:300]
    b = run([os.path.join(work, 'x')])
    k = run([PERL, '-c', 'x.pl'], cwd=work, env=ENV)
    if k.returncode != 0 or k.stderr != b'x.pl syntax OK\n': return 'WRONG', 'accepted; perl -c says %r' % k.stderr
    p = run([PERL, 'x.pl'], cwd=work, env=ENV)
    if b.returncode == 0:
        if p.stdout == b.stdout and not p.stderr and p.returncode == 0: return 'same', repr(b.stdout)
        return 'WRONG', 'prints %r; perl prints %r, says %r, exit %d' % (b.stdout, p.stdout, p.stderr, p.returncode)
    if not p.stdout.startswith(b.stdout): return 'WRONG', 'faults after %r; perl prints %r' % (b.stdout, p.stdout)
    return 'faults', b.stderr.decode().strip()[:110]


def main():
    loud = '-v' in sys.argv
    tally = {}
    for name in [a for a in sys.argv[1:] if a != '-v']:
        for case in open(name).read().split('\n---\n'):
            case = case.strip('\n')
            if not case: continue
            src = case[4:] + '\n' if case.startswith('RAW\n') else 'use v5.42;\n' + case + '\n'
            what, detail = verdict(src)
            tally[what] = tally.get(what, 0) + 1
            if loud or what == 'WRONG': print('%s\n  %s: %s' % (case, what, detail))
    print(tally)


main()
