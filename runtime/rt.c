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

// The one range check (D10): every result goes through here.
static rt_value encode(int64_t n) {
    if (n < RT_INT_MIN || n > RT_INT_MAX) rt_fault("integer overflow");
    return rt_int(n);
}

// An arithmetic right shift, as rt_print does.
static int64_t decode(rt_value v) { return v >> RT_INT_SHIFT; }

// Two 63-bit operands cannot overflow 64 bits, so the plain operation is
// defined and only the range check is needed.
rt_value rt_add(rt_value a, rt_value b) { return encode(decode(a) + decode(b)); }
rt_value rt_sub(rt_value a, rt_value b) { return encode(decode(a) - decode(b)); }

// The product can pass 64 bits, and a signed multiply that does is
// undefined C, so the builtin reports it. Its result is written in a
// statement of its own and read in the next (CLAUDE.md, code style).
rt_value rt_mul(rt_value a, rt_value b) {
    int64_t product;
    int passed = __builtin_mul_overflow(decode(a), decode(b), &product);
    if (passed) rt_fault("integer overflow");
    return encode(product);
}

// C's / and % truncate toward zero and give % the dividend's sign, which
// is D11, so there is no fix-up. The zero divisor is checked first. The
// minimum is only 2^62 in magnitude, so INT64_MIN / -1, the one divide
// that traps, cannot occur; the minimum / -1 is 2^62, which encode faults.
rt_value rt_div(rt_value a, rt_value b) {
    if (decode(b) == 0) rt_fault("division by zero");
    return encode(decode(a) / decode(b));
}

rt_value rt_rem(rt_value a, rt_value b) {
    if (decode(b) == 0) rt_fault("division by zero");
    return encode(decode(a) % decode(b));
}

int main(void) {
    rt_print(lang_main());
    putchar('\n');
    return 0;
}
