// The collector (D26, D66), driven from C: frames made by hand, values
// held in slots and out of them, a collection asked for by name, and the
// context's counters read. No program of the language can see a
// collection, so what one frees and what it keeps is tested here. The
// argument says which case; the knobs come from the environment, as they
// do for any compiled program.
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
#include "rt.h"

static const char *which;
static const rt_str AB = { 2, 2, "ab", RT_STR_CONSTANT };

static int is(const char *name) {
    return strcmp(which, name) == 0;
}

static void report(rt_ctx *cx, const char *when) {
    printf("%s: %" PRIu64 " on the heap, %" PRIu64 " made, %" PRIu64 " collections\n", when, cx->objects, cx->allocations, cx->collections);
}

static void body(rt_ctx *cx) {
    rt_value slots[4];
    rt_frame frame;
    // What the C stack held before is not a value: a frame opens empty.
    memset(slots, 3, sizeof slots);
    rt_enter(cx, &frame, slots, 4);
    if (is("opens-empty")) {
        rt_collect(cx);
        report(cx, "collected");
    }
    cx->line = 1;
    rt_value ab = rt_string(&AB);
    if (is("kept-and-freed")) {
        // One string in a slot and one in none: a collection frees the
        // second, and the first when its slot is given something else.
        slots[0] = rt_concat(cx, ab, rt_int(1));
        rt_concat(cx, ab, rt_int(2));
        report(cx, "made");
        rt_collect(cx);
        report(cx, "collected");
        rt_say(cx, slots[0]);
        slots[0] = rt_undef();
        rt_collect(cx);
        report(cx, "and again");
    }
    if (is("constant")) {
        // A constant is not on the heap, and a collection leaves it alone.
        slots[0] = ab;
        rt_collect(cx);
        rt_collect(cx);
        rt_say(cx, slots[0]);
        report(cx, "collected");
    }
    if (is("numbers")) {
        // A number where a string is wanted makes no string: joining two
        // is one allocation, and reading one is none.
        slots[0] = rt_concat(cx, rt_int(12), rt_num(1.5));
        report(cx, "joined");
        slots[1] = rt_length(cx, rt_int(-9223372036854775807 - 1));
        slots[2] = rt_str_eq(cx, rt_int(12), rt_num(12.0));
        slots[3] = rt_index2(cx, rt_num(0.1 + 0.2), rt_int(3));
        report(cx, "read");
        rt_say(cx, slots[0]);
        rt_say(cx, slots[1]);
        rt_say(cx, slots[2]);
        rt_say(cx, slots[3]);
    }
    if (is("two-frames")) {
        // A string held only by an older frame is kept while a newer one
        // is open, and what the newer one held is garbage once it closes.
        slots[0] = rt_concat(cx, ab, rt_int(1));
        rt_value inner[2];
        rt_frame second;
        rt_enter(cx, &second, inner, 2);
        inner[1] = rt_concat(cx, ab, rt_int(2));
        rt_collect(cx);
        report(cx, "both open");
        rt_say(cx, slots[0]);
        rt_say(cx, inner[1]);
        rt_leave(cx, &second);
        rt_collect(cx);
        report(cx, "the newer closed");
        rt_say(cx, slots[0]);
    }
    if (is("every-slot")) {
        // The first slot and the last are roots as the ones between are.
        for (int k = 0; k < 4; k++) slots[k] = rt_concat(cx, ab, rt_int(k));
        rt_collect(cx);
        report(cx, "four held");
        for (int k = 0; k < 4; k++) rt_say(cx, slots[k]);
    }
    if (is("repeat-after") || is("case-after") || is("substr-after")) {
        // Each operation that makes a string from one reads its operand
        // after the allocation, and looks at it again there.
        rt_value loose = rt_concat(cx, ab, rt_int(1));
        rt_say(cx, loose);
        if (is("repeat-after")) slots[0] = rt_repeat(cx, loose, rt_int(2));
        if (is("case-after")) slots[0] = rt_uc(cx, loose);
        if (is("substr-after")) slots[0] = rt_substr2(cx, loose, rt_int(1));
        rt_say(cx, slots[0]);
    }
    if (is("used-after") || is("number-after") || is("truth-after") || is("operand-after") || is("slot-after")) {
        // A string in no slot, collected, and then used: each way a string
        // is read says so, and so does the collector when it finds one in
        // a slot. (Under poison: without it the memory is the system's.)
        rt_value loose = rt_concat(cx, ab, rt_int(1));
        rt_say(cx, loose);
        if (is("operand-after")) {
            // Under stress the collection is inside the operation itself,
            // after its operands were read the first time.
            slots[0] = rt_concat(cx, loose, loose);
        }
        rt_collect(cx);
        if (is("used-after")) rt_say(cx, loose);
        if (is("number-after")) slots[0] = rt_add(cx, loose, rt_int(1));
        if (is("truth-after")) slots[0] = rt_not(cx, loose);
        if (is("slot-after")) {
            slots[0] = loose;
            rt_collect(cx);
        }
    }
    if (is("policy")) {
        // No knob: a hundred megabytes of garbage, a kilobyte at a time,
        // each in the same slot. A collection comes when a megabyte has
        // been allocated since the last.
        for (int k = 0; k < 100000; k++) slots[1] = rt_repeat(cx, ab, rt_int(500));
        printf("%" PRIu64 " made, %" PRIu64 " collections, %" PRIu64 " on the heap, %" PRIu64 " bytes held\n", cx->allocations, cx->collections, cx->objects, cx->held);
    }
    if (is("policy-grows")) {
        // What is live is kept, and the next collection waits for as much
        // again: eight megabytes held in four slots, and then garbage.
        for (int k = 0; k < 4; k++) slots[k] = rt_repeat(cx, ab, rt_int(1000000));
        uint64_t before = cx->collections;
        slots[0] = rt_repeat(cx, ab, rt_int(1000000));
        slots[0] = rt_repeat(cx, ab, rt_int(1000000));
        printf("%" PRIu64 " collections for two more\n", cx->collections - before);
    }
    if (is("cap")) {
        // Garbage is not held: a megabyte of it passes under a cap of 4096
        // bytes. Four kilobyte strings in four slots do not.
        for (int k = 0; k < 1000; k++) slots[0] = rt_repeat(cx, ab, rt_int(500));
        report(cx, "garbage");
        for (int k = 0; k < 4; k++) {
            slots[k] = rt_repeat(cx, ab, rt_int(500));
            printf("held %d\n", k + 1);
        }
    }
    if (is("left-open")) return;
    if (is("closed-out-of-turn")) {
        rt_value inner[1];
        rt_frame second;
        rt_enter(cx, &second, inner, 1);
        rt_leave(cx, &frame);
    }
    rt_leave(cx, &frame);
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "collect.pl");
}
