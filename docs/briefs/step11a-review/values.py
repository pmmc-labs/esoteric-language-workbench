#!/usr/bin/env python3
"""Is an interpolated string "a value, worked out where it stands" (T196)?

Random programs of assignments, `.=`, `say` with a list, calls and `join`,
whose operands are interpolated strings, bare variables and bracketed
assignments, kept inside what the language takes:

  - D57/D76: no later piece of a row of dots, and no later item of a list,
    changes a scalar that an earlier piece or item is (a bare variable, or an
    assignment to it, which is "the variable itself");
  - T129/T198: the right side of `.=` is never an assignment of a
    concatenation or of a string of more than one piece;
  - an interpolated string is a VALUE: it may read anything, whatever changes
    later.  That is the claim under test.

The model works every string out where it stands, left to right.  perl must
print the same, with nothing on stderr.

    python3 values.py N SEED        N programs of 12 statements each
"""

import os
import random
import subprocess
import sys
from multiprocessing import Pool

PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
TMP = os.environ.get('REVIEW_TMP', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp'))

SC = ['$x', '$y', '$z']
INIT = {'$x': 'X', '$y': 'Y', '$z': 'Z', '@a': ['p', 'q', 'r'], '$i': 1}
HEADER = '''use v5.42;
my $x = "X"; my $y = "Y"; my $z = "Z"; my @a = ("p", "q", "r"); my $i = 1;
sub f($p, $q) { return "[$p$q]" }
sub g($p, $q = "d") { $x = $x . "g"; return "<$p$q>" }
sub dump_() { say "  = ", join("|", $x, $y, $z, @a); }
'''

# A tree: ('str', [parts]) parts: ('t', text) ('s', '$x') ('e', n) ('ei',) ('arr',) ('sl',) ('last',)
#         ('var', '$x') ('asg', target, op, row) ('rep', strnode) ('call', 'f'|'g', [rows]) ('join', sepnode, [rows])
#         ('tern', row, row)
# A row is a list of pieces joined by dots.  A target is '$x' or ('el', n).


def gen_str(r, minparts=1):
    parts = []
    for _ in range(r.randint(minparts, 3)):
        k = r.random()
        if k < 0.25:
            parts.append(('t', r.choice(['-', 'a', ' ', ',', '.'])))
        elif k < 0.6:
            parts.append(('s', r.choice(SC), r.random() < 0.3))
        elif k < 0.75:
            parts.append(('e', r.choice([0, 1, 2, -1])))
        elif k < 0.8:
            parts.append(('ei',))
        elif k < 0.9:
            parts.append(('arr',))
        elif k < 0.95:
            parts.append(('sl',))
        else:
            parts.append(('last',))
    return ('str', parts)


def gen_piece(r, depth):
    k = r.random()
    if k < 0.45:
        return gen_str(r)
    if k < 0.6:
        return ('var', r.choice(SC))
    if depth >= 2:
        return gen_str(r)
    if k < 0.8:
        return ('asg', gen_target(r), r.choice(['=', '=', '.=']), gen_row(r, depth + 1, 2))
    if k < 0.85:
        return ('rep', gen_str(r))
    if k < 0.93:
        return ('call', r.choice(['f', 'g']), [gen_row(r, depth + 1, 2), gen_row(r, depth + 1, 2)])
    if k < 0.97:
        return ('join', gen_str(r), [gen_row(r, depth + 1, 2), gen_row(r, depth + 1, 2)])
    return ('tern', gen_row(r, depth + 1, 2), gen_row(r, depth + 1, 2))


def gen_row(r, depth, maxn=4):
    return [gen_piece(r, depth) for _ in range(r.randint(1, maxn))]


def gen_target(r):
    return r.choice(SC) if r.random() < 0.75 else ('el', r.choice([0, 1]))


# ---- what a piece changes, and what it "is" --------------------------------

def tname(t):
    return t if isinstance(t, str) else '$a[%d]' % t[1]


def changes(node):
    """Every variable a piece can change, sub g's $x included."""
    k = node[0]
    if k == 'asg':
        return {tname(node[1])} | row_changes(node[3])
    if k == 'call':
        s = set().union(*[row_changes(a) for a in node[2]])
        return s | ({'$x'} if node[1] == 'g' else set())
    if k == 'join':
        return set().union(*[row_changes(a) for a in node[2]])
    if k == 'tern':
        return row_changes(node[1]) | row_changes(node[2])
    return set()


def row_changes(row):
    return set().union(*[changes(p) for p in row]) if row else set()


def names(node):
    """What a piece is, as a variable itself: a bare variable, or an assignment."""
    if node[0] == 'var':
        return {node[1]}
    if node[0] == 'asg':
        return {tname(node[1])}
    if node[0] == 'tern':          # ? : gives one of its operands
        out = set()
        for row in (node[1], node[2]):
            if len(row) == 1:
                out |= names(row[0])
        return out
    return set()


def legal_row(row, first=None):
    """D57: no later piece changes what an earlier piece is.  `first` is the
    left of a `.=`."""
    seen = set(first or ())
    for p in row:
        if changes(p) & seen:
            return False
        if not legal(p):
            return False
        seen |= names(p)
    return True


def legal_list(rows):
    """D76 for the items of a list or a call's arguments: an item that is one
    piece, a variable itself, is named; a later item may not change it."""
    seen = set()
    for row in rows:
        if row_changes(row) & seen:
            return False
        if not legal_row(row):
            return False
        if len(row) == 1:
            seen |= names(row[0])
    return True


def is_concat(row):
    return len(row) > 1


def legal(node):
    k = node[0]
    if k == 'asg':
        t, op, row = node[1], node[2], node[3]
        if op == '.=':
            if not legal_row(row, first={tname(t)}):
                return False
            # T129 and T198: the right side of .= may not be an assignment of
            # a concatenation, nor of a string of more than one piece
            if len(row) == 1 and row[0][0] == 'asg' and row[0][2] == '=':
                inner = row[0][3]
                if is_concat(inner):
                    return False
                if len(inner) == 1 and inner[0][0] == 'str' and not one_piece(inner[0]):
                    return False
            return True
        return legal_row(row)
    if k == 'call':
        return legal_list(node[2])
    if k == 'join':
        return legal_list(node[2])
    if k == 'tern':
        return legal_row(node[1]) and legal_row(node[2])
    return True


def one_piece(s):
    """T198's exception: one variable, one array or one element and nothing else."""
    return len(s[1]) == 1 and s[1][0][0] in ('s', 'e', 'ei', 'arr')


# ---- writing it as perl -----------------------------------------------------

def w_str(s):
    out = []
    parts = s[1]
    for n, p in enumerate(parts):
        nxt = parts[n + 1] if n + 1 < len(parts) else None
        # braces when asked, and whenever a letter follows that would go on with the name
        glue = nxt is not None and nxt[0] == 't' and nxt[1][0].isalnum()
        if p[0] == 't':
            out.append(p[1])
        elif p[0] == 's':
            out.append('${%s}' % p[1][1:] if (p[2] or glue) else p[1])
        elif p[0] == 'e':
            out.append('$a[%d]' % p[1])
        elif p[0] == 'ei':
            out.append('$a[$i]')
        elif p[0] == 'arr':
            out.append('@{a}' if glue else '@a')
        elif p[0] == 'sl':
            out.append('@a[0, $i]')
        elif p[0] == 'last':
            out.append('$#{a}' if glue else '$#a')
    return '"' + ''.join(out) + '"'


def w_piece(p):
    k = p[0]
    if k == 'str':
        return w_str(p)
    if k == 'var':
        return p[1]
    if k == 'asg':
        return '(%s %s %s)' % (tname(p[1]), p[2], w_row(p[3]))
    if k == 'rep':
        return '(%s x 2)' % w_str(p[1])
    if k == 'call':
        return '%s(%s)' % (p[1], ', '.join(w_row(a) for a in p[2]))
    if k == 'join':
        return 'join(%s, %s)' % (w_str(p[1]), ', '.join(w_row(a) for a in p[2]))
    if k == 'tern':
        return '($i ? %s : %s)' % (w_row(p[1]), w_row(p[2]))


def w_row(row):
    return ' . '.join(w_piece(p) for p in row)


# ---- the model ---------------------------------------------------------------

def e_str(s, env):
    out = []
    a = env['@a']
    for p in s[1]:
        if p[0] == 't':
            out.append(p[1])
        elif p[0] == 's':
            out.append(env[p[1]])
        elif p[0] == 'e':
            out.append(a[p[1]])
        elif p[0] == 'ei':
            out.append(a[1])
        elif p[0] == 'arr':
            out.append(' '.join(a))
        elif p[0] == 'sl':
            out.append(a[0] + ' ' + a[1])
        elif p[0] == 'last':
            out.append(str(len(a) - 1))
    return ''.join(out)


def get(env, t):
    return env[t] if isinstance(t, str) else env['@a'][t[1]]


def put(env, t, v):
    if isinstance(t, str):
        env[t] = v
    else:
        env['@a'][t[1]] = v


def e_piece(p, env):
    k = p[0]
    if k == 'str':
        return e_str(p, env)
    if k == 'var':
        return env[p[1]]
    if k == 'asg':
        if p[2] == '=':
            v = e_row(p[3], env)
        else:
            # `$t .= E`: with D57 kept, nothing in E changes $t, so its value
            # before or after is the same
            v = get(env, p[1]) + e_row(p[3], env)
        put(env, p[1], v)
        return v
    if k == 'rep':
        return e_str(p[1], env) * 2
    if k == 'call':
        args = [e_row(a, env) for a in p[2]]
        if p[1] == 'f':
            return '[' + args[0] + args[1] + ']'
        env['$x'] = env['$x'] + 'g'
        return '<' + args[0] + args[1] + '>'
    if k == 'join':
        sep = e_str(p[1], env)
        return sep.join(e_row(a, env) for a in p[2])
    if k == 'tern':
        return e_row(p[1], env)


def e_row(row, env):
    return ''.join(e_piece(p, env) for p in row)


def gen_program(seed):
    r = random.Random(seed)
    env = {k: (list(v) if isinstance(v, list) else v) for k, v in INIT.items()}
    lines = []
    want = []
    n = 0
    while n < 12:
        kind = r.random()
        if kind < 0.6:
            node = ('asg', gen_target(r), r.choice(['=', '=', '.=']), gen_row(r, 0))
            if not legal(node):
                continue
            lines.append('%s %s %s;' % (tname(node[1]), node[2], w_row(node[3])))
            e_piece(node, env)
        else:
            rows = [gen_row(r, 0, 3) for _ in range(r.randint(1, 3))]
            if not legal_list(rows):
                continue
            lines.append('say(%s);' % ', '.join(w_row(a) for a in rows))
            want.append(''.join(e_row(a, env) for a in rows))
        lines.append('dump_();')
        want.append('  = ' + '|'.join([env['$x'], env['$y'], env['$z']] + env['@a']))
        n += 1
        if any(len(v) > 400 for v in [env['$x'], env['$y'], env['$z']] + env['@a']):
            break
    return HEADER + '\n'.join(lines) + '\n', '\n'.join(want) + '\n'


def run(seed):
    prog, want = gen_program(seed)
    path = os.path.join(TMP, 'v%d.pl' % seed)
    with open(path, 'w') as f:
        f.write(prog)
    try:
        r = subprocess.run([PERL, path], capture_output=True, timeout=10)
        got, err, code = r.stdout.decode(), r.stderr.decode(), r.returncode
    except subprocess.TimeoutExpired:
        got, err, code = '', 'TIMEOUT', -1
    if got == want and err == '' and code == 0:
        os.unlink(path)
        return None
    return seed, prog, want, got, err


def main():
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    os.makedirs(TMP, exist_ok=True)
    bad = []
    with Pool(4) as pool:
        for res in pool.imap_unordered(run, range(seed, seed + n), chunksize=32):
            if res:
                bad.append(res)
    bad.sort()
    print('%d programs, %d differ' % (n, len(bad)))
    for seed_, prog, want, got, err in bad[:8]:
        w, g = want.split('\n'), got.split('\n')
        at = next((k for k in range(min(len(w), len(g))) if w[k] != g[k]), min(len(w), len(g)))
        stmts = prog[len(HEADER):].split('\n')
        print('--- seed %d, first difference at output line %d' % (seed_, at + 1))
        print('\n'.join(stmts))
        print('model: %r\nperl:  %r\nerr: %s' % (w[at:at + 2], g[at:at + 2], err[:300]))


if __name__ == '__main__':
    main()
