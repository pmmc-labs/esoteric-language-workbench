// References (step 13a; D107, D112, D114), driven from C as arrays.c
// drives arrays: what the collector does with a chain of references a
// million long and with a cycle, what an arrow reads through and what it
// makes, the freeze through a reference, and every operator's fault for a
// reference where a number or a string is wanted. The argument says which
// case.
#include <inttypes.h>
#include <stdio.h>
#include <string.h>
#include "rt.h"

static const char *which;
static const rt_str A = { 1, 1, "a", RT_STR_CONSTANT };
static const rt_str AB = { 2, 2, "ab", RT_STR_CONSTANT };

static int is(const char *name) {
    return strcmp(which, name) == 0;
}

static void report(rt_ctx *cx, const char *when) {
    printf("%s: %" PRIu64 " on the heap\n", when, cx->objects);
}

// An operator given a reference, by name: each must fault.
static void apply(rt_ctx *cx, const char *op, rt_value r) {
    rt_value one = rt_int(1);
    rt_value s = rt_string(&AB);
    if (strcmp(op, "add") == 0) rt_add(cx, r, one);
    if (strcmp(op, "add-right") == 0) rt_add(cx, one, r);
    if (strcmp(op, "sub") == 0) rt_sub(cx, r, one);
    if (strcmp(op, "mul") == 0) rt_mul(cx, r, one);
    if (strcmp(op, "div") == 0) rt_div(cx, r, one);
    if (strcmp(op, "mod") == 0) rt_mod(cx, r, one);
    if (strcmp(op, "pow") == 0) rt_pow(cx, r, one);
    if (strcmp(op, "neg") == 0) rt_neg(cx, r);
    if (strcmp(op, "inc") == 0) rt_inc(cx, r);
    if (strcmp(op, "dec") == 0) rt_dec(cx, r);
    if (strcmp(op, "add-to") == 0) rt_add_to(cx, r, one);
    if (strcmp(op, "lt") == 0) rt_num_lt(cx, r, one);
    if (strcmp(op, "cmp-num") == 0) rt_num_cmp(cx, r, r);
    if (strcmp(op, "eq-num") == 0) rt_num_eq(cx, r, one);
    if (strcmp(op, "eq-num-right") == 0) rt_num_eq(cx, one, r);
    if (strcmp(op, "ne-num") == 0) rt_num_ne(cx, one, r);
    if (strcmp(op, "chr") == 0) rt_chr(cx, r);
    if (strcmp(op, "repeat-count") == 0) rt_repeat(cx, s, r);
    if (strcmp(op, "substr-offset") == 0) rt_substr2(cx, s, r);
    if (strcmp(op, "index") == 0) rt_elem(cx, rt_array_new(cx), r);
    if (strcmp(op, "concat") == 0) rt_concat(cx, r, s);
    if (strcmp(op, "concat-right") == 0) rt_concat(cx, s, r);
    if (strcmp(op, "concat-to") == 0) rt_concat_to(cx, r, s);
    if (strcmp(op, "repeat") == 0) rt_repeat(cx, r, one);
    if (strcmp(op, "length") == 0) rt_length(cx, r);
    if (strcmp(op, "uc") == 0) rt_uc(cx, r);
    if (strcmp(op, "lc") == 0) rt_lc(cx, r);
    if (strcmp(op, "ord") == 0) rt_ord(cx, r);
    if (strcmp(op, "eq-str") == 0) rt_str_eq(cx, r, r);
    if (strcmp(op, "cmp-str") == 0) rt_str_cmp(cx, s, r);
    if (strcmp(op, "substr") == 0) rt_substr2(cx, r, one);
    if (strcmp(op, "index-str") == 0) rt_index2(cx, s, r);
    if (strcmp(op, "say") == 0) rt_say(cx, r);
    if (strcmp(op, "print") == 0) rt_print(cx, r);
    if (strcmp(op, "key") == 0) rt_helem(cx, rt_hash_new(cx), r);
    if (strcmp(op, "key-stored") == 0) rt_helem_store(cx, rt_hash_new(cx), r, one);
    if (strcmp(op, "join") == 0) {
        rt_value l = rt_array_new(cx);
        rt_list_add(cx, l, r);
        rt_join(cx, s, l);
    }
    if (strcmp(op, "join-separator") == 0) rt_join(cx, r, rt_array_new(cx));
    if (strcmp(op, "range") == 0) rt_list_add_range(cx, rt_array_new(cx), r, one);
    if (strcmp(op, "sort") == 0) {
        rt_value l = rt_array_new(cx);
        rt_list_add(cx, l, s);
        rt_list_add(cx, l, r);
        rt_value into = rt_array_new(cx);
        rt_sort_strings(cx, l, into);
    }
    if (strcmp(op, "say-list") == 0) {
        rt_value l = rt_array_new(cx);
        rt_list_add(cx, l, s);
        rt_list_add(cx, l, r);
        rt_say_list(cx, l);
    }
}

