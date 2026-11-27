// The core: the context, values as strings and as numbers, the operators,
// printing, faults. A compiled program prints to stdout and exits 0; a
// fault goes to stderr and exits 1.
#include <errno.h>
#include <inttypes.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
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
#define SPLIT "a string with a point this close to the next whole number has two values in perl"
#define NEG_LARGE "a minus before a string that is a whole number this large has two answers in perl"

// ---- the heap, and its collector (D26, D66)

// Every string a program makes is a block on the context's list: this
// header, the rt_str, its bytes. One that no slot of any frame holds is
// garbage, and a collection frees it.
//
// The rule everything here leans on: a value the program can still use is
// in a slot whenever a collection can happen, and one can happen only
// inside `str_new`. So a runtime function allocates at most once, as the
// last thing it does (its operands are still in its caller's slots, and
// what it makes is in a slot before anything allocates again), or it
// opens a frame of its own for what it makes.
typedef struct rt_block {
    struct rt_block *next;
    uint64_t size;          // of the whole block, this header and the string
    uint64_t marked;        // bit 0: reached, in the collection that is running;
                            // bit 1: an rt_array follows, and not an rt_str
} rt_block;

#define REACHED ((uint64_t)1)
#define IS_ARRAY ((uint64_t)2)

// An array's values are storage of its own, which grows; it is counted
// with the block against the cap.
static uint64_t storage(const rt_array *a) {
    return a->room * sizeof(rt_value) + a->slots * sizeof(uint32_t);
}

// With no knob set, the first collection comes after this many bytes, and
// each one after when as many have been allocated as were live after the
// last, or this many if that is more: the heap about doubles between two.
#define FIRST_COLLECTION ((uint64_t)1 << 20)

static void free_list(rt_block *list) {
    while (list) {
        rt_block *next = list->next;
        if (list->marked & IS_ARRAY) {
            free(((rt_array *)(list + 1))->items);
            free(((rt_array *)(list + 1))->index);
        }
        free(list);
        list = next;
    }
}

static void sorts_release(rt_ctx *cx);
// unwind.c's (step 15): the freezes as a stack, for a `die` to give back.
static void sorts_release_to(rt_ctx *cx, struct rt_sort *keep);
static void unwind_frozen(rt_ctx *cx, rt_array *a);
static void unwind_thawed(rt_ctx *cx, rt_array *a);
static void unwind_release(rt_ctx *cx);

static void release(rt_ctx *cx) {
    sorts_release(cx);
    unwind_release(cx);
    free_list(cx->heap);
    free_list(cx->dead);
    cx->heap = NULL;
    cx->dead = NULL;
}

// A string that is being read. One that was collected is a root the
// collector was not shown: its bytes are poison, and under the poison
// knob its memory is still its own, so this is seen every time.
static const rt_str *alive(rt_ctx *cx, const rt_str *s) {
    if (s->where == RT_STR_DEAD) rt_internal(cx, "a string was used after it was collected");
    return s;
}

// What a frame counts for against the limit on recursion (D68).
static uint64_t weight(uint64_t count) {
    return count * sizeof(rt_value) + RT_CALL_BYTES;
}

void rt_enter(rt_ctx *cx, rt_frame *frame, rt_value *slots, uint64_t count) {
    // Before the frame is touched: the line is still the caller's.
    if (weight(count) > RT_DEPTH_LIMIT - cx->deep) rt_fault(cx, "recursion too deep");
    cx->deep += weight(count);
    memset(slots, 0, count * sizeof(rt_value));
    frame->prev = cx->frames;
    frame->count = count;
    frame->slots = slots;
    cx->frames = frame;
}

void rt_leave(rt_ctx *cx, rt_frame *frame) {
    if (cx->frames != frame) rt_internal(cx, "a frame was closed that is not the newest");
    cx->frames = frame->prev;
    cx->deep -= weight(frame->count);
}

static void mark_string(rt_ctx *cx, rt_value v) {
    if (v.tag == RT_TAG_ARRAY || v.tag == RT_TAG_HASH) rt_internal(cx, "an array holds an array");
    if (v.tag != RT_TAG_STR) return;
    if (v.as.s->where == RT_STR_DEAD) rt_internal(cx, "a slot holds a string that was collected");
    if (v.as.s->where == RT_STR_HEAP) ((rt_block *)v.as.s - 1)->marked |= REACHED;
}

void rt_collect(rt_ctx *cx) {
    cx->collections += 1;
    // Mark: every slot of every frame, and through an array to the values
    // it holds. An array holds no array (step 13 will bring that, and a
    // stack of what is still to be walked, so that C's is not used).
    for (rt_frame *frame = cx->frames; frame; frame = frame->prev) {
        for (uint64_t k = 0; k < frame->count; k++) {
            rt_value v = frame->slots[k];
            if (v.tag == RT_TAG_ARRAY || v.tag == RT_TAG_HASH) {
                rt_array *a = v.as.a;
                if (a->dead) rt_internal(cx, "a slot holds an array that was collected");
                ((rt_block *)a - 1)->marked |= REACHED;
                for (uint64_t n = 0; n < a->count; n++) mark_string(cx, a->items[n]);
                continue;
            }
            mark_string(cx, v);
        }
    }
    // Sweep: what was not reached is poisoned, and freed; or, under the
    // poison knob, kept where nothing will be put in its place.
    uint64_t live = 0;
    rt_block **link = &cx->heap;
    while (*link) {
        rt_block *block = *link;
        if (block->marked & REACHED) {
            block->marked &= ~REACHED;
            live += block->size;
            link = &block->next;
            continue;
        }
        *link = block->next;
        cx->objects -= 1;
        if (block->marked & IS_ARRAY) {
            // Its values go at once, poison or not: what is kept is the
            // array itself, marked dead, for whoever still points at it.
            rt_array *a = (rt_array *)(block + 1);
            cx->held -= storage(a);
            block->size -= storage(a);
            free(a->items);
            free(a->index);
            a->items = NULL;
            a->index = NULL;
            a->count = a->room = a->slots = 0;
            a->dead = 1;
        } else {
            rt_str *s = (rt_str *)(block + 1);
            memset((char *)(s + 1), '~', s->len);
            s->where = RT_STR_DEAD;
        }
        if (cx->poison) {
            block->next = cx->dead;
            cx->dead = block;
        } else {
            cx->held -= block->size;
            free(block);
        }
    }
    cx->since = 0;
    cx->threshold = live > FIRST_COLLECTION ? live : FIRST_COLLECTION;
}

