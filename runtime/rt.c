// The core: arithmetic, printing, faults, main. The runtime prints the
// program's value, then a newline, and exits 0; a fault goes to stderr
// and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

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

// The operators take integers (D14). The compiler can't know the type of
// what an `if` gives, so the check is here, at run time.
static void need_ints(rt_value a, rt_value b) {
    if (!rt_is_int(a) || !rt_is_int(b)) rt_fault("not an integer");
}

#define RT_CHECKED(op, a, b) do { int64_t r; int o = __builtin_##op##_overflow(rt_int_of(a), rt_int_of(b), &r); return checked(r, o); } while (0)
rt_value rt_add(rt_value a, rt_value b) { need_ints(a, b); RT_CHECKED(add, a, b); }
rt_value rt_sub(rt_value a, rt_value b) { need_ints(a, b); RT_CHECKED(sub, a, b); }
rt_value rt_mul(rt_value a, rt_value b) { need_ints(a, b); RT_CHECKED(mul, a, b); }

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

// The orderings take two integers; == and != take any two values (D12).
rt_value rt_lt(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) < rt_int_of(b)); }
rt_value rt_le(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) <= rt_int_of(b)); }
rt_value rt_gt(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) > rt_int_of(b)); }
rt_value rt_ge(rt_value a, rt_value b) { need_ints(a, b); return rt_bool(rt_int_of(a) >= rt_int_of(b)); }
rt_value rt_eq(rt_value a, rt_value b) { return rt_bool(a == b); }
rt_value rt_ne(rt_value a, rt_value b) { return rt_bool(a != b); }

// The test of an `if` is a boolean or the program faults (D13): there is
// no truthiness, so (if 0 ...) says what the mistake is.
int rt_truth(rt_value v) {
    if (!rt_is_bool(v)) rt_fault("not a boolean");
    return (v & RT_BOOL_BIT) != 0;
}

void rt_print(rt_value v) {
    if (rt_is_int(v)) printf("%lld", (long long)rt_int_of(v));
    else if (rt_is_bool(v)) fputs((v & RT_BOOL_BIT) ? "#true" : "#false", stdout);
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
