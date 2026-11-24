// The longest string `x` may make is 2^31 - 1 characters. No program can
// test the edge: perl works a constant `x` out as it compiles, and would
// need the memory for it (T102). So it is tested from here, one
// character past.
#include "rt.h"

static const rt_str ab = { 2, 2, "ab" };

static void body(rt_ctx *cx) {
    cx->line = 5;
    rt_say(cx, rt_length(cx, rt_repeat(cx, rt_string(&ab), rt_int(1000))));
    rt_say(cx, rt_length(cx, rt_repeat(cx, rt_string(&ab), rt_int(1073741824))));
}

int main(void) {
    return rt_run(body, "limit.pl");
}
