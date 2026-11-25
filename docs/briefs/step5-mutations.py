#!/usr/bin/env python3
"""Break step 5's runtime and its code generator on purpose, one way at a
time, and see that a test goes red each time.

    python3 docs/briefs/step5-mutations.py            # all of them
    python3 docs/briefs/step5-mutations.py "late"     # those named so

Nothing in the tree is written: a broken runtime is build/mut/rt.c,
linked with every test's own C, which is compiled once; a broken
compiler is a copy of bin/ and compiler/src/ under build/mut/tree/, and
every test is compiled again with it.

A record of step 5, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil
from concurrent.futures import ThreadPoolExecutor
RT = open('runtime/rt.c').read()
TWO = '"++ or -- on a string that is a whole number this large has two answers in perl"'
RUNTIME = [
 ("++ on undef is 0", "    if (a.tag == RT_TAG_UNDEF) return rt_int(d);", "    if (a.tag == RT_TAG_UNDEF) return rt_int(0);"),
 ("-- on undef is 1", "    if (a.tag == RT_TAG_UNDEF) return rt_int(d);", "    if (a.tag == RT_TAG_UNDEF) return rt_int(1);"),
 ("a step on undef faults", "    if (a.tag == RT_TAG_UNDEF) return rt_int(d);\n", ""),
 ("a stepped boolean is a boolean", "    if (a.tag == RT_TAG_BOOL) return rt_int(a.as.i + d);", "    if (a.tag == RT_TAG_BOOL) return rt_bool(a.as.i + d != 0);"),
 ("a stepped boolean forgets itself", "    if (a.tag == RT_TAG_BOOL) return rt_int(a.as.i + d);", "    if (a.tag == RT_TAG_BOOL) return rt_int(d);"),
 ("a stepped string is an Int", "        return rt_num(f + d);\n    }", "        return f == trunc(f) ? rt_int((int64_t)f + d) : rt_num(f + d);\n    }"),
 ("a stepped string: no fault at 2^53", "fabs(f) >= TWO_53 || fabs(f + d) >= TWO_53", "fabs(f) >= 2 * TWO_53 || fabs(f + d) >= 2 * TWO_53"),
 ("a stepped string: the fault only by where it starts", "fabs(f) >= TWO_53 || fabs(f + d) >= TWO_53", "fabs(f) >= TWO_53"),
 ("a stepped string: the fault only by where it ends", "fabs(f) >= TWO_53 || fabs(f + d) >= TWO_53", "fabs(f + d) >= TWO_53"),
 ("a stepped string: no fault at all for a large one", "            rt_fault(cx, " + TWO + ");\n", "            ;\n"),
 ("++ on a string that begins with a zero", '        if (d > 0 && digits) rt_fault(cx, "++ on a string of digits that begins with a zero has two answers in perl");\n', ""),
 ("-- on a string that begins with a zero faults too", "        if (d > 0 && digits) rt_fault", "        if (digits) rt_fault"),
 ("a lone 0 as a string faults", "        int digits = s->len > 1 && s->bytes[0] == '0';", "        int digits = s->bytes[0] == '0';"),
 ("a zero before a point faults", "        for (uint64_t at = 0; digits && at < s->len; at++) digits = digit(s->bytes[at]);\n", ""),
 ("a stepped Int doesn't overflow", "        int o = __builtin_add_overflow(x.i, (int64_t)d, &r);\n        return checked(cx, r, o);", "        return rt_int((int64_t)((uint64_t)x.i + (uint64_t)(int64_t)d));"),
 ("a stepped Int goes the other way", "        int o = __builtin_add_overflow(x.i, (int64_t)d, &r);", "        int o = __builtin_sub_overflow(x.i, (int64_t)d, &r);"),
 ("++ on a whole Num is a Num", "    if (d > 0 && is_whole) return rt_int(whole + 1);\n", ""),
 ("-- on a whole Num is an Int", "    if (d > 0 && is_whole) return rt_int(whole + 1);", "    if (is_whole && magnitude(whole + d) < (uint64_t)1 << 53) return rt_int(whole + d);"),
 ("++ on a whole Num adds nothing", "    if (d > 0 && is_whole) return rt_int(whole + 1);", "    if (d > 0 && is_whole) return rt_int(whole);"),
 ("a float too large to step: no fault", '    if (x.n + d == x.n) rt_fault(cx, "a float too large to step by one");\n', ""),
 ("-- on a whole float at 2^53: no fault", '    if (is_whole && magnitude(whole - 1) >= (uint64_t)1 << 53) rt_fault(cx, "-- on a whole float that reaches 2^53 has two answers in perl");\n', ""),
 ("-- on a whole float: the fault one early", "magnitude(whole - 1) >= (uint64_t)1 << 53) rt_fault", "magnitude(whole - 1) >= ((uint64_t)1 << 53) - 1) rt_fault"),
 ("a stepped Num goes the other way", "    return rt_num(x.n + d);\n}", "    return rt_num(x.n - d);\n}"),
 ("-- is ++", "    return step(cx, a, -1);", "    return step(cx, a, 1);"),
 ("++ is --", "    return step(cx, a, 1);", "    return step(cx, a, -1);"),
 ("$x++ on undef is worth undef", "    return rt_is_undef(cx, a) ? rt_int(0) : a;", "    return a;"),
 ("$x++ is always worth 0", "    return rt_is_undef(cx, a) ? rt_int(0) : a;", "    return rt_int(0);"),
 (".= on undef faults", "    return rt_concat(cx, a.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : a, b);", "    return rt_concat(cx, a, b);"),
 (".= on undef starts from 0", "    return rt_concat(cx, a.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : a, b);", "    return rt_concat(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);"),
 (".= the wrong way round", "    return rt_concat(cx, a.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : a, b);", "    return rt_concat(cx, b, a.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : a);"),
 ("+= on undef faults", "    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);", "    return rt_add(cx, a, b);"),
 ("+= on undef starts from 1", "    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);", "    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(1) : a, b);"),
 ("+= takes an undef on the right", "    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);", "    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b.tag == RT_TAG_UNDEF ? rt_int(0) : b);"),
 ("-= on undef faults", "    return rt_sub(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);", "    return rt_sub(cx, a, b);"),
 ("-= the wrong way round", "    return rt_sub(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);", "    return rt_sub(cx, b, a.tag == RT_TAG_UNDEF ? rt_int(0) : a);"),
 ("-= adds", "    return rt_sub(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);", "    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);"),
]

GEN = 'compiler/src/codegen.ts'
NAMES = 'compiler/src/names.ts'
RESOLVE = 'compiler/src/resolver.ts'
PARSE = 'compiler/src/parser.ts'
COMPILER = [
 ("late: a variable is copied where it is met", GEN, "    case 'var': return { c: variable(b, e), place: true };", "    case 'var': return temp(b, variable(b, e));"),
 ("late: an assignment is worth a copy", GEN, "        return { c: v, place: true };\n    }\n    // `++$x`", "        return temp(b, v);\n    }\n    // `++$x`"),
 ("late: ++$x is worth a copy", GEN, "        return was ?? { c: v, place: true };", "        return was ?? temp(b, v);"),
 ("late: $x++ is worth the variable", GEN, "        const was = e.before ? undefined : temp(", "        const was = true ? undefined : temp("),
 ("late: a unary plus copies", GEN, "        return rt === undefined ? operand : temp(b, `${rt}(cx, ${operand.c})`);", "        return temp(b, rt === undefined ? operand.c : `${rt}(cx, ${operand.c})`);"),
 ("late: ? : is worth a copy", GEN, "        b.lines.push(`${p} = ${pointTo(b, genExpr(e.else, b))};`, '}');\n        return { c: `(*${p})`, place: true };", "        b.lines.push(`${p} = ${pointTo(b, genExpr(e.else, b))};`, '}');\n        return temp(b, `(*${p})`);"),
 ("late: || is worth a copy", GEN, "            b.lines.push(`${p} = ${pointTo(b, genExpr(e.right, b))};`, '}');\n            return { c: `(*${p})`, place: true };", "            b.lines.push(`${p} = ${pointTo(b, genExpr(e.right, b))};`, '}');\n            return temp(b, `(*${p})`);"),
 ("late: the left of || is copied", GEN, "            b.lines.push(`${p} = ${pointTo(b, left)};`,", "            b.lines.push(`${p} = ${pointTo(b, temp(b, left.c))};`,"),
 ("late: a branch of ? : is copied", GEN, "        b.lines.push(`${p} = ${pointTo(b, genExpr(e.then, b))};`, '} else {');", "        b.lines.push(`${p} = ${pointTo(b, temp(b, genExpr(e.then, b).c))};`, '} else {');"),
 ("$x++ on undef is worth what it held", GEN, "temp(b, op.before === undefined ? v : `${op.before}(cx, ${v})`)", "temp(b, v)"),
 ("$x-- on undef is worth 0", NAMES, "{ rt: 'rt_dec' }", "{ rt: 'rt_dec', before: 'rt_before_inc' }"),
 ("||= always assigns", GEN, "            b.lines.push(`if (${op.when}(cx, ${v})) {`);", "            b.lines.push(`if (${op.when}(cx, ${v}) || 1) {`);"),
 ("||= works its right side out first", GEN, "            b.lines.push(`if (${op.when}(cx, ${v})) {`);\n            b.lines.push(`${v} = ${genExpr(e.value, b).c};`, '}');", "            const early = genExpr(e.value, b).c;\n            b.lines.push(`if (${op.when}(cx, ${v})) {`);\n            b.lines.push(`${v} = ${early};`, '}');"),
 ("&&= is ||=", NAMES, "assign: true, when: 'rt_is_true'", "assign: true, when: 'rt_is_false'"),
 ("//= is ||=", NAMES, "assign: true, when: 'rt_is_undef'", "assign: true, when: 'rt_is_false'"),
 ("+= is the plain +", NAMES, "put('+=', 'rt_add_to')", "put('+=', 'rt_add')"),
 ("-= is the plain -", NAMES, "put('-=', 'rt_sub_from')", "put('-=', 'rt_sub')"),
 (".= is the plain dot", NAMES, "put('.=', 'rt_concat_to')", "put('.=', 'rt_concat')"),
 ("*= takes an undef", NAMES, "put('*=', 'rt_mul')", "put('*=', 'rt_add_to')"),
 ("x= is .=", NAMES, "put('x=', 'rt_repeat')", "put('x=', 'rt_concat_to')"),
 ("%= is /=", NAMES, "put('%=', 'rt_mod')", "put('%=', 'rt_div')"),
 ("**= is *=", NAMES, "put('**=', 'rt_pow')", "put('**=', 'rt_mul')"),
 ("an op-assign reads the variable before the right side", GEN, "            const value = genExpr(e.value, b);\n            b.lines.push(op?.rt === undefined ? `${v} = ${value.c};` : `${v} = ${op.rt}(cx, ${v}, ${value.c});`);", "            const held = op?.rt === undefined ? '' : temp(b, v).c;\n            const value = genExpr(e.value, b);\n            b.lines.push(op?.rt === undefined ? `${v} = ${value.c};` : `${v} = ${op.rt}(cx, ${held}, ${value.c});`);"),
 ("unless is if", GEN, "arm.negate ? 'rt_is_false' : 'rt_is_true'", "'rt_is_true'"),
 ("if is unless", GEN, "arm.negate ? 'rt_is_false' : 'rt_is_true'", "arm.negate ? 'rt_is_true' : 'rt_is_false'"),
 ("the arms after one that ran, run", GEN, "        ...(rest.length ? ['} else {', ...indent(rest), '}'] : ['}']),", "        '}', ...rest,"),
 ("the else is dropped", GEN, "    if (arm === undefined) return (s.otherwise ?? []).flatMap(t => genStmt(t, out));", "    if (arm === undefined) return [];"),
 ("the else runs with the last arm", GEN, "        ...(rest.length ? ['} else {', ...indent(rest), '}'] : ['}']),", "        ...(n + 1 < s.arms.length ? ['} else {', ...indent(rest), '}'] : [...indent(rest), '}']),"),
 ("an elsif's fault names the if's line", GEN, "s.modifier ? s.pos.line : arm.pos.line", "s.pos.line"),
 ("a modifier's fault names the if's line", GEN, "s.modifier ? s.pos.line : arm.pos.line", "arm.pos.line"),
 ("a statement's fault names the line before", GEN, "        const whole = genWhole(s.expr, s.pos.line, out, () => []);", "        const whole = genWhole(s.expr, s.pos.line - 1, out, () => []);"),
 # Not here, being no change to what any program of step 5 does: a `my`
 # that is not made undef again each time its block is entered. No block
 # is entered twice until there is a loop: step 6 must test it.
 ("scope: a block's my is the outer one", RESOLVE, "    const inner = (body: readonly Stmt[]): void => {\n        scopes.push(new Map());\n        body.forEach(statement);\n        scopes.pop();", "    const inner = (body: readonly Stmt[]): void => {\n        body.forEach(statement);"),
 ("scope: a variable is the first of its name, not the nearest", RESOLVE, "            const found = [...scopes].reverse().find(s => s.has(e.name));", "            const found = scopes.find(s => s.has(e.name));"),
 ("scope: my $x = $x is its own", RESOLVE, "            walk(e.value, declared);\n            return walk(e.target, declared);", "            walk(e.target, declared);\n            for (const d of declared) scopes.at(-1)!.set(d.name, of.get(d)!);\n            return walk(e.value, declared);"),
 ("scope: an if's test is in the scope outside", RESOLVE, "            scopes.push(new Map());\n            for (const arm of s.arms) {", "            for (const arm of s.arms) {"),
 ("assignment groups left to right", PARSE, "value: expression(infix.row + 1), pos: t.pos };", "value: expression(infix.row), pos: t.pos };"),
]

only = sys.argv[1:]
os.makedirs('build/mut', exist_ok=True)
tests = []
for src in sorted(glob.glob('t/5*.pl') + glob.glob('t/6*.pl')):
    if 'kind: refused' in open(src, encoding='utf-8', errors='replace').read(400):
        continue
    name = os.path.basename(src)[:-3]
    tests.append((name, open(src[:-3] + '.expected', 'rb').read()))

def compiled(test, driver='bin/curlyc.ts'):
    name = test[0]
    r = subprocess.run(['node', driver, '-o', f'build/mut/{name}', f't/{name}.pl'], capture_output=True)
    if r.returncode:
        return False
    return subprocess.run(['cc', '-O0', '-c', '-Iruntime', '-o', f'build/mut/{name}.o', f'build/mut/{name}.c'], capture_output=True).returncode == 0

def passes(test):
    name, expected = test
    if subprocess.run(['cc', '-o', f'build/mut/{name}', f'build/mut/{name}.o', 'build/mut/rt.o', '-lm'], capture_output=True).returncode:
        return False
    try:
        r = subprocess.run([f'build/mut/{name}'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
    except subprocess.TimeoutExpired:
        return False
    got = r.stdout + (f'exit: {r.returncode}\n'.encode() if r.returncode else b'')
    return got == expected

def runtime(source):
    open('build/mut/rt.c', 'w').write(source)
    c = subprocess.run(['cc', '-O1', '-c', '-Iruntime', '-o', 'build/mut/rt.o', 'build/mut/rt.c'], capture_output=True, text=True)
    return c.returncode == 0

def failures(driver=None):
    def one(test):
        return (driver is None or compiled(test, driver)) and passes(test)
    with ThreadPoolExecutor(3) as pool:
        return [t[0] for t, ok in zip(tests, pool.map(one, tests)) if not ok]

def report(name, failed):
    if failed:
        print(f'{name}: {len(failed)} fail ({", ".join(f[:3] for f in failed[:8])})', flush=True)
    else:
        print(f'{name}: 0 fail   <-- NOT CAUGHT', flush=True)
        missed.append(name)

assert runtime(RT)
whole = failures('bin/curlyc.ts')
assert whole == [], f'the compiler and runtime as they are fail: {whole}'
print(f'{len(tests)} tests pass as things are', flush=True)
missed = []
for name, old, new in RUNTIME:
    if only and not any(o in name for o in only):
        continue
    assert RT.count(old) == 1, (name, RT.count(old))
    if not runtime(RT.replace(old, new)):
        print(f'{name}: DOES NOT COMPILE', flush=True)
        missed.append(name)
        continue
    report(name, failures())
assert runtime(RT)
for name, path, old, new in COMPILER:
    if only and not any(o in name for o in only):
        continue
    shutil.rmtree('build/mut/tree', ignore_errors=True)
    shutil.copytree('bin', 'build/mut/tree/bin')
    shutil.copytree('compiler/src', 'build/mut/tree/compiler/src')
    shutil.copytree('runtime', 'build/mut/tree/runtime')
    text = open(path).read()
    assert text.count(old) == 1, (name, text.count(old))
    open('build/mut/tree/' + path, 'w').write(text.replace(old, new))
    report(name, failures('build/mut/tree/bin/curlyc.ts'))
print(f'{len(missed)} not caught: {missed}')
