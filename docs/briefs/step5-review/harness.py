#!/usr/bin/env python3
"""Run programs under the model and under perl 5.42, and hold them to the rule:
no fault -> same bytes, exit 0, nothing on stderr; fault -> the model's output
is a prefix of perl's. One perl at a time."""
import os, subprocess, sys
import model

import tempfile
PERL = os.environ.get('CURLY_PERL', 'perl')
HERE = os.path.join(tempfile.gettempdir(), 'curly-step5-review-%d' % os.getuid())      # programs and logs go here, not in the tree
os.makedirs(os.path.join(HERE, 't'), exist_ok=True)
ENV = dict(os.environ, PERL_HASH_SEED='1')


def perl(src, name=None, check=False):
    if name is None: name = 't/g%d.pl' % os.getpid()      # one file per process: two runs must not share it
    path = os.path.join(HERE, name)
    with open(path, 'w') as f: f.write(src)
    args = [PERL] + (['-c'] if check else []) + [name]
    r = subprocess.run(args, capture_output=True, env=ENV, stdin=subprocess.DEVNULL, cwd=HERE, timeout=30)
    return r.stdout, r.stderr, r.returncode


def verdict(prog, src=None):
    """None if the program keeps the rule, or a string that says how it doesn't."""
    if src is None: src = model.source(prog)
    out, fault = model.run(prog)
    pout, perr, pexit = perl(src)
    if fault is None:
        if pout != out: return 'DIFFERS: model %r perl %r (perl stderr %r)' % (out, pout, perr)
        if perr or pexit: return 'PERL COMPLAINS: exit %d stderr %r (stdout same)' % (pexit, perr)
        return None
    if not pout.startswith(out): return 'NOT A PREFIX: model %r then fault (%s); perl %r stderr %r' % (out, fault, pout, perr)
    if b'syntax error' in perr or b'compilation errors' in perr or b'masks' in perr or b'Found =' in perr or b'Useless' in perr:
        return 'PERL COMPILE COMPLAINT on a faulting program: %r' % perr
    return None


class Tally:
    def __init__(self, label, logname):
        self.label = label; self.n = 0; self.faults = 0; self.bad = 0
        self.log = open(os.path.join(HERE, logname), 'w')

    def check(self, prog, src=None):
        if src is None: src = model.source(prog)
        self.n += 1
        out, fault = model.run(prog)
        if fault is not None: self.faults += 1
        v = verdict(prog, src)
        if v is not None:
            self.bad += 1
            self.log.write('----\n' + src + '## ' + v + '\n'); self.log.flush()
            if self.bad <= 12: print('----\n' + src + '## ' + v, flush=True)
        return v

    def done(self):
        print('%s: %d programs, %d fault in the model, %d break the rule' % (self.label, self.n, self.faults, self.bad), flush=True)
