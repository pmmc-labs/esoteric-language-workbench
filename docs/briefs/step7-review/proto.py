#!/usr/bin/env python3
"""A prototype of step 7's rule, to break it before it is built.

    node docs/briefs/step7-review/gen.ts WORK/c       # the C of every golden test
    python3 docs/briefs/step7-review/proto.py WORK     # run them, every way

It changes nothing in the repository: the runtime it runs is a patched
COPY of runtime/rt.c and rt.h, written to WORK/rt, and every patch asserts
that it matched.

What the copy does, and how it differs from the proposal:
  - a number as a string is on the C stack (the proposal's cure for 2);
  - a collection at EVERY allocation, before it (stress 1);
  - a string that isn't reached is poisoned, marked dead and never handed
    out again (poison, with its quarantine);
  - a dead string that is read stops the program with `internal: ...`
    and status 2, wherever a string's bytes are read (to_str, numeric,
    rt_is_true), or in to_str alone with RT7_CHECK=one, which is what the
    proposal says ("the one place a value becomes a string to read");
  - the roots are NOT slots of a frame. The generated C is left as it is,
    and each `rt_value` local registers its address as it is declared and
    takes it back as its C scope ends (gcc's and clang's `cleanup`). That
    is a SUBSET of what the proposal marks (a frame's slot stays a root
    after its statement or block is over; a C local doesn't), so a
    program this prototype runs right, the proposal's roots run right.
    What it can't show is two things sharing one slot.

The mutations (RT7_SKIP), each a root the collector doesn't look at:
    everything   no root at all: every string is freed at the next allocation
    vars         no variable
    temps        no temporary
    lasttemp     the temporaries with the highest number in the program
                 (the last slot of the proposal's frame)
    lastvar      the variables at the greatest depth (the last variable slot)
    temp:N var:N one slot of the proposal's frame

A test "sees" a mutation when what it prints changes.
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CC = os.environ.get('CURLY_CC', 'cc').split()


def sub(text, old, new, count=1):
    """Replace, and say so if it didn't match as many times as it should."""
    found = text.count(old)
    assert found == count, f'{old!r}: found {found} times, wanted {count}'
    return text.replace(old, new)


