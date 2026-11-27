#!/usr/bin/env python3
"""Break step 15 on purpose, one way at a time, in the runtime and in each
pass of the compiler, and see that a test goes red each time: the
unwinding (frames, freezes, sorts), the message, the uncaught `die`, the
underflow's fault, `warn` and stderr, `try` and `catch` in every pass, and
the refusals (D141 to D151).

    python3 docs/briefs/step15-mutations.py            # all of them
    python3 docs/briefs/step15-mutations.py "freeze"   # those named so
    python3 docs/briefs/step15-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut15/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 15, t/3000*.pl to t/3299*.pl, and 008, the
           refused ones too, run with the knobs of t/knobs.sh and each
           test's own `# env:`, stdout and then stderr as t/run.sh has them
  unit     the runtime's own test of unwinding, in the copy

A record of step 15, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
UNWIND = 'runtime/unwind.c'
SORT = 'runtime/sort.c'
GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
CHECK = 'compiler/src/checker.ts'
PARSE = 'compiler/src/parser.ts'
LEX = 'compiler/src/lexer.ts'
SHAPES = 'compiler/src/shapes.ts'
MUTATIONS = [
 # ---- the runtime: unwinding
 ("a die gives back no freeze", UNWIND, "    while (cx->frozen_count > t->frozen) {", "    while (0) {"),
 ("a die gives back every freeze, the try's own loop's too", UNWIND, "    while (cx->frozen_count > t->frozen) {", "    while (cx->frozen_count > 0) {"),
 ("a die leaves the sorts open", UNWIND, "    sorts_release_to(cx, t->sorts);\n", ""),
 ("a die leaves the frames open", UNWIND, "    cx->frames = t->frames;\n", ""),
 ("a die leaves the depth as it was at the die", UNWIND, "    cx->deep = t->deep;\n", ""),
 ("a die leaves the try open", UNWIND, "    cx->tries = t->outer;\n    cx->thrown = v;", "    cx->thrown = v;"),
 ("a caught die is undef", UNWIND, "    rt_value v = cx->thrown;\n", "    rt_value v = rt_undef();\n"),
 ("a thaw takes the bottom freeze", UNWIND, "    for (uint64_t k = cx->frozen_count; k > 0; k--) {\n        if (cx->frozen[k - 1] != a) continue;", "    for (uint64_t k = 1; k <= cx->frozen_count; k++) {\n        if (cx->frozen[k - 1] != a) continue;"),
 ("a freeze is not noted", RT, "    unwind_frozen(cx, a);\n", ""),
 ("a try's freezes are counted from none", UNWIND, "    t->frozen = cx->frozen_count;", "    t->frozen = 0;"),
 ("a sort released to the bottom", SORT, "    while (cx->sorts != NULL && cx->sorts != keep) {", "    while (cx->sorts != NULL) {"),
 # ---- the runtime: the message
 ("a message is never Died", UNWIND, "    const char *head = len == 0 ? empty : \"\";", "    const char *head = \"\";"),
 ("the place is added always", UNWIND, "        newline = s->bytes[s->len - 1] == '\\n';", "        newline = 0;"),
 ("the place is never added", UNWIND, "        newline = s->bytes[s->len - 1] == '\\n';", "        newline = 1;"),
 ("the newline is looked for in the first value", UNWIND, "    for (uint64_t n = a->count; n > 0; n--) {\n        const rt_str *s = to_str(cx, a->items[n - 1], &x);", "    for (uint64_t n = 1; n <= a->count; n++) {\n        const rt_str *s = to_str(cx, a->items[n - 1], &x);"),
 ("an empty value ends the look for the newline", UNWIND, "        if (s->len == 0) continue;\n        newline", "        if (s->len == 0) break;\n        newline"),
 ("the line is one off", UNWIND, "\" line %\" PRId64 \".\\n\", cx->line);", "\" line %\" PRId64 \".\\n\", cx->line + 1);"),
 ("the values are joined with a space", UNWIND, "        memcpy(bytes, s->bytes, s->len);\n        bytes += s->len;\n    }\n    if (!newline) {", "        memcpy(bytes, s->bytes, s->len);\n        bytes += s->len;\n        if (n + 1 < a->count && s->len) *bytes++ = ' ';\n    }\n    if (!newline) {"),
 ("an uncaught die exits 1", UNWIND, "        exit(255);", "        exit(1);"),
 ("an uncaught message is not looked at before it is written", UNWIND, "    emit_checked(cx, message, 0, 0);\n", ""),
 ("an underflow is forgotten at a die", UNWIND, "        if (cx->underflowed) rt_fault(", "        if (0) rt_fault("),
 ("a string's underflow is not noted", RT, "(x == 0.0 && nonzero)) cx->underflowed = 1;", "(x == 0.0 && nonzero)) (void)0;"),
 ("a power's underflow is not noted", RT, "(r == 0.0 && as_double(left) != 0.0)) cx->underflowed = 1;", "(r == 0.0 && as_double(left) != 0.0)) (void)0;"),
 ("warn is false", UNWIND, "    return rt_bool(1);\n}\n\n// `say STDERR", "    return rt_bool(0);\n}\n\n// `say STDERR"),
 ("warn's empty message is Died", UNWIND, "    to_stderr(cx, message(cx, list, \"Warning: something's wrong\"));", "    to_stderr(cx, message(cx, list, \"Died\"));"),
 ("say STDERR has no newline", UNWIND, "    emit_list_err(cx, list, 1);", "    emit_list_err(cx, list, 0);"),
 ("say STDERR writes to stdout", UNWIND, "            fwrite(s->bytes, 1, s->len, stderr);\n        }", "            fwrite(s->bytes, 1, s->len, stdout);\n        }"),
 ("stderr is not looked at before it is written", UNWIND, "    for (uint64_t n = 0; n < a->count; n++) emit_checked(cx, a->items[n], 0, 0);\n    fflush(stdout);", "    fflush(stdout);"),
 # ---- the code generator
 ("a try is never closed at its end", GEN, "                ...indent(['{', ...indent(body), '}', `rt_try_end(cx, &${t});`]),", "                ...indent(['{', ...indent(body), '}']),"),
 ("a return out of a try leaves it open", GEN, "        out.open.push({ id: -1, thaws: [`rt_try_end(cx, &${t});`] });", "        out.open.push({ id: -1, thaws: [] });"),
 ("the catch's variable is not set", GEN, "                ...indent([`${v} = rt_caught(cx); // $${s.var.name}`, '{', ...indent(handler), '}']),", "                ...indent(['{', ...indent(handler), '}']),"),
 ("the handler runs inside the try", GEN, "        out.open.pop();\n        const handler = s.handler.flatMap(b => genStmt(b, out));", "        const handler = s.handler.flatMap(b => genStmt(b, out));\n        out.open.pop();"),
 ("die carries on", GEN, "            b.lines.push(`rt_die(cx, ${values.c});`);", "            b.lines.push(`rt_warn(cx, ${values.c});`);"),
 ("say STDERR is say", GEN, "        const rt = s.stderr && handle?.kind === 'handle' ? (s.name === 'say' ? handle.say : handle.print) : name.rt;", "        const rt = name.rt;"),
 # ---- the resolver
 ("the catch's variable is in the try's scope", RESOLVE, "            inner(s.body);\n            scopes.push(new Map());\n            of.set(s.var, names.length);", "            scopes.push(new Map());\n            of.set(s.var, names.length);"),
 ("the catch's block is the variable's own scope", RESOLVE, "            declare(s.var);\n            inner(s.handler);", "            declare(s.var);\n            s.handler.forEach(statement);"),
 # ---- the checker and shapes
 ("a die may be tested", CHECK, "    if (isDie(e)) refuse('a die that is tested", "    if (false) refuse('a die that is tested"),
 ("a die may be a left operand", CHECK, "    if (e.kind === 'binary' && isDie(e.left)) refuse(", "    if (false) refuse("),
 ("a die is a statement that only has a value", CHECK, "            || (s.expr.kind === 'listop' && (s.expr.op === 'die' || s.expr.op === 'warn'));", "            || (s.expr.kind === 'listop' && s.expr.op === 'warn');"),
 ("a try's blocks are not checked", CHECK, "    case 'try':\n        s.body.forEach(b => checkStmt(w, b));\n        return s.handler.forEach(b => checkStmt(w, b));", "    case 'try':\n        return;"),
 ("a try's changes are not seen by D69", CHECK, "        case 'try':\n            s.body.forEach(b => stmt(b, fn));\n            return s.handler.forEach(b => stmt(b, fn));", "        case 'try':\n            return;"),
 ("a return in a try is not a sub's", SHAPES, "        case 'try':\n            t.body.forEach(walk);\n            return t.handler.forEach(walk);", "        case 'try':\n            return;"),
 # ---- the parser
 ("a try needs no catch", PARSE, "            if (word.kind !== 'word' || NAMES.get(word.text)?.kind !== 'catch') return refuse('a try has a catch after its block: perl refuses it without one', word.pos);", "            if (word.kind !== 'word' || NAMES.get(word.text)?.kind !== 'catch') return { kind: 'block', body, pos: head.pos };"),
 ("a second catch is read on", PARSE, "            if (more.kind === 'word' && NAMES.get(more.text)?.kind === 'catch') refuse('a second catch: perl takes one', more.pos);\n", ""),
 ("finally is read on", PARSE, "            if (more.kind === 'word' && more.text === 'finally') refuse(", "            if (false) refuse("),
 ("... takes a modifier", PARSE, "            if (!ends(after)) return refuse(\"'...' is a statement alone: perl does not compile anything after it but ';'\", after.pos);\n", ""),
 ("... says nothing", PARSE, "value: 'Unimplemented', pos: head.pos }]", "value: '', pos: head.pos }]"),
 ("or die is taken for a statement's", PARSE, "        if (after.kind === 'op' && infixOp(after.text) && then?.kind === 'word' && then.text === 'die') {", "        if (false) {"),
 ("a message's line is never refused", PARSE, "            if (to !== from.line) refuse(", "            if (false) refuse("),
 ("a while's test is a statement's", PARSE, "            const test = unit(head.pos, bracketed, true);", "            const test = unit(head.pos, bracketed);"),
 ("a message's newline is not looked at", PARSE, "            if (endsInNewline(d)) continue;\n", ""),
 ("a die is not noted in its unit", PARSE, "        if (empty) units.at(-1)?.push(made);\n", ""),
 ("a default is no unit", PARSE, "                        param = { ...param, default: unit(v.pos, () => expression(COMMA_ROW)) };", "                        param = { ...param, default: expression(COMMA_ROW) };"),
 ("an empty die is refused", PARSE, "        if (args.length === 0 && !empty) refuse(", "        if (args.length === 0) refuse("),
 ("STDERR in brackets is taken", PARSE, "                if (after.kind === '(') refuse(`${head.text} ${handle.text} (...)", "                if (false) refuse(`${head.text} ${handle.text} (...)"),
 # ---- the lexer
 ("a line directive is a comment", LEX, "            if (start.col === 1 && /^#[ \\t]*line[ \\t]+[0-9]/", "            if (false && /^#[ \\t]*line[ \\t]+[0-9]/"),
 ("a line directive needs a blank after the #", LEX, "            if (start.col === 1 && /^#[ \\t]*line[ \\t]+[0-9]/", "            if (start.col === 1 && /^#[ \\t]+line[ \\t]+[0-9]/"),
 ("... is refused everywhere", LEX, "            const yada = NAMES.get(op)?.kind === 'yada' && !afterValue();", "            const yada = false;"),
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
for src in sorted(glob.glob('t/3[012][0-9][0-9]-*.pl') + glob.glob('t/008-*.pl')):
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
        if subprocess.run(['cc', '-o', f'build/mut15/{name}', f'build/mut15/{name}.o', 'build/mut15/rt.o', '-lm'], capture_output=True).returncode:
            return False
    else:
        built = subprocess.run(['node', driver, '-o', f'build/mut15/{name}', f't/{name}.pl'], capture_output=True)
        if refused:
            return built.stderr + f'exit: {built.returncode}\n'.encode() == expected
        if built.returncode:
            return False
    try:
        run = checks.run_capped([f'build/mut15/{name}'], env, b'', 20)
    except checks.Runaway:
        return False
    if run is None:
        return False
    got = run.stdout + run.stderr + (f'exit: {run.returncode}\n'.encode() if run.returncode else b'')
    return got == expected

def golden(driver):
    which = ran if driver is None else tests
    with ThreadPoolExecutor(6) as pool:
        return [t[0] for t, ok in zip(which, pool.map(lambda t: passes(t, driver), which)) if not ok]

def unit(tree):
    """How many of the runtime's own tests of unwinding fail, in the copy."""
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'a die puts back', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
    return len(re.findall(r'^not ok', r.stdout, re.M)) if r.returncode else 0

