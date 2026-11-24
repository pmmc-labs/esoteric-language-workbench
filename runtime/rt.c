// The core: the context, printing, faults. A compiled program prints to
// stdout and exits 0; a fault goes to stderr and exits 1.
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

int rt_run(void (*body)(rt_ctx *cx), const char *file) {
    rt_ctx cx = { .file = file, .line = 0 };
    body(&cx);
    return 0;
}

// Every operator checks its operand's tag, this one too: until types give
// the compiler a reason (step 26), the runtime trusts nothing it is handed.
void rt_say(rt_ctx *cx, rt_value v) {
    switch (v.tag) {
    case RT_TAG_INT:
        printf("%" PRId64 "\n", v.as.i);
        return;
    default:
        rt_fault(cx, "not a value");
    }
}

// Every operator checks its operands' tags (and faults by name) before it
// believes them. Only an Int can reach these yet; step 2 brings the Num,
// and with it the question each of these has to ask.
static int64_t need_int(rt_ctx *cx, rt_value v) {
    if (v.tag != RT_TAG_INT) rt_fault(cx, "not a number");
    return v.as.i;
}

// perl goes on past 2^63 as an unsigned integer and then a float; the
// language has neither, and stops (D23).
static rt_value checked(rt_ctx *cx, int64_t n, int overflowed) {
    if (overflowed) rt_fault(cx, "integer overflow");
    return rt_int(n);
}

// The overflow flag is computed in a statement of its own, and so are the
// two operands: C doesn't order a call's arguments, and `checked(cx, r,
// overflow(..., &r))` read r before it was set under clang.
rt_value rt_add(rt_ctx *cx, rt_value a, rt_value b) {
    int64_t x = need_int(cx, a);
    int64_t y = need_int(cx, b);
    int64_t r;
    int o = __builtin_add_overflow(x, y, &r);
    return checked(cx, r, o);
}

rt_value rt_sub(rt_ctx *cx, rt_value a, rt_value b) {
    int64_t x = need_int(cx, a);
    int64_t y = need_int(cx, b);
    int64_t r;
    int o = __builtin_sub_overflow(x, y, &r);
    return checked(cx, r, o);
}

rt_value rt_mul(rt_ctx *cx, rt_value a, rt_value b) {
    int64_t x = need_int(cx, a);
    int64_t y = need_int(cx, b);
    int64_t r;
    int o = __builtin_mul_overflow(x, y, &r);
    return checked(cx, r, o);
}

// perl's `%` takes the sign of its right operand, and C's the sign of its
// left: -7 % 3 is 2 in perl and -1 in C. So C's remainder is moved over by
// one divisor when its sign is the wrong one; the two have opposite signs
// then and the sum can't overflow. -1 is answered first: every remainder
// by it is 0, and C's `INT64_MIN % -1` is undefined (it traps on x86).
rt_value rt_mod(rt_ctx *cx, rt_value a, rt_value b) {
    int64_t x = need_int(cx, a);
    int64_t y = need_int(cx, b);
    if (y == 0) rt_fault(cx, "modulus by zero");
    if (y == -1) return rt_int(0);
    int64_t r = x % y;
    if (r != 0 && (r < 0) != (y < 0)) r += y;
    return rt_int(r);
}

// 0 - x overflows for the one Int that has no negation, -2^63.
rt_value rt_neg(rt_ctx *cx, rt_value a) {
    int64_t x = need_int(cx, a);
    int64_t r;
    int o = __builtin_sub_overflow((int64_t)0, x, &r);
    return checked(cx, r, o);
}

// stdout is flushed first, so that what the program printed before the
// fault comes before the fault's line wherever the two streams meet: the
// start of perl's output, then the stop (D12).
void rt_fault(rt_ctx *cx, const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s at %s line %" PRId64 ".\n", what, cx->file, cx->line);
    exit(1);
}
