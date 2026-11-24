// Every operator checks its operands' tags before it believes them, and
// faults by name. No program can hand one anything but an Int yet, so the
// check is driven from here: the argument says which operand of which
// operator gets a value that was never made.
#include <string.h>
#include "rt.h"

static const char *which;

static void body(rt_ctx *cx) {
    rt_value never_set = { 0 };
    rt_value one = rt_int(1);
    cx->line = 3;
    rt_say(cx, rt_add(cx, one, one));
    if (strcmp(which, "add-left") == 0) rt_add(cx, never_set, one);
    if (strcmp(which, "add-right") == 0) rt_add(cx, one, never_set);
    if (strcmp(which, "sub-left") == 0) rt_sub(cx, never_set, one);
    if (strcmp(which, "sub-right") == 0) rt_sub(cx, one, never_set);
    if (strcmp(which, "mul-left") == 0) rt_mul(cx, never_set, one);
    if (strcmp(which, "mul-right") == 0) rt_mul(cx, one, never_set);
    if (strcmp(which, "mod-left") == 0) rt_mod(cx, never_set, one);
    if (strcmp(which, "mod-right") == 0) rt_mod(cx, one, never_set);
    if (strcmp(which, "div-left") == 0) rt_div(cx, never_set, one);
    if (strcmp(which, "div-right") == 0) rt_div(cx, one, never_set);
    if (strcmp(which, "pow-left") == 0) rt_pow(cx, never_set, one);
    if (strcmp(which, "pow-right") == 0) rt_pow(cx, one, never_set);
    if (strcmp(which, "neg") == 0) rt_neg(cx, never_set);
    rt_say(cx, rt_int(2));
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "tags.pl");
}
