#!/usr/bin/env python3
"""The checker for rules (1)-(3), bytes against bytes, and a batch runner.

check_file(src bytes) -> list of failures for one whole program.
check_statements(header, [statement text...]) -> statistics and the single
statements that break a rule, found by splitting failing batches.
"""
import os, re, subprocess, sys, tempfile, itertools, collections
from concurrent.futures import ThreadPoolExecutor
import model

sys.set_int_max_str_digits(0)
PERL = '/opt/perl-5.42/bin/perl'
HERE = os.path.dirname(os.path.abspath(__file__))
ENV = dict(os.environ, PERL_HASH_SEED='1')
_counter = itertools.count()


def perl_run(src, check_only=False):
    """run perl plain on src (bytes) as t/NAME.pl from HERE"""
    name = 't/w%d_%d.pl' % (os.getpid(), next(_counter))
    path = os.path.join(HERE, name)
    with open(path, 'wb') as f:
        f.write(src)
    try:
        args = [PERL, '-c', name] if check_only else [PERL, name]
        p = subprocess.run(args, cwd=HERE, env=ENV, stdin=subprocess.DEVNULL,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
        return p.stdout, p.stderr.replace(name.encode(), b'FILE'), p.returncode
    finally:
        os.unlink(path)


def check_file(src):
    """-> (status, failures). status: 'refused', 'ok', 'fault'.  failures is a
    list of strings, empty when rules (1) to (3) hold."""
    if isinstance(src, str):
        src = src.encode('utf-8')
    try:
        prog = model.parse(src)
    except model.Refuse as r:
        return 'refused: ' + str(r), []
    fails = []
    out, err, code = perl_run(src, check_only=True)
    if code != 0 or err != b'FILE syntax OK\n' or out != b'':
        fails.append('rule 1: perl -c exit %d stderr %r' % (code, err[:300]))
    mout, fault = model.run(prog)
    out, err, code = perl_run(src)
    if fault is None:
        if out != mout:
            fails.append('rule 2: stdout differs: model %r perl %r' % (mout[:200], out[:200]))
        if code != 0:
            fails.append('rule 2: perl exit %d' % code)
        if err != b'':
            fails.append('rule 2: perl stderr %r' % err[:300])
        return 'ok', fails
    if not out.startswith(mout):
        fails.append('rule 3: model printed %r before its fault, perl printed %r' % (mout[:200], out[:200]))
    return 'fault (%s)' % fault[1], fails


def _batch_ok(header, stmts, expected):
    src = (header + ''.join(s + '\n' for s in stmts)).encode('utf-8')
    out, err, code = perl_run(src)
    return out == expected and err == b'' and code == 0


def _c_ok(header, stmts):
    src = (header + ''.join(s + '\n' for s in stmts)).encode('utf-8')
    out, err, code = perl_run(src, check_only=True)
    return code == 0 and err == b'FILE syntax OK\n' and out == b''


def _split(ok, items):
    """the single items for which ok([item]) is false, given ok(items) is false"""
    if len(items) == 1:
        return items
    mid = len(items) // 2
    bad = []
    for part in (items[:mid], items[mid:]):
        if not ok(part):
            bad += _split(ok, part)
    return bad


def check_statements(header, stmts, batch=1500, jobs=4, quiet=False):
    """Each statement must be a complete statement the model accepts alone
    after header.  Statements the model runs without a fault are batched and
    their output compared to perl's; statements that fault are batched and
    given to perl -c (rule 1), and rule 3 holds trivially for them alone.
    -> (Counter of classes, list of (statement, failure description))."""
    stats = collections.Counter()
    good, faulty = [], []
    for s in stmts:
        try:
            prog = model.parse(header + s + '\n')
        except model.Refuse as r:
            stats['refused'] += 1
            continue
        tr = []
        try:
            mout, fault = model.run(prog, tr)
        except model.Big:
            stats['skipped: a string over %d characters' % model.BIG] += 1
            continue
        if fault is None:
            stats['ok ' + '+'.join(sorted(set(tr)))] += 1
            good.append((s, mout))
        else:
            stats[tr[-1]] += 1
            faulty.append(s)
    fails = []

    hl = header.count('\n')

    def culprits(items, text_of, expected_of, check_only):
        """the items that break the batch: by the line numbers in perl's
        stderr and the first place stdout leaves the expected bytes, removed
        and rerun until the rest is clean; by halving when that finds nothing"""
        res = []
        items = list(items)
        oneline = all('\n' not in text_of(x) for x in items)
        while items:
            src = (header + ''.join(text_of(x) + '\n' for x in items)).encode('utf-8')
            out, err, code = perl_run(src, check_only)
            exp = b'' if check_only else b''.join(expected_of(x) for x in items)
            experr = b'FILE syntax OK\n' if check_only else b''
            if out == exp and err == experr and code == 0:
                break
            bad = set()
            if oneline:
                for m in re.finditer(rb'FILE line (\d+)', err):
                    i = int(m.group(1)) - hl - 1
                    if 0 <= i < len(items):
                        bad.add(i)
                if not check_only:
                    pos = 0
                    for i, x in enumerate(items):
                        m = expected_of(x)
                        if out.startswith(m, pos):
                            pos += len(m)
                        else:
                            bad.add(i)
                            break
            if not bad:
                def ok(part):
                    src = (header + ''.join(text_of(x) + '\n' for x in part)).encode('utf-8')
                    o, e, c = perl_run(src, check_only)
                    return o == (b'' if check_only else b''.join(expected_of(x) for x in part)) and e == experr and c == 0
                got = _split(ok, items)
                res += got
                break
            res += [items[i] for i in sorted(bad)]
            items = [x for i, x in enumerate(items) if i not in bad]
        return res

    def do_good(chunk):
        res = []
        for s, m in culprits(chunk, lambda x: x[0], lambda x: x[1], False):
            out, err, code = perl_run((header + s + '\n').encode('utf-8'))
            alone = '' if (out != m or err or code) else ' (ONLY IN A BATCH)'
            res.append((s, 'rule 2%s: model %r perl %r stderr %r exit %d' % (alone, m[:120], out[:120], err[:200], code)))
        for s, m in culprits(chunk, lambda x: x[0], lambda x: x[1], True):
            out, err, code = perl_run((header + s + '\n').encode('utf-8'), True)
            res.append((s, 'rule 1: perl -c stderr %r exit %d' % (err[:200], code)))
        return res

    def do_faulty(chunk):
        res = []
        for s in culprits(chunk, lambda x: x, None, True):
            out, err, code = perl_run((header + s + '\n').encode('utf-8'), True)
            res.append((s, 'rule 1 (a statement that faults): perl -c stderr %r exit %d' % (err[:200], code)))
        return res

    with ThreadPoolExecutor(jobs) as ex:
        futs = [ex.submit(do_good, good[i:i + batch]) for i in range(0, len(good), batch)]
        futs += [ex.submit(do_faulty, faulty[i:i + batch]) for i in range(0, len(faulty), batch)]
        for f in futs:
            fails += f.result()
    if not quiet:
        for k in sorted(stats):
            print('  %8d  %s' % (stats[k], k))
        print('  %8d  FAILURES' % len(fails))
    return stats, fails


def show(fails, per=3):
    """failures grouped by what perl said, a few examples of each"""
    groups = collections.OrderedDict()
    for s, why in fails:
        m = re.search(r"stderr b(['\"])(.*?)\1 exit (\d+)", why)
        sig = m.group(2) if m else why
        sig = re.sub(r'\(.*?\) in chr', '(N) in chr', sig)
        sig = re.sub(r'Argument \\?".*?\\?" isn', 'Argument "S" isn', sig)
        sig = re.sub(r'line \d+', 'line N', sig)
        sig = re.sub(r'Use of \\?".*?\\?" without', 'Use of "W" without', sig)
        mm = re.search(r"model (b(['\"]).*?\2) perl (b(['\"]).*?\4) stderr", why)
        differs = bool(mm) and mm.group(1) != mm.group(3)
        key = (why.split(':')[0], sig, 'STDOUT DIFFERS' if differs else 'stdout same', m.group(3) if m else '')
        groups.setdefault(key, []).append((s, why))
    for key, items in groups.items():
        print('  [%d] %s | %s | %s | exit %s' % (len(items), key[0], key[1][:150], key[2], key[3]))
        for s, why in items[:per]:
            mm = re.search(r"model (b(['\"]).*?\2) perl (b(['\"]).*?\4) stderr", why)
            print('        %s   %s' % (s, ('model %s perl %s' % (mm.group(1), mm.group(3))) if mm else ''))


H = 'use v5.42;\n'
HO = "use v5.42;\nuse open ':std', ':encoding(UTF-8)';\n"
HU = "use v5.42;\nuse utf8;\nuse open ':std', ':encoding(UTF-8)';\n"

if __name__ == '__main__':
    # check one file given on the command line
    for p in sys.argv[1:]:
        src = open(p, 'rb').read()
        print(p, check_file(src))
