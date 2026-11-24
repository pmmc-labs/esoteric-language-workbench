#!/usr/bin/env python3
"""Break step 3's runtime on purpose, one way at a time, and see that a
test goes red each time.

    python3 docs/briefs/step3-mutations.py            # all of them
    python3 docs/briefs/step3-mutations.py "D45"      # those named so

runtime/rt.c is read and never written: each broken copy is
build/mut/rt.c, linked with every test's own C, which is compiled once.

A record of step 3, and not part of make test: each breakage is a piece
of the runtime's text as it was then, and one that no longer matches
stops the run. The first run, of 70, let eight through; six were holes
in the tests (t/180 to t/186 are their tests now) and two changed
nothing a program can see, which the list says where they were."""
import subprocess, glob, sys, os
from concurrent.futures import ThreadPoolExecutor
KEEP = open('runtime/rt.c').read()
M = [
 ("no vertical tab among the blanks", "|| c == '\\f' || c == '\\v';", "|| c == '\\f';"),
 ("no form feed among the blanks", "c == '\\r' || c == '\\f' ||", "c == '\\r' ||"),
 ("text after a number is ignored", '    if (p != end) rt_fault(cx, "not a numeric string");\n\n    number v', '\n    number v'),
 ("a string of no digits is 0", '    if (!digits) rt_fault(cx, "not a numeric string");\n', ''),
 ("digits: -2^63 overflows", "if (o || m > (uint64_t)INT64_MAX + (negative ? 1 : 0)) rt_fault", "if (o || m > (uint64_t)INT64_MAX) rt_fault"),
 ("digits: 2^63 allowed", "m > (uint64_t)INT64_MAX + (negative ? 1 : 0)", "m > (uint64_t)INT64_MAX + 1"),
 ("digits: no overflow check", 'if (o || m > (uint64_t)INT64_MAX + (negative ? 1 : 0)) rt_fault(cx, "integer overflow");', ''),
 ("a string float may be infinite", '    if (isinf(x)) rt_fault(cx, "float overflow");\n    int whole', '    int whole'),
 ("exponent, whole: a Num", "    if (exponent && whole && fabs(x) < TWO_53) {", "    if (0 && exponent && whole && fabs(x) < TWO_53) {"),
 ("exponent, whole and large: no fault", "    if (exponent && whole) rt_fault(cx, EXPONENT);\n", ""),
 ("exponent, whole: Int up to 2^53 inclusive", "    if (exponent && whole && fabs(x) < TWO_53) {", "    if (exponent && whole && fabs(x) <= TWO_53) {"),
 ("no soft strings", "    v.soft = whole && fabs(x) < TWO_53;", "    v.soft = 0;"),
 # Not here, being no change to what any program does: `soft` up to 2^53
 # inclusive (a soft string matters only beside an integral operand, and
 # it isn't integral itself from 2^53); an exponent's digits unchecked
 # (the C library's own reading stops at the `e`, and that is checked).
 ("D45 off", "    if ((large_and_exact(p) && !y.plain) || (large_and_exact(q) && !x.plain)) rt_fault(cx, TWO_ANSWERS);", ""),
 ("D45: a string that is an Int counts as one", "    if ((large_and_exact(p) && !y.plain) || (large_and_exact(q) && !x.plain)) rt_fault(cx, TWO_ANSWERS);", "    if ((large_and_exact(p) && !y.is_int) || (large_and_exact(q) && !x.is_int)) rt_fault(cx, TWO_ANSWERS);"),
 ("D45: only the left operand", "    if ((large_and_exact(p) && !y.plain) || (large_and_exact(q) && !x.plain)) rt_fault(cx, TWO_ANSWERS);", "    if ((large_and_exact(p) && !y.plain)) rt_fault(cx, TWO_ANSWERS);"),
 ("D45: from past 2^53", "return m >= (uint64_t)1 << 53 && m >> __builtin_ctzll(m)", "return m > (uint64_t)1 << 53 && m >> __builtin_ctzll(m)"),
 ("D45: every large number", "return m >= (uint64_t)1 << 53 && m >> __builtin_ctzll(m) < (uint64_t)1 << 53;", "return m >= (uint64_t)1 << 53;"),
 ("D45 not in +", "    if (integral(x, &p) && integral(y, &q)) {\n        two_answers(cx, x, y, p, q);\n        int64_t r;\n        int o = __builtin_add_overflow", "    if (integral(x, &p) && integral(y, &q)) {\n        int64_t r;\n        int o = __builtin_add_overflow"),
 ("D45 not in -", "    if (integral(x, &p) && integral(y, &q)) {\n        two_answers(cx, x, y, p, q);\n        int64_t r;\n        int o = __builtin_sub_overflow", "    if (integral(x, &p) && integral(y, &q)) {\n        int64_t r;\n        int o = __builtin_sub_overflow"),
 ("D45 not in *", "    if (integral(x, &p) && integral(y, &q)) {\n        two_answers(cx, x, y, p, q);\n        int64_t r;\n        int o = __builtin_mul_overflow", "    if (integral(x, &p) && integral(y, &q)) {\n        int64_t r;\n        int o = __builtin_mul_overflow"),
 ("soft: the operands unchecked", "    if (magnitude(p) >= (uint64_t)1 << 53 || magnitude(q) >= (uint64_t)1 << 53) rt_fault(cx, SOFT);\n", ""),
 ("soft: the answer unchecked", "    if (overflowed || magnitude(exact) >= (uint64_t)1 << 53) rt_fault(cx, SOFT);", ""),
 ("soft: an answer of 2^53 allowed", "    if (overflowed || magnitude(exact) >= (uint64_t)1 << 53) rt_fault(cx, SOFT);", "    if (overflowed || magnitude(exact) > (uint64_t)1 << 53) rt_fault(cx, SOFT);"),
 ("soft +: integer arithmetic", "        if (!soft_pair(cx, x, y, p, q)) return checked(cx, r, o);\n        soft_answer(cx, r, o);\n    }\n    return num(cx, as_double(x) + as_double(y));", "        return checked(cx, r, o);\n    }\n    return num(cx, as_double(x) + as_double(y));"),
 ("soft **: the answer unchecked", "                if (o || reached >= (uint64_t)1 << 53) rt_fault(cx, SOFT);", ""),
 ("soft **: the integer route", "        if (soft_pair(cx, left, right, x, y)) {", "        if (0) {"),
 ("soft /: not checked", "    int soft = whole && soft_pair(cx, x, y, p, q);", "    int soft = 0; (void)whole;"),
 ("string * string overflow goes to floats", "            if ((x.is_int && y.is_int) || (positive && !past))", "            if ((x.plain && y.plain) || (positive && !past))"),
 ("minus: a plus is fine", "        if (a.as.s->bytes[0] == '+') rt_fault(cx, \"a minus before a string that starts with a plus\");\n", ""),
 ("minus: large is fine", "        if (d == trunc(d) && fabs(d) >= TWO_53) rt_fault(cx, NEG_LARGE);\n", ""),
 ("minus: an Int for a string of digits", "        double d = as_double(x);\n        if (d == trunc(d) && fabs(d) >= TWO_53) rt_fault(cx, NEG_LARGE);\n        return rt_num(-d);", "        double d = as_double(x);\n        if (d == trunc(d) && fabs(d) >= TWO_53) rt_fault(cx, NEG_LARGE);\n        if (x.is_int) return rt_int(-x.i);\n        return rt_num(-d);"),
 ("whole number: no range", '    if (!(t >= -TWO_63 && t < TWO_63)) rt_fault(cx, "a number outside the integers where a whole number is wanted");\n', '    if (!(t >= -TWO_63 && t < TWO_63)) t = 0;\n'),
 ("x: a count below zero repeats nothing", '    if (below_zero(c)) rt_fault(cx, "negative repeat count");\n', '    if (below_zero(c)) c.is_int = 1, c.i = 0;\n'),
 ("x: only a whole count below zero faults", '    if (below_zero(c)) rt_fault(cx, "negative repeat count");\n', '    if (whole_number(cx, c) < 0) rt_fault(cx, "negative repeat count");\n'),
 ("x: one more character allowed", "n > (uint64_t)INT32_MAX / s->chars", "n > ((uint64_t)INT32_MAX + 1) / s->chars"),
 ("x: characters counted as bytes", "str_new(cx, s->len * n, s->chars * n, &bytes)", "str_new(cx, s->len * n, s->len * n, &bytes)"),
 ("concat: characters counted as bytes", "str_new(cx, s->len + t->len, s->chars + t->chars, &bytes)", "str_new(cx, s->len + t->len, s->chars + t->len, &bytes)"),
 ("length in bytes", "    return rt_int((int64_t)to_str(cx, a)->chars);", "    return rt_int((int64_t)to_str(cx, a)->len);"),
 ("uc: not z", "c >= from && c <= from + 25", "c >= from && c <= from + 24"),
 ("uc: one past z", "c >= from && c <= from + 25", "c >= from && c <= from + 26"),
 ("uc and lc past ASCII: no fault", "    if (s->len != s->chars) rt_fault(cx, fault);\n", ""),
 ("ord: the first byte", "    return rt_int((int64_t)decode(s->bytes, &size));", "    (void)size; return rt_int((int64_t)(unsigned char)s->bytes[0]);"),
 ("chr: U+110000", "t > 0x10FFFF ||", "t > 0x110000 ||"),
 ("chr: surrogates", " || (t >= 0xD800 && t <= 0xDFFF)) rt_fault", ") rt_fault"),
 ("chr: the first surrogate", "(t >= 0xD800 && t <= 0xDFFF)", "(t > 0xD800 && t <= 0xDFFF)"),
 ("chr: the last surrogate", "(t >= 0xD800 && t <= 0xDFFF)", "(t >= 0xD800 && t < 0xDFFF)"),
 ("chr: below zero cut to 0", "    if (below_zero(v) || t > 0x10FFFF", "    if (t < 0 || t > 0x10FFFF"),
 ("chr: U+0800 in two bytes", "c < 0x800 ? 2", "c <= 0x800 ? 2"),
 ("chr: U+10000 in three bytes", "c < 0x10000 ? 3", "c <= 0x10000 ? 3"),
 ("chr: U+0080 in one byte", "int size = c < 0x80 ? 1", "int size = c <= 0x80 ? 1"),
 ("substr: a start at the end faults", "    if (start > size || (start < 0 && end < 0))", "    if (start >= size || (start < 0 && end < 0))"),
 ("substr: before the beginning is fine", "    if (start > size || (start < 0 && end < 0))", "    if (start > size)"),
 ("substr: an end at the beginning faults", "(start < 0 && end < 0))", "(start < 0 && end <= 0))"),
 ("substr: any end before the beginning faults", "(start < 0 && end < 0))", "(end < 0))"),
 ("substr: a sum past the Ints wraps", "    if (has_count && n >= 0 && __builtin_add_overflow(start, n, &end)) end = INT64_MAX;", "    if (has_count && n >= 0) end = (int64_t)((uint64_t)start + (uint64_t)n);"),
 ("substr: a negative length counts from the start", "    if (has_count && n < 0) end = size + n;", "    if (has_count && n < 0) end = start + n;"),
 ("substr: positions in bytes", "    uint64_t from = offset_of(s, (uint64_t)start);\n    uint64_t to = offset_of(s, (uint64_t)end);", "    uint64_t from = (uint64_t)start;\n    uint64_t to = (uint64_t)end;"),
 ("index: a position past the end", "    if (position > (int64_t)s->chars) position = (int64_t)s->chars;\n", ""),
 ("index: a position below zero", "    if (position < 0) position = 0;\n    if (position > (int64_t)s->chars)", "    if (position < 0) return rt_int(-1);\n    if (position > (int64_t)s->chars)"),
 ("index: the answer in bytes", "return rt_int((int64_t)chars_in(s, at));", "return rt_int((int64_t)at);"),
 ("index: the position in bytes", "    for (uint64_t at = offset_of(s, (uint64_t)position);", "    for (uint64_t at = (uint64_t)position;"),
 ("print: noncharacters", '                if (noncharacter(decode(s->bytes + at, &size))) rt_fault(cx, "a noncharacter printed");', '                decode(s->bytes + at, &size);'),
 ("print: past ASCII without use open", '            if (!cx->out_utf8) rt_fault(cx, "a character past ASCII printed without \'use open\'");\n', ''),
 ("noncharacter: only U+FFFE and U+FFFF", "(c & 0xFFFE) == 0xFFFE;", "c == 0xFFFE || c == 0xFFFF;"),
 ("noncharacter: not U+FDEF", "c <= 0xFDEF", "c < 0xFDEF"),
 ("noncharacter: not U+FDD0", "c >= 0xFDD0", "c > 0xFDD0"),
 ("print adds a newline", "    emit(cx, v, 0);", "    emit(cx, v, 1);"),
 ("a number as a string: no window", "    if (x == trunc(x) && fabs(x) >= 1e15 && fabs(x) < TWO_53) rt_fault(cx, WHOLE_FLOAT);\n", ""),
]
only = sys.argv[1:]
os.makedirs('build/mut', exist_ok=True)
tests = []
for src in sorted(glob.glob('t/04*.pl') + glob.glob('t/07[5-8]*.pl') + glob.glob('t/09*.pl') + glob.glob('t/1[0-8]*.pl')):
    if 'kind: refused' in open(src, encoding='utf-8', errors='replace').read(400):
        continue
    name = os.path.basename(src)[:-3]
    tests.append((name, open(src[:-3] + '.expected', 'rb').read()))

