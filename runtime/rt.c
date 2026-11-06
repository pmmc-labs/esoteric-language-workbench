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

// Bit operations (D15, D16). and, or and xor on the sign-extended 64-bit
// values agree with two's complement of any width and stay in range.
rt_value rt_band(rt_value a, rt_value b) { need_ints(a, b); return rt_int(rt_int_of(a) & rt_int_of(b)); }
rt_value rt_bor(rt_value a, rt_value b) { need_ints(a, b); return rt_int(rt_int_of(a) | rt_int_of(b)); }
rt_value rt_bxor(rt_value a, rt_value b) { need_ints(a, b); return rt_int(rt_int_of(a) ^ rt_int_of(b)); }

// The count is checked before the value is used, whatever a is (D16).
static int64_t shift_count(rt_value b) {
    int64_t n = rt_int_of(b);
    if (n < 0 || n > 62) rt_fault("bad shift");
    return n;
}

// a * 2^n, multiplied rather than shifted (a left shift of a negative is
// undefined C), with the range checked after (D4, D16). 2^62 fits int64.
rt_value rt_shl(rt_value a, rt_value b) {
    need_ints(a, b);
    int64_t n = shift_count(b);
    int64_t r;
    int o = __builtin_mul_overflow(rt_int_of(a), INT64_C(1) << n, &r);
    return checked(r, o);
}

// Rounds toward negative infinity (D16). C's >> on a negative is
// implementation-defined, so a negative is complemented, shifted and
// complemented back: ~a is non-negative, and ~(~a >> n) is the floor.
rt_value rt_shr(rt_value a, rt_value b) {
    need_ints(a, b);
    int64_t n = shift_count(b);
    int64_t x = rt_int_of(a);
    return rt_int(x >= 0 ? x >> n : ~(~x >> n));
}

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
