#!/usr/bin/env python3
"""The census: other people's probes, each given a verdict (step 11b; D11,
D96, D97).

    python3 t/census.py            # make census: run every probe of t/census/run/, write t/census/census.json
    python3 t/census.py --sort     # the same, and a probe refused by design is moved to t/census/by-design/
    python3 t/census.py --self     # the census's own tests: the judge, the reasons, the check
    python3 t/census.py NAME ...   # those probes alone, their verdicts printed, nothing written

A probe is a Perl program nobody wrote for this language (t/census/
import.py says where they came from). It is compiled, run with the knobs
every test runs with, and held to what perl 5.42 prints for it, run plain
under eight hash seeds. Its verdict:

    SAME      it prints what perl prints, and perl says nothing more
    WARNS     it prints what perl prints, and perl warns: no agreement
              (D15), and a place to look
    LOUD      it faults, having printed the start of what perl prints
    REFUSED   it does not compile; with the reason, by the compiler's
              message: `later N`, a step will take it; `open`, nobody has
              said; (`design Dn` is by design, and --sort moves it away)
    UNJUDGED  perl's own output moves with the hash seed, or perl does not
              end
    WRONG     anything else: it ran, did not fault, and differed; or
              faulted after printing what perl does not; or did not end;
              or broke

t/census/census.json is written by this and by nothing else, one probe a
line, and is kept in git: its history is the census's. t/checks.py holds
it to the files of run/, to no WRONG, and to the last commit's: a probe
that was SAME there is SAME here, or is named in t/census/LEFT-SAME.tsv
with the decision that moved it.

A probe's reason is its first refusal's (D97): a program refused for `@_`
on its first line may want a hash on its third.
"""

import collections
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks

RUN = 't/census/run'
BY_DESIGN = 't/census/by-design'
NOT_PERL = 't/census/not-perl'
JSON = 't/census/census.json'
SORTED = 't/census/BY-DESIGN.tsv'
LEFT = 't/census/LEFT-SAME.tsv'
BUILD = 'build/census'
VERDICTS = ('SAME', 'WARNS', 'LOUD', 'REFUSED', 'UNJUDGED', 'WRONG')
# A probe is small: one that runs this long has not ended.
OURS_LIMIT = 60

