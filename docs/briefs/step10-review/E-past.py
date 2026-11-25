#!/usr/bin/env python3
"""Step 10 review: does a value that a binder has *used* (sorted numerically or by
string, grepped, joined, mapped, reversed, walked by for) then print anything a
fresh one doesn't, in a place where today's compiler does not fault on the fresh one?
perl against perl, then curlyc on the fresh program for every difference."""
import os, subprocess, tempfile, sys
PERL = os.environ['CURLY_PERL']
CURLYC = '/workspace/esoteric-language-workbench/bin/curlyc.ts'
VALS = ['10000000000000000', '9007199254740992', '9007199254740993', '9223372036854775807', '9007199254740992.0', '-9007199254740991.0', '9007199254740991.0',
        '1e15', '999999999999999.0', '0.0', '-0.0', '3.0', '"3.0"', '"1e3"', '"007"', '"9007199254740992"', '"9007199254740993"', '"9223372036854775807"', '"9223372036854775808"', '"18446744073709551615"', '"18446744073709551616"', '"99999999999999999999999"', '"1e15"', '"1e16"', '"1e20"', '"1.5e3"', '"0x10"', '" 12"', '"12 "', '"1_000"', '"-0"', '"-0.0"', '".5"', '"+5"', '"5."', '"10"', '"9"', '"-3"', '"3.7"', '"0 but true"',
        '"abc"', '""', '"0"', '"00"', '"0.0"', '"0E0"', '1 == 1', '1 == 2', '!1', '!0', '0.1 + 0.2', '2 ** 53', '2 ** 62', '-17', '17 / 4', '18 / 3', '"18" / "3"', '7 % 3', '1.5e9', '9223372036854775807 + 1', '0 * -1', '"1" . "0"', '1 . 0', '1.0', '"1.0"', '1.10', '"1.10"', '"1e0"', '"100000000000000000000"', '"9007199254740994"', '"9007199254740993.0"','"4611686018427387904"', '4611686018427387904.0', '1e19', '"1e19"', '"-9223372036854775808"', '"-9223372036854775809"']
