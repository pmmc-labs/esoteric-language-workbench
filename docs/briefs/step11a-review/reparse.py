#!/usr/bin/env python3
"""Does an interpolated string where a plain one stood change how perl reads
the statement round it?

Every golden test of kind `same` (t/NNN-*.pl with no `# kind:` line) is
rewritten three ways: each double-quoted string "TEXT" becomes "${Zq}TEXT",
"TEXT${Zq}" or "@{Zq}TEXT$Zq[0]", with `my $Zq = ""; my @Zq = ("");` after
the pragmas.  perl
5.42 must print for each what it prints for the original, and say nothing new
on stderr.  Strings on `use` and `no` lines are left alone.

    python3 reparse.py         prints "N tests, S strings, M differ"
"""
import glob, os, re, subprocess, sys
from multiprocessing import Pool
PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ.get('REVIEW_TMP', os.path.join(HERE, 'tmp'))
T = os.path.join(HERE, '..', '..', '..', 't')

FORMS = [lambda t: '${Zq}' + t, lambda t: t + '${Zq}', lambda t: '@{Zq}' + t + '$Zq[0]']


def rewrite(src, form):
    """The source with each double-quoted string given a variable; and how many."""
    out = []
    n = 0
    lines = src.split('\n')
    decl = False
    for line in lines:
        s = line.lstrip()
        if not decl and not (s.startswith('#') or s.startswith('use ') or s.startswith('no ') or s == ''):
            out.append('my $Zq = ""; my @Zq = ("");')
            decl = True
        out.append(line)
    src = '\n'.join(out)
    res = []
    i = 0
    line_start = 0
    while i < len(src):
        c = src[i]
        if c == '\n':
            line_start = i + 1
        if c == '#' and (i == 0 or src[i - 1] != '$'):
            j = src.find('\n', i)
            j = len(src) if j < 0 else j
            res.append(src[i:j]); i = j
            continue
        if c == "'":
            j = i + 1
            while src[j] != "'":
                j += 2 if src[j] == '\\' else 1
            res.append(src[i:j + 1]); i = j + 1
            continue
        if c == '"':
            j = i + 1
            while src[j] != '"':
                j += 2 if src[j] == '\\' else 1
            body = src[i + 1:j]
            head = src[line_start:i].lstrip()
            if head.startswith('use ') or head.startswith('no ') or 'Zq' in src[line_start:i]:
                res.append(src[i:j + 1])
            else:
                res.append('"' + form(body) + '"'); n += 1
            line_start = src.rfind('\n', 0, j + 1) + 1 if '\n' in body else line_start
            i = j + 1
            continue
        res.append(c); i += 1
    return ''.join(res), n


def perl(path):
    try:
        r = subprocess.run([PERL, path], capture_output=True, timeout=60,
                           env={'PATH': os.environ.get('PATH', ''), 'PERL_HASH_SEED': '1'})
        return r.returncode, r.stdout, re.sub(rb' at \S+ line \d+\.?', b'', r.stderr)
    except subprocess.TimeoutExpired:
        return -1, b'', b'TIMEOUT'


def one(path):
    try:
        src = open(path, encoding='utf-8').read()
    except UnicodeDecodeError:
        return None          # a refusal test: a file that is not UTF-8
    if re.search(r'^# kind:', src, re.M):
        return None
    base = perl(path)
    bad = []
    count = 0
    for k, form in enumerate(FORMS):
        new, n = rewrite(src, form)
        count = n
        if n == 0:
            continue
        p = os.path.join(TMP, 'r%d-%s' % (k, os.path.basename(path)))
        open(p, 'w', encoding='utf-8').write(new)
        got = perl(p)
        if got != base:
            bad.append((k, got[0], got[2][:300].decode('utf-8', 'replace'), got[1] == base[1]))
        else:
            os.unlink(p)
    return os.path.basename(path), count, bad


def main():
    os.makedirs(TMP, exist_ok=True)
    files = sorted(glob.glob(os.path.join(T, '[0-9]*.pl')))
    with Pool(4) as pool:
        res = [r for r in pool.map(one, files) if r]
    strings = sum(r[1] for r in res)
    bad = [r for r in res if r[2]]
    print('%d tests of kind same, %d strings in them, each rewritten %d ways; %d tests differ'
          % (len(res), strings, len(FORMS), len(bad)))
    for name, _, b in bad:
        for k, code, err, same_out in b:
            print('  %s form %d: exit %d, stdout %s, stderr %r' % (name, k, code, 'same' if same_out else 'DIFFERS', err[:200]))


if __name__ == '__main__':
    main()
