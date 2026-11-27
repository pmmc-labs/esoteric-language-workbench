// Unwinding (step 15; D141), driven from C as the generated code drives
// it: a `try` round frames opened inside it, freezes made, a sort under
// way; a `die` from deep inside; and after the catch, everything put back.
// The argument says which case.
#include <inttypes.h>
#include <setjmp.h>
#include <stdio.h>
#include <string.h>
#include "rt.h"

static const char *which;
static const rt_str MSG = { 3, 3, "msg", RT_STR_CONSTANT };
static const rt_str NL = { 4, 4, "msg\n", RT_STR_CONSTANT };

static int is(const char *name) {
    return strcmp(which, name) == 0;
}

// What is open: the depth the frames count for, the frames, the sorts,
// the freezes, and the arrays' own counts.
static void report(rt_ctx *cx, const char *when, rt_value a, rt_value h) {
    uint64_t frames = 0;
    for (rt_frame *f = cx->frames; f; f = f->prev) frames++;
    uint64_t sorts = 0;
    printf("%s: %" PRIu64 " frames, deep %" PRIu64 ", sorts %s, %" PRIu64 " freezes, @a %" PRIu64 ", %%h %" PRIu64 ", tries %s\n",
           when, frames, cx->deep, cx->sorts ? "some" : "none", cx->frozen_count, a.as.a->frozen, h.as.a->frozen, cx->tries ? "open" : "none");
    (void)sorts;
}

// A sub's frame, a freeze, and a die from three calls down.
static void down(rt_ctx *cx, int n, rt_value a, rt_value h) {
    rt_value f[2];
    rt_frame frame;
    rt_enter(cx, &frame, f, 2);
    f[0] = a;
    rt_freeze(cx, f[0]);
    if (n == 0) {
        rt_freeze(cx, h);
        // A sort under way, as a block that dies leaves it.
        f[1] = rt_array_new(cx);
        rt_list_add(cx, f[1], rt_int(2));
        rt_list_add(cx, f[1], rt_int(1));
        rt_sort *s = rt_sort_begin(cx, f[1], 0);
        rt_value x, y;
        rt_sort_next(cx, s, &x, &y);
        report(cx, "at the die", a, h);
        rt_value list = rt_array_new(cx);
        f[1] = list;
        rt_list_add(cx, list, rt_string(&MSG));
        cx->line = 9;
        rt_die(cx, list);
    }
    if (n > 0) down(cx, n - 1, a, h);
    rt_thaw(cx, f[0]);
    rt_leave(cx, &frame);
}

static void body(rt_ctx *cx) {
    rt_value slots[4];
    rt_frame frame;
    rt_enter(cx, &frame, slots, 4);
    cx->line = 1;
    slots[0] = rt_array_new(cx);
    slots[1] = rt_hash_new(cx);
    rt_list_add(cx, slots[0], rt_int(1));
    // A loop round the try: its freeze is not the try's to give back.
    rt_freeze(cx, slots[0]);
    report(cx, "before", slots[0], slots[1]);
    if (is("unwind")) {
        rt_try t;
        rt_try_begin(cx, &t);
        if (setjmp(t.jump) == 0) {
            down(cx, 3, slots[0], slots[1]);
            rt_try_end(cx, &t);
            printf("not reached\n");
        } else {
            slots[2] = rt_caught(cx);
            report(cx, "caught", slots[0], slots[1]);
            // Under stress, the message is a heap string, and the collector
            // must find it where the catch put it.
            rt_collect(cx);
            rt_print(cx, slots[2]);
        }
        // The arrays may be changed now, and a sort is a sort.
        rt_thaw(cx, slots[0]);
        rt_push(cx, slots[0], slots[0]);
        rt_helem_store(cx, slots[1], rt_int(1), rt_int(2));
        report(cx, "after", slots[0], slots[1]);
    }
    if (is("nested")) {
        // A try in a try: the inner catches; a die in its catch goes to
        // the outer; and a try closed by its own way out is not jumped to.
        rt_try outer;
        rt_try_begin(cx, &outer);
        if (setjmp(outer.jump) == 0) {
            rt_try closed;
            rt_try_begin(cx, &closed);
            if (setjmp(closed.jump) == 0) rt_try_end(cx, &closed);
            rt_try inner;
            rt_try_begin(cx, &inner);
            if (setjmp(inner.jump) == 0) {
                down(cx, 1, slots[0], slots[1]);
            } else {
                slots[2] = rt_caught(cx);
                report(cx, "inner caught", slots[0], slots[1]);
                rt_value list = rt_array_new(cx);
                slots[3] = list;
                rt_list_add(cx, list, rt_string(&NL));
                rt_die(cx, list);
            }
        } else {
            slots[2] = rt_caught(cx);
            report(cx, "outer caught", slots[0], slots[1]);
            rt_print(cx, slots[2]);
        }
        rt_thaw(cx, slots[0]);
    }
    if (is("uncaught")) {
        rt_thaw(cx, slots[0]);
        down(cx, 2, slots[0], slots[1]);
    }
    rt_leave(cx, &frame);
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "unwind.pl");
}