def patch_runtime(work):
    h = open(os.path.join(ROOT, 'runtime', 'rt.h')).read()
    c = open(os.path.join(ROOT, 'runtime', 'rt.c')).read()

    # A constant's rt_str says it is one: the last field, zero in every
    # initializer the generated C and the runtime already have.
    h = sub(h, '    const char *bytes;\n} rt_str;', '    const char *bytes;\n    uint64_t heap;\n} rt_str;')
    h = sub(h, '// The context (D28)', '''struct rt_ctx;
rt_value rt_root_t(struct rt_ctx *cx, rt_value *at, int index);
rt_value rt_root_v(struct rt_ctx *cx, rt_value *at, int depth);
void rt_unroot(rt_value *at);
#define RT_ROOTED __attribute__((unused, cleanup(rt_unroot)))
extern int rt7_maxtemp, rt7_maxvar;
// The proposal's frame, when the generated C was rewritten to use one:
// the variables by depth, then the temporaries by number.
extern rt_value *rt7_frame;
extern int rt7_slots, rt7_base;
rt_value rt7_my(rt_value old);

// The context (D28)''')

    c = sub(c, '''typedef struct rt_block {
    struct rt_block *next;
} rt_block;''', '''typedef struct rt_block {
    struct rt_block *next;
    uint64_t mark, dead;
} rt_block;

// The prototype's state is global, which the real one's must not be (D28).
static rt_value **roots;
static int *root_kind, *root_slot;
static long nroots, roots_cap;
static rt_block *quarantine;
static const char *skip;
static int skip_slot = -1, check_one;
static long stress = 1;
static int stale, recheck;
static long collections, freed;

static void root(rt_value *at, int kind, int slot) {
    if (nroots == roots_cap) {
        roots_cap = roots_cap ? roots_cap * 2 : 64;
        roots = realloc(roots, (size_t)roots_cap * sizeof *roots);
        root_kind = realloc(root_kind, (size_t)roots_cap * sizeof *root_kind);
        root_slot = realloc(root_slot, (size_t)roots_cap * sizeof *root_slot);
    }
    roots[nroots] = at; root_kind[nroots] = kind; root_slot[nroots] = slot; nroots++;
}

rt_value rt_root_t(rt_ctx *cx, rt_value *at, int index) {
    (void)cx;
    root(at, 1, index);
    rt_value v; v.tag = 0; v.as.i = 0;
    return v;
}

rt_value rt_root_v(rt_ctx *cx, rt_value *at, int depth) {
    (void)cx;
    root(at, 0, depth);
    return rt_undef();
}

void rt_unroot(rt_value *at) {
    if (nroots == 0 || roots[nroots - 1] != at) { fprintf(stderr, "prototype: roots out of order\\n"); exit(3); }
    nroots--;
}

// `my $x`: an undef. RT7_STALE is the mutation: the slot keeps what the
// last variable to have it left there.
rt_value rt7_my(rt_value old) {
    return stale && old.tag != 0 ? old : rt_undef();
}

static int skipped(int kind, int slot) {
    if (skip == NULL) return 0;
    if (strcmp(skip, "everything") == 0) return 1;
    if (strcmp(skip, "vars") == 0) return kind == 0;
    if (strcmp(skip, "temps") == 0) return kind == 1;
    if (strcmp(skip, "lasttemp") == 0) return kind == 1 && slot == rt7_maxtemp;
    if (strcmp(skip, "lastvar") == 0) return kind == 0 && slot == rt7_maxvar;
    if (strncmp(skip, "temp:", 5) == 0) return kind == 1 && slot == skip_slot;
    if (strncmp(skip, "var:", 4) == 0) return kind == 0 && slot == skip_slot;
    return 0;
}

static void collect(rt_ctx *cx) {
    static long allocations;
    if (allocations++ % stress != stress - 1) return;
    collections++;
    for (rt_block *b = cx->heap; b; b = b->next) b->mark = 0;
    for (long k = 0; k < nroots; k++) {
        if (skipped(root_kind[k], root_slot[k])) continue;
        rt_value *v = roots[k];
        if (v->tag == RT_TAG_STR && v->as.s->heap) ((rt_block *)v->as.s - 1)->mark = 1;
    }
    for (int k = 0; k < rt7_slots; k++) {
        if (k <= rt7_maxvar ? skipped(0, k) : skipped(1, k - rt7_maxvar)) continue;
        rt_value *v = &rt7_frame[k];
        if (v->tag == RT_TAG_STR && v->as.s->heap) ((rt_block *)v->as.s - 1)->mark = 1;
    }
    rt_block **link = &cx->heap;
    while (*link) {
        rt_block *b = *link;
        if (b->mark) { link = &b->next; continue; }
        *link = b->next;
        rt_str *s = (rt_str *)(b + 1);
        memset((char *)(s + 1), '~', s->len);
        b->dead = 1;
        b->next = quarantine;
        quarantine = b;
        freed++;
    }
}

static const rt_str *alive(rt_ctx *cx, const rt_str *s, int in_to_str) {
    if (s->heap && ((const rt_block *)s - 1)->dead && (in_to_str || !check_one)) {
        fflush(stdout);
        fprintf(stderr, "internal: a string was used after it was collected, at %s line %" PRId64 "\\n", cx->file, cx->line);
        exit(2);
    }
    return s;
}

static void again(rt_ctx *cx, const rt_str *s) {
    if (recheck) alive(cx, s, 1);
}

typedef struct { rt_str s; char buf[32]; } scratch;''')

    c = sub(c, '''static void release(rt_ctx *cx) {
    while (cx->heap) {''', '''static void release(rt_ctx *cx) {
    if (getenv("RT7_COUNT")) {
        // What is still held when the program ends, after one last look.
        stress = 1;
        collect(cx);
        long held = 0, bytes = 0;
        for (rt_block *b = cx->heap; b; b = b->next) { held++; bytes += (long)((rt_str *)(b + 1))->len; }
        fprintf(stderr, "collections %ld freed %ld held %ld strings, %ld bytes\\n", collections - 1, freed, held, bytes);
    }
    while (quarantine) {
        rt_block *next = quarantine->next;
        free(quarantine);
        quarantine = next;
    }
    while (cx->heap) {''')
    c = sub(c, '    body(&cx);', '''    skip = getenv("RT7_SKIP");
    if (skip && strchr(skip, ':')) skip_slot = atoi(strchr(skip, ':') + 1);
    check_one = getenv("RT7_CHECK") != NULL;
    if (getenv("RT7_STRESS")) stress = atol(getenv("RT7_STRESS"));
    stale = getenv("RT7_STALE") != NULL;
    recheck = getenv("RT7_RECHECK") != NULL;
    // The mutation: the temporaries begin one slot early, on the deepest variable.
    if (getenv("RT7_OVERLAP") && rt7_base > 0) rt7_base -= 1;
    body(&cx);''')
    c = sub(c, '    rt_block *block = malloc(sizeof(rt_block) + sizeof(rt_str) + len + 1);',
            '    collect(cx);\n    rt_block *block = malloc(sizeof(rt_block) + sizeof(rt_str) + len + 1);')
    c = sub(c, '    block->next = cx->heap;', '    block->mark = 0;\n    block->dead = 0;\n    block->next = cx->heap;')
    c = sub(c, '    s->bytes = p;\n    *bytes = p;', '    s->bytes = p;\n    s->heap = 1;\n    *bytes = p;')

    # A number as a string, on the C stack of whoever asked.
    c = sub(c, '''static const rt_str *to_str(rt_ctx *cx, rt_value v) {
    if (v.tag == RT_TAG_STR) return v.as.s;''', '''static const rt_str *to_str(rt_ctx *cx, rt_value v, scratch *k) {
    if (v.tag == RT_TAG_STR) return alive(cx, v.as.s, 1);''')
    c = sub(c, '''    char buf[32];
    int len = format_number(cx, v, buf);
    char *bytes;
    const rt_str *s = str_new(cx, (uint64_t)len, (uint64_t)len, &bytes);
    memcpy(bytes, buf, (size_t)len);
    return s;''', '''    int len = format_number(cx, v, k->buf);
    k->s.len = (uint64_t)len;
    k->s.chars = (uint64_t)len;
    k->s.bytes = k->buf;
    k->s.heap = 0;
    return &k->s;''')
    # Every caller: a scratch of its own, which lives as long as the block
    # the call is in.
    calls = len(re.findall(r'\bto_str\(cx, (\w+)\)', c))
    assert calls == 14, calls
    c = re.sub(r'\bto_str\(cx, (\w+)\)', r'to_str(cx, \1, &(scratch){ 0 })', c)
    # RT7_RECHECK, which the proposal doesn't have: an operand is looked at
    # again after the allocation, since under stress 1 the collection that
    # frees an operand nobody rooted is the one inside the very operation
    # that reads it, after to_str has passed it.
    c = sub(c, '    memcpy(bytes, s->bytes, s->len);\n    memcpy(bytes + s->len, t->bytes, t->len);',
            '    again(cx, s);\n    again(cx, t);\n    memcpy(bytes, s->bytes, s->len);\n    memcpy(bytes + s->len, t->bytes, t->len);')
    c = sub(c, '    for (uint64_t k = 0; k < n; k++) memcpy(', '    again(cx, s);\n    for (uint64_t k = 0; k < n; k++) memcpy(')
    c = sub(c, '    for (uint64_t at = 0; at < s->len; at++) {\n        char c = s->bytes[at];', '    again(cx, s);\n    for (uint64_t at = 0; at < s->len; at++) {\n        char c = s->bytes[at];')
    c = sub(c, '    memcpy(bytes, s->bytes + from, to - from);', '    again(cx, s);\n    memcpy(bytes, s->bytes + from, to - from);')
    # The other places a string's bytes are read.
    c = sub(c, '        return from_string(cx, v.as.s);', '        return from_string(cx, alive(cx, v.as.s, 0));')
    c = sub(c, '    case RT_TAG_STR: return !(v.as.s->len == 0', '    case RT_TAG_STR: alive(cx, v.as.s, 0); return !(v.as.s->len == 0')

    os.makedirs(os.path.join(work, 'rt'), exist_ok=True)
    open(os.path.join(work, 'rt', 'rt.h'), 'w').write(h)
    open(os.path.join(work, 'rt', 'rt.c'), 'w').write(c)
    subprocess.run(CC + ['-Wall', '-O1', '-c', '-o', os.path.join(work, 'rt', 'rt.o'), os.path.join(work, 'rt', 'rt.c')], check=True)


