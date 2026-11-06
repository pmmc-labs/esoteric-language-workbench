// The core: arithmetic, comparisons, printing, faults, main. The runtime
// prints the program's value, then a newline, and exits 0; a fault goes
// to stderr and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

// Arithmetic and orderings take integers (D11, D14): a boolean is a fault
// here, since the compiler can't know what an `if` gives.
static void need_ints(rt_value a, rt_value b) {
    if (!rt_is_int(a) || !rt_is_int(b)) rt_fault("not an integer");
}

// Arithmetic on the 64-bit values, checked against 63-bit range after
// (D4: a result that doesn't fit faults, rather than wrapping or growing).
// __builtin_*_overflow catches the one case 64 bits can't hold either.
// The flag is a statement of its own: C doesn't order a call's
// arguments, and `checked(r, overflow(..., &r))` read r before it was
// set under clang (0 on the M2) while gcc happened to set it first.
static rt_value checked(int64_t n, int overflowed) {
    if (overflowed || n < RT_INT_MIN || n > RT_INT_MAX) rt_fault("overflow");
    return rt_int(n);
}

#define RT_CHECKED(op, a, b) do { need_ints(a, b); int64_t r; int o = __builtin_##op##_overflow(rt_int_of(a), rt_int_of(b), &r); return checked(r, o); } while (0)
rt_value rt_add(rt_value a, rt_value b) { RT_CHECKED(add, a, b); }
rt_value rt_sub(rt_value a, rt_value b) { RT_CHECKED(sub, a, b); }
rt_value rt_mul(rt_value a, rt_value b) { RT_CHECKED(mul, a, b); }

// Division truncates toward zero and the remainder takes the dividend's
// sign, as C's do (D5). RT_INT_MIN / -1 is 2^62, past the range.
rt_value rt_div(rt_value a, rt_value b) {
    need_ints(a, b);
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return checked(rt_int_of(a) / rt_int_of(b), 0);
}
rt_value rt_mod(rt_value a, rt_value b) {
    need_ints(a, b);
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return rt_int(rt_int_of(a) % rt_int_of(b));
}

// The bit operations take two integers (D15, D17): a boolean faults `not an
// integer`. and, or and xor are on the sign-extended two's-complement value,
// and their result is always in range (D15), so there is no check.
rt_value rt_bit_and(rt_value a, rt_value b) { need_ints(a, b); return rt_int(rt_int_of(a) & rt_int_of(b)); }
rt_value rt_bit_or(rt_value a, rt_value b) { need_ints(a, b); return rt_int(rt_int_of(a) | rt_int_of(b)); }
rt_value rt_bit_xor(rt_value a, rt_value b) { need_ints(a, b); return rt_int(rt_int_of(a) ^ rt_int_of(b)); }

// A shift count is 0 to 62 (D16); any other faults `bad shift`, whatever the
// value is. A left shift is a * 2^n, checked against range; a right shift is
// a / 2^n rounded toward negative infinity, so the sign is kept and
// (-7 shr 1) is -4 where (/ -7 2) is -3. The count and the value are read
// before the call, since C does not order a call's arguments.
static rt_value shift(rt_value a, rt_value b, int left) {
    need_ints(a, b);
    int64_t n = rt_int_of(b);
    if (n < 0 || n > 62) rt_fault("bad shift");
    int64_t x = rt_int_of(a);
    int64_t d = INT64_C(1) << n;
    if (left) {
        int64_t r;
        int o = __builtin_mul_overflow(x, d, &r);
        return checked(r, o);
    }
    // Floor division by 2^n: a shift is enough for x >= 0; for x < 0,
    // (x - (d - 1)) / d rounds toward negative infinity, and the form avoids
    // negating x, which would overflow at MIN.
    if (x >= 0) return rt_int(x >> n);
    return rt_int((x - (d - 1)) / d);
}
rt_value rt_bit_shl(rt_value a, rt_value b) { return shift(a, b, 1); }
rt_value rt_bit_shr(rt_value a, rt_value b) { return shift(a, b, 0); }

// The orderings take two integers (D12). == and != take any two values:
// values of different types are unequal, since their bits differ (D14),
// so comparing the bits is the comparison.
rt_value rt_lt(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) < rt_int_of(b)); }
rt_value rt_le(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) <= rt_int_of(b)); }
rt_value rt_gt(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) > rt_int_of(b)); }
rt_value rt_ge(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) >= rt_int_of(b)); }
rt_value rt_eq(rt_value a, rt_value b) { return rt_bool(a == b); }
rt_value rt_ne(rt_value a, rt_value b) { return rt_bool(a != b); }

// The test of an `if` is a boolean, and only a boolean (D13).
int rt_test(rt_value v) {
    if (v == RT_TRUE) return 1;
    if (v == RT_FALSE) return 0;
    rt_fault("not a boolean");
}

void rt_print(rt_value v) {
    if (rt_is_int(v)) printf("%lld", (long long)rt_int_of(v));
    else if (v == RT_TRUE) printf("#true");
    else if (v == RT_FALSE) printf("#false");
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
