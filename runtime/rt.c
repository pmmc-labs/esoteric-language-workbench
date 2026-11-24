// The core: the context, printing, faults. A compiled program prints to
// stdout and exits 0; a fault goes to stderr and exits 1.
#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

int rt_run(void (*body)(rt_ctx *cx), const char *file) {
    rt_ctx cx = { .file = file, .line = 0 };
    body(&cx);
    return 0;
}

// 2^53: a double holds every whole number below it, and not every one
// above. 2^63 as a double, which is exact.
#define TWO_53 9007199254740992.0
#define TWO_63 9223372036854775808.0

// Every operator checks its operand's tag, this one too: until types give
// the compiler a reason (step 26), the runtime trusts nothing it is handed.
//
// A Num prints as perl prints it, which is C's %.15g, and a zero of
// either sign as `0`. But a whole Num from 10^15 up to 2^53 has no one
// way to print: perl prints it as a float until it has been used as an
// integer and as an integer after, and a value here doesn't carry that
// past (D36). Below 10^15 the two ways are the same digits, and from 2^53
// perl never takes a Num for an integer.
void rt_say(rt_ctx *cx, rt_value v) {
    switch (v.tag) {
    case RT_TAG_INT:
        printf("%" PRId64 "\n", v.as.i);
        return;
    case RT_TAG_NUM: {
        double x = v.as.n;
        if (x == trunc(x) && fabs(x) >= 1e15 && fabs(x) < TWO_53) {
            rt_fault(cx, "a whole float this size prints two ways in perl (add 0 to print the integer)");
        }
        if (x == 0.0) printf("0\n");
        else printf("%.15g\n", x);
        return;
    }
    default:
        rt_fault(cx, "not a value");
    }
}

// Every operator checks its operands' tags (and faults by name) before it
// believes them. Only numbers can reach these yet; step 3 brings strings,
// and with them what a string that isn't a number does here.
static void need_number(rt_ctx *cx, rt_value v) {
    if (v.tag != RT_TAG_INT && v.tag != RT_TAG_NUM) rt_fault(cx, "not a numeric value");
}

// The one question (D35): is this operand integral, an Int or a whole Num
// below 2^53? perl does an operation on whole numbers when both are, and
// on doubles otherwise. A negative zero is integral, and is 0.
static int integral(rt_value v, int64_t *whole) {
    if (v.tag == RT_TAG_INT) {
        *whole = v.as.i;
        return 1;
    }
    double x = v.as.n;
    if (x == trunc(x) && fabs(x) < TWO_53) {
        *whole = (int64_t)x;
        return 1;
    }
    return 0;
}

static double as_double(rt_value v) {
    return v.tag == RT_TAG_INT ? (double)v.as.i : v.as.n;
}

// A Num is finite (D37): perl would go on with an infinity or a NaN.
static rt_value num(rt_ctx *cx, double x) {
    if (isinf(x)) rt_fault(cx, "float overflow");
    if (isnan(x)) rt_fault(cx, "not a number");
    return rt_num(x);
}

// perl goes on past 2^63 as an unsigned integer and then a float; the
// language has neither, and stops (D23).
static rt_value checked(rt_ctx *cx, int64_t n, int overflowed) {
    if (overflowed) rt_fault(cx, "integer overflow");
    return rt_int(n);
}

// The overflow flag is computed in a statement of its own, and so are the
// two operands: C doesn't order a call's arguments, and `checked(cx, r,
// overflow(..., &r))` read r before it was set under clang.
rt_value rt_add(rt_ctx *cx, rt_value a, rt_value b) {
    need_number(cx, a);
    need_number(cx, b);
    int64_t x, y;
    if (integral(a, &x) && integral(b, &y)) {
        int64_t r;
        int o = __builtin_add_overflow(x, y, &r);
        return checked(cx, r, o);
    }
    return num(cx, as_double(a) + as_double(b));
}

rt_value rt_sub(rt_ctx *cx, rt_value a, rt_value b) {
    need_number(cx, a);
    need_number(cx, b);
    int64_t x, y;
    if (integral(a, &x) && integral(b, &y)) {
        int64_t r;
        int o = __builtin_sub_overflow(x, y, &r);
        return checked(cx, r, o);
    }
    return num(cx, as_double(a) - as_double(b));
}

static uint64_t magnitude(int64_t x) {
    return x < 0 ? -(uint64_t)x : (uint64_t)x;
}

// Two integral operands whose product isn't an Int: two Ints overflow
// (D23). With a Num among them perl has two answers. A product from 2^63
// to 2^64 - 1 it keeps exactly, as an unsigned integer, which the
// language doesn't have: that stops too (`1e10 * 1e9`). Beyond, it
// multiplies the doubles (`1e10 * 1e10` is 1e+20), and so does this. The
// product is positive and fits 64 unsigned bits exactly when it is in
// that band, the Ints having been ruled out.
rt_value rt_mul(rt_ctx *cx, rt_value a, rt_value b) {
    need_number(cx, a);
    need_number(cx, b);
    int64_t x, y;
    if (integral(a, &x) && integral(b, &y)) {
        int64_t r;
        int o = __builtin_mul_overflow(x, y, &r);
        if (!o) return rt_int(r);
        uint64_t unsigned_product;
        int past = __builtin_mul_overflow(magnitude(x), magnitude(y), &unsigned_product);
        int positive = (x < 0) == (y < 0);
        if ((a.tag == RT_TAG_INT && b.tag == RT_TAG_INT) || (positive && !past)) rt_fault(cx, "integer overflow");
    }
    return num(cx, as_double(a) * as_double(b));
}

