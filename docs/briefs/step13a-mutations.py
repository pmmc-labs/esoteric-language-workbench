#!/usr/bin/env python3
"""Break step 13a on purpose, one way at a time, in the runtime and in each
pass of the compiler, and see that a test goes red each time: references,
elements through them read and stored, what a store makes, the freeze
through a reference, a reference as a value, the collector's walk, and
the walks over names that know what references reach (D109, D114).

    python3 docs/briefs/step13a-mutations.py            # all of them
    python3 docs/briefs/step13a-mutations.py "freeze"   # those named so
    python3 docs/briefs/step13a-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 13a, t/1810*.pl to t/1999*.pl, the refused
           ones too, and 474 and 1557 to 1559, run with the knobs of
           t/knobs.sh and each test's own `# env:`, as t/run.sh runs them
  unit     the runtime's own tests of references, in the copy

A record of step 13a, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
REF = 'runtime/ref.c'
GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
CHECK = 'compiler/src/checker.ts'
PARSE = 'compiler/src/parser.ts'
LEX = 'compiler/src/lexer.ts'
MUTATIONS = [
 # ---- the runtime
 ("reading through undef gives undef", REF, "    if (v.tag == RT_TAG_UNDEF) rt_fault(cx, UNDEF_REFERENCE);\n    if (v.tag != (hash", "    if (v.tag == RT_TAG_UNDEF) return rt_undef();\n    if (v.tag != (hash"),
 ("reading through the other kind is allowed", REF, "    if (v.tag != (hash ? RT_TAG_HREF : RT_TAG_AREF)) {", "    if (v.tag != RT_TAG_HREF && v.tag != RT_TAG_AREF) {"),
 ("the two faults are one", REF, "        rt_fault(cx, hash ? NOT_HASH : NOT_ARRAY);", "        rt_fault(cx, NOT_ARRAY);"),
 ("a variable stored through is never made", REF, "    if (slot->tag != RT_TAG_UNDEF) return rt_deref(cx, *slot, hash);", "    return rt_deref(cx, *slot, hash);"),
 ("a variable made is not given the reference", REF, "    *slot = reference_to(c);\n", ""),
 ("a hop is made of the kind that holds it", REF, "    rt_value c = made_container(cx, hash);\n    rt_elem_put(", "    rt_value c = made_container(cx, 0);\n    rt_elem_put("),
 ("a hop is made but not stored", REF, "    rt_elem_put(cx, array, at, reference_to(c));\n", ""),
 ("a hop through a key is always made anew", REF, "    rt_value v = rt_helem(cx, h, key);\n    if (v.tag != RT_TAG_UNDEF) return rt_deref(cx, v, hash);", "    rt_value v = rt_undef();"),
 ("a hop is made without the freeze", REF, "    int64_t at = rt_elem_make(cx, array, index);", "    uint64_t was = array_of(cx, array)->frozen;\n    array_of(cx, array)->frozen = 0;\n    int64_t at = rt_elem_make(cx, array, index);\n    array_of(cx, array)->frozen = was;"),
 ("ref of a hash is ARRAY", REF, "    if (v.tag == RT_TAG_HREF) return rt_string(&STR_HASH);", "    if (v.tag == RT_TAG_HREF) return rt_string(&STR_ARRAY);"),
 ("ref of a number is the number", REF, "    if (!a_scalar(v.tag)) rt_fault(cx, \"not a value\");\n    return rt_string(&STR_FALSE);", "    if (!a_scalar(v.tag)) rt_fault(cx, \"not a value\");\n    return v.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : v;"),
 ("the frozen are never frozen", REF, "    for (uint64_t n = 0; n < a->count; n++) rt_freeze(cx, a->items[n]);", "    (void)a;"),
 ("the frozen are never given back", REF, "    for (uint64_t n = 0; n < a->count; n++) rt_thaw(cx, a->items[n]);", "    (void)a;"),
 ("the frozen are not kept", REF, "    append(cx, array_of(cx, frozen), c);", "    (void)frozen;"),
 ("a reference is false", RT, "    case RT_TAG_AREF: case RT_TAG_HREF: return 1;\n    default: rt_fault(cx, \"not a value\");", "    case RT_TAG_AREF: case RT_TAG_HREF: return 0;\n    default: rt_fault(cx, \"not a value\");"),
 ("a reference is undef", RT, "int rt_is_undef(rt_ctx *cx, rt_value v) {\n    if (!a_scalar(v.tag)) rt_fault(cx, \"not a value\");\n    return v.tag == RT_TAG_UNDEF;", "int rt_is_undef(rt_ctx *cx, rt_value v) {\n    if (!a_scalar(v.tag)) rt_fault(cx, \"not a value\");\n    return v.tag == RT_TAG_UNDEF || v.tag == RT_TAG_AREF || v.tag == RT_TAG_HREF;"),
 ("a reference is a number, its address", RT, "    case RT_TAG_AREF: case RT_TAG_HREF:\n        rt_fault(cx, \"a reference where a number is wanted\");", "    case RT_TAG_AREF: case RT_TAG_HREF:\n        x.is_int = 1;\n        x.plain = 1;\n        x.i = (int64_t)(uintptr_t)v.as.a;\n        return x;"),
 ("a reference is a string, empty", RT, "    if (v.tag == RT_TAG_AREF || v.tag == RT_TAG_HREF) rt_fault(cx, \"a reference where a string is wanted\");", "    if (v.tag == RT_TAG_AREF || v.tag == RT_TAG_HREF) return &STR_FALSE;"),
 ("== between two references compares nothing", RT, "    if (is_ref(a) && is_ref(b)) return rt_bool(a.as.a == b.as.a);", "    if (is_ref(a) && is_ref(b)) return rt_bool(1);"),
 ("!= between two references is ==", RT, "    if (is_ref(a) && is_ref(b)) return rt_bool(a.as.a != b.as.a);", "    if (is_ref(a) && is_ref(b)) return rt_bool(a.as.a == b.as.a);"),
 ("an array holds no reference", RT, "    return (tag >= RT_TAG_INT && tag <= RT_TAG_BOOL) || tag == RT_TAG_AREF || tag == RT_TAG_HREF;", "    return tag >= RT_TAG_INT && tag <= RT_TAG_BOOL;"),
 ("the collector does not walk into a container", RT, "        for (uint64_t n = 0; n < a->count; n++) mark(cx, a->items[n]);\n    }", "        (void)a;\n    }"),
 ("the collector does not follow a reference", RT, "    case RT_TAG_ARRAY: case RT_TAG_HASH: case RT_TAG_AREF: case RT_TAG_HREF:\n        mark_container(cx, v.as.a);", "    case RT_TAG_ARRAY: case RT_TAG_HASH:\n        mark_container(cx, v.as.a);"),
 ("the collector walks only from the frames", RT, "    while (cx->marking > 0) {", "    while (0) {"),
 # ---- the code generator
 ("a store through a variable never makes it", GEN, "        if (store && base.kind === 'var' && !b.names.readonly.has(id!)) {", "        if (false) {"),
 ("a store through a read-only variable makes it", GEN, "        if (store && base.kind === 'var' && !b.names.readonly.has(id!)) {", "        if (store && base.kind === 'var') {"),
 ("a store through a call makes it, nowhere", GEN, "        if (store && base.kind === 'var' && !b.names.readonly.has(id!)) {", "        if (store && base.kind !== 'var') {\n            container = kept(temp(b, `rt_vivify(cx, &${pointTo(b, genExpr(base, b))}, ${wanted})`).c);\n        } else if (store && base.kind === 'var' && !b.names.readonly.has(id!)) {"),
 ("a hop of a store is only read", GEN, "        if (store) {\n            container = kept(temp(b, `${read}_hop(", "        if (false) {\n            container = kept(temp(b, `${read}_hop("),
 ("a hop is read as the next subscript's kind", GEN, "        const read = subs[k]!.hash ? 'rt_helem' : 'rt_elem';", "        const read = subs[k + 1]!.hash ? 'rt_helem' : 'rt_elem';"),
 ("a named array's element starts no chain", GEN, "        container = variable(b, base);\n        subs.unshift({ index: base.index, hash: base.hash === true });", "        container = variable(b, base);"),
 ("the containers of a loop's list are not kept", GEN, "        if (b.frozen !== undefined) b.lines.push(`rt_frozen_add(cx, ${b.frozen}, ${c});`);", "        if (false) b.lines.push(`rt_frozen_add(cx, ${b.frozen}, ${c});`);"),
 ("an element through a reference in a loop's list is not strict", GEN, "        const value = temp(b, `${elem(e)}_strict(cx, ${container}, ${at.c})`);", "        const value = temp(b, `${elem(e)}(cx, ${container}, ${at.c})`);"),
 ("a new hash is an array", GEN, "        if (!e.hash) return temp(b, `rt_aref(cx, ${values.c})`);", "        return temp(b, `rt_aref(cx, ${values.c})`);"),
 ("a new array is the list made again each time it is read", GEN, "        const values = genList(e.items, b);\n        if (!e.hash)", "        const values = genList(e.items.slice(0, 1), b);\n        if (!e.hash)"),
 ("=: the chain before the right side", GEN, "                const value = genExpr(e.value, b);\n                const { array, last } = where();", "                const { array, last } = where();\n                const value = genExpr(e.value, b);"),
 ("exists through a reference is delete", GEN, "            return temp(b, `rt_hash_${e.op}(cx, ${container}, ${key.c})`);", "            return temp(b, `rt_hash_delete(cx, ${container}, ${key.c})`);"),
 ("a list assignment's chain is read, not made", GEN, "                const { container, last } = genChain(t, b, true);\n                containers[n] = container;", "                const { container, last } = genChain(t, b, false);\n                containers[n] = container;"),
 ("a map's list freezes what its block reads through", GEN, "    // (What the block works out freezes nothing of this list's.)\n    b.frozen = undefined;", "    b.frozen = b.frozen;"),
 # ---- the resolver
 ("a chain in a loop's list freezes nothing", RESOLVE, "            if (!quoted) chains.fill(true);", "            if (false) chains.fill(true);"),
 ("a reference taken counts for nothing", RESOLVE, "            taken.add(of.get(e.of)!);\n", ""),
 ("a reference to an array freezes it in a loop's list", RESOLVE, "            array(e.of, e.of.name, true);", "            array(e.of, e.of.name);"),
 ("a chain's head is not looked up", RESOLVE, "        case 'chain':\n            walk(e.head, declared);", "        case 'chain':"),
 # ---- the checker
 ("a read through a reference names nothing", CHECK, "    if (e.kind === 'chain') chain(e);\n", ""),
 ("a read through a reference names only its head", CHECK, "    const chain = (c: Chain): void => {\n        into.add(REACH);", "    const chain = (c: Chain): void => {"),
 ("a read through a reference names only what references reach", CHECK, "        if (base.kind === 'var' || base.kind === 'elem') id(base);\n        else named(w, base, true, into);", "        void base;"),
 ("a store through a reference changes nothing", CHECK, "    if ((e.kind === 'assign' || e.kind === 'step') && e.target.kind === 'chain') return direct ? [] : [REACH, ...making(w, e.target)];", "    if ((e.kind === 'assign' || e.kind === 'step') && e.target.kind === 'chain') return [];"),
 ("a store through a reference does not change its head", CHECK, "    if ((e.kind === 'assign' || e.kind === 'step') && e.target.kind === 'chain') return direct ? [] : [REACH, ...making(w, e.target)];", "    if ((e.kind === 'assign' || e.kind === 'step') && e.target.kind === 'chain') return direct ? [] : [REACH];"),
 ("a delete through a reference changes nothing", CHECK, "    if (e.kind === 'hashop' && e.op === 'delete' && e.chain !== undefined) return direct ? [] : [REACH];", "    if (e.kind === 'hashop' && e.op === 'delete' && e.chain !== undefined) return [];"),
 ("a reference taken is no second name", CHECK, "    into.add(id);\n    if (w.names.taken.has(id)) into.add(REACH);", "    into.add(id);"),
 ("a sub that stores through a reference changes nothing a caller sees", CHECK, "            if (id === REACH || names.owner[id] === 0) own[fn]!.add(id);", "            if (names.owner[id] === 0) own[fn]!.add(id);"),
 ("a store through a loop's variable is a store to it", CHECK, "        for (const id of changesItself(w, e, true)) {\n            if (variables.has(id)) refuse(", "        for (const id of [...changesItself(w, e, true), ...((e.kind === 'assign' || e.kind === 'step') && e.target.kind === 'chain' ? [...making(w, e.target)] : [])]) {\n            if (variables.has(id)) refuse("),
 ("making a hop is never checked against the right side", CHECK, "            if (e.target.kind === 'chain') checkMaking(w, e.target, e.value, false);\n", ""),
 ("a list assignment's making is not checked", CHECK, "        e.targets.forEach(t => { if (t.kind === 'chain') checkMaking(w, t, e.value, true); });\n", ""),
 ("T230's rule looks at the last index alone", CHECK, "        const index = e.target.kind === 'chain' ? chainParts(e.target) : [e.target.index];", "        const index = [e.target.index];"),
 ("a concatenation's pieces through a reference read nothing", CHECK, "        variables(piece).forEach(v => (v.kind === 'chain' ? readIds.add(REACH) : addId(w, readIds, w.names.of.get(v)!)));", "        variables(piece).forEach(v => (v.kind === 'chain' ? undefined : addId(w, readIds, w.names.of.get(v)!)));"),
 ("a new container folds to a constant", CHECK, "    : e.kind === 'chain' || e.kind === 'anon' || e.kind === 'ref' ? false\n", ""),
 # ---- the parser
 ("ref of a concatenation is taken", PARSE, "            if (head.text === 'ref' && arg.kind === 'binary' && !arg.bracketed) {", "            if (false) {"),
 ("a brace first after say is a hash", PARSE, "        if (open.kind === '{') refuse(`'{' first after ${head.text}:", "        if (false) refuse(`'{' first after ${head.text}:"),
 ("a block of a word and a comma is a block", PARSE, "            if ((first.kind === 'str' || first.kind === 'int' || first.kind === 'num' || first.kind === 'word') && second?.kind === ',') {", "            if (false) {"),
 ("a blank between subscripts is read on", PARSE, "                if (!touching(i - 1)) refuse(\"a blank between two subscripts", "                if (false) refuse(\"a blank between two subscripts"),
 ("a reference to an element is a reference to its array", PARSE, "            if ((what.kind === 'array' || what.kind === 'hash') && !subscripted) {", "            if (what.kind === 'array' || what.kind === 'hash') {"),
 ("exists through an array's element is taken", PARSE, "            } else if (element?.kind === 'chain' && element.hash) {", "            } else if (element?.kind === 'chain') {"),
 # ---- the lexer
 ("a brace after an arrow is a block's", LEX, "                || (name?.kind === 'op' && name.text === '->');\n", ";\n"),
 ("a brace after a key's is a block's", LEX, "|| (name?.kind === '}' && name.subscript === true)\n", "\n"),
 ("a brace where a value may begin is a block", LEX, "        if (last.kind === 'op' || last.kind === '(' || last.kind === '[' || last.kind === ',' || last.kind === '?' || last.kind === ':') return true;", "        if (last.kind === '(' || last.kind === '[') return true;"),
 ("a new hash ends no value", LEX, "            || (last?.kind === '}' && (last.subscript === true || last.anon === true))", "            || (last?.kind === '}' && last.subscript === true)"),
 ("$$r is $r", LEX, "            if (at() === '$' && (isWordStart(src[i + 1] ?? '') || src[i + 1] === '{')) {\n                refuse(", "            if (at() === '$' && (isWordStart(src[i + 1] ?? '') || src[i + 1] === '{')) {\n                take();\n            }\n            if (false) {\n                refuse("),
 ("an arrow before a name is taken", LEX, "                if (isWordStart(next) || next === '$') refuse(\"'->' and a name", "                if (next === '$') refuse(\"'->' and a name"),
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
for src in sorted(glob.glob('t/18[1-9][0-9]-*.pl') + glob.glob('t/19[0-9][0-9]-*.pl') + glob.glob('t/474-*.pl') + glob.glob('t/155[7-9]-*.pl')):
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
    with ThreadPoolExecutor(4) as pool:
        return [t[0] for t, ok in zip(which, pool.map(lambda t: passes(t, driver), which)) if not ok]

def unit(tree):
    """How many of the runtime's own tests of references fail, in the copy."""
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'reference|arrow|hop|walks a chain', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
    if path in (RT, REF):
        failed = golden(None) if runtime() else ['the runtime does not compile']
        units = unit('build/mut/tree')
    else:
        failed = golden('build/mut/tree/bin/curlyc.ts')
        units = 0
    if failed or units:
        print(f'{name}: golden {len(failed)} ({", ".join(f[:4] for f in failed[:6])}), unit {units}', flush=True)
    else:
        print(f'{name}: golden 0, unit 0   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
