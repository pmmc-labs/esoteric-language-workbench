// perl's merge sort, as a machine that asks (step 10c; D82, D83).
//
// **Where this came from, for whoever settles the repository's licence
// (D82).** The algorithm in `rt_sort_next`, its two thresholds, and the
// order of every comparison it makes are those of `dynprep` and
// `S_sortsv_flags_impl` in pp_sort.c of perl 5.42.0: a binary merge with
// natural runs, by Peter McIlroy ("Optimistic Sorting and Information
// Theoretic Complexity", SODA 1993), written with the BSD Computer Systems
// Research Group at Berkeley, and fitted to perl by John P. Linderman.
// perl says of that file that it "can be distributed under the same terms
// as Perl itself", which are the Artistic License or the GNU General
// Public License. This file is a port of it, statement for statement, and
// so a work derived from it; it is kept apart from the rest of the runtime
// so that it can be found, and dealt with, whole. It is part of rt.c's
// translation unit, which includes it.
//
// **Why a port.** A program can see the order a sort compares in: by a
// block that prints or counts, by one that is no consistent order, by a
// fault only some pairs reach (T3, T173). So every comparison here is the
// one perl makes, in perl's order.
//
// **Why a machine.** perl's sort calls the block. Here the generated code
// drives (D83): `rt_sort_next` runs the merge as far as its next
// comparison, hands back the two values and returns; the generated C runs
// the block where it stands and hands the answer to `rt_sort_answer`; and
// `rt_sort_next` takes up where it left off. So the runtime calls no
// generated code, and none of its C frames is on the stack while a block
// runs. In C that is the merge with every variable in a struct and a
// `switch` on where it was: each `ASK` is a place it returns from and
// comes back into, in the middle of whatever loops it is in.
//
// perl keeps two arrays, the list and one beside it, and writes into each
// both the things being sorted and, at the start of each run, where that
// run ends (its `NEXT`). Here the two are arrays of indexes: a thing is
// its place in the list as it was given, and a pointer into one array and
// the same offset into the other are one number. No value is held here:
// the list is in a slot of the program's, and is not changed until the
// sort is over. t/models/merge.py is the same port in Python, and both are
// held to perl by a block that logs every pair it is given.

#define SORT_PTHRESH 8      // pairs with one sense before a run is looked for
#define SORT_RTHRESH 6      // low in a row before a merge steps by doubling

struct rt_sort {
    struct rt_sort *outer;      // the sort this one is inside: a block may sort
    rt_array *list;             // what is being sorted: not changed until the end
    int64_t n;
    int lone;                   // a list of one value is looked at, as perl looks at it (T190)
    int where;                  // which ASK to come back to; 0 at the start
    int64_t answer;             // what the last comparison gave
    int64_t *cells[3];          // base, aux, base: perl's `which`
    int64_t *list1, *list2;
    // dynprep's
    int64_t b, p, q, t, r, last, p2, savep, runs;
    int sense;
    // the merge's
    int64_t offset, f1, f2, l1, l2, tp2, p1, i, run;
    int level, sp;
    struct { int64_t offset, runs; } stack[60];
};

// The block's value, as perl takes it: a whole number, cut toward zero,
// and then only its sign. perl cuts it to 32 bits as well, so that 2^32 is
// "equal" and 2^31 "less" (T173): there it is a fault.
void rt_sort_answer(rt_ctx *cx, rt_sort *s, rt_value v) {
    int64_t n = whole_of(cx, v);
    if (n < INT32_MIN || n > INT32_MAX) rt_fault(cx, "a sort block's value is outside 32 bits, where perl wraps it");
    s->answer = n;
}

rt_sort *rt_sort_begin(rt_ctx *cx, rt_value list, int lone) {
    rt_array *a = array_of(cx, list);
    rt_sort *s = malloc(sizeof *s);
    int64_t *cells = a->count > 1 ? malloc(2 * a->count * sizeof *cells) : NULL;
    if (s == NULL || (a->count > 1 && cells == NULL)) {
        free(s);
        free(cells);
        rt_fault(cx, "out of memory");
    }
    s->outer = cx->sorts;
    cx->sorts = s;
    s->list = a;
    s->n = (int64_t)a->count;
    s->lone = lone;
    s->where = 0;
    s->answer = 0;
    s->cells[0] = s->cells[2] = cells;
    s->cells[1] = cells == NULL ? NULL : cells + a->count;
    for (int64_t k = 0; k < s->n && cells != NULL; k++) cells[k] = k;
    return s;
}

