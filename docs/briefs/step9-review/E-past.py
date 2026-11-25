#!/usr/bin/env python3
"""Review of step 9: does a value that went through an array or a list (an
element, a list, push and pop, shift, a slice, a list assignment, splice, a
foreach, a list repeat, a flattened argument) print anything a directly
assigned one doesn't? perl against perl. Step 8's E-past.py, with new routes.
  CURLY_PERL=... python3 E-past.py"""
import os, subprocess, itertools, tempfile
PERL = os.environ['CURLY_PERL']
VALS = ['10000000000000000', '9007199254740992', '9007199254740993', '9223372036854775807', '9007199254740992.0', '-9007199254740991.0', '9007199254740991.0',
        '1e15', '999999999999999.0', '0.0', '-0.0', '3.0', '"3.0"', '"1e3"', '"007"', '"9007199254740992"', '"9007199254740993"', '"0x10"', '" 12"', '"12 "', '"1_000"', '"-0"', '"-0.0"', '".5"', '"+5"',
        '"abc"', '""', '"0"', '"00"', '"0.0"', '"0E0"', '1 == 1', '1 == 2', '!1', '!0', '0.1 + 0.2', '1e300 * 10', '2 ** 53', '2 ** 62', '2 ** 64', '-17', '17 / 4', '18 / 3', '"18" / "3"', '7 % 3', '"a" x 3', '1.5e9', '4294967296 * 4294967296', '9223372036854775807 + 1', '-9223372036854775807 - 1', '18446744073709551615', '18446744073709551615 + 0', '0 * -1', '-"abc"', '-"-abc"', '"1" . "0"', '1 . 0', '1.0', '"1.0"', '1.10', '"1.10"', '0x10', '1_000']
USES = ['', 'my $t = $x / 3;', 'my $t = $x . "";', 'my $t = $x % 7;', 'my $t = $x == 1;', 'my $t = $x + 0;', 'my $t = length($x);', 'my $t = $x x 1;', 'my $t = $x eq "1";', 'my $t = -$x;']
OPS = ['say $y + 1.0;', 'say $y + 1;', 'say $y * 3.0;', 'say $y - 1;', 'say $y;', 'say $y . "";', 'say -$y;', '$y++; say $y;', '$y--; say $y;', '$y--; say $y - 1;', '$y++; say $y + 1;', 'say $y / 3;', 'say $y % 7;', 'say $y ** 2;', 'say $y x 2;', 'say $y == 1 ? "t" : "f";', 'say $y eq "1" ? "t" : "f";', 'say $y <=> 9007199254740993;', 'say length($y);', 'say !$y;', 'say $y + $y;', 'say $y * $y;', 'say $y cmp "1";', 'say $y . $y;', 'say substr("abcdefgh", $y < 5 ? ($y > -5 ? $y : 0) : 0);', 'say "ab" x ($y < 5 ? $y : 0);', 'say defined($y) ? 1 : 0;', 'say $y ? "T" : "F";', 'say $y + 0.5;', 'say $y + 9007199254740992;', 'say $y - 9007199254740993;', 'say $y * 1;', 'say $y < 9007199254740993 ? 1 : 0;', 'say 0 + $y;', 'say 1.0 * $y;']
def progs(v, use):
    body = lambda intro: 'use v5.42;\nno warnings;\nsub id($p) { return $p }\nsub second($p, $q) { return $q }\n' + intro + '\n' + '\n'.join('{ my $y = $c; %s }' % o for o in OPS) + '\n'
    pre = 'my $x = %s; %s ' % (v, use)
    return {
      'direct':  body(pre + 'my $c = $x;'),
      'element': body(pre + 'my @a; $a[0] = $x; my $c = $a[0];'),
      'literal': body(pre + 'my @a = (1, $x, 2); my $c = $a[1];'),
      'negative': body(pre + 'my @a = (1, $x); my $c = $a[-1];'),
      'push-pop': body(pre + 'my @a; push @a, $x; my $c = pop(@a);'),
      'unshift-shift': body(pre + 'my @a; unshift @a, $x, 1; my $c = shift(@a);'),
      'slice':   body(pre + 'my @a = ($x, 1); my @b = @a[1, 0]; my $c = $b[1];'),
      'lslice':  body(pre + 'my $c = (1, $x, 2)[1];'),
      'listassign': body(pre + 'my ($p, $c) = (1, $x);'),
      'swap':    body(pre + 'my $c = 1; my $o = $x; ($c, $o) = ($o, $c);'),
      'copy':    body(pre + 'my @a = ($x); my @b = @a; my @d = (@b, @b); my $c = $d[1];'),
      'splice':  body(pre + 'my @a = (1, $x, 2); my @b = splice(@a, 1, 1); my $c = $b[0];'),
      'splice-in': body(pre + 'my @a = (1, 2); splice(@a, 1, 0, $x); my $c = $a[1];'),
      'foreach': body(pre + 'my @a = ($x); my $c; for my $e (@a) { $c = $e; }'),
      'foreach-list': body(pre + 'my $c; for my $e (1, $x) { $c = $e; }'),
      'repeat':  body(pre + 'my @a = ($x) x 3; my $c = $a[2];'),
      'flatten': body(pre + 'my @a = (1, $x); my $c = second(@a);'),
      'elem-arg': body(pre + 'my @a = ($x); my $c = id($a[0]);'),
      'past-end': body(pre + 'my @a; $a[3] = $x; my $c = $a[3];'),
      'expr-literal': body('my @a = (%s); my $c = $a[0];' % v) if not use else None,
      'expr-push': body('my @a; push @a, %s; my $c = $a[0];' % v) if not use else None,
      'expr-store': body('my @a; $a[0] = %s; my $c = $a[0];' % v) if not use else None,
      'used-in-element': body('my $x = %s; my @a = ($x); { my $x = $a[0]; %s } my $c = $x;' % (v, use)) if use else None,
      'used-through-foreach': body('my $x0 = %s; my @a = ($x0); for my $x (@a) { %s } my $x = %s; %s my $c = $a[0]; ' % (v, use, v, '')) if False else None,
      'element-used': body('my @a = (%s); { my $t = 0; %s } my $c = $a[0];' % (v, use.replace('$x', '$a[0]'))) if use else None,
    }
def run(text):
    with tempfile.NamedTemporaryFile('w', suffix='.pl', delete=False, dir='.') as f: f.write(text)
    p = subprocess.run([PERL, f.name], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=20)
    os.unlink(f.name)
    return p.stdout + ('EXIT %d %s' % (p.returncode, p.stderr[:80]) if p.returncode else '')
n = 0; diffs = 0
for v in VALS:
    fresh = None
    for use in USES:
        ps = progs(v, use)
        base = run(ps['direct'])
        if not use: fresh = base
        for k, t in ps.items():
            if t is None or k == 'direct': continue
            n += len(OPS)
            # a value used only inside the callee: the caller's variable should be as fresh
            want = fresh if k == 'used-in-element' else base
            got = run(t)
            if got != want:
                w = want.split('\n'); g = got.split('\n')
                for i, o in enumerate(OPS):
                    if i < len(w) and i < len(g) and w[i] != g[i]:
                        diffs += 1
                        print('DIFF v=%s use=%r via=%s op=%r direct=%r array=%r' % (v, use, k, o, w[i], g[i]))
                if len(w) != len(g): print('LEN v=%s use=%r via=%s' % (v, use, k), got[-200:])
print(n, 'comparisons,', diffs, 'differ')
