// The limit on recursion (D68), driven by hand: what a frame counts for,
// that closing one gives it back, and the fault when the next would pass
// the limit. `rt_enter` is called on frames that all share one array of
// slots: nothing here reads a slot, and the C stack is not what is being
// counted.
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

static rt_value slots[40];
static rt_frame frames[5000];
static long want;

static void body(rt_ctx *cx) {
    // An empty frame is RT_CALL_BYTES, and each slot 16 more.
    rt_enter(cx, &frames[0], slots, 0);
    printf("one frame of no slots: %" PRIu64 "\n", cx->deep);
    rt_enter(cx, &frames[1], slots, 40);
    printf("and one of forty: %" PRIu64 "\n", cx->deep);
    rt_leave(cx, &frames[1]);
    rt_leave(cx, &frames[0]);
    printf("both closed: %" PRIu64 "\n", cx->deep);
    // 4 MB is 4,096 frames of no slots, and not one more.
    cx->line = 7;
    for (long k = 0; k < want; k++) rt_enter(cx, &frames[k], slots, 0);
    printf("%ld open: %" PRIu64 "\n", want, cx->deep);
    for (long k = want - 1; k >= 0; k--) rt_leave(cx, &frames[k]);
    printf("closed: %" PRIu64 "\n", cx->deep);
}

int main(int argc, char **argv) {
    want = argc > 1 ? atol(argv[1]) : 0;
    return rt_run(body, "deep.pl");
}
