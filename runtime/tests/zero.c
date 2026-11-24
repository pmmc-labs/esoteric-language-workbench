// The sign of a zero, which `say` doesn't show (it prints 0 for both) and
// no program can see until `atan2` and `sprintf` come (T79). Negating a
// Num zero gives a negative zero, as perl's negation of a float does; a
// whole-number operation gives the Int 0, which has no sign.
#include <math.h>
#include <stdio.h>
#include "rt.h"

static void show(const char *what, rt_value v) {
    printf("%s: %s\n", what, v.tag == RT_TAG_INT ? "Int" : signbit(v.as.n) ? "negative Num" : "Num");
}

static void body(rt_ctx *cx) {
    rt_value zero = rt_num(0.0);
    show("-(0.0)", rt_neg(cx, zero));
    show("-(-(0.0))", rt_neg(cx, rt_neg(cx, zero)));
    show("0 * -1.5", rt_mul(cx, rt_int(0), rt_num(-1.5)));
    show("0.0 * -1", rt_mul(cx, zero, rt_int(-1)));
    show("0 / -5", rt_div(cx, rt_int(0), rt_int(-5)));
    show("-(0.0) + 0", rt_add(cx, rt_neg(cx, zero), rt_int(0)));
    show("-(0)", rt_neg(cx, rt_int(0)));
    rt_say(cx, rt_neg(cx, zero));
}

int main(void) {
    return rt_run(body, "zero.pl");
}
