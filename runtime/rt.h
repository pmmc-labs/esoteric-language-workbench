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
enum { RT_TAG_INT = 1 };
typedef struct {
    uint64_t tag;
    union { int64_t i; } as;
} rt_value;

static inline rt_value rt_int(int64_t n) {
    rt_value v;
    v.tag = RT_TAG_INT;
    v.as.i = n;
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

// A fault (D13): stdout as far as it got, then
// `fault: WHAT at FILE line N.` on stderr, and exit 1. Never returns, and
// nothing can catch it.
void rt_fault(rt_ctx *cx, const char *what) __attribute__((noreturn));
#endif