# ---- why a probe is refused: the compiler's message, to its reason.
# The first that matches. `design`: a decision cut it, and the probe will
# never run. `later`: the step that will take it. Anything else is `open`:
# the message is one a program of the language's own could meet too, or
# nobody has said. This table is what the language has decided about
# Perl, as far as the probes ask; a step that takes a construct in takes
# its row out.
N = r"'[^']*'"
REASONS = [
    # ---- by design
    (r'^@_ is not in the language', 'design', 'D17'),
    (r"is an element of perl's own @_ or %_", 'design', 'D17'),
    (r'is read-only: in perl, changing it changes', 'design', 'D17'),
    (r"is its loop's variable, and read-only", 'design', 'D17'),
    (r"is its loop's own element", 'design', 'D17'),
    (r'borrows a variable from outside the loop', 'design', 'D17'),
    (r"^'(our|local|package)' is not in the language$", 'design', 'D19'),
    (r"^'::' hard after", 'design', 'D19'),
    (r"^'(eval|redo|goto|continue|BEGIN|END|require|wantarray|caller)' is not in the language$", 'design', 'D13'),
    (r"^expected a value, found '(eval|caller|wantarray)'$", 'design', 'D13'),
    (r"^'use (feature|strict|warnings)' is not in the language$", 'design', 'D16'),
    (r"^'(use|no) \w+' goes at the top", 'design', 'D16'),
    # (Step 13a: what references reach is D109's name in D76's walk, and
    # making a hop changes the head of its chain, D114.)
    (r"can change what references reach", 'design', 'D109'),
    (r"^the store makes what", 'design', 'D114'),
    (r"^a later part of .* can change .* which an earlier part names", 'design', 'D76'),
    (r"^a later piece of a concatenation", 'design', 'D57'),
    (r"of an assignment of (a concatenation|an interpolated string)", 'design', 'D57'),
    (r"^this can change .* which the list of the loop it is in names", 'design', 'D77'),
    (r"^an assignment of a list is a statement", 'design', 'D78'),
    (r"is not a name a program may declare", 'design', 'D55'),
    (r"outside the block of a (sort|for)", 'design', 'D55'),
    (r"is past the largest integer", 'design', 'D38'),
    (r"starts with a zero: perl reads that as octal", 'design', 'D38'),
    (r"ends with a point", 'design', 'D38'),
    (r"is not a number in the language", 'design', 'D38'),
    (r"where one value is wanted", 'design', 'D80'),
    (r"^else after unless", 'design', 'D54'),
    (r"^a sub may not be called", 'design', 'D21'),
    (r"^(print|say) is a statement, and has no value", 'design', 'D21'),
    (r"^sort takes no brackets of its own", 'design', 'D87'),
    (r"here: a my begins a statement", 'design', 'D56'),
    (r"again in one scope", 'design', 'D56'),
    (r"^in a string an index is a whole number or a scalar variable", 'design', 'D91'),
    (r"in a double-quoted string begins a (variable|array), and no name is hard against it", 'design', 'D92'),
    (r"^'\[' hard after .* in a string: another index, to perl; write", 'design', 'D92'),
    (r"with nothing but a constant on its right", 'design', 'D53'),
    (r"perl chains two comparisons", 'design', 'D50'),
    (r"perl takes .* for a file handle", 'design', 'D21'),
    (r"^a line that starts '#!'", 'design', 'D33'),
    (r"only has a value, and nothing is done with it", 'design', 'D15'),
    (r"^'(chop|srand|local|tie|format|write|each)' is not in the language$", 'design', 'D17'),
    (r"^in a string a key is a word or a scalar variable", 'design', 'D99'),
    (r"a slice of a hash, to perl, which is not in a string", 'design', 'D99'),
    (r"^a hash was changed while a foreach is over it", 'design', 'D17'),
    (r"are on one line: across the end of a line", 'design', 'D102'),
    (r"is on one line with them: across the end of a line", 'design', 'D102'),
    (r"which is a string here: perl makes one string of the two", 'design', 'D102'),
    (r"alone in a hash's braces is the string", 'design', 'D102'),
    (r"^a comma in the block of a map, a grep or a sort", 'design', 'D102'),
    (r"perl reads on for (exists|delete|keys|values)'s argument", 'design', 'D102'),
    (r"^expected a value, found '(chop|each)'$", 'design', 'D17'),
    # ---- step 13a's (D108, D110, D112, D113)
    (r"is cut \(D108\)", 'design', 'D108'),
    (r"\(D110\)", 'design', 'D110'),
    (r"^ref before '", 'design', 'D112'),
    (r"perl guesses that it is a new hash", 'design', 'D113'),
    (r"^'\{' first (after|in) (say|print)", 'design', 'D113'),
    (r"^a blank between (two subscripts|a subscript and)", 'design', 'D104'),
    # ---- later, by the step
    (r"\(step 13b\)", 'later', '13b'),
    (r"\(step 13c\)", 'later', '13c'),
    (r"\(step 13d\)", 'later', '13d'),
    (r"\(step 14\)", 'later', '14'),
    (r"\(step 17\)", 'later', '17'),
    (r"^a sub with no name, as a value", 'later', '14'),
    (r"^'&' is not in the language yet", 'later', '14'),
    (r"^'(die|warn|try|catch)' is not in the language$", 'later', '15'),
    (r"^expected a value, found '(die|warn)'$", 'later', '15'),
    (r"^expected a value, found '(sprintf|qw|q|qq|ucfirst|lcfirst|rindex|join|reverse|sprintf|chomp|abs|int|sqrt)'$", 'later', '16'),
    (r"^'(printf|chomp|qw|q|qq)' is not in the language$", 'later', '16'),
    (r"^'<<' is not in the language yet", 'later', '16'),
    (r"^'(class|method|field|bless)' is not in the language$", 'later', '17'),
    (r"^expected a value, found 'bless'$", 'later', '17'),
    (r"^'use \w+' is not in the language$", 'later', '18'),
    (r"^'=~' is not in the language yet", 'later', '19'),
    (r"^'(s|m|tr|y|split)' is not in the language$", 'later', '19'),
    (r"^expected a value, found '(split|m|s|tr)'$", 'later', '19'),
    (r"^expected a value, found '(time|localtime|gmtime|rand)'$", 'later', '22'),
    (r"^expected a value, found '(STDERR|STDOUT|STDIN|open)'$", 'later', '21'),
]
REASONS = [(re.compile(pattern), kind, ref) for pattern, kind, ref in REASONS]

