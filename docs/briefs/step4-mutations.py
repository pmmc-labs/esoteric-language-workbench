#!/usr/bin/env python3
"""Break step 4's runtime on purpose, one way at a time, and see that a
test goes red each time.

    python3 docs/briefs/step4-mutations.py            # all of them
    python3 docs/briefs/step4-mutations.py "truth"    # those named so

runtime/rt.c is read and never written: each broken copy is
build/mut/rt.c, linked with every test's own C, which is compiled once.

A record of step 4, and not part of make test: each breakage is a piece
of the runtime's text as it was then, and one that no longer matches
stops the run."""
import subprocess, glob, sys, os
from concurrent.futures import ThreadPoolExecutor
KEEP = open('runtime/rt.c').read()
M = [
 ("true as a string is empty", 'static const rt_str STR_TRUE = { 1, 1, "1" };', 'static const rt_str STR_TRUE = { 0, 0, "" };'),
 ("false as a string is 0", 'static const rt_str STR_FALSE = { 0, 0, "" };', 'static const rt_str STR_FALSE = { 1, 1, "0" };'),
 ("undef as a string is empty", '    if (v.tag == RT_TAG_UNDEF) rt_fault(cx, "undef where a string is wanted");\n', '    if (v.tag == RT_TAG_UNDEF) return &STR_FALSE;\n'),
 ("undef as a number is 0", '    case RT_TAG_UNDEF:\n        rt_fault(cx, "undef where a number is wanted");', '    case RT_TAG_UNDEF:\n        x.is_int = 1; x.plain = 1; return x;'),
 ("a boolean is not a plain Int", "        x.is_int = 1;\n        x.plain = 1;\n        x.i = v.as.i;\n        return x;\n    case RT_TAG_UNDEF:", "        x.is_int = 1;\n        x.i = v.as.i;\n        return x;\n    case RT_TAG_UNDEF:"),
 ("a boolean as a number, the other way", "        x.plain = 1;\n        x.i = v.as.i;\n        return x;\n    case RT_TAG_UNDEF:", "        x.plain = 1;\n        x.i = !v.as.i;\n        return x;\n    case RT_TAG_UNDEF:"),
 ("a boolean as a number is a Num", "        x.is_int = 1;\n        x.plain = 1;\n        x.i = v.as.i;\n        return x;\n    case RT_TAG_UNDEF:", "        x.n = (double)v.as.i;\n        return x;\n    case RT_TAG_UNDEF:"),
 ("the length of an undef faults", "    if (a.tag == RT_TAG_UNDEF) return a;\n", ""),
 ("the length of an undef is 0", "    if (a.tag == RT_TAG_UNDEF) return a;\n", "    if (a.tag == RT_TAG_UNDEF) return rt_int(0);\n"),
 ("truth: the string 0 is true", "return !(v.as.s->len == 0 || (v.as.s->len == 1 && v.as.s->bytes[0] == '0'));", "return !(v.as.s->len == 0);"),
 ("truth: the empty string is true", "return !(v.as.s->len == 0 || (v.as.s->len == 1 && v.as.s->bytes[0] == '0'));", "return !(v.as.s->len == 1 && v.as.s->bytes[0] == '0');"),
 ("truth: a string that starts with 0 is false", "return !(v.as.s->len == 0 || (v.as.s->len == 1 && v.as.s->bytes[0] == '0'));", "return !(v.as.s->len == 0 || v.as.s->bytes[0] == '0');"),
 ("truth: a string that is a zero is false", "return !(v.as.s->len == 0 || (v.as.s->len == 1 && v.as.s->bytes[0] == '0'));", "return !(v.as.s->len == 0 || strtod(v.as.s->bytes, NULL) == 0.0);"),
 ("truth: a negative zero is true", "    case RT_TAG_NUM: return v.as.n != 0.0;", "    case RT_TAG_NUM: return v.as.bits != 0;"),
 ("truth: a tiny Num is false", "    case RT_TAG_NUM: return v.as.n != 0.0;", "    case RT_TAG_NUM: return fabs(v.as.n) > 1e-300;"),
 ("truth: undef is true", "    case RT_TAG_UNDEF: return 0;", "    case RT_TAG_UNDEF: return 1;"),
 ("truth: a negative Int is false", "    case RT_TAG_INT: return v.as.i != 0;", "    case RT_TAG_INT: return v.as.i > 0;"),
 ("truth: false is true", "    case RT_TAG_BOOL: return v.as.i != 0;", "    case RT_TAG_BOOL: return 1;"),
 ("false is undefined", "    return v.tag == RT_TAG_UNDEF;", "    return v.tag == RT_TAG_UNDEF || (v.tag == RT_TAG_BOOL && !v.as.i);"),
 ("nothing is undefined", "    return v.tag == RT_TAG_UNDEF;", "    return 0;"),
 ("not doesn't", "    return rt_bool(!rt_is_true(cx, a));", "    return rt_bool(rt_is_true(cx, a));"),
 ("xor is or", "    return rt_bool(left != right);", "    return rt_bool(left || right);"),
 ("xor is equality", "    return rt_bool(left != right);", "    return rt_bool(left == right);"),
 ("defined is truth", "    return rt_bool(!rt_is_undef(cx, a));", "    return rt_bool(rt_is_true(cx, a));"),
 ("numbers: always as doubles", "    if (integral(x, &p) && integral(y, &q)) return (p > q) - (p < q);\n    double f", "    (void)p; (void)q;\n    double f"),
 # Not here, being no change to what any program does: whole numbers
 # compared exactly only when both are Ints or strings of digits. A whole
 # Num is below 2^53, and beside it the double of any Int is on the same
 # side as the Int is.
 ("numbers: whole numbers backwards", "return (p > q) - (p < q);", "return (p < q) - (p > q);"),
 ("numbers: doubles backwards", "    return (f > g) - (f < g);", "    return (f < g) - (f > g);"),
 ("numbers: doubles cut to whole", "    double f = as_double(x);\n    double g = as_double(y);", "    double f = trunc(as_double(x));\n    double g = trunc(as_double(y));"),
 ("strings: a prefix is equal", "    return (s->len > t->len) - (s->len < t->len);", "    return 0;"),
 ("strings: the longer first", "    return (s->len > t->len) - (s->len < t->len);", "    return (s->len < t->len) - (s->len > t->len);"),
 ("strings: by length first", "    int c = memcmp(s->bytes, t->bytes, s->len < t->len ? s->len : t->len);\n    if (c != 0)", "    int c = s->len != t->len ? (s->len > t->len ? 1 : -1) : memcmp(s->bytes, t->bytes, s->len);\n    if (c != 0)"),
 ("strings: backwards", "    if (c != 0) return (c > 0) - (c < 0);", "    if (c != 0) return (c < 0) - (c > 0);"),
 ("strings: bytes as signed", "    int c = memcmp(s->bytes, t->bytes, s->len < t->len ? s->len : t->len);", "    int c = 0; for (uint64_t k = 0; c == 0 && k < (s->len < t->len ? s->len : t->len); k++) c = (signed char)s->bytes[k] - (signed char)t->bytes[k];"),
 ("<=> backwards", "    return rt_int(compare_numbers(cx, a, b));", "    return rt_int(-compare_numbers(cx, a, b));"),
 ("cmp as numbers", "    return rt_int(compare_strings(cx, a, b));", "    return rt_int(compare_numbers(cx, a, b));"),
]
for name, compare, right, wrong in [('rt_num_eq', 'numbers', '==', '<='), ('rt_num_ne', 'numbers', '!=', '<'), ('rt_num_lt', 'numbers', '<', '<='),
                                    ('rt_num_gt', 'numbers', '>', '>='), ('rt_num_le', 'numbers', '<=', '<'), ('rt_num_ge', 'numbers', '>=', '>'),
                                    ('rt_str_eq', 'strings', '==', '>='), ('rt_str_ne', 'strings', '!=', '>'), ('rt_str_lt', 'strings', '<', '<='),
                                    ('rt_str_gt', 'strings', '>', '>='), ('rt_str_le', 'strings', '<=', '<'), ('rt_str_ge', 'strings', '>=', '>'),
                                    ('rt_str_eq', 'strings', 'compare_strings, ==', 'compare_numbers, =='), ('rt_num_eq', 'numbers', 'compare_numbers, ==', 'compare_strings, ==')]:
    if 'compare' in right:
        M.append((f'{name} with the other comparison', f'COMPARISON({name}, {right})', f'COMPARISON({name}, {wrong})'))
    else:
        M.append((f'{name} as {wrong}', f'COMPARISON({name}, compare_{compare}, {right})', f'COMPARISON({name}, compare_{compare}, {wrong})'))
only = sys.argv[1:]
os.makedirs('build/mut', exist_ok=True)
tests = []
for src in sorted(glob.glob('t/3*.pl')):
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
