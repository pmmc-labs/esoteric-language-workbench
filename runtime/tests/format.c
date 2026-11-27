// The longest string `sprintf` may make is 2^31 - 1 characters, as for
// `x` (limit.c). No program can test the edge, since perl would make the
// string (D46), so it is tested from here: the format is counted before
// anything is made, and one character past is the fault.
#include "rt.h"

static const rt_str fmt = { 5, 5, "%*s%s" };
static const rt_str a = { 1, 1, "a" };

static void format(rt_ctx *cx, rt_value *slot, int64_t width) {
    *slot = rt_array_new(cx);
    rt_list_add(cx, *slot, rt_string(&fmt));
    rt_list_add(cx, *slot, rt_int(width));
    rt_list_add(cx, *slot, rt_string(&a));
    rt_list_add(cx, *slot, rt_string(&a));
    rt_say(cx, rt_length(cx, rt_sprintf(cx, *slot)));
}

static void body(rt_ctx *cx) {
    rt_frame frame;
    rt_value slots[1] = { { 0 } };
    rt_enter(cx, &frame, slots, 1);
    cx->line = 5;
    format(cx, &slots[0], 10);
    cx->line = 6;
    format(cx, &slots[0], 2147483647);
    rt_leave(cx, &frame);
}

int main(void) {
    return rt_run(body, "format.pl");
}
