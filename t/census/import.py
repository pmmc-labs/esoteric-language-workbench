#!/usr/bin/env python3
"""Import the census's probes into t/census/ (step 11b; D11, D96).

    python3 t/census/import.py PERL5-SON CHALK PVM

Each argument is a checkout of that repository. Run once, and again when
a source moves: it writes what is not there and changes nothing that is,
so a probe that `census.py --sort` has moved to by-design/ stays there.

What is imported: perl5-son's t/corpus/probes and the probes of its audit
of 2026-11-19, Chalk's t/data/audit-probes, and the programs of pvm's
conformance/mdtest (one a case, its ```perl block). `use v5.42;` is put in
front of a program that lacks it: the language has no other first line.
Two programs that are then the same text are one probe, named for the
first place it was found, in the order above; t/census/SOURCES.tsv lists
every place.

A probe goes to run/, or to not-perl/ when perl 5.42 itself stops at it
with that line in front: it does not compile, or it dies. Those are kept
and never run.
"""
import hashlib
import os
import re
import subprocess
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
PERL = os.environ.get('CURLY_PERL', 'perl')
USE = 'use v5.42;\n'

def found(son, chalk, pvm):
    """(name, origin, text) for every program, in the order names are given."""
    def tree(set_, repo, root, origin):
        for d, dirs, files in os.walk(os.path.join(repo, root)):
            dirs.sort()
            for f in sorted(files):
                if f.endswith('.pl'):
                    rel = os.path.relpath(os.path.join(d, f), os.path.join(repo, root))
                    text = open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
                    yield f'{set_}/{rel}', f'{origin}:{root}/{rel}', text
    yield from tree('son-corpus', son, 't/corpus/probes', 'perl5-son')
    yield from tree('son-audit', son, 'docs/research/son-ir-audit-2026-11-19/probes', 'perl5-son')
    yield from tree('chalk', chalk, 't/data/audit-probes', 'chalk')
    md = os.path.join(pvm, 'conformance/mdtest')
    for f in sorted(os.listdir(md)):
        if not f.endswith('.md') or f == 'FORMAT.md':
            continue
        blocks = re.findall(r'^```perl\n(.*?)^```', open(os.path.join(md, f), encoding='utf-8').read(), re.S | re.M)
        for k, text in enumerate(blocks, 1):
            yield f'pvm/{f[:-3]}-{k:02d}.pl', f'pvm:conformance/mdtest/{f}#{k}', text

def stops(text):
    """Whether perl itself stops at the program: it does not compile, or dies."""
    try:
        r = subprocess.run([PERL, '-e', text], capture_output=True, timeout=10, stdin=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        return False
    return r.returncode != 0

def main(argv):
    son, chalk, pvm = argv
    revisions = {name: subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
                 for name, repo in (('perl5-son', son), ('chalk', chalk), ('pvm', pvm))}
    probes, places = {}, {}
    for name, origin, text in found(son, chalk, pvm):
        if not re.search(r'^use v5\.42;', text, re.M):
            text = USE + text
        key = hashlib.sha1(text.encode()).hexdigest()
        if key not in probes:
            probes[key] = (name, text)
        places.setdefault(key, []).append(origin)
    with Pool() as pool:
        stopped = pool.map(stops, [text for _, text in probes.values()], chunksize=50)
    wrote = 0
    for (name, text), stop in zip(probes.values(), stopped):
        if any(os.path.exists(os.path.join(HERE, d, name)) for d in ('run', 'by-design', 'not-perl')):
            continue
        path = os.path.join(HERE, 'not-perl' if stop else 'run', name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(text)
        wrote += 1
    with open(os.path.join(HERE, 'SOURCES.tsv'), 'w', encoding='utf-8') as f:
        f.write('# Where each probe came from (t/census/import.py writes this file).\n')
        f.write('# perl5-son and Chalk: no licence file; used by perigrin\'s agreement (D11).\n')
        f.write('# pvm: Artistic License 2.0, copyright 2025 Chris Prather.\n')
        for name, rev in revisions.items():
            f.write(f'# {name} at {rev}\n')
        f.write('# probe\tplaces\n')
        for key, (name, _) in sorted(probes.items(), key=lambda kv: kv[1][0]):
            f.write(name + '\t' + ' '.join(places[key]) + '\n')
    print(f'{len(probes)} probes from {sum(len(p) for p in places.values())} programs; {sum(stopped)} that perl stops at; {wrote} files written')

if __name__ == '__main__':
    main(sys.argv[1:])