// The sort is over: its values, in order, added to `into`, and its
// memory given back.
void rt_sort_end(rt_ctx *cx, rt_sort *s, rt_value into) {
    if (cx->sorts != s) rt_internal(cx, "a sort ended that was not the newest");
    rt_array *to = array_of(cx, into);
    rt_array *from = s->list;
    if (from->dead || from->count != (uint64_t)s->n) rt_internal(cx, "a list changed while it was sorted");
    reserve(cx, to, to->count + from->count);
    for (int64_t k = 0; k < s->n; k++) to->items[to->count++] = from->items[s->cells[0] == NULL ? k : s->cells[0][k]];
    cx->sorts = s->outer;
    free(s->cells[0]);
    free(s);
}

// Every sort that a fault left open: the program is stopping.
static void sorts_release(rt_ctx *cx) {
    while (cx->sorts != NULL) {
        rt_sort *s = cx->sorts;
        cx->sorts = s->outer;
        free(s->cells[0]);
        free(s);
    }
}

// Compare the things at X and Y: hand them back, and come back here with
// the answer.
#define ASK(X, Y, N) \
    do { \
        s->where = N; \
        *a = s->list->items[X]; \
        *b = s->list->items[Y]; \
        return 1; \
        case N:; \
    } while (0)

// As far as the next comparison: 1, with the two values to compare, or 0
// when the list is sorted.
int rt_sort_next(rt_ctx *cx, rt_sort *s, rt_value *a, rt_value *b) {
    if (cx->sorts != s) rt_internal(cx, "a sort was taken up that was not the newest");
    int64_t *base = s->cells[0];
    int64_t *aux = s->cells[1];
    switch (s->where) {
    case 0:
        if (s->n <= 1) {
            // perl turns every value of such a sort to a number or a
            // string before it sorts, and so looks at a lone one.
            if (s->n == 1 && s->lone) {
                s->where = 1;
                *a = s->list->items[0];
                *b = s->list->items[0];
                return 1;
            }
            return 0;
        }
        // ---- dynprep: find the runs. Pairs, and longer ones where eight
        // pairs agree; a run that goes down is turned round.
        s->runs = 0;
        s->b = 0;
        s->last = s->n;
        ASK(base[s->b], base[s->b + 1], 2);
        s->sense = s->answer > 0;
        s->p2 = 0;
        while (s->b < s->last) {
            // We just started, or just reversed sense: t at the end of
            // the pairs with the prevailing sense.
            s->p = s->b + 2;
            s->t = s->p;
            for (;;) {
                s->p += 1;
                if (!(s->p < s->last)) break;
                ASK(base[s->t], base[s->p], 3);
                if ((s->answer > 0) != s->sense) break;
                s->p += 1;
                s->t = s->p;
            }
            s->q = s->b;
            do {
                s->p = s->r = s->b + 2 * SORT_PTHRESH;
                if (s->r >= s->t) {
                    s->p = s->r = s->t;         // too short to care about
                } else {
                    for (;;) {
                        ASK(base[s->p - 1], base[s->p], 4);
                        if ((s->answer > 0) != s->sense) break;
                        s->p -= 2;
                        if (!(s->p > s->q)) break;
                    }
                    if (s->p <= s->q) {
                        // b through r is a long run: as far as it goes.
                        s->p = s->q = s->r;
                        for (;;) {
                            s->p += 2;
                            if (!(s->p < s->t)) break;
                            ASK(base[s->p - 1], base[s->p], 5);
                            if ((s->answer > 0) != s->sense) break;
                            s->q = s->p;
                        }
                        s->r = s->p = s->q + 2;
                    }
                }
                if (s->q > s->b) {              // a run of more than 2 at b
                    s->savep = s->p;
                    s->q += 2;
                    s->p = s->q;
                    // pick up a singleton, if possible
                    if (s->p == s->t && s->t + 1 == s->last) {
                        ASK(base[s->p - 1], base[s->p], 6);
                        if ((s->answer > 0) == s->sense) s->savep = s->r = s->p = s->q = s->last;
                    }
                    aux[s->p2] = s->p2 + (s->p - s->b);
                    s->p2 = aux[s->p2];
                    s->runs += 1;
                    if (s->sense) {
                        for (;;) {
                            s->p -= 1;
                            if (!(s->b < s->p)) break;
                            int64_t c = base[s->b];
                            base[s->b] = base[s->p];
                            base[s->p] = c;
                            s->b += 1;
                        }
                    }
                    s->p = s->savep;
                }
                while (s->q < s->p) {           // simple pairs
                    aux[s->p2] = s->p2 + 2;
                    s->p2 = aux[s->p2];
                    s->runs += 1;
                    if (s->sense) {
                        int64_t c = base[s->q];
                        base[s->q] = base[s->q + 1];
                        base[s->q + 1] = c;
                    }
                    s->q += 2;
                }
                s->b = s->p;
                if (s->b == s->t && s->t + 1 == s->last) {
                    aux[s->p2] = s->p2 + 1;
                    s->runs += 1;
                    s->b += 1;
                }
                s->q = s->r;
            } while (s->b < s->t);
            s->sense = !s->sense;
        }
        // ---- the merge
        s->level = 0;
        s->sp = 0;
        s->stack[0].runs = s->runs;
        s->stack[0].offset = s->offset = 0;
        for (;;) {
            s->runs = s->stack[s->sp].runs;
            if (s->runs == 0) {
                // Both runs of this level are made: merge them, and go
                // up, for as long as that is so.
                s->list1 = s->cells[s->level & 1];          // where the runs are now
                s->list2 = s->cells[(s->level & 1) + 1];    // where the merged run goes
                do {
                    s->offset = s->stack[s->sp].offset;
                    s->f1 = s->p1 = s->offset;              // the first run
                    s->tp2 = s->offset;                     // where the merged run goes
                    s->t = s->list2[s->offset];             // where the first run ends
                    s->f2 = s->l1 = s->t;
                    s->t = s->list2[s->t];                  // where the second ends
                    s->l2 = s->t;
                    s->offset = s->t;
                    while (s->f1 < s->l1 && s->f2 < s->l2) {
                        // q is the head that goes second: all of the other
                        // run that is strictly lower goes before it. Equal
                        // counts as high when q is from the second run and
                        // as low when it is from the first, which keeps
                        // the sort stable.
                        ASK(s->list1[s->f1], s->list1[s->f2], 7);
                        if (s->answer <= 0) {
                            s->q = s->f2;
                            s->b = s->f1;
                            s->t = s->l1;
                            s->sense = -1;
                        } else {
                            s->q = s->f1;
                            s->b = s->f2;
                            s->t = s->l2;
                            s->sense = 0;
                        }
                        // ramp up: t at something strictly above q (or the
                        // end), b at something strictly below it
                        s->i = 1;
                        s->run = 0;
                        for (;;) {
                            s->p = s->b + s->i;
                            if (s->p >= s->t) {
                                s->p = s->t - 1;
                                if (s->p > s->b) {
                                    ASK(s->list1[s->q], s->list1[s->p], 8);
                                    if (s->answer <= s->sense) s->t = s->p;
                                    else s->b = s->p;
                                } else {
                                    s->b = s->p;
                                }
                                break;
                            }
                            ASK(s->list1[s->q], s->list1[s->p], 9);
                            if (s->answer <= s->sense) {
                                s->t = s->p;
                                break;
                            }
                            s->b = s->p;
                            s->run += 1;
                            if (s->run >= SORT_RTHRESH) s->i += s->i;
                        }
                        // q follows b and goes before t: a binary search
                        // of what is between, rounding down
                        s->b += 1;
                        while (s->b < s->t) {
                            s->p = s->b + (s->t - s->b - 1) / 2;
                            ASK(s->list1[s->q], s->list1[s->p], 10);
                            if (s->answer <= s->sense) s->t = s->p;
                            else s->b = s->p + 1;
                        }
                        // copy all the strictly low ones, then q
                        if (s->q == s->f1) {
                            do s->list2[s->tp2++] = s->list1[s->f2++]; while (s->f2 < s->t);
                            s->list2[s->tp2++] = s->list1[s->f1++];
                        } else {
                            do s->list2[s->tp2++] = s->list1[s->f1++]; while (s->f1 < s->t);
                            s->list2[s->tp2++] = s->list1[s->f2++];
                        }
                    }
                    // run out the list that is left
                    if (s->f1 == s->l1) {
                        while (s->f2 < s->l2) s->list2[s->tp2++] = s->list1[s->f2++];
                    } else {
                        do s->list2[s->tp2++] = s->list1[s->f1++]; while (s->f1 < s->l1);
                    }
                    s->list1[s->p1] = s->tp2;
                    s->level -= 1;
                    if (s->level == 0) return 0;
                    s->sp -= 1;
                    {
                        int64_t *swap = s->list1;
                        s->list1 = s->list2;
                        s->list2 = swap;
                    }
                    s->runs = s->stack[s->sp].runs;
                } while (s->runs == 0);
            }
            s->stack[s->sp].runs = 0;           // this run will finish the level
            // More than 2 runs: make them 2, each of about half, the
            // second half stacked for later.
            while (s->runs > 2) {
                s->level += 1;
                s->sp += 1;
                s->stack[s->sp].offset = s->offset;
                s->stack[s->sp].runs = s->runs / 2;
                s->runs -= s->runs / 2;
            }
            if (s->runs == 1) {
                // One run from one run: copied to where it belongs, if it
                // is not there.
                if (s->level & 1) {
                    s->f1 = s->b = s->offset;
                    s->f2 = s->offset;
                    s->t = aux[s->f2];
                    s->offset = s->t;
                    do aux[s->f2++] = base[s->f1++]; while (s->f1 < s->t);
                    base[s->b] = s->t;
                } else if (s->level == 0) {
                    return 0;
                }
            } else {
                // One run from two: the merge above does it, from the
                // other array.
                int belongs = s->level & 1;
                s->level += 1;
                s->sp += 1;
                s->stack[s->sp].offset = s->offset;
                s->stack[s->sp].runs = 0;
                if (!belongs) {
                    s->f1 = s->b = s->offset;
                    s->f2 = s->offset;
                    s->t = aux[s->f2];
                    s->offset = s->t;
                    s->p = s->offset;
                    s->t = aux[s->t];
                    do aux[s->f2++] = base[s->f1++]; while (s->f1 < s->t);
                    base[s->b] = s->p;
                    base[s->p] = s->t;
                }
            }
        }
    case 1:
        return 0;
    default:
        rt_internal(cx, "a sort has lost its place");
    }
    return 0;
}

#undef ASK

// `sort LIST`, with no block: by string, as `cmp` orders. perl makes every
// value a string before it sorts, so each is looked at, a lone one too.
void rt_sort_strings(rt_ctx *cx, rt_value list, rt_value into) {
    rt_array *given = array_of(cx, list);
    for (uint64_t k = 0; k < given->count; k++) {
        scratch x;
        to_str(cx, given->items[k], &x);
    }
    rt_sort *s = rt_sort_begin(cx, list, 0);
    rt_value a, b;
    while (rt_sort_next(cx, s, &a, &b)) rt_sort_answer(cx, s, rt_str_cmp(cx, a, b));
    rt_sort_end(cx, s, into);
}

// perl sorts `@a = sort BLOCK @a` in place, and drops every element that
// was never stored; whether one was is a past of the array's that is not
// kept here (T187, D87).
void rt_sort_in_place(rt_ctx *cx, rt_value list) {
    rt_array *a = array_of(cx, list);
    for (uint64_t k = 0; k < a->count; k++) {
        if (a->items[k].tag == RT_TAG_UNDEF) rt_fault(cx, "an undef in an array sorted in place: perl drops an element that was never stored");
    }
}