// A knob (D63): a whole number in digits, and unset, empty or 0 is off.
// Anything else stops the program before it starts: a knob that was
// misread would be a test that passed for the wrong reason.
static uint64_t knob(const char *name, uint64_t most) {
    const char *text = getenv(name);
    if (text == NULL || text[0] == '\0') return 0;
    uint64_t n = 0;
    for (const char *p = text; *p; p++) {
        int overflowed = *p < '0' || *p > '9' || __builtin_mul_overflow(n, (uint64_t)10, &n) || __builtin_add_overflow(n, (uint64_t)(*p - '0'), &n);
        if (overflowed || n > most) {
            fprintf(stderr, "curly: %s is '%s': it is a whole number from 0 to %" PRIu64 ", in digits\n", name, text, most);
            exit(2);
        }
    }
    return n;
}

int rt_run(void (*body)(rt_ctx *cx), const char *file) {
    rt_ctx cx = { .file = file, .threshold = FIRST_COLLECTION };
    cx.stress = knob("CURLY_GC_STRESS", UINT32_MAX);
    cx.poison = knob("CURLY_GC_POISON", 1);
    cx.cap = knob("CURLY_HEAP_CAP", (uint64_t)1 << 62);
    // The limit on recursion is counted, and must be reached before the C
    // stack ends (D68): so the stack has to be what the count assumes.
    struct rlimit stack;
    if (getrlimit(RLIMIT_STACK, &stack) == 0 && stack.rlim_cur != RLIM_INFINITY && (uint64_t)stack.rlim_cur < RT_STACK_NEEDED) {
        fprintf(stderr, "curly: the stack is limited to %" PRIu64 " bytes, and a program needs %" PRIu64 " (ulimit -s)\n",
                (uint64_t)stack.rlim_cur, RT_STACK_NEEDED);
        exit(2);
    }
    body(&cx);
    // The generated C closes what it opens; a frame still here would be
    // one the next function's collections walked after its slots were gone.
    if (cx.frames != NULL) rt_internal(&cx, "a frame was left open");
    release(&cx);
    return 0;
}

// A new string of `len` bytes and `chars` characters, for the caller to
// fill through `*bytes`: the one place a string is made, and it is not
// changed after the function that made it returns. And the one place a
// collection can happen: before the string is made, so that what is made
// is never looked at before it is in a slot.
static rt_block *block_new(rt_ctx *cx, uint64_t size) {
    cx->allocations += 1;
    int collected = 0;
    // The stress knob: every nth allocation (D63). Otherwise, when enough
    // has been allocated since the last (D66).
    if ((cx->stress != 0 && cx->allocations % cx->stress == 0) || cx->since > cx->threshold) {
        rt_collect(cx);
        collected = 1;
    }
    // The cap is on what is held (D65): what is alive, and under poison
    // the dead that are kept. Garbage is not held once it is collected, so
    // a collection comes before the fault.
    if (cx->cap != 0 && (size > cx->cap || cx->held > cx->cap - size)) {
        if (!collected) rt_collect(cx);
        collected = 1;
        if (size > cx->cap || cx->held > cx->cap - size) rt_fault(cx, "out of memory");
    }
    rt_block *block = malloc(size);
    if (block == NULL && !collected) {
        rt_collect(cx);
        block = malloc(size);
    }
    if (block == NULL) rt_fault(cx, "out of memory");
    block->size = size;
    block->marked = 0;
    cx->held += size;
    cx->since += size;
    cx->objects += 1;
    block->next = cx->heap;
    cx->heap = block;
    return block;
}