TEMP = re.compile(r'^(\s*)rt_value t(\d+) RT_UNUSED;$')
VAR = re.compile(r'^(\s*)rt_value (v\d+_\w+) RT_UNUSED = rt_undef\(\);$')


def rewrite(c, frame):
    """A variable's `depth` is how many variables are in scope before it,
    which is the slot the proposal gives it; a temporary's index is its
    number in its statement. Scoped (`frame` false): each rt_value local
    registers itself. Frame: there are no rt_value locals; `v3_x` is the
    frame's slot for its depth and `t2` the second slot after the
    variables, whatever statement it is in, and nothing is cleared but a
    variable where its `my` stands. That is the proposal's layout."""
    out = []
    defines = []
    start = None
    scopes = [0]            # variables declared in each open C block
    maxtemp, maxvar = 0, -1
    inside = False
    for line in c.split('\n'):
        if line.startswith('static void curly_main'):
            inside = True
            start = len(out)
        if not inside:
            out.append(line)
            continue
        m = TEMP.match(line)
        if m:
            n = int(m.group(2))
            maxtemp = max(maxtemp, n)
            if not frame:
                out.append(f'{m.group(1)}rt_value t{n} RT_ROOTED = rt_root_t(cx, &t{n}, {n});')
            continue
        m = VAR.match(line)
        if m:
            depth = sum(scopes)
            maxvar = max(maxvar, depth)
            scopes[-1] += 1
            if frame:
                defines.append(f'#define {m.group(2)} rt7_f[{depth}]')
                out.append(f'{m.group(1)}{m.group(2)} = rt7_my({m.group(2)});')
            else:
                out.append(f'{m.group(1)}rt_value {m.group(2)} RT_ROOTED = rt_root_v(cx, &{m.group(2)}, {depth});')
            continue
        assert 'rt_value t' not in line and not re.search(r'rt_value v\d', line), line
        # A string literal is never in the body: the literals are constants
        # above it. So every brace on a line is a C block's.
        if not line.startswith('    return rt_run('):
            for ch in line:
                if ch == '{':
                    scopes.append(0)
                elif ch == '}':
                    scopes.pop()
        out.append(line)
    assert scopes == [] or scopes == [0], scopes
    tail = f'\nint rt7_maxtemp = {maxtemp}, rt7_maxvar = {maxvar};\n'
    if frame:
        slots = maxvar + 1 + maxtemp
        defines += [f'#define t{n} rt7_f[rt7_base + {n - 1}]' for n in range(1, maxtemp + 1)]
        defines += [f'static rt_value rt7_f[{slots + 1}];', f'rt_value *rt7_frame = rt7_f;', f'int rt7_slots = {slots}, rt7_base = {maxvar + 1};']
        out[start:start] = defines
    else:
        tail += 'rt_value *rt7_frame = 0;\nint rt7_slots = 0, rt7_base = 0;\n'
    return '\n'.join(out) + tail, maxtemp, maxvar


