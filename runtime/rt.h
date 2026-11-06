// Shared between the runtime and generated code. Every name is prefixed
// rt_/RT_: macOS's <stdlib.h> pulls in <sys/wait.h>, which has a P_PID,
// and its <sys/types.h> defines major() and minor() as macros.
#ifndef RT_H
#define RT_H
#include <stdint.h>

// A value: a 63-bit integer, shifted left one bit, tag 0. Later steps
// add tags for the other immediates and for pointers.
typedef intptr_t rt_value;
#define RT_INT_TAG 0
#define RT_INT_SHIFT 1
#define RT_INT_MIN (-(INT64_C(1) << 62))
#define RT_INT_MAX ((INT64_C(1) << 62) - 1)

// Multiplied, not shifted: a left shift of a negative value is undefined
// before C23, and UBSan says so; the compiler emits the shift anyway.
static inline rt_value rt_int(int64_t n) { return (rt_value)(n * (1 << RT_INT_SHIFT)) | RT_INT_TAG; }
static inline int64_t rt_int_of(rt_value v) { return (int64_t)v >> RT_INT_SHIFT; }

// A boolean (D14): its own immediate, the low two bits 11, the value in
// bit 2. An integer's low bit is 0, so the two tags never collide.
#define RT_BOOL_TAG 3
#define RT_BOOL_SHIFT 2
static inline rt_value rt_bool(int b) { return (rt_value)(b << RT_BOOL_SHIFT) | RT_BOOL_TAG; }

rt_value lang_main(void);
rt_value rt_add(rt_value a, rt_value b);
rt_value rt_sub(rt_value a, rt_value b);
rt_value rt_mul(rt_value a, rt_value b);
rt_value rt_div(rt_value a, rt_value b);
rt_value rt_mod(rt_value a, rt_value b);
rt_value rt_lt(rt_value a, rt_value b);
rt_value rt_le(rt_value a, rt_value b);
rt_value rt_gt(rt_value a, rt_value b);
rt_value rt_ge(rt_value a, rt_value b);
rt_value rt_eq(rt_value a, rt_value b);
rt_value rt_ne(rt_value a, rt_value b);
// The test of an if (D13): it must be a boolean, and its value is the
// 0 or 1 C's ?: selects on, so only the taken branch is evaluated.
rt_value rt_if_test(rt_value test);
void rt_print(rt_value v);
void rt_fault(const char *what) __attribute__((noreturn));
#endif
