#!/usr/bin/env python3
"""Break step 6's compiler on purpose, one way at a time, and see that a
test goes red each time. (The runtime gained nothing at step 6, so there
is nothing of it to break.)

    python3 docs/briefs/step6-mutations.py            # all of them
    python3 docs/briefs/step6-mutations.py "next"     # those named so

Nothing in the tree is written: a broken compiler is a copy of bin/ and
compiler/src/ under build/mut/tree/, and every test of step 6 is compiled
again with it and run: 700 on, the refused ones too, since half of what a
resolver and a checker do is refuse.

A broken loop may never end, or print without end: each run has ten
seconds, and what it prints goes to a file with a limit on its size
(t/checks.py's run_capped).

A record of step 6, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
PARSE = 'compiler/src/parser.ts'
CHECK = 'compiler/src/checker.ts'
NAMES = 'compiler/src/names.ts'
WHILE_BODY = "...indent([...test.vars, ...test.code, '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', `next_${id}: RT_UNUSED;`]),"
FOR_BODY = "...indent([...(test.length ? ['{', ...indent(test), '}'] : []), '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', `next_${id}: RT_UNUSED;`, ...each.code]),"
COMPILER = [
 ("a while's test is turned round", GEN, "s.negate ? 'rt_is_true' : 'rt_is_false'", "s.negate ? 'rt_is_false' : 'rt_is_true'"),
 ("until is while", GEN, "s.negate ? 'rt_is_true' : 'rt_is_false'", "'rt_is_false'"),
 ("while is until", GEN, "s.negate ? 'rt_is_true' : 'rt_is_false'", "'rt_is_true'"),
 ("a for's test is turned round", GEN, "c => [`if (rt_is_false(cx, ${c})) break;`]).code", "c => [`if (rt_is_true(cx, ${c})) break;`]).code"),
 ("a for's test is not made", GEN, "const test = s.test === undefined ? []", "const test = true ? []"),
 ("next is last", GEN, "name.leaves ? 'last' : 'next'", "'last'"),
 ("last is next", GEN, "name.leaves ? 'last' : 'next'", "'next'"),
 ("next in a for skips the third part", GEN, FOR_BODY, FOR_BODY.replace("`next_${id}: RT_UNUSED;`, ...each.code", "...each.code, `next_${id}: RT_UNUSED;`")),
 ("last in a for runs the third part first", GEN, "                '}',\n                `last_${id}: RT_UNUSED;`,\n            ]),", "                '}',\n                `last_${id}: RT_UNUSED;`,\n                ...each.code,\n            ]),"),
 ("the block runs before the first test", GEN, WHILE_BODY, WHILE_BODY.replace("[...test.vars, ...test.code, '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}',", "[...test.vars, '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', ...test.code,")),
 ("a my in a test is one variable for the whole loop", GEN, "        return [\n            'for (;;) {',\n            " + WHILE_BODY, "        return [\n            ...test.vars,\n            'for (;;) {',\n            " + WHILE_BODY.replace("[...test.vars, ...test.code,", "[...test.code,")),
 ("a my in a block is not undef again each time round", GEN, "        b.vars.push(`rt_value ${variable(b, e)} RT_UNUSED = rt_undef();`);", "        b.vars.push(`static rt_value ${variable(b, e)} RT_UNUSED = { RT_TAG_UNDEF, { 0 } };`);"),
 ("a for's first part runs each time round", GEN, "                ...first.vars, ...first.code,\n                'for (;;) {',\n                ...indent([", "                ...first.vars,\n                'for (;;) {',\n                ...indent([...first.code, "),
 ("a for's third part runs before the block", GEN, FOR_BODY, FOR_BODY.replace("'{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', `next_${id}: RT_UNUSED;`, ...each.code", "...each.code, '{', ...indent(s.body.flatMap(t => genStmt(t, out))), '}', `next_${id}: RT_UNUSED;`")),
 ("a for's third part is not run", GEN, FOR_BODY, FOR_BODY.replace(", ...each.code]", "]")),
 ("the expressions of a part run right to left", GEN, "    es.forEach(e => genExpr(e, b));", "    [...es].reverse().forEach(e => genExpr(e, b));"),
 ("a fault in a while's test names the line after", GEN, "const test = genWhole(s.test, s.pos.line, out, c => [`if (${s.negate", "const test = genWhole(s.test, s.pos.line + 1, out, c => [`if (${s.negate"),
 ("a fault in a for's test names the line after", GEN, "genWhole(s.test, s.pos.line, out, c => [`if (rt_is_false(cx, ${c})) break;`]).code", "genWhole(s.test, s.pos.line + 1, out, c => [`if (rt_is_false(cx, ${c})) break;`]).code"),
 ("a fault in a for's first part names the line after", GEN, "const first = genParts(s.first, s.pos.line, out);", "const first = genParts(s.first, s.pos.line + 1, out);"),
 ("a fault in a for's third part names the line after", GEN, "const each = genParts(s.each, s.pos.line, out);", "const each = genParts(s.each, s.pos.line + 1, out);"),
 ("a fault under while names the line of the while", PARSE, "            return modifier.until ? { kind: 'while', test, negate: true, body: [inner], modifier: true, pos: inner.pos }\n                : { kind: 'while', test, body: [inner], modifier: true, pos: inner.pos };",
  "            return modifier.until ? { kind: 'while', test, negate: true, body: [inner], modifier: true, pos: word.pos }\n                : { kind: 'while', test, body: [inner], modifier: true, pos: word.pos };"),
 ("a statement until is a statement while", PARSE, "return modifier.until ? { kind: 'while', test, negate: true, body: [inner], modifier: true, pos: inner.pos }", "return false ? { kind: 'while', test, negate: true, body: [inner], modifier: true, pos: inner.pos }"),
 ("until with a block is while", PARSE, "...(name.until ? { negate: true as const } : {})", "...(false ? { negate: true as const } : {})"),
 ("a label is forgotten", PARSE, "return { kind: 'while', test, body, pos: head.pos, ...(name.until ? { negate: true as const } : {}), ...(label ? { label } : {}) };", "return { kind: 'while', test, body, pos: head.pos, ...(name.until ? { negate: true as const } : {}) };"),
 ("a for's label is forgotten", PARSE, "return { kind: 'for', first, each, body, pos: head.pos, ...(test ? { test } : {}), ...(label ? { label } : {}) };", "return { kind: 'for', first, each, body, pos: head.pos, ...(test ? { test } : {}) };"),
 ("a label after last is forgotten", PARSE, "return label === undefined ? { kind: 'jump', name: head.text, pos: head.pos } : { kind: 'jump', name: head.text, label, pos: head.pos };", "return { kind: 'jump', name: head.text, pos: head.pos };"),
 ("while () is taken", PARSE, "            if (peek().kind === ')' && !name.until) refuse(\"while () is while (1), to perl: say that, or for (;;)\", open.pos);\n", ""),
 ("anything may follow last", PARSE, "            if (after.kind !== ';' && !(after.kind === 'word' && NAMES.get(after.text)?.kind === 'if')) {", "            if (false) {"),
 ("a label in small letters is taken", NAMES, "/^[A-Z][A-Z0-9_]*$/.test(word)", "/^[A-Za-z][A-Za-z0-9_]*$/.test(word)"),
 ("a blank before a label's colon is taken", PARSE, "            if (colon.pos.line !== head.pos.line || colon.pos.col !== head.pos.col + head.text.length) {", "            if (false) {"),
 ("a label goes on any statement", PARSE, "            if (kind !== 'while' && kind !== 'for') {\n                refuse(`a label is on a loop", "            if (false) {\n                refuse(`a label is on a loop"),
 ("say (...) and a while on the next line is taken", PARSE, "    return kind === 'if' || kind === 'while';", "    return kind === 'if';"),
 ("a for with no semicolons is taken for one with", PARSE, "        if (semicolons === 0) refuse(\"for over a list is not in the language yet: this for is for (FIRST; TEST; EACH)\", open.pos);\n", ""),
 ("a last with no label is for the outermost loop", RESOLVE, "            const nearest = round.at(-1);", "            const nearest = round[0];"),
 ("a last with no label goes through a bare block", RESOLVE, "            const nearest = round.at(-1);", "            const nearest = [...round].reverse().find(r => 'loop' in r);"),
 ("a label means the outermost loop of that name", RESOLVE, "const found = [...round].reverse().find(r => 'loop' in r && r.loop.label?.name === name);", "const found = round.find(r => 'loop' in r && r.loop.label?.name === name);"),
 ("a label means the nearest loop, whatever its name", RESOLVE, "const found = [...round].reverse().find(r => 'loop' in r && r.loop.label?.name === name);", "const found = [...round].reverse().find(r => 'loop' in r);"),
 ("a loop that has ended is still round what follows", RESOLVE, "            round.push({ loop: s });\n            inner(s.body);\n            round.pop();\n            scopes.pop();\n            return;\n        case 'for':", "            round.push({ loop: s });\n            inner(s.body);\n            scopes.pop();\n            return;\n        case 'for':"),
 ("an if's block is a bare block", RESOLVE, "            for (const arm of s.arms) {\n                whole(arm.test);\n                inner(arm.body);", "            for (const arm of s.arms) {\n                whole(arm.test);\n                round.push({ bare: s.pos });\n                inner(arm.body);\n                round.pop();"),
 ("a while's test is in the scope outside", RESOLVE, "            scopes.push(new Map());\n            whole(s.test);\n            round.push({ loop: s });", "            whole(s.test);\n            scopes.push(new Map());\n            round.push({ loop: s });"),
 ("a for's first part is in the scope outside", RESOLVE, "            loops.set(s, loops.size);\n            scopes.push(new Map());\n            whole(...s.first);", "            loops.set(s, loops.size);\n            whole(...s.first);\n            scopes.push(new Map());"),
 ("a for's first part is seen as it is read", RESOLVE, "            whole(...s.first);", "            s.first.forEach(e => whole(e));"),
 ("a loop's test is no test", CHECK, "    case 'while':\n        tested(s.test);\n", "    case 'while':\n"),
 ("a for's test is no test", CHECK, "        if (s.test) {\n            tested(s.test);\n", "        if (s.test) {\n"),
 ("a my under while is taken", CHECK, "        return s.body.forEach(b => checkStmt(b, s.modifier === true));\n    case 'for':", "        return s.body.forEach(b => checkStmt(b));\n    case 'for':"),
 ("a my in a modifier's while is taken", CHECK, "        checkExpr(s.test, !s.modifier);\n        return s.body", "        checkExpr(s.test, true);\n        return s.body"),
 ("a my in a for's test is taken", CHECK, "            tested(s.test);\n            checkExpr(s.test, false);", "            tested(s.test);\n            checkExpr(s.test, true);"),
 ("a my in a for's third part is taken", CHECK, "        s.each.forEach(e => checkPart(e, false));", "        s.each.forEach(e => checkPart(e, true));"),
 ("a part of a for may be only a value", CHECK, "    if (e.kind !== 'assign' && e.kind !== 'step' && e.kind !== 'my') {\n        refuse('this part of the for", "    if (false) {\n        refuse('this part of the for"),
]

only = sys.argv[1:]
os.makedirs('build/mut', exist_ok=True)
tests = []
for src in sorted(glob.glob('t/7*.pl')):
    name = os.path.basename(src)[:-3]
    refused = 'kind: refused' in open(src, encoding='utf-8', errors='replace').read(400)
    tests.append((name, open(src[:-3] + '.expected', 'rb').read(), refused))

def passes(test, driver):
    name, expected, refused = test
    r = subprocess.run(['node', driver, '-o', f'build/mut/{name}', f't/{name}.pl'], capture_output=True)
    if refused:
        return r.returncode == 1 and r.stderr + b'exit: 1\n' == expected
    if r.returncode:
        return False
    try:
        run = checks.run_capped(['sh', '-c', 'exec "$0" 2>&1', f'build/mut/{name}'], dict(os.environ), b'', 10)
    except checks.Runaway:
        return False
    if run is None:
        return False
    got = run.stdout + (f'exit: {run.returncode}\n'.encode() if run.returncode else b'')
    return got == expected

def failures(driver):
    with ThreadPoolExecutor(3) as pool:
        return [t[0] for t, ok in zip(tests, pool.map(lambda t: passes(t, driver), tests)) if not ok]

whole = failures('bin/curlyc.ts')
assert whole == [], f'the compiler as it is fails: {whole}'
print(f'{len(tests)} tests pass as things are', flush=True)
missed = []
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
    failed = failures('build/mut/tree/bin/curlyc.ts')
    if failed:
        print(f'{name}: {len(failed)} fail ({", ".join(f[:3] for f in failed[:8])})', flush=True)
    else:
        print(f'{name}: 0 fail   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