def expected_of(name):
    return open(os.path.join(ROOT, 't', name + '.expected'), 'rb').read()


def run(binary, env):
    # A mutation can make a loop run without end, printing: ten seconds,
    # and a megabyte of what it prints, and no more is ever held.
    r = subprocess.run(['bash', '-c', 'timeout 10 "$0" 2>&1 | head -c 1000000; exit ${PIPESTATUS[0]}', binary], cwd=ROOT,
                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env={**os.environ, **env})
    return r.stdout + (b'' if r.returncode == 0 else f'exit: {r.returncode}\n'.encode())


def build(work, name, frame, rt=None):
    src = os.path.join(work, 'c', name + '.c')
    c, maxtemp, maxvar = rewrite(open(src).read(), frame)
    os.makedirs(os.path.join(work, 'bin'), exist_ok=True)
    name += '.frame' if frame else '.scoped'
    rewritten = os.path.join(work, 'bin', name + '.c')
    open(rewritten, 'w').write(c)
    binary = os.path.join(work, 'bin', name)
    rt = os.path.join(rt or work, 'rt')
    r = subprocess.run(CC + ['-Wall', '-O0', '-I' + rt, '-o', binary, rewritten, os.path.join(rt, 'rt.o'), '-lm'],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert r.returncode == 0, r.stdout.decode()
    return binary, maxtemp, maxvar


# A name, and the environment it is run in.
MODES = {
    'none': {},
    'everything': {'RT7_SKIP': 'everything'},
    'vars': {'RT7_SKIP': 'vars'},
    'temps': {'RT7_SKIP': 'temps'},
    'lasttemp': {'RT7_SKIP': 'lasttemp'},
    'lastvar': {'RT7_SKIP': 'lastvar'},
    'var:0': {'RT7_SKIP': 'var:0'},
    'temp:1': {'RT7_SKIP': 'temp:1'},
    # The proposal's one check, in to_str alone.
    'everything, one check': {'RT7_SKIP': 'everything', 'RT7_CHECK': 'one'},
    # Not the proposal's: the operands checked again after the allocation.
    'everything, recheck': {'RT7_SKIP': 'everything', 'RT7_RECHECK': '1'},
    'temps, recheck': {'RT7_SKIP': 'temps', 'RT7_RECHECK': '1'},
    # A collection at every 2nd, 3rd, 10th allocation and not at every one.
    'everything, stress 2': {'RT7_SKIP': 'everything', 'RT7_STRESS': '2'},
    'everything, stress 3': {'RT7_SKIP': 'everything', 'RT7_STRESS': '3'},
    'everything, stress 10': {'RT7_SKIP': 'everything', 'RT7_STRESS': '10'},
    'vars, stress 2': {'RT7_SKIP': 'vars', 'RT7_STRESS': '2'},
    'temps, stress 2': {'RT7_SKIP': 'temps', 'RT7_STRESS': '2'},
    # Not the collector's but the generated C's, and only of a frame: a
    # `my` that leaves in its slot what was there, and a frame whose
    # temporaries begin on its deepest variable.
    'stale my': {'RT7_STALE': '1'},
    'overlap': {'RT7_OVERLAP': '1'},
}


def one(work, name, frame):
    binary, maxtemp, maxvar = build(work, name, frame)
    want = expected_of(name)
    seen = {}
    for mode, env in MODES.items():
        got = run(binary, env)
        seen[mode] = got != want
        # Wrong, and not said to be: the program ran on with a dead string.
        if seen[mode] and b'internal: ' not in got:
            seen[mode] = 'silent'
    assert not seen['none'], name
    # How many collections freed how much, and what the proposal's one
    # check would have caught of the test's blindness to nothing at all.
    count = run(binary, {'RT7_COUNT': '1'}).decode('utf8', 'replace')
    m = re.search(r'collections (\d+) freed (\d+)', count)
    return name, seen, maxtemp, maxvar, (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def probe(work, argv):
    """proto.py WORK probe FILE.pl [NAME=value ...]: one program of your
    own, under the proposal's frame, with that environment."""
    src = os.path.relpath(os.path.abspath(argv[0]), ROOT)
    r = subprocess.run(['node', os.path.join('docs', 'briefs', 'step7-review', 'gen.ts'), os.path.join(work, 'probes', 'c'), src], cwd=ROOT,
                       stderr=subprocess.PIPE)
    assert b'1 programs' in r.stderr, r.stderr.decode()
    binary, maxtemp, maxvar = build(os.path.join(work, 'probes'), os.path.basename(src)[:-3], True, rt=work)
    env = dict(a.split('=', 1) for a in argv[1:])
    sys.stdout.write(run(binary, env).decode('utf8', 'replace'))


def main():
    work = os.path.abspath(sys.argv[1])
    patch_runtime(work)
    if len(sys.argv) > 2 and sys.argv[2] == 'probe':
        return probe(work, sys.argv[3:])
    names = sorted(f[:-2] for f in os.listdir(os.path.join(work, 'c')) if f.endswith('.c'))
    if len(sys.argv) > 2:
        names = [n for n in names if any(n.startswith(p) for p in sys.argv[2:])]
    for frame in (False, True):
        print('==== the proposal\'s frame: every slot a root, stale or not' if frame else '==== scoped roots: a C local is a root while its C block is open')
        report(work, names, frame)


def report(work, names, frame):
    with ThreadPoolExecutor(max_workers=int(os.environ.get('JOBS', '4'))) as pool:
        results = list(pool.map(lambda n: one(work, n, frame), names))
    red = {mode: [n for n, seen, *_ in results if seen[mode]] for mode in MODES}
    allocating = [n for n, _, _, _, (collections, _) in results if collections > 0]
    freeing = [n for n, _, _, _, (_, freed) in results if freed > 0]
    print(f'{len(results)} tests; {len(allocating)} allocate at all; {len(freeing)} have freed a string by the time they end')
    for mode in MODES:
        silent = sum(1 for n, seen, *_ in results if seen[mode] == 'silent')
        print(f'{mode:24} {len(red[mode]):4} red, {silent} of them with no `internal:`')
    print('red with nothing skipped (the rule itself broken):', red['none'])
    for mode in list(MODES)[2:8] + list(MODES)[-2:]:
        print(f'{mode}:', ' '.join(n.split('-')[0] for n in red[mode]))
    blind = [n for n in allocating if n not in red['everything']]
    both = [n for n in red['everything'] if n not in red['everything, one check']]
    print('red with every root missed, and green when to_str alone checks:', both)
    print(f'allocate, and print the same with every root missed: {len(blind)}')
    with open(os.path.join(work, 'results.frame.txt' if frame else 'results.scoped.txt'), 'w') as f:
        for n, seen, maxtemp, maxvar, (collections, freed) in results:
            f.write(f'{n} maxtemp={maxtemp} maxvar={maxvar} collections={collections} freed={freed} ' + ' '.join(m for m in MODES if seen[m]) + '\n')


if __name__ == '__main__':
    main()