def reason(message):
    for pattern, kind, ref in REASONS:
        if pattern.search(message):
            return f'{kind} {ref}'
    return 'open'

# ---- the judge

def clip(data, n=120):
    text = data.decode('utf-8', 'replace') if isinstance(data, bytes) else data
    return text if len(text) <= n else text[:n] + '...'

def judge(perl, ours):
    """A verdict and what to say of it, from perl's runs (one a seed: each
    None for one that did not end, or (status, stdout, stderr)) and the
    compiled program's run (None, or the same three)."""
    if any(p is None for p in perl):
        return 'UNJUDGED', 'perl does not end'
    if len(set(p[1] for p in perl)) > 1 or len(set(p[0] for p in perl)) > 1:
        return 'UNJUDGED', "perl's output moves with the hash seed"
    status, out, err = perl[0]
    if ours is None:
        return 'WRONG', f'it does not end in {OURS_LIMIT} seconds, and perl does'
    code, mine, said = ours
    if code == 1 and said.startswith(b'fault: '):
        if out.startswith(mine):
            return 'LOUD', re.sub(rb' at \S+ line (\d+)\.\n$', rb' at line \1', said[7:]).decode('utf-8', 'replace')
        return 'WRONG', f'it faults after printing what perl does not: {clip(mine)!r}, where perl prints {clip(out)!r}'
    if code != 0 or said:
        return 'WRONG', f'it breaks: exit {code}, {clip(said)!r}'
    if status != 0:
        return 'WRONG', f'it runs, and perl dies: {clip(err)!r}'
    if mine != out:
        return 'WRONG', f'it prints {clip(mine)!r}, and perl {clip(out)!r}'
    if err:
        return 'WARNS', clip(re.sub(rb' at \S+ line (\d+)\.', rb' at line \1.', err.split(b'\n')[0]))
    return 'SAME', ''

def triple(run):
    return None if run is None else (run.returncode, run.stdout, run.stderr)

def probe(name, knobs):
    """One probe that passes the compiler's front: compiled by the driver,
    run, and judged."""
    path = f'{RUN}/{name}'
    exe = f'{BUILD}/{name[:-3]}'
    os.makedirs(os.path.dirname(exe), exist_ok=True)
    built = subprocess.run(['node', 'bin/curlyc.ts', '-o', exe, path], capture_output=True, text=True)
    try:
        if built.returncode == 1:
            where, _, message = built.stderr.strip().partition(': ')
            return refusal(where.split(':', 1)[1], message)
        if built.returncode != 0:
            return {'verdict': 'WRONG', 'why': f'the compiler breaks: {clip(built.stderr)!r}'}
        try:
            perl = [triple(checks.run_perl([], path, {}, seed, checks.PERL_LIMIT)) for seed in checks.SEEDS]
            env = dict(knobs, PATH=os.environ.get('PATH', ''))
            ours = triple(checks.run_capped([exe], env, b'', OURS_LIMIT))
        except checks.Runaway as e:
            return {'verdict': 'UNJUDGED', 'why': str(e)}
        verdict, why = judge(perl, ours)
        return {'verdict': verdict, 'why': why} if why else {'verdict': verdict}
    finally:
        for f in (exe, exe + '.c', exe + '.rt.o'):
            if os.path.exists(f):
                os.unlink(f)

def refusal(at, message):
    return {'verdict': 'REFUSED', 'reason': reason(message), 'at': at, 'why': message}

def names(root):
    return sorted(os.path.relpath(os.path.join(d, f), root) for d, _, files in os.walk(root) for f in files if f.endswith('.pl'))

