#!/usr/bin/env python3
"""The compiler held to perl, and to the reviewer's model of step 5.

    python3 docs/briefs/step5-review/compiler.py KIND SEED COUNT [batch=N] [faults=N | all-faults] [plant]

KIND is the generator a program is drawn from:

  late     gen_late.py: assignment as an operator, ++/--, OP=, the logical
           operators and builtins over three variables, every operand in
           brackets
  prec     the same trees printed with the fewest brackets perlop's table
           allows (minshow.py)
  struct   gen_struct.py: blocks, if/elsif/else, unless, modifiers, a `my` in
           a condition, shadowing
  past     gen_past.py: a value of every kind and edge, read-only statements,
           then ++ -- OP= and one observation

and KIND-min (late-min is prec) prints a kind's trees with the fewest
brackets, KIND-bare with the fewest brackets and `say E;` for `say(E);`.

Each program is run by the model alone first (model.py: the proposal's words
over the built runtime's operators). Then:

  the model prints   The programs go to the compiler N to a file (40), each in
                     a block of its own behind a line that says which it is,
                     and the same file goes to perl. The compiled program must
                     print what perl prints, and perl must say nothing. A
                     program the compiler refuses or faults on is taken out
                     and counted, by its message: the compiler may be stricter.
  the model faults   One rides last in each file, where its fault costs
                     nothing; of the rest one in four goes alone (one in N
                     with faults=N, all of them with all-faults). The compiler must refuse it, or fault
                     having printed the beginning of what perl prints, or
                     print what perl prints with perl silent.

Whatever differs in a file is run again alone, at the top of a file with no
block round it, before it is called anything. WRONG is a program the compiler
accepts that runs without a fault and prints what perl doesn't, or that perl
complains of. A few programs in a hundred also go alone as a check on the
blocks. `plant` puts two programs known to be WRONG among the others, as a
check on this script: both must be reported. Not part of make test. One perl
runs at a time.
"""
import collections, os, random, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path.insert(0, HERE)
import model, minshow, gen_late, gen_struct, gen_past

PERL = os.environ.get('CURLY_PERL', 'perl')
ENV = dict(os.environ, PERL_HASH_SEED='1')
work = tempfile.mkdtemp(prefix='step5-review-')


def draw(kind, r, state):
    """(tree, its statements as text at a given indent)."""
    base = kind.split('-')[0]
    if base == 'prec': base, kind = 'late', 'late-min'
    if base == 'late':
        p = gen_late.program(r)
    elif base == 'struct':
        p = gen_struct.program(r)
    elif base == 'past':
        if 'inits' not in state: state['inits'] = gen_past.inits()
        p = gen_past.program(r, state['inits'])
    else:
        raise SystemExit('no such kind: ' + kind)
    minshow.BARE = kind.endswith('-bare')
    return p, (minshow.block if '-' in kind else model.show_block)


class Item:
    def __init__(self, n, prog, printer):
        self.n = n
        self.prog = prog
        self.body = printer(prog, '    ')
        self.alone = 'use v5.42;\n' + printer(prog, '')
        self.out, self.fault = model.run(prog)


def run(args, **kw):
    try:
        return subprocess.run(args, capture_output=True, stdin=subprocess.DEVNULL, timeout=60, **kw)
    except subprocess.TimeoutExpired:
        return None


def both(text):
    """What the compiler and perl make of one file:
    ('refused', line, message) | ('broken', stderr) | ('unclean', what perl -c said) |
    ('ran' | 'faulted', stdout, fault line, fault message, perl stdout, perl stderr, perl exit)"""
    path = os.path.join(work, 'p.pl')
    open(path, 'w').write(text)
    c = run(['node', os.path.join(ROOT, 'bin', 'curlyc.ts'), '-o', os.path.join(work, 'p'), path])
    if c is None: return ('broken', 'the compiler did not finish')
    if c.returncode == 1:
        m = re.match(r'[^:]*:(\d+):\d+: (.*)', c.stderr.decode().strip().split('\n')[-1])
        return ('refused', int(m.group(1)), m.group(2))
    if c.returncode != 0: return ('broken', c.stderr.decode()[:300])
    b = run([os.path.join(work, 'p')])
    k = run([PERL, '-c', 'p.pl'], cwd=work, env=ENV)
    if k is None or k.returncode != 0 or k.stderr != b'p.pl syntax OK\n':
        # the first rule: perl -c takes every file the compiler does, and says nothing
        return ('unclean', (k.stderr if k is not None else b'perl -c did not finish'))
    p = run([PERL, 'p.pl'], cwd=work, env=ENV)
    if b is None: return ('broken', 'the compiled program did not finish')
    pout, perr, pexit = (p.stdout, p.stderr, p.returncode) if p is not None else (b'', b'perl did not finish', -1)
    if b.returncode == 0: return ('ran', b.stdout, 0, '', pout, perr, pexit)
    m = re.match(r'fault: (.*) at \S+ line (\d+)\.', b.stderr.decode().strip().split('\n')[-1])
    if b.returncode != 1 or not m: return ('broken', 'exit %d, stderr %r' % (b.returncode, b.stderr[:300]))
    return ('faulted', b.stdout, int(m.group(2)), m.group(1), pout, perr, pexit)


