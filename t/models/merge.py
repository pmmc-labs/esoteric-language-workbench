#!/usr/bin/env python3
"""perl's merge sort, as a thing that asks (step 10c; D82, D83).

`merge(n)` sorts n things it never sees. It is a generator: it yields the
two it wants compared, as their places in the list as it was given (0 to
n - 1), is sent how they compare (below zero, zero, above), and at the
end returns the order: the places, sorted. So whoever drives it runs the
comparison, which is how the language's `sort` is built: the runtime's
merge asks, and the generated code answers (D83).

It is `S_sortsv_flags_impl` and `dynprep` of perl 5.42's pp_sort.c, by
Peter McIlroy and John P. Linderman, statement for statement, with its
pointers as indexes: every comparison is the one perl makes, in perl's
order (D82), so a block that prints, counts, or is no consistent order
shows the same here as there. perl keeps two arrays, the list and one
beside it, and writes in each both the things being sorted and, at the
start of each run, where that run ends (`NEXT`); a pointer into one
array and the same offset into the other are one index here.

    python3 t/models/merge.py            # hold it to perl: about 4,000 lists
    python3 t/models/merge.py --self     # break it on purpose, and see it caught
    python3 t/models/merge.py --cases    # the lists, one a line, for the runtime's test

The check runs perl with a block that logs each pair it is given, over
lists of 0 to 300 values: random ones, sorted, reversed, long runs each
way for the pass that looks for them (16 and more in order), few keys
for the pass that gallops (6 and more low in a row), and blocks that are
no order at all, whose answers are a table perl and this are both
given. The pairs logged and the order must be the same.
"""

import os
import random
import subprocess
import sys

PTHRESH = 8     # pairs with one sense before a run is looked for
RTHRESH = 6     # low in a row before a merge steps by doubling

def dynprep(list1, list2, nmemb, cmp):
    """Find the runs: pairs, and longer ones where 8 pairs agree. A run
    that goes down is turned round. `list2[start]` is where each run
    ends. Returns how many runs."""
    runs = 0
    b = 0
    last = nmemb
    sense = (yield from cmp(list1[b], list1[b + 1])) > 0
    p2 = 0
    while b < last:
        # We just started, or just reversed sense: t at the end of the
        # pairs with the prevailing sense.
        p = b + 2
        t = p
        while True:
            p += 1
            if not p < last:
                break
            if ((yield from cmp(list1[t], list1[p])) > 0) != sense:
                break
            p += 1
            t = p
        q = b
        while True:
            p = r = b + 2 * PTHRESH
            if r >= t:
                p = r = t               # too short to care about
            else:
                while True:
                    if ((yield from cmp(list1[p - 1], list1[p])) > 0) != sense:
                        break
                    p -= 2
                    if not p > q:
                        break
                if p <= q:
                    # b through r is a long run: extend it as far as it goes.
                    p = q = r
                    while True:
                        p += 2
                        if not p < t:
                            break
                        if ((yield from cmp(list1[p - 1], list1[p])) > 0) != sense:
                            break
                        q = p
                    r = p = q + 2
            if q > b:                   # a run of more than 2 at b
                savep = p
                q += 2
                p = q
                # pick up a singleton, if possible
                if p == t and t + 1 == last and ((yield from cmp(list1[p - 1], list1[p])) > 0) == sense:
                    savep = r = p = q = last
                list2[p2] = p2 + (p - b)
                p2 = list2[p2]
                runs += 1
                if sense:
                    while True:
                        p -= 1
                        if not b < p:
                            break
                        list1[b], list1[p] = list1[p], list1[b]
                        b += 1
                p = savep
            while q < p:                # simple pairs
                list2[p2] = p2 + 2
                p2 = list2[p2]
                runs += 1
                if sense:
                    list1[q], list1[q + 1] = list1[q + 1], list1[q]
                q += 2
            b = p
            if b == t and t + 1 == last:
                list2[p2] = p2 + 1
                runs += 1
                b += 1
            q = r
            if not b < t:
                break
        sense = not sense
    return runs

