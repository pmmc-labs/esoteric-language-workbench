#!/usr/bin/env python3
"""A string of many pieces: perl's one operation for a string takes at most
64 operands (PERL_MULTICONCAT_MAXARG).  Is a longer string still a value made
where it stands?  2 to 200 pieces of six kinds, in eight statements each.

    python3 long-strings.py       prints "N programs, M differ"
"""
import os, subprocess
PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
TMP = os.environ.get('REVIEW_TMP', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp'))
os.makedirs(TMP, exist_ok=True)
n_prog = bad = 0
for n in (2, 63, 64, 65, 66, 100, 129, 200):
    for piece in ('$x', '$x-', '${x}', '$a[0]', '@a', '$x@a'):
        s = piece * n
        prog = f'''use v5.42;
my $x = 3; my @a = (3); my $y; my $t = "t"; my $u = "u";
say "{s}" . ($x = 5); $x = 3;
say "{s}", ($x = 5); $x = 3;
$y = "{s}" . ($x = 5); say $y; $x = 3;
say "a" . "{s}" . ($x = 5); $x = 3;
$x = "{s}"; say $x; $x = 3;
$x .= "{s}"; say $x; $x = 3;
$y = "{s}" . ($a[0] = 5); say $y; $a[0] = 3;
$t = "{s}" . ($t = "5"); say $t;
'''
        path = os.path.join(TMP, 'long.pl')
        open(path, 'w').write(prog)
        r = subprocess.run([PERL, path], capture_output=True, text=True, timeout=10)
        v = piece.replace('${x}', '3').replace('$x', '3').replace('$a[0]', '3').replace('@a', '3') * n
        want = '\n'.join([v + '5', v + '5', v + '5', 'a' + v + '5', v, '3' + v, v + '5', v + '5']) + '\n'
        n_prog += 1
        if r.stdout != want or r.stderr:
            bad += 1
            print('DIFFER', n, piece, r.stderr[:100])
print('%d programs, %d differ' % (n_prog, bad))
