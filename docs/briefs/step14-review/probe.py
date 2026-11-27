"""Run every probe in a .t file under perl 5.42, plain; print each with its output.

A .t file is probes separated by lines `### NAME`; `use v5.42;` is put in
front of each.  python3 probe.py viv.t [NAME...] > viv.out
"""
import os, subprocess, sys, tempfile

PERL = os.environ.get('CURLY_PERL', '/opt/perl-5.42/bin/perl')


def probes(path):
    name, body, out = None, [], []
    for line in open(path):
        if line.startswith('### '):
            if name:
                out.append((name, ''.join(body)))
            name, body = line[4:].strip(), []
        else:
            body.append(line)
    if name:
        out.append((name, ''.join(body)))
    return out


def run(body):
    with tempfile.NamedTemporaryFile('w', suffix='.pl', delete=False) as f:
        f.write('use v5.42;\n' + body)
        p = f.name
    env = {k: v for k, v in os.environ.items() if k not in ('PERL5OPT', 'PERL_HASH_SEED')}
    try:
        r = subprocess.run([PERL, p], capture_output=True, timeout=10, env=env, stdin=subprocess.DEVNULL)
        res = (r.stdout.decode('utf-8', 'replace'), r.stderr.decode('utf-8', 'replace').replace(p, '-'), r.returncode)
    except subprocess.TimeoutExpired:
        res = ('', 'TIMEOUT\n', -1)
    os.unlink(p)
    return res


if __name__ == '__main__':
    want = set(sys.argv[2:])
    for name, body in probes(sys.argv[1]):
        if want and name not in want:
            continue
        o, e, x = run(body)
        print('### %s\n%s--- perl:\n%s%s[exit %d]\n' % (name, body, o, ''.join('stderr: ' + l + '\n' for l in e.splitlines()), x))
