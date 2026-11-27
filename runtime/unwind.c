// `die`, `try` and `catch` (step 15; D141, D142), and `warn` (15b). A
// file of its own, which rt.c includes, as it does sort.c and hash.c.
//
// **How a `die` unwinds (D141).** Everything a `die` must put back is in
// the context: the frames that are open (D66), the sorts under way
// (sort.c), and the freezes, which are a stack here, one entry a freeze,
// beside the count on each container. A `try` writes down how far each of
// the three goes and `setjmp`s, in the generated code, since the jump has
// to come back into the function the `try` is in. A `die` gives back
// every freeze above the mark, frees every sort above it, drops the
// frames above it, and `longjmp`s. The runtime calls no generated code
// (D83), so no C frame of the runtime's is between the `die` and the
// `try` but `rt_throw`'s own.
//
// The value thrown is handed over in the context, not in the `try`'s
// record: a C local changed between `setjmp` and `longjmp` is
// indeterminate to C. Between the jump and the catch's variable there is
// no allocation, so the collector need not see it there.
//
// `return`, `last` and `next` leave a `try` by a `goto` and close it with
// `rt_try_end` on the way: they are not a `die`.

// The freezes, as they are made and given back. A loop gives back what
// it froze in the order it froze it, so the entry given back is looked
// for from the top.
static void unwind_frozen(rt_ctx *cx, rt_array *a) {
    if (cx->frozen_count == cx->frozen_room) {
        uint64_t room = cx->frozen_room ? 2 * cx->frozen_room : 16;
        rt_array **grown = realloc(cx->frozen, room * sizeof *grown);
        if (grown == NULL) rt_fault(cx, "out of memory");
        cx->frozen = grown;
        cx->frozen_room = room;
    }
    cx->frozen[cx->frozen_count++] = a;
}

static void unwind_thawed(rt_ctx *cx, rt_array *a) {
    for (uint64_t k = cx->frozen_count; k > 0; k--) {
        if (cx->frozen[k - 1] != a) continue;
        memmove(&cx->frozen[k - 1], &cx->frozen[k], (cx->frozen_count - k) * sizeof *cx->frozen);
        cx->frozen_count -= 1;
        return;
    }
    rt_internal(cx, "a freeze was given back that was never made");
}

static void unwind_release(rt_ctx *cx) {
    free(cx->frozen);
    cx->frozen = NULL;
    cx->frozen_count = cx->frozen_room = 0;
}

void rt_try_begin(rt_ctx *cx, rt_try *t) {
    t->outer = cx->tries;
    t->frames = cx->frames;
    t->deep = cx->deep;
    t->sorts = cx->sorts;
    t->frozen = cx->frozen_count;
    cx->tries = t;
}

void rt_try_end(rt_ctx *cx, rt_try *t) {
    if (cx->tries != t) rt_internal(cx, "a try was closed that is not the newest");
    cx->tries = t->outer;
}

rt_value rt_caught(rt_ctx *cx) {
    rt_value v = cx->thrown;
    cx->thrown = rt_undef();
    return v;
}

// A message, as stderr is written to (D148): the checks `say` makes, then
// the bytes. stdout first, so that what the program printed comes first
// wherever the two streams meet.
static void to_stderr(rt_ctx *cx, rt_value message) {
    emit_checked(cx, message, 0, 0);
    scratch none;
    const rt_str *s = to_str(cx, message, &none);
    fflush(stdout);
    fwrite(s->bytes, 1, s->len, stderr);
    fflush(stderr);
}

void rt_throw(rt_ctx *cx, rt_value v) {
    rt_try *t = cx->tries;
    if (t == NULL) {
        // perl exits with errno when it is set, and a number that
        // underflowed set it (T319, D151): the language keeps no errno.
        if (cx->underflowed) rt_fault(cx, "an uncaught die after a number underflowed: perl exits with the status of $! there, which the language does not keep");
        if (v.tag == RT_TAG_AREF || v.tag == RT_TAG_HREF) rt_fault(cx, "a reference where a string is wanted");
        // Uncaught: the message on stderr, and 255 (D12).
        to_stderr(cx, v);
        release(cx);
        exit(255);
    }
    while (cx->frozen_count > t->frozen) {
        rt_array *a = cx->frozen[--cx->frozen_count];
        if (a->frozen == 0) rt_internal(cx, "a die gave back a freeze that was not held");
        a->frozen -= 1;
    }
    sorts_release_to(cx, t->sorts);
    cx->frames = t->frames;
    cx->deep = t->deep;
    cx->tries = t->outer;
    cx->thrown = v;
    longjmp(t->jump, 1);
}

