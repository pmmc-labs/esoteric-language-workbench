#!/usr/bin/env python3
"""Review of step 8: sub names of 1 to 3 characters in 22 call positions
that briefs/step8-names.py did not try, definition first and calls first.
Names are batched and a failing batch is bisected to single names.
  CURLY_PERL=/opt/perl-5.42/bin/perl python3 sweep.py [maxlen]
"""
import os, subprocess, sys, string, tempfile, itertools
from concurrent.futures import ThreadPoolExecutor
PERL = os.environ['CURLY_PERL']
first = string.ascii_letters + '_'
rest = string.ascii_letters + string.digits + '_'
maxlen = int(sys.argv[1]) if len(sys.argv) > 1 else 3
names = [a for a in first] + [a + b for a in first for b in rest]
if maxlen >= 3:
    names += [a + b + c for a in first for b in rest for c in rest]
import os as _o
if _o.environ.get('NAMES'): names = _o.environ['NAMES'].split()
funcs = set(subprocess.run([PERL, '-MPod::Functions', '-e', 'print join " ", sort keys %Type'], capture_output=True, text=True).stdout.split())
# what step8-names.py already found perl refuses or reads otherwise
found = set('m q s y eq ge gt if le lt ne or qq qr qw qx tr not and xor cmp END try isa'.split()) | {'v%d' % i for i in range(10)}
names = [n for n in names if (n not in funcs and n not in found) or _o.environ.get('NAMES')]
LINES = [  # (tag, code, expected)
 ('minus-hard',  '$r = $q-{n}(3); say $r;', '13'),
 ('neg-hard',    '$r = -{n}(3); say $r;', '-13'),
 ('lt-hard',     '$r = $q <{n}(3) ? 1 : 0; say $r;', '0'),
 ('div-hard',    '$r = $q /{n}(3); say $r;', '2'),
 ('mul-hard',    '$r = 2 *{n}(3); say $r;', '26'),
 ('mod-hard',    '$r = 30 %{n}(3); say $r;', '4'),
 ('q-hard',      '$r = $c ?{n}(3) : 0; say $r;', '13'),
 ('colon-hard',  '$r = $c ? 0 :{n}(3); say $r;', '0'),
 ('before-colon','$r = $c ? {n}(3): 0; say $r;', '13'),
 ('x-right',     '$r = "a" x {n}(-8); say $r;', 'aa'),
 ('dot-hard',    '$r = "a" .{n}(3); say $r;', 'a13'),
 ('not-hard',    '$r = !{n}(3); say $r ? 1 : 0;', '0'),
 ('brace',       'if ($c) {{{n}(3); say "b"; }}', 'b'),
 ('for-parts',   'for ($r = {n}(3); $r < {n}(4); $r = {n}($r)) {{ say $r; }}', '13'),
 ('blank',       '$r = {n} (3); say $r;', '13'),
 ('newline',     '$r = {n}\n (3); say $r;', '13'),
 ('print',       'print {n}(3); print "\\n";', '13'),
 ('say-plus',    'say {n}(3) + 1;', '14'),
 ('args',        'say show({n}(3), {n}(4));', '[13,14]'),
 ('nested',      'say {n}({n}(3));', '23'),
 ('defined',     'say defined({n}(3)) ? "d" : "u";', 'd'),
 ('eq-hard',     '$r ={n}(3); say $r;', '13'),
 ('modifier',    '{n}(3) if {n}(3); say "m" unless {n}(3) < 0;', 'm'),
 ('unop',        'say length {n}(3);', '2'),
 ('after-block', 'if ($c) {{ }} {n}(3); say "ab";', 'ab'),
 ('after-block-nl', 'if ($c) {{ }}\n{n}(3);\n{n}\n(3); say "ab2";', 'ab2'),
 ('while-test',  'while ({n}(3) < 0) {{ }} until ({n}(3)) {{ }} say "w";', 'w'),
 ('neg-blank',   '$r = - {n}(3); say $r;', '-13'),
 ('ret-blank',   '$r = $q - {n} (3) - {n}\n(3); say $r;', '0'),
 ('unless-mod',  'say "u" unless {n}(-10); say "v" if {n}(1);', 'u\nv'),
 ('cmp-ops',     'say {n}(3) == {n}(3) ? "e" : "n"; say {n}(3) eq {n}(3) ? "e" : "n"; say {n}(3) x 2; say {n}(3) . {n}(3); say {n}(3) lt {n}(4) ? "l" : "g"; say {n}(3) <=> {n}(4);', 'e\ne\n1313\n1313\nl\n-1'),
 ('ternary-all', '$r = {n}(3) ? {n}(4) : {n}(5); say $r; $r = {n}(-10) ? {n}(4):{n}(5); say $r;', '14\n15'),
 ('logic',       '$r = {n}(-10) || {n}(4); say $r; $r = {n}(3) && {n}(4); say $r; $r = {n}(3) // {n}(4); say $r; $r = !{n}(3) || !!{n}(4); say $r;', '14\n14\n13\n1'),
]
only = os.environ.get('ONLY')
if only: LINES = [l for l in LINES if l[0] in only.split(',')]
HEAD = 'use v5.42;\nsub show($p, $s) {{ return "[" . $p . "," . $s . "]" }}\n'
def block(n):
    return '{ my $q = 26; my $r; my $c = 1;\n' + ''.join(code.format(n=n) + '\n' for _, code, _ in LINES) + '}\n'
