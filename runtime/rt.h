// Shared between the runtime and generated code. Every name is prefixed
// rt_/RT_: macOS's <stdlib.h> pulls in <sys/wait.h>, which has a P_PID,
// and its <sys/types.h> defines major() and minor() as macros.
#ifndef RT_H
#define RT_H
#include <stdint.h>

// A value is two words, a tag and a payload (D25), so that a 64-bit
// integer fits whole; both C compilers pass the pair in registers. The
// union gains a member per kind of value. No tag is 0: memory that was
// never made a value then faults at the first operator that checks it.
enum { RT_TAG_INT = 1, RT_TAG_NUM = 2, RT_TAG_STR = 3 };

// A Str (D24): Unicode characters, held as UTF-8, and never changed once
// made. `len` is its bytes and `chars` its characters, which are the same
// number when every character is ASCII. The byte after the last is a NUL,
// which is not part of the string; a string may hold NULs of its own.
typedef struct rt_str {
    uint64_t len;
    uint64_t chars;
    const char *bytes;
} rt_str;

typedef struct {
    uint64_t tag;
    union { int64_t i; double n; uint64_t bits; const rt_str *s; } as;
} rt_value;

static inline rt_value rt_int(int64_t n) {
    rt_value v;
    v.tag = RT_TAG_INT;
    v.as.i = n;
    return v;
}

// A Num (D23): a double, and always a finite one (D37); the operators see
// to that, and a literal that isn't was refused. The compiler hands a
// literal over as its bits.
static inline rt_value rt_num(double x) {
    rt_value v;
    v.tag = RT_TAG_NUM;
    v.as.n = x;
    return v;
}

static inline rt_value rt_num_bits(uint64_t bits) {
    rt_value v;
    v.tag = RT_TAG_NUM;
    v.as.bits = bits;
    return v;
}

// A string literal is a constant in the generated C, and this is its
// value.
static inline rt_value rt_string(const rt_str *s) {
    rt_value v;
    v.tag = RT_TAG_STR;
    v.as.s = s;
    return v;
}

// The context (D28): everything the runtime knows that isn't a value,
// passed first to every runtime function and every compiled sub, so that
// nothing is global and a second context can one day run beside this one.
typedef struct rt_ctx {
    const char *file;       // the program's path, as the compiler was given it
    int64_t line;           // the line of the statement that is running
    int out_utf8;           // `use open ':std', ':encoding(UTF-8)';` was said (D39)
    struct rt_block *heap;  // every string made so far: nothing is freed until
                            // the program ends, or the collector comes (step 7)
} rt_ctx;

// Run a compiled program: make its context, call its body, return the
// status main should. The generated C's main is this and nothing else.
int rt_run(void (*body)(rt_ctx *cx), const char *file);

// `use open ':std', ':encoding(UTF-8)';` (D39): from here a character
// past ASCII may be printed.
void rt_use_open(rt_ctx *cx);

// `say`: the value as a string, and a newline; `print`: without one. The
// bytes are UTF-8. Faults: a character past ASCII without `use open`
// (perl would print another byte, or warn), and a noncharacter (D42).
void rt_say(rt_ctx *cx, rt_value v);
void rt_print(rt_ctx *cx, rt_value v);

// Arithmetic (D23, D35). Each is done on whole numbers when both operands
// are integral (an Int, or a whole Num below 2^53) and on doubles
// otherwise, as perl does it; rt.c has the rule for each. The faults:
// `integer overflow`, `float overflow`, `not a number`, `division by
// zero`, `modulus by zero`, `modulus of a number outside the integers`;
// and where perl has two answers by what was done with a value before
// (D40, D45).
rt_value rt_add(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_sub(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_mul(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_div(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_mod(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_pow(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_neg(rt_ctx *cx, rt_value a);

// Strings (D24, D40 to D44). An operand that is a number is made a
// string as `say` prints it, and one that is a string is made a number by
// D40's rule where a number is wanted; rt.c has both. `x` takes a count,
// `substr` and `index` positions, cut toward zero. A character is a
// Unicode scalar value, and positions count characters.
rt_value rt_concat(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_repeat(rt_ctx *cx, rt_value a, rt_value count);
rt_value rt_length(rt_ctx *cx, rt_value a);
rt_value rt_uc(rt_ctx *cx, rt_value a);
rt_value rt_lc(rt_ctx *cx, rt_value a);
rt_value rt_ord(rt_ctx *cx, rt_value a);
rt_value rt_chr(rt_ctx *cx, rt_value a);
rt_value rt_substr2(rt_ctx *cx, rt_value a, rt_value offset);
rt_value rt_substr3(rt_ctx *cx, rt_value a, rt_value offset, rt_value count);
rt_value rt_index2(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_index3(rt_ctx *cx, rt_value a, rt_value b, rt_value position);

// A fault (D13): stdout as far as it got, then
// `fault: WHAT at FILE line N.` on stderr, and exit 1. Never returns, and
// nothing can catch it.
void rt_fault(rt_ctx *cx, const char *what) __attribute__((noreturn));
#endif
