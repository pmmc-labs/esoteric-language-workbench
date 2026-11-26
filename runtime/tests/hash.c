// Hashes (step 12a; D27), driven from C as arrays.c drives arrays: the
// order of the keys, a key made a string, the holes a delete leaves and
// their closing, the table as it grows, what the collector keeps and what
// counts against the cap, and the faults. The argument says which case.
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
#include "rt.h"

static const char *which;
static const rt_str AB = { 2, 2, "ab", RT_STR_CONSTANT };
static const rt_str AB1 = { 3, 3, "ab1", RT_STR_CONSTANT };
static const rt_str SEVEN = { 1, 1, "7", RT_STR_CONSTANT };
static const rt_str COMMA = { 1, 1, ",", RT_STR_CONSTANT };
static const rt_str K = { 1, 1, "k", RT_STR_CONSTANT };
static const rt_str A = { 1, 1, "a", RT_STR_CONSTANT };
static const rt_str B = { 1, 1, "b", RT_STR_CONSTANT };
static const rt_str C = { 1, 1, "c", RT_STR_CONSTANT };
static const rt_str D = { 1, 1, "d", RT_STR_CONSTANT };
static const rt_str EMPTY = { 0, 0, "", RT_STR_CONSTANT };

static int is(const char *name) {
    return strcmp(which, name) == 0;
}

static void report(rt_ctx *cx, const char *when) {
    printf("%s: %" PRIu64 " on the heap, %" PRIu64 " made, %" PRIu64 " collections, %" PRIu64 " bytes held\n",
           when, cx->objects, cx->allocations, cx->collections, cx->held);
}

// The keys, then the values, each joined with commas: slot 3 is the list.
static void show(rt_ctx *cx, rt_value *slots) {
    slots[3] = rt_array_new(cx);
    rt_list_add_keys(cx, slots[3], slots[0]);
    slots[3] = rt_join(cx, rt_string(&COMMA), slots[3]);
    rt_print(cx, slots[3]);
    printf("|");
    slots[3] = rt_array_new(cx);
    rt_list_add_values(cx, slots[3], slots[0]);
    slots[3] = rt_join(cx, rt_string(&COMMA), slots[3]);
    rt_print(cx, slots[3]);
    printf("|");
    rt_say(cx, rt_hash_count(cx, slots[0]));
}

// The four keys a, b, c, d with 1 to 4, in slot 0.
static void four(rt_ctx *cx, rt_value *slots) {
    slots[0] = rt_hash_new(cx);
    rt_helem_store(cx, slots[0], rt_string(&A), rt_int(1));
    rt_helem_store(cx, slots[0], rt_string(&B), rt_int(2));
    rt_helem_store(cx, slots[0], rt_string(&C), rt_int(3));
    rt_helem_store(cx, slots[0], rt_string(&D), rt_int(4));
}

