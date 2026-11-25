#!/usr/bin/env python3
"""Step 8's evidence for D75, that the last statement of a block may leave
its semicolon out: every `same` test that has a block, with the semicolon
before each closing brace taken out, given to perl 5.42. perl must compile
it in silence and print what it prints for the test as it stands.

    CURLY_PERL=/opt/perl-5.42/bin/perl python3 docs/briefs/step8-semicolons.py

2026-11-25: 31 tests, 5,505 semicolons taken out, none differs. The files
it writes, build/semi/NNN-name.pl, were then compiled, and each prints
what its test expects. A record, not a test.
"""
import glob, os, re, subprocess

os.makedirs('build/semi', exist_ok=True)
PERL = os.environ['CURLY_PERL']
n = stripped = 0
bad = []
for src in sorted(glob.glob('t/[0-9]*.pl')):
    text = open(src, 'rb').read()
    if re.search(rb'^# kind:', text, re.M):
        continue
    new, k = re.subn(rb';([ \t]*(?:#[^\n]*)?\n?[ \t\n]*)\}', rb'\1}', text)
    if k == 0:
        continue
    n += 1; stripped += k
    path = 'build/semi/' + os.path.basename(src)
    open(path, 'wb').write(new)
    a = subprocess.run([PERL, src], capture_output=True)
    c = subprocess.run([PERL, '-c', path], capture_output=True)
    b = subprocess.run([PERL, path], capture_output=True)
    if a.stdout != b.stdout or b.stderr or b.returncode or c.stderr.decode() != f'{path} syntax OK\n':
        bad.append((src, (c.stderr + b.stderr)[:200]))
print(n, 'same tests with a block;', stripped, 'semicolons before a closing brace taken out;', len(bad), 'differ')
for b in bad: print(b)
