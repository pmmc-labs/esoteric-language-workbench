#!/usr/bin/env python3
"""Break step 10b's `$_`, its two fors, map and grep on purpose, one way at
a time, in each pass of the compiler, and see that a test goes red each
time. (The runtime gained nothing at 10b: a binder is a foreach.)

    python3 docs/briefs/step10b-mutations.py            # all of them
    python3 docs/briefs/step10b-mutations.py "grep"     # those named so
    python3 docs/briefs/step10b-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken compiler is a copy of bin/,
compiler/src/ and runtime/ under build/mut/tree/. A breakage is caught if
a golden test goes red: every test of step 10b, t/1100*.pl to t/1195*.pl,
and 582, 601, 770, 875, 880 and 969, the refused ones too, each compiled by
the copy and run with the knobs of t/knobs.sh and its own `# env:`, as
t/run.sh runs them.

A record of step 10b, and not part of make test: each breakage is a piece
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
MUTATIONS = [
 # ---- the code generator
 ("a block's temporaries are the statement's own", GEN, "    b.out.base = b.values;\n    const statements", "    b.out.base = 0;\n    const statements"),
 ("a map freezes nothing", GEN, "    b.lines.push(`${held} = ${source.c};`, ...each.arrays.map(a => `rt_freeze(cx, ${slot(a)});`));", "    b.lines.push(`${held} = ${source.c};`);"),
 ("a map gives nothing back", GEN, "    b.lines.push('}', ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`), `cx->line = ${b.line};`);", "    b.lines.push('}', `cx->line = ${b.line};`);"),
 ("the line after a block is the block's", GEN, "    b.lines.push('}', ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`), `cx->line = ${b.line};`);", "    b.lines.push('}', ...each.arrays.map(a => `rt_thaw(cx, ${slot(a)});`));"),
 ("a map's list is any list", GEN, "    const source = genList(e.items, b, 2);", "    const source = genList(e.items, b, 0);"),
 ("grep keeps everything", GEN, "        b.lines.push(`if (rt_is_true(cx, ${kept.c})) rt_list_add(cx, ${list}, ${it});`);", "        b.lines.push(`rt_list_add(cx, ${list}, ${it});`);"),
 ("grep keeps what its block gave", GEN, "        b.lines.push(`if (rt_is_true(cx, ${kept.c})) rt_list_add(cx, ${list}, ${it});`);", "        b.lines.push(`if (rt_is_true(cx, ${kept.c})) rt_list_add(cx, ${list}, ${kept.c});`);"),
 ("a grep whose block ends in a say keeps true", GEN, "${e.op === 'grep' ? it : 'rt_bool(1)'}", "${'rt_bool(1)'}"),
 ("a map whose block ends in a say gives its value", GEN, "${e.op === 'grep' ? it : 'rt_bool(1)'}", "${it}"),
 ("where one value is wanted a map is its last index", GEN, "        return temp(b, `rt_count(cx, ${values.c})`);", "        return temp(b, `rt_last_index(cx, ${values.c})`);"),
 ("the block's value is worked out before its statements", GEN, "    b.lines.push(...statements, `cx->line = ${last.pos.line};`);", "    const early = statements;\n    b.lines.push(`cx->line = ${last.pos.line};`);"),
 # ---- the resolver
 ("what a statement declares has a slot a map in it uses", RESOLVE, "            for (; inScope < peak; inScope += 1) scopes.at(-1)!.set(` ${inScope}`, -1);\n", ""),
 ("a block is no wall to last and next", RESOLVE, "            round.push({ wall: e.op });\n", "            round.push({ bare: e.pos });\n"),
 ("a loop's variable and $_ are not read-only", RESOLVE, "        readonly.add(of.get(variable)!);\n", ""),
 ("only the innermost list hears of an array named", RESOLVE, "        naming.forEach(set => set.add(found.get('@' + name)!));", "        naming.at(-1)?.add(found.get('@' + name)!);"),
 ("$_ outside a binder is any variable with no my", RESOLVE, "            if (found === undefined && e.name === '_') return refuse(", "            if (false) return refuse("),
 # ---- the checker
 ("a block is no part of its map", CHECK, "    : e.kind === 'binder' ? [...e.items, ...within(e.body)]\n", "    : e.kind === 'binder' ? [...e.items]\n"),
 ("grep names nothing", CHECK, "    else if (e.kind === 'binder' && e.op === 'grep') e.items.forEach(x => named(w, x, true, into));\n", ""),
 ("a binder's list is not held to D76 and D77", CHECK, "        bound(w, `${e.op}'s list`, `the ${e.op}`, e.items, e.body);\n", ""),
 ("a grep's block gives a list", CHECK, "        checkExpr(w, last.expr, true, e.op === 'grep' ? 'scalar' : 'list');", "        checkExpr(w, last.expr, true, 'list');"),
 ("a map's block gives one value", CHECK, "        checkExpr(w, last.expr, true, e.op === 'grep' ? 'scalar' : 'list');", "        checkExpr(w, last.expr, true, 'scalar');"),
 ("a grep's block is no test", CHECK, "        if (e.op === 'grep') tested(last.expr);\n", ""),
 ("a block's statements are not checked", CHECK, "        e.body.slice(0, -1).forEach(s => checkStmt(w, s));\n        // A block that ends in a `say`", "        // A block that ends in a `say`"),
 ("a map is no statement", CHECK, "            || s.expr.kind === 'binder';\n        if (!does && !last) {", "            ;\n        if (!does && !last) {"),
 ("a my may stand under a for modifier", CHECK, "'the loop', s.items, s.body);\n        return s.body.forEach(b => checkStmt(w, b, s.modifier === true));", "'the loop', s.items, s.body);\n        return s.body.forEach(b => checkStmt(w, b));"),
 # ---- what is list-shaped
 ("a map is not list-shaped", SHAPES, "    case 'binder': return true;", "    case 'binder': return false;"),
 # ---- the parser and the lexer
 ("an empty block is taken", PARSE, "        if (first.kind === '}') refuse(`an empty block after ${head.text}: an anonymous hash, to perl`, first.pos);\n", ""),
 ("a block may begin with a block", PARSE, "        if (first.kind === '{') refuse(`'{' first in ${head.text}'s block: an anonymous hash, to perl`, first.pos);\n", ""),
 ("a block may begin with a string and a comma", PARSE, "        if ((first.kind === 'str' || first.kind === 'int' || first.kind === 'num') && tokens[i + 1]?.kind === ',') {", "        if ((first.kind === 'int' || first.kind === 'num') && tokens[i + 1]?.kind === ',') {"),
 ("a block may begin with a number and a comma", PARSE, "        if ((first.kind === 'str' || first.kind === 'int' || first.kind === 'num') && tokens[i + 1]?.kind === ',') {", "        if ((first.kind === 'str') && tokens[i + 1]?.kind === ',') {"),
 ("a comma may follow a block", PARSE, "        if (after.kind === ',') refuse(`a comma after ${head.text}'s block: perl does not compile it`, after.pos);\n", "        if (after.kind === ',') next();\n"),
 ("a block may end in anything", PARSE, "        if (last?.kind !== 'do' && last?.kind !== 'call') refuse(", "        if (last === undefined) refuse("),
 ("a return may stand in a block", PARSE, "            if (blocks > 0) refuse('return in the block of a map or a grep: a loop says it', head.pos);\n", ""),
 ("a word operator may not join a block's last statement", PARSE, "        const expr = expression(blocks > 0 ? Infinity : AND_ROW);", "        const expr = expression(AND_ROW);"),
 ("a word operator may join any statement", PARSE, "        const expr = expression(blocks > 0 ? Infinity : AND_ROW);", "        const expr = expression(Infinity);"),
 ("for () is taken", PARSE, "            if (peek().kind === ')') refuse(`${head.text} () is a loop over nothing, and perl does not compile it`, open.pos);\n            const items = itemsTo(')');\n            const body = block();\n            return { kind: 'foreach', var: { kind: 'my', name: '_', pos: head.pos }", "            const items = itemsTo(')');\n            const body = block();\n            return { kind: 'foreach', var: { kind: 'my', name: '_', pos: head.pos }"),
 ("a return may stand under a for", PARSE, "            if (inner.kind === 'return' || inner.kind === 'jump') refuse(", "            if (false) refuse("),
 ("two modifiers are taken", PARSE, "            if (isModifier(peek())) refuse(`a second modifier after ${word.text}'s list: perl does not compile it`, peek().pos);\n", "            if (isModifier(peek())) { next(); expression(Infinity); }\n"),
 ("a program may declare $_", PARSE, "        (v.name === '_' ? refuse('$_ is not a name a program may declare: it is what a for, a map or a grep gives its block', v.pos) : v.name);", "        v.name;"),
 ("$_[0] is an element", LEX, "            if (name === '_' && (at() === '[' || at() === '{')) refuse(", "            if (false) refuse("),
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
for src in sorted(glob.glob('t/11[0-9][0-9]-*.pl') + glob.glob('t/582-*.pl') + glob.glob('t/601-*.pl') + glob.glob('t/770-*.pl') + glob.glob('t/875-*.pl') + glob.glob('t/880-*.pl') + glob.glob('t/969-*.pl')):
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
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'no test of the runtime is run for this step', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
