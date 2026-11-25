// Arrays under the collector (D26, D80), driven from C, as collect.c
// drives strings: an array in a slot keeps the values it holds, one in no
// slot is collected with its storage, the storage counts against the cap,
// and an array holds no array. The argument says which case.
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
    printf("%s: %" PRIu64 " on the heap, %" PRIu64 " made, %" PRIu64 " collections, %" PRIu64 " bytes held\n",
           when, cx->objects, cx->allocations, cx->collections, cx->held);
}

static void body(rt_ctx *cx) {
    rt_value slots[3];
    rt_frame frame;
    rt_enter(cx, &frame, slots, 3);
    cx->line = 1;
    rt_value ab = rt_string(&AB);
    if (is("kept-through")) {
        // A string held only by an array that a slot holds is kept; one
        // in no slot goes; and when the slot lets the array go, both go,
        // and the array's storage with them.
        slots[0] = rt_array_new(cx);
        slots[1] = rt_concat(cx, ab, rt_int(1));
        rt_list_add(cx, slots[0], slots[1]);
        slots[1] = rt_undef();
        rt_concat(cx, ab, rt_int(2));
        report(cx, "made");
        rt_collect(cx);
        report(cx, "collected");
        rt_say(cx, rt_elem(cx, slots[0], rt_int(0)));
        slots[0] = rt_undef();
        rt_collect(cx);
        report(cx, "and again");
    }
    if (is("dropped")) {
        // An array in no slot is collected, and using it afterwards is
        // the collector's own error.
        rt_value a = rt_array_new(cx);
        rt_list_add(cx, a, rt_int(7));
        rt_collect(cx);
        report(cx, "collected");
        rt_say(cx, rt_count(cx, a));
    }
    if (is("storage")) {
        // An array's values are counted against the cap as they are
        // added: 16 bytes each, in storage that doubles.
        slots[0] = rt_array_new(cx);
        printf("pushing\n");
        for (int k = 0; k < 10000; k++) rt_list_add(cx, slots[0], rt_int(k));
        printf("not reached\n");
    }
    if (is("no-array-in-an-array")) {
        slots[0] = rt_array_new(cx);
        slots[1] = rt_array_new(cx);
        rt_elem_store(cx, slots[0], rt_int(0), slots[1]);
    }
    if (strncmp(which, "handed-", 7) == 0) {
        // What a call hands about (step 10a): a list added to a list is
        // its values; reversed; joined; the one value of a list of one.
        slots[0] = rt_array_new(cx);
        rt_list_add(cx, slots[0], rt_int(1));
        rt_list_add(cx, slots[0], ab);
        rt_list_add(cx, slots[0], rt_num(2.5));
        slots[1] = rt_array_new(cx);
        rt_list_add(cx, slots[1], rt_bool(1));
        rt_list_add(cx, slots[1], slots[0]);
        rt_list_add(cx, slots[1], rt_absent());
        rt_say(cx, rt_count(cx, slots[1]));
        rt_list_add_reversed(cx, slots[1], slots[0]);
        rt_say_list(cx, slots[1]);
        rt_say(cx, rt_join(cx, rt_string(&AB), slots[0]));
        rt_say(cx, rt_join(cx, rt_int(0), slots[1]));
        slots[2] = rt_array_new(cx);
        rt_say(cx, rt_length(cx, rt_join(cx, ab, slots[2])));
        printf("%d\n", rt_only(cx, slots[2]).tag == RT_TAG_ABSENT);
        rt_list_add(cx, slots[2], rt_int(7));
        rt_say(cx, rt_only(cx, slots[2]));
        rt_say(cx, rt_join(cx, ab, slots[2]));
        // A slurpy parameter, from a list and from places: the second
        // argument on.
        rt_value *where[3] = { &slots[0], &slots[1], &slots[2] };
        rt_value places[3] = { rt_int(4), rt_int(5), rt_int(6) };
        for (int n = 0; n < 3; n++) where[n] = &places[n];
        rt_slurp(cx, slots[2], 3, where, NULL, 1);
        rt_slurp(cx, slots[2], 3, NULL, rt_list_items(cx, slots[0]), 1);
        rt_slurp(cx, slots[2], 3, where, NULL, 3);
        rt_say_list(cx, slots[2]);
        if (is("handed-join-undef")) rt_join(cx, ab, slots[1]) , rt_list_add(cx, slots[0], rt_undef()), rt_join(cx, ab, slots[0]);
        if (is("handed-separator-undef")) rt_join(cx, rt_undef(), slots[1]);
        if (is("handed-only-two")) rt_only(cx, slots[0]);
    }
    if (is("every-way")) {
        // What each way of changing an array leaves, read back.
        slots[0] = rt_array_new(cx);
        slots[1] = rt_array_new(cx);
        for (int k = 1; k <= 3; k++) rt_list_add(cx, slots[1], rt_int(k));
        rt_array_assign(cx, slots[0], slots[1]);
        rt_say(cx, rt_push(cx, slots[0], slots[1]));
        rt_say(cx, rt_unshift(cx, slots[0], slots[1]));
        rt_say(cx, rt_pop(cx, slots[0]));
        rt_say(cx, rt_shift(cx, slots[0]));
        rt_say_list(cx, slots[0]);
        rt_say(cx, rt_elem_store(cx, slots[0], rt_int(9), rt_int(5)));
        rt_say(cx, rt_last_index(cx, slots[0]));
        rt_say(cx, rt_defined(cx, rt_elem(cx, slots[0], rt_int(8))));
        rt_say(cx, rt_elem(cx, slots[0], rt_int(-1)));
        rt_say(cx, rt_defined(cx, rt_elem(cx, slots[0], rt_int(INT64_MIN))));
        rt_say(cx, rt_defined(cx, rt_elem(cx, slots[0], rt_int(INT64_MAX))));
        slots[2] = rt_array_new(cx);
        rt_splice(cx, slots[2], slots[0], 2, rt_int(-2), rt_int(INT64_MAX), slots[1]);
        rt_say(cx, rt_count(cx, slots[2]));
        rt_say(cx, rt_count(cx, slots[0]));
    }
    if (strncmp(which, "frozen-", 7) == 0 || is("thaw-unfrozen")) {
        slots[0] = rt_array_new(cx);
        for (int n = 1; n <= 3; n++) rt_list_add(cx, slots[0], rt_int(n));
        slots[1] = rt_array_new(cx);
        rt_list_add(cx, slots[1], rt_int(7));
        slots[2] = rt_array_new(cx);
        if (is("thaw-unfrozen")) rt_thaw(cx, slots[0]);
        rt_freeze(cx, slots[0]);
        rt_freeze(cx, slots[0]);
        rt_say(cx, rt_count(cx, slots[0]));
        rt_say(cx, rt_last_index(cx, slots[0]));
        rt_say(cx, rt_elem(cx, slots[0], rt_int(-1)));
        rt_say(cx, rt_first(cx, slots[0]));
        rt_say(cx, rt_elem_strict(cx, slots[0], rt_int(1)));
        rt_say_list(cx, slots[0]);
        rt_thaw(cx, slots[0]);
        if (is("frozen-none")) rt_thaw(cx, slots[0]);
        if (is("frozen-none") || is("frozen-push")) rt_say(cx, rt_push(cx, slots[0], slots[1]));
        if (is("frozen-unshift")) rt_unshift(cx, slots[0], slots[1]);
        if (is("frozen-pop")) rt_pop(cx, slots[0]);
        if (is("frozen-shift")) rt_shift(cx, slots[0]);
        // A splice that takes nothing out and puts nothing in.
        if (is("frozen-splice")) rt_splice(cx, slots[2], slots[0], 2, rt_int(0), rt_int(0), slots[2]);
        if (is("frozen-store")) rt_elem_store(cx, slots[0], rt_int(0), rt_int(1));
        // An element that is there already, made for a store.
        if (is("frozen-make")) rt_elem_make(cx, slots[0], rt_int(-1));
        if (is("frozen-assign")) rt_array_assign(cx, slots[0], slots[1]);
        if (is("frozen-rest")) rt_array_rest(cx, slots[0], slots[1], 0);
    }
    if (strncmp(which, "strict", 6) == 0 || strncmp(which, "range-", 6) == 0) {
        slots[0] = rt_array_new(cx);
        for (int n = 1; n <= 3; n++) rt_list_add(cx, slots[0], rt_int(n));
        int64_t lo = 0, hi = 0;
        if (is("strict")) {
            rt_say(cx, rt_elem_strict(cx, slots[0], rt_int(2)));
            rt_say(cx, rt_elem_strict(cx, slots[0], rt_int(-1)));
            int go = rt_range_ends(cx, rt_int(1), rt_int(3), &lo, &hi);
            printf("%d %" PRId64 " %" PRId64 "\n", go, lo, hi);
            go = rt_range_ends(cx, rt_int(3), rt_int(1), &lo, &hi);
            printf("%d %" PRId64 " %" PRId64 "\n", go, lo, hi);
            go = rt_range_ends(cx, rt_num(-1.9), rt_num(1.9), &lo, &hi);
            printf("%d %" PRId64 " %" PRId64 "\n", go, lo, hi);
            go = rt_range_ends(cx, rt_int(INT64_MIN + 513), rt_int(0), &lo, &hi);
            printf("%d %" PRId64 " %" PRId64 "\n", go, lo, hi);
        }
        if (is("strict-past")) rt_elem_strict(cx, slots[0], rt_int(3));
        if (is("strict-before")) rt_elem_strict(cx, slots[0], rt_int(-4));
        if (is("range-low")) rt_range_ends(cx, rt_int(INT64_MIN + 512), rt_int(0), &lo, &hi);
        if (is("range-low-end")) rt_range_ends(cx, rt_int(0), rt_int(INT64_MIN + 512), &lo, &hi);
        if (is("range-string")) rt_range_ends(cx, rt_int(0), ab, &lo, &hi);
        if (is("range-string-from")) rt_range_ends(cx, ab, rt_int(0), &lo, &hi);
    }
    rt_leave(cx, &frame);
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "arrays.pl");
}