def merge(nmemb):
    """The order of nmemb things, by what is sent for each pair yielded."""
    def cmp(x, y):
        return (yield (x, y))
    base = list(range(nmemb))
    if nmemb <= 1:
        return base
    aux = [None] * nmemb
    level = 0
    stack = [[0, 0] for _ in range(60)]         # [offset, runs]
    sp = 0
    stack[sp][1] = yield from dynprep(base, aux, nmemb, cmp)
    stack[sp][0] = offset = 0
    which = [base, aux, base]
    while True:
        runs = stack[sp][1]
        if runs == 0:
            # Both runs of this level are made: merge them, and go up.
            iwhich = level & 1
            list1 = which[iwhich]               # where the runs are now
            list2 = which[iwhich + 1]           # where the merged run goes
            while True:
                offset = stack[sp][0]
                f1 = p1 = offset                # the first run
                tp2 = offset                    # where the merged run goes
                t = list2[offset]               # where the first run ends
                f2 = l1 = t
                t = list2[t]                    # where the second ends
                l2 = t
                offset = t
                while f1 < l1 and f2 < l2:
                    # q is the head that goes second: all of the other run
                    # that is strictly lower goes before it. Equal counts
                    # as high when q is from the second run, and as low
                    # when it is from the first, which keeps the sort
                    # stable.
                    if (yield from cmp(list1[f1], list1[f2])) <= 0:
                        q, b, t, sense = f2, f1, l1, -1
                    else:
                        q, b, t, sense = f1, f2, l2, 0
                    # ramp up: t at something strictly above q (or the
                    # end), b at something strictly below it
                    i = 1
                    run = 0
                    while True:
                        p = b + i
                        if p >= t:
                            p = t - 1
                            if p > b and (yield from cmp(list1[q], list1[p])) <= sense:
                                t = p
                            else:
                                b = p
                            break
                        elif (yield from cmp(list1[q], list1[p])) <= sense:
                            t = p
                            break
                        else:
                            b = p
                        run += 1
                        if run >= RTHRESH:
                            i += i
                    # q follows b and goes before t: a binary search of
                    # what is between, rounding down
                    b += 1
                    while b < t:
                        p = b + (t - b - 1) // 2
                        if (yield from cmp(list1[q], list1[p])) <= sense:
                            t = p
                        else:
                            b = p + 1
                    # copy all the strictly low ones, then q
                    if q == f1:
                        while True:
                            list2[tp2] = list1[f2]
                            tp2 += 1
                            f2 += 1
                            if not f2 < t:
                                break
                        list2[tp2] = list1[f1]
                        tp2 += 1
                        f1 += 1
                    else:
                        while True:
                            list2[tp2] = list1[f1]
                            tp2 += 1
                            f1 += 1
                            if not f1 < t:
                                break
                        list2[tp2] = list1[f2]
                        tp2 += 1
                        f2 += 1
                # run out the list that is left
                if f1 == l1:
                    while f2 < l2:
                        list2[tp2] = list1[f2]
                        tp2 += 1
                        f2 += 1
                else:
                    while True:
                        list2[tp2] = list1[f1]
                        tp2 += 1
                        f1 += 1
                        if not f1 < l1:
                            break
                list1[p1] = tp2
                level -= 1
                if level == 0:
                    return base
                sp -= 1
                list1, list2 = list2, list1
                runs = stack[sp][1]
                if runs != 0:
                    break
        stack[sp][1] = 0                # this run will finish the level
        # More than 2 runs: make them 2, each of about half, the second
        # half stacked for later.
        while runs > 2:
            level += 1
            sp += 1
            stack[sp][0] = offset
            stack[sp][1] = runs // 2
            runs -= runs // 2
        iwhich = level & 1
        if runs == 1:
            # One run from one run: copied to where it belongs, if it is
            # not there.
            if iwhich:
                f1 = b = offset
                f2 = offset
                t = aux[f2]
                offset = t
                while True:
                    aux[f2] = base[f1]
                    f2 += 1
                    f1 += 1
                    if not f1 < t:
                        break
                base[b] = t
            elif level == 0:
                return base
        else:
            # One run from two: the merge above does it, from the other
            # array.
            level += 1
            sp += 1
            stack[sp][0] = offset
            stack[sp][1] = 0
            if not iwhich:
                f1 = b = offset
                f2 = offset
                t = aux[f2]
                offset = t
                p = offset
                t = aux[t]
                while True:
                    aux[f2] = base[f1]
                    f2 += 1
                    f1 += 1
                    if not f1 < t:
                        break
                base[b] = p
                base[p] = t

def sort(values, compare):
    """The values sorted, and the pairs that were compared, in order."""
    asked = []
    g = merge(len(values))
    try:
        pair = next(g)
        while True:
            asked.append((values[pair[0]], values[pair[1]]))
            pair = g.send(compare(values[pair[0]], values[pair[1]]))
    except StopIteration as done:
        return [values[i] for i in done.value], asked

# ---- held to perl

def lists(seed):
    r = random.Random(seed)
    out = [[], [5], [2, 1], [1, 2], [1, 1]]
    for n in list(range(3, 40)) + [47, 48, 49, 63, 64, 65, 100, 128, 200, 300]:
        out.append([r.randrange(1000) for _ in range(n)])
        out.append(sorted(r.randrange(1000) for _ in range(n)))
        out.append(sorted((r.randrange(1000) for _ in range(n)), reverse=True))
        out.append([r.randrange(4) for _ in range(n)])
        out.append([7] * n)
    for _ in range(1500):
        n = r.randrange(2, 120)
        kind = r.randrange(6)
        if kind == 0:
            v = [r.randrange(1000) for _ in range(n)]
        elif kind == 1:
            v = [r.randrange(3) for _ in range(n)]
        else:
            # runs each way, of every length, so that the long-run pass and
            # the doubling in the merge are both met
            v = []
            while len(v) < n:
                k = r.randrange(1, 40)
                start = r.randrange(1000)
                step = r.choice([1, -1, 0, 3, -3]) if kind != 5 else r.choice([1, -1])
                v += [start + step * j for j in range(k)]
            v = v[:n]
        out.append(v)
    return out

