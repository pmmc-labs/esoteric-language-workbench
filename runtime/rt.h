// Shared between the runtime and generated code. Every name is prefixed
// rt_/RT_: macOS's <stdlib.h> pulls in <sys/wait.h>, which has a P_PID,
// and its <sys/types.h> defines major() and minor() as macros.
#ifndef RT_H
#define RT_H
#include <stdint.h>

// A value: a 63-bit integer, shifted left one bit, tag 0 (D4). An
// immediate whose low two bits are 11 is a boolean, its value in bit 2
// (D14); 01 is left for what comes next.
typedef intptr_t rt_value;
#define RT_INT_TAG 0
#define RT_INT_SHIFT 1
#define RT_INT_MIN (-(INT64_C(1) << 62))
#define RT_INT_MAX ((INT64_C(1) << 62) - 1)
#define RT_IMM_TAG 3
#define RT_TRUE ((rt_value)7)
#define RT_FALSE ((rt_value)3)

// Multiplied, not shifted: a left shift of a negative value is undefined
// before C23, and UBSan says so; the compiler emits the shift anyway.
static inline rt_value rt_int(int64_t n) { return (rt_value)(n * (1 << RT_INT_SHIFT)) | RT_INT_TAG; }
static inline int64_t rt_int_of(rt_value v) { return (int64_t)v >> RT_INT_SHIFT; }
static inline int rt_is_int(rt_value v) { return (v & 1) == RT_INT_TAG; }
static inline rt_value rt_bool(int b) { return b ? RT_TRUE : RT_FALSE; }

rt_value lang_main(void);
rt_value rt_add(rt_value a, rt_value b);
rt_value rt_sub(rt_value a, rt_value b);
rt_value rt_mul(rt_value a, rt_value b);
rt_value rt_div(rt_value a, rt_value b);
rt_value rt_mod(rt_value a, rt_value b);
rt_value rt_band(rt_value a, rt_value b);
rt_value rt_bor(rt_value a, rt_value b);
rt_value rt_bxor(rt_value a, rt_value b);
rt_value rt_shl(rt_value a, rt_value b);
rt_value rt_shr(rt_value a, rt_value b);
rt_value rt_lt(rt_value a, rt_value b);
rt_value rt_le(rt_value a, rt_value b);
rt_value rt_gt(rt_value a, rt_value b);
rt_value rt_ge(rt_value a, rt_value b);
rt_value rt_eq(rt_value a, rt_value b);
rt_value rt_ne(rt_value a, rt_value b);
int rt_test(rt_value v);
void rt_print(rt_value v);
void rt_fault(const char *what) __attribute__((noreturn));
#endif
