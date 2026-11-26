#!/usr/bin/env python3
"""Every word perl 5.42 gives a meaning to (compiler/src/names.ts: PERL_KEYWORDS
and PERL_OTHER, 299 words), as the name of a scalar and of an array, written
into a string in every shape the proposal has: is it only a name there?

    python3 words.py        prints "N words, M differ" and each difference
"""
import os, re, subprocess, sys
from multiprocessing import Pool
PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ.get('REVIEW_TMP', os.path.join(HERE, 'tmp'))
src = open(os.path.join(HERE, '..', '..', '..', 'compiler', 'src', 'names.ts')).read()
def words(name):
    body = src[src.index('export const %s' % name):]
    body = body[body.index('= [') + 3:body.index('];')]
    return re.findall(r"'([^']+)'", body)
WORDS = words('PERL_KEYWORDS') + words('PERL_OTHER')

def run(w):
    prog = ('use v5.42;\nmy $%s = "S"; my @%s = ("p", "q", "r"); my $i = 1;\n'
            'say "$%s|${%s}|@%s|@{%s}|$%s[0]|$%s[-1]|$%s[$i]|@%s[0, 1]|@%s[$i .. 2]|$#%s|$#{%s}|$%s-|$%s $%s:|${%s}x|@{%s}x|$#{%s}x|$%s->|@%s.";\n'
            'my @k = (0, 2); my $%s_ = 2; my @z = (7, 8, 9);\n'
            'say "$z[$%s_]|@z[$%s_, 0]";\n') % ((w,) * 24)
    path = os.path.join(TMP, 'w-%s.pl' % w)
    open(path, 'w').write(prog)
    r = subprocess.run([PERL, path], capture_output=True, timeout=10)
    os.unlink(path)
    want = 'S|S|p q r|p q r|p|r|q|p q|q r|2|2|S-|S S:|Sx|p q rx|2x|S->|p q r.\n9|9 7\n'
    out = r.stdout.decode()
    if out != want or r.stderr or r.returncode:
        return w, out, r.stderr.decode().strip().split('\n')[0]

os.makedirs(TMP, exist_ok=True)
with Pool(4) as p:
    bad = [b for b in p.map(run, WORDS) if b]
print('%d words, %d differ' % (len(WORDS), len(bad)))
for b in bad:
    print('  %s: %r %s' % b)
