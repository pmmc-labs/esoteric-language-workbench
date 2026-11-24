// The core: the context, values as strings and as numbers, the operators,
// printing, faults. A compiled program prints to stdout and exits 0; a
// fault goes to stderr and exits 1.
#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "rt.h"

// 2^53: a double holds every whole number below it, and not every one
// above. 2^63 as a double, which is exact.
#define TWO_53 9007199254740992.0
#define TWO_63 9223372036854775808.0

// Where perl has two answers, by what was done with a value before, and a
// value here has no past to choose by (D36, D40, D45).
#define WHOLE_FLOAT "a whole float this size prints two ways in perl (add 0 to print the integer)"
#define TWO_ANSWERS "an integer this large with a whole float or a string has two answers in perl"
#define EXPONENT "a string with an exponent that is a whole number this large has two values in perl"
#define SOFT "a string like \"3.0\" in arithmetic this large has two answers in perl"
#define NEG_LARGE "a minus before a string that is a whole number this large has two answers in perl"

// ---- the heap

// Every string a program makes is a block on the context's list, and
// stays there until the program ends: there is no collector yet (step 7).
typedef struct rt_block {
    struct rt_block *next;
} rt_block;

static void release(rt_ctx *cx) {
    while (cx->heap) {
        rt_block *next = cx->heap->next;
        free(cx->heap);
        cx->heap = next;
    }
}

int rt_run(void (*body)(rt_ctx *cx), const char *file) {
    rt_ctx cx = { .file = file, .line = 0, .out_utf8 = 0, .heap = NULL };
    body(&cx);
    release(&cx);
    return 0;
}

// A new string of `len` bytes and `chars` characters, for the caller to
// fill through `*bytes`: the one place a string is made, and it is not
// changed after the function that made it returns.
static const rt_str *str_new(rt_ctx *cx, uint64_t len, uint64_t chars, char **bytes) {
    rt_block *block = malloc(sizeof(rt_block) + sizeof(rt_str) + len + 1);
    if (block == NULL) rt_fault(cx, "out of memory");
    block->next = cx->heap;
    cx->heap = block;
    rt_str *s = (rt_str *)(block + 1);
    char *p = (char *)(s + 1);
    p[len] = '\0';
    s->len = len;
    s->chars = chars;
    s->bytes = p;
    *bytes = p;
    return s;
}

// ---- UTF-8

// Every string here is well-formed UTF-8, by how it was made: a literal
// the compiler encoded, `chr`, or pieces of other strings cut between
// characters. So a character's first byte says how long it is, and
// nothing is checked again.
static int continues(char c) {
    return ((unsigned char)c & 0xC0) == 0x80;
}

// The character at p, and how many bytes it is.
static uint32_t decode(const char *p, int *size) {
    const unsigned char *u = (const unsigned char *)p;
    if (u[0] < 0x80) { *size = 1; return u[0]; }
    if (u[0] < 0xE0) { *size = 2; return (uint32_t)(u[0] & 0x1F) << 6 | (u[1] & 0x3F); }
    if (u[0] < 0xF0) { *size = 3; return (uint32_t)(u[0] & 0x0F) << 12 | (uint32_t)(u[1] & 0x3F) << 6 | (u[2] & 0x3F); }
    *size = 4;
    return (uint32_t)(u[0] & 0x07) << 18 | (uint32_t)(u[1] & 0x3F) << 12 | (uint32_t)(u[2] & 0x3F) << 6 | (u[3] & 0x3F);
}

// The byte at which character number `k` begins, for k from 0 to the
// string's length.
static uint64_t offset_of(const rt_str *s, uint64_t k) {
    if (s->len == s->chars) return k;
    uint64_t at = 0;
    while (k > 0) {
        at += 1;
        while (at < s->len && continues(s->bytes[at])) at += 1;
        k -= 1;
    }
    return at;
}

// How many characters begin in the first `n` bytes.
static uint64_t chars_in(const rt_str *s, uint64_t n) {
    if (s->len == s->chars) return n;
    uint64_t count = 0;
    for (uint64_t at = 0; at < n; at++) count += !continues(s->bytes[at]);
    return count;
}

// ---- a number as a string

