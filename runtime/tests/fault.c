// The fault path (D13), driven from C, since no program can fault yet:
// what was printed comes first, then the fault's line with the file and
// the line the context holds, then exit 1, and nothing after. The file's
// name has a space and quotes in it because a path can.
#include "rt.h"

static void body(rt_ctx *cx) {
    rt_say(cx, rt_int(1));
    rt_say(cx, rt_int(INT64_MAX));
    cx->line = 7;
    rt_value never_set = { 0 };
    rt_say(cx, never_set);
    rt_say(cx, rt_int(2));
}

int main(void) {
    return rt_run(body, "some dir/a \"file\".pl");
}
