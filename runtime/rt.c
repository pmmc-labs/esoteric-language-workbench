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

// An integer's operand: a boolean or anything else that isn't one faults
// (D14), which is what the checks before arithmetic are for.
static int64_t int_arg(rt_value v) {
    if ((v & 1) != RT_INT_TAG) rt_fault("not an integer");
    return rt_int_of(v);
}

#define RT_CHECKED(op, a, b) do { int64_t x = int_arg(a); int64_t y = int_arg(b); int64_t r; int o = __builtin_##op##_overflow(x, y, &r); return checked(r, o); } while (0)
rt_value rt_add(rt_value a, rt_value b) { RT_CHECKED(add, a, b); }
rt_value rt_sub(rt_value a, rt_value b) { RT_CHECKED(sub, a, b); }
rt_value rt_mul(rt_value a, rt_value b) { RT_CHECKED(mul, a, b); }

// Division truncates toward zero and the remainder takes the dividend's
// sign, as C's do (D5). RT_INT_MIN / -1 is 2^62, past the range.
rt_value rt_div(rt_value a, rt_value b) {
    int64_t x = int_arg(a);
    int64_t y = int_arg(b);
    if (y == 0) rt_fault("division by zero");
    return checked(x / y, 0);
}
rt_value rt_mod(rt_value a, rt_value b) {
    int64_t x = int_arg(a);
    int64_t y = int_arg(b);
    if (y == 0) rt_fault("division by zero");
    return rt_int(x % y);
}

// The orderings check both operands are integers (D12); each reads its
// operands into a statement of its own, as the arithmetic does above.
#define RT_ORDER(name, op) rt_value rt_##name(rt_value a, rt_value b) { int64_t x = int_arg(a); int64_t y = int_arg(b); return rt_bool(x op y); }
RT_ORDER(lt, <)
RT_ORDER(le, <=)
RT_ORDER(gt, >)
RT_ORDER(ge, >=)

// Equality is on any two values: the encodings are unique, so an integer
// is never equal to a boolean, and two values of different types are
// #false rather than a fault (D12).
rt_value rt_eq(rt_value a, rt_value b) { return rt_bool(a == b); }
rt_value rt_ne(rt_value a, rt_value b) { return rt_bool(a != b); }

// The test of an `if` must be a boolean (D13); anything else faults.
int rt_truth(rt_value v) {
    if (v == RT_TRUE) return 1;
    if (v == RT_FALSE) return 0;
    rt_fault("not a boolean");
}

void rt_print(rt_value v) {
    if ((v & 1) == RT_INT_TAG) printf("%lld", (long long)rt_int_of(v));
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
