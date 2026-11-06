// Shared between the runtime and generated code. Every name is prefixed
// rt_/RT_: macOS's <stdlib.h> pulls in <sys/wait.h>, which has a P_PID,
// and its <sys/types.h> defines major() and minor() as macros.
#ifndef RT_H
#define RT_H
#include <stdint.h>

// Step 0's value: a 63-bit integer, shifted left one bit, tag 0. Later
// steps add tags for the other immediates and for pointers.
typedef intptr_t rt_value;
#define RT_INT_TAG 0
#define RT_INT_SHIFT 1

// Multiplied, not shifted: a left shift of a negative value is undefined
// before C23, and UBSan says so; the compiler emits the shift anyway.
static inline rt_value rt_int(int64_t n) { return (rt_value)(n * (1 << RT_INT_SHIFT)) | RT_INT_TAG; }

// The range of an integer, 63 bits (D10). Written out, not computed from a
// shift, so that the compiler's copy of it and this one can be read side
// by side.
#define RT_INT_MAX ((int64_t)4611686018427387903LL)
#define RT_INT_MIN (-RT_INT_MAX - 1)

rt_value lang_main(void);
void rt_print(rt_value v);
void rt_fault(const char *what) __attribute__((noreturn));

// Arithmetic (D10, D11, D13): each decodes both operands, computes in
// int64_t, and faults, `integer overflow` or `division by zero`, rather
// than return a result outside the range.
rt_value rt_add(rt_value a, rt_value b);
rt_value rt_sub(rt_value a, rt_value b);
rt_value rt_mul(rt_value a, rt_value b);
rt_value rt_div(rt_value a, rt_value b);
rt_value rt_rem(rt_value a, rt_value b);
#endif