def prepare(test):
    name = test[0]
    r = subprocess.run(['node', 'bin/curlyc.ts', '-o', f'build/mut/{name}', f't/{name}.pl'], capture_output=True)
    assert r.returncode == 0, (name, r.stderr)
    subprocess.run(['cc', '-O0', '-c', '-Iruntime', '-o', f'build/mut/{name}.o', f'build/mut/{name}.c'], check=True)

def passes(test):
    name, expected = test
    if subprocess.run(['cc', '-o', f'build/mut/{name}', f'build/mut/{name}.o', 'build/mut/rt.o', '-lm']).returncode:
        return False
    try:
        r = subprocess.run([f'build/mut/{name}'], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
    except subprocess.TimeoutExpired:
        return False
    got = r.stdout + (f'exit: {r.returncode}\n'.encode() if r.returncode else b'')
    return got == expected

def failures(source):
    open('build/mut/rt.c', 'w').write(source)
    c = subprocess.run(['cc', '-O1', '-c', '-Iruntime', '-o', 'build/mut/rt.o', 'build/mut/rt.c'], capture_output=True, text=True)
    if c.returncode:
        return None
    with ThreadPoolExecutor(3) as pool:
        return [t[0] for t, ok in zip(tests, pool.map(passes, tests)) if not ok]

with ThreadPoolExecutor(3) as pool:
    list(pool.map(prepare, tests))
whole = failures(KEEP)
assert whole == [], f'the runtime as it is fails: {whole}'
print(f'{len(tests)} tests pass with the runtime as it is', flush=True)
missed = []
for name, old, new in M:
    if only and not any(o in name for o in only):
        continue
    assert KEEP.count(old) == 1, (name, KEEP.count(old))
    failed = failures(KEEP.replace(old, new))
    if failed is None:
        print(f'{name}: DOES NOT COMPILE', flush=True)
        missed.append(name)
    elif failed:
        print(f'{name}: {len(failed)} fail ({", ".join(f[:3] for f in failed[:8])})', flush=True)
    else:
        print(f'{name}: 0 fail   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
