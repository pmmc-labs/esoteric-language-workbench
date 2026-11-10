#!/usr/bin/env python3
"""The mechanical checks: what the working rules say, enforced rather
than remembered. `make checks` runs them all; `make models` regenerates
what the models write.

  models    Every command in a model's docstring (a line that starts
            `python3 t/models/`, with `> file`) is run, and its output
            must equal the file. A file that was patched by hand, or a
            model that was changed without rerunning it, fails here.
            `--write` writes the files instead (make models).
  tests     Every t/*.smol, examples/*.smol and docs/guide/code/*.smol
            has a .expected and the other way round; a test that names a
            model (`t/models/x.py` in its comments) names one that
            exists and that lists the test's files.
  referee   Every referee in t/referee/ (an evaluator of the language
            written from the decisions, not the runtime) is run over
            every golden test, and must print the .expected, or say the
            program is outside what it covers (exit 3), which is skipped.
  commits   Every commit in a range (BASE..HEAD, default origin/main..HEAD)
            that touches compiler/, lib/ or bin/ names a decision
            (D12) or a plan step (step 3) in its subject, so that the
            change can be found from the log and the log from the
            change. `commit-msg FILE [--staged]` checks one message, for
            the git hook that `make hooks` installs.
"""

import glob
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
IMPL = ('compiler/', 'lib/', 'bin/')
TEST_DIRS = ['t', 'examples', 'docs/guide/code']
EXT = '.smol'

def model_commands():
    """(model, args, path) for every regenerating command in every model."""
    out = []
    for model in sorted(glob.glob('t/models/*.py')):
        src = open(model).read()
        for line in src.splitlines():
            m = re.match(r'\s*python3 (t/models/\S+\.py)((?: \S+)*) > (\S+)$', line)
            if m:
                if m.group(1) != model:
                    out.append((model, None, f'{model} lists a command for {m.group(1)}'))
                else:
                    out.append((model, m.group(2).split(), m.group(3)))
    return out

def check_models(write=False):
    bad = []
    commands = model_commands()
    for model, args, path in commands:
        if args is None:
            bad.append(path)
            continue
        r = subprocess.run(['python3', '-I', model, *args], capture_output=True)
        if r.returncode != 0:
            bad.append(f'{model} {" ".join(args)}: exit {r.returncode}\n{r.stderr.decode()}')
            continue
        if write:
            open(path, 'wb').write(r.stdout)
        elif not os.path.exists(path):
            bad.append(f'{path}: not written; `make models`')
        elif open(path, 'rb').read() != r.stdout:
            bad.append(f'{path}: differs from what {model} writes; rerun it (`make models`), don\'t patch the file')
    models_without = [m for m in sorted(glob.glob('t/models/*.py')) if not any(c[0] == m for c in commands)]
    bad += [f'{m}: lists no command that writes a file' for m in models_without]
    print(f'models: {len(commands)} files from {len(set(c[0] for c in commands))} models' + (' written' if write else ''))
    return bad

def check_tests():
    bad = []
    listed = {path for _, _, path in model_commands() if path}
    for d in TEST_DIRS:
        for src in sorted(glob.glob(f'{d}/*{EXT}')):
            base = src[:-len(EXT)]
            if not os.path.exists(base + '.expected'):
                bad.append(f'{src}: no .expected')
            text = open(src).read()
            for model in set(re.findall(r't/models/\S+\.py', text)):
                if not os.path.exists(model):
                    bad.append(f'{src}: names {model}, which doesn\'t exist')
                elif src not in listed:
                    bad.append(f'{src}: names {model}, which doesn\'t list it')
        for exp in sorted(glob.glob(f'{d}/*.expected')):
            if not os.path.exists(exp[:-len('.expected')] + EXT):
                bad.append(f'{exp}: no {EXT} file')
    return bad

def check_referee():
    bad, ran, skipped = [], 0, 0
    referees = sorted(glob.glob('t/referee/*.py'))
    for ref in referees:
        for d in TEST_DIRS:
            for src in sorted(glob.glob(f'{d}/*{EXT}')):
                exp = src[:-len(EXT)] + '.expected'
                if not os.path.exists(exp):
                    continue
                r = subprocess.run(['python3', '-I', ref, src], capture_output=True)
                if r.returncode == 3:
                    skipped += 1
                elif r.returncode != 0:
                    bad.append(f'{ref} on {src}: exit {r.returncode}\n{r.stderr.decode()}')
                elif r.stdout != open(exp, 'rb').read():
                    bad.append(f'{ref} on {src}: the referee and the .expected disagree; one of them is wrong, and the decisions say which')
                else:
                    ran += 1
    print(f'referee: {len(referees)} referees, {ran} tests agree, {skipped} outside them')
    return bad

SUBJECT_OK = re.compile(r'\bD\d+\b|\bstep \d+\b', re.I)

def touches_impl(files):
    return any(f.startswith(IMPL) for f in files)

def check_message(subject, files, what):
    if touches_impl(files) and not SUBJECT_OK.search(subject):
        return [f'{what}: changes {", ".join(sorted({f.split("/")[0] for f in files if f.startswith(IMPL)}))}/ '
                f'but its subject names no decision (D12) or plan step (step 3): "{subject}"']
    return []

def check_commits(rng):
    bad = []
    log = subprocess.run(['git', 'log', '--format=%H%x00%s', rng], capture_output=True, text=True, check=True).stdout
    for line in log.splitlines():
        sha, subject = line.split('\0')
        files = subprocess.run(['git', 'show', '--format=', '--name-only', sha], capture_output=True, text=True, check=True).stdout.split()
        bad += check_message(subject, files, sha[:10])
    print(f'commits: {len(log.splitlines())} in {rng}')
    return bad

def check_commit_msg(path, staged):
    subject = next((l for l in open(path).read().splitlines() if l and not l.startswith('#')), '')
    files = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, check=True).stdout.split() if staged else []
    return check_message(subject, files, 'this commit')

def main(argv):
    os.chdir(ROOT)
    what = argv[0] if argv else 'all'
    if what == 'models':
        bad = check_models('--write' in argv)
    elif what == 'tests':
        bad = check_tests()
    elif what == 'referee':
        bad = check_referee()
    elif what == 'commits':
        upstream = subprocess.run(['git', 'rev-parse', '--verify', '-q', 'origin/main'], capture_output=True).returncode == 0
        bad = check_commits(argv[1] if len(argv) > 1 else 'origin/main..HEAD' if upstream else 'HEAD')
    elif what == 'commit-msg':
        bad = check_commit_msg(argv[1], '--staged' in argv)
    elif what == 'all':
        bad = check_models() + check_tests() + check_referee()
    else:
        sys.exit(__doc__)
    for b in bad:
        print(f'FAIL {b}')
    print(f'{what}: {len(bad)} failed')
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main(sys.argv[1:])
