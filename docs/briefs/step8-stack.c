// Step 8's evidence for the limit on recursion: how much of the C stack one
// call of a compiled sub takes. The sub is what the code generator would
// write for `sub d($n) { return $n == 0 ? 0 : 1 + d($n - 1) }`, with
// SLOTS slots in its frame.
//
//     cc -O1 -c -o rt.o runtime/rt.c && cc -O0 -DSLOTS=4 -Iruntime -o stk docs/briefs/step8-stack.c rt.o -lm
//     ./stk 1000        # bytes per call, measured
//     ./stk 40000       # or a segmentation fault: the stack ended
//
// 2026-11-25, Linux x86-64, an 8 MB stack (ulimit -s 8192), bytes a call
// and the deepest call that returned:
//
//     gcc 13, 4 slots       223    37,357        400 slots   1,270 deep
//     clang 18, 4 slots     335    24,872        400 slots   1,231 deep
//     clang, ASan + UBSan   (its locals are not on the stack, so the
//                            bytes can't be measured this way)
//                           4 slots 10,581 deep; 40 slots 5,983; 400 slots 1,229
//
// So a call costs its slots at 16 bytes each and, at worst, about 750 bytes
// more. A record, not a test.
#include "rt.h"
#include <stdio.h>
#include <stdlib.h>
#ifndef SLOTS
#define SLOTS 4
#endif
static char *base; static long deepest; static long target;
static rt_value sub_d(rt_ctx *cx, int want, uint64_t argc, rt_value a0) {
    rt_value f[SLOTS];
    rt_frame frame;
    rt_enter(cx, &frame, f, SLOTS);
    f[0] = a0;
    cx->line = 2;
    long used = base - (char *)&frame;
    if (used > deepest) deepest = used;
    f[1] = rt_num_eq(cx, f[0], rt_int(0));
    rt_value r;
    if (rt_is_true(cx, f[1])) { r = rt_int(0); }
    else {
        f[2] = rt_sub(cx, f[0], rt_int(1));
        f[3] = sub_d(cx, want, 1, f[2]);
        r = rt_add(cx, rt_int(1), f[3]);
    }
    rt_leave(cx, &frame);
    return r;
}
static void curly_main(rt_ctx *cx) {
    char here; base = &here;
    rt_value f[1]; rt_frame frame; rt_enter(cx, &frame, f, 1);
    f[0] = sub_d(cx, 1, 1, rt_int(target));
    printf("%ld bytes per call\n", deepest / (target + 1));
    rt_leave(cx, &frame);
}
int main(int argc, char **argv) { target = atol(argv[1]); return rt_run(curly_main, "x.pl"); }