PERL = r'''
use v5.42;
while (my $line = <STDIN>) {
    chomp $line;
    my ($how, @v) = split / /, $line;
    my @log;
    my @s;
    if ($how eq 'n') { @s = sort { push @log, "$a,$b"; $a <=> $b } @v; }
    elsif ($how eq 'r') { @s = sort { push @log, "$a,$b"; $b <=> $a } @v; }
    elsif ($how eq 'm') { @s = sort { push @log, "$a,$b"; ($a * 7 + $b * 13) % 3 - 1 } @v; }
    elsif ($how eq 'k') { @s = sort { push @log, "$a,$b"; ($a % 10) <=> ($b % 10) } @v; }
    say join(" ", @s), "|", join(" ", @log);
}
'''

HOW = {
    'n': lambda a, b: (a > b) - (a < b),
    'r': lambda a, b: (b > a) - (b < a),
    # no order at all: an answer that is a table of the two values
    'm': lambda a, b: (a * 7 + b * 13) % 3 - 1,
    # many equal keys among different values: what stable means
    'k': lambda a, b: (a % 10 > b % 10) - (a % 10 < b % 10),
}

def check(merge_=None):
    """How many lists differ from perl, of how many."""
    global merge
    kept = merge
    if merge_ is not None:
        merge = merge_
    try:
        cases = [(how, v) for seed in (1, 2) for v in lists(seed) for how in 'nrmk'][:4200]
        text = ''.join(how + ''.join(f' {x}' for x in v) + '\n' for how, v in cases)
        out = subprocess.run([os.environ.get('CURLY_PERL', 'perl'), '-e', PERL], input=text, capture_output=True, text=True, check=True).stdout.split('\n')
        bad = 0
        for (how, v), line in zip(cases, out):
            try:
                got, asked = sort(v, HOW[how])
                mine = ' '.join(map(str, got)) + '|' + ' '.join(f'{a},{b}' for a, b in asked)
            except Exception as e:
                mine = f'({type(e).__name__})'
            if mine != line:
                bad += 1
                if bad == 1 and merge_ is None:
                    print('differs:', how, v, '\n  perl:', line[:300], '\n  here:', mine[:300])
        return bad, len(cases)
    finally:
        merge = kept

def broken(old, new):
    """This file's merge with one piece of its text changed."""
    text = open(__file__).read()
    start = text.index('PTHRESH = 8')
    end = text.index('def sort(values, compare)')
    body = text[start:end]
    assert body.count(old) == 1, (old, body.count(old))
    scope = {}
    exec(body.replace(old, new), scope)
    return scope['merge']

BREAKAGES = [
    ('a run is looked for after 7 pairs', 'PTHRESH = 8 ', 'PTHRESH = 7 '),
    ('a merge doubles its step after 5', 'RTHRESH = 6 ', 'RTHRESH = 5 '),
    ('equal is low from either run', 'q, b, t, sense = f2, f1, l1, -1', 'q, b, t, sense = f2, f1, l1, 0'),
    ('the search rounds up', 'p = b + (t - b - 1) // 2', 'p = b + (t - b) // 2'),
    ('a run that goes down is not turned round', '                        list1[b], list1[p] = list1[p], list1[b]\n', ''),
    ('the halves are split the other way', '            stack[sp][1] = runs // 2\n            runs -= runs // 2', '            stack[sp][1] = runs - runs // 2\n            runs = runs // 2'),
    ('the singleton at the end is not picked up', 'if p == t and t + 1 == last and', 'if False and'),
    ('the first sense is taken from equal', 'sense = (yield from cmp(list1[b], list1[b + 1])) > 0', 'sense = (yield from cmp(list1[b], list1[b + 1])) >= 0'),
]

def main(argv):
    if argv == ['--cases']:
        # The lists the check sorts, for the runtime's own test of its
        # machine (runtime/tests/sortm.c): one a line.
        cases = [(how, v) for seed in (1, 2) for v in lists(seed) for how in 'nrmk'][:4200]
        sys.stdout.write(''.join(how + ''.join(f' {x}' for x in v) + '\n' for how, v in cases))
        return
    if argv == ['--self']:
        for name, old, new in BREAKAGES:
            bad, n = check(broken(old, new))
            print(f'{name}: {bad} of {n} lists differ' + ('' if bad else '   <-- NOT CAUGHT'))
        return
    bad, n = check()
    print(f'{n} lists sorted as perl 5.42 sorts them, pair for pair: {bad} differ')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main(sys.argv[1:])