// A number as perl prints it, into `buf`; the length. A Num is C's
// %.15g, and a zero of either sign is `0`. But a whole Num from 10^15 up
// to 2^53 has no one way to print: perl prints it as a float until it has
// been used as an integer and as an integer after, and a value here
// doesn't carry that past (D36). Below 10^15 the two ways are the same
// digits, and from 2^53 perl never takes a Num for an integer.
//
// Every operator checks its operand's tag, this one too: until types give
// the compiler a reason (step 26), the runtime trusts nothing it is handed.
static int format_number(rt_ctx *cx, rt_value v, char buf[32]) {
    if (v.tag == RT_TAG_INT) return snprintf(buf, 32, "%" PRId64, v.as.i);
    if (v.tag != RT_TAG_NUM) rt_fault(cx, "not a value");
    double x = v.as.n;
    if (x == trunc(x) && fabs(x) >= 1e15 && fabs(x) < TWO_53) rt_fault(cx, WHOLE_FLOAT);
    if (x == 0.0) return snprintf(buf, 32, "0");
    return snprintf(buf, 32, "%.15g", x);
}

// A value where a string is wanted (D24): a Str is itself, and a number
// is what `say` prints for it.
static const rt_str *to_str(rt_ctx *cx, rt_value v) {
    if (v.tag == RT_TAG_STR) return v.as.s;
    char buf[32];
    int len = format_number(cx, v, buf);
    char *bytes;
    const rt_str *s = str_new(cx, (uint64_t)len, (uint64_t)len, &bytes);
    memcpy(bytes, buf, (size_t)len);
    return s;
}

// ---- printing

// The 66 noncharacters: perl warns when it prints one (T88).
static int noncharacter(uint32_t c) {
    return (c >= 0xFDD0 && c <= 0xFDEF) || (c & 0xFFFE) == 0xFFFE;
}

// The file alone says how perl's streams are encoded (D39): without `use
// open`, perl prints a character from U+0080 to U+00FF as one byte and
// warns on a wider one, and neither is what the language prints.
static void emit(rt_ctx *cx, rt_value v, int newline) {
    char buf[32];
    const char *bytes = buf;
    size_t len;
    if (v.tag == RT_TAG_STR) {
        const rt_str *s = v.as.s;
        if (s->len != s->chars) {
            int size;
            for (uint64_t at = 0; at < s->len; at += (uint64_t)size) {
                if (noncharacter(decode(s->bytes + at, &size))) rt_fault(cx, "a noncharacter printed");
            }
            if (!cx->out_utf8) rt_fault(cx, "a character past ASCII printed without 'use open'");
        }
        bytes = s->bytes;
        len = s->len;
    } else {
        len = (size_t)format_number(cx, v, buf);
    }
    fwrite(bytes, 1, len, stdout);
    if (newline) putc('\n', stdout);
}

void rt_use_open(rt_ctx *cx) {
    cx->out_utf8 = 1;
}

void rt_say(rt_ctx *cx, rt_value v) {
    emit(cx, v, 1);
}

void rt_print(rt_ctx *cx, rt_value v) {
    emit(cx, v, 0);
}

// ---- a value as a number

// An operand where a number is wanted: an Int or a Num, and two things an
// operator has to know about where it came from.
typedef struct {
    int is_int;     // an Int, `i`; otherwise a Num, `n`
    int64_t i;
    double n;
    int plain;      // an Int that was an Int, and not a string that is one (D45)
    int soft;       // a string with a point, whole and below 2^53: "3.0" (D40)
} number;

static uint64_t magnitude(int64_t x) {
    return x < 0 ? -(uint64_t)x : (uint64_t)x;
}

static int blank(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f' || c == '\v';
}

static int digit(char c) {
    return c >= '0' && c <= '9';
}