def census(only=None):
    """Every probe of run/, or those named, to its verdict."""
    wanted = only or names(RUN)
    front = subprocess.run(['node', 't/census/front.ts'], input=''.join(f'{RUN}/{n}\n' for n in wanted), capture_output=True, text=True)
    assert front.returncode == 0, front.stderr[-2000:]
    found, compile_ = {}, []
    for line in front.stdout.splitlines():
        j = json.loads(line)
        name = os.path.relpath(j['path'], RUN)
        if 'refused' in j:
            found[name] = refusal(j['at'], j['refused'])
        else:
            compile_.append(name)
    assert len(found) + len(compile_) == len(wanted), 'the front lost a probe'
    knobs = checks.knobs()
    with ThreadPoolExecutor(int(os.environ.get('JOBS', os.cpu_count() or 4))) as pool:
        for name, result in zip(compile_, pool.map(lambda n: probe(n, knobs), compile_)):
            found[name] = result
    return dict(sorted(found.items()))

def count(root):
    return len(names(root)) if os.path.isdir(root) else 0

def dumps(probes):
    """The file: its counts, and one probe a line."""
    counts = collections.Counter(p['verdict'] for p in probes.values())
    reasons = collections.Counter(p['reason'].split()[0] for p in probes.values() if p['verdict'] == 'REFUSED')
    head = {
        # (5.42, and not which 5.42: the file is written on more than one machine.)
        'perl': 'v5.42',
        'counts': {v: counts.get(v, 0) for v in VERDICTS},
        'refused': {k: reasons.get(k, 0) for k in ('later', 'open', 'design')},
        'by_design': count(BY_DESIGN),
        'not_perl': count(NOT_PERL),
    }
    lines = [f'  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}' for k, v in head.items()]
    body = ',\n'.join(f'    {json.dumps(name)}: {json.dumps(p, ensure_ascii=False)}' for name, p in probes.items())
    return '{\n' + ',\n'.join(lines) + ',\n  "probes": {\n' + body + '\n  }\n}\n'

def sort(probes):
    """A probe refused by design leaves run/ for by-design/, with the
    decision that refuses it written down; returns the rest."""
    kept, moved = {}, []
    for name, p in probes.items():
        if p['verdict'] == 'REFUSED' and p['reason'].startswith('design '):
            os.makedirs(os.path.dirname(f'{BY_DESIGN}/{name}'), exist_ok=True)
            shutil.move(f'{RUN}/{name}', f'{BY_DESIGN}/{name}')
            moved.append((name, p['reason'].split()[1], p['why']))
        else:
            kept[name] = p
    rows = {}
    if os.path.exists(SORTED):
        for line in open(SORTED, encoding='utf-8'):
            if not line.startswith('#'):
                rows[line.split('\t')[0]] = line
    for name, decision, why in moved:
        rows[name] = f'{name}\t{decision}\t{why}\n'
    with open(SORTED, 'w', encoding='utf-8') as f:
        f.write('# The probes the language refuses by design, and are not run (t/census.py --sort writes this file):\n')
        f.write('# the decision, and what the compiler said when the probe was moved. If the language takes back\n')
        f.write('# what refuses one, move it to t/census/run/ and take its line out.\n# probe\tdecision\trefusal\n')
        f.writelines(rows[k] for k in sorted(rows))
    return kept, len(moved)

# ---- what t/checks.py holds the file to

def left_same():
    if not os.path.exists(LEFT):
        return set()
    return {line.split('\t')[0] for line in open(LEFT, encoding='utf-8') if line.strip() and not line.startswith('#')}

