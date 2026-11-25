#!/usr/bin/env python3
"""The compiler held to the reviewer's model of step 4, and to perl.

    python3 docs/briefs/step4-review/compiler.py SEED COUNT [nl] [tight] [heavy]

model4.py, h4.py and gen4.py are the reviewer's own, as it left them
(docs/PLAN.md, step 4): a model of the step's definition on the step 3
reviewer's (../step3-review/model.py), with the amendments its review
asked for as switches, on here; and its generator of random statements
over the whole grammar, which this script draws from. What is done with
each statement is step 3's script's: see ../step3-review/compiler.py.
Not part of make test.
"""
import os, random, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
sys.path[:0] = [HERE, os.path.join(HERE, '..', 'step3-review')]
sys.set_int_max_str_digits(0)
import model, model4
for k in model.OPT:
    if k.startswith('amend_'):
        model.OPT[k] = True
import gen4                 # reads the seed and the count from the command line
model4.OPT4['args'] = 11
model4.OPT4['amend_not_cmp'] = True

PERL = os.environ.get('CURLY_PERL', 'perl')
HO = "use v5.42;\nuse open ':std', ':encoding(UTF-8)';\n"
seed, count = gen4.seed, gen4.count
R = gen4.R
pending_statements = gen4.gen(count)

def statement():
    return pending_statements.pop()

def verdict(stmt):
    """What the reviewer's model makes of one statement alone."""
    try:
        prog = model4.parse(HO + stmt + '\n')
        out, fault = model4.run(prog)
    except model4.Refuse:
        return 'refuses'
    except model4.Big:
        return 'faults'
    return 'faults' if fault is not None else 'prints'

work = tempfile.mkdtemp(prefix='step4-review-')

def both(stmts):
    """(what the compiler did, its stdout, perl's stdout, perl's stderr,
    the line of a refusal or a fault) for a program of these statements."""
    path = os.path.join(work, 'p.pl')
    open(path, 'w').write(HO + ''.join(s + '\n' for s in stmts))
    c = subprocess.run(['node', os.path.join(ROOT, 'bin', 'curlyc.ts'), '-o', os.path.join(work, 'p'), path], capture_output=True, text=True)
    if c.returncode == 1:
        return 'refused', b'', b'', b'', int(c.stderr.split(':')[1])
    assert c.returncode == 0, c.stderr
    r = subprocess.run([os.path.join(work, 'p')], capture_output=True, stdin=subprocess.DEVNULL)
    p = subprocess.run([PERL, path], capture_output=True, stdin=subprocess.DEVNULL)
    if r.returncode == 0:
        return 'ran', r.stdout, p.stdout, p.stderr, 0
    assert r.returncode == 1, r
    return 'faulted', r.stdout, p.stdout, p.stderr, int(r.stderr.split(b' line ')[-1].rstrip(b'.\n'))

def line_of(stmts, line):
    """Which statement a line of the program is in."""
    at = 3
    for n, s in enumerate(stmts):
        at += s.count('\n') + 1
        if line < at:
            return n
    return len(stmts) - 1

counts = {'the model prints': 0, 'and the compiler agrees with perl': 0, 'which the compiler refuses': 0,
          'which the compiler faults on': 0, 'the model faults (sampled)': 0, 'the model refuses (sampled)': 0, 'WRONG': 0}
wrong = []
stricter = []       # what the compiler refuses or faults on, and the model prints
by = {'prints': [], 'faults': [], 'refuses': []}
for _ in range(count):
    s = statement()
    by[verdict(s)].append(s)
print(f"seed {seed}: {count} statements; the reviewer's model prints for {len(by['prints'])}, faults on {len(by['faults'])}, refuses {len(by['refuses'])}", flush=True)

pending = by['prints']
counts['the model prints'] = len(pending)
while pending:
    batch, pending = pending[:300], pending[300:]
    while batch:
        what, out, perl_out, perl_err, line = both(batch)
        if what == 'ran':
            if out == perl_out and not perl_err:
                counts['and the compiler agrees with perl'] += len(batch)
            elif len(batch) == 1:
                counts['WRONG'] += 1
                wrong.append((batch[0], out, perl_out, perl_err))
            else:
                # Somewhere in here: one at a time.
                pending = [[s] for s in batch] and pending
                for s in batch:
                    w, o, po, pe, _ = both([s])
                    if w == 'ran' and (o != po or pe):
                        counts['WRONG'] += 1
                        wrong.append((s, o, po, pe))
                    elif w == 'ran':
                        counts['and the compiler agrees with perl'] += 1
                    else:
                        counts['which the compiler refuses' if w == 'refused' else 'which the compiler faults on'] += 1
            break
        n = line_of(batch, line)
        counts['which the compiler refuses' if what == 'refused' else 'which the compiler faults on'] += 1
        stricter.append((what, batch[n]))
        if what == 'faulted' and not perl_out.startswith(out):
            counts['WRONG'] += 1
            wrong.append((batch[n], out, perl_out, perl_err))
        del batch[n]

for kind, name in (('faults', 'the model faults (sampled)'), ('refuses', 'the model refuses (sampled)')):
    for s in R.sample(by[kind], min(150, len(by[kind]))):
        counts[name] += 1
        what, out, perl_out, perl_err, _ = both([s])
        if what == 'ran' and (out != perl_out or perl_err):
            counts['WRONG'] += 1
            wrong.append((s, out, perl_out, perl_err))
        elif what == 'faulted' and not perl_out.startswith(out):
            counts['WRONG'] += 1
            wrong.append((s, out, perl_out, perl_err))

for k, v in counts.items():
    print(f'{v:8}  {k}')
for what, s in stricter[:12]:
    print(f'{what}: {s!r}')
for s, out, perl_out, perl_err in wrong[:20]:
    print(f'WRONG: {s!r}\n   the compiler: {out[:120]!r}\n   perl: {perl_out[:120]!r} {perl_err[:200]!r}')
sys.exit(1 if wrong else 0)
