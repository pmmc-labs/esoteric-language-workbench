// The core: arithmetic, printing, faults, main. The runtime prints the
// program's value, then a newline, and exits 0; a fault goes to stderr
// and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

// Arithmetic on the 64-bit values, checked against 63-bit range after
// (D4: a result that doesn't fit faults, rather than wrapping or growing).
// __builtin_*_overflow catches the one case 64 bits can't hold either.
static rt_value checked(int64_t n, int overflowed) {
    if (overflowed || n < RT_INT_MIN || n > RT_INT_MAX) rt_fault("overflow");
    return rt_int(n);
}

rt_value rt_add(rt_value a, rt_value b) { int64_t r; return checked(r, __builtin_add_overflow(rt_int_of(a), rt_int_of(b), &r)); }
rt_value rt_sub(rt_value a, rt_value b) { int64_t r; return checked(r, __builtin_sub_overflow(rt_int_of(a), rt_int_of(b), &r)); }
rt_value rt_mul(rt_value a, rt_value b) { int64_t r; return checked(r, __builtin_mul_overflow(rt_int_of(a), rt_int_of(b), &r)); }

// Division truncates toward zero and the remainder takes the dividend's
// sign, as C's do (D5). RT_INT_MIN / -1 is 2^62, past the range.
rt_value rt_div(rt_value a, rt_value b) {
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return checked(rt_int_of(a) / rt_int_of(b), 0);
}
rt_value rt_mod(rt_value a, rt_value b) {
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return rt_int(rt_int_of(a) % rt_int_of(b));
}

void rt_print(rt_value v) {
    if ((v & 1) == RT_INT_TAG) printf("%lld", (long long)rt_int_of(v));
    else rt_fault("unknown value");
}

void rt_fault(const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s\n", what);
    exit(1);
}

int main(void) {
    rt_print(lang_main());
    putchar('\n');
    return 0;
}