USES = {
 'num1': 'my @s = sort { $a <=> $b } @a;',
 'numd1': 'my @s = sort { $b <=> $a } @a;',
 'str1': 'my @s = sort @a;',
 'cmp1': 'my @s = sort { $a cmp $b } @a;',
 'cmpd1': 'my @s = sort { $b cmp $a } @a;',
 'num2': 'push @a, 1; my @s = sort { $a <=> $b } @a;',
 'num2f': 'push @a, 1.5; my @s = sort { $a <=> $b } @a;',
 'num2s': 'push @a, "2"; my @s = sort { $a <=> $b } @a;',
 'num2big': 'push @a, 9007199254740993; my @s = sort { $a <=> $b } @a;',
 'numd2': 'push @a, 1; my @s = sort { $b <=> $a } @a;',
 'str2': 'push @a, 1; my @s = sort @a;',
 'cmp2': 'push @a, "x"; my @s = sort { $a cmp $b } @a;',
 'inplace': 'push @a, 1; @a = sort { $a <=> $b } @a; @a = grep { !($_ eq "1" && length($_) == 1) } @a; push @a, 1 if !@a;',
 'revsort': 'push @a, 1; my @s = reverse sort { $a <=> $b } @a;',
 'gen2': 'push @a, 1; my @s = sort { my $r = $a <=> $b; $r } @a;',
 'grepnum': 'my @s = grep { $_ > 1 } @a;',
 'grepeq': 'my @s = grep { $_ eq "1" } @a;',
 'greptrue': 'my @s = grep { $_ } @a;',
 'join': 'my $j = join(",", @a);',
 'join2': 'my $j = join(",", @a, 1);',
 'mapnum': 'my @s = map { $_ + 0 } @a;',
 'mapstr': 'my @s = map { $_ . "" } @a;',
 'mapneg': 'my @s = map { -$_ } @a;',
 'reverse': 'my @s = reverse @a;',
 'for': 'for (@a) { my $t = $_ * 2; }',
 'formod': 'my $t = 0; $t += $_ for @a;',
}
# routes that take the checked value from the result rather than the original
RES = {
 'res-num2': 'push @a, 1; my @s = sort { $a <=> $b } @a; @a = grep { !($_ eq "1" && length($_) == 1) } @s; push @a, 1 if !@a;',
 'res-str2': 'push @a, "zzz"; my @s = sort @a; @a = ($s[0]);',
 'res-grep': 'my @s = grep { $_ > 1 || 1 } @a; @a = @s;',
 'res-map': 'my @s = map { $_ } @a; @a = @s;',
 'res-rev': 'my @s = reverse @a; @a = @s;',
 'res-sortdirect': 'my @s = sort { $a <=> $b } @a; @a = @s;',
}
USES.update(RES)
OPS = ['say $y + 1.0;', 'say $y + 1;', 'say $y * 3.0;', 'say $y - 1;', 'say $y;', 'say $y . "";', 'say -$y;', '$y++; say $y;', '$y--; say $y;', '$y--; say $y - 1;', '$y++; say $y + 1;', 'say $y / 3;', 'say $y % 7;', 'say $y ** 2;', 'say $y x 2;', 'say $y == 1 ? "t" : "f";', 'say $y eq "1" ? "t" : "f";', 'say $y <=> 9007199254740993;', 'say length($y);', 'say !$y;', 'say $y + $y;', 'say $y * $y;', 'say $y cmp "1";', 'say $y . $y;', 'say defined($y) ? 1 : 0;', 'say $y ? "T" : "F";', 'say $y + 0.5;', 'say $y + 9007199254740992;', 'say $y - 9007199254740993;', 'say $y * 1;', 'say $y < 9007199254740993 ? 1 : 0;', 'say 0 + $y;', 'say 1.0 * $y;', 'say $y <=> 9007199254740992.0;', 'say $y == 9007199254740993 ? "t" : "f";', 'say $y <=> "9007199254740993";', 'say $y - 1.0;', 'say $y % 2;', 'say $y >= 9223372036854775807 ? 1 : 0;', 'say $y == 9223372036854775807 ? 1 : 0;', 'say $y + 9223372036854775807;', 'say $y <=> 1e19;', 'say $y == "9007199254740992" ? 1:0;', 'say $y <=> "1e16";']
def body(v, use):
    return 'use v5.42;\nno warnings;\nmy @a = (%s); %s\nmy $c = $a[0];\n' % (v, use) + '\n'.join('{ my $y = $c; %s }' % o for o in OPS) + '\n'
def run(text):
    with tempfile.NamedTemporaryFile('w', suffix='.pl', delete=False, dir='.') as f: f.write(text)
    p = subprocess.run([PERL, f.name], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=20)
    os.unlink(f.name)
    return p.stdout + ('EXIT %d %s' % (p.returncode, p.stderr[:80]) if p.returncode else '')
def curly(v, op):
    text = 'use v5.42;\nmy $c = %s;\nmy $y = $c; %s\n' % (v, op)
    with open('cz.pl', 'w') as f: f.write(text)
    p = subprocess.run(['node', CURLYC, '-o', 'cz', 'cz.pl'], capture_output=True, text=True)
    if p.returncode: return 'REFUSED ' + p.stderr.strip()[:100]
    q = subprocess.run(['./cz'], capture_output=True, text=True)
    return (q.stdout.strip() + (' FAULT ' + q.stderr.strip()[:80] if q.returncode else ''))
n = 0; diffs = 0; wrong = 0; cache = {}
for v in VALS:
    fresh = run(body(v, ''))
    w = fresh.split('\n')
    for k, use in USES.items():
        got = run(body(v, use)); g = got.split('\n')
        n += len(OPS)
        if got == fresh: continue
        if len(w) != len(g): print('LEN v=%s via=%s' % (v, k), got[-200:]); continue
        for i, o in enumerate(OPS):
            if w[i] != g[i]:
                diffs += 1
                if (v, o) not in cache: cache[(v, o)] = curly(v, o)
                c = cache[(v, o)]
                bad = 'FAULT' not in c and 'REFUSED' not in c
                wrong += bad
                print('%s v=%s via=%s op=%r fresh=%r used=%r curly=%r' % ('WRONG' if bad else 'diff ', v, k, o, w[i], g[i], c))
                sys.stdout.flush()
print(n, 'comparisons,', diffs, 'differ,', wrong, 'where the compiler does not fault on the fresh value')
