#!/usr/bin/env python3
"""The step-3 reviewer's harness, pointed at the step-4 model, three perls at once."""
import harness, model4, collections, re
from harness import perl_run, show, H, HO, HU, _split
harness.model = model4


def check_file(src):
    return harness.check_file(src)


def check_statements(header, stmts, batch=1500, jobs=2, quiet=False):
    keep = []
    skipped = 0
    for s in stmts:
        try:
            prog = model4.parse(header + s + '\n')
            model4.safe(prog)
        except model4.Refuse:
            pass
        except model4.Big:
            skipped += 1
            continue
        keep.append(s)
    if skipped and not quiet:
        print('  %8d  skipped: a constant too long for a mass run' % skipped)
    return harness.check_statements(header, keep, batch=batch, jobs=jobs, quiet=quiet)
