// The core: printing, faults, main. The runtime prints the program's
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

// The range is 63 bits, not the 64 that int64_t holds, so every result is
// checked against it (D9). Operands are 63-bit, so a sum or a difference
// can't overflow int64_t, and the only int64_t division that could
// (INT64_MIN / -1) can't arise. A product can: 2^64 wraps to 0 in int64_t,
// which is in range, so the multiply's own overflow is a fault as well.
#define RT_MIN (-((int64_t)1 << 62))
#define RT_MAX (((int64_t)1 << 62) - 1)

static int64_t untag(rt_value v) { return v >> RT_INT_SHIFT; }

static rt_value checked(int64_t n) {
    if (n < RT_MIN || n > RT_MAX) rt_fault("integer overflow");
    return rt_int(n);
}

rt_value rt_add(rt_value a, rt_value b) { return checked(untag(a) + untag(b)); }
rt_value rt_sub(rt_value a, rt_value b) { return checked(untag(a) - untag(b)); }

rt_value rt_mul(rt_value a, rt_value b) {
    int64_t n;
    if (__builtin_mul_overflow(untag(a), untag(b), &n)) rt_fault("integer overflow");
    return checked(n);
}

// C99's / and % truncate toward zero and % takes the dividend's sign, which
// is D10, so they divide directly once the divisor is known not to be 0.
rt_value rt_div(rt_value a, rt_value b) {
    if (untag(b) == 0) rt_fault("division by zero");
    return checked(untag(a) / untag(b));
}

rt_value rt_rem(rt_value a, rt_value b) {
    if (untag(b) == 0) rt_fault("division by zero");
    return checked(untag(a) % untag(b));
}

int main(void) {
    rt_print(lang_main());
    putchar('\n');
    return 0;
}
