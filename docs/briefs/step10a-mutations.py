#!/usr/bin/env python3
"""Break step 10a's list returns, slurpy parameters, join and reverse on
purpose, one way at a time, in the runtime and in each pass of the
compiler, and see that a test goes red each time.

    python3 docs/briefs/step10a-mutations.py            # all of them
    python3 docs/briefs/step10a-mutations.py "slurpy"   # those named so
    python3 docs/briefs/step10a-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 10a, t/1000*.pl to t/1071*.pl, and 480 to
           482, 990 and 991, the refused ones too, run with the knobs of
           t/knobs.sh and each test's own `# env:`, as t/run.sh runs
           them. For a broken runtime each test's C is compiled once, by
           the compiler as it is, and linked again with the broken
           runtime; for a broken compiler each is compiled again by the
           copy
  unit     the runtime's own test of what a call hands about, the one of
           runtime/tests/rt.test.ts that says "slurpy", in the copy

A record of step 10a, and not part of make test: each breakage is a piece
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
LEX = 'compiler/src/lexer.ts'
BINARY = "    case 'binary': return isRange(e) || isRepeat(e) || (infixOp(e.op)?.when !== undefined && shaped(e.right, gives));"
FAULT = "        return ['if (want == RT_SCALAR) {', `    cx->line = ${line};`, `    rt_fault_sub(cx, ${cString(out.sub!.name)}, RT_LISTED);`, '}', ...asList()];"
MUTATIONS = [
 # ---- the runtime
 ("a list added to a list is not its values", RT, "    if (v.tag == RT_TAG_ARRAY) {\n        rt_list_add_all(cx, list, v);\n        return;\n    }\n", ""),
 ("a list of none is an undef to a call that wants a list", RT, "    return a->count == 0 ? rt_absent() : a->items[0];", "    return a->count == 0 ? rt_undef() : a->items[0];"),
 ("a slurpy parameter takes every argument", RT, "    for (int64_t n = from; n < argc; n++) append(", "    for (int64_t n = 0; n < argc; n++) append("),
 ("a slurpy parameter takes one argument fewer", RT, "    for (int64_t n = from; n < argc; n++) append(", "    for (int64_t n = from + 1; n < argc; n++) append("),
 ("a slurpy parameter reads a list of arguments from its start", RT, "flat != NULL ? flat[n] : *argv[n]", "flat != NULL ? flat[n - from] : *argv[n]"),
 ("reverse does not reverse", RT, "to->items[to->count++] = from->items[n - 1];", "to->items[to->count++] = from->items[from->count - n];"),
 ("join's separator is not looked at unless it is used", RT, "    const rt_str *sep = to_str(cx, separator, &x);\n    uint64_t len = 0, chars = 0;", "    const rt_str *sep = a->count < 2 ? &STR_FALSE : to_str(cx, separator, &x);\n    uint64_t len = 0, chars = 0;"),
 ("join does not count its separators' characters", RT, "        chars += s->chars + (n > 0 ? sep->chars : 0);", "        chars += s->chars;"),
 ("join leaves out its first separator", RT, "        if (n > 0) {\n            memcpy(bytes, sep->bytes, sep->len);", "        if (n > 1) {\n            memcpy(bytes, sep->bytes, sep->len);"),
 # ---- what is list-shaped
 ("an array is not list-shaped", SHAPES, "    case 'array': return true;", "    case 'array': return false;"),
 ("brackets round an array are one value", SHAPES, "e.items.length > 1 || (e.items.length === 1 && shaped(e.items[0]!, gives))", "e.items.length > 1"),
 ("a list of two is not list-shaped", SHAPES, "e.items.length > 1 || (e.items.length === 1 && shaped(e.items[0]!, gives))", "e.items.length === 1 && shaped(e.items[0]!, gives)"),
 ("a slice of an array is not list-shaped", SHAPES, "    case 'slice': return e.name !== undefined || ", "    case 'slice': return "),
 ("a slice of a list by two indexes is not list-shaped", SHAPES, "e.name !== undefined || e.indexes.length !== 1 || shaped(", "e.name !== undefined || shaped("),
 ("splice is not list-shaped", SHAPES, "    case 'arrayop': return e.op === 'splice';", "    case 'arrayop': return false;"),
 ("reverse is not list-shaped", SHAPES, "    case 'listop': return e.op === 'reverse';", "    case 'listop': return false;"),
 ("an arm of ? : is not looked at", SHAPES, "    case 'ternary': return shaped(e.then, gives) || shaped(e.else, gives);", "    case 'ternary': return false;"),
 ("only the first arm of ? : is looked at", SHAPES, "    case 'ternary': return shaped(e.then, gives) || shaped(e.else, gives);", "    case 'ternary': return shaped(e.then, gives);"),
 ("a range is not list-shaped", SHAPES, BINARY, BINARY.replace("isRange(e) || ", "")),
 ("a list repeated is not list-shaped", SHAPES, BINARY, BINARY.replace("isRepeat(e) || ", "")),
 ("the right of || is not looked at", SHAPES, BINARY, "    case 'binary': return isRange(e) || isRepeat(e);"),
 ("a unary plus hides a shape", SHAPES, "    const e = behind(in_);\n    switch (e.kind) {", "    const e = in_;\n    switch (e.kind) {"),
 # ---- which subs give a list
 ("no call hands a list on", SHAPES, "    return (e.kind === 'invoke' && gives(e))", "    return false"),
 ("a sub that hands on a call's list is not one that gives a list", SHAPES, "returned(s).some(e => shaped(e, gives) || handsOn(e, gives))", "returned(s).some(e => shaped(e, gives))"),
 ("a sub's last statement is not looked at", SHAPES, "    if (last?.kind === 'do') found.push(last.expr);\n", ""),
 ("a return in a loop is not looked at", SHAPES, "        case 'block': case 'while': case 'for': case 'foreach': return t.body.forEach(walk);\n", ""),
 ("a return in an if is not looked at", SHAPES, "            t.arms.forEach(arm => arm.body.forEach(walk));\n", ""),
 ("no sub gives a list", RESOLVE, "lists: listSubs(subs, calls),", "lists: [false, ...subs.map(() => false)],"),
 # ---- the code generator
 ("a list-shaped return never faults", GEN, FAULT, "        return asList();"),
 ("the fault for a list-shaped return names the caller's line", GEN, FAULT, FAULT.replace("`    cx->line = ${line};`, ", "")),
 ("a list-shaped return is worked out before its fault", GEN, FAULT, "        return genListWhole([e], line, out, c => ['if (want == RT_SCALAR) {', `    rt_fault_sub(cx, ${cString(out.sub!.name)}, RT_LISTED);`, '}', `r = ${c};`, ...after]).code;"),
 ("a void call of a sub that returns a list faults", GEN, "['if (want == RT_SCALAR) {', `    cx->line = ${line};`, `    rt_fault_sub(", "['if (want != RT_LIST) {', `    cx->line = ${line};`, `    rt_fault_sub("),
 ("a sub that gives no list hands back the list it made", GEN, "    const few = out.names.lists[out.fn] === true ? asList()", "    const few = true ? asList()"),
 ("what may be a list is always one value", GEN, "    if (!listy(e)) return asValue();\n", "    if (!shaped(e, gives(out.names))) return asValue();\n"),
 ("a list as a last statement is one value", GEN, "    } else if (last.kind === 'do' && listy(last.expr)) {", "    } else if (last.kind === 'do' && false) {"),
 ("brackets round one value and a comma are an undef", GEN, "        if (e.items.length === 1 && !e.my) return genExpr(e.items[0]!, b, want);\n", ""),
 ("a call that gives a list is handed on as one argument", GEN, "        if (e.args.some(a => listy(a) || handsOn(a, gives(b.names)))) {", "        if (e.args.some(listy)) {"),
 ("a parameter is read from where a list of arguments is not", GEN, "(flat != NULL ? &flat[${n}] : argv[${n}])", "(flat != NULL ? &flat[0] : argv[${n}])"),
 ("a slurpy parameter starts one argument late", GEN, "`rt_slurp(cx, ${rest}, argc, argv, flat, ${n});`", "`rt_slurp(cx, ${rest}, argc, argv, flat, ${n + 1});`"),
 ("a slurpy parameter makes up for a required one", GEN, "        slurpy ? `    if (argc < ${least}) rt_fault_arguments(", "        slurpy ? `    if (0) rt_fault_arguments("),
 ("a slurpy parameter is counted as required", GEN, "    const least = s.params.filter(p => p.op === undefined && !p.slurpy).length;", "    const least = s.params.filter(p => p.op === undefined).length;"),
 ("join's separator is read before its list is built", GEN, "        const kept = sep.place ? sep : temp(b, sep.c);\n        const values = genList(e.args.slice(1), b);", "        const kept = temp(b, sep.c);\n        const values = genList(e.args.slice(1), b);"),
 # ---- the checker
 ("reverse may stand where one value is wanted", CHECK, "    if (e.kind === 'listop' && e.op === 'reverse') refuse('reverse where one value is wanted", "    if (false) refuse('reverse where one value is wanted"),
 ("reverse names nothing", CHECK, "    else if (e.kind === 'listop' && e.op === 'reverse') e.args.forEach(x => named(w, x, true, into));\n", ""),
 ("join and reverse are not held to D76", CHECK, "    if (e.kind === 'listop') checkOrder(w, e.op, e.args, true);\n", ""),
 ("an argument beside a call that gives a list is read late", CHECK, "e.args, e.args.some(a => listy(a) || handsOn(a, gives(w))), { changes:", "e.args, e.args.some(listy), { changes:"),
 ("a slice by a call that gives a list is one value", CHECK, " || handsOn(e.indexes[0]!, gives(w)))) refuse(", ")) refuse("),
 ("a return's value is one value", CHECK, "    case 'return': return s.value === undefined ? undefined : checkExpr(w, s.value, false, 'list');", "    case 'return': return s.value === undefined ? undefined : checkExpr(w, s.value, false);"),
 ("join's separator is a list", CHECK, "    case 'listop': return e.op === 'join' ? [...all(e.args.slice(0, 1), 'scalar'), ...all(e.args.slice(1), 'list')] : all(e.args, 'list');", "    case 'listop': return all(e.args, 'list');"),
 ("a slurpy parameter is a required one after an optional one", CHECK, "        if (p.op === undefined && !p.slurpy && optional) refuse(", "        if (p.op === undefined && optional) refuse("),
 # ---- the parser and the lexer
 ("a slurpy parameter may have a default", PARSE, "refuse('a slurpy parameter has no default: perl refuses one', after.pos);", "next();"),
 ("a parameter may follow a slurpy one", PARSE, "                    if (after.kind !== ')') refuse(`${v.text} takes every argument that is left, so it is the last parameter: perl refuses one after it`, after.pos);\n", "                    if (after.kind === ',') next();\n"),
 ("an index may follow reverse's brackets", PARSE, "            if (peek().kind === '[') refuse(`'[' after ${head.text}(...): perl does not compile it; bracket the whole, (${head.text}(...))[...]`, peek().pos);\n", ""),
 ("join may have nothing", PARSE, "        if (args.length === 0) refuse(head.text === 'join' ? 'join needs a separator: join(SEP, LIST)' : `${head.text} of nothing`, head.pos);\n", ""),
 ("a comma after return's value is another message", PARSE, "            if (after.kind === ',') refuse('a list after return is in brackets: return (..., ...);', after.pos);\n", ""),
 ("@ alone is no parameter", LEX, "                push({ kind: 'array', text: '@', name: '', pos: start });", "                refuse('no', start);"),
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
for src in sorted(glob.glob('t/10[0-7][0-9]-*.pl') + glob.glob('t/48[0-2]-*.pl') + glob.glob('t/99[01]-*.pl')):
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
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'slurpy', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
