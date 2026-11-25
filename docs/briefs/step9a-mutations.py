#!/usr/bin/env python3
"""Break step 9a's arrays and lists on purpose, one way at a time, in the
runtime and in each pass of the compiler, and see that a test goes red
each time.

    python3 docs/briefs/step9a-mutations.py            # all of them
    python3 docs/briefs/step9a-mutations.py "splice"   # those named so
    python3 docs/briefs/step9a-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 9a, t/41*.pl to t/49*.pl, and 580 and 903, the
           refused ones too, run with the knobs of t/knobs.sh and each
           test's own `# env:`, as t/run.sh runs them. For a broken
           runtime each test's C is compiled once, by the compiler as it
           is, and linked again with the broken runtime; for a broken
           compiler each is compiled again by the copy
  unit     the runtime's own tests of arrays, the four of
           runtime/tests/rt.test.ts that say so, in the copy

A record of step 9a, and not part of make test: each breakage is a piece
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
LEX = 'compiler/src/lexer.ts'
MUTATIONS = [
 # ---- the runtime: the collector
 ("an array's values are not marked", RT, "                for (uint64_t n = 0; n < a->count; n++) mark_string(cx, a->items[n]);\n", ""),
 ("an array is not marked", RT, "                ((rt_block *)a - 1)->marked |= REACHED;\n", ""),
 ("an array that was collected is not seen to be", RT, "    if (v.as.a->dead) rt_internal(cx, \"an array was used after it was collected\");\n", ""),
 ("an array's storage is not counted", RT, "    cx->held += more;\n    cx->since += more;", "    cx->since += more;"),
 ("storage that was freed is still held", RT, "            cx->held -= storage(a);\n", ""),
 # ---- the runtime: lists
 ("what is absent is added to a list", RT, "    if (v.tag == RT_TAG_ABSENT) return;\n", ""),
 ("a range is one short", RT, "    uint64_t count = (uint64_t)hi - (uint64_t)lo + 1;", "    uint64_t count = (uint64_t)hi - (uint64_t)lo;"),
 ("a string may begin a range", RT, "    if (from.tag == RT_TAG_STR) rt_fault(cx, \"a string as the end of a range\");\n", ""),
 ("a string may end a range", RT, "    if (to.tag == RT_TAG_STR) rt_fault(cx, \"a string as the end of a range\");\n", ""),
 ("a range backwards is built", RT, "    if (lo > hi) return;\n", "    if (lo > hi) { int64_t t = lo; lo = hi; hi = t; }\n"),
 ("an index at the count is in the array", RT, "    if (i >= 0) return (uint64_t)i < count ? i : -1;", "    if (i >= 0) return (uint64_t)i <= count ? i : -1;"),
 ("a negative index is one too far", RT, "? (int64_t)(count - (uint64_t)(-(i + 1)) - 1) : -1;", "? (int64_t)(count - (uint64_t)(-(i + 1)) - 1) - ((uint64_t)(-(i + 1)) + 1 < count) : -1;"),
 ("a slice of a list with no values is undefs", RT, "        if (how == 1 && a->count == 0) continue;\n", ""),
 ("a slice past the end among arguments is let through", RT, "        if (how == 2 && at < 0) rt_fault(cx, \"a slice past the end of the array, where perl would make the elements\");\n", ""),
 ("a list repeated a negative number of times is none", RT, "    if (below_zero(c)) rt_fault(cx, \"negative repeat count\");\n    uint64_t times", "    if (below_zero(c)) return;\n    uint64_t times"),
 ("a store before the start is at the start", RT, "        if (at < 0) rt_fault(cx, \"an element before the start of the array\");\n        return at;", "        if (at < 0) return 0;\n        return at;"),
 ("the gap a store leaves is not undef", RT, "        while (a->count <= (uint64_t)i) a->items[a->count++] = rt_undef();", "        while (a->count <= (uint64_t)i) a->items[a->count++] = rt_int(0);"),
 ("pop from an empty array is 0", RT, "    return a->count == 0 ? rt_undef() : a->items[--a->count];", "    return a->count == 0 ? rt_int(0) : a->items[--a->count];"),
 ("shift from an empty array is 0", RT, "    if (a->count == 0) return rt_undef();\n    rt_value first", "    if (a->count == 0) return rt_int(0);\n    rt_value first"),
 ("unshift adds at the end", RT, "    shift_values(a, more, 0, a->count);\n    for (uint64_t n = 0; n < more; n++) a->items[n] = from->items[n];", "    for (uint64_t n = 0; n < more; n++) a->items[a->count + n] = from->items[n];"),
 ("splice past the end is at the end", RT, "        if ((uint64_t)o > count) rt_fault(cx, \"splice past the end of the array\");\n        start = (uint64_t)o;", "        start = (uint64_t)o > count ? count : (uint64_t)o;"),
 ("splice before the start is at the start", RT, "        if ((uint64_t)(-(o + 1)) >= count) rt_fault(cx, \"splice before the start of the array\");\n        start = count - (uint64_t)(-(o + 1)) - 1;", "        start = (uint64_t)(-(o + 1)) >= count ? 0 : count - (uint64_t)(-(o + 1)) - 1;"),
 ("a negative length removes to the end", RT, "        end = left < count - start ? count - left : start;", "        end = count;"),
 ("a length past the end is not cut to it", RT, "        end = (uint64_t)l < count - start ? start + (uint64_t)l : count;", "        end = (uint64_t)l < count ? start + (uint64_t)l : count;"),
 ("splice gives nothing back", RT, "    for (uint64_t n = start; n < end; n++) append(cx, out, a->items[n]);\n", ""),
 ("splice's length is not asked for its fault", RT, "    int64_t l = given > 1 ? whole_of(cx, length) : 0;", "    int64_t l = given > 1 && length.tag == RT_TAG_INT ? length.as.i : given > 1 ? INT64_MAX : 0;"),
 ("say of a list writes each value as it looks at it", RT, "    for (uint64_t n = 0; n < a->count; n++) emit_checked(cx, a->items[n], 0, 0);\n", ""),
 ("a target past the last value is 0", RT, "    return (uint64_t)n < a->count ? a->items[n] : rt_undef();", "    return (uint64_t)n < a->count ? a->items[n] : rt_int(0);"),
 ("an array among the targets takes every value", RT, "    for (uint64_t k = 0; k < count; k++) a->items[k] = from->items[(uint64_t)n + k];", "    for (uint64_t k = 0; k < count; k++) a->items[k] = from->items[k];"),
 ("the first of a list with no values is 0", RT, "    return a->count == 0 ? rt_undef() : a->items[0];", "    return a->count == 0 ? rt_int(0) : a->items[0];"),
 ("the last index is the count", RT, "    return rt_int((int64_t)array_of(cx, array)->count - 1);", "    return rt_int((int64_t)array_of(cx, array)->count);"),
 # ---- the code generator
 ("= works out its index before its right side", GEN, "                const value = genExpr(e.value, b);\n                const at = genExpr(e.target.index, b);\n                return temp(b, `rt_elem_store", "                const at = genExpr(e.target.index, b);\n                const value = genExpr(e.value, b);\n                return temp(b, `rt_elem_store"),
 ("a list assignment's index is read at its store", GEN, "        const kept = (v: C): C => (v.place ? temp(b, v.c) : v);", "        const kept = (v: C): C => v;"),
 ("a slice of a list works its list out before its indexes", GEN, "        const indexes = genList(e.indexes, b);\n        if (e.name !== undefined) {\n            b.lines.push(`rt_list_add_slice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, ${strict ? 2 : 0});`);\n        } else {\n            const from = genList(e.items!, b);",
  "        const early = e.name === undefined ? genList(e.items!, b) : undefined;\n        const indexes = genList(e.indexes, b);\n        if (e.name !== undefined) {\n            b.lines.push(`rt_list_add_slice(cx, ${list}, ${variable(b, e)}, ${indexes.c}, ${strict ? 2 : 0});`);\n        } else {\n            const from = early!;"),
 ("a slice among a call's arguments is not held to its array's ends", GEN, "            const values = genList(e.args, b, true);", "            const values = genList(e.args, b, false);"),
 ("an argument that is absent is handed over", GEN, "            where.forEach(p => b.lines.push(`if ((${p})->tag != RT_TAG_ABSENT) av${n}[ac${n}++] = ${p};`));", "            where.forEach(p => b.lines.push(`av${n}[ac${n}++] = ${p};`));"),
 ("return alone gives a list an undef", GEN, "'r = want == RT_LIST ? rt_absent() : rt_undef();', 'goto done;'", "'r = rt_undef();', 'goto done;'"),
 ("an empty body gives a list an undef", GEN, "        lines.push('if (want == RT_LIST) r = rt_absent();');\n", ""),
 ("a file's array is made again at its my", GEN, "        if (!isFile(b, e)) b.vars.push(`${variable(b, e)} = rt_array_new(cx); // my @${e.name}`);", "        b.vars.push(`${variable(b, e)} = rt_array_new(cx); // my @${e.name}`);"),
 ("an array in a block is not made new", GEN, "        if (!isFile(b, e)) b.vars.push(`${variable(b, e)} = rt_array_new(cx); // my @${e.name}`);", "        if (false) b.vars.push(`${variable(b, e)} = rt_array_new(cx); // my @${e.name}`);"),
 ("the left of || in a list is not kept", GEN, "        b.lines.push('} else {', `rt_list_add(cx, ${list}, ${kept.c});`, '}');", "        b.lines.push('}');"),
 ("an array where one value is wanted is its last index", GEN, "    case 'array': return temp(b, `rt_count(cx, ${variable(b, e)})`);", "    case 'array': return temp(b, `rt_last_index(cx, ${variable(b, e)})`);"),
 ("a step on an element gives what it holds after, whichever side it is on", GEN, "            return e.before ? now : was;", "            return now;"),
 ("||= on an element stores whatever it held", GEN, "                b.lines.push(`if (${op.when}(cx, ${was.c})) {`);\n                b.lines.push(`rt_elem_put", "                b.lines.push(`if (1) {`);\n                b.lines.push(`rt_elem_put"),
 # ---- the checker
 ("a later part may change what an earlier part names", CHECK, "            for (const id of changeSet(w, part)) if (seen.has(id)) refused(id, part);\n", ""),
 ("a sub's defaults are not looked at for what its arguments name", CHECK, "    if (also) for (const id of also.changes) if (seen.has(id)) refused(id, also.at);\n", ""),
 ("a variable that is an item of a list is not named", CHECK, "    else if (e.kind === 'var' && scalars) id(e);\n", ""),
 ("an array in a list is not named", CHECK, "    if (e.kind === 'elem' || e.kind === 'array' || e.kind === 'lastindex') id(e);", "    if (e.kind === 'elem' || e.kind === 'lastindex') id(e);"),
 ("an element is not named", CHECK, "    if (e.kind === 'elem' || e.kind === 'array' || e.kind === 'lastindex') id(e);", "    if (e.kind === 'array' || e.kind === 'lastindex') id(e);"),
 ("what a sub changes is not what calling it changes", CHECK, "    if (e.kind === 'invoke') w.changed[w.names.calls.get(e)!]!.forEach(id => into.add(id));\n    parts(e).forEach(p => changeSet(w, p, into));", "    parts(e).forEach(p => changeSet(w, p, into));"),
 ("push and its kin change nothing", CHECK, "    if (e.kind === 'arrayop' && e.op !== 'scalar') return [id(e)];\n", ""),
 ("a list where one value is wanted is let through", CHECK, "    if (ctx === 'scalar') checkOneValue(e);\n", ""),
 ("an assignment of a list is a value", CHECK, "&& !root) {\n        refuse('an assignment of a list is a statement", "&& false) {\n        refuse('an assignment of a list is a statement"),
 ("a list may follow return", CHECK, "        return checkNoList(s.value, 'after return');", "        return;"),
 ("a slice with one index is let through", CHECK, "        if (!listy(one) && one.kind !== 'invoke' && !one.bracketed) refuse(", "        if (false) refuse("),
 ("the index of a target is no later part", CHECK, "checkOrder(w, `'${e.op}'`, [e.value, e.target.index], false);", "checkOrder(w, `'${e.op}'`, [e.value], false);"),
 ("a right side may change the array its target is in", CHECK, "        else checkOrder(w, `'${e.op}'`, [e.target, e.value], false);\n", ""),
 ("an index that is no number is let through", CHECK, "        if (index.kind === 'str' && !NUMERIC_STRING.test(index.value)) {", "        if (false) {"),
 ("length and defined take an array", CHECK, "    if (e.kind === 'apply' && (e.name === 'length' || e.name === 'defined') && plain(e.args[0]!).kind === 'array') {", "    if (false) {"),
 ("an array need not be the last target", CHECK, "            if (array && n !== e.targets.length - 1) refuse(", "            if (false) refuse("),
 ("an array may end a sub", CHECK, "    } else if (listy(e) || e.kind === 'slice' || e.kind === 'listassign'", "    } else if (e.kind === 'slice' || e.kind === 'listassign'"),
 # ---- the parser and the lexer
 ("pop without brackets may come before an operator", PARSE, "isModifier(after))) {\n            refuse(`${head.text} @${array.name} before", "isModifier(after)) && false) {\n            refuse(`${head.text} @${array.name} before"),
 ("a comma may follow an assignment's right side", PARSE, "        if (after.kind === ',') {\n            refuse(\"a comma after an assignment's right side", "        if (false) {\n            refuse(\"a comma after an assignment's right side"),
 ("a range may be the end of a range", PARSE, "            if (infix.range && peek().kind === 'op' && infixOp(peek().text)?.range) {", "            if (false) {"),
 ("an element of an element", PARSE, "        if (peek().kind === '[') refuse('an element of an element: an array of arrays is not in the language yet', peek().pos);\n        return { kind: 'elem'", "        return { kind: 'elem'"),
 ("a slice may have no index", PARSE, "            if (indexes.length === 0) refuse('a slice with no index: perl refuses it', open.pos);\n", ""),
 ("an assigning operator on an array", PARSE, "                    if (t.text !== '=') refuse(`'${t.text}' on an array: an array is assigned with =`, t.pos);\n", ""),
 ("one thing in brackets is a list of one", PARSE, "            const isList = peek().kind === ')' || commaAhead(i, ')');", "            const isList = true;"),
 ("$a alone is a variable", LEX, "            if (RESERVED.has(name) && !(at() === '[' && name !== '_')) refuse(", "            if (false) refuse("),
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
for src in sorted(glob.glob('t/4[1-9]*.pl') + ['t/580-name-a.pl', 't/903-context.pl']):
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
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'array', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
