#!/usr/bin/env python3
"""probe.py FILE [-d]: cases separated by a line '---'. Each is prefixed 'use v5.42;\n'
(unless it starts with 'RAW\n'), written to t/x.pl, and given to perl -c and perl.
-d adds B::Deparse -p."""
import subprocess, sys, os
import tempfile
PERL = os.environ.get('CURLY_PERL', 'perl')
here = os.path.join(tempfile.gettempdir(), 'curly-step5-review-%d' % os.getuid())
os.makedirs(os.path.join(here, 't'), exist_ok=True)
def run(args, **kw):
    env = dict(os.environ, PERL_HASH_SEED='1')
    return subprocess.run(args, capture_output=True, env=env, stdin=subprocess.DEVNULL, timeout=20, **kw)
def main():
    text = open(sys.argv[1]).read()
    os.chdir(here)
    dep = '-d' in sys.argv[2:]
    for case in text.split('\n---\n'):
        case = case.strip('\n')
        if not case: continue
        if case.startswith('RAW\n'): src = case[4:] + '\n'
        else: src = 'use v5.42;\n' + case + '\n'
        open('t/x.pl', 'w').write(src)
        c = run([PERL, '-c', 't/x.pl'])
        r = run([PERL, 't/x.pl'])
        cerr = c.stderr.decode('utf-8', 'replace')
        ok = (c.returncode == 0 and cerr == 't/x.pl syntax OK\n')
        print('=' * 60)
        print(case)
        print('  -c: exit %d %s' % (c.returncode, 'CLEAN' if ok else repr(cerr)))
        print('  run: exit %d out=%r err=%r' % (r.returncode, r.stdout.decode('utf-8','replace'), r.stderr.decode('utf-8','replace')))
        if dep:
            d = run([PERL, '-MO=Deparse,-p', 't/x.pl'])
            print('  deparse:', ' '.join(d.stdout.decode().split('\n')[4:]) if d.returncode == 0 else d.stderr.decode()[:200])
main()