static const rt_str *str_new(rt_ctx *cx, uint64_t len, uint64_t chars, char **bytes) {
    rt_block *block = block_new(cx, sizeof(rt_block) + sizeof(rt_str) + len + 1);
    rt_str *s = (rt_str *)(block + 1);
    char *p = (char *)(s + 1);
    p[len] = '\0';
    s->len = len;
    s->chars = chars;
    s->bytes = p;
    s->where = RT_STR_HEAP;
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

// A boolean as a string (D47): `1`, or nothing.
static const rt_str STR_TRUE = { 1, 1, "1", RT_STR_CONSTANT };
static const rt_str STR_FALSE = { 0, 0, "", RT_STR_CONSTANT };

// A number as a string, for as long as one operation runs: on the C
// stack, in its caller's own (D66). It is never made on the heap, so
// reading a number as a string is no allocation, and a function that
// reads two and makes one string allocates once.
typedef struct {
    rt_str s;
    char bytes[32];
} scratch;

// A value where a string is wanted (D24): a Str is itself, a number is
// what `say` prints for it, a boolean is `1` or the empty string, and an
// undef is a fault: perl warns, and goes on with the empty string (D48).
static const rt_str *to_str(rt_ctx *cx, rt_value v, scratch *number) {
    if (v.tag == RT_TAG_STR) return alive(cx, v.as.s);
    if (v.tag == RT_TAG_BOOL) return v.as.i ? &STR_TRUE : &STR_FALSE;
    if (v.tag == RT_TAG_UNDEF) rt_fault(cx, "undef where a string is wanted");
    int len = format_number(cx, v, number->bytes);
    number->s.len = (uint64_t)len;
    number->s.chars = (uint64_t)len;
    number->s.bytes = number->bytes;
    number->s.where = RT_STR_SCRATCH;
    return &number->s;
}

// ---- printing

// The 66 noncharacters: perl warns when it prints one (T88).
static int noncharacter(uint32_t c) {
    return (c >= 0xFDD0 && c <= 0xFDEF) || (c & 0xFFFE) == 0xFFFE;
}

// The file alone says how perl's streams are encoded (D39): without `use
// open`, perl prints a character from U+0080 to U+00FF as one byte and
// warns on a wider one, and neither is what the language prints.
static void emit_checked(rt_ctx *cx, rt_value v, int newline, int write);

static void emit(rt_ctx *cx, rt_value v, int newline) {
    emit_checked(cx, v, newline, 1);
}

// `write` 0 is the look alone: every fault a value can raise as it is
// printed, and nothing printed.
static void emit_checked(rt_ctx *cx, rt_value v, int newline, int write) {
    char buf[32];
    const char *bytes = buf;
    size_t len;
    if (v.tag == RT_TAG_STR || v.tag == RT_TAG_BOOL || v.tag == RT_TAG_UNDEF) {
        scratch none;
        const rt_str *s = to_str(cx, v, &none);
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
    if (!write) return;
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
    int split;      // a string with a point whose digits before it aren't its
                    // number cut to a whole one: "0.99999999999999995", which
                    // is the double 1 (T103)
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
    errno = 0;
    double x = strtod(start, &read_to);
    if (read_to != stop) rt_fault(cx, "not a numeric string");
    // perl's own read of it sets errno, which an uncaught `die` exits
    // with (T319, D151): noted, for `rt_throw`.
    int nonzero = 0;
    for (const char *d = first; d < stop && *d != 'e' && *d != 'E'; d++) nonzero |= *d >= '1' && *d <= '9';
    if (errno == ERANGE || (x != 0.0 && fpclassify(x) == FP_SUBNORMAL) || (x == 0.0 && nonzero)) cx->underflowed = 1;
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
    // Where a whole number is wanted, perl takes the digits before the
    // point of a string it has not used as a float, and the double cut
    // toward zero of one it has. They differ when the digits after the
    // point round the double up to the next whole number.
    if (!exponent && fabs(x) < TWO_63) {
        uint64_t before = 0;
        int o = 0;
        for (const char *d = first; d < whole_end; d++) {
            o |= __builtin_mul_overflow(before, (uint64_t)10, &before);
            o |= __builtin_add_overflow(before, (uint64_t)(*d - '0'), &before);
        }
        v.split = o || before != (uint64_t)trunc(fabs(x));
    }
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
        return from_string(cx, alive(cx, v.as.s));
    case RT_TAG_BOOL:
        // The Int 1 or 0, and nothing less: perl has one answer for a
        // boolean beside any operand, whatever its past (D47).
        x.is_int = 1;
        x.plain = 1;
        x.i = v.as.i;
        return x;
    case RT_TAG_UNDEF:
        rt_fault(cx, "undef where a number is wanted");
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

// `+=` and `-=` with an undef on the left: perl takes it for 0, and says
// nothing (D56).
rt_value rt_add_to(rt_ctx *cx, rt_value a, rt_value b) {
    return rt_add(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);
}

rt_value rt_sub_from(rt_ctx *cx, rt_value a, rt_value b) {
    return rt_sub(cx, a.tag == RT_TAG_UNDEF ? rt_int(0) : a, b);
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
    errno = 0;
    double r = pow(as_double(left), as_double(right));
    // As a string's read does (T319, D151).
    if (errno == ERANGE || (r != 0.0 && fpclassify(r) == FP_SUBNORMAL) || (r == 0.0 && as_double(left) != 0.0)) cx->underflowed = 1;
    return num(cx, r);
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
        if (alive(cx, a.as.s)->bytes[0] == '+') rt_fault(cx, "a minus before a string that starts with a plus");
        double d = as_double(x);
        if (d == trunc(d) && fabs(d) >= TWO_53) rt_fault(cx, NEG_LARGE);
        return rt_num(-d);
    }
    if (!x.is_int) return rt_num(-x.n);
    int64_t r;
    int o = __builtin_sub_overflow((int64_t)0, x.i, &r);
    return checked(cx, r, o);
}

// ---- stepping

// `++` and `--`, by what the variable holds (D52). perl has a route of
// its own for each kind, and for some of them two, by what the variable
// has been used as: docs/briefs/step5-increments.py.
//   undef, a boolean   the Int.
//   an Int             one more or less, or an overflow.
//   a Num              `++`: as `$x + 1` is, the Int if the Num is
//                      integral. `--`: the Num one less, always: perl
//                      subtracts as a float unless the Num has been used
//                      as an integer, and the two part when the answer
//                      reaches 2^53 (T93). Either: a Num of 2^53 or
//                      more, either side of zero; perl warns.
//   a string           its number (D40), and then the Num: perl steps a
//                      fresh string of digits as text, "12" to the string
//                      "13", and one it has used as a number as an
//                      integer, which are the same while a double holds
//                      them and the digits don't begin with a zero ("009"
//                      to "010", or to 10: T113). A string that isn't a
//                      number is a fault here: perl makes the next
//                      string of one, "aa" to "ab" (T44).
static rt_value step(rt_ctx *cx, rt_value a, int d) {
    if (a.tag == RT_TAG_UNDEF) return rt_int(d);
    if (a.tag == RT_TAG_BOOL) return rt_int(a.as.i + d);
    number x = numeric(cx, a);
    if (a.tag == RT_TAG_STR) {
        double f = as_double(x);
        // Every double of 2^53 and up is whole.
        if (fabs(f) >= TWO_53 || fabs(f + d) >= TWO_53) {
            rt_fault(cx, "++ or -- on a string that is a whole number this large has two answers in perl");
        }
        const rt_str *s = alive(cx, a.as.s);
        int digits = s->len > 1 && s->bytes[0] == '0';
        for (uint64_t at = 0; digits && at < s->len; at++) digits = digit(s->bytes[at]);
        if (d > 0 && digits) rt_fault(cx, "++ on a string of digits that begins with a zero has two answers in perl");
        return rt_num(f + d);
    }
    if (x.is_int) {
        int64_t r;
        int o = __builtin_add_overflow(x.i, (int64_t)d, &r);
        return checked(cx, r, o);
    }
    int64_t whole;
    int is_whole = integral(x, &whole);
    if (d > 0 && is_whole) return rt_int(whole + 1);
    // Where perl warns `Lost precision`, which is by where the float is
    // and not by whether the step was lost: 2^53 + 2 and one more is a
    // tie that rounds away, and it warns (T130).
    if (d > 0 ? x.n >= TWO_53 || x.n < -TWO_53 : x.n > TWO_53 || x.n <= -TWO_53) rt_fault(cx, "a float too large to step by one");
    if (is_whole && magnitude(whole - 1) >= (uint64_t)1 << 53) rt_fault(cx, "-- on a whole float that reaches 2^53 has two answers in perl");
    return rt_num(x.n + d);
}

rt_value rt_inc(rt_ctx *cx, rt_value a) {
    return step(cx, a, 1);
}

rt_value rt_dec(rt_ctx *cx, rt_value a) {
    return step(cx, a, -1);
}

// `$x++` on an undef is worth 0, where `$x--` is worth the undef (T43).
rt_value rt_before_inc(rt_ctx *cx, rt_value a) {
    return rt_is_undef(cx, a) ? rt_int(0) : a;
}

// ---- strings

// A number where a whole number is wanted, a count or a position: cut
// toward zero, and then an Int. perl's own cut of a float past the Ints
// is whatever the machine gives: `substr("abc", 0, 1e30)` is `ab`.
static int64_t whole_number(rt_ctx *cx, number v) {
    if (v.is_int) return v.i;
    double t = trunc(v.n);
    if (!(t >= -TWO_63 && t < TWO_63)) rt_fault(cx, "a number outside the integers where a whole number is wanted");
    if (v.split) rt_fault(cx, SPLIT);
    return (int64_t)t;
}

static int below_zero(number v) {
    return v.is_int ? v.i < 0 : v.n < 0.0;
}

rt_value rt_concat_to(rt_ctx *cx, rt_value a, rt_value b) {
    return rt_concat(cx, a.tag == RT_TAG_UNDEF ? rt_string(&STR_FALSE) : a, b);
}

// (An operand is read after the allocation, which may have been a
// collection: so it is looked at again there. Under stress a root that
// was missed is collected in the very operation that reads it.)
rt_value rt_concat(rt_ctx *cx, rt_value a, rt_value b) {
    scratch x, y;
    const rt_str *s = to_str(cx, a, &x);
    const rt_str *t = to_str(cx, b, &y);
    char *bytes;
    const rt_str *joined = str_new(cx, s->len + t->len, s->chars + t->chars, &bytes);
    alive(cx, s);
    alive(cx, t);
    memcpy(bytes, s->bytes, s->len);
    memcpy(bytes + s->len, t->bytes, t->len);
    return rt_string(joined);
}

// `x`. perl warns of a count below zero, before it is cut (so of -0.5,
// which cuts to 0), and repeats nothing. A string of 2^31 characters or
// more is refused here: perl would make it if the machine could.
rt_value rt_repeat(rt_ctx *cx, rt_value a, rt_value count) {
    scratch x;
    const rt_str *s = to_str(cx, a, &x);
    number c = numeric(cx, count);
    if (below_zero(c)) rt_fault(cx, "negative repeat count");
    uint64_t n = (uint64_t)whole_number(cx, c);
    if (s->chars != 0 && n > (uint64_t)INT32_MAX / s->chars) rt_fault(cx, "repeated string too long");
    if (s->chars == 0) n = 0;
    char *bytes;
    const rt_str *repeated = str_new(cx, s->len * n, s->chars * n, &bytes);
    alive(cx, s);
    for (uint64_t k = 0; k < n; k++) memcpy(bytes + k * s->len, s->bytes, s->len);
    return rt_string(repeated);
}

// The length of an undef is undef, in perl and here (D48).
rt_value rt_length(rt_ctx *cx, rt_value a) {
    if (a.tag == RT_TAG_UNDEF) return a;
    scratch x;
    return rt_int((int64_t)to_str(cx, a, &x)->chars);
}

// `uc` and `lc` change the ASCII letters. Past ASCII perl has tables,
// under which a string can change length (T45); until they come, a
// character past ASCII is a fault.
static rt_value change_case(rt_ctx *cx, rt_value a, char from, char to, const char *fault) {
    scratch x;
    const rt_str *s = to_str(cx, a, &x);
    if (s->len != s->chars) rt_fault(cx, fault);
    char *bytes;
    const rt_str *changed = str_new(cx, s->len, s->chars, &bytes);
    alive(cx, s);
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
    scratch x;
    const rt_str *s = to_str(cx, a, &x);
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
    if (v.split) rt_fault(cx, SPLIT);
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
    scratch x;
    const rt_str *s = to_str(cx, a, &x);
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
    alive(cx, s);
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
static rt_value find(const rt_str *s, const rt_str *t, int64_t position) {
    if (position < 0) position = 0;
    if (position > (int64_t)s->chars) position = (int64_t)s->chars;
    for (uint64_t at = offset_of(s, (uint64_t)position); at + t->len <= s->len; at++) {
        if (memcmp(s->bytes + at, t->bytes, t->len) == 0) return rt_int((int64_t)chars_in(s, at));
    }
    return rt_int(-1);
}

rt_value rt_index2(rt_ctx *cx, rt_value a, rt_value b) {
    scratch x, y;
    const rt_str *s = to_str(cx, a, &x);
    const rt_str *t = to_str(cx, b, &y);
    return find(s, t, 0);
}

rt_value rt_index3(rt_ctx *cx, rt_value a, rt_value b, rt_value position) {
    // The two strings are read before the position is a number, as the
    // arguments are written.
    scratch x, y;
    const rt_str *s = to_str(cx, a, &x);
    const rt_str *t = to_str(cx, b, &y);
    return find(s, t, whole_number(cx, numeric(cx, position)));
}

// ---- truth and comparison

// perl's truth (D49). A string is false when it is empty or the one
// character `0`: `0.0` and `00` are true, which a number that is zero
// never prints as.
int rt_is_true(rt_ctx *cx, rt_value v) {
    switch (v.tag) {
    case RT_TAG_UNDEF: return 0;
    case RT_TAG_BOOL: return v.as.i != 0;
    case RT_TAG_INT: return v.as.i != 0;
    case RT_TAG_NUM: return v.as.n != 0.0;
    case RT_TAG_STR: {
        const rt_str *s = alive(cx, v.as.s);
        return !(s->len == 0 || (s->len == 1 && s->bytes[0] == '0'));
    }
    default: rt_fault(cx, "not a value");
    }
}

int rt_is_false(rt_ctx *cx, rt_value v) {
    return !rt_is_true(cx, v);
}

int rt_is_undef(rt_ctx *cx, rt_value v) {
    if (v.tag < RT_TAG_INT || v.tag > RT_TAG_BOOL) rt_fault(cx, "not a value");
    return v.tag == RT_TAG_UNDEF;
}

rt_value rt_not(rt_ctx *cx, rt_value a) {
    return rt_bool(!rt_is_true(cx, a));
}

rt_value rt_xor(rt_ctx *cx, rt_value a, rt_value b) {
    int left = rt_is_true(cx, a);
    int right = rt_is_true(cx, b);
    return rt_bool(left != right);
}

rt_value rt_defined(rt_ctx *cx, rt_value a) {
    return rt_bool(!rt_is_undef(cx, a));
}

// Two operands as numbers: -1, 0 or 1. D35's question again: whole
// numbers when both are integral, doubles otherwise, an Int going to the
// nearest double, so that 9007199254740993 == 2 ** 53 (T39). perl has no
// second answer here for any past of either operand, D40's faults aside:
// docs/briefs/step4-comparisons.py. No operand is a NaN (D37).
static int compare_numbers(rt_ctx *cx, rt_value a, rt_value b) {
    number x = numeric(cx, a);
    number y = numeric(cx, b);
    int64_t p, q;
    if (integral(x, &p) && integral(y, &q)) return (p > q) - (p < q);
    double f = as_double(x);
    double g = as_double(y);
    return (f > g) - (f < g);
}

// Two operands as strings: -1, 0 or 1. Bytes are compared, which is the
// order of the characters: UTF-8 keeps it.
static int compare_strings(rt_ctx *cx, rt_value a, rt_value b) {
    scratch x, y;
    const rt_str *s = to_str(cx, a, &x);
    const rt_str *t = to_str(cx, b, &y);
    int c = memcmp(s->bytes, t->bytes, s->len < t->len ? s->len : t->len);
    if (c != 0) return (c > 0) - (c < 0);
    return (s->len > t->len) - (s->len < t->len);
}

#define COMPARISON(name, compare, test) \
    rt_value name(rt_ctx *cx, rt_value a, rt_value b) { \
        int c = compare(cx, a, b); \
        return rt_bool(c test 0); \
    }
COMPARISON(rt_num_eq, compare_numbers, ==)
COMPARISON(rt_num_ne, compare_numbers, !=)
COMPARISON(rt_num_lt, compare_numbers, <)
COMPARISON(rt_num_gt, compare_numbers, >)
COMPARISON(rt_num_le, compare_numbers, <=)
COMPARISON(rt_num_ge, compare_numbers, >=)
COMPARISON(rt_str_eq, compare_strings, ==)
COMPARISON(rt_str_ne, compare_strings, !=)
COMPARISON(rt_str_lt, compare_strings, <)
COMPARISON(rt_str_gt, compare_strings, >)
COMPARISON(rt_str_le, compare_strings, <=)
COMPARISON(rt_str_ge, compare_strings, >=)

rt_value rt_num_cmp(rt_ctx *cx, rt_value a, rt_value b) {
    return rt_int(compare_numbers(cx, a, b));
}

rt_value rt_str_cmp(rt_ctx *cx, rt_value a, rt_value b) {
    return rt_int(compare_strings(cx, a, b));
}

// ---- arrays and lists (D76, D80)

// The most values an array may hold: as a string's characters are.
#define ARRAY_MAX ((uint64_t)INT32_MAX)

// An array that is being used. One that was collected is a root the
// collector was not shown.
static rt_array *array_of(rt_ctx *cx, rt_value v) {
    if (v.tag != RT_TAG_ARRAY) rt_fault(cx, "not an array");
    if (v.as.a->dead) rt_internal(cx, "an array was used after it was collected");
    return v.as.a;
}

// An array about to be stored to or to change its size: a fault while a
// `foreach` is over it (D17, D80).
static rt_array *changing(rt_ctx *cx, rt_value v) {
    rt_array *a = array_of(cx, v);
    if (a->frozen != 0) rt_fault(cx, "an array was changed while a foreach is over it");
    return a;
}

// (A hash is frozen as an array is: step 12b's loops will ask.)
static rt_array *container_of(rt_ctx *cx, rt_value v) {
    if (v.tag == RT_TAG_HASH && !v.as.a->dead) return v.as.a;
    return array_of(cx, v);
}

void rt_freeze(rt_ctx *cx, rt_value array) {
    rt_array *a = container_of(cx, array);
    unwind_frozen(cx, a);
    a->frozen += 1;
}

void rt_thaw(rt_ctx *cx, rt_value array) {
    rt_array *a = container_of(cx, array);
    if (a->frozen == 0) rt_internal(cx, "an array that no foreach is over was given back");
    unwind_thawed(cx, a);
    a->frozen -= 1;
}

// A value an array may hold: one of the five kinds, and no array.
static rt_value scalar(rt_ctx *cx, rt_value v) {
    if (v.tag < RT_TAG_INT || v.tag > RT_TAG_BOOL) rt_fault(cx, "not a value");
    return v;
}

rt_value rt_array_new(rt_ctx *cx) {
    rt_block *block = block_new(cx, sizeof(rt_block) + sizeof(rt_array));
    block->marked = IS_ARRAY;
    rt_array *a = (rt_array *)(block + 1);
    a->count = a->room = a->slots = a->gone = 0;
    a->items = NULL;
    a->index = NULL;
    a->dead = 0;
    a->frozen = 0;
    rt_value v;
    v.tag = RT_TAG_ARRAY;
    v.as.a = a;
    return v;
}

// Room for `count` values in all. The storage is counted against the cap,
// and no collection is started for it: whoever is adding holds values the
// collector may not have been shown.
static void reserve(rt_ctx *cx, rt_array *a, uint64_t count) {
    if (count <= a->room) return;
    if (count > ARRAY_MAX) rt_fault(cx, "array too long");
    uint64_t room = a->room < 8 ? 8 : a->room * 2;
    if (room < count) room = count;
    uint64_t more = (room - a->room) * sizeof(rt_value);
    if (cx->cap != 0 && (more > cx->cap || cx->held > cx->cap - more)) rt_fault(cx, "out of memory");
    rt_value *items = realloc(a->items, room * sizeof(rt_value));
    if (items == NULL) rt_fault(cx, "out of memory");
    a->items = items;
    a->room = room;
    cx->held += more;
    cx->since += more;
    ((rt_block *)a - 1)->size += more;
}

// Values moved within an array's storage. An array that has never held a
// value has no storage, and C leaves arithmetic on a null pointer
// undefined, by a count of nothing too.
static void shift_values(rt_array *a, uint64_t to, uint64_t from, uint64_t count) {
    if (count != 0) memmove(a->items + to, a->items + from, count * sizeof(rt_value));
}

static void append(rt_ctx *cx, rt_array *a, rt_value v) {
    reserve(cx, a, a->count + 1);
    a->items[a->count++] = v;
}

void rt_list_add(rt_ctx *cx, rt_value list, rt_value v) {
    if (v.tag == RT_TAG_ABSENT) return;
    // What a call gave where a list was wanted: every value of it (D18).
    if (v.tag == RT_TAG_ARRAY) {
        rt_list_add_all(cx, list, v);
        return;
    }
    append(cx, array_of(cx, list), scalar(cx, v));
}

void rt_list_add_all(rt_ctx *cx, rt_value list, rt_value array) {
    rt_array *to = array_of(cx, list);
    rt_array *from = array_of(cx, array);
    // `push @a, @a`: the count before, since the values move as it grows.
    uint64_t count = from->count;
    reserve(cx, to, to->count + count);
    for (uint64_t n = 0; n < count; n++) to->items[to->count++] = from->items[n];
}

// A whole number, by the rule `substr` has for a position: for an index,
// an offset, a length, an end of a range.
static int64_t whole_of(rt_ctx *cx, rt_value v) {
    number x = numeric(cx, v);
    int64_t t = whole_number(cx, x);
    if (x.split) rt_fault(cx, SPLIT);
    return t;
}

void rt_list_add_range(rt_ctx *cx, rt_value list, rt_value from, rt_value to) {
    rt_array *a = array_of(cx, list);
    // perl's range of strings is another thing (T154).
    if (from.tag == RT_TAG_STR) rt_fault(cx, "a string as the end of a range");
    int64_t lo = whole_of(cx, from);
    if (to.tag == RT_TAG_STR) rt_fault(cx, "a string as the end of a range");
    int64_t hi = whole_of(cx, to);
    if (lo > hi) return;
    uint64_t count = (uint64_t)hi - (uint64_t)lo + 1;
    if (count == 0 || count > ARRAY_MAX || a->count + count > ARRAY_MAX) rt_fault(cx, "array too long");
    reserve(cx, a, a->count + count);
    for (uint64_t n = 0; n < count; n++) a->items[a->count++] = rt_int((int64_t)((uint64_t)lo + n));
}

// Where index `i` is in an array of `count`, from the start; or -1 for
// past either end.
static int64_t place(uint64_t count, int64_t i) {
    if (i >= 0) return (uint64_t)i < count ? i : -1;
    // -count <= i, without negating the smallest integer
    return (uint64_t)(-(i + 1)) < count ? (int64_t)(count - (uint64_t)(-(i + 1)) - 1) : -1;
}

void rt_list_add_slice(rt_ctx *cx, rt_value list, rt_value from, rt_value indexes, int how) {
    rt_array *to = array_of(cx, list);
    rt_array *a = array_of(cx, from);
    rt_array *ix = array_of(cx, indexes);
    // Every index is looked at, for its fault, though a list with no
    // values gives none back.
    for (uint64_t n = 0; n < ix->count; n++) {
        int64_t at = place(a->count, whole_of(cx, ix->items[n]));
        if (how == 1 && a->count == 0) continue;
        if (how == 2 && at < 0) rt_fault(cx, "a slice past the end of the array, where perl would make the elements");
        append(cx, to, at < 0 ? rt_undef() : a->items[at]);
    }
}

// `@a[INDEXES] = LIST`: a value for each index in turn, and an undef for
// each the list does not reach, which grows the array all the same (T228).
void rt_slice_store(rt_ctx *cx, rt_value array, rt_value indexes, rt_value list) {
    rt_array *ix = array_of(cx, indexes);
    rt_array *from = array_of(cx, list);
    for (uint64_t n = 0; n < ix->count; n++) {
        rt_elem_store(cx, array, ix->items[n], n < from->count ? from->items[n] : rt_undef());
    }
}

void rt_list_add_repeat(rt_ctx *cx, rt_value list, rt_value values, rt_value count) {
    rt_array *to = array_of(cx, list);
    rt_array *from = array_of(cx, values);
    number c = numeric(cx, count);
    if (below_zero(c)) rt_fault(cx, "negative repeat count");
    uint64_t times = (uint64_t)whole_number(cx, c);
    if (c.split) rt_fault(cx, SPLIT);
    if (from->count == 0) return;
    if (times > ARRAY_MAX / from->count || to->count + times * from->count > ARRAY_MAX) rt_fault(cx, "array too long");
    reserve(cx, to, to->count + times * from->count);
    for (uint64_t t = 0; t < times; t++) {
        for (uint64_t n = 0; n < from->count; n++) to->items[to->count++] = from->items[n];
    }
}

void rt_array_assign(rt_ctx *cx, rt_value array, rt_value list) {
    rt_array *a = changing(cx, array);
    rt_array *from = array_of(cx, list);
    if (a == from) return;
    reserve(cx, a, from->count);
    for (uint64_t n = 0; n < from->count; n++) a->items[n] = from->items[n];
    a->count = from->count;
}

rt_value rt_list_item(rt_ctx *cx, rt_value list, int64_t n) {
    rt_array *a = array_of(cx, list);
    return (uint64_t)n < a->count ? a->items[n] : rt_undef();
}

void rt_array_rest(rt_ctx *cx, rt_value array, rt_value list, int64_t n) {
    rt_array *a = changing(cx, array);
    rt_array *from = array_of(cx, list);
    uint64_t count = (uint64_t)n < from->count ? from->count - (uint64_t)n : 0;
    reserve(cx, a, count);
    for (uint64_t k = 0; k < count; k++) a->items[k] = from->items[(uint64_t)n + k];
    a->count = count;
}

int64_t rt_list_length(rt_ctx *cx, rt_value list) {
    return (int64_t)array_of(cx, list)->count;
}

rt_value rt_elem_strict(rt_ctx *cx, rt_value array, rt_value index) {
    int64_t i = whole_of(cx, index);
    rt_array *a = array_of(cx, array);
    int64_t at = place(a->count, i);
    if (at < 0) rt_fault(cx, "an element past the end of the array in a foreach, where perl would make it");
    return a->items[at];
}

int rt_range_ends(rt_ctx *cx, rt_value from, rt_value to, int64_t *lo, int64_t *hi) {
    if (from.tag == RT_TAG_STR) rt_fault(cx, "a string as the end of a range");
    *lo = whole_of(cx, from);
    if (to.tag == RT_TAG_STR) rt_fault(cx, "a string as the end of a range");
    *hi = whole_of(cx, to);
    // perl counts such a loop in a way that can't hold these (T166).
    if (*lo < INT64_MIN + 513 || *hi < INT64_MIN + 513) {
        rt_fault(cx, "a foreach over a range that begins or ends this near the smallest integer: perl refuses it");
    }
    return *lo <= *hi;
}

rt_value rt_count(rt_ctx *cx, rt_value array) {
    return rt_int((int64_t)array_of(cx, array)->count);
}

rt_value rt_last_index(rt_ctx *cx, rt_value array) {
    return rt_int((int64_t)array_of(cx, array)->count - 1);
}

rt_value rt_first(rt_ctx *cx, rt_value list) {
    rt_array *a = array_of(cx, list);
    return a->count == 0 ? rt_undef() : a->items[0];
}

rt_value rt_elem(rt_ctx *cx, rt_value array, rt_value index) {
    int64_t i = whole_of(cx, index);
    rt_array *a = array_of(cx, array);
    int64_t at = place(a->count, i);
    return at < 0 ? rt_undef() : a->items[at];
}

int64_t rt_elem_make(rt_ctx *cx, rt_value array, rt_value index) {
    int64_t i = whole_of(cx, index);
    rt_array *a = array_of(cx, array);
    if (i < 0) {
        int64_t at = place(a->count, i);
        if (at < 0) rt_fault(cx, "an element before the start of the array");
        changing(cx, array);
        return at;
    }
    changing(cx, array);
    if ((uint64_t)i >= ARRAY_MAX) rt_fault(cx, "array too long");
    if ((uint64_t)i >= a->count) {
        reserve(cx, a, (uint64_t)i + 1);
        while (a->count <= (uint64_t)i) a->items[a->count++] = rt_undef();
    }
    return i;
}

rt_value rt_elem_get(rt_ctx *cx, rt_value array, int64_t at) {
    rt_array *a = array_of(cx, array);
    if (at < 0 || (uint64_t)at >= a->count) rt_internal(cx, "an element that was made is not there");
    return a->items[at];
}

rt_value rt_elem_put(rt_ctx *cx, rt_value array, int64_t at, rt_value v) {
    rt_array *a = array_of(cx, array);
    if (at < 0 || (uint64_t)at >= a->count) rt_internal(cx, "an element that was made is not there");
    a->items[at] = scalar(cx, v);
    return v;
}

rt_value rt_elem_store(rt_ctx *cx, rt_value array, rt_value index, rt_value v) {
    return rt_elem_put(cx, array, rt_elem_make(cx, array, index), v);
}

rt_value rt_push(rt_ctx *cx, rt_value array, rt_value list) {
    changing(cx, array);
    rt_list_add_all(cx, array, list);
    return rt_count(cx, array);
}

rt_value rt_unshift(rt_ctx *cx, rt_value array, rt_value list) {
    rt_array *a = changing(cx, array);
    rt_array *from = array_of(cx, list);
    uint64_t more = from->count;
    reserve(cx, a, a->count + more);
    shift_values(a, more, 0, a->count);
    for (uint64_t n = 0; n < more; n++) a->items[n] = from->items[n];
    a->count += more;
    return rt_count(cx, array);
}

rt_value rt_pop(rt_ctx *cx, rt_value array) {
    rt_array *a = changing(cx, array);
    return a->count == 0 ? rt_undef() : a->items[--a->count];
}

rt_value rt_shift(rt_ctx *cx, rt_value array) {
    rt_array *a = changing(cx, array);
    if (a->count == 0) return rt_undef();
    rt_value first = a->items[0];
    a->count -= 1;
    shift_values(a, 0, 1, a->count);
    return first;
}

void rt_splice(rt_ctx *cx, rt_value removed, rt_value array, int given, rt_value offset, rt_value length, rt_value put) {
    // Both numbers before anything moves: each has its fault.
    int64_t o = given > 0 ? whole_of(cx, offset) : 0;
    int64_t l = given > 1 ? whole_of(cx, length) : 0;
    rt_array *a = array_of(cx, array);
    rt_array *out = array_of(cx, removed);
    rt_array *in = array_of(cx, put);
    uint64_t count = a->count;
    uint64_t start;
    if (o < 0) {
        if ((uint64_t)(-(o + 1)) >= count) rt_fault(cx, "splice before the start of the array");
        start = count - (uint64_t)(-(o + 1)) - 1;
    } else {
        if ((uint64_t)o > count) rt_fault(cx, "splice past the end of the array");
        start = (uint64_t)o;
    }
    uint64_t end = count;
    if (given > 1 && l >= 0) {
        end = (uint64_t)l < count - start ? start + (uint64_t)l : count;
    } else if (given > 1) {
        // That many are left at the end; none are removed if that is
        // before where it starts.
        uint64_t left = (uint64_t)(-(l + 1)) + 1;
        end = left < count - start ? count - left : start;
    }
    uint64_t gone = end - start;
    uint64_t came = in->count;
    changing(cx, array);
    for (uint64_t n = start; n < end; n++) append(cx, out, a->items[n]);
    // `in` may be the array's own values in a list of their own, never
    // the array: a list is a copy (D76).
    reserve(cx, a, count - gone + came);
    shift_values(a, start + came, end, count - end);
    for (uint64_t n = 0; n < came; n++) a->items[start + n] = in->items[n];
    a->count = count - gone + came;
}

static void emit_list(rt_ctx *cx, rt_value list, int newline) {
    rt_array *a = array_of(cx, list);
    for (uint64_t n = 0; n < a->count; n++) emit_checked(cx, a->items[n], 0, 0);
    for (uint64_t n = 0; n < a->count; n++) emit_checked(cx, a->items[n], 0, 1);
    if (newline) putc('\n', stdout);
}

void rt_say_list(rt_ctx *cx, rt_value list) {
    emit_list(cx, list, 1);
}

void rt_print_list(rt_ctx *cx, rt_value list) {
    emit_list(cx, list, 0);
}

rt_value rt_only(rt_ctx *cx, rt_value list) {
    rt_array *a = array_of(cx, list);
    if (a->count > 1) rt_internal(cx, "a sub that gives no list gave one");
    return a->count == 0 ? rt_absent() : a->items[0];
}

rt_value *rt_list_items(rt_ctx *cx, rt_value list) {
    return array_of(cx, list)->items;
}

void rt_slurp(rt_ctx *cx, rt_value array, int64_t argc, rt_value **argv, rt_value *flat, int64_t from) {
    rt_array *a = array_of(cx, array);
    for (int64_t n = from; n < argc; n++) append(cx, a, scalar(cx, flat != NULL ? flat[n] : *argv[n]));
}

void rt_list_add_reversed(rt_ctx *cx, rt_value list, rt_value values) {
    rt_array *to = array_of(cx, list);
    rt_array *from = array_of(cx, values);
    reserve(cx, to, to->count + from->count);
    for (uint64_t n = from->count; n > 0; n--) to->items[to->count++] = from->items[n - 1];
}

// Every value is looked at twice: once for its faults and its size, and
// once, after the one allocation, to be copied. A number is a scratch
// string each time.
rt_value rt_join(rt_ctx *cx, rt_value separator, rt_value list) {
    rt_array *a = array_of(cx, list);
    scratch x, y;
    const rt_str *sep = to_str(cx, separator, &x);
    uint64_t len = 0, chars = 0;
    for (uint64_t n = 0; n < a->count; n++) {
        const rt_str *s = to_str(cx, a->items[n], &y);
        len += s->len + (n > 0 ? sep->len : 0);
        chars += s->chars + (n > 0 ? sep->chars : 0);
        if (chars > (uint64_t)INT32_MAX) rt_fault(cx, "joined string too long");
    }
    char *bytes;
    const rt_str *joined = str_new(cx, len, chars, &bytes);
    alive(cx, sep);
    for (uint64_t n = 0; n < a->count; n++) {
        if (n > 0) {
            memcpy(bytes, sep->bytes, sep->len);
            bytes += sep->len;
        }
        const rt_str *s = to_str(cx, a->items[n], &y);
        alive(cx, s);
        memcpy(bytes, s->bytes, s->len);
        bytes += s->len;
    }
    return rt_string(joined);
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

// perl says `expected 2`, or `at least` the required ones when too few
// came and some are optional, or `at most` all of them when too many.
void rt_fault_arguments(rt_ctx *cx, const char *name, int64_t got, int64_t least, int64_t most) {
    char what[512];
    int few = got < least;
    snprintf(what, sizeof what, "too %s arguments for %.300s: got %" PRId64 ", expected %s%" PRId64, few ? "few" : "many", name, got,
             least == most ? "" : few ? "at least " : "at most ", few ? least : most);
    rt_fault(cx, what);
}

// An odd number of arguments left for a last parameter that is a hash:
// perl dies as the sub is entered (T226).
void rt_fault_odd_arguments(rt_ctx *cx, const char *name) {
    char what[512];
    snprintf(what, sizeof what, "an odd number of arguments for %.300s's hash", name);
    rt_fault(cx, what);
}

void rt_fault_sub(rt_ctx *cx, const char *name, const char *what) {
    char both[512];
    snprintf(both, sizeof both, "%.300s %s", name, what);
    rt_fault(cx, both);
}

void rt_internal(rt_ctx *cx, const char *what) {
    fflush(stdout);
    fprintf(stderr, "internal: %s at %s line %" PRId64 ".\n", what, cx->file, cx->line);
    release(cx);
    exit(2);
}

// perl's merge sort, ported: a file of its own, for its origin (D82).
#include "sort.c"
#include "hash.c"
#include "unwind.c"
