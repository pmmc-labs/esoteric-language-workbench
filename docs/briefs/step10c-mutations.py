#!/usr/bin/env python3
"""Break step 10c's sort on purpose, one way at a time, in the runtime's
merge and in each pass of the compiler, and see that a test goes red each
time.

    python3 docs/briefs/step10c-mutations.py            # all of them
    python3 docs/briefs/step10c-mutations.py "block"    # those named so
    python3 docs/briefs/step10c-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 10c, t/1200*.pl to t/1269*.pl, and 580, 581
           and 1177, the refused ones too, run with the knobs of
           t/knobs.sh and each test's own `# env:`, as t/run.sh runs
           them. For a broken runtime each test's C is compiled once, by
           the compiler as it is, and linked again with the broken
           runtime; for a broken compiler each is compiled again by the
           copy
  unit     the runtime's own test of its sort machine, held to perl over
           4,200 lists, in the copy

(t/models/merge.py, the same merge in Python, breaks itself eight ways:
`python3 t/models/merge.py --self`.)

A record of step 10c, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
CHECK = 'compiler/src/checker.ts'
PARSE = 'compiler/src/parser.ts'
FROZEN = '    if (a->frozen != 0) rt_fault(cx, "an array was changed while a foreach is over it");\n'
SHAPES = 'compiler/src/shapes.ts'
SORT = 'runtime/sort.c'
BLOCK = "    b.out.base = b.values;\n    const statements = e.body.slice(0, -1).flatMap(t => genStmt(t, b.out));\n    b.out.base = base;\n    b.lines.push(...statements, `cx->line = ${last.pos.line};`);\n    const answer"
END = "`rt_sort_end(cx, ${so}, ${list});`,\n        ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`), `cx->line = ${b.line};`);"
MUTATIONS = [
 # ---- the runtime's merge
 ("a run is looked for after 7 pairs", SORT, "#define SORT_PTHRESH 8 ", "#define SORT_PTHRESH 7 "),
 ("a merge doubles its step after 5", SORT, "#define SORT_RTHRESH 6 ", "#define SORT_RTHRESH 5 "),
 ("equal is low from either run", SORT, "                            s->sense = -1;", "                            s->sense = 0;"),
 ("the search rounds up", SORT, "s->p = s->b + (s->t - s->b - 1) / 2;", "s->p = s->b + (s->t - s->b) / 2;"),
 ("a run that goes down is not turned round", SORT, "                            base[s->b] = base[s->p];\n                            base[s->p] = c;\n", ""),
 ("the halves are split the other way", SORT, "                s->stack[s->sp].runs = s->runs / 2;\n                s->runs -= s->runs / 2;", "                s->stack[s->sp].runs = s->runs - s->runs / 2;\n                s->runs = s->runs / 2;"),
 ("the singleton at the end is not picked up", SORT, "                    if (s->p == s->t && s->t + 1 == s->last) {\n                        ASK(", "                    if (0) {\n                        ASK("),
 ("a block's value may be any size", SORT, "    if (n < INT32_MIN || n > INT32_MAX) rt_fault(", "    if (0) rt_fault("),
 ("the limit on a block's value is one lower", SORT, "    if (n < INT32_MIN || n > INT32_MAX) rt_fault(", "    if (n < INT32_MIN || n >= INT32_MAX) rt_fault("),
 ("the limit on a block's value is one higher below", SORT, "    if (n < INT32_MIN || n > INT32_MAX) rt_fault(", "    if (n < INT32_MIN - INT64_C(1) || n > INT32_MAX) rt_fault("),
 ("a block's value is taken the other way", SORT, "    s->answer = n;", "    s->answer = -n;"),
 ("a lone value is never looked at", SORT, "            if (s->n == 1 && s->lone) {", "            if (0) {"),
 ("a sort with no block does not look at each value first", SORT, "        to_str(cx, given->items[k], &x);\n", "        (void)x;\n"),
 ("an undef may be sorted in place", SORT, "        if (a->items[k].tag == RT_TAG_UNDEF) rt_fault(", "        if (0) rt_fault("),
 ("the values come out as they went in", SORT, "from->items[s->cells[0] == NULL ? k : s->cells[0][k]]", "from->items[k]"),
 # ---- the code generator
 ("a sort's list is any list", GEN, "    const source = genList(e.items, b, 2);\n    if (e.body === undefined) {", "    const source = genList(e.items, b, 0);\n    if (e.body === undefined) {"),
 ("a sort freezes nothing", GEN, "    b.lines.push(`${held} = ${source.c};`, ...each.arrays.map(a => `rt_freeze(cx, ${slot(a)});`));\n    if (b.inPlace === e)", "    b.lines.push(`${held} = ${source.c};`);\n    if (b.inPlace === e)"),
 ("a sort gives nothing back", GEN, END, "`rt_sort_end(cx, ${so}, ${list});`,\n        `cx->line = ${b.line};`);"),
 ("the line after a sort is its block's", GEN, END, "`rt_sort_end(cx, ${so}, ${list});`,\n        ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`));"),
 ("no sort is in place", GEN, "    if (b.inPlace === e) b.lines.push(", "    if (false) b.lines.push("),
 ("every sort is in place", GEN, "    if (b.inPlace === e) b.lines.push(", "    if (true) b.lines.push("),
 ("a sort through brackets is not in place", GEN, "    const sort = behind(value);\n    if (target.kind !== 'array' || sort.kind !== 'sort'", "    const sort = value;\n    if (target.kind !== 'array' || sort.bracketed || sort.kind !== 'sort'"),
 ("a sort of another array is in place", GEN, "    return from.kind === 'array' && b.names.of.get(from) === b.names.of.get(target) ? sort : undefined;", "    return from.kind === 'array' ? sort : undefined;"),
 ("no block is one perl throws away", GEN, "${thrownAway(e) ? 1 : 0}", "${0}"),
 ("every block is one perl throws away", GEN, "${thrownAway(e) ? 1 : 0}", "${1}"),
 ("a sort block's temporaries are the statement's own", GEN, BLOCK, BLOCK.replace("b.out.base = b.values;", "b.out.base = 0;")),
 # ---- the resolver
 ("a sort's block is no wall to last and next", RESOLVE, "            round.push({ wall: 'sort' });\n", "            round.push({ bare: e.pos });\n"),
 ("$a outside a sort is any variable with no my", RESOLVE, "            if (found === undefined && (e.name === 'a' || e.name === 'b')) return refuse(", "            if (false) return refuse("),
 ("$a and $b are not read-only", RESOLVE, "        variables.forEach(v => readonly.add(of.get(v)!));\n", ""),
 # ---- the checker
 ("sort names nothing", CHECK, "    else if (e.kind === 'sort') e.items.forEach(x => named(w, x, true, into));\n", ""),
 ("a sort's block is no part of it", CHECK, "    : e.kind === 'sort' ? [...e.items, ...within(e.body ?? [])]\n", "    : e.kind === 'sort' ? [...e.items]\n"),
 ("a sort's list is not held to D76 and D77", CHECK, "        bound(w, \"sort's list\", 'the sort', e.items, e.body);\n", ""),
 ("sort may stand where one value is wanted", CHECK, "    if (e.kind === 'sort') refuse('sort where one value is wanted", "    if (false) refuse('sort where one value is wanted"),
 ("a sort's block gives a list", CHECK, "        // One value, which says which of the two comes first.\n        checkExpr(w, last.expr, true, 'scalar');", "        checkExpr(w, last.expr, true, 'list');"),
 # ---- what is list-shaped
 ("a sort is not list-shaped", SHAPES, "    case 'sort': return true;", "    case 'sort': return false;"),
 # ---- the parser
 ("a word may come first after sort", PARSE, "        if (first.kind === 'word' && !PERL_KEYWORDS.includes(first.text)) {", "        if (false) {"),
 ("a scalar may come first after sort", PARSE, "        if (first.kind === 'var') refuse(`${first.text} first after sort:", "        if (false) refuse(`${first.text} first after sort:"),
 ("sort may have brackets of its own", PARSE, "        if (first.kind === '(') refuse('sort takes no brackets of its own: sort LIST, or sort { ... } LIST', first.pos);\n", ""),
 ("a sort's block may end in a say", PARSE, "            const { body, items } = blockAndList(head, false);", "            const { body, items } = blockAndList(head, true);"),
 ("a program may declare $a", PARSE, "        : v.name === 'a' || v.name === 'b' ? refuse(", "        : false ? refuse("),
]

only = sys.argv[1:]
if only == ['--match']:
    for name, path, old, new in MUTATIONS:
        n = open(path).read().count(old)
        if n != 1:
            print(n, name)
    print(len(MUTATIONS), 'pieces of text looked for')
    sys.exit(0)
knobs = checks.knobs()
tests = []
for src in sorted(glob.glob('t/12[0-6][0-9]-*.pl') + glob.glob('t/58[01]-*.pl') + glob.glob('t/1177-*.pl')):
    head = open(src, encoding='utf-8', errors='replace').read(1200)
    env = dict(os.environ)
    env.update(knobs)
    found = re.search(r'^# env: (.*)$', head, re.M)
    if found:
        env.update(pair.split('=', 1) for pair in found.group(1).split())
    tests.append((os.path.basename(src)[:-3], open(src[:-3] + '.expected', 'rb').read(), env, 'kind: refused' in head))
ran = [t for t in tests if not t[3]]

def passes(test, driver):
    name, expected, env, refused = test
    if driver is None:
        # The test's own C as it was compiled at the start, and the
        # runtime of the copy.
        if subprocess.run(['cc', '-o', f'build/mut/{name}', f'build/mut/{name}.o', 'build/mut/rt.o', '-lm'], capture_output=True).returncode:
            return False
    else:
        built = subprocess.run(['node', driver, '-o', f'build/mut/{name}', f't/{name}.pl'], capture_output=True)
        if refused:
            return built.stderr + f'exit: {built.returncode}\n'.encode() == expected
        if built.returncode:
            return False
    try:
        run = checks.run_capped(['sh', '-c', 'exec "$0" 2>&1', f'build/mut/{name}'], env, b'', 20)
    except checks.Runaway:
        return False
    if run is None:
        return False
    got = run.stdout + (f'exit: {run.returncode}\n'.encode() if run.returncode else b'')
    return got == expected

def golden(driver):
    which = ran if driver is None else tests
    with ThreadPoolExecutor(6) as pool:
        return [t[0] for t, ok in zip(which, pool.map(lambda t: passes(t, driver), which)) if not ok]

def unit(tree):
    """How many of the runtime's own tests fail, in the copy."""
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'sort machine', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
    return len(re.findall(r'^not ok', r.stdout, re.M)) if r.returncode else 0