// A string where a number is wanted (D40). It is one of the shapes perl
// takes in silence, in full: blanks, a sign, digits with a point among
// them or not, an exponent, blanks. perl warns on anything else and goes
// on with the number it began with, or 0; that is a fault (D15), and so
// are `Inf`, `NaN` and `0 but true`, which perl takes in silence (D37).
//
// What number it is turns on how it is written, because perl settles a
// string's value the first time it is used as a number, one way for a use
// that wants an integer and another for a float, and keeps it (T83):
//   digits only          the Int. Past the Ints perl goes on as an
//                        unsigned integer and then a float: an overflow.
//   with an exponent     whole and below 2^53, the Int, by either route.
//                        Whole and larger, perl has the integer or the
//                        float: a fault. Otherwise the Num.
//   with a point, and    the Num. Whole and below 2^53, perl adds it as a
//   no exponent          float until it has been used as one, and as an
//                        integer after: `soft`, and the operators say
//                        what that costs.
static number from_string(rt_ctx *cx, const rt_str *s) {
    const char *p = s->bytes;
    const char *end = p + s->len;
    while (p < end && blank(*p)) p++;
    const char *start = p;
    int negative = p < end && *p == '-';
    if (p < end && (*p == '+' || *p == '-')) p++;
    const char *first = p;
    while (p < end && digit(*p)) p++;
    const char *whole_end = p;
    int digits = (int)(p > first);
    int point = p < end && *p == '.';
    if (point) {
        p++;
        digits |= p < end && digit(*p);
        while (p < end && digit(*p)) p++;
    }
    if (!digits) rt_fault(cx, "not a numeric string");
    int exponent = p < end && (*p == 'e' || *p == 'E');
    if (exponent) {
        p++;
        if (p < end && (*p == '+' || *p == '-')) p++;
        if (!(p < end && digit(*p))) rt_fault(cx, "not a numeric string");
        while (p < end && digit(*p)) p++;
    }
    const char *stop = p;
    while (p < end && blank(*p)) p++;
    if (p != end) rt_fault(cx, "not a numeric string");

    number v = { 0 };
    if (!point && !exponent) {
        uint64_t m = 0;
        for (const char *d = first; d < whole_end; d++) {
            int o = __builtin_mul_overflow(m, (uint64_t)10, &m);
            o |= __builtin_add_overflow(m, (uint64_t)(*d - '0'), &m);
            if (o || m > (uint64_t)INT64_MAX + (negative ? 1 : 0)) rt_fault(cx, "integer overflow");
        }
        // 0 - m, in unsigned arithmetic: -2^63 has no positive to negate.
        v.is_int = 1;
        v.i = negative ? (int64_t)(0 - m) : (int64_t)m;
        return v;
    }
    // The C library reads a decimal as perl does, to the nearest double
    // (docs/briefs/step2-literals.py). The text from `start` to `stop` is
    // all it can take: a blank or the string's last NUL comes next.
    char *read_to;
    double x = strtod(start, &read_to);
    if (read_to != stop) rt_fault(cx, "not a numeric string");
    if (isinf(x)) rt_fault(cx, "float overflow");
    int whole = x == trunc(x);
    if (exponent && whole && fabs(x) < TWO_53) {
        v.is_int = 1;
        v.i = (int64_t)x;
        return v;
    }
    if (exponent && whole) rt_fault(cx, EXPONENT);
    // With an exponent a whole number has gone one of the two ways above.
    v.n = x;
    v.soft = whole && fabs(x) < TWO_53;
    return v;
}

// Every operator checks its operands' tags (and faults by name) before it
// believes them.
static number numeric(rt_ctx *cx, rt_value v) {
    number x = { 0 };
    switch (v.tag) {
    case RT_TAG_INT:
        x.is_int = 1;
        x.plain = 1;
        x.i = v.as.i;
        return x;
    case RT_TAG_NUM:
        x.n = v.as.n;
        return x;
    case RT_TAG_STR:
        return from_string(cx, v.as.s);
    default:
        rt_fault(cx, "not a numeric value");
    }
}

// The one question (D35): is this operand integral, an Int or a whole Num
// below 2^53? perl does an operation on whole numbers when both are, and
// on doubles otherwise. A negative zero is integral, and is 0.
static int integral(number v, int64_t *whole) {
    if (v.is_int) {
        *whole = v.i;
        return 1;
    }
    if (v.n == trunc(v.n) && fabs(v.n) < TWO_53) {
        *whole = (int64_t)v.n;
        return 1;
    }
    return 0;
}

