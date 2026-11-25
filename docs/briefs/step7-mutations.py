#!/usr/bin/env python3
"""Break step 7's collector on purpose, and the code generator's side of
it, one way at a time, and see that a test goes red each time.

    python3 docs/briefs/step7-mutations.py            # all of them
    python3 docs/briefs/step7-mutations.py "slot"     # those named so

Nothing in the tree is written: a broken runtime or compiler is a copy of
bin/, compiler/src/ and runtime/ under build/mut/tree/. Each breakage is
run two ways, and is caught if either goes red:

  golden   the tests that make strings (1xx, 5xx, 7xx, 8xx; not the
           refused ones), run with the knobs of t/knobs.sh and each
           test's own `# env:`, as t/run.sh runs them. For a broken
           runtime each test's C is compiled once, by the compiler as it
           is, and linked again with the broken runtime; for a broken
           compiler each is compiled again by the copy
  unit     the runtime's own tests, runtime/tests/ of the copy

A record of step 7, and not part of make test: each breakage is a piece
of the text as it was then, and one that no longer matches stops the
run."""
import subprocess, glob, sys, os, shutil, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 't')
import checks

RT = 'runtime/rt.c'
GEN = 'compiler/src/codegen.ts'
RESOLVE = 'compiler/src/resolver.ts'
MUTATIONS = [
 # ---- the collector
 ("the first slot of a frame is not marked", RT, "        for (uint64_t k = 0; k < frame->count; k++) {", "        for (uint64_t k = 1; k < frame->count; k++) {"),
 ("the last slot of a frame is not marked", RT, "        for (uint64_t k = 0; k < frame->count; k++) {", "        for (uint64_t k = 0; k + 1 < frame->count; k++) {"),
 ("every other slot is not marked", RT, "        for (uint64_t k = 0; k < frame->count; k++) {", "        for (uint64_t k = 0; k < frame->count; k += 2) {"),
 ("only the newest frame is marked", RT, "    for (rt_frame *frame = cx->frames; frame; frame = frame->prev) {", "    for (rt_frame *frame = cx->frames; frame; frame = NULL) {"),
 ("nothing is marked", RT, "            if (v.as.s->where == RT_STR_HEAP) ((rt_block *)v.as.s - 1)->marked = 1;\n", ""),
 ("the sweep frees what was marked", RT, "        if (block->marked) {\n            block->marked = 0;", "        if (!block->marked) {\n            block->marked = 0;"),
 ("the marks are not cleared", RT, "        if (block->marked) {\n            block->marked = 0;\n", "        if (block->marked) {\n"),
 ("nothing is ever freed", RT, "        if (block->marked) {\n            block->marked = 0;", "        if (1) {\n            block->marked = 0;"),
 ("a constant is marked as a heap string is", RT, "            if (v.as.s->where == RT_STR_HEAP) ((rt_block", "            if (v.as.s->where != RT_STR_DEAD) ((rt_block"),
 ("a collection comes after the string is made, not before", RT, "    s->where = RT_STR_HEAP;\n    *bytes = p;\n", "    s->where = RT_STR_HEAP;\n    *bytes = p;\n    if (cx->stress) rt_collect(cx);\n"),
 ("a number as a string is made on the heap", RT, "    number->s.where = RT_STR_SCRATCH;\n    return &number->s;", "    char *made;\n    const rt_str *heap = str_new(cx, (uint64_t)len, (uint64_t)len, &made);\n    memcpy(made, number->bytes, (size_t)len);\n    return heap;"),
 ("a frame is not linked", RT, "    frame->slots = slots;\n    cx->frames = frame;", "    frame->slots = slots;"),
 ("a frame is not unlinked", RT, "    cx->frames = frame->prev;\n}", "}"),
 ("a frame does not open empty", RT, "    memset(slots, 0, count * sizeof(rt_value));\n", ""),
 ("a frame left open goes unseen", RT, '    if (cx.frames != NULL) rt_internal(&cx, "a frame was left open");\n', ""),
 ("a frame closed out of turn goes unseen", RT, '    if (cx->frames != frame) rt_internal(cx, "a frame was closed that is not the newest");\n', ""),
 # ---- the knobs
 ("the stress knob does nothing", RT, "(cx->stress != 0 && cx->allocations % cx->stress == 0) || ", ""),
 ("the ordinary policy never collects", RT, " || cx->since > cx->threshold) {", ") {"),
 ("the threshold does not grow with what is live", RT, "    cx->threshold = live > FIRST_COLLECTION ? live : FIRST_COLLECTION;", "    cx->threshold = FIRST_COLLECTION;"),
 ("the count since the last collection is not begun again", RT, "    cx->since = 0;\n", ""),
 ("the first collection comes after eight megabytes", RT, "#define FIRST_COLLECTION ((uint64_t)1 << 20)", "#define FIRST_COLLECTION ((uint64_t)1 << 23)"),
 ("what is allocated is not counted toward the cap", RT, "    cx->held += size;\n", ""),
 ("what is freed is still held", RT, "            cx->held -= block->size;\n", ""),
 ("the cap is on the living alone, under poison", RT, "            block->next = cx->dead;\n            cx->dead = block;", "            block->next = cx->dead;\n            cx->dead = block;\n            cx->held -= block->size;"),
 ("the cap faults before a collection", RT, "        if (!collected) rt_collect(cx);\n        collected = 1;\n", ""),
 ("the cap does not fault", RT, '        if (size > cx->cap || cx->held > cx->cap - size) rt_fault(cx, "out of memory");\n    }\n    rt_block *block', '    }\n    rt_block *block'),
 ("poison hands the memory back", RT, "        if (cx->poison) {", "        if (0) {"),
 ("a collected string is not marked dead", RT, "        s->where = RT_STR_DEAD;\n", ""),
 ("a knob that is not a number is taken for 0", RT, "        if (overflowed || n > most) {", "        if (0) {"),
 # ---- reading a string that was collected
 ("a dead string is read as a string", RT, "    if (v.tag == RT_TAG_STR) return alive(cx, v.as.s);", "    if (v.tag == RT_TAG_STR) return v.as.s;"),
 ("a dead string is read as a number", RT, "        return from_string(cx, alive(cx, v.as.s));", "        return from_string(cx, v.as.s);"),
 ("a dead string is tested for truth", RT, "        const rt_str *s = alive(cx, v.as.s);\n        return !(s->len == 0", "        const rt_str *s = v.as.s;\n        return !(s->len == 0"),
 ("a dead string is found in a slot, and marked", RT, '            if (v.as.s->where == RT_STR_DEAD) rt_internal(cx, "a slot holds a string that was collected");\n', ""),
 ("concat does not look at its operands again", RT, "    alive(cx, s);\n    alive(cx, t);\n", ""),
 ("repeat does not look at its operand again", RT, "    const rt_str *repeated = str_new(cx, s->len * n, s->chars * n, &bytes);\n    alive(cx, s);\n", "    const rt_str *repeated = str_new(cx, s->len * n, s->chars * n, &bytes);\n"),
 ("uc does not look at its operand again", RT, "    const rt_str *changed = str_new(cx, s->len, s->chars, &bytes);\n    alive(cx, s);\n", "    const rt_str *changed = str_new(cx, s->len, s->chars, &bytes);\n"),
 ("substr does not look at its operand again", RT, "    const rt_str *piece = str_new(cx, to - from, (uint64_t)(end - start), &bytes);\n    alive(cx, s);\n", "    const rt_str *piece = str_new(cx, to - from, (uint64_t)(end - start), &bytes);\n"),
 # ---- the generated C
 ("a my does not make its slot undef", GEN, "        b.vars.push(`${variable(b, e)} = rt_undef(); // my $${e.name}`);\n", ""),
 ("the temporaries begin one slot early", GEN, "const t = `f[${b.names.variables + b.values}]`;", "const t = `f[${Math.max(0, b.names.variables - 1) + b.values}]`;"),
 ("the temporaries are all one slot", GEN, "const t = `f[${b.names.variables + b.values}]`;", "const t = `f[${b.names.variables}]`;"),
 ("the frame is a slot short", GEN, "        `    rt_enter(cx, &frame, f, ${slots});`,", "        `    rt_enter(cx, &frame, f, ${slots - 1});`,"),
 ("the frame's temporaries are not roots", GEN, "        `    rt_enter(cx, &frame, f, ${slots});`,", "        `    rt_enter(cx, &frame, f, ${Math.max(1, names.variables)});`,"),
 ("the frame is not opened", GEN, "        `    rt_enter(cx, &frame, f, ${slots});`,\n", ""),
 ("the frame is not closed", GEN, "        '    rt_leave(cx, &frame);',\n", ""),
 ("a variable is given the slot of the one before it", RESOLVE, "            slots[of.get(d)!] = inScope;", "            slots[of.get(d)!] = Math.max(0, inScope - 1);"),
 ("every variable has slot 0", RESOLVE, "            slots[of.get(d)!] = inScope;", "            slots[of.get(d)!] = 0;"),
 ("a block that ends keeps its slots, and the count is of one block", RESOLVE, "            variables = Math.max(variables, inScope);", "            variables = Math.max(variables, scope.size);"),
]

