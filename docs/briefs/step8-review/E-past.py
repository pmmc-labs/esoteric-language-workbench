#!/usr/bin/env python3
"""Review of step 8: does a value that went through a sub (argument, return,
last statement) print anything a directly assigned one doesn't? perl against perl.
  CURLY_PERL=... python3 past.py"""
import os, subprocess, itertools, tempfile
PERL = os.environ['CURLY_PERL']
VALS = ['10000000000000000', '9007199254740992', '9007199254740993', '9223372036854775807', '9007199254740992.0', '-9007199254740991.0', '9007199254740991.0',
        '1e15', '999999999999999.0', '0.0', '-0.0', '3.0', '"3.0"', '"1e3"', '"007"', '"9007199254740992"', '"9007199254740993"', '"0x10"', '" 12"', '"12 "', '"1_000"', '"-0"', '"-0.0"', '".5"', '"+5"',
        '"abc"', '""', '"0"', '"00"', '"0.0"', '"0E0"', '1 == 1', '1 == 2', '!1', '!0', '0.1 + 0.2', '1e300 * 10', '2 ** 53', '2 ** 62', '2 ** 64', '-17', '17 / 4', '18 / 3', '"18" / "3"', '7 % 3', '"a" x 3', '1.5e9', '4294967296 * 4294967296', '9223372036854775807 + 1', '-9223372036854775807 - 1', '18446744073709551615', '18446744073709551615 + 0', '0 * -1', '-"abc"', '-"-abc"', '"1" . "0"', '1 . 0', '1.0', '"1.0"', '1.10', '"1.10"', '0x10', '1_000']
USES = ['', 'my $t = $x / 3;', 'my $t = $x . "";', 'my $t = $x % 7;', 'my $t = $x == 1;', 'my $t = $x + 0;', 'my $t = length($x);', 'my $t = $x x 1;', 'my $t = $x eq "1";', 'my $t = -$x;']
OPS = ['say $y + 1.0;', 'say $y + 1;', 'say $y * 3.0;', 'say $y - 1;', 'say $y;', 'say $y . "";', 'say -$y;', '$y++; say $y;', '$y--; say $y;', '$y--; say $y - 1;', '$y++; say $y + 1;', 'say $y / 3;', 'say $y % 7;', 'say $y ** 2;', 'say $y x 2;', 'say $y == 1 ? "t" : "f";', 'say $y eq "1" ? "t" : "f";', 'say $y <=> 9007199254740993;', 'say length($y);', 'say !$y;', 'say $y + $y;', 'say $y * $y;', 'say $y cmp "1";', 'say $y . $y;', 'say substr("abcdefgh", $y < 5 ? ($y > -5 ? $y : 0) : 0);', 'say "ab" x ($y < 5 ? $y : 0);', 'say defined($y) ? 1 : 0;', 'say $y ? "T" : "F";', 'say $y + 0.5;', 'say $y + 9007199254740992;', 'say $y - 9007199254740993;', 'say $y * 1;', 'say $y < 9007199254740993 ? 1 : 0;', 'say 0 + $y;', 'say 1.0 * $y;']
def progs(v, use):
    body = lambda intro: 'use v5.42;\nno warnings;\nsub id($p) { return $p }\nsub idl($p) { $p }\nsub id2($p) { return id($p) }\n' + intro + '\n' + '\n'.join('{ my $y = $c; %s }' % o for o in OPS) + '\n'
    return {
      'direct':  body('my $x = %s; %s my $c = $x;' % (v, use)),
      'arg-ret': body('my $x = %s; %s my $c = id($x);' % (v, use)),
      'last':    body('my $x = %s; %s my $c = idl($x);' % (v, use)),
      'two':     body('my $x = %s; %s my $c = id2($x);' % (v, use)),
      'made-in': body('sub mk() { my $x = %s; %s return $x } my $c = mk();' % (v, use)),
      'made-last': body('sub mk() { my $x = %s; %s $x } my $c = mk();' % (v, use)),
      'expr-arg': body('my $c = id(%s);' % v) if not use else None,
      'expr-ret': body('sub mk() { return %s } my $c = mk();' % v) if not use else None,
      'expr-last': body('sub mk() { %s } my $c = mk();' % v) if not use else None,
      'used-in-callee': body('sub us($x) { %s return 1 } my $x = %s; my $k = us($x); my $c = $x;' % (use, v)) if use else None,
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
            want = fresh if k == 'used-in-callee' else base
            got = run(t)
            if got != want:
                w = want.split('\n'); g = got.split('\n')
                for i, o in enumerate(OPS):
                    if i < len(w) and i < len(g) and w[i] != g[i]:
                        diffs += 1
                        print('DIFF v=%s use=%r via=%s op=%r direct=%r sub=%r' % (v, use, k, o, w[i], g[i]))
                if len(w) != len(g): print('LEN v=%s use=%r via=%s' % (v, use, k), got[-200:])
print(n, 'comparisons,', diffs, 'differ')