static double as_double(number v) {
    return v.is_int ? (double)v.i : v.n;
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

// ---- arithmetic

// D45, which amends D35: perl adds, subtracts and multiplies as floats
// when both operands carry a float, and a whole number that has been used
// as a float carries one from then on, if a double holds it exactly. So
// a whole number of 2^53 or more that is exactly a double (10^16, 2^60)
// has two answers beside anything but an Int: `10000000000000000 + 1.0`
// is 10000000000000001, or 1e+16 once the Int has been divided (T92).
// With an Int perl works on integers whatever came before, and with a Num
// that isn't whole on floats.
static int large_and_exact(int64_t w) {
    uint64_t m = magnitude(w);
    return m >= (uint64_t)1 << 53 && m >> __builtin_ctzll(m) < (uint64_t)1 << 53;
}

static void two_answers(rt_ctx *cx, number x, number y, int64_t p, int64_t q) {
    if ((large_and_exact(p) && !y.plain) || (large_and_exact(q) && !x.plain)) rt_fault(cx, TWO_ANSWERS);
}

// A soft string beside an integral operand (D40): perl works in floats,
// until the string has been used as a float, and in whole numbers after.
// The two agree while nothing is rounded, so this is what must hold of
// the operands; the exact answer is each operator's to check.
static int soft_pair(rt_ctx *cx, number x, number y, int64_t p, int64_t q) {
    if (!x.soft && !y.soft) return 0;
    if (magnitude(p) >= (uint64_t)1 << 53 || magnitude(q) >= (uint64_t)1 << 53) rt_fault(cx, SOFT);
    return 1;
}

static void soft_answer(rt_ctx *cx, int64_t exact, int overflowed) {
    if (overflowed || magnitude(exact) >= (uint64_t)1 << 53) rt_fault(cx, SOFT);
}

// The overflow flag is computed in a statement of its own, and so are the
// two operands: C doesn't order a call's arguments, and `checked(cx, r,
// overflow(..., &r))` read r before it was set under clang.
rt_value rt_add(rt_ctx *cx, rt_value a, rt_value b) {
    number x = numeric(cx, a);
    number y = numeric(cx, b);
    int64_t p, q;
    if (integral(x, &p) && integral(y, &q)) {
        two_answers(cx, x, y, p, q);
        int64_t r;
        int o = __builtin_add_overflow(p, q, &r);
        if (!soft_pair(cx, x, y, p, q)) return checked(cx, r, o);
        soft_answer(cx, r, o);
    }
    return num(cx, as_double(x) + as_double(y));
}

rt_value rt_sub(rt_ctx *cx, rt_value a, rt_value b) {
    number x = numeric(cx, a);
    number y = numeric(cx, b);
    int64_t p, q;
    if (integral(x, &p) && integral(y, &q)) {
        two_answers(cx, x, y, p, q);
        int64_t r;
        int o = __builtin_sub_overflow(p, q, &r);
        if (!soft_pair(cx, x, y, p, q)) return checked(cx, r, o);
        soft_answer(cx, r, o);
    }
    return num(cx, as_double(x) - as_double(y));
}

// Two integral operands whose product isn't an Int: two Ints overflow
// (D23). With a Num among them perl has two answers. A product from 2^63
// to 2^64 - 1 it keeps exactly, as an unsigned integer, which the
// language doesn't have: that stops too (`1e10 * 1e9`). Beyond, it
// multiplies the doubles (`1e10 * 1e10` is 1e+20), and so does this. The
// product is positive and fits 64 unsigned bits exactly when it is in
// that band, the Ints having been ruled out.
rt_value rt_mul(rt_ctx *cx, rt_value a, rt_value b) {
    number x = numeric(cx, a);
    number y = numeric(cx, b);
    int64_t p, q;
    if (integral(x, &p) && integral(y, &q)) {
        two_answers(cx, x, y, p, q);
        int64_t r;
        int o = __builtin_mul_overflow(p, q, &r);
        if (soft_pair(cx, x, y, p, q)) {
            soft_answer(cx, r, o);
        } else {
            if (!o) return rt_int(r);
            uint64_t unsigned_product;
            int past = __builtin_mul_overflow(magnitude(p), magnitude(q), &unsigned_product);
            int positive = (p < 0) == (q < 0);
            if ((x.is_int && y.is_int) || (positive && !past)) rt_fault(cx, "integer overflow");
        }
    }
    return num(cx, as_double(x) * as_double(y));
}

// Division is of doubles, and gives a Num: `6 / 2` is the Num 3. Except
// that perl divides whole numbers when the left one is too large for a
// double to hold (past 2^53, so an Int) and the answer is exact:
// `18014398509481984 / 2` is the Int 9007199254740992, where
// `4000000000000000 / 2` is the Num 2e+15. -1 is taken first, since C's
// `INT64_MIN % -1` is undefined.
rt_value rt_div(rt_ctx *cx, rt_value a, rt_value b) {
    number x = numeric(cx, a);
    number y = numeric(cx, b);
    int64_t p, q;
    int whole = integral(x, &p) && integral(y, &q);
    int soft = whole && soft_pair(cx, x, y, p, q);
    double divisor = as_double(y);
    if (divisor == 0.0) rt_fault(cx, "division by zero");
    if (!soft && x.is_int && magnitude(x.i) > (uint64_t)1 << 53 && integral(y, &q)) {
        if (q == -1) {
            int64_t r;
            int o = __builtin_sub_overflow((int64_t)0, x.i, &r);
            return checked(cx, r, o);
        }
        if (x.i % q == 0) return rt_int(x.i / q);
    }
    return num(cx, as_double(x) / divisor);
}

// An operand of `%` cut to its whole part, toward zero, which must be an
// Int. perl has answers past there, by other routes (`1e20 % 7` is 2, by
// fmod, where `1e19 % 7` is 3, by unsigned integers).
static int64_t whole_part(rt_ctx *cx, number v) {
    if (v.is_int) return v.i;
    double t = trunc(v.n);
    if (!(t >= -TWO_63 && t < TWO_63)) rt_fault(cx, "modulus of a number outside the integers");
    return (int64_t)t;
}

// perl's `%` takes the sign of its right operand, and C's the sign of its
// left: -7 % 3 is 2 in perl and -1 in C. So C's remainder is moved over by
// one divisor when its sign is the wrong one; the two have opposite signs
// then and the sum can't overflow. -1 is answered first: every remainder
// by it is 0, and C's `INT64_MIN % -1` is undefined (it traps on x86).
rt_value rt_mod(rt_ctx *cx, rt_value a, rt_value b) {
    number left = numeric(cx, a);
    number right = numeric(cx, b);
    int64_t x = whole_part(cx, left);
    int64_t y = whole_part(cx, right);
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
//
// With a soft string it is pow, and a fault if the exact answer reaches
// 2^53, where the integer route would have given another.
rt_value rt_pow(rt_ctx *cx, rt_value a, rt_value b) {
    number left = numeric(cx, a);
    number right = numeric(cx, b);
    int64_t x, y;
    if (integral(left, &x) && integral(right, &y)) {
        uint64_t base = magnitude(x);
        if (soft_pair(cx, left, right, x, y)) {
            // Each product is checked, so the one before was below 2^53
            // and this one can't wrap past noticing.
            uint64_t reached = 1;
            for (int64_t n = 0; base > 1 && n < y; n++) {
                int o = __builtin_mul_overflow(reached, base, &reached);
                if (o || reached >= (uint64_t)1 << 53) rt_fault(cx, SOFT);
            }
        } else if (y >= 0) {
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
    }
    return num(cx, pow(as_double(left), as_double(right)));
}

// 0 - x overflows for the one Int that has no negation, -2^63. A Num's
// sign is changed, which makes a negative zero of a zero: `say` prints 0
// for both, and what else can tell them apart faults when it comes (T79).
//
// A minus before a string (D40): the string must be a number, and the
// answer is a Num. perl negates a string of digits as an integer until it
// has been used as a float and as a float after, which is the same number
// while a double holds it: so a whole number of 2^53 or more is a fault.
// And a string that starts with a plus perl negates as text, `-"+0"`
// being the string `-0` (T85), unless it has been used as a number.
rt_value rt_neg(rt_ctx *cx, rt_value a) {
    number x = numeric(cx, a);
    if (a.tag == RT_TAG_STR) {
        if (a.as.s->bytes[0] == '+') rt_fault(cx, "a minus before a string that starts with a plus");
        double d = as_double(x);
        if (d == trunc(d) && fabs(d) >= TWO_53) rt_fault(cx, NEG_LARGE);
        return rt_num(-d);
    }
    if (!x.is_int) return rt_num(-x.n);
    int64_t r;
    int o = __builtin_sub_overflow((int64_t)0, x.i, &r);
    return checked(cx, r, o);
}

// ---- strings

// A number where a whole number is wanted, a count or a position: cut
// toward zero, and then an Int. perl's own cut of a float past the Ints
// is whatever the machine gives: `substr("abc", 0, 1e30)` is `ab`.
static int64_t whole_number(rt_ctx *cx, number v) {
    if (v.is_int) return v.i;
    double t = trunc(v.n);
    if (!(t >= -TWO_63 && t < TWO_63)) rt_fault(cx, "a number outside the integers where a whole number is wanted");
    return (int64_t)t;
}

static int below_zero(number v) {
    return v.is_int ? v.i < 0 : v.n < 0.0;
}

rt_value rt_concat(rt_ctx *cx, rt_value a, rt_value b) {
    const rt_str *s = to_str(cx, a);
    const rt_str *t = to_str(cx, b);
    char *bytes;
    const rt_str *joined = str_new(cx, s->len + t->len, s->chars + t->chars, &bytes);
    memcpy(bytes, s->bytes, s->len);
    memcpy(bytes + s->len, t->bytes, t->len);
    return rt_string(joined);
}

// `x`. perl warns of a count below zero, before it is cut (so of -0.5,
// which cuts to 0), and repeats nothing. A string of 2^31 characters or
// more is refused here: perl would make it if the machine could.
rt_value rt_repeat(rt_ctx *cx, rt_value a, rt_value count) {
    const rt_str *s = to_str(cx, a);
    number c = numeric(cx, count);
    if (below_zero(c)) rt_fault(cx, "negative repeat count");
    uint64_t n = (uint64_t)whole_number(cx, c);
    if (s->chars != 0 && n > (uint64_t)INT32_MAX / s->chars) rt_fault(cx, "repeated string too long");
    if (s->chars == 0) n = 0;
    char *bytes;
    const rt_str *repeated = str_new(cx, s->len * n, s->chars * n, &bytes);
    for (uint64_t k = 0; k < n; k++) memcpy(bytes + k * s->len, s->bytes, s->len);
    return rt_string(repeated);
}

rt_value rt_length(rt_ctx *cx, rt_value a) {
    return rt_int((int64_t)to_str(cx, a)->chars);
}

// `uc` and `lc` change the ASCII letters. Past ASCII perl has tables,
// under which a string can change length (T45); until they come, a
// character past ASCII is a fault.
static rt_value change_case(rt_ctx *cx, rt_value a, char from, char to, const char *fault) {
    const rt_str *s = to_str(cx, a);
    if (s->len != s->chars) rt_fault(cx, fault);
    char *bytes;
    const rt_str *changed = str_new(cx, s->len, s->chars, &bytes);
    for (uint64_t at = 0; at < s->len; at++) {
        char c = s->bytes[at];
        bytes[at] = c >= from && c <= from + 25 ? (char)(c - from + to) : c;
    }
    return rt_string(changed);
}

rt_value rt_uc(rt_ctx *cx, rt_value a) {
    return change_case(cx, a, 'a', 'A', "uc of a character past ASCII");
}

rt_value rt_lc(rt_ctx *cx, rt_value a) {
    return change_case(cx, a, 'A', 'a', "lc of a character past ASCII");
}

rt_value rt_ord(rt_ctx *cx, rt_value a) {
    const rt_str *s = to_str(cx, a);
    if (s->len == 0) return rt_int(0);
    int size;
    return rt_int((int64_t)decode(s->bytes, &size));
}

// A character is a Unicode scalar value (D42). perl makes a "character"
// of any number, a surrogate or one past U+10FFFF, and warns when it is
// printed; and of a number below zero (before it is cut: -0.5) it makes
// U+FFFD, with a warning.
rt_value rt_chr(rt_ctx *cx, rt_value a) {
    number v = numeric(cx, a);
    double t = v.is_int ? (double)v.i : trunc(v.n);
    if (below_zero(v) || t > 0x10FFFF || (t >= 0xD800 && t <= 0xDFFF)) rt_fault(cx, "not a character");
    uint32_t c = (uint32_t)t;
    int size = c < 0x80 ? 1 : c < 0x800 ? 2 : c < 0x10000 ? 3 : 4;
    char *bytes;
    const rt_str *s = str_new(cx, (uint64_t)size, 1, &bytes);
    if (size == 1) {
        bytes[0] = (char)c;
    } else {
        // The first byte: as many high bits set as there are bytes.
        bytes[0] = (char)((0xF00 >> size & 0xFF) | c >> 6 * (size - 1));
        for (int k = 1; k < size; k++) bytes[k] = (char)(0x80 | (c >> 6 * (size - 1 - k) & 0x3F));
    }
    return rt_string(s);
}

// `substr`, reading. A start below zero counts from the end, and so does
// a length below zero. Then, as perl has it: a start past the end, or a
// piece that starts and ends before the beginning, is outside the string
// (perl warns, and gives undef); otherwise the piece is moved in to what
// the string has. `has_count` is 0 for the two-argument form.
static rt_value substring(rt_ctx *cx, rt_value a, rt_value offset, rt_value count, int has_count) {
    const rt_str *s = to_str(cx, a);
    int64_t off = whole_number(cx, numeric(cx, offset));
    int64_t n = has_count ? whole_number(cx, numeric(cx, count)) : 0;
    int64_t size = (int64_t)s->chars;
    int64_t start = off < 0 ? off + size : off;
    int64_t end = size;
    // The sum is past every string when it is past the Ints.
    if (has_count && n >= 0 && __builtin_add_overflow(start, n, &end)) end = INT64_MAX;
    if (has_count && n < 0) end = size + n;
    if (start > size || (start < 0 && end < 0)) rt_fault(cx, "substr outside of string");
    if (start < 0) start = 0;
    if (end > size) end = size;
    if (end < start) end = start;
    uint64_t from = offset_of(s, (uint64_t)start);
    uint64_t to = offset_of(s, (uint64_t)end);
    char *bytes;
    const rt_str *piece = str_new(cx, to - from, (uint64_t)(end - start), &bytes);
    memcpy(bytes, s->bytes + from, to - from);
    return rt_string(piece);
}

rt_value rt_substr2(rt_ctx *cx, rt_value a, rt_value offset) {
    return substring(cx, a, offset, offset, 0);
}

rt_value rt_substr3(rt_ctx *cx, rt_value a, rt_value offset, rt_value count) {
    return substring(cx, a, offset, count, 1);
}

// `index`: where `b` first is in `a`, at or after a position, which is
// moved into the string; -1 if nowhere. Bytes are compared: a match can
// only begin at a character, since the first byte of one is never a later
// byte of another.
static rt_value find(rt_ctx *cx, rt_value a, rt_value b, int64_t position) {
    const rt_str *s = to_str(cx, a);
    const rt_str *t = to_str(cx, b);
    if (position < 0) position = 0;
    if (position > (int64_t)s->chars) position = (int64_t)s->chars;
    for (uint64_t at = offset_of(s, (uint64_t)position); at + t->len <= s->len; at++) {
        if (memcmp(s->bytes + at, t->bytes, t->len) == 0) return rt_int((int64_t)chars_in(s, at));
    }
    return rt_int(-1);
}

rt_value rt_index2(rt_ctx *cx, rt_value a, rt_value b) {
    return find(cx, a, b, 0);
}

rt_value rt_index3(rt_ctx *cx, rt_value a, rt_value b, rt_value position) {
    // The two strings are made before the position is a number, as the
    // arguments are written.
    const rt_str *s = to_str(cx, a);
    const rt_str *t = to_str(cx, b);
    return find(cx, rt_string(s), rt_string(t), whole_number(cx, numeric(cx, position)));
}

// stdout is flushed first, so that what the program printed before the
// fault comes before the fault's line wherever the two streams meet: the
// start of perl's output, then the stop (D12).
void rt_fault(rt_ctx *cx, const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s at %s line %" PRId64 ".\n", what, cx->file, cx->line);
    release(cx);
    exit(1);
}
