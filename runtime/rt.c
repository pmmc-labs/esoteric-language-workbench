// The core: printing, faults, the four operators, main. The runtime prints the program's
// value, then a newline, and exits 0; a fault goes to stderr and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

void rt_print(rt_value v) {
    if ((v & 1) == RT_INT_TAG) printf("%lld", (long long)(v >> RT_INT_SHIFT));
    else rt_fault("unknown value");
}

void rt_fault(const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s\n", what);
    exit(1);
}

// An operand is always in range, so only a result is checked.
static int64_t rt_untag(rt_value v) { return (int64_t)(v >> RT_INT_SHIFT); }

// D26: `wrapped` is the builtin's own overflow flag, since a 64-bit result
// that wrapped can land back in range (2^32 * 2^32 wraps to 0). Callers
// compute it in a statement of its own: C doesn't order a call's
// arguments, and passing r beside the builtin that sets it read r unset
// under clang.
static rt_value rt_ranged(int wrapped, int64_t r) {
    if (wrapped || r < RT_INT_MIN || r > RT_INT_MAX) rt_fault("integer overflow");
    return rt_int(r);
}

rt_value rt_add(rt_value a, rt_value b) {
    int64_t r;
    int wrapped = __builtin_add_overflow(rt_untag(a), rt_untag(b), &r);
    return rt_ranged(wrapped, r);
}

rt_value rt_sub(rt_value a, rt_value b) {
    int64_t r;
    int wrapped = __builtin_sub_overflow(rt_untag(a), rt_untag(b), &r);
    return rt_ranged(wrapped, r);
}

rt_value rt_mul(rt_value a, rt_value b) {
    int64_t r;
    int wrapped = __builtin_mul_overflow(rt_untag(a), rt_untag(b), &r);
    return rt_ranged(wrapped, r);
}

// C's / truncates toward zero (D24). With both operands in 63 bits the
// quotient fits in 64, so only the range check can fail: -2^62 / -1 is
// 2^62, an overflow (D25). The zero check comes first.
rt_value rt_div(rt_value a, rt_value b) {
    int64_t y = rt_untag(b);
    if (y == 0) rt_fault("division by zero");
    return rt_ranged(0, rt_untag(a) / y);
}

int main(void) {
    rt_print(lang_main());
    putchar('\n');
    return 0;
}
