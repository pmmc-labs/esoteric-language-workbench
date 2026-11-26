#!/usr/bin/env python3
"""Which of today's refusals stand on a string being a plain one?

Every `refused` golden test that has a double-quoted string, and that perl
itself warns of or does not run, is rewritten with
"${Zq}TEXT" for "TEXT" (reparse.py's first form).  If perl 5.42 still does not
take the rewritten program in silence, the refusal has to hold for an
interpolated string too; the list is what a build of 11a must not lose.
Printed: the test, what the compiler says today (its .expected), and what
perl says of the rewritten program.

    python3 refusals.py
"""
import glob, os, re, subprocess
import reparse
T = reparse.T
os.makedirs(reparse.TMP, exist_ok=True)
n = quiet = 0
for path in sorted(glob.glob(os.path.join(T, '[0-9]*.pl'))):
    try:
        src = open(path, encoding='utf-8').read()
    except UnicodeDecodeError:
        continue
    if not re.search(r'^# kind: refused', src, re.M):
        continue
    try:
        new, k = reparse.rewrite(src, reparse.FORMS[0])
    except IndexError:
        continue                 # a string that does not end: the refusal under test
    if k == 0:
        continue
    code0, out0, err0 = reparse.perl(path)
    if code0 == 0 and not err0:
        continue                 # perl takes the original in silence: the refusal is the language's own
    n += 1
    p = os.path.join(reparse.TMP, 'q-' + os.path.basename(path))
    open(p, 'w', encoding='utf-8').write(new)
    code, out, err = reparse.perl(p)
    os.unlink(p)
    if code == 0 and not err:
        quiet += 1
        tag = 'QUIET'
    else:
        tag = 'still '
    exp = open(path[:-3] + '.expected', encoding='utf-8').read().strip().split('\n')[0]
    exp = re.sub(r'^\S+?:(\d+:\d+:)', r'\1', exp)
    print('%s %s\n    curlyc: %s\n    perl:   %s' % (tag, os.path.basename(path), exp[:150],
          err.decode('utf-8', 'replace').strip().split('\n')[0][:150] if err else '(nothing; exit %d)' % code))
print('%d refused tests with a string that perl itself warns of or refuses; perl takes %d of them in silence once the string interpolates' % (n, quiet))