def shape(msg):
    """A refusal or a fault by its kind: the message without its names and numbers."""
    msg = re.sub(r'\$\w+', '$v', msg)
    msg = re.sub(r'^(say|print) \$v \S+:', 'say $v ...:', msg)
    msg = re.sub(r"'[^']*'", "'..'", msg)
    return re.sub(r'\d+', 'N', msg)[:80]


counts = collections.Counter()
kinds = collections.Counter()
examples = {}
wrong = []
log = None


def note(key, item, detail=''):
    kinds[key] += 1
    if key not in examples:
        examples[key] = item.alone + ('## ' + detail + '\n' if detail else '')


def alone(item):
    """One program at the top of a file. Returns True if it is WRONG."""
    r = both(item.alone)
    if r[0] == 'refused':
        counts['the compiler refuses'] += 1
        note('refused: ' + shape(r[2]) + (' (the model faults)' if item.fault else ''), item)
        return False
    if r[0] == 'broken':
        wrong.append((item, 'THE COMPILER BREAKS: ' + r[1]))
        return True
    if r[0] == 'unclean':
        wrong.append((item, 'accepts it; perl -c says %r' % r[1]))
        return True
    what, out, line, msg, pout, perr, pexit = r
    if what == 'faulted':
        if not pout.startswith(out):
            wrong.append((item, 'faults (%s) having printed %r, which is not the beginning of perl\'s %r' % (msg, out, pout)))
            return True
        counts['the compiler faults'] += 1
        note('faults: ' + shape(msg) + ('' if item.fault else ' (the model prints)'), item, 'perl prints %r, and says %r' % (pout[:200], perr[:200]))
        return False
    if pout != out or perr or pexit:
        wrong.append((item, 'prints %r; perl prints %r, says %r, exit %d' % (out, pout, perr, pexit)))
        return True
    agreed(item, out)
    return False


def agreed(item, out):
    counts['the compiler prints what perl prints, perl silent'] += 1
    if item.fault is not None:
        counts['... where the model faults'] += 1
        note('agrees with perl where the model faults: ' + shape(item.fault), item)
    elif item.out is not None and item.out != out:
        counts['... where the model prints something else'] += 1
        note('agrees with perl where the model prints something else', item, 'the model: %r; both: %r' % (item.out, out))


def which(starts, line):
    k = 0
    while k + 1 < len(starts) and starts[k + 1] <= line: k += 1
    return k


def segments(out, n):
    """The output of each of n programs, by the marker lines."""
    parts = re.split(rb'^#\d+\n', out, flags=re.M)[1:]
    return parts + [None] * (n - len(parts))


def batch(items):
    while items:
        text = 'use v5.42;\n'
        starts = []
        for k, it in enumerate(items):
            starts.append(text.count('\n') + 1)
            text += 'say("#%d");\n{\n%s}\n' % (k, it.body)
        r = both(text)
        if r[0] == 'refused':
            k = which(starts, r[1])
            counts['the compiler refuses'] += 1
            note('refused: ' + shape(r[2]) + (' (the model faults)' if items[k].fault else ''), items[k])
            del items[k]
            continue
        if r[0] == 'broken':
            # find which, one at a time
            for it in items: alone(it)
            return
        if r[0] == 'unclean':
            m = re.search(r' line (\d+)', r[1].decode('utf-8', 'replace'))
            if not m:
                for it in items: alone(it)
                return
            it = items.pop(which(starts, int(m.group(1))))
            if not alone(it):
                counts['differs in a file of many and not alone'] += 1
                note('differs in a file of many and not alone', it, 'perl -c: %r' % r[1])
            continue
        what, out, line, msg, pout, perr, pexit = r
        last = len(items) if what == 'ran' else which(starts, line)       # programs before this one ran to their ends
        mine, perls = segments(out, len(items)), segments(pout, len(items))
        bad = None
        for k in range(last):
            if mine[k] != perls[k]: bad = k; break
        if bad is None and what == 'faulted' and not (perls[last] or b'').startswith(mine[last] or b''): bad = last
        if bad is None and perr:
            # a complaint of perl's about a program that ran to its end here
            for l in perr.decode('utf-8', 'replace').split('\n'):
                m = re.search(r' line (\d+)', l)
                if m and which(starts, int(m.group(1))) < last: bad = which(starts, int(m.group(1))); break
            if bad is None and what == 'ran': bad = 0 if not re.search(r' line (\d+)', perr.decode('utf-8', 'replace')) else None
        if bad is None and what == 'ran' and pexit: bad = len(items) - 1
        if bad is not None:
            it = items.pop(bad)
            if not alone(it):
                counts['differs in a file of many and not alone'] += 1
                note('differs in a file of many and not alone', it)
            continue
        for k in range(last): agreed(items[k], mine[k])
        if what == 'ran': return
        it = items[last]
        counts['the compiler faults'] += 1
        note('faults: ' + shape(msg) + ('' if it.fault else ' (the model prints)'), it)
        items = items[last + 1:]


