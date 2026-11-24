"""Hold an accepted program to perl by rules (1), (2), (3)."""
import os, subprocess, sys
import model
sys.setrecursionlimit(1000000)
import threading
threading.stack_size(512 * 1024 * 1024)

HERE = os.path.dirname(os.path.abspath(__file__))
PERL = '/opt/perl-5.42/bin/perl'
ENV = dict(os.environ, PERL_HASH_SEED='1')

def perl_c(rel):
    p = subprocess.run([PERL, '-c', rel], cwd=HERE, env=ENV, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout, p.stderr

def perl_run(rel):
    p = subprocess.run([PERL, '-CSDA', rel], cwd=HERE, env=ENV, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout, p.stderr

def check(src: bytes, rel: str):
    """Returns None if refused, else a list of findings (empty = fine)."""
    try:
        lines, fault = model.run(src)
    except model.Refused:
        return None
    with open(os.path.join(HERE, rel), 'wb') as f:
        f.write(src)
    finds = []
    rc, out, err = perl_c(rel)
    if rc != 0 or out != b'' or err != (rel + ' syntax OK\n').encode():
        finds.append(('rule1', rc, out[:300], err[:600]))
    rc, out, err = perl_run(rel)
    want = ''.join(l + '\n' for l in lines).encode()
    if fault is None:
        if out != want:
            finds.append(('rule2-stdout', rc, out[:300], want[:300], err[:300]))
        if rc != 0:
            finds.append(('rule2-exit', rc, err[:300]))
        if err != b'':
            finds.append(('rule2-stderr', rc, err[:600]))
    else:
        if not out.startswith(want):
            finds.append(('rule3-prefix', rc, out[:300], want[:300], err[:300]))
    return finds

if __name__ == '__main__':
    for rel in sys.argv[1:]:
        src = open(os.path.join(HERE, rel), 'rb').read()
        print(rel, check(src, rel))