// The message of a `die` or a `warn`, as perl makes it (D142, T300,
// T301): the values joined with nothing between, each made a string as
// `.` makes one; `empty` for an empty message; and ` at FILE line N.` and
// a newline when it does not end in one. One allocation, last.
static rt_value message(rt_ctx *cx, rt_value list, const char *empty) {
    rt_array *a = array_of(cx, list);
    scratch x;
    uint64_t len = 0, chars = 0;
    for (uint64_t n = 0; n < a->count; n++) {
        rt_value v = a->items[n];
        // A reference among the values would be its address to perl (D112).
        if (v.tag == RT_TAG_AREF || v.tag == RT_TAG_HREF) rt_fault(cx, "a reference where a string is wanted");
        if (v.tag < RT_TAG_INT || v.tag > RT_TAG_BOOL) rt_internal(cx, "a die or a warn was handed what is not a value");
        const rt_str *s = to_str(cx, v, &x);
        len += s->len;
        chars += s->chars;
        if (chars > (uint64_t)INT32_MAX) rt_fault(cx, "joined string too long");
    }
    const char *head = len == 0 ? empty : "";
    uint64_t headlen = strlen(head);
    // The last value that is not empty says whether the message ends in a
    // newline.
    int newline = 0;
    for (uint64_t n = a->count; n > 0; n--) {
        const rt_str *s = to_str(cx, a->items[n - 1], &x);
        if (s->len == 0) continue;
        newline = s->bytes[s->len - 1] == '\n';
        break;
    }
    char tail[64];
    int taillen = newline ? 0 : snprintf(tail, sizeof tail, " line %" PRId64 ".\n", cx->line);
    uint64_t filelen = newline ? 0 : strlen(cx->file) + 4;
    uint64_t filechars = 0;
    if (!newline) {
        for (const char *p = cx->file; *p; p++) filechars += !continues(*p);
        filechars += 4;
    }
    char *bytes;
    const rt_str *made = str_new(cx, headlen + len + filelen + (uint64_t)taillen, headlen + chars + filechars + (uint64_t)taillen, &bytes);
    memcpy(bytes, head, headlen);
    bytes += headlen;
    for (uint64_t n = 0; n < a->count; n++) {
        const rt_str *s = to_str(cx, a->items[n], &x);
        alive(cx, s);
        memcpy(bytes, s->bytes, s->len);
        bytes += s->len;
    }
    if (!newline) {
        memcpy(bytes, " at ", 4);
        memcpy(bytes + 4, cx->file, filelen - 4);
        memcpy(bytes + filelen, tail, (size_t)taillen);
    }
    return rt_string(made);
}

void rt_die(rt_ctx *cx, rt_value list) {
    // One value that is a reference is thrown as itself, as perl throws it
    // (D142): a `catch` gets the container. Uncaught, perl writes its
    // address, which is D112's fault (`rt_throw`).
    rt_array *a = array_of(cx, list);
    if (a->count == 1 && (a->items[0].tag == RT_TAG_AREF || a->items[0].tag == RT_TAG_HREF)) rt_throw(cx, a->items[0]);
    rt_throw(cx, message(cx, list, "Died"));
}

rt_value rt_warn(rt_ctx *cx, rt_value list) {
    to_stderr(cx, message(cx, list, "Warning: something's wrong"));
    return rt_bool(1);
}

// `say STDERR LIST` and `print STDERR LIST` (15b): every value looked at
// before any is written, as `say` does.
static void emit_list_err(rt_ctx *cx, rt_value list, int newline) {
    rt_array *a = array_of(cx, list);
    for (uint64_t n = 0; n < a->count; n++) emit_checked(cx, a->items[n], 0, 0);
    fflush(stdout);
    for (uint64_t n = 0; n < a->count; n++) {
        char buf[32];
        rt_value v = a->items[n];
        if (v.tag == RT_TAG_INT || v.tag == RT_TAG_NUM) {
            int k = format_number(cx, v, buf);
            fwrite(buf, 1, (size_t)k, stderr);
        } else {
            scratch none;
            const rt_str *s = to_str(cx, v, &none);
            fwrite(s->bytes, 1, s->len, stderr);
        }
    }
    if (newline) putc('\n', stderr);
    fflush(stderr);
}

void rt_say_err_list(rt_ctx *cx, rt_value list) {
    emit_list_err(cx, list, 1);
}

void rt_print_err_list(rt_ctx *cx, rt_value list) {
    emit_list_err(cx, list, 0);
}