def problems(now, before, files, allowed):
    """What is wrong with the census's file: `now` and `before` are the
    file as it is and as the last commit has it (None for none), `files`
    the probes of run/."""
    bad = []
    probes = now['probes']
    if sorted(probes) != sorted(files):
        missing = sorted(set(files) - set(probes))[:3]
        extra = sorted(set(probes) - set(files))[:3]
        bad.append(f'{JSON}: not the probes of {RUN}/ (not in the file: {missing}; not in run/: {extra}); `make census`')
    counts = collections.Counter(p['verdict'] for p in probes.values())
    if {v: counts.get(v, 0) for v in VERDICTS} != now.get('counts'):
        bad.append(f'{JSON}: its counts are not its probes\'; `make census` writes the file, and nothing else does')
    for name, p in probes.items():
        if p['verdict'] not in VERDICTS:
            bad.append(f'{JSON}: {name} has the verdict {p["verdict"]}, which is none')
        if p['verdict'] == 'WRONG':
            bad.append(f'census: {name} is WRONG: {p.get("why", "")}')
    if before is not None:
        for name, p in before['probes'].items():
            if p['verdict'] == 'SAME' and name not in allowed and probes.get(name, {}).get('verdict') != 'SAME':
                what = probes[name]['verdict'] if name in probes else 'gone'
                bad.append(f'census: {name} was SAME in the last commit and is {what}: a probe leaves SAME by a decision, named in {LEFT}')
    return bad

def check():
    if not os.path.exists(JSON):
        return [f'{JSON}: not there; `make census`']
    now = json.load(open(JSON, encoding='utf-8'))
    old = subprocess.run(['git', 'show', f'HEAD:{JSON}'], capture_output=True, text=True)
    before = json.loads(old.stdout) if old.returncode == 0 else None
    bad = problems(now, before, names(RUN), left_same())
    listed = set()
    if os.path.exists(SORTED):
        listed = {line.split('\t')[0] for line in open(SORTED, encoding='utf-8') if not line.startswith('#')}
    for name in names(BY_DESIGN) if os.path.isdir(BY_DESIGN) else []:
        if name not in listed:
            bad.append(f'{BY_DESIGN}/{name}: no decision in {SORTED}; a probe is moved there by `t/census.py --sort`, never by hand')
    return bad

# ---- the census's own tests