// Division is of doubles, and gives a Num: `6 / 2` is the Num 3. Except
// that perl divides whole numbers when the left one is too large for a
// double to hold (past 2^53, so an Int) and the answer is exact:
// `18014398509481984 / 2` is the Int 9007199254740992, where
// `4000000000000000 / 2` is the Num 2e+15. -1 is taken first, since C's
// `INT64_MIN % -1` is undefined.
rt_value rt_div(rt_ctx *cx, rt_value a, rt_value b) {
    need_number(cx, a);
    need_number(cx, b);
    double divisor = as_double(b);
    if (divisor == 0.0) rt_fault(cx, "division by zero");
    int64_t y;
    if (a.tag == RT_TAG_INT && magnitude(a.as.i) > (uint64_t)1 << 53 && integral(b, &y)) {
        int64_t x = a.as.i;
        if (y == -1) return rt_neg(cx, a);
        if (x % y == 0) return rt_int(x / y);
    }
    return num(cx, as_double(a) / divisor);
}

// An operand of `%` cut to its whole part, toward zero, which must be an
// Int. perl has answers past there, by other routes (`1e20 % 7` is 2, by
// fmod, where `1e19 % 7` is 3, by unsigned integers).
static int64_t whole_part(rt_ctx *cx, rt_value v) {
    if (v.tag == RT_TAG_INT) return v.as.i;
    double t = trunc(v.as.n);
    if (!(t >= -TWO_63 && t < TWO_63)) rt_fault(cx, "modulus of a number outside the integers");
    return (int64_t)t;
}

// perl's `%` takes the sign of its right operand, and C's the sign of its
// left: -7 % 3 is 2 in perl and -1 in C. So C's remainder is moved over by
// one divisor when its sign is the wrong one; the two have opposite signs
// then and the sum can't overflow. -1 is answered first: every remainder
// by it is 0, and C's `INT64_MIN % -1` is undefined (it traps on x86).
rt_value rt_mod(rt_ctx *cx, rt_value a, rt_value b) {
    need_number(cx, a);
    need_number(cx, b);
    int64_t x = whole_part(cx, a);
    int64_t y = whole_part(cx, b);
    if (y == 0) rt_fault(cx, "modulus by zero");
    if (y == -1) return rt_int(0);
    int64_t r = x % y;
    if (r != 0 && (r < 0) != (y < 0)) r += y;
    return rt_int(r);
}

// `**`, as perl has it. A whole number to a whole power of 0 or more goes
// one of three ways. A base of 0, 1, -1 or plus or minus a power of two:
// a Num, by squaring in doubles, which is exact until it overflows, so
// `2 ** 10` is the Num 1024 and `2 ** 62` prints 4.61168601842739e+18.
// Any other base, when its bits times the power come to 64 or fewer: the
// exact Int, which then fits 64 unsigned bits, so `10 ** 15` is an Int and
// `4294967295 ** 2` overflows. Everything else, and every operand that
// isn't integral or power that is negative: the C library's pow.
// (perl makes the bits-times-power test in 64 bits, where a vast power
// wraps it, and prints 0 for `10 ** 4611686018427387904`: T77. Here the
// test is `power <= 64 / bits`, which can't wrap, and that case is pow's.)
rt_value rt_pow(rt_ctx *cx, rt_value a, rt_value b) {
    need_number(cx, a);
    need_number(cx, b);
    int64_t x, y;
    if (integral(a, &x) && integral(b, &y) && y >= 0) {
        uint64_t base = magnitude(x);
        uint64_t power = (uint64_t)y;
        if ((base & (base - 1)) == 0) {
            double result = 1.0;
            double square = x < 0 ? -(double)base : (double)base;
            if (power & 1) result *= square;
            while (power >>= 1) {
                square *= square;
                if (power & 1) result *= square;
            }
            return num(cx, result);
        }
        uint64_t bits = 64 - (uint64_t)__builtin_clzll(base);
        if (power <= 64 / bits) {
            uint64_t result = 1;
            int negative = x < 0 && (power & 1);
            for (uint64_t n = 0; n < power; n++) result *= base;
            if (result > (uint64_t)INT64_MAX + (negative ? 1 : 0)) rt_fault(cx, "integer overflow");
            return rt_int(negative ? (int64_t)(0 - result) : (int64_t)result);
        }
    }
    return num(cx, pow(as_double(a), as_double(b)));
}

// 0 - x overflows for the one Int that has no negation, -2^63. A Num's
// sign is changed, which makes a negative zero of a zero: `say` prints 0
// for both, and what else can tell them apart faults when it comes (T79).
rt_value rt_neg(rt_ctx *cx, rt_value a) {
    need_number(cx, a);
    if (a.tag == RT_TAG_NUM) return rt_num(-a.as.n);
    int64_t r;
    int o = __builtin_sub_overflow((int64_t)0, a.as.i, &r);
    return checked(cx, r, o);
}

// stdout is flushed first, so that what the program printed before the
// fault comes before the fault's line wherever the two streams meet: the
// start of perl's output, then the stop (D12).
void rt_fault(rt_ctx *cx, const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s at %s line %" PRId64 ".\n", what, cx->file, cx->line);
    exit(1);
}
