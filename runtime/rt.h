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
enum { RT_TAG_INT = 1, RT_TAG_NUM = 2 };
typedef struct {
    uint64_t tag;
    union { int64_t i; double n; uint64_t bits; } as;
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

// The context (D28): everything the runtime knows that isn't a value,
// passed first to every runtime function and every compiled sub, so that
// nothing is global and a second context can one day run beside this one.
typedef struct rt_ctx {
    const char *file;   // the program's path, as the compiler was given it
    int64_t line;       // the line of the statement that is running
} rt_ctx;

// Run a compiled program: make its context, call its body, return the
// status main should. The generated C's main is this and nothing else.
int rt_run(void (*body)(rt_ctx *cx), const char *file);

// `say`: the value as perl prints it, and a newline.
void rt_say(rt_ctx *cx, rt_value v);

// Arithmetic (D23, D35). Each is done on whole numbers when both operands
// are integral (an Int, or a whole Num below 2^53) and on doubles
// otherwise, as perl does it; rt.c has the rule for each. The faults:
// `integer overflow`, `float overflow`, `not a number`, `division by
// zero`, `modulus by zero`, `modulus of a number outside the integers`.
rt_value rt_add(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_sub(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_mul(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_div(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_mod(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_pow(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_neg(rt_ctx *cx, rt_value a);

// A fault (D13): stdout as far as it got, then
// `fault: WHAT at FILE line N.` on stderr, and exit 1. Never returns, and
// nothing can catch it.
void rt_fault(rt_ctx *cx, const char *what) __attribute__((noreturn));
#endif
