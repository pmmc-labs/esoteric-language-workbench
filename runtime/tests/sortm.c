// The sort machine (step 10c), driven as generated code drives it: lists
// of whole numbers on standard input, one a line after a letter that says
// how to compare, and for each the values sorted and every pair that was
// compared, in order. rt.test.ts holds what this prints to perl's own.
// `stop` as the one argument: the machine is left in the middle of a sort,
// and a fault there gives its memory back.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include "rt.h"

static const char *which;

// perl's `%`, which is never below zero for a divisor above it (C's is).
static int64_t mod(int64_t x, int64_t m) {
    return ((x % m) + m) % m;
}

static int64_t compare(char how, int64_t a, int64_t b) {
    switch (how) {
    case 'n': return (a > b) - (a < b);
    case 'r': return (b > a) - (b < a);
    // No order at all: a table of the two values.
    case 'm': return mod(a * 7 + b * 13, 3) - 1;
    // Many equal keys among different values.
    default: return (mod(a, 10) > mod(b, 10)) - (mod(a, 10) < mod(b, 10));
    }
}

static void body(rt_ctx *cx) {
    rt_value slots[4];
    rt_frame frame;
    rt_enter(cx, &frame, slots, 4);
    cx->line = 1;
    static char line[1 << 16];
    while (fgets(line, sizeof line, stdin) != NULL) {
        char how = line[0];
        slots[0] = rt_array_new(cx);
        slots[1] = rt_array_new(cx);
        for (char *at = line + 1; *at == ' ';) rt_list_add(cx, slots[0], rt_int(strtoll(at + 1, &at, 10)));
        rt_sort *s = rt_sort_begin(cx, slots[0], 0);
        int asked = 0;
        while (rt_sort_next(cx, s, &slots[2], &slots[3])) {
            if (asked++ == 3 && strcmp(which, "stop") == 0) rt_sort_answer(cx, s, rt_undef());
            // A sort in the block of a sort: the outer one is where it was.
            if (how == 'k' && asked % 5 == 0) {
                rt_value inner = rt_array_new(cx);
                rt_sort *t = rt_sort_begin(cx, slots[0], 0);
                rt_value x, y;
                while (rt_sort_next(cx, t, &x, &y)) rt_sort_answer(cx, t, rt_int(compare('n', x.as.i, y.as.i)));
                rt_sort_end(cx, t, inner);
            }
            printf("%s%" PRId64 ",%" PRId64, asked == 1 ? "|" : " ", slots[2].as.i, slots[3].as.i);
            rt_sort_answer(cx, s, rt_int(compare(how, slots[2].as.i, slots[3].as.i)));
        }
        rt_sort_end(cx, s, slots[1]);
        if (asked == 0) printf("|");
        printf("\n");
        for (int64_t k = 0; k < rt_list_length(cx, slots[1]); k++) printf("%s%" PRId64, k ? " " : "", rt_list_items(cx, slots[1])[k].as.i);
        printf("\n");
    }
    rt_leave(cx, &frame);
}

int main(int argc, char **argv) {
    which = argc > 1 ? argv[1] : "";
    return rt_run(body, "sortm.pl");
}
