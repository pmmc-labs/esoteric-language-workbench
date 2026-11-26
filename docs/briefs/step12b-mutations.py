#!/usr/bin/env python3
"""Break step 12b on purpose, one way at a time, in the runtime and in each
pass of the compiler, and see that a test goes red each time: the freeze
of a hash in a loop's list, slices read, stored and deleted, a hash as a
last parameter, and an element in a string.

    python3 docs/briefs/step12b-mutations.py            # all of them
    python3 docs/briefs/step12b-mutations.py "slice"    # those named so
    python3 docs/briefs/step12b-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 12b, t/1620*.pl to t/1759*.pl, and 1381 to
           1384 and 1568, the refused ones too, run with the knobs of
           t/knobs.sh and each test's own `# env:`, as t/run.sh runs them
  unit     the runtime's own tests of its hash table, in the copy

A record of step 12b, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
HASH = 'runtime/hash.c'
GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
CHECK = 'compiler/src/checker.ts'
PARSE = 'compiler/src/parser.ts'
LEX = 'compiler/src/lexer.ts'
SHAPES = 'compiler/src/shapes.ts'
NAMING = "        if (!quoted && !counted) naming.forEach(set => set.add(found.get('%' + name)!));"
MUTATIONS = [
 # ---- the runtime
 ("an element that is not there in a loop's list is undef", HASH, '    if (pair < 0) rt_fault(cx, "a key that is not there in a foreach, where perl would make it");', '    if (pair < 0) return rt_undef();'),
 ("a slice with a key that is not there is never a fault", HASH, "        if (pair < 0 && strict) rt_fault(", "        if (0) rt_fault("),
 ("a slice with a key that is not there is always a fault", HASH, "        if (pair < 0 && strict) rt_fault(", "        if (pair < 0) rt_fault("),
 ("a slice gives the keys", HASH, "        append(cx, to, pair < 0 ? rt_undef() : h->items[2 * pair + 1]);", "        append(cx, to, pair < 0 ? rt_undef() : h->items[2 * pair]);"),
 ("a slice stored to leaves what the list does not reach", HASH, "        rt_helem_store(cx, hash, ks->items[n], n < from->count ? from->items[n] : rt_undef());", "        if (n < from->count) rt_helem_store(cx, hash, ks->items[n], from->items[n]);"),
 ("a slice stored to takes the list's last value for what it does not reach", HASH, "        rt_helem_store(cx, hash, ks->items[n], n < from->count ? from->items[n] : rt_undef());", "        rt_helem_store(cx, hash, ks->items[n], n < from->count ? from->items[n] : from->count ? from->items[from->count - 1] : rt_undef());"),
 ("a slice deleted is only read", HASH, "        rt_value was = rt_hash_delete(cx, hash, ks->items[n]);", "        rt_value was = rt_helem(cx, hash, ks->items[n]);"),
 ("a slice deleted gives nothing back", HASH, "        append(cx, array_of(cx, list), was);", "        (void)was;"),
 ("a hash parameter takes values for keys", HASH, "        int64_t pair = hash_make(cx, hash, flat != NULL ? flat[n] : *argv[n]);\n        hash_of(cx, hash)->items[2 * pair + 1] = scalar(cx, flat != NULL ? flat[n + 1] : *argv[n + 1]);", "        int64_t pair = hash_make(cx, hash, flat != NULL ? flat[n + 1] : *argv[n + 1]);\n        hash_of(cx, hash)->items[2 * pair + 1] = scalar(cx, flat != NULL ? flat[n] : *argv[n]);"),
 ("a hash parameter takes the first pair alone", HASH, "    for (int64_t n = from; n + 1 < argc; n += 2) {", "    for (int64_t n = from; n + 1 < argc && n == from; n += 2) {"),
 ("an array's slice stored to leaves what the list does not reach", RT, "        rt_elem_store(cx, array, ix->items[n], n < from->count ? from->items[n] : rt_undef());", "        if (n < from->count) rt_elem_store(cx, array, ix->items[n], from->items[n]);"),
 ("an array's slice is stored last index first", RT, "    for (uint64_t n = 0; n < ix->count; n++) {\n        rt_elem_store(cx, array, ix->items[n], n < from->count ? from->items[n] : rt_undef());", "    for (uint64_t m = ix->count; m > 0; m--) {\n        uint64_t n = m - 1;\n        rt_elem_store(cx, array, ix->items[n], n < from->count ? from->items[n] : rt_undef());"),
 ("a frozen hash may be changed", HASH, 'if (h->frozen != 0) rt_fault(cx, "a hash was changed while a foreach is over it");', 'if (0) rt_fault(cx, "a hash was changed while a foreach is over it");'),
 # ---- the code generator
 ("an odd number of arguments for a hash is taken", GEN, "        ...(s.params.at(-1)?.hash ? [`", "        ...(false ? [`"),
 ("an odd number is counted over all the arguments", GEN, "(argc - ${s.params.length - 1}) % 2 != 0) rt_fault_odd_arguments", "argc % 2 != 0) rt_fault_odd_arguments"),
 ("a slice in a loop's list makes no fault", GEN, "rt_list_add_hslice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, ${strict ? 1 : 0});", "rt_list_add_hslice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, 0);"),
 ("a slice is always strict", GEN, "rt_list_add_hslice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, ${strict ? 1 : 0});", "rt_list_add_hslice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, 1);"),
 ("an element in a loop's list makes no fault", GEN, "        const value = temp(b, `${elem(e)}_strict(cx, ${variable(b, e)}, ${at.c})`);", "        const value = temp(b, `${e.hash ? 'rt_helem' : 'rt_elem_strict'}(cx, ${variable(b, e)}, ${at.c})`);"),
 ("a delete of a slice as a statement does nothing", GEN, "            addItem(e, temp(b, 'rt_array_new(cx)').c, b, 0);\n", ""),
 ("a hash's slice is stored as an array's", GEN, "${t.hash ? 'rt_hslice_store' : 'rt_slice_store'}", "${'rt_slice_store'}"),
 ("a hash parameter is filled before the parameters before it", GEN, "                    `${p.hash ? 'rt_slurp_hash' : 'rt_slurp'}(cx, ${rest}, argc, argv, flat, ${n});`);", "                    `${p.hash ? 'rt_slurp_hash' : 'rt_slurp'}(cx, ${rest}, argc, argv, flat, ${p.hash ? 0 : n});`);"),
 # ---- the resolver
 ("a hash in a loop's list is not frozen", RESOLVE, NAMING, "        if (false) naming.forEach(set => set.add(found.get('%' + name)!));"),
 ("keys freeze their hash", RESOLVE, NAMING, "        if (!quoted) naming.forEach(set => set.add(found.get('%' + name)!));"),
 ("a hash in a string in a loop's list is frozen", RESOLVE, NAMING, "        if (!counted) naming.forEach(set => set.add(found.get('%' + name)!));"),
 ("the keys of a delete are not looked up", RESOLVE, "            e.keys?.forEach(x => walk(x, declared));\n", ""),
 ("a hash parameter is an array", RESOLVE, "                isHash.push(p.rest.hash === true);", "                isHash.push(false);"),
 # ---- the checker
 ("a slice of a hash by one key is taken", CHECK, "    if (e.kind !== 'slice' || e.name === undefined || e.indexes.length !== 1) return;", "    if (e.kind !== 'slice' || e.name === undefined || e.hash || e.indexes.length !== 1) return;"),
 ("a slice of one on the left is taken", CHECK, "            if (t.kind === 'slice' && t.name !== undefined && e.targets.length === 1 && !e.my) {\n                checkSliceOfOne(t);\n                return;", "            if (t.kind === 'slice' && t.name !== undefined && e.targets.length === 1 && !e.my) {\n                return;"),
 ("a delete of a slice of one is taken", CHECK, "        checkSliceOfOne({ kind: 'slice', name: e.name, hash: true, indexes: e.keys, pos: e.at });\n", ""),
 ("a delete of a slice may be one value", CHECK, "    if (e.kind === 'hashop' && e.keys !== undefined) refuse('delete of a slice where one value is wanted", "    if (false) refuse('delete of a slice where one value is wanted"),
 ("a slice may be one target among others", CHECK, "            if (t.kind === 'slice' && t.name !== undefined && e.targets.length === 1 && !e.my) {", "            if (t.kind === 'slice' && t.name !== undefined && !e.my) {"),
 ("a slice's keys on the left are no part of D76", CHECK, "(t.kind === 'elem' ? [t.index] : t.kind === 'slice' ? t.indexes : []));", "(t.kind === 'elem' ? [t.index] : []));"),
 ("a slice's keys on the left are not checked", CHECK, "            if (part.kind === 'slice') part.indexes.forEach(x => checkExpr(w, x, false, 'list'));\n", ""),
 ("the keys of a delete are in no order", CHECK, "        checkOrder(w, 'delete', e.keys, true);\n", ""),
 ("the keys of a delete are no part of it", CHECK, "    : e.kind === 'hashop' ? (e.keys ?? (e.key === undefined ? [] : [e.key]))", "    : e.kind === 'hashop' ? (e.key === undefined ? [] : [e.key])"),
 ("a delete of a slice is one value to a return", SHAPES, "    case 'hashop': return e.op === 'keys' || e.op === 'values' || e.keys !== undefined;", "    case 'hashop': return e.op === 'keys' || e.op === 'values';"),
 # ---- the parser
 ("a blank before a slice's brace is read on", PARSE, "            if (brace.kind === '{') refuse(`a blank between @${t.name} and '{': a slice of a hash is written @${t.name}{...}`, brace.pos);\n", ""),
 ("a slice with no key is read on", PARSE, "        if (keys.length === 0) refuse('a slice with no key: perl refuses it', open.pos);\n", ""),
 ("a slice takes any assigning operator", PARSE, "                if (slice && t.text !== '=') refuse(", "                if (false) refuse("),
 ("a delete of a slice takes what binds tighter", PARSE, "                else bareOperand(head, `delete @${slice.name}{...}`);\n", ""),
 ("exists takes a slice", PARSE, "            if (op === 'delete' && what.kind === 'array' && brace.kind === '{' && brace.subscript === true) {", "            if (what.kind === 'array' && brace.kind === '{' && brace.subscript === true) {"),
 ("a hash parameter may stand anywhere", PARSE, "refuse('a slurpy parameter has no default: perl refuses one', after.pos);\n                    if (after.kind !== ')') refuse(`${v.text} takes every argument that is left, so it is the last parameter: perl refuses one after it`, after.pos);\n                    params.push(v.name === '' ? { slurpy: true, hash: true", "refuse('a slurpy parameter has no default: perl refuses one', after.pos);\n                    params.push(v.name === '' ? { slurpy: true, hash: true"),
 ("a hash parameter may have a default", PARSE, "                if (v.kind === 'hash') {\n                    const after = peek();\n                    if (after.kind === 'op' && (after.text === '=' || after.text === '//=' || after.text === '||=')) refuse('a slurpy parameter has no default: perl refuses one', after.pos);", "                if (v.kind === 'hash') {\n                    const after = peek();"),
 # ---- the lexer
 ("a number is a key in a string", LEX, "                if (!isWordStart(at())) refuse(KEY, keyAt);\n                key = { kind: 'word', text: run(isWord) };", "                if (!isWord(at())) refuse(KEY, keyAt);\n                key = { kind: 'word', text: run(isWord) };"),
 ("blanks are taken round a key in a string", LEX, "            take();\n            const keyAt = pos();", "            take();\n            while (at() === ' ') take();\n            const keyAt = pos();"),
 ("'::' after an element in a string is refused", LEX, "        if (src.startsWith('::', i) && piece.kind !== 'helem') refuse(", "        if (src.startsWith('::', i)) refuse("),
 ("a brace after an element in a string is text", LEX, "        if (at() === '{') {\n            refuse(piece.kind === 'array'", "        if (at() === '{' && piece.kind !== 'helem') {\n            refuse(piece.kind === 'array'"),
 ("a square bracket after an element in a string is text", LEX, "        if (at() === '[') refuse(`'[' hard after ${shown} in a string: another index", "        if (at() === '[' && piece.kind !== 'helem') refuse(`'[' hard after ${shown} in a string: another index"),
 ("an arrow after an element in a string is text", LEX, "        if (src.startsWith('->', i) && then !== '' && '[{@$'.includes(then)) {", "        if (src.startsWith('->', i) && then !== '' && '[{@$'.includes(then) && piece.kind !== 'helem') {"),
 ("a slice of a hash in a string is the array and text", LEX, "        if (at() === '{') {\n            refuse(piece.kind === 'array'", "        if (at() === '{' && piece.kind !== 'array') {\n            refuse(piece.kind === 'array'"),
 ("a % alone is a hash anywhere", LEX, "            if (signature > 0 && !isWordStart(at()) && at() !== '$' && at() !== '{') {", "            if (!isWordStart(at()) && at() !== '$' && at() !== '{') {"),
 ("a brace after an array is a block's", LEX, "            if (c === '{' && (name?.kind === 'var' || name?.kind === 'array') && lastEnd === i) {", "            if (c === '{' && name?.kind === 'var' && lastEnd === i) {"),
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
for src in sorted(glob.glob('t/16[2-9][0-9]-*.pl') + glob.glob('t/17[0-6][0-9]-*.pl') + glob.glob('t/138[1-4]-*.pl') + glob.glob('t/1568-*.pl')):
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
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'hash', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
    if path in (RT, HASH):
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
