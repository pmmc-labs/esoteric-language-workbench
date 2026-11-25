#!/usr/bin/env python3
"""Break step 9b's foreach and its freeze on purpose, one way at a time,
in the runtime and in each pass of the compiler, and see that a test goes
red each time.

    python3 docs/briefs/step9b-mutations.py            # all of them
    python3 docs/briefs/step9b-mutations.py "thaw"     # those named so
    python3 docs/briefs/step9b-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 9b, t/81*.pl to t/88*.pl, and 769 to 771,
           the refused ones too, run with the knobs of t/knobs.sh and
           each test's own `# env:`, as t/run.sh runs them. For a broken
           runtime each test's C is compiled once, by the compiler as it
           is, and linked again with the broken runtime; for a broken
           compiler each is compiled again by the copy
  unit     the runtime's own tests of the freeze and of a foreach, the
           two of runtime/tests/rt.test.ts that say so, in the copy

A record of step 9b, and not part of make test: each breakage is a piece
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
MUTATIONS = [
 # ---- the runtime: the freeze
 ("a frozen array may be changed", RT, FROZEN, ""),
 ("the freeze is no count", RT, "    array_of(cx, array)->frozen += 1;", "    array_of(cx, array)->frozen = 1;"),
 ("an array is never given back", RT, "    a->frozen -= 1;", ""),
 ("an array is given back all at once", RT, "    a->frozen -= 1;", "    a->frozen = 0;"),
 ("an array given back too often is not noticed", RT, '    if (a->frozen == 0) rt_internal(cx, "an array that no foreach is over was given back");\n', "    if (a->frozen == 0) return;\n"),
 ("assigning a frozen array", RT, "void rt_array_assign(rt_ctx *cx, rt_value array, rt_value list) {\n    rt_array *a = changing(cx, array);", "void rt_array_assign(rt_ctx *cx, rt_value array, rt_value list) {\n    rt_array *a = array_of(cx, array);"),
 ("a frozen array as the last target of a list assignment", RT, "void rt_array_rest(rt_ctx *cx, rt_value array, rt_value list, int64_t n) {\n    rt_array *a = changing(cx, array);", "void rt_array_rest(rt_ctx *cx, rt_value array, rt_value list, int64_t n) {\n    rt_array *a = array_of(cx, array);"),
 ("a store to a frozen array by an index from its end", RT, "        changing(cx, array);\n        return at;", "        return at;"),
 ("a store to a frozen array by an index from its start", RT, "    changing(cx, array);\n    if ((uint64_t)i >= ARRAY_MAX)", "    if ((uint64_t)i >= ARRAY_MAX)"),
 ("push on a frozen array", RT, "    changing(cx, array);\n    rt_list_add_all", "    rt_list_add_all"),
 ("unshift on a frozen array", RT, "rt_value rt_unshift(rt_ctx *cx, rt_value array, rt_value list) {\n    rt_array *a = changing(cx, array);", "rt_value rt_unshift(rt_ctx *cx, rt_value array, rt_value list) {\n    rt_array *a = array_of(cx, array);"),
 ("pop on a frozen array", RT, "rt_value rt_pop(rt_ctx *cx, rt_value array) {\n    rt_array *a = changing(cx, array);", "rt_value rt_pop(rt_ctx *cx, rt_value array) {\n    rt_array *a = array_of(cx, array);"),
 ("shift on a frozen array", RT, "rt_value rt_shift(rt_ctx *cx, rt_value array) {\n    rt_array *a = changing(cx, array);", "rt_value rt_shift(rt_ctx *cx, rt_value array) {\n    rt_array *a = array_of(cx, array);"),
 ("splice on a frozen array", RT, "    uint64_t came = in->count;\n    changing(cx, array);\n", "    uint64_t came = in->count;\n"),
 # ---- the runtime: a foreach's list and its range
 ("an element past the end in a foreach's list is undef", RT, '    if (at < 0) rt_fault(cx, "an element past the end of the array in a foreach, where perl would make it");\n    return a->items[at];', "    return at < 0 ? rt_undef() : a->items[at];"),
 ("a list is one shorter than it is", RT, "    return (int64_t)array_of(cx, list)->count;", "    return (int64_t)array_of(cx, list)->count - 1;"),
 ("a range near the smallest integer is walked", RT, "    if (*lo < INT64_MIN + 513 || *hi < INT64_MIN + 513) {", "    if (0) {"),
 ("the low edge of a range is one lower", RT, "    if (*lo < INT64_MIN + 513 || *hi < INT64_MIN + 513) {", "    if (*lo < INT64_MIN + 512 || *hi < INT64_MIN + 512) {"),
 ("the low edge of a range is one higher", RT, "    if (*lo < INT64_MIN + 513 || *hi < INT64_MIN + 513) {", "    if (*lo < INT64_MIN + 514 || *hi < INT64_MIN + 514) {"),
 ("a range's start is not held to the low edge", RT, "    if (*lo < INT64_MIN + 513 || *hi < INT64_MIN + 513) {", "    if (*hi < INT64_MIN + 513) {"),
 ("a range's end is not held to the low edge", RT, "    if (*lo < INT64_MIN + 513 || *hi < INT64_MIN + 513) {", "    if (*lo < INT64_MIN + 513) {"),
 ("a range that is backwards is walked", RT, "    return *lo <= *hi;", "    return 1;"),
 ("a range of one value is none", RT, "    return *lo <= *hi;", "    return *lo < *hi;"),
 ("a string may end a counted range", RT, '    if (to.tag == RT_TAG_STR) rt_fault(cx, "a string as the end of a range");\n    *hi = whole_of(cx, to);', "    *hi = whole_of(cx, to);"),
 ("a string may begin a counted range", RT, '    if (from.tag == RT_TAG_STR) rt_fault(cx, "a string as the end of a range");\n    *lo = whole_of(cx, from);', "    *lo = whole_of(cx, from);"),
 # ---- the code generator
 ("nothing is frozen", GEN, "                ...each.arrays.map(a => `rt_freeze(cx, ${slot(a)});`),\n", ""),
 ("nothing is given back when a loop ends", GEN, "                `last_${id}: RT_UNUSED;`,\n                ...thaws,\n", "                `last_${id}: RT_UNUSED;`,\n"),
 ("a jump to a loop further out gives nothing back", GEN, "        return [...out.open.slice(at + 1).reverse().flatMap(l => l.thaws), `goto", "        return [`goto"),
 ("a jump gives back what its own loop froze too", GEN, "        return [...out.open.slice(at + 1).reverse()", "        return [...out.open.slice(at).reverse()"),
 ("a return gives nothing back", GEN, "const leaving = (out: Out): string[] => [...out.open].reverse().flatMap(l => l.thaws);", "const leaving = (out: Out): string[] => [];"),
 ("a return gives back the nearest loop's alone", GEN, "const leaving = (out: Out): string[] => [...out.open].reverse().flatMap(l => l.thaws);", "const leaving = (out: Out): string[] => out.open.slice(-1).flatMap(l => l.thaws);"),
 ("a foreach's list is any list", GEN, "            const list = genList(s.items, b, 2);", "            const list = genList(s.items, b, 0);"),
 ("a foreach's list is a call's arguments", GEN, "            const list = genList(s.items, b, 2);", "            const list = genList(s.items, b, 1);"),
 ("an element in a branch of ? : is not held to its array", GEN, "    } else if (e.kind === 'ternary' && (listy(e) || strict === 2)) {", "    } else if (e.kind === 'ternary' && listy(e)) {"),
 ("an element on the right of || is not held to its array", GEN, "infixOp(e.op)?.when !== undefined && (listy(e) || strict === 2)) {", "infixOp(e.op)?.when !== undefined && listy(e)) {"),
 ("an element in a list repeated is not held to its array", GEN, "        const values = genList([e.left], b, strict === 2 ? 2 : 0);", "        const values = genList([e.left], b);"),
 ("a counted loop does not stop", GEN, "...(range ? [`if (at_${id} == end_${id}) break;`] : [])", "...[]"),
 ("a range is built as a list", GEN, "        const range = one !== undefined && one.kind === 'binary' && isRange(one) ? one : undefined;", "        const range = undefined as (Expr & { kind: 'binary' }) | undefined;"),
 # ---- the resolver
 ("the arrays a list names are not noted", RESOLVE, "        naming?.add(found.get('@' + name)!);\n", ""),
 ("the loop's variable is seen in its own list", RESOLVE, "            naming = new Set<number>();\n            whole(...s.items);\n            const arrays = naming;\n            naming = undefined;\n            scopes.push(new Map());\n",
  "            scopes.push(new Map());\n            of.set(s.var, names.length);\n            isArray.push(false);\n            names.push(s.var.name);\n            declare(s.var);\n            naming = new Set<number>();\n            whole(...s.items);\n            const arrays = naming;\n            naming = undefined;\n"),
 # ---- the checker
 ("a loop's variable may be changed", CHECK, "    checkReadOnly(program, names);\n", ""),
 ("the block may assign a scalar the list names", CHECK, "            for (const id of changesItself(w, e)) if (scalars.has(id)) refused(id, e);\n", ""),
 ("a sub the block calls may assign a scalar the list names", CHECK, "            if (e.kind === 'invoke') for (const id of w.changed[w.names.calls.get(e)!]!) if (scalars.has(id)) refused(id, e);\n", ""),
 ("a scalar is named only where it is an item", CHECK, "            parts(e).forEach(collect);\n", ""),
 ("a change inside an expression of the block is not seen", CHECK, "            parts(e).forEach(guard);\n        };\n        if (scalars.size > 0)", "        };\n        if (scalars.size > 0)"),
 ("a loop's list is not held to D76", CHECK, "        checkOrder(w, \"the loop's list\", s.items, true);\n", ""),
 ("a loop's list is not checked", CHECK, "        s.items.forEach(e => checkExpr(w, e, false, 'list'));\n        // perl walks", "        // perl walks"),
 ("what a sub changes inside a foreach is not counted", CHECK, "        case 'foreach':\n            s.items.forEach(e => expr(e, fn));\n            return s.body.forEach(b => stmt(b, fn));\n", ""),
 ("a foreach in the block is not looked into", CHECK, "    case 'foreach':\n        s.items.forEach(f);\n        return s.body.forEach(b => expressions(b, f));\n", ""),
 ("a loop of three parts in the block is not looked into", CHECK, "    case 'for':\n        [...s.first, ...(s.test ? [s.test] : []), ...s.each].forEach(f);\n        return s.body.forEach(b => expressions(b, f));\n", ""),
 ("a while in the block is not looked into", CHECK, "    case 'while':\n        f(s.test);\n        return s.body.forEach(b => expressions(b, f));\n", ""),
 ("an if in the block is not looked into", CHECK, "            f(arm.test);\n            arm.body.forEach(b => expressions(b, f));\n", ""),
 # ---- the parser
 ("a loop over nothing compiles", PARSE, "            if (peek().kind === ')') refuse(`${head.text} my $${v.name} () is a loop over nothing, and perl does not compile it`, paren.pos);\n", ""),
 ("foreach may have three parts", PARSE, "        if (name?.kind === 'for' && name.each) refuse('foreach is the loop over a list here, foreach my $x (...): the loop of three parts is spelled for', head.pos);\n", ""),
 ("a foreach loses its label", PARSE, "items, body, pos: head.pos, ...(label ? { label } : {}) };\n        }\n        if (open.kind !== '(') {", "items, body, pos: head.pos };\n        }\n        if (open.kind !== '(') {"),
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
for src in sorted(glob.glob('t/8[1-8]*.pl') + glob.glob('t/769-*.pl') + glob.glob('t/77[01]-*.pl')):
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
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'frozen|foreach', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
    if path == RT:
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