static void body(rt_ctx *cx) {
    rt_value slots[4];
    rt_frame frame;
    rt_enter(cx, &frame, slots, 4);
    cx->line = 1;
    rt_value ab = rt_string(&AB);
    if (is("kept-through")) {
        // A key and a value held only by a hash that a slot holds are
        // kept; a string in no slot goes; and when the slot lets the hash
        // go, all go, and the hash's storage and index with them.
        slots[0] = rt_hash_new(cx);
        slots[1] = rt_concat(cx, ab, rt_int(1));
        slots[2] = rt_concat(cx, ab, rt_int(2));
        rt_helem_store(cx, slots[0], slots[1], slots[2]);
        slots[1] = rt_undef();
        slots[2] = rt_undef();
        rt_concat(cx, ab, rt_int(3));
        report(cx, "made");
        rt_collect(cx);
        report(cx, "collected");
        rt_say(cx, rt_helem(cx, slots[0], rt_string(&AB1)));
        slots[0] = rt_undef();
        rt_collect(cx);
        report(cx, "and again");
    }
    if (is("dropped")) {
        rt_value h = rt_hash_new(cx);
        rt_helem_store(cx, h, ab, rt_int(7));
        rt_collect(cx);
        report(cx, "collected");
        rt_say(cx, rt_hash_count(cx, h));
    }
    if (is("number-key")) {
        // A key is a string: the Int 7, the Num 7 and "7" are one key,
        // true is "1" and false is "". A key that was a number is a
        // string made for the hash: one allocation, at the store.
        slots[0] = rt_hash_new(cx);
        rt_helem_store(cx, slots[0], rt_int(7), ab);
        printf("%" PRIu64 " made\n", cx->allocations);
        rt_say(cx, rt_helem(cx, slots[0], rt_string(&SEVEN)));
        rt_say(cx, rt_helem(cx, slots[0], rt_num(7.0)));
        rt_helem_store(cx, slots[0], rt_num(7.0), rt_int(1));
        rt_helem_store(cx, slots[0], rt_string(&SEVEN), rt_int(2));
        rt_helem_store(cx, slots[0], rt_bool(1), rt_int(3));
        rt_helem_store(cx, slots[0], rt_bool(0), rt_int(4));
        rt_helem_store(cx, slots[0], rt_num(1.5), rt_int(5));
        printf("%" PRIu64 " made\n", cx->allocations);
        rt_say(cx, rt_helem(cx, slots[0], rt_int(1)));
        rt_say(cx, rt_helem(cx, slots[0], rt_string(&EMPTY)));
        rt_say(cx, rt_hash_exists(cx, slots[0], rt_int(8)));
        rt_say(cx, rt_hash_exists(cx, slots[0], rt_int(7)));
        show(cx, slots);
    }
    if (is("order")) {
        // The order the keys were first stored in; a key stored again
        // keeps its place; one deleted and stored again is last; a read
        // makes nothing.
        four(cx, slots);
        show(cx, slots);
        rt_helem_store(cx, slots[0], rt_string(&B), rt_int(22));
        rt_say(cx, rt_defined(cx, rt_helem(cx, slots[0], rt_string(&K))));
        show(cx, slots);
        rt_say(cx, rt_hash_delete(cx, slots[0], rt_string(&B)));
        rt_say(cx, rt_defined(cx, rt_hash_delete(cx, slots[0], rt_string(&B))));
        show(cx, slots);
        rt_helem_store(cx, slots[0], rt_string(&B), rt_int(5));
        show(cx, slots);
        // Made, got and put by the number of its pair.
        int64_t at = rt_helem_make(cx, slots[0], rt_string(&K));
        rt_say(cx, rt_defined(cx, rt_helem_get(cx, slots[0], at)));
        rt_helem_put(cx, slots[0], at, rt_int(6));
        show(cx, slots);
        // The hash where a list is wanted, and assigned from one: a key
        // given twice keeps its first place and its last value.
        slots[1] = rt_array_new(cx);
        rt_list_add_pairs(cx, slots[1], slots[0]);
        rt_list_add(cx, slots[1], rt_string(&A));
        rt_list_add(cx, slots[1], rt_int(9));
        rt_say(cx, rt_count(cx, slots[1]));
        rt_hash_assign(cx, slots[0], slots[1]);
        show(cx, slots);
        // From the list's third value on.
        rt_hash_rest(cx, slots[0], slots[1], 2);
        show(cx, slots);
        rt_hash_rest(cx, slots[0], slots[1], 99);
        show(cx, slots);
    }
    if (is("grow")) {
        // Ten thousand keys, every one found; the even ones deleted, and
        // only they are gone; the order holds through the holes and
        // their closing.
        slots[0] = rt_hash_new(cx);
        for (int k = 1; k <= 10000; k++) {
            slots[1] = rt_concat(cx, rt_string(&K), rt_int(k));
            rt_helem_store(cx, slots[0], slots[1], rt_int(k));
        }
        rt_say(cx, rt_hash_count(cx, slots[0]));
        int64_t sum = 0;
        for (int k = 1; k <= 10000; k++) {
            slots[1] = rt_concat(cx, rt_string(&K), rt_int(k));
            sum += rt_helem(cx, slots[0], slots[1]).as.i;
        }
        printf("%" PRId64 "\n", sum);
        for (int k = 2; k <= 10000; k += 2) {
            slots[1] = rt_concat(cx, rt_string(&K), rt_int(k));
            if (rt_hash_delete(cx, slots[0], slots[1]).as.i != k) printf("wrong value deleted at %d\n", k);
        }
        rt_say(cx, rt_hash_count(cx, slots[0]));
        int found = 0, missing = 0;
        for (int k = 1; k <= 10000; k++) {
            slots[1] = rt_concat(cx, rt_string(&K), rt_int(k));
            rt_value v = rt_helem(cx, slots[0], slots[1]);
            if (v.tag == RT_TAG_INT && v.as.i == k) found += 1;
            if (v.tag == RT_TAG_UNDEF && rt_hash_exists(cx, slots[0], slots[1]).as.i == 0) missing += 1;
        }
        printf("%d found, %d missing\n", found, missing);
        for (int k = 1; k <= 9990; k += 2) {
            slots[1] = rt_concat(cx, rt_string(&K), rt_int(k));
            rt_hash_delete(cx, slots[0], slots[1]);
        }
        rt_helem_store(cx, slots[0], rt_string(&A), rt_int(0));
        slots[1] = rt_concat(cx, rt_string(&K), rt_int(9993));
        rt_hash_delete(cx, slots[0], slots[1]);
        rt_helem_store(cx, slots[0], slots[1], rt_int(1));
        show(cx, slots);
    }
    if (is("storage")) {
        // A hash's pairs and its index are counted against the cap as
        // they grow.
        slots[0] = rt_hash_new(cx);
        printf("storing\n");
        for (int k = 0; k < 5000; k++) rt_helem_store(cx, slots[0], rt_int(k), rt_int(k));
        printf("stored\n");
    }
    if (is("odd")) {
        slots[1] = rt_array_new(cx);
        for (int k = 0; k < 3; k++) rt_list_add(cx, slots[1], rt_int(k));
        slots[0] = rt_hash_new(cx);
        rt_hash_rest(cx, slots[0], slots[1], 1);
        show(cx, slots);
        rt_hash_assign(cx, slots[0], slots[1]);
    }
    if (is("undef-key")) {
        four(cx, slots);
        rt_helem(cx, slots[0], rt_undef());
    }
    if (is("whole-num-key")) {
        // D36: a whole Num from 10^15 up has two ways to print.
        four(cx, slots);
        rt_helem_store(cx, slots[0], rt_num(1e15), rt_int(1));
    }
    if (is("no-array-in-a-hash")) {
        four(cx, slots);
        slots[1] = rt_array_new(cx);
        rt_helem_store(cx, slots[0], rt_string(&A), slots[1]);
    }
    if (is("no-hash-in-an-array")) {
        four(cx, slots);
        slots[1] = rt_array_new(cx);
        rt_list_add(cx, slots[1], slots[0]);
    }
    if (is("not-a-hash")) {
        slots[0] = rt_array_new(cx);
        rt_helem(cx, slots[0], rt_string(&A));
    }
    if (is("not-an-array")) {
        four(cx, slots);
        rt_elem(cx, slots[0], rt_int(0));
    }
    if (is("put-nowhere")) {
        four(cx, slots);
        rt_helem_put(cx, slots[0], 4, rt_int(1));
    }
    if (is("put-in-a-hole")) {
        // A key made, and deleted before it was stored to.
        four(cx, slots);
        int64_t at = rt_helem_make(cx, slots[0], rt_string(&B));
        rt_hash_delete(cx, slots[0], rt_string(&B));
        rt_helem_put(cx, slots[0], at, rt_int(1));
    }
    if (strncmp(which, "frozen-", 7) == 0) {
        // While a loop is over a hash (step 12b will be the first to ask):
        // it is read, and every change is a fault.
        four(cx, slots);
        rt_freeze(cx, slots[0]);
        rt_say(cx, rt_helem(cx, slots[0], rt_string(&A)));
        rt_say(cx, rt_hash_exists(cx, slots[0], rt_string(&K)));
        rt_say(cx, rt_defined(cx, rt_hash_delete(cx, slots[0], rt_string(&K))));
        show(cx, slots);
        slots[1] = rt_array_new(cx);
        if (is("frozen-store")) rt_helem_store(cx, slots[0], rt_string(&A), rt_int(9));
        if (is("frozen-new")) rt_helem_store(cx, slots[0], rt_string(&K), rt_int(9));
        if (is("frozen-make")) rt_helem_make(cx, slots[0], rt_string(&A));
        if (is("frozen-delete")) rt_hash_delete(cx, slots[0], rt_string(&A));
        if (is("frozen-assign")) rt_hash_assign(cx, slots[0], slots[1]);
        rt_thaw(cx, slots[0]);
        rt_helem_store(cx, slots[0], rt_string(&K), rt_int(9));
        rt_say(cx, rt_hash_count(cx, slots[0]));
    }
    if (strncmp(which, "on-", 3) == 0) {
        // What stands on a hash (step 12b). Slot 1 is a list of keys, a,
        // k and d, of which k is not there; slot 2 a list of two values.
        four(cx, slots);
        slots[1] = rt_array_new(cx);
        rt_list_add(cx, slots[1], rt_string(&A));
        rt_list_add(cx, slots[1], rt_string(&K));
        rt_list_add(cx, slots[1], rt_string(&D));
        slots[2] = rt_array_new(cx);
        rt_list_add(cx, slots[2], rt_int(10));
        rt_list_add(cx, slots[2], rt_int(20));
        slots[3] = rt_array_new(cx);
        if (is("on-strict")) {
            rt_say(cx, rt_helem_strict(cx, slots[0], rt_string(&D)));
            rt_helem_strict(cx, slots[0], rt_string(&K));
        }
        if (is("on-slice") || is("on-slice-strict")) {
            // The value at each key, in the order asked; undef, and no key
            // made, for one that is not there.
            rt_list_add_hslice(cx, slots[3], slots[0], slots[1], 0);
            rt_say(cx, rt_count(cx, slots[3]));
            rt_say(cx, rt_list_item(cx, slots[3], 0));
            rt_say(cx, rt_defined(cx, rt_list_item(cx, slots[3], 1)));
            rt_say(cx, rt_list_item(cx, slots[3], 2));
            rt_say(cx, rt_hash_count(cx, slots[0]));
            if (is("on-slice-strict")) rt_list_add_hslice(cx, slots[3], slots[0], slots[1], 1);
        }
        if (is("on-store") || is("on-store-frozen")) {
            // A value for each key in turn, and an undef for the third,
            // which the list does not reach: its key is made all the same.
            if (is("on-store-frozen")) rt_freeze(cx, slots[0]);
            rt_hslice_store(cx, slots[0], slots[1], slots[2]);
            rt_say(cx, rt_hash_count(cx, slots[0]));
            rt_say(cx, rt_helem(cx, slots[0], rt_string(&A)));
            rt_say(cx, rt_helem(cx, slots[0], rt_string(&K)));
            rt_say(cx, rt_defined(cx, rt_helem(cx, slots[0], rt_string(&D))));
            rt_say(cx, rt_hash_exists(cx, slots[0], rt_string(&D)));
            slots[3] = rt_array_new(cx);
            rt_list_add_keys(cx, slots[3], slots[0]);
            rt_say(cx, rt_join(cx, rt_string(&COMMA), slots[3]));
        }
        if (is("on-delete") || is("on-delete-frozen")) {
            if (is("on-delete-frozen")) rt_freeze(cx, slots[0]);
            rt_hash_delete_slice(cx, slots[3], slots[0], slots[1]);
            rt_say(cx, rt_count(cx, slots[3]));
            rt_say(cx, rt_list_item(cx, slots[3], 0));
            rt_say(cx, rt_defined(cx, rt_list_item(cx, slots[3], 1)));
            rt_say(cx, rt_list_item(cx, slots[3], 2));
            show(cx, slots);
        }
        if (is("on-parameter")) {
            // The arguments left for a hash, from the second on: from
            // where they are, and from a list of them.
            rt_value given[5] = { rt_int(7), rt_string(&K), rt_int(1), rt_string(&A), rt_int(2) };
            rt_value *where[5] = { &given[0], &given[1], &given[2], &given[3], &given[4] };
            slots[3] = rt_hash_new(cx);
            rt_slurp_hash(cx, slots[3], 5, where, NULL, 1);
            slots[0] = slots[3];
            show(cx, slots);
            slots[0] = rt_hash_new(cx);
            rt_slurp_hash(cx, slots[0], 5, NULL, given, 3);
            rt_slurp_hash(cx, slots[0], 5, NULL, given, 5);
            show(cx, slots);
            rt_fault_odd_arguments(cx, "f");
        }
        if (is("on-array") || is("on-array-before")) {
            // An array's slice stored to: the indexes 0 and 4 of an array
            // of three, and one value.
            slots[0] = rt_array_new(cx);
            for (int k = 1; k <= 3; k++) rt_list_add(cx, slots[0], rt_int(k));
            slots[1] = rt_array_new(cx);
            rt_list_add(cx, slots[1], rt_int(0));
            rt_list_add(cx, slots[1], rt_int(is("on-array-before") ? -4 : 4));
            slots[2] = rt_array_new(cx);
            rt_list_add(cx, slots[2], rt_int(9));
            rt_slice_store(cx, slots[0], slots[1], slots[2]);
            rt_say(cx, rt_count(cx, slots[0]));
            rt_say(cx, rt_elem(cx, slots[0], rt_int(0)));
            rt_say(cx, rt_defined(cx, rt_elem(cx, slots[0], rt_int(4))));
        }
    }
    rt_leave(cx, &frame);
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "hash.pl");
}
