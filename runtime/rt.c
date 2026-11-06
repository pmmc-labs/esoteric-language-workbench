// The core: arithmetic, comparisons, the budget, printing, faults, main. The runtime
// prints the program's value, then a newline, and exits 0; a fault goes
// to stderr and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

// The budget (D27): every operator function counts itself first, in or out
// of any `within`, and faults when the count passes the limit, which starts
// at the largest 64-bit integer and which `rt_within` lowers. The charge is
// the first thing an operator does, so it comes before the operator's own
// checks (D25). Counting past 2^63 would take longer than a machine runs.
static int64_t rt_ops = 0;
static int64_t rt_limit = INT64_MAX;
static void charge(void) {
    rt_ops += 1;
    if (rt_ops > rt_limit) rt_fault("out of budget");
}

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
rt_value rt_add(rt_value a, rt_value b) { charge(); RT_CHECKED(add, a, b); }
rt_value rt_sub(rt_value a, rt_value b) { charge(); RT_CHECKED(sub, a, b); }
rt_value rt_mul(rt_value a, rt_value b) { charge(); RT_CHECKED(mul, a, b); }

// Division truncates toward zero and the remainder takes the dividend's
// sign, as C's do (D5). RT_INT_MIN / -1 is 2^62, past the range.
rt_value rt_div(rt_value a, rt_value b) {
    charge();
    need_ints(a, b);
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return checked(rt_int_of(a) / rt_int_of(b), 0);
}
rt_value rt_mod(rt_value a, rt_value b) {
    charge();
    need_ints(a, b);
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return rt_int(rt_int_of(a) % rt_int_of(b));
}

// The orderings take two integers (D12). == and != take any two values:
// values of different types are unequal, since their bits differ (D14),
// so comparing the bits is the comparison.
rt_value rt_lt(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_bool(rt_int_of(a) < rt_int_of(b)); }
rt_value rt_le(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_bool(rt_int_of(a) <= rt_int_of(b)); }
rt_value rt_gt(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_bool(rt_int_of(a) > rt_int_of(b)); }
rt_value rt_ge(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_bool(rt_int_of(a) >= rt_int_of(b)); }
rt_value rt_eq(rt_value a, rt_value b) { charge(); return rt_bool(a == b); }
rt_value rt_ne(rt_value a, rt_value b) { charge(); return rt_bool(a != b); }

// Bit operations on the sign-extended values (D15): two's complement of
// any width agrees, so the 64-bit operators give the 63-bit answer, which
// is always in range.
rt_value rt_bit_and(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_int(rt_int_of(a) & rt_int_of(b)); }
rt_value rt_bit_or(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_int(rt_int_of(a) | rt_int_of(b)); }
rt_value rt_bit_xor(rt_value a, rt_value b) { charge(); need_ints(a, b); return rt_int(rt_int_of(a) ^ rt_int_of(b)); }

// A shift's count is 0 to 62 (D16): 63 or more shifts every bit out of a
// 63-bit integer, and a negative count is a mistake, not the other shift.
static int64_t shift_count(rt_value a, rt_value n) {
    need_ints(a, n);
    if (rt_int_of(n) < 0 || rt_int_of(n) > 62) rt_fault("bad shift");
    return rt_int_of(n);
}

// A left shift is a multiplication by 2^k, checked as one (D4, D16): a
// result past the range faults overflow. The count is a statement of its
// own, for the argument-order reason at `checked`.
rt_value rt_bit_shl(rt_value a, rt_value b) {
    charge();
    int64_t k = shift_count(a, b);
    int64_t r;
    int o = __builtin_mul_overflow(rt_int_of(a), (int64_t)1 << k, &r);
    return checked(r, o);
}

// A right shift rounds toward negative infinity (D16), where `/` rounds
// toward zero (D5). So the quotient is C's, corrected when a negative
// dividend left a remainder. `>>` isn't used: a right shift of a negative
// value is implementation-defined in C.
rt_value rt_bit_shr(rt_value a, rt_value b) {
    charge();
    int64_t k = shift_count(a, b);
    int64_t d = (int64_t)1 << k;
    int64_t x = rt_int_of(a);
    int64_t q = x / d;
    if (x < 0 && x % d != 0) q -= 1;
    return rt_int(q);
}

// a to the power b (D18, D19). A negative exponent faults `bad exponent`,
// even for a base of 1 or -1 whose power would fit. Squaring, so the loop
// runs at most 62 times however large b is, and a base of 0, 1 or -1 with
// the largest exponent doesn't take 2^62 steps. The base is squared only
// while bits remain: then some later step multiplies by it or a larger
// square, so a square that overflows means the result does too (|base| >= 2
// here; 0, 1 and -1 never overflow). Overflow is the multiplication's own
// check (D4), the flags statements of their own as at `checked`.
rt_value rt_pow(rt_value a, rt_value b) {
    charge();
    need_ints(a, b);
    int64_t e = rt_int_of(b);
    if (e < 0) rt_fault("bad exponent");
    int64_t base = rt_int_of(a);
    int64_t r = 1;
    while (e > 0) {
        if (e & 1) {
            int o = __builtin_mul_overflow(r, base, &r);
            checked(r, o);
        }
        e >>= 1;
        if (e > 0) {
            int o = __builtin_mul_overflow(base, base, &base);
            checked(base, o);
        }
    }
    return checked(r, 0);
}

// `(within n e)` (D23, D24, D27): the body is a function the generated code
// passes, so it runs after the limit is lowered. The limit in force is the
// smallest of the surrounding ones: the count now plus n, if that is lower.
// A fault ends the program (D6), so there is nothing to undo on that way
// out. The limit is saved, and the body called, in statements of their own
// (the argument-order lesson at `checked`).
rt_value rt_within(rt_value n, rt_value (*body)(void)) {
    if (!rt_is_int(n)) rt_fault("not an integer");
    int64_t k = rt_int_of(n);
    if (k < 0) rt_fault("bad budget");
    int64_t saved = rt_limit;
    int64_t mine = rt_ops + k;
    if (mine < rt_limit) rt_limit = mine;
    rt_value v = body();
    rt_limit = saved;
    return v;
}

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
