#!/usr/bin/env python3
"""Step 10 review. Is perl's optimised sort ({ $a <=> $b }, { $b <=> $a }, { $a cmp $b },
{ $b cmp $a }, no block, reverse sort, in place) the same as the merge run with the
language's own pairwise answers? The pairwise answers come from today's compiler
(one `say $v[i] OP $v[j];` a line; a fault names its line and is recorded as F)."""
import os, subprocess, sys, random, re
PERL = os.environ['CURLY_PERL']; CURLYC = '/workspace/esoteric-language-workbench/bin/curlyc.ts'
VALS = ['0', '1', '-1', '5', '9007199254740992', '9007199254740993', '9007199254740994', '9223372036854775807', '-9007199254740993', '9007199254740991',
 '0.5', '9007199254740992.0', '9007199254740994.0', '9223372036854775807.0', '1e19', '-9007199254740992.0', '1.5', '4611686018427387904.0', '1e15', '2.0',
 '"10"', '"9"', '"1e3"', '"3.0"', '" 3"', '"9007199254740993"', '"9007199254740992"', '"9007199254740992.0"', '"1.5"', '"-0"', '"9223372036854775807"', '"1e16"', '"0.5"', '"1e19"', '"9007199254740994.0"', '"abc"', '"B"', '""',
 '(1 == 1)', '(1 == 2)', '18446744073709551615.0', '"9007199254740995"', '9223372036854775806', '"9223372036854775806"', '9007199254740995']
N = len(VALS)
def matrix(op):
    M = [[None]*N for _ in range(N)]
    while True:
        lines = ['use v5.42;', 'my @v = (' + ', '.join(VALS) + ');']
        where = {}
        for i in range(N):
            for j in range(N):
                if M[i][j] is None:
                    where[len(lines)+1] = (i, j); lines.append('say $v[%d] %s $v[%d];' % (i, op, j))
        open('mx.pl', 'w').write('\n'.join(lines) + '\n')
        p = subprocess.run(['node', CURLYC, '-o', 'mx', 'mx.pl'], capture_output=True, text=True)
        assert p.returncode == 0, p.stderr
        q = subprocess.run(['./mx'], capture_output=True, text=True)
        out = q.stdout.split('\n')
        ks = sorted(where)
        for n, k in enumerate(ks):
            if n < len(out) - 1: M[where[k][0]][where[k][1]] = out[n]
        if q.returncode == 0: break
        m = re.search(r'line (\d+)\.', q.stderr); assert m, q.stderr
        M[where[int(m.group(1))][0]][where[int(m.group(1))][1]] = 'F'
    return M
def trial_prog(M, op, subsets):
    L = ['use v5.42; no warnings;', 'my @M = (' + ','.join('[' + ','.join('"%s"' % x for x in row) + ']' for row in M) + ');', 'my ($bad, $n, $faults) = (0, 0, 0);']
    forms = {'<=>': ['sort { $a <=> $b } @v', 'reverse sort { $a <=> $b } @v'], 'cmp': ['sort { $a cmp $b } @v', 'sort @v', 'reverse sort @v']}[op]
    dforms = {'<=>': ['sort { $b <=> $a } @v'], 'cmp': ['sort { $b cmp $a } @v']}[op]
    for s in subsets:
        vals = ', '.join(VALS[i] for i in s); idx = ', '.join(map(str, s))
        for f in forms + dforms + ['INPLACE']:
            desc = f in dforms
            cmpx = '$M[$b][$a]' if desc else '$M[$a][$b]'
            if f == 'INPLACE': run = 'my @got = @v; @got = sort { $a %s $b } @got;' % op
            else: run = 'my @got = %s;' % f
            rev = 'reverse ' if f.startswith('reverse') else ''
            L.append('{ my @v = (%s); my @i = (%s); my @o; my $ok = eval { @o = %ssort { my $r = %s; die "F\\n" if $r eq "F"; $r } @i; 1 }; if (!$ok) { $faults++ } else { my @w = map { $v[$_] } (map { my $k = $_; (grep { $i[$_] == $k } 0 .. $#i)[0] } @o); my @f = (%s); %s $n++; my $x = join("|", map { defined($_) ? $_ : "u" } @got); my $y = join("|", @f[@o]); my @fr = (%s); my %%pos; @pos{@i} = (0 .. $#i); my $y2 = join("|", map { $fr[$pos{$_}] } @o); if ($x ne $y2) { $bad++; say "DIFF %s on (%s): perl $x; the merge with pairwise answers $y2" if $bad < 40; } } }' % (vals, idx, rev, cmpx, vals, run, vals, f.replace('@', '\\@').replace('$', '\\$'), vals.replace('"', '\\"').replace('@','\\@')))
    L.append('say "$n sorts compared, $bad differ, $faults where a compared pair faults";')
    return '\n'.join(L) + '\n'
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
for op in ['<=>', 'cmp']:
    import json, os.path
    fn = 'M-%s.json' % ('num' if op == '<=>' else 'cmp')
    if os.path.exists(fn): M = json.load(open(fn))
    else:
        M = matrix(op); json.dump(M, open(fn, 'w'))
    nf = sum(row.count('F') for row in M); print(op, 'pairs that fault:', nf, 'of', N*N); sys.stdout.flush()
    # only values that do not fault against themselves are worth sorting
    ok = [i for i in range(N) if M[i][i] != 'F' and VALS[i] != '1e15']  # 1e15 prints two ways in perl by its past (D36: the language faults on printing it), which is not an order
    subsets = []
    for t in range(1200):
        k = random.choice([2, 2, 3, 3, 4, 5, 6, 8, 12, 20])
        subsets.append([random.choice(ok) for _ in range(k)] if t % 3 == 0 else random.sample(ok, min(k, len(ok))))
    open('tr.pl', 'w').write(trial_prog(M, op, subsets))
    p = subprocess.run([PERL, 'tr.pl'], capture_output=True, text=True, timeout=600)
    print(p.stdout[-6000:], p.stderr[-2000:]); sys.stdout.flush()
