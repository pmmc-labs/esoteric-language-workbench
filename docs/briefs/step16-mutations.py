#!/usr/bin/env python3
"""Break step 16 on purpose, one way at a time, in the runtime and in each
pass of the compiler, and see that a test goes red each time: q, qq, qw
and heredocs (16a), sprintf and printf (16b), ucfirst, lcfirst, rindex,
chomp and chop (16c).

    python3 docs/briefs/step16-mutations.py            # all of them
    python3 docs/briefs/step16-mutations.py "rindex"   # those named so
    python3 docs/briefs/step16-mutations.py --match    # only see that each piece of text is there

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   every test of step 16, t/2600*.pl to t/2899*.pl, and 953 (a
           sub named q), the refused ones too, run with the knobs of
           t/knobs.sh and each test's own `# env:`, as t/run.sh runs them
  unit     the runtime's own test of the format's limit, in the copy

A record of step 16, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
FORMAT_C = 'runtime/format.c'
STRFN = 'runtime/strfn.c'
FORMAT = 'compiler/src/format.ts'
GEN = 'compiler/src/codegen.ts'
CHECK = 'compiler/src/checker.ts'
PARSE = 'compiler/src/parser.ts'
LEX = 'compiler/src/lexer.ts'
NAMES = 'compiler/src/names.ts'
C_FILES = (RT, FORMAT_C, STRFN)
MUTATIONS = [
 # ---- 16a, the lexer
 ("q keeps a backslash before its bracket", LEX, "word === 'q' ? '\\\\' + open + close : ''", "word === 'q' ? '\\\\' : ''"),
 ("q takes away every backslash", LEX, "            } else if (c === '\\\\' && i < end && backslashed.includes(at())) {", "            } else if (c === '\\\\' && i < end) {"),
 ("brackets do not nest", LEX, "            else if (ch === open) depth += 1;", "            else if (ch === open) depth += 0;"),
 ("a backslash does not take the next character with it", LEX, "            if (ch === '\\\\') k += 1;\n            else if (ch === open)", "            if (ch === '\\\\') k += 0;\n            else if (ch === open)"),
 ("qq does not interpolate", LEX, "        const read = body(end, word === 'qq',", "        const read = body(end, false,"),
 ("a backslash before a qq's bracket is taken", LEX, "                if (brackets.includes(at())) refuse(", "                if (false) refuse("),
 ("qw keeps the blanks", LEX, "                if (isBlank(ch)) {\n                    if (w !== '') words.push(w);", "                if (ch === ' ') {\n                    if (w !== '') words.push(w);"),
 ("qw takes a comma", LEX, "                if (ch === ',') refuse(", "                if (false) refuse("),
 ("qw takes a backslash", LEX, "                if (ch === '\\\\') refuse('a backslash in qw", "                if (false) refuse('a backslash in qw"),
 ("qw drops its last word", LEX, "            if (w !== '') words.push(w);\n            take();", "            take();"),
 ("q takes any delimiter", LEX, "        if (close === undefined) {\n            refuse(`${word} takes a bracket", "        if (false) {\n            refuse(`${word} takes a bracket"),
 ("a heredoc in single quotes interpolates", LEX, "        const read = body(bodyEnd, quote !== \"'\", '', indent);", "        const read = body(bodyEnd, true, '', indent);"),
 ("a heredoc in double quotes does not interpolate", LEX, "        const read = body(bodyEnd, quote !== \"'\", '', indent);", "        const read = body(bodyEnd, quote === '\"', '', indent);"),
 ("~ takes no indentation off", LEX, "        const read = body(bodyEnd, quote !== \"'\", '', indent);", "        const read = body(bodyEnd, quote !== \"'\", '', '');"),
 ("a line that does not begin with the indentation is taken", LEX, "                if (at() !== '\\n') refuse(\"a line of a <<~ heredoc", "                if (false) refuse(\"a line of a <<~ heredoc"),
 ("a terminator after blanks ends a heredoc without ~", LEX, "            const blanks = squiggle ? text.length - text.replace(/^[ \\t]*/, '').length : 0;", "            const blanks = text.length - text.replace(/^[ \\t]*/, '').length;"),
 ("a second heredoc on a line is taken", LEX, "        if (heredoc !== undefined) refuse('a second heredoc", "        if (false) refuse('a second heredoc"),
 ("a string past a heredoc's line is taken", LEX, "        if (heredoc !== undefined && line !== heredoc.line) {", "        if (false) {"),
 ("the body is not skipped", LEX, "            [i, line, col] = [heredoc.resume, heredoc.resumeLine, 1];", "            take();"),
 ("the lines after a heredoc are counted one short", LEX, "        const resumeLine = line + 1;", "        const resumeLine = line;"),
 ("a blank after << is taken", LEX, "            refuse(isBlank(at()) || at() === ''", "            if (isBlank(at())) { while (isBlank(at())) take(); } else refuse(isBlank(at()) || at() === ''"),
 ("sub q(...) is a string", LEX, "            && !(tokens.at(-1)?.kind === 'word' && NAMES.get(tokens.at(-1)!.text)?.kind === 'sub')) {", "            ) {"),
 # ---- 16a, the parser
 ("a qw of one word is a list", PARSE, "            const inner: Expr = items.length === 1 ? { ...items[0]!, bracketed: true } : { kind: 'list', items, pos: t.pos, bracketed: true };", "            const inner: Expr = { kind: 'list', items, pos: t.pos, bracketed: true };"),
 ("a qw is not bracketed", PARSE, "            const inner: Expr = items.length === 1 ? { ...items[0]!, bracketed: true } : { kind: 'list', items, pos: t.pos, bracketed: true };", "            const inner: Expr = items.length === 1 ? items[0]! : { kind: 'list', items, pos: t.pos };"),
 ("a qw cannot be sliced", PARSE, "            if (peek().kind !== '[') return inner;\n            const open = next();\n            const indexes = itemsTo(']');\n            if (indexes.length === 0) refuse('a slice with no index', open.pos);\n            if (peek().kind === '[') refuse('an element of an element: an array of arrays is not in the language yet', peek().pos);\n            return { kind: 'slice', items, indexes, pos: open.pos };\n        }\n        if (t.kind === '(') {", "            return inner;\n        }\n        if (t.kind === '(') {"),
 # ---- 16b, the compiler
 ("a format may be a variable", FORMAT, "    if (f.kind !== 'str') {", "    if (f.kind !== 'str' && f.kind !== 'var') {"),
 ("printf's format is not looked at", CHECK, "        if (s.name === 'printf') checkFormat(s.args, 'printf', s.pos);\n", ""),
 ("sprintf's format is not looked at", CHECK, "    if (e.kind === 'listop' && e.op === 'sprintf') checkFormat(e.args, 'sprintf', e.pos);\n", ""),
 ("%c takes a width", FORMAT, "        if (conv === 'c' && (width || precision)) bad(", "        if (false) bad("),
 ("a size letter is taken", FORMAT, "        if (SIZES.includes(conv)) bad(", "        if (false) bad("),
 ("%i is taken", FORMAT, "        if (OTHER[conv] !== undefined) bad(", "        if (false) bad("),
 ("a width of 2^31 is taken", FORMAT, "            if (digits !== '' && Number(digits) > LIMIT) bad(", "            if (false) bad("),
 ("%% takes a width", FORMAT, "        if (conv === '%') bad(", "        if (false) bad("),
 ("a flag on %s is taken", FORMAT, "        const allowed = FLAGS[conv] ?? NUMERIC_FLAGS;", "        const allowed = NUMERIC_FLAGS;"),
 ("sprintf's list is a list of one", CHECK, "    case 'listop': return e.op === 'join' || e.op === 'sprintf' ? [", "    case 'listop': return e.op === 'join' ? ["),
 # ---- 16b, the runtime
 ("the count is not checked", FORMAT_C, "    if (want != a->count - 1) {", "    if (want > a->count - 1) {"),
 ("a star is not counted", FORMAT_C, "        n += 1 + (uint64_t)sw + (uint64_t)sp;", "        n += 1;"),
 ("a negative width pads on the left", FORMAT_C, "            if (w < 0) {\n                s.left = 1;\n                w = -w;", "            if (w < 0) {\n                w = -w;"),
 ("a negative precision is zero", FORMAT_C, "            s.precision = n < 0 ? -1 : n;", "            s.precision = n < 0 ? 0 : n;"),
 ("a star's bound is not looked at", FORMAT_C, "    if (n > INT32_MAX || n < -INT32_MAX) rt_fault(", "    if (0) rt_fault("),
 ("%s pads with blanks under 0", FORMAT_C, "    if (!s->left) put_fill(cx, b, s->zero ? '0' : ' ', pad);", "    if (!s->left) put_fill(cx, b, ' ', pad);"),
 ("%s counts bytes", FORMAT_C, "    uint64_t chars = str->chars;\n    if (s->precision", "    uint64_t chars = str->len;\n    if (s->precision"),
 ("%s's precision is ignored", FORMAT_C, "    if (s->precision >= 0 && (uint64_t)s->precision < chars) chars = (uint64_t)s->precision;", ""),
 ("zero padding goes before the sign", FORMAT_C, "    if (!s->left && !(s->zero && s->precision < 0)) put_fill(cx, b, ' ', pad);\n    put(cx, b, sign, strlen(sign), strlen(sign));\n    if (!s->left && s->zero && s->precision < 0) put_fill(cx, b, '0', pad);", "    if (!s->left && !(s->zero && s->precision < 0)) put_fill(cx, b, ' ', pad);\n    if (!s->left && s->zero && s->precision < 0) put_fill(cx, b, '0', pad);\n    put(cx, b, sign, strlen(sign), strlen(sign));"),
 ("zero padding with a precision", FORMAT_C, "    if (!s->left && s->zero && s->precision < 0) put_fill(cx, b, '0', pad);", "    if (!s->left && s->zero) put_fill(cx, b, '0', pad);"),
 ("a precision of 0 prints the digit 0", FORMAT_C, "    if (!(u == 0 && s->precision == 0)) {", "    {"),
 ("# puts 0x before 0", FORMAT_C, "    else if (s->alt && u != 0 && base == 16)", "    else if (s->alt && base == 16)"),
 ("# on %o puts no zero", FORMAT_C, "    if (s->conv == 'o' && s->alt && (len == 0 || *end != '0') && s->precision <= len) {", "    if (0) {"),
 ("%B is lower case", FORMAT_C, "s->alt && u != 0 && base == 2) sign = s->conv == 'B' ? \"0B\" : \"0b\";", "s->alt && u != 0 && base == 2) sign = \"0b\";"),
 ("+ on %d is ignored", FORMAT_C, "    if (s->conv == 'd') sign = negative ? \"-\" : s->plus ? \"+\" : s->space ? \" \" : \"\";", "    if (s->conv == 'd') sign = negative ? \"-\" : s->space ? \" \" : \"\";"),
 ("a negative Int is no 64 bits to %x", FORMAT_C, "        u = (uint64_t)x.i;", "        u = x.i < 0 ? -(uint64_t)x.i : (uint64_t)x.i;"),
 ("%d of a number past the Ints wraps", FORMAT_C, "        int64_t n = whole_number(cx, x);", "        int64_t n = x.is_int ? x.i : (int64_t)(uint64_t)x.n;"),
 ("an unsigned number past 2^64 is clamped", FORMAT_C, "        else rt_fault(cx, \"a number outside 64 bits where a format wants a whole number\");", "        else u = UINT64_MAX;"),
 ("an unsigned Num from 2^63 faults", FORMAT_C, "        if (t >= TWO_63 && t < 2.0 * TWO_63) u = (uint64_t)t;", "        if (0) u = (uint64_t)t;"),
 ("perl's own %.0f is C's", FORMAT_C, "        char *p = f0convert(d, end + sizeof end, &len);", "        char *p = NULL; (void)f0convert;"),
 ("perl's own %.0f with a flag too", FORMAT_C, "    if (s->conv == 'f' && !s->left && !s->plus && !s->space && !s->zero && !s->alt && s->width == 0 && s->precision == 0) {", "    if (s->conv == 'f' && s->precision == 0) {"),
 ("%.0f rounds up from an odd number", FORMAT_C, "            if (uv & 1 && (double)uv == nv) uv--;", ""),
 ("a negative zero is formatted", FORMAT_C, "    if (negative_zero(cx, v, d)) rt_fault(", "    if (0) rt_fault("),
 ("a string's negative zero is formatted", FORMAT_C, "    if (v.tag != RT_TAG_STR) return 0;\n    const rt_str *s", "    if (1) return 0;\n    const rt_str *s"),
 ("a float's precision is always 6", FORMAT_C, "    int precision = s->precision < 0 ? 6 : (int)s->precision;", "    int precision = 6;"),
 ("# is lost on a float", FORMAT_C, "    if (s->alt) how[k++] = '#';\n    how[k++] = '*';", "    how[k++] = '*';"),
 ("%c of a surrogate is made", FORMAT_C, "    if (below_zero(x) || t > 0x10FFFF || (t >= 0xD800 && t <= 0xDFFF)) rt_fault(cx, \"not a character\");\n    if (x.split) rt_fault(cx, SPLIT);\n    uint32_t c = (uint32_t)t;\n    char bytes[4];", "    if (below_zero(x) || t > 0x10FFFF) rt_fault(cx, \"not a character\");\n    if (x.split) rt_fault(cx, SPLIT);\n    uint32_t c = (uint32_t)t;\n    char bytes[4];"),
 ("undef is the empty string to %s", FORMAT_C, "        if (v.tag == RT_TAG_UNDEF) rt_fault(cx, s.conv == 's'", "        if (v.tag == RT_TAG_UNDEF && s.conv != 's') rt_fault(cx, s.conv == 's'"),
 ("%% is two characters", FORMAT_C, "            put(cx, b, \"%\", 1, 1);", "            put(cx, b, \"%%\", 2, 2);"),
 ("the text after the last conversion is lost", FORMAT_C, "        if (q > p) put(cx, b, p,", "        if (q > p && q < end) put(cx, b, p,"),
 ("printf prints a newline", FORMAT_C, "    emit(cx, made, 0);", "    emit(cx, made, 1);"),
 # ---- 16c
 ("ucfirst changes nothing", STRFN, "    if (s->len > 0 && bytes[0] >= from && bytes[0] <= from + 25) bytes[0] = (char)(bytes[0] - from + to);\n", ""),
 ("ucfirst changes every letter's case", STRFN, "    if (s->len > 0 && bytes[0] >= from && bytes[0] <= from + 25) bytes[0] = (char)(bytes[0] - from + to);\n", "    for (uint64_t k = 0; k < s->len; k++) if (bytes[k] >= from && bytes[k] <= from + 25) bytes[k] = (char)(bytes[k] - from + to);\n"),
 ("ucfirst past ASCII is taken", STRFN, "    if (s->len > 0 && (unsigned char)s->bytes[0] >= 0x80) rt_fault(cx, fault);", "    if (0) rt_fault(cx, fault);"),
 ("rindex moves the position in first", STRFN, "        int64_t p = whole_number(cx, numeric(cx, position));", "        int64_t p = whole_number(cx, numeric(cx, position));\n        if (p < 0) p = 0;"),
 ("rindex takes the position as where the piece ends", STRFN, "        if (__builtin_add_overflow(p, (int64_t)t->chars, &end))", "        if (__builtin_add_overflow(p, (int64_t)0, &end))"),
 ("rindex past the Ints is the end", STRFN, "&end)) rt_fault(cx, \"an rindex position this far past the end has two answers in perl\");", "&end)) end = size;"),
 ("rindex looks in the middle of a character", STRFN, "        if (continues(s->bytes[at])) continue;\n", ""),
 ("rindex counts bytes", STRFN, "return rt_int((int64_t)chars_in(s, (uint64_t)at));", "return rt_int(at);"),
 ("chomp makes a number a string", STRFN, "    if (a.tag != RT_TAG_STR) {\n        if (a.tag != RT_TAG_INT", "    if (a.tag != RT_TAG_STR && a.tag != RT_TAG_NUM) {\n        if (a.tag != RT_TAG_INT"),
 ("chomp takes any last character", STRFN, "    if (s->len == 0 || s->bytes[s->len - 1] != '\\n') return a;", "    if (s->len == 0) return a;"),
 ("chomp of undef is the empty string", STRFN, "    if (a.tag == RT_TAG_UNDEF) rt_fault(cx, \"undef where a string is wanted\");\n    if (a.tag != RT_TAG_STR) {", "    if (a.tag == RT_TAG_UNDEF) return rt_string(&STR_FALSE);\n    if (a.tag != RT_TAG_STR) {"),
 ("chop takes nothing", STRFN, "    uint64_t chars = s->chars > 0 ? s->chars - 1 : 0;", "    uint64_t chars = s->chars;"),
 ("chop takes a byte", STRFN, "    uint64_t len = offset_of(s, chars);\n    char *bytes;\n    const rt_str *less", "    uint64_t len = s->len > 0 ? s->len - 1 : 0;\n    char *bytes;\n    const rt_str *less"),
 ("chomp is a value as itself", PARSE, "            return { kind: 'block', body: [change], pos: head.pos };", "            return change;"),
 ("chomp's value is taken", PARSE, "        if (name?.kind === 'changer') return refuse(`${t.text} is a statement here", "        if (false) return refuse(`${t.text} is a statement here"),
 ("chomp of an element is taken", PARSE, "            if (v.name === '_' || peek().kind === '[' || peek().kind === '{') refuse(one, v.pos);", "            if (v.name === '_') refuse(one, v.pos);"),
 ("chop is chomp", NAMES, "    ['chop', { kind: 'changer', rt: 'rt_chop' }],", "    ['chop', { kind: 'changer', rt: 'rt_chomp' }],"),
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
for src in sorted(glob.glob('t/2[678][0-9][0-9]-*.pl') + glob.glob('t/953-*.pl')):
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
    """How many of the runtime's own tests of the format fail, in the copy."""
    r = subprocess.run(['node', '--test', '--test-name-pattern', 'formatted', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
    if path in C_FILES:
        failed = golden(None) if runtime() else ['the runtime does not compile']
        units = unit('build/mut/tree')
    else:
        failed = golden('build/mut/tree/bin/curlyc.ts')
        units = 0
    if failed or units:
        print(f'{name}: golden {len(failed)} ({", ".join(f[:4] for f in failed[:6])}), unit {units}', flush=True)
    else:
        print(f'{name}: golden 0, unit 0   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
