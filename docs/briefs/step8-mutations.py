#!/usr/bin/env python3
"""Break step 8's subs on purpose, one way at a time, in the runtime and
in each pass of the compiler, and see that a test goes red each time.

    python3 docs/briefs/step8-mutations.py            # all of them
    python3 docs/briefs/step8-mutations.py "return"   # those named so

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 8, t/9*.pl, the refused ones too (a parser
           and a checker are half refusals), run with the knobs of
           t/knobs.sh and each test's own `# env:`, as t/run.sh runs
           them. For a broken runtime each test's C is compiled once, by
           the compiler as it is, and linked again with the broken
           runtime; for a broken compiler each is compiled again by the
           copy
  unit     the runtime's own tests of the limit on recursion, the two of
           runtime/tests/rt.test.ts that name D68, in the copy (all of
           them take a minute, and the rest are step 7's)

A record of step 8, and not part of make test: each breakage is a piece
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
 # ---- the runtime: the limit on recursion, and the faults of a call
 ("an open frame is not counted", RT, "    cx->deep += weight(count);\n", ""),
 ("a closed frame is still counted", RT, "    cx->deep -= weight(frame->count);\n", ""),
 ("a frame's slots are not counted", RT, "    return count * sizeof(rt_value) + RT_CALL_BYTES;", "    return RT_CALL_BYTES;"),
 ("the limit lets one more call through", RT, "    if (weight(count) > RT_DEPTH_LIMIT - cx->deep) rt_fault", "    if (weight(count) > RT_DEPTH_LIMIT + 1120 - cx->deep) rt_fault"),
 ("the limit stops one call early", RT, "    if (weight(count) > RT_DEPTH_LIMIT - cx->deep) rt_fault", "    if (weight(count) + 1120 > RT_DEPTH_LIMIT - cx->deep) rt_fault"),
 ("there is no limit", RT, '    if (weight(count) > RT_DEPTH_LIMIT - cx->deep) rt_fault(cx, "recursion too deep");\n', ""),
 ("the stack the program was given is not looked at", RT, "    if (getrlimit(RLIMIT_STACK, &stack) == 0 && ", "    if (0 && getrlimit(RLIMIT_STACK, &stack) == 0 && "),
 ("too few is said as too many", RT, 'few ? "few" : "many"', 'few ? "many" : "few"'),
 ("at least and at most change places", RT, 'few ? "at least " : "at most "', 'few ? "at most " : "at least "'),
 ("the count expected is the other end's", RT, "few ? least : most);", "few ? most : least);"),
 ("a sub's fault leaves its name out", RT, 'snprintf(both, sizeof both, "%.300s %s", name, what);', 'snprintf(both, sizeof both, "%s", what); (void)name;'),
 # ---- the code generator: a call
 ("arguments are worked out right to left", GEN, "        const args = e.args.map(a => genExpr(a, b, 'list'));", "        const args = [...e.args].reverse().map(a => genExpr(a, b, 'list')).reverse();"),
 ("an argument that is a variable is copied at the call", GEN, "(args[n] === undefined ? 'NULL' : pointTo(b, args[n])));", "(args[n] === undefined ? 'NULL' : pointTo(b, temp(b, args[n].c))));"),
 ("the line is not stored again after a call", GEN, "        b.lines.push(`cx->line = ${b.line};`);\n        return result;", "        return result;"),
 ("too few arguments are let through", GEN, "        if (args.length < least || args.length > most) {", "        if (args.length > most) {"),
 ("too many arguments are let through", GEN, "        if (args.length < least || args.length > most) {", "        if (args.length < least) {"),
 ("the count is looked at before the arguments run", GEN, "        const args = e.args.map(a => genExpr(a, b, 'list'));\n        const least = called.params.filter(p => p.op === undefined).length;\n        const most = called.params.length;\n        if (args.length < least || args.length > most) {",
  "        const least = called.params.filter(p => p.op === undefined).length;\n        const most = called.params.length;\n        if (e.args.length < least || e.args.length > most) b.lines.push(`rt_fault_arguments(cx, ${cString(e.name)}, ${e.args.length}, ${least}, ${most});`);\n        const args = e.args.map(a => genExpr(a, b, 'list'));\n        if (args.length < least || args.length > most) {"),
 # ---- the code generator: context
 ("an argument of a call is a scalar", GEN, "        const args = e.args.map(a => genExpr(a, b, 'list'));", "        const args = e.args.map(a => genExpr(a, b, 'scalar'));"),
 ("say's argument is a scalar", GEN, "c => [`${name.rt}(cx, ${c});`], 'list').code", "c => [`${name.rt}(cx, ${c});`], 'scalar').code"),
 ("a call that is a statement is not void", GEN, "        const whole = genWhole(s.expr, s.pos.line, out, () => [], 'void');", "        const whole = genWhole(s.expr, s.pos.line, out, () => [], 'scalar');"),
 ("a call that is a part of a for is not void", GEN, "    es.forEach(e => genExpr(e, b, 'void'));", "    es.forEach(e => genExpr(e, b, 'scalar'));"),
 ("return does not hand its context on", GEN, "c => [`r = ${c};`, 'goto done;'], 'pass').code", "c => [`r = ${c};`, 'goto done;'], 'scalar').code"),
 ("return makes every call a list", GEN, "c => [`r = ${c};`, 'goto done;'], 'pass').code", "c => [`r = ${c};`, 'goto done;'], 'list').code"),
 ("a last statement does not hand its context on", GEN, "c => [`r = ${c};`], 'pass');", "c => [`r = ${c};`], 'scalar');"),
 ("a last statement is void", GEN, "c => [`r = ${c};`], 'pass');", "c => [`r = ${c};`], 'void');"),
 ("the context is not handed to the first branch of ? :", GEN, "pointTo(b, genExpr(e.then, b, want))", "pointTo(b, genExpr(e.then, b))"),
 ("the context is not handed to the second branch of ? :", GEN, "pointTo(b, genExpr(e.else, b, want))", "pointTo(b, genExpr(e.else, b))"),
 ("the context is not handed to the right of ||", GEN, "pointTo(b, genExpr(e.right, b, want))", "pointTo(b, genExpr(e.right, b))"),
 ("the context is not handed through a unary plus", GEN, "genExpr(e.operand, b, rt === undefined ? want : 'scalar');", "genExpr(e.operand, b, 'scalar');"),
 ("the context is handed to an operand of !", GEN, "genExpr(e.operand, b, rt === undefined ? want : 'scalar');", "genExpr(e.operand, b, want);"),
 # ---- the code generator: a sub
 ("a sub's frame is not closed", GEN, "        '    rt_leave(cx, &frame);',\n        '    return r;',", "        '    return r;',"),
 ("return with a value does not leave", GEN, "c => [`r = ${c};`, 'goto done;'], 'pass').code", "c => [`r = ${c};`], 'pass').code"),
 ("return alone does not leave", GEN, "'r = rt_undef();', 'goto done;']", "'r = rt_undef();']"),
 ("return alone gives a list an undef", GEN, "`if (want == RT_LIST) rt_fault_sub(cx, ${name}, RT_NOTHING);`, ", ""),
 ("an empty body gives a list an undef", GEN, "        lines.push(`if (want == RT_LIST) {`,", "        lines.push(`if (0) {`,"),
 ("a sub with no value gives an undef", GEN, "        lines.push(`if (want != RT_VOID) {`,", "        lines.push(`if (0) {`,"),
 ("a sub with no value faults when it was called void", GEN, "        lines.push(`if (want != RT_VOID) {`,", "        lines.push(`if (1) {`,"),
 ("a sub that ends in say is worth undef", GEN, "        lines.push('r = rt_bool(1);');", "        lines.push('r = rt_undef();');"),
 # (Not here: a sub that ends in `say` being worth the Int 1 and not
 # `true`. Nothing in the language can tell the two apart: each is 1 as a
 # number and `1` as a string, and `++` makes an Int of either.)
 ("a default is used though the argument was given", GEN, "            : `a${n} != NULL`;", "            : '0';"),
 ("//= is =", GEN, "p.op === '//=' ? `a${n} != NULL && !rt_is_undef(cx, *a${n})`", "p.op === '//=' ? `a${n} != NULL`"),
 ("||= is //=", GEN, "`a${n} != NULL && rt_is_true(cx, *a${n})`", "`a${n} != NULL && !rt_is_undef(cx, *a${n})`"),
 ("a placeholder's default does not run", GEN, "            lines.push(`if (${given}) {`, ...indent(copy), '} else {', ...indent(fallback), '}');", "            if (slot !== undefined) lines.push(`if (${given}) {`, ...indent(copy), '} else {', ...indent(fallback), '}');"),
 ("a fault in a default names the caller's line", GEN, "genWhole(p.default, p.pos.line, out, c => (slot === undefined ? [] : [`${slot} = ${c};`])).code;", "genWhole(p.default, p.pos.line, out, c => (slot === undefined ? [] : [`${slot} = ${c};`])).code.slice(1);"),
 # ---- the code generator: the file's variables
 ("a file variable's my makes it undef", GEN, "        if (!isFile(b, e)) b.vars.push(", "        b.vars.push("),
 ("the file's variables are not undef as the program starts", GEN, "        ...(names.file ? [`    for (int k = 0; k < ${names.file}; k++) f[k] = rt_undef();`] : []),\n", ""),
 ("a sub looks in its own frame for a file variable", GEN, "    return b.names.owner[id] === b.fn ? `f[${slot}]` : `g[${slot}]`;", "    return `f[${slot}]`;"),
 ("a sub's temporaries begin at the file's count of variables", GEN, "    const t = `f[${b.names.frames[b.fn]! + b.values}]`;", "    const t = `f[${b.names.frames[0]! + b.values}]`;"),
 # ---- the resolver
 ("a file variable has a slot a block may use", RESOLVE, "        if (scopes.at(-1) === fileScope) {\n            fileSlots.add(id);", "        if (false) {\n            fileSlots.add(id);"),
 ("a default sees its own parameter", RESOLVE, "            if (p.default) whole(p.default);\n            if (p.my === undefined) continue;\n            if (scopes.at(-1)!.has(p.my.name)) refuse(`two parameters called $${p.my.name}: perl warns that the second masks the first`, p.my.pos);\n            of.set(p.my, names.length);\n            names.push(p.my.name);\n            declare(p.my);",
  "            if (p.my === undefined) { if (p.default) whole(p.default); continue; }\n            if (scopes.at(-1)!.has(p.my.name)) refuse(`two parameters called $${p.my.name}: perl warns that the second masks the first`, p.my.pos);\n            of.set(p.my, names.length);\n            names.push(p.my.name);\n            declare(p.my);\n            if (p.default) whole(p.default);"),
 ("two parameters may have one name", RESOLVE, "            if (scopes.at(-1)!.has(p.my.name)) refuse(", "            if (false) refuse("),
 ("two subs may have one name", RESOLVE, "        if (called.has(s.name)) refuse(", "        if (false) refuse("),
 ("a sub's body is a scope inside its parameters'", RESOLVE, "        s.body.forEach(statement);\n        frames[fn] = variables;", "        inner(s.body);\n        frames[fn] = variables;"),
 ("a sub's count of variables is the file's", RESOLVE, "        frames[fn] = variables;\n        ({ fn, inScope, variables, scopes, round } = outer);", "        ({ fn, inScope, variables, scopes, round } = outer);\n        frames[called.get(s.name)!] = variables;"),
 # ---- the checker
 ("a row of dots and a call that changes what it read is let through", CHECK, "                if (readIds.has(id)) {", "                if (false) {"),
 ("only a sub's own assignments are counted against a row", CHECK, "    for (let grew = true; grew;) {", "    for (let grew = false; grew;) {"),
 ("a default's assignments and calls are not counted against a row", CHECK, "        s.params.forEach(p => p.default && expr(p.default, n + 1));\n", ""),
 ("(...) x is let through as an argument", CHECK, "    if (e.kind === 'invoke') e.args.forEach(a => checkListContext(a, `as an argument of ${e.name}`));\n", ""),
 ("(...) x is let through after return", CHECK, "        return checkListContext(s.value, 'after return');", "        return;"),
 ("(...) x is let through as a last statement", CHECK, "        if (last) checkListContext(s.expr, \"as a sub's last statement\");\n", ""),
 ("a value alone is a statement anywhere", CHECK, "s.expr.kind !== 'invoke' && !last) {", "s.expr.kind !== 'invoke' && false) {"),
 ("a value alone is no statement, a sub's last or not", CHECK, "s.expr.kind !== 'invoke' && !last) {", "s.expr.kind !== 'invoke') {"),
 ("a call is no statement", CHECK, "s.expr.kind !== 'my' && s.expr.kind !== 'invoke' && !last) {", "s.expr.kind !== 'my' && !last) {"),
 ("a required parameter may follow an optional one", CHECK, "        if (p.op === undefined && optional) refuse(", "        if (false) refuse("),
 ("a default is not checked", CHECK, "        if (p.default) checkExpr(w, p.default, false);\n", ""),
 # ---- the parser
 ("a minus hard against one letter is let through", PARSE, "/^[A-Za-z]$/.test(word.text) && touching(k)) {", "/^[A-Za-z]$/.test(word.text) && false) {"),
 ("a blank after the first word after say is let through", PARSE, "        if (callable(tokens[first]!) && tokens[first + 1]!.kind === '(' && !touching(first)) {", "        if (false) {"),
 ("say's rule does not look through brackets", PARSE, "        while (tokens[first]!.kind === '(') first += 1;\n", ""),
 ("say's rule refuses a call that touches its bracket", PARSE, "tokens[first + 1]!.kind === '(' && !touching(first)) {", "tokens[first + 1]!.kind === '(') {"),
 ("a sub may stand in a block", PARSE, "            if (depth > 0) refuse('a sub stands", "            if (false) refuse('a sub stands"),
 ("return may stand outside a sub", PARSE, '            if (!inSub) refuse("return outside', '            if (false) refuse("return outside'),
 ("a sub may be named for a word of perl's", PARSE, "            if (NAMES.has(named.text) || PERL_WORDS.has(named.text)) refuse(", "            if (false) refuse("),
 ("a sub may be named v1_0", PARSE, "            if (named.kind === 'version' || isVersionString(named.text)) {", "            if (false) {"),
 ("two commas together are one", PARSE, "            if (peek().kind === ',') refuse(\"a comma with no argument before it", "            while (peek().kind === ',') next();\n            if (false) refuse(\"a comma with no argument before it"),
 ("a word operator may follow return's value", PARSE, "            if (after.kind === 'op' && infixOp(after.text)) {\n                refuse(`'${after.text}' after return's value", "            if (false) {\n                refuse(`'${after.text}' after return's value"),
 ("return may be a value", PARSE, "        if (name?.kind === 'jump' || name?.kind === 'return') {", "        if (name?.kind === 'jump') {"),
 ("return takes a while", PARSE, "        if (inner.kind === 'return' && modifier.kind === 'while') {", "        if (false) {"),
 ("a sub needs no signature", PARSE, "            if (open.kind !== '(') return refuse(`sub ${named.text} needs a signature", "            if (false) return refuse(`sub ${named.text} needs a signature"),
 ("a comma may not follow the last argument", PARSE, "            if (t.kind !== ',') break;\n            next();\n        }\n        inList = outer;\n        closing();\n        return { kind: 'invoke'", "            if (t.kind !== ',') break;\n            next();\n            if (peek().kind === ')') refuse('a comma before the bracket', peek().pos);\n        }\n        inList = outer;\n        closing();\n        return { kind: 'invoke'"),
 # ---- the lexer
 ("a $ alone is taken anywhere", LEX, "            if (signature > 0 && !isWordStart(at())) {", "            if (!isWordStart(at())) {"),
 ("a $ alone is not taken in a signature", LEX, "            if (signature > 0 && !isWordStart(at())) {", "            if (false) {"),
]

only = sys.argv[1:]
knobs = checks.knobs()
tests = []
for src in sorted(glob.glob('t/9*.pl')):
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
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'D68', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
