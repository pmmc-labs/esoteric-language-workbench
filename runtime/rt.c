// The core: the context, printing, faults. A compiled program prints to
// stdout and exits 0; a fault goes to stderr and exits 1.
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

int rt_run(void (*body)(rt_ctx *cx), const char *file) {
    rt_ctx cx = { .file = file, .line = 0 };
    body(&cx);
    return 0;
}

// Every operator checks its operand's tag, this one too: until types give
// the compiler a reason (step 26), the runtime trusts nothing it is handed.
void rt_say(rt_ctx *cx, rt_value v) {
    switch (v.tag) {
    case RT_TAG_INT:
        printf("%" PRId64 "\n", v.as.i);
        return;
    default:
        rt_fault(cx, "not a value");
    }
}

// stdout is flushed first, so that what the program printed before the
// fault comes before the fault's line wherever the two streams meet: the
// start of perl's output, then the stop (D12).
void rt_fault(rt_ctx *cx, const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s at %s line %" PRId64 ".\n", what, cx->file, cx->line);
    exit(1);
}
