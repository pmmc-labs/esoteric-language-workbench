#!/usr/bin/env python3
"""Break step 12a's hashes on purpose, one way at a time, in the runtime's
table and in each pass of the compiler, and see that a test goes red each
time.

    python3 docs/briefs/step12a-mutations.py            # all of them
    python3 docs/briefs/step12a-mutations.py "delete"   # those named so
    python3 docs/briefs/step12a-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 12a, t/1500*.pl to t/1606*.pl, the refused
           ones too, run with the knobs of t/knobs.sh and each test's own
           `# env:`, as t/run.sh runs them. For a broken runtime each
           test's C is compiled once, by the compiler as it is, and
           linked again with the broken runtime; for a broken compiler
           each is compiled again by the copy
  unit     the runtime's own tests of its hash table, in the copy

A record of step 12a, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
HASH = 'runtime/hash.c'
SORT = HASH
GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
CHECK = 'compiler/src/checker.ts'
PARSE = 'compiler/src/parser.ts'
LEX = 'compiler/src/lexer.ts'
SHAPES = 'compiler/src/shapes.ts'
FIND = "    int64_t pair = hash_find(cx, h, to_str(cx, key, &number));\n    return pair < 0 ? rt_undef() : h->items[2 * pair + 1];"
EXISTS = "    return rt_bool(hash_find(cx, h, to_str(cx, key, &number)) >= 0);"
LOOP = "    for (uint64_t k = 0; k < h->count; k += 2) {\n        if (h->items[k].tag == RT_TAG_ABSENT) continue;\n        if (step == 1"
MUTATIONS = [
 # ---- the runtime's table
 ("a hole's key is looked at", HASH, "        if (k.tag == RT_TAG_ABSENT) continue;\n        if (k.tag != RT_TAG_STR)", "        if (k.tag != RT_TAG_STR)"),
 ("keys are the same if they are as long", HASH, "    return a->len == b->len && (a->len == 0 || memcmp(a->bytes, b->bytes, a->len) == 0);", "    return a->len == b->len;"),
 ("keys are the same if they begin the same", HASH, "memcmp(a->bytes, b->bytes, a->len) == 0);", "memcmp(a->bytes, b->bytes, 1) == 0);"),
 ("keys are the same if one begins the other", HASH, "    return a->len == b->len && (a->len == 0 ||", "    return (a->len == 0 && b->len == 0) || (a->len != 0 && a->len <= b->len &&"),
 ("the index grows too late", HASH, "    if (2 * (h->count / 2 + 1) > h->slots) hash_index(cx, h, 1);", "    if (h->count / 2 + 1 > 4 * h->slots + 8) hash_index(cx, h, 1);"),
 ("a delete does not count its hole", HASH, "    h->gone += 1;\n", ""),
 ("a delete gives nothing back", HASH, "    if (h->gone > h->count / 4) hash_index(cx, h, 0);\n    return was;", "    if (h->gone > h->count / 4) hash_index(cx, h, 0);\n    return rt_undef();"),
 ("a delete leaves the value where it was", HASH, "    h->items[2 * pair].tag = RT_TAG_ABSENT;\n", ""),
 ("a store to a key that is there adds it again", HASH, "    if (found >= 0) return found;", "    if (0) return found;"),
 ("a new key's value is its key", HASH, "    h->items[h->count++] = rt_undef();\n    index_add", "    h->items[h->count++] = k;\n    index_add"),
 ("a number is a key as it is", HASH, "    rt_value k = key.tag == RT_TAG_STR ? key : rt_concat(cx, key, rt_string(&STR_FALSE));", "    rt_value k = key;"),
 ("the count is of the holes too", HASH, "    return rt_int((int64_t)(h->count / 2 - h->gone));", "    return rt_int((int64_t)(h->count / 2));"),
 ("keys are the values", HASH, "        if (step == 1 || from == 0) to->items[to->count++] = h->items[k];", "        if (step == 1 || from == 0) to->items[to->count++] = h->items[k + 1];"),
 ("a hole is in the list", HASH, LOOP, "    for (uint64_t k = 0; k < h->count; k += 2) {\n        if (step == 1"),
 ("the last key is the first in a list", HASH, LOOP, "    for (uint64_t j = 0; j < h->count; j += 2) {\n        uint64_t k = h->count - 2 - j;\n        if (h->items[k].tag == RT_TAG_ABSENT) continue;\n        if (step == 1"),
 ("an odd list is taken", HASH, "    if ((from->count - first) % 2 != 0) rt_fault(", "    if (0) rt_fault("),
 ("an odd list is one that has a value over after two", HASH, "    if ((from->count - first) % 2 != 0) rt_fault(", "    if ((from->count - first) % 2 != 0 && from->count - first > 2) rt_fault("),
 ("an assignment keeps the keys that were there", HASH, "    h->count = 0;\n    h->gone = 0;\n    hash_index(cx, h, (from->count - first) / 2);", "    hash_index(cx, h, (from->count - first) / 2);"),
 ("a key given twice keeps its first value", HASH, "        h->items[2 * pair + 1] = scalar(cx, from->items[k + 1]);", "        if (h->items[2 * pair + 1].tag == RT_TAG_UNDEF) h->items[2 * pair + 1] = scalar(cx, from->items[k + 1]);"),
 ("the rest of a list begins one early", HASH, "    uint64_t first = (uint64_t)n < from->count ? (uint64_t)n : from->count;", "    uint64_t first = (uint64_t)n < from->count ? (uint64_t)(n > 0 ? n - 1 : 0) : from->count;"),
 ("an undef key is read as the empty string", HASH, FIND, "    int64_t pair = hash_find(cx, h, to_str(cx, key.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : key, &number));\n    return pair < 0 ? rt_undef() : h->items[2 * pair + 1];"),
 ("a read makes the key", HASH, FIND, "    (void)number; (void)h;\n    return h->items[2 * hash_make(cx, hash, key) + 1];"),
 ("exists makes the key", HASH, EXISTS, "    (void)number; (void)h;\n    return rt_bool(hash_make(cx, hash, key) >= 0);"),
 ("exists asks for a value that is defined", HASH, EXISTS, "    int64_t at = hash_find(cx, h, to_str(cx, key, &number));\n    return rt_bool(at >= 0 && h->items[2 * at + 1].tag != RT_TAG_UNDEF);"),
 ("exists is always true", HASH, EXISTS, "    (void)number; (void)h;\n    return rt_bool(1);"),
 ("a frozen hash may be changed", HASH, 'if (h->frozen != 0) rt_fault(cx, "a hash was changed while a foreach is over it");', 'if (0) rt_fault(cx, "a hash was changed while a foreach is over it");'),
 ("the index is not counted against the cap", HASH, "        cx->held = cx->held - was + now;\n", ""),
 ("an array may be read as a hash", HASH, '    if (v.tag != RT_TAG_HASH) rt_fault(cx, "not a hash");', '    if (v.tag != RT_TAG_HASH && v.tag != RT_TAG_ARRAY) rt_fault(cx, "not a hash");'),
 ("a hash in a slot is not a root", RT, "            if (v.tag == RT_TAG_ARRAY || v.tag == RT_TAG_HASH) {\n                rt_array *a = v.as.a;", "            if (v.tag == RT_TAG_HASH) continue;\n            if (v.tag == RT_TAG_ARRAY) {\n                rt_array *a = v.as.a;"),
 # ---- the lexer
 ("a word in braces may be on another line", LEX, "                    if (near !== from || src[past(wordEnd(near), false)] !== '}') {", "                    if (false) {"),
 ("a word and a comment in braces", LEX, "                    if (near !== from || src[past(wordEnd(near), false)] !== '}') {", "                    if (near !== from) {"),
 ("a word before => may be on another line", LEX, "            if (!src.startsWith('=>', past(wordEnd(i), false))) {", "            if (false) {"),
 ("=> makes no string of a word of the language's", LEX, "        } else if (isWordStart(c) && !afterValue() && src.startsWith('=>', past(wordEnd(i), true))) {", "        } else if (isWordStart(c) && !afterValue() && !NAMES.has(src.slice(i, wordEnd(i))) && src.startsWith('=>', past(wordEnd(i), true))) {"),
 ("a word in braces that is one of the language's is no string", LEX, "                if (isWordStart(src[from] ?? '') && src[past(wordEnd(from), true)] === '}') {", "                if (isWordStart(src[from] ?? '') && !NAMES.has(src.slice(from, wordEnd(from))) && src[past(wordEnd(from), true)] === '}') {"),
 ("a word in braces with blanks round it is no string", LEX, "                    run(ch => ch === ' ' || ch === '\\t');\n                    bare();", "                    if (near === i) bare();"),
 ("a brace that closes a key ends no value", LEX, "            || (last?.kind === '}' && last.subscript === true)\n", ""),
 ("a step after an element ends no value", LEX, "            return target?.kind === 'var' || target?.kind === ']' || (target?.kind === '}' && target.subscript === true);", "            return target?.kind === 'var';"),
 ("-word in braces is the parser's", LEX, "                if (src[sign] === '-' && isWordStart(src[sign + 1] ?? '')", "                if (false && isWordStart(src[sign + 1] ?? '')"),
 ("%_ may be named", LEX, """            if (name === '_') refuse("%_ is perl's own, and not in the language", start);\n""", ""),
 ("%h{ is the hash", LEX, "            if (at() === '{') refuse(`%${name}{...} is a slice of keys and values, and not in the language`, start);\n", ""),
 ("a % after a value is a hash", LEX, "        } else if (c === '%' && !afterValue()) {", "        } else if (c === '%' && isWordStart(src[i + 1] ?? '')) {"),
 # ---- the parser
 ("$h{} is read on", PARSE, "        if (peek().kind === '}') refuse(`$${v.text.slice(1)}{} has no key: perl does not compile it`, open.pos);\n", ""),
 ("an element of an element is read on", PARSE, "        if (peek().kind === '{' || peek().kind === '[') refuse('an element of an element: a hash of hashes or of arrays is not in the language yet', peek().pos);\n", ""),
 ("a blank before a key's brace is read on", PARSE, "        if (after.kind === '{') refuse(`a blank between ${v.text} and '{': an element of a hash is written ${v.text}{...}`, after.pos);\n", ""),
 ("exists takes what binds tighter", PARSE, "        if (after.kind === '[' || (after.kind === 'op' && (infixOp(after.text)?.row ?? Infinity) < NAMED_UNARY_ROW)) {", "        if (false) {"),
 ("exists may stand before a sum", PARSE, "(infixOp(after.text)?.row ?? Infinity) < NAMED_UNARY_ROW)) {", "(infixOp(after.text)?.row ?? Infinity) < NAMED_UNARY_ROW - 2)) {"),
 ("exists may not stand before a comparison", PARSE, "(infixOp(after.text)?.row ?? Infinity) < NAMED_UNARY_ROW)) {", "(infixOp(after.text)?.row ?? Infinity) < NAMED_UNARY_ROW + 3)) {"),
 ("-word before => is the word", PARSE, "            if (t.bare && sign?.kind === 'op' && prefixOp(sign.text)?.sign) {", "            if (false) {"),
 ("keys(%h)[0] is read on", PARSE, "            if (peek().kind === '[') refuse(`'[' after ${head.text}(...): perl does not compile it; bracket the whole, (${head.text}(...))[...]`, peek().pos);\n        } else {\n            bareOperand", "        } else {\n            bareOperand"),
 ("keys takes an array", PARSE, "            if (what.kind !== 'hash') return refuse(", "            if (what.kind !== 'hash' && what.kind !== 'array') return refuse("),
 ("a comma in a map's block has the old message", PARSE, "            if (blocks > 0) refuse(\"a comma in the block of a map, a grep or a sort: put the list in brackets, map { ($_ => 1) } ...\", after.pos);\n", ""),
 ("a hash parameter is read on", PARSE, "                if (v.kind === 'hash') return refuse(`${v.text} as a parameter is not in the language yet (step 12b)`, v.pos);\n", ""),
 ("scalar(%h) is not taken", PARSE, "        if (name.shape === 'scalar' && (peek().kind === 'hash' || ", "        if (name.shape === 'scalar' && (false || "),
 ("a hash takes any assigning operator", PARSE, "                    if (t.text !== '=') refuse(`'${t.text}' on ${left.hash", "                    if (t.text !== '=' && !left.hash) refuse(`'${t.text}' on ${left.hash"),
 # ---- the resolver
 ("keys names its hash for a loop", RESOLVE, "            return hash(e, e.name, e.op === 'keys' || e.op === 'count');", "            return hash(e, e.name, false);"),
 ("values names nothing for a loop", RESOLVE, "            return hash(e, e.name, e.op === 'keys' || e.op === 'count');", "            return hash(e, e.name, true);"),
 ("a hash may be named in a loop's list", RESOLVE, "        if (!quoted && !counted && naming.length > 0) {", "        if (false) {"),
 ("%h is found where @h is", RESOLVE, "        const found = [...scopes].reverse().find(scope => scope.has('%' + name));\n        if (found === undefined) return refuse(`%${name} is not declared: my %${name}`, at);\n        of.set(e, found.get('%' + name)!);", "        const found = [...scopes].reverse().find(scope => scope.has('%' + name) || scope.has('@' + name));\n        if (found === undefined) return refuse(`%${name} is not declared: my %${name}`, at);\n        of.set(e, (found.get('%' + name) ?? found.get('@' + name))!);"),
 ("a second my %h is taken", RESOLVE, "(d.kind === 'myarray' ? (d.hash ? '%' : '@') : '') + d.name;", "(d.kind === 'myarray' ? (d.hash ? '%' + scopes.length + ' ' + names.length : '@') : '') + d.name;"),
 ("a builtin's refusal is at its word", RESOLVE, "        const at = e.kind === 'hashop' ? e.at : e.pos;", "        const at = e.pos;"),
 # ---- the checker
 ("a delete is no change", CHECK, "    if (e.kind === 'hashop' && e.op === 'delete') return [id(e)];\n", ""),
 ("values names nothing", CHECK, "    else if (e.kind === 'hashop' && e.op === 'values') id(e);\n", ""),
 ("keys names its hash", CHECK, "    else if (e.kind === 'hashop' && e.op === 'values') id(e);", "    else if (e.kind === 'hashop' && (e.op === 'values' || e.op === 'keys')) id(e);"),
 ("a delete alone is no statement", CHECK, "            || (s.expr.kind === 'hashop' && s.expr.op === 'delete')\n", ""),
 ("exists alone has the old message", CHECK, "        if (!does && !last && s.expr.kind === 'hashop') refuse('this statement only has a value, and nothing is done with it', s.pos);\n", ""),
 ("a key is checked as an index", CHECK, "    if (e.kind === 'elem' && !e.hash) {", "    if (e.kind === 'elem') {"),
 ("a hash may be any target", CHECK, "            if (array && n !== e.targets.length - 1) refuse(", "            if (array && !t.hash && n !== e.targets.length - 1) refuse("),
 ("a key's own expression is not checked", CHECK, "    case 'hashop': return e.key === undefined ? [] : [[e.key, 'scalar']];\n", ""),
 ("a key is not a part of its builtin", CHECK, "    : e.kind === 'hashop' ? (e.key === undefined ? [] : [e.key])\n", ""),
 ("an index may change what a concatenation on the right reads (T230)", CHECK, "            if (changed !== undefined || through !== undefined) {", "            if (false) {"),
 ("only the index itself, and no sub it calls, is looked at (T230)", CHECK, "            if (changed !== undefined || through !== undefined) {", "            if (changed !== undefined) {"),
 ("an interpolated string is no row (T230)", CHECK, " || (v.kind === 'interp' && v.parts.length > 1));\n            const names", ");\n            const names"),
 ("length of a hash is taken", CHECK, "    if (e.kind === 'apply' && (e.name === 'length' || e.name === 'defined') && of?.kind === 'array') {", "    if (e.kind === 'apply' && (e.name === 'length' || e.name === 'defined') && of?.kind === 'array' && !of.hash) {"),
 ("keys is one value to a return", SHAPES, "    case 'hashop': return e.op === 'keys' || e.op === 'values';\n", ""),
 ("a hash is one value to a return", SHAPES, "    case 'array': return true;", "    case 'array': return !e.hash;"),
 # ---- the code generator
 ("a hash in a list is its values", GEN, "${e.hash ? 'rt_list_add_pairs' : 'rt_list_add_all'}", "${e.hash ? 'rt_list_add_values' : 'rt_list_add_all'}"),
 ("values are the keys", GEN, "        b.lines.push(`rt_list_add_${e.op}(cx, ${list}, ${variable(b, e)});`);", "        b.lines.push(`rt_list_add_keys(cx, ${list}, ${variable(b, e)});`);"),
 ("keys in one arm of a ? : is its count", GEN, "        || (e.kind === 'hashop' && (e.op === 'keys' || e.op === 'values'))\n        || e.kind === 'binder' || e.kind === 'sort'\n        || (e.kind === 'ternary' && (listy(e.then) || listy(e.else)))\n        || (e.kind === 'binary' && infixOp(e.op)?.when !== undefined && listy(e.right));\n};\n\n// Where perl", "        || e.kind === 'binder' || e.kind === 'sort'\n        || (e.kind === 'ternary' && (listy(e.then) || listy(e.else)))\n        || (e.kind === 'binary' && infixOp(e.op)?.when !== undefined && listy(e.right));\n};\n\n// Where perl"),
 ("delete only asks", GEN, "        return temp(b, `rt_hash_${e.op}(cx, ${variable(b, e)}, ${key.c})`);", "        return temp(b, `rt_hash_exists(cx, ${variable(b, e)}, ${key.c})`);"),
 ("exists deletes", GEN, "        return temp(b, `rt_hash_${e.op}(cx, ${variable(b, e)}, ${key.c})`);", "        return temp(b, `rt_hash_delete(cx, ${variable(b, e)}, ${key.c})`);"),
 ("a store works its key out first", GEN, "                const value = genExpr(e.value, b);\n                const at = genExpr(e.target.index, b);", "                const at = genExpr(e.target.index, b);\n                const value = genExpr(e.value, b);"),
 ("an operator's right side is worked out before the key is made", GEN, "            const at = index(b, e.target);\n            if (op.when !== undefined) {", "            if (op.when === undefined && e.target.hash) {\n                const value = genExpr(e.value, b);\n                const at = index(b, e.target);\n                const was = temp(b, `${elem(e.target)}_get(cx, ${array}, ${at})`);\n                const now = temp(b, `${op.rt}(cx, ${was.c}, ${value.c})`);\n                b.lines.push(`${elem(e.target)}_put(cx, ${array}, ${at}, ${now.c});`);\n                return now;\n            }\n            const at = index(b, e.target);\n            if (op.when !== undefined) {"),
 ("&&= makes no key", GEN, "            const at = index(b, e.target);\n            if (op.when !== undefined) {", "            if (op.when !== undefined && e.target.hash && e.op === '&&=') {\n                const had = temp(b, `rt_helem(cx, ${array}, ${genExpr(e.target.index, b).c})`);\n                b.lines.push(`if (rt_is_true(cx, ${had.c})) {`);\n                const put = temp(b, `rt_helem_store(cx, ${array}, ${genExpr(e.target.index, b).c}, ${genExpr(e.value, b).c})`);\n                b.lines.push(`${had.c} = ${put.c};`, '}');\n                return had;\n            }\n            const at = index(b, e.target);\n            if (op.when !== undefined) {"),
 ("a my of a hash keeps the hash its slot held", GEN, "`rt_hash_new(cx); // my %${e.name}`", "`(${variable(b, e)}.tag == RT_TAG_HASH ? ${variable(b, e)} : rt_hash_new(cx)); // my %${e.name}`"),
 ("a file's hash is made as an array", GEN, "${names.isHash[id] ? 'rt_hash_new(cx)' : names.isArray[id] ? 'rt_array_new(cx)' : 'rt_undef()'}", "${names.isArray[id] ? 'rt_array_new(cx)' : 'rt_undef()'}"),
 ("a hash where one value is wanted is twice its count", GEN, "    case 'array': return temp(b, `${e.hash ? 'rt_hash_count' : 'rt_count'}(cx, ${variable(b, e)})`);", "    case 'array': if (e.hash) { const n = temp(b, `rt_hash_count(cx, ${variable(b, e)})`); return temp(b, `rt_add(cx, ${n.c}, ${n.c})`); } return temp(b, `rt_count(cx, ${variable(b, e)})`);"),
 ("a hash as the last target takes the whole list", GEN, "b.lines.push(`${t.hash ? 'rt_hash_rest' : 'rt_array_rest'}(cx, ${variable(b, t)}, ${values.c}, ${n});`);", "b.lines.push(`${t.hash ? 'rt_hash_rest' : 'rt_array_rest'}(cx, ${variable(b, t)}, ${values.c}, ${t.hash ? 0 : n});`);"),
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
for src in sorted(glob.glob('t/15[0-9][0-9]-*.pl') + glob.glob('t/16[0-9][0-9]-*.pl')):
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