def expect(ns):
    return ''.join(e + '\n' for _ in ns for _, _, e in LINES)
def prog(ns, order):
    subs = ''.join('sub %s($p) { return $p + 10 }\n' % n for n in ns)
    body = ''.join(block(n) for n in ns)
    return 'use v5.42;\nsub show($p, $s) { return "[" . $p . "," . $s . "]" }\n' + (subs + body if order == 'after' else body + subs)
def runp(text):
    with tempfile.NamedTemporaryFile('w', suffix='.pl', delete=False, dir='.') as f:
        f.write(text)
    try:
        p = subprocess.run([PERL, f.name], capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=60, errors='replace')
        return p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired:
        return '', 'TIMEOUT', -1
    finally:
        os.unlink(f.name)
def ok(ns, order):
    o, e, c = runp(prog(ns, order))
    return o == expect(ns) and e == '' and c == 0
def bisect(ns, order):
    if ok(ns, order): return []
    if len(ns) == 1: return ns
    h = len(ns) // 2
    return bisect(ns[:h], order) + bisect(ns[h:], order)
def detail(n, order):
    bad = []
    for tag, code, e in LINES:
        text = 'use v5.42;\nsub show($p, $s) { return "[" . $p . "," . $s . "]" }\n'
        sub = 'sub %s($p) { return $p + 10 }\n' % n
        body = '{ my $q = 26; my $r; my $c = 1;\n' + code.format(n=n) + '\n}\n'
        o, er, c = runp(text + (sub + body if order == 'after' else body + sub))
        if not (o == e + '\n' and er == '' and c == 0):
            bad.append((tag, o.strip(), er.strip().split('\n')[0][:90], c))
    return bad
B = 300
batches = [names[i:i+B] for i in range(0, len(names), B)]
res = {}
for order in ('after', 'before'):
    with ThreadPoolExecutor(4) as ex:
        out = list(ex.map(lambda b: bisect(b, order), batches))
    res[order] = [n for b in out for n in b]
print(len(names), 'names,', len(LINES), 'positions')
for order in res:
    print(order, len(res[order]), 'names fail')
allbad = sorted(set(res['after']) | set(res['before']), key=lambda n: (len(n), n))
for n in allbad:
    for order in ('after', 'before'):
        if n in res[order]:
            d = detail(n, order)
            print(n, order, '; '.join('%s: out=%r err=%r exit=%d' % x for x in d) if d else 'fails only among the others')