static void body(rt_ctx *cx) {
    rt_value slots[4];
    rt_frame frame;
    rt_enter(cx, &frame, slots, 4);
    cx->line = 1;
    if (is("deep")) {
        // A list linked a million deep: each array holds a reference to the
        // one made before. A mark that recursed would need the C stack's
        // hundreds of megabytes for it; rt_run gives it eight.
        slots[0] = rt_undef();
        for (int k = 0; k < 1000000; k++) {
            slots[1] = rt_array_new(cx);
            rt_list_add(cx, slots[1], slots[0]);
            slots[0] = rt_aref(cx, slots[1]);
        }
        slots[1] = rt_undef();
        rt_collect(cx);
        report(cx, "a million kept");
        // The last one is reached through all the others.
        rt_value r = slots[0];
        int64_t n = 0;
        while (r.tag == RT_TAG_AREF) {
            r = rt_elem(cx, rt_deref(cx, r, 0), rt_int(0));
            n += 1;
        }
        printf("%" PRId64 " deep\n", n);
        slots[0] = rt_undef();
        rt_collect(cx);
        report(cx, "dropped");
    }
    if (is("cycle")) {
        // Two hashes that hold each other, and a third that holds itself:
        // kept while a slot holds one, and all freed when none does.
        slots[0] = rt_hash_new(cx);
        slots[1] = rt_hash_new(cx);
        rt_helem_store(cx, slots[0], rt_string(&A), rt_href(cx, slots[1]));
        rt_helem_store(cx, slots[1], rt_string(&A), rt_href(cx, slots[0]));
        slots[2] = rt_hash_new(cx);
        rt_helem_store(cx, slots[2], rt_string(&A), rt_href(cx, slots[2]));
        slots[1] = rt_undef();
        slots[2] = rt_undef();
        rt_collect(cx);
        report(cx, "one held");
        slots[0] = rt_undef();
        rt_collect(cx);
        report(cx, "none held");
    }
    if (is("strings-inside")) {
        // A string held only by an array that only a reference holds.
        slots[1] = rt_array_new(cx);
        rt_list_add(cx, slots[1], rt_concat(cx, rt_string(&AB), rt_int(7)));
        slots[0] = rt_aref(cx, slots[1]);
        slots[1] = rt_undef();
        rt_collect(cx);
        rt_say(cx, rt_elem(cx, rt_deref(cx, slots[0], 0), rt_int(0)));
        report(cx, "kept");
    }
    if (is("deref")) {
        slots[0] = rt_array_new(cx);
        rt_list_add(cx, slots[0], rt_int(5));
        slots[1] = rt_aref(cx, slots[0]);
        slots[2] = rt_href(cx, rt_hash_new(cx));
        rt_say(cx, rt_elem(cx, rt_deref(cx, slots[1], 0), rt_int(0)));
        rt_say(cx, rt_ref(cx, slots[1]));
        rt_say(cx, rt_ref(cx, slots[2]));
        rt_say(cx, rt_ref(cx, rt_int(1)));
        rt_say(cx, rt_ref(cx, rt_undef()));
        rt_say(cx, rt_bool(rt_is_true(cx, slots[1])));
        rt_say(cx, rt_defined(cx, slots[2]));
        rt_say(cx, rt_num_eq(cx, slots[1], rt_aref(cx, slots[0])));
        rt_say(cx, rt_num_ne(cx, slots[1], slots[2]));
        rt_say(cx, rt_num_eq(cx, slots[1], slots[2]));
    }
    if (is("deref-undef")) rt_deref(cx, rt_undef(), 0);
    if (is("deref-number")) rt_deref(cx, rt_int(5), 1);
    if (is("deref-string")) rt_deref(cx, rt_string(&A), 0);
    if (is("deref-other-kind")) rt_deref(cx, rt_href(cx, rt_hash_new(cx)), 0);
    if (is("deref-other-kind-hash")) {
        slots[0] = rt_array_new(cx);
        rt_deref(cx, rt_aref(cx, slots[0]), 1);
    }
    if (is("deref-container")) rt_deref(cx, rt_array_new(cx), 0);
    if (is("vivify")) {
        // undef made a container, and the variable a reference to it; a
        // reference kept; anything else a fault.
        slots[0] = rt_undef();
        slots[1] = rt_vivify(cx, &slots[0], 1);
        rt_helem_store(cx, slots[1], rt_string(&A), rt_int(3));
        rt_say(cx, rt_ref(cx, slots[0]));
        rt_say(cx, rt_helem(cx, rt_vivify(cx, &slots[0], 1), rt_string(&A)));
        rt_vivify(cx, &slots[0], 0);
    }
    if (is("hop")) {
        // $a[2]{a}[1] = 7 into an empty array: two containers made, and
        // the array grown to three. Then a hop that is there is read.
        slots[0] = rt_array_new(cx);
        slots[1] = rt_elem_hop(cx, slots[0], rt_int(2), 1);
        slots[1] = rt_helem_hop(cx, slots[1], rt_string(&A), 0);
        rt_elem_store(cx, slots[1], rt_int(1), rt_int(7));
        rt_say(cx, rt_count(cx, slots[0]));
        slots[2] = rt_elem_hop(cx, slots[0], rt_int(2), 1);
        slots[2] = rt_helem_hop(cx, slots[2], rt_string(&A), 0);
        rt_say(cx, rt_elem(cx, slots[2], rt_int(1)));
        rt_say(cx, rt_count(cx, slots[2]));
        // A hop through what is there and is not a reference.
        rt_elem_store(cx, slots[0], rt_int(0), rt_string(&A));
        rt_elem_hop(cx, slots[0], rt_int(0), 0);
    }
    if (is("hop-key-made-under-stress")) {
        // A number key is made a string, and then the container: under the
        // stress knob both are collections, and the hash keeps both.
        slots[0] = rt_hash_new(cx);
        rt_value c = rt_helem_hop(cx, slots[0], rt_int(12), 0);
        slots[1] = c;
        rt_elem_store(cx, slots[1], rt_int(0), rt_int(5));
        slots[1] = rt_undef();
        rt_collect(cx);
        rt_say(cx, rt_elem(cx, rt_deref(cx, rt_helem(cx, slots[0], rt_int(12)), 0), rt_int(0)));
    }
    if (is("hop-frozen") || is("hop-frozen-there") || is("hop-frozen-hash")) {
        // A hop that makes is a store, and faults while the container is
        // frozen; one that only reads does not.
        slots[0] = is("hop-frozen-hash") ? rt_hash_new(cx) : rt_array_new(cx);
        if (is("hop-frozen-there")) rt_list_add(cx, slots[0], rt_aref(cx, rt_array_new(cx)));
        rt_freeze(cx, slots[0]);
        if (is("hop-frozen-hash")) rt_helem_hop(cx, slots[0], rt_string(&A), 0);
        else rt_elem_hop(cx, slots[0], rt_int(0), 0);
        printf("read\n");
    }
    if (is("frozen-through")) {
        // A container frozen by the list of a foreach, stored to through a
        // reference: the freeze is the container's (T237).
        slots[0] = rt_array_new(cx);
        rt_list_add(cx, slots[0], rt_int(1));
        slots[1] = rt_aref(cx, slots[0]);
        slots[2] = rt_array_new(cx);
        rt_frozen_add(cx, slots[2], rt_deref(cx, slots[1], 0));
        rt_frozen_add(cx, slots[2], slots[0]);
        rt_freeze_all(cx, slots[2]);
        rt_thaw(cx, slots[0]);
        rt_elem(cx, rt_deref(cx, slots[1], 0), rt_int(0));
        printf("read\n");
        rt_elem_store(cx, rt_deref(cx, slots[1], 0), rt_int(0), rt_int(2));
    }
    if (is("thawed")) {
        slots[0] = rt_hash_new(cx);
        slots[2] = rt_array_new(cx);
        rt_frozen_add(cx, slots[2], slots[0]);
        rt_frozen_add(cx, slots[2], slots[0]);
        rt_freeze_all(cx, slots[2]);
        rt_thaw_all(cx, slots[2]);
        rt_helem_store(cx, slots[0], rt_string(&A), rt_int(1));
        rt_say(cx, rt_hash_count(cx, slots[0]));
        rt_thaw(cx, slots[0]);
    }
    if (strncmp(which, "op-", 3) == 0) {
        slots[0] = rt_array_new(cx);
        slots[1] = rt_aref(cx, slots[0]);
        printf("2\n");
        apply(cx, which + 3, slots[1]);
        printf("not faulted\n");
    }
    rt_leave(cx, &frame);
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "ref.pl");
}