only = sys.argv[1:]
knobs = checks.knobs()
tests = []
for src in sorted(glob.glob('t/1*.pl') + glob.glob('t/5*.pl') + glob.glob('t/7*.pl') + glob.glob('t/8*.pl')):
    head = open(src, encoding='utf-8', errors='replace').read(600)
    if 'kind: refused' in head:
        continue
    env = dict(os.environ)
    env.update(knobs)
    found = re.search(r'^# env: (.*)$', head, re.M)
    if found:
        env.update(pair.split('=', 1) for pair in found.group(1).split())
    tests.append((os.path.basename(src)[:-3], open(src[:-3] + '.expected', 'rb').read(), env))

def passes(test, driver):
    name, expected, env = test
    if driver is None:
        # The test's own C as it was compiled at the start, and the
        # runtime of the copy.
        if subprocess.run(['cc', '-o', f'build/mut/{name}', f'build/mut/{name}.o', 'build/mut/rt.o', '-lm'], capture_output=True).returncode:
            return False
    elif subprocess.run(['node', driver, '-o', f'build/mut/{name}', f't/{name}.pl'], capture_output=True).returncode:
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
    with ThreadPoolExecutor(3) as pool:
        return [t[0] for t, ok in zip(tests, pool.map(lambda t: passes(t, driver), tests)) if not ok]

def unit(tree):
    """How many of the runtime's own tests fail, in the copy."""
    r = subprocess.run(['node', '--test', f'{tree}/runtime/tests/rt.test.ts'], capture_output=True, text=True)
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
for name, _, _ in tests:
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
    else:
        failed = golden('build/mut/tree/bin/curlyc.ts')
    units = unit('build/mut/tree')
    if failed or units:
        print(f'{name}: golden {len(failed)} ({", ".join(f[:3] for f in failed[:6])}), unit {units}', flush=True)
    else:
        print(f'{name}: golden 0, unit 0   <-- NOT CAUGHT', flush=True)
        missed.append(name)
print(f'{len(missed)} not caught: {missed}')