def copy():
    shutil.rmtree('build/mut15/tree', ignore_errors=True)
    for part in ('bin', 'compiler/src', 'runtime'):
        shutil.copytree(part, 'build/mut15/tree/' + part)

def runtime():
    """The copy's runtime, compiled; whether it compiled."""
    return subprocess.run(['cc', '-O1', '-c', '-Ibuild/mut15/tree/runtime', '-o', 'build/mut15/rt.o', 'build/mut15/tree/runtime/rt.c'], capture_output=True).returncode == 0

os.makedirs('build/mut15', exist_ok=True)
copy()
whole, units = golden('build/mut15/tree/bin/curlyc.ts'), unit('build/mut15/tree')
assert whole == [] and units == 0, f'things as they are fail: {whole}, {units} unit tests'
for name, _, _, _ in ran:
    subprocess.run(['cc', '-O0', '-c', '-Iruntime', '-o', f'build/mut15/{name}.o', f'build/mut15/{name}.c'], check=True)
assert runtime() and golden(None) == []
print(f'{len(tests)} golden tests and the unit tests pass as things are', flush=True)
missed = []
for name, path, old, new in MUTATIONS:
    if only and not any(o in name for o in only):
        continue
    copy()
    text = open(path).read()
    assert text.count(old) == 1, (name, text.count(old))
    open('build/mut15/tree/' + path, 'w').write(text.replace(old, new))
    if path in (RT, UNWIND, SORT):
        failed = golden(None) if runtime() else ['the runtime does not compile']
        units = unit('build/mut15/tree')
    else:
        failed = golden('build/mut15/tree/bin/curlyc.ts')
        units = 0
    if failed or units:
        print(f'{name}: golden {len(failed)} ({", ".join(f[:4] for f in failed[:6])}), unit {units}', flush=True)
    else:
        print(f'{name}: golden 0, unit 0   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