def main():
    kind, seed, count = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    size = 40
    for a in sys.argv[4:]:
        if a.startswith('batch='): size = int(a[6:])
    one_in = 1 if 'all-faults' in sys.argv else 4
    for a in sys.argv[4:]:
        if a.startswith('faults='): one_in = int(a[7:])
    r = random.Random(seed)
    state = {}
    prints, faults = [], []
    for n in range(count):
        prog, printer = draw(kind, r, state)
        it = Item(n, prog, printer)
        (faults if it.fault is not None else prints).append(it)
    if 'plant' in sys.argv:
        # the check of this script: two programs known to differ from perl (one in what it prints,
        # one in what perl says), put among the others; both must come out WRONG
        L, v = model.lit, lambda n: ('var', n)
        p1 = [('my', 't', L('"t"')), ('my', 'u', L('"u"')), ('my', 'x', L('"a"')),
              ('expr', ('asg', '.=', v('t'), ('asg', '=', v('u'), ('bin', '.', v('x'), v('x'))))), ('say', v('t')), ('say', v('u'))]
        p2 = [('my', 'x', L('9007199254740994.0')), ('expr', ('post', '++', 'x')), ('say', ('bin', '-', v('x'), L('9007199254740000')))]
        for p in (p1, p2):
            prints.insert(r.randrange(len(prints) + 1), Item(-1, p, model.show_block))
    print('%s, seed %d: %d programs; the model prints for %d and faults on %d' % (kind, seed, count, len(prints), len(faults)), flush=True)
    done = 0
    while prints:
        group, prints = prints[:size], prints[size:]
        for it in group[:1]:
            if it.n % 100 < 3: alone(it); group = group[1:]          # a check on the blocks
        if faults: group.append(faults.pop())
        batch(group)
        done += size
        if done % 2000 < size: print('  ... %d of the printing programs; %d WRONG so far' % (done, len(wrong)), flush=True)
    sampled = 0
    for n, it in enumerate(faults):
        if n % one_in == 0:
            alone(it); sampled += 1
    counts['the model faults, and the program was not run'] = len(faults) - sampled
    report('%s-%d' % (kind, seed))


class Text:
    """A program written as text, for a script with no tree: the model has no say."""
    def __init__(self, n, statements):
        self.n = n
        self.prog = None
        self.body = ''.join('    ' + l + '\n' for l in statements.split('\n'))
        self.alone = 'use v5.42;\n' + statements + '\n'
        self.out, self.fault = None, None


def report(name):
    print()
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]): print('%7d  %s' % (v, k))
    print('%7d  WRONG' % len(wrong))
    by = collections.OrderedDict()
    for it, why in wrong:
        m = re.search(r"(Found = in conditional|Lost precision|Reversed [-+]= operator|masks earlier|Useless use|syntax error|Identifier too long|isn't numeric|uninitialized|did not finish|BREAKS)", why)
        by.setdefault(m.group(1) if m else 'prints what perl does not', []).append((it, why))
    for k, v in by.items(): print('%7d    of them: %s' % (len(v), k))
    print()
    for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]): print('%7d  %s' % (v, k))
    logname = os.path.join(tempfile.gettempdir(), 'step5-review-%s.log' % name)
    with open(logname, 'w') as f:
        for it, why in wrong: f.write('==== WRONG\n%s## the compiler %s\n\n' % (it.alone, why))
        for k, v in examples.items(): f.write('==== the first of: %s\n%s\n' % (k, v))
    print('\nthe WRONG programs, and the first of each kind: ' + logname)
    for k, v in by.items():
        for it, why in v[:2 if k != 'prints what perl does not' else 6]: print('==== WRONG (%s)\n%s## the compiler %s' % (k, it.alone, why[:600]))


if __name__ == '__main__':
    main()
