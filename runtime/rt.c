// The core: arithmetic, printing, faults, main. The runtime prints the
// program's value, then a newline, and exits 0; a fault goes to stderr
// and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

// A value is an integer when its low bit is 0 (D14); a boolean's is 1.
// The runtime checks the tag now that an if can hand a boolean to an
// operator, so the compiler can't know what a value is.
static void check_int(rt_value v) {
    if ((v & 1) != RT_INT_TAG) rt_fault("not an integer");
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

#define RT_CHECKED(op, a, b) do { int64_t r; int o = __builtin_##op##_overflow(rt_int_of(a), rt_int_of(b), &r); return checked(r, o); } while (0)
rt_value rt_add(rt_value a, rt_value b) { check_int(a); check_int(b); RT_CHECKED(add, a, b); }
rt_value rt_sub(rt_value a, rt_value b) { check_int(a); check_int(b); RT_CHECKED(sub, a, b); }
rt_value rt_mul(rt_value a, rt_value b) { check_int(a); check_int(b); RT_CHECKED(mul, a, b); }

// Division truncates toward zero and the remainder takes the dividend's
// sign, as C's do (D5). RT_INT_MIN / -1 is 2^62, past the range.
rt_value rt_div(rt_value a, rt_value b) {
    check_int(a); check_int(b);
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return checked(rt_int_of(a) / rt_int_of(b), 0);
}
rt_value rt_mod(rt_value a, rt_value b) {
    check_int(a); check_int(b);
    if (rt_int_of(b) == 0) rt_fault("division by zero");
    return rt_int(rt_int_of(a) % rt_int_of(b));
}

// The orderings (D12) take two integers and give a boolean; an ordering
// given a boolean faults "not an integer".
#define RT_ORDER(op, a, b) do { check_int(a); check_int(b); return rt_bool(rt_int_of(a) op rt_int_of(b)); } while (0)
rt_value rt_lt(rt_value a, rt_value b) { RT_ORDER(<, a, b); }
rt_value rt_le(rt_value a, rt_value b) { RT_ORDER(<=, a, b); }
rt_value rt_gt(rt_value a, rt_value b) { RT_ORDER(>, a, b); }
rt_value rt_ge(rt_value a, rt_value b) { RT_ORDER(>=, a, b); }

// == and != (D12) compare any two values: the tags are injective, so two
// equal values are equal words, and a value of one type is never equal
// to one of another, so a mismatch is #false, not a fault.
rt_value rt_eq(rt_value a, rt_value b) { return rt_bool(a == b); }
rt_value rt_ne(rt_value a, rt_value b) { return rt_bool(a != b); }

// The test of an if (D13): it must be a boolean, and its value is the 0
// or 1 C's ?: selects on, so only the taken branch is evaluated.
rt_value rt_if_test(rt_value test) {
    if ((test & 3) != RT_BOOL_TAG) rt_fault("not a boolean");
    return test >> RT_BOOL_SHIFT;
}

void rt_print(rt_value v) {
    if ((v & 1) == RT_INT_TAG) printf("%lld", (long long)rt_int_of(v));
    else if ((v & 3) == RT_BOOL_TAG) printf("%s", (v >> RT_BOOL_SHIFT) ? "#true" : "#false");
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
