#!/usr/bin/env python3
"""Step 8's evidence for which names a program's sub may have (D21, T28).

For 3,448 names (every name of one or two characters, and the words perl
or its documents make special) it defines `sub NAME($p)`, calls it eight
ways, and asks perl 5.42 whether the sub was simply called, in silence;
once with the definition first and once with the calls first. perl's own
functions (Pod::Functions) are left out: every one is refused already, and
calling `mkdir` or `sleep` blind is not something to do.

    CURLY_PERL=/opt/perl-5.42/bin/perl python3 docs/briefs/step8-names.py

2026-11-25, perl 5.42.0: 59 names fail. 47 in both orders, each a word of
perl's (m q s y eq ge gt if le lt ne or qq qr qw qx tr not and xor cmp;
DESTROY AUTOLOAD BEGIN END INIT CHECK UNITCHECK; true false trim ceil floor
isa try catch finally weaken blessed reftype refaddr indexed is_tainted
is_weak unweaken; __END__ __DATA__). 12 only when called before the
definition: v0 to v9, v65, v1_0, which perl reads as version strings. None
fails only when called after. It is a record, not a test.

The review of step 8 found what this missed (briefs/step8-review/): `else
elsif for foreach unless until while` are in neither list used here, and
none is a sub's name to perl, so it is 66 of 3,455. They are not added:
a sub named for a loop word, called blind, filled the reviewer's machine.
"""
import itertools, os, subprocess, sys, string, tempfile
from concurrent.futures import ThreadPoolExecutor
PERL = os.environ['CURLY_PERL']
first = string.ascii_letters + '_'
rest = string.ascii_letters + string.digits + '_'
names = [a for a in first] + [a + b for a in first for b in rest]
names += ['v1', 'v65', 'v1_0', 'e1', 'x3', 'main', 'STDIN', 'STDOUT', 'STDERR', 'ARGV', 'DATA', 'ENV', 'INC', 'inf', 'nan', 'err', 'dump', 'format', 'default', 'given', 'when', 'ADJUST', 'CORE', 'SUPER', 'UNIVERSAL', 'can', 'DOES', 'VERSION', 'import', 'unimport', 'DESTROY', 'AUTOLOAD', 'BEGIN', 'END', 'INIT', 'CHECK', 'UNITCHECK', 'CLONE', 'true', 'false', 'trim', 'ceil', 'floor', 'any', 'all', 'isa', 'try', 'catch', 'finally', 'defer', 'class', 'field', 'method', 'say', 'state', 'fc', 'evalbytes', 'weaken', 'blessed', 'reftype', 'refaddr', 'indexed', 'stringify', 'is_tainted', 'created_as_number', 'created_as_string', 'is_weak', 'unweaken', 'export_lexically', 'load_module', 'is_bool', '__SUB__', '__CLASS__', '__PACKAGE__', '__LINE__', '__FILE__', '__END__', '__DATA__', 'EQ', 'NE', 'LT', 'eq', 'ne', 'lt', 'not', 'and', 'xor', 'cmp', 'sub', 'our', 'local', 'my', 'use', 'no', 'do', 'if']
import subprocess
funcs = subprocess.run([PERL, '-MPod::Functions', '-e', 'print join " ", sort keys %Type'], capture_output=True, text=True).stdout.split()
known = set(funcs)
names = [n for n in names if n not in known]
names = list(dict.fromkeys(names))
BODY = '''sub show($p) {{ return "[$p]" }}
my $r = 1 + {n}(3); say $r;
say {n}(3);
say show({n}(3));
say "a" . {n}(3);
my $q = 5 - {n}(3); say $q;
say 2 * {n}(3) + 1;
{n}(3);
if ({n}(3) == 13) {{ say "t" }}
'''
EXPECT = '14\n13\n[13]\na13\n-8\n27\nt\n'
SUB = 'sub {n}($p) {{ return $p + 10 }}\n'
def run(n):
    res = []
    for order, prog in (('after', 'use v5.42;\n' + SUB.format(n=n) + BODY.format(n=n)), ('before', 'use v5.42;\n' + BODY.format(n=n) + SUB.format(n=n))):
        with tempfile.NamedTemporaryFile('w', suffix='.pl', delete=False) as f:
            f.write(prog)
        try:
            p = subprocess.run([PERL, f.name], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=20, errors='replace')
            ok = p.stdout == EXPECT and p.stderr == '' and p.returncode == 0
        except subprocess.TimeoutExpired:
            ok = False
        os.unlink(f.name)
        res.append(ok)
    return n, res
with ThreadPoolExecutor(8) as ex:
    out = list(ex.map(run, names))
bad = [(n, r) for n, r in out if not all(r)]
print(len(names), 'names;', len(bad), 'where perl does not simply call the sub')
both = [n for n, r in bad if not r[0] and not r[1]]
onlybefore = [n for n, r in bad if r[0] and not r[1]]
onlyafter = [n for n, r in bad if not r[0] and r[1]]
print('fails both orders:', ' '.join(both))
print('fails only when called before its definition:', ' '.join(onlybefore))
print('fails only when called after:', ' '.join(onlyafter))