def copy():
    shutil.rmtree('build/mut/tree', ignore_errors=True)
    for part in ('bin', 'compiler/src', 'runtime'):
        shutil.copytree(part, 'build/mut/tree/' + part)

def runtime():
    """The copy's runtime, compiled; whether it compiled."""
    return subprocess.run(['cc', '-O1', '-c', '-Ibuild/mut/tree/runtime', '-o', 'build/mut/rt.o', 'build/mut/tree/runtime/rt.c'], capture_output=True).returncode == 0

os.makedirs('build/mut', exist_ok=True)
copy()
whole, units = golden('build/mut/tree/bin/curlyc.ts'), unit('build/mut/tree')
assert whole == [] and units == 0, f'things as they are fail: {whole}, {units} unit tests'
for name, _, _, _ in ran:
    subprocess.run(['cc', '-O0', '-c', '-Iruntime', '-o', f'build/mut/{name}.o', f'build/mut/{name}.c'], check=True)
assert runtime() and golden(None) == []
print(f'{len(tests)} golden tests and the unit tests pass as things are', flush=True)
missed = []
for name, path, old, new in MUTATIONS:
    if only and not any(o in name for o in only):
        continue
    copy()
    text = open(path).read()
    assert text.count(old) == 1, (name, text.count(old))
    open('build/mut/tree/' + path, 'w').write(text.replace(old, new))
    if path in (RT, SORT):
        failed = golden(None) if runtime() else ['the runtime does not compile']
        units = unit('build/mut/tree')
    else:
        failed = golden('build/mut/tree/bin/curlyc.ts')
        units = 0
    if failed or units:
        print(f'{name}: golden {len(failed)} ({", ".join(f[:3] for f in failed[:6])}), unit {units}', flush=True)
    else:
        print(f'{name}: golden 0, unit 0   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