def self_test():
    """The judge on each kind of run, the reasons, and the check broken
    each way it guards against: every line an assertion."""
    ok, clean = (0, b'1\n2\n', b''), [(0, b'1\n2\n', b'')] * 8
    cases = [
        ('SAME', clean, ok),
        ('WARNS', [(0, b'1\n2\n', b'Use of uninitialized value at t/x.pl line 3.\n')] * 8, ok),
        ('LOUD', clean, (1, b'1\n', b'fault: division by zero at t/x.pl line 2.\n')),
        ('LOUD', clean, (1, b'', b'fault: division by zero at t/x.pl line 1.\n')),
        ('WRONG', clean, (1, b'1\n3\n', b'fault: division by zero at t/x.pl line 2.\n')),
        ('WRONG', clean, (0, b'1\n3\n', b'')),
        ('WRONG', clean, (0, b'1\n', b'')),
        ('WRONG', clean, (0, b'1\n2\n3\n', b'')),
        ('WRONG', clean, None),
        ('WRONG', clean, (2, b'1\n2\n', b'internal: a string that was collected\n')),
        ('WRONG', clean, (-11, b'1\n2\n', b'')),
        ('WRONG', clean, (0, b'1\n2\n', b'something on stderr\n')),
        ('WRONG', [(255, b'1\n2\n', b'Died at t/x.pl line 3.\n')] * 8, ok),
        ('UNJUDGED', clean[:7] + [(0, b'2\n1\n', b'')], ok),
        ('UNJUDGED', clean[:7] + [None], ok),
        ('UNJUDGED', clean[:7] + [(0, b'2\n1\n', b'')], (0, b'9\n', b'')),
    ]
    failed = []
    for n, (want, perl, ours) in enumerate(cases):
        got = judge(perl, ours)[0]
        if got != want:
            failed.append(f'judge, case {n}: {got}, not {want}')
    for message, want in (
        ('@_ is not in the language: a sub has a signature (D17)', 'design D17'),
        ('in a string a key is a word or a scalar variable, hard against its braces (D99): take the key into a my first', 'design D99'),
        ("a comma in the block of a map, a grep or a sort: put the list in brackets, map { ($_ => 1) } ...", 'design D102'),
        ("'=~' is not in the language yet", 'later 19'),
        ("@$ before a name is cut (D108): an array through a reference is written $r->@* (step 13b)", 'design D108'),
        ("->@*: the whole container through a reference is not in the language yet (step 13b)", 'later 13b'),
        ("'[' hard after $a[0] in a string: another index, to perl, and an element through a reference in a string is not in the language yet (step 13d); write $a[0]\\[", 'later 13d'),
        ("'[' hard after $#a in a string: another index, to perl; write $#a\\[", 'design D92'),
        ("a later part of say's list can change what references reach, which an earlier part names: perl reads it after the change; take the value into a my first", 'design D109'),
        ("expected ';', found '{'", 'open'),
        ('a message no table has', 'open'),
    ):
        if reason(message) != want:
            failed.append(f'reason of {message!r}: {reason(message)}, not {want}')
    same, refused = {'verdict': 'SAME'}, {'verdict': 'REFUSED', 'reason': 'open', 'at': '1:1', 'why': 'x'}
    def file(probes):
        counts = collections.Counter(p['verdict'] for p in probes.values())
        return {'counts': {v: counts.get(v, 0) for v in VERDICTS}, 'probes': probes}
    good = file({'a.pl': same, 'b.pl': refused})
    checks_ = [
        ('a file as it should be', problems(good, good, ['a.pl', 'b.pl'], set()), 0),
        ('no last commit', problems(good, None, ['a.pl', 'b.pl'], set()), 0),
        ('a probe of run/ not in the file', problems(good, good, ['a.pl', 'b.pl', 'c.pl'], set()), 1),
        ('a probe in the file and not in run/', problems(good, good, ['a.pl'], set()), 1),
        ('a WRONG', problems(file({'a.pl': same, 'b.pl': {'verdict': 'WRONG', 'why': 'x'}}), good, ['a.pl', 'b.pl'], set()), 1),
        ('a SAME that is refused now', problems(file({'a.pl': refused, 'b.pl': refused}), good, ['a.pl', 'b.pl'], set()), 1),
        ('a SAME that is refused now, by a decision', problems(file({'a.pl': refused, 'b.pl': refused}), good, ['a.pl', 'b.pl'], {'a.pl'}), 0),
        ('a SAME that is gone', problems(file({'b.pl': refused}), good, ['b.pl'], set()), 1),
        ('a refusal that is SAME now', problems(file({'a.pl': same, 'b.pl': same}), good, ['a.pl', 'b.pl'], set()), 0),
        ('counts that are not the probes\'', problems(dict(good, counts=dict(good['counts'], SAME=5)), good, ['a.pl', 'b.pl'], set()), 1),
        ('a verdict there is none of', problems(file({'a.pl': same, 'b.pl': {'verdict': 'FINE'}}), None, ['a.pl', 'b.pl'], set()), 1),
    ]
    for what, bad, want in checks_:
        if len(bad) != want:
            failed.append(f'check, {what}: {len(bad)} problems, not {want}: {bad}')
    total = len(cases) + 6 + len(checks_)
    return failed, total

def main(argv):
    os.chdir(ROOT)
    if argv == ['--self']:
        failed, total = self_test()
        for f in failed:
            print(f'FAIL {f}')
        print(f'census: {total} tests of the census itself, {len(failed)} failed')
        sys.exit(1 if failed else 0)
    if checks.perl_problem():
        sys.exit(f'census: {checks.perl_problem()}')
    only = [a for a in argv if not a.startswith('--')]
    probes = census(only or None)
    if only:
        for name, p in probes.items():
            print(name, json.dumps(p, ensure_ascii=False))
        return
    moved = 0
    if '--sort' in argv:
        probes, moved = sort(probes)
    open(JSON, 'w', encoding='utf-8').write(dumps(probes))
    counts = collections.Counter(p['verdict'] for p in probes.values())
    print(f'census: {len(probes)} probes: ' + ', '.join(f'{counts.get(v, 0)} {v}' for v in VERDICTS)
          + (f'; {moved} moved to by-design/' if moved else '') + f'; {count(BY_DESIGN)} refused by design and {count(NOT_PERL)} that perl stops at are not run')
    for name, p in probes.items():
        if p['verdict'] == 'WRONG':
            print(f'WRONG {name}: {p.get("why", "")}')
    sys.exit(1 if counts.get('WRONG') else 0)

if __name__ == '__main__':
    main(sys.argv[1:])
