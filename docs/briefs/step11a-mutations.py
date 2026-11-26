#!/usr/bin/env python3
"""Break step 11a's interpolation on purpose, one way at a time, in each
pass of the compiler, and see that a test goes red each time. (The runtime
gained nothing at 11a: a string is `.` and `join`.)

    python3 docs/briefs/step11a-mutations.py            # all of them
    python3 docs/briefs/step11a-mutations.py "index"    # those named so
    python3 docs/briefs/step11a-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken compiler is a copy of bin/,
compiler/src/ and runtime/ under build/mut/tree/. A breakage is caught if
a golden test goes red: every test of step 11a, t/1300*.pl to t/1450*.pl,
and 200, 201 and 610, the refused ones too, each compiled by the copy and
run with the knobs of t/knobs.sh and its own `# env:`, as t/run.sh runs
them.

A record of step 11a, and not part of make test: each breakage is a piece
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
 # ---- the lexer: where a variable ends
 ("a name stops at a digit", LEX, "        const name = run(isWord);\n        if (kind === 'array' && name === '_') refuse('@_ is not in the language: a sub has a signature (D17)', where);\n        if (kind === 'var'", "        const name = run(isWordStart);\n        if (kind === 'array' && name === '_') refuse('@_ is not in the language: a sub has a signature (D17)', where);\n        if (kind === 'var'"),
 ("blanks may stand between a $ and its name", LEX, "        if (!isWordStart(at())) {\n            refuse(sigil === '$'", "        while (at() === ' ') take();\n        if (!isWordStart(at())) {\n            refuse(sigil === '$'"),
 (":: after a shape is text", LEX, "        if (src.startsWith('::', i)) refuse(", "        if (false) refuse("),
 ("{ after a shape is text", LEX, "        if (at() === '{') refuse(`'{' hard after", "        if (false) refuse(`'{' hard after"),
 ("a second [ is text", LEX, "        if (at() === '[') refuse(`'[' hard after", "        if (false) refuse(`'[' hard after"),
 ("an arrow before a bracket is text", LEX, "        if (src.startsWith('->', i) && then !== '' && '[{@$'.includes(then)) {", "        if (false) {"),
 ("an arrow before a $ is text", LEX, "'[{@$'.includes(then)", "'[{@'.includes(then)"),
 ("an arrow before an @ is text", LEX, "'[{@$'.includes(then)", "'[{$'.includes(then)"),
 ("an arrow before a brace is text", LEX, "'[{@$'.includes(then)", "'[@$'.includes(then)"),
 ("a character past ASCII after a name is text", LEX, "        if (named && next > 0x7f && line >= utf8From) {", "        if (false) {"),
 ("a character past ASCII is refused after an index too", LEX, "        if (named && next > 0x7f && line >= utf8From) {", "        if (next > 0x7f && line >= utf8From) {"),
 ("what follows braces is held to what follows a name", LEX, "            tooLong(name);\n            return { kind, name, pos: where };\n        }", "            tooLong(name);\n            if (src.startsWith('::', i) || at() === '{' || at() === '[') refuse('after braces', pos());\n            return { kind, name, pos: where };\n        }"),
 ("$#a and a bracket is an element", LEX, "        if (at() === '[' && kind !== 'lastindex') {", "        if (at() === '[') {"),
 # ---- the lexer: the shapes
 ("blanks in braces", LEX, "            take();\n            if (!isWordStart(at())) hard();\n            const name = run(isWord);", "            take();\n            while (at() === ' ') take();\n            if (!isWordStart(at())) hard();\n            const name = run(isWord);"),
 ("an index in braces is not known for one", LEX, "            if (at() === '[') refuse(`${open}{${name}[...]} in a string", "            if (false) refuse(`${open}{${name}[...]} in a string"),
 ("a brace and a backslash is not known for a reference", LEX, "            if (inside === '\\\\' || inside === '[' || inside === '$') reference(open + '{' + inside);", "            if (inside === '[' || inside === '$') reference(open + '{' + inside);"),
 ("a brace and a bracket is not known for a reference", LEX, "            if (inside === '\\\\' || inside === '[' || inside === '$') reference(open + '{' + inside);", "            if (inside === '\\\\' || inside === '$') reference(open + '{' + inside);"),
 ("a brace and a $ is not known for a reference", LEX, "            if (inside === '\\\\' || inside === '[' || inside === '$') reference(open + '{' + inside);", "            if (inside === '\\\\' || inside === '[') reference(open + '{' + inside);"),
 ("$$x is not known for a reference", LEX, "        if (at() === '$' && (isWordStart(src[i + 1] ?? '') || src[i + 1] === '{')) reference(open + '$');", ""),
 ("$# and no name is not known", LEX, "            if (!isWordStart(src[i + 1] ?? '') && src[i + 1] !== '{') {\n                refuse(\"after '$#' in a string", "            if (false) {\n                refuse(\"after '$#' in a string"),
 ("@_ in a string is an array", LEX, "        if (kind === 'array' && name === '_') refuse('@_ is not in the language: a sub has a signature (D17)', where);\n        if (kind === 'var'", "        if (kind === 'var'"),
 ("$_[ in a string is an element", LEX, "        if (kind === 'var' && name === '_' && (at() === '[' || at() === '{')) refuse(`$_${at()} is an element", "        if (false) refuse(`$_${at()} is an element"),
 ("an @ in a string is a scalar's", LEX, "        const kind = open === '$' ? 'var' : open === '@' ? 'array' : 'lastindex';", "        const kind = open === '$' ? 'var' : open === '@' ? 'var' : 'lastindex';"),
 ("$#a in a string is the array", LEX, "        const kind = open === '$' ? 'var' : open === '@' ? 'array' : 'lastindex';", "        const kind = open === '$' ? 'var' : 'array';"),
 # ---- the lexer: the index
 ("a leading zero in an index is decimal", LEX, "        if (digits.length > 1 && digits[0] === '0') refuse(", "        if (false) refuse("),
 ("an index of any size", LEX, "        if (BigInt(digits) > INDEX_MAX) refuse(", "        if (false) refuse("),
 ("an index of 2^63 - 1 is too large", LEX, "        if (BigInt(digits) > INDEX_MAX) refuse(", "        if (BigInt(digits) >= INDEX_MAX) refuse("),
 ("the minus of an index is lost", LEX, "        return { kind: 'int', text: digits, negative, pos: where };", "        return { kind: 'int', text: digits, negative: false, pos: where };"),
 ("a blank may follow an index's minus", LEX, "            if (!isDigit(src[i + 1] ?? '')) refuse(INDEX, where);\n            take();", "            take();\n            while (at() === ' ') take();"),
 ("an element takes commas and ranges", LEX, "{ kind: 'elem', name, index: indexes(false)[0]!, pos: where }", "{ kind: 'elem', name, index: indexes(true)[0]!, pos: where }"),
 ("a slice takes no range", LEX, "            if (slice && src.startsWith('..', i)) {", "            if (false) {"),
 ("no comma after a slice's last index", LEX, "                blanks();\n                if (at() === ']') break;\n                continue;", "                blanks();\n                continue;"),
 ("no blank before an index", LEX, "        for (;;) {\n            blanks();\n            let one = index(open);", "        for (;;) {\n            let one = index(open);"),
 ("no blank after an index", LEX, "            let one = index(open);\n            blanks();", "            let one = index(open);"),
 ("a tab is a blank in an index", LEX, "        const blanks = (): void => { while (at() === ' ') take(); };", "        const blanks = (): void => { while (at() === ' ' || at() === '\\t' || at() === '\\n') take(); };"),
 ("an index the string cuts short, after its bracket", LEX, "        const where = pos();\n        const cut = (): never => (i >= src.length || at() === '\"'", "        const where = pos();\n        const cut = (): never => (false"),
 ("an index the string cuts short, after an index", LEX, "        const blanks = (): void => { while (at() === ' ') take(); };\n        const cut = (): never => (i >= src.length || at() === '\"'", "        const blanks = (): void => { while (at() === ' ') take(); };\n        const cut = (): never => (false"),
 ("a scalar index with no name", LEX, "            take();\n            if (!isWordStart(at())) refuse(INDEX, where);\n            const name = run(isWord);", "            take();\n            const name = run(isWord);"),
 # ---- the lexer: the pieces
 ("the text before a variable is lost", LEX, "                    if (value !== '') pieces.push({ kind: 'text', value });\n                    value = '';", "                    value = '';"),
 ("the text after the last variable is lost", LEX, "        if (value !== '') pieces.push({ kind: 'text', value });\n        return { kind: 'str', text: src.slice(from, i), value: '', pos: start, pieces };", "        return { kind: 'str', text: src.slice(from, i), value: '', pos: start, pieces };"),
 ("the text before a variable is said again after it", LEX, "                    value = '';\n                    pieces.push(variable(c, where));", "                    pieces.push(variable(c, where));"),
 ("a variable in single quotes", LEX, "                if (quote === '\"' && (c === '$' || c === '@')) {", "                if (c === '$' || c === '@') {"),
 # ---- the parser
 ("a range in a slice is its first end", PARSE, "                if (x.kind === 'range') return { kind: 'binary', op: '..', left: index(x.from), right: index(x.to), pos: x.pos };", "                if (x.kind === 'range') return index(x.from);"),
 ("a range in a slice is backwards", PARSE, "left: index(x.from), right: index(x.to), pos: x.pos };", "left: index(x.to), right: index(x.from), pos: x.pos };"),
 ("an index's minus is not applied", PARSE, "                return x.negative ? { kind: 'unary', op: '-', operand: whole, pos: x.pos } : whole;", "                return whole;"),
 ("the pieces are in reverse", PARSE, "            return { kind: 'interp', text: t.text, parts, pos: t.pos };", "            return { kind: 'interp', text: t.text, parts: [...parts].reverse(), pos: t.pos };"),
 ("the text between is dropped", PARSE, "                p.kind === 'text' ? { kind: 'str', text: '', value: p.value, pos: t.pos }", "                p.kind === 'text' ? { kind: 'str', text: '', value: '', pos: t.pos }"),
 ("a slice in a string is an element", PARSE, "                : p.kind === 'slice' ? { kind: 'slice', name: p.name, indexes: p.indexes.map(index), pos: p.pos }", "                : p.kind === 'slice' ? { kind: 'elem', name: p.name, index: index(p.indexes[0]!), pos: p.pos }"),
 # ---- the resolver
 ("an array in a string is named by the list it stands in", RESOLVE, "        if (!quoted) naming.forEach(set => set.add(found.get('@' + name)!));", "        naming.forEach(set => set.add(found.get('@' + name)!));"),
 ("the resolver does not know it is in a string", RESOLVE, "            quoted = true;\n", "            quoted = false;\n"),
 ("in a string for good", RESOLVE, "            e.parts.forEach(x => walk(x, declared));\n            quoted = outer;", "            e.parts.forEach(x => walk(x, declared));"),
 # ---- the checker
 ("a string is a constant", CHECK, "|| e.kind === 'invoke' || e.kind === 'interp' ? false", "|| e.kind === 'invoke' ? false"),
 ("a string's pieces are not checked", CHECK, "    case 'interp': return all(e.parts, 'list');", "    case 'interp': return [];"),
 ("an array in a string is where one value is wanted", CHECK, "    case 'interp': return all(e.parts, 'list');", "    case 'interp': return all(e.parts, 'scalar');"),
 ("the lost assignment is not looked for in a string", CHECK, "wholes(w.value).some(v => v.kind === 'interp' && v.parts.length > 1)", "false"),
 ("a string of one variable is lost too", CHECK, "v.kind === 'interp' && v.parts.length > 1", "v.kind === 'interp' && v.parts.length > 0"),
 ("only a string of two pieces is lost", CHECK, "v.kind === 'interp' && v.parts.length > 1", "v.kind === 'interp' && v.parts.length === 2"),
 ("the lost assignment is not looked for behind a test", CHECK, "        if (w.kind === 'assign' && plainAssign && wholes(w.value).some(v => v.kind === 'interp'", "        if (w.kind === 'assign' && plainAssign && [plain(w.value)].some(v => v.kind === 'interp'"),
 ("a string is a piece of the row it stands in", CHECK, "    // list holds, it has no parts. (`children` has them, to be checked.)\n    : [];", "    : e.kind === 'interp' ? e.parts : [];"),
 # ---- the code generator
 ("an array's values are joined with nothing", GEN, "rt_join(cx, ${literal(' ').c}, ${genList([part], b).c})", "rt_join(cx, ${literal('').c}, ${genList([part], b).c})"),
 ("an array in a string is its count", GEN, "            const joined = part.kind === 'array' || part.kind === 'slice';", "            const joined = part.kind === 'slice';"),
 ("a slice in a string is its first", GEN, "            const joined = part.kind === 'array' || part.kind === 'slice';", "            const joined = part.kind === 'array';"),
 ("the pieces are joined right to left", GEN, "temp(b, `rt_concat(cx, ${whole.c}, ${piece.c})`)", "temp(b, `rt_concat(cx, ${piece.c}, ${whole.c})`)"),
 ("a string of one variable is the variable", GEN, "                : temp(b, `rt_concat(cx, ${piece.c}, ${literal('').c})`);", "                : piece;"),
 ("a slice past the end is the list's fault", GEN, "${genList([part], b).c})`) : genExpr(part, b);", "${genList([part], b, 2).c})`) : genExpr(part, b);"),
 ("every piece is worked out before any is joined", GEN, """        let whole: C | undefined;
        for (const part of e.parts) {
            const joined = part.kind === 'array' || part.kind === 'slice';
            const piece = joined ? temp(b, `rt_join(cx, ${literal(' ').c}, ${genList([part], b).c})`) : genExpr(part, b);
            whole = whole !== undefined ? temp(b, `rt_concat(cx, ${whole.c}, ${piece.c})`)
                : joined || part.kind === 'str' ? piece
                : temp(b, `rt_concat(cx, ${piece.c}, ${literal('').c})`);
        }
        return whole!;""", """        let whole: C | undefined;
        const all: C[] = [];
        for (const part of e.parts) {
            const joined = part.kind === 'array' || part.kind === 'slice';
            const piece = joined ? temp(b, `rt_join(cx, ${literal(' ').c}, ${genList([part], b).c})`) : genExpr(part, b);
            all.push(piece);
        }
        for (const piece of all) {
            whole = whole !== undefined ? temp(b, `rt_concat(cx, ${whole.c}, ${piece.c})`) : temp(b, `rt_concat(cx, ${piece.c}, ${literal('').c})`);
        }
        return whole!;"""),
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
for src in sorted(glob.glob('t/13[0-9][0-9]-*.pl') + glob.glob('t/14[0-5][0-9]-*.pl') + glob.glob('t/200-*.pl') + glob.glob('t/201-*.pl') + glob.glob('t/610-*.pl')):
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
