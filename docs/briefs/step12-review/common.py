"""Shared by the step 12 review's scripts: run perl 5.42 plain, with a timeout."""
import os, re, subprocess, tempfile

PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TMP = os.environ.get('REVIEW_TMP', '/tmp/claude-0/-workspace/fef024de-67a3-5769-b4b4-da3a2d1b64f4/scratchpad/review12')
os.makedirs(TMP, exist_ok=True)
SEEDS = ['%064x' % (0x9E3779B97F4A7C15F39CC0605CEDC8341082276BF3A27251F86C6A11D0C18E95 * (i + 1) % (1 << 256)) for i in range(8)]


def perl(body, seed=None, head='use v5.42;\n', name='p.pl'):
    """(stdout, stderr, exit) of a program; stderr has the file's path cut to `-`."""
    path = os.path.join(TMP, '%d-%s' % (os.getpid(), name))
    with open(path, 'w') as f:
        f.write(head + body + '\n')
    env = dict(os.environ)
    env.pop('PERL_HASH_SEED', None)
    env.pop('PERL5OPT', None)
    if seed is not None:
        env['PERL_HASH_SEED'] = seed
        env['PERL_PERTURB_KEYS'] = '0' if seed == '0' else env.get('PERL_PERTURB_KEYS', '')
        if not env['PERL_PERTURB_KEYS']:
            del env['PERL_PERTURB_KEYS']
    try:
        r = subprocess.run([PERL, path], capture_output=True, timeout=10, env=env)
    except subprocess.TimeoutExpired:
        return ('', 'TIMEOUT', -1)
    return (r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace').replace(path, '-'), r.returncode)


def seeds(body, n=8):
    """The set of distinct (stdout, stderr, exit) over n real seeds."""
    return {perl(body, seed=s) for s in SEEDS[:n]}


def keywords():
    src = open(os.path.join(ROOT, 'compiler/src/names.ts')).read()
    out = []
    for name in ('PERL_KEYWORDS', 'PERL_OTHER'):
        m = re.search(r'export const %s: readonly string\[\] = \[(.*?)\];' % name, src, re.S)
        out += re.findall(r"'([^']+)'", m.group(1))
    return out
