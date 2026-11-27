// References (step 13a; D107, D112, D114). rt.c includes this file: it is
// a part of the runtime, apart for its subject.
//
// A reference is a value whose payload is a container's block: the very
// block an array's or a hash's variable holds, so `\@a` is that block
// with another tag, and `[ LIST ]` is the list the generated code built,
// which is a new array no one else holds. The collector walks from a
// container to what it holds (rt.c, `rt_collect`), and a container is
// frozen, changed and collected whatever reaches it.
//
// What an arrow reads through is made a container value again, ARRAY or
// HASH, which the element functions of rt.c and hash.c take as they take
// a variable's: so `$r->[0]` is `rt_elem` of `rt_deref` of `$r`.

#define UNDEF_REFERENCE "undef where a reference is wanted"
#define NOT_ARRAY "not a reference to an array"
#define NOT_HASH "not a reference to a hash"

static rt_value container(rt_array *a, int hash) {
    rt_value v;
    v.tag = hash ? RT_TAG_HASH : RT_TAG_ARRAY;
    v.as.a = a;
    return v;
}

rt_value rt_aref(rt_ctx *cx, rt_value array) {
    rt_value v;
    v.tag = RT_TAG_AREF;
    v.as.a = array_of(cx, array);
    return v;
}

rt_value rt_href(rt_ctx *cx, rt_value hash) {
    rt_value v;
    v.tag = RT_TAG_HREF;
    v.as.a = hash_of(cx, hash);
    return v;
}

// Reading through undef, or through anything that is not the reference
// wanted, is a fault (D107): perl makes the container on a read too, the
// variable included (T231), and dies of a string or the other kind of
// reference (T234).
rt_value rt_deref(rt_ctx *cx, rt_value v, int hash) {
    if (v.tag == RT_TAG_UNDEF) rt_fault(cx, UNDEF_REFERENCE);
    if (v.tag != (hash ? RT_TAG_HREF : RT_TAG_AREF)) {
        if (!a_scalar(v.tag)) rt_fault(cx, "not a value");
        rt_fault(cx, hash ? NOT_HASH : NOT_ARRAY);
    }
    if (v.as.a->dead) rt_internal(cx, "a reference to a container that was collected");
    return container(v.as.a, hash);
}

// A new container, empty: the one allocation of the two functions below,
// and the last thing either does before it stores what it made.
static rt_value made_container(rt_ctx *cx, int hash) {
    return hash ? rt_hash_new(cx) : rt_array_new(cx);
}

static rt_value reference_to(rt_value c) {
    rt_value v;
    v.tag = c.tag == RT_TAG_HASH ? RT_TAG_HREF : RT_TAG_AREF;
    v.as.a = c.as.a;
    return v;
}

// A variable stored through (T248): undef is made a new container, as
// perl makes it, and the variable a reference to it. The variable is in a
// slot, and holds undef while the container is made.
rt_value rt_vivify(rt_ctx *cx, rt_value *slot, int hash) {
    if (slot->tag != RT_TAG_UNDEF) return rt_deref(cx, *slot, hash);
    rt_value c = made_container(cx, hash);
    *slot = reference_to(c);
    return c;
}

// One hop of a store: the element of `array` at `index`, made if it is not
// there or undef, and what it points at. Making it is a store to the array,
// so it faults while a foreach is over it (D114); an element that already
// holds the reference wanted is only read, as perl only reads it.
rt_value rt_elem_hop(rt_ctx *cx, rt_value array, rt_value index, int hash) {
    rt_value v = rt_elem(cx, array, index);
    if (v.tag != RT_TAG_UNDEF) return rt_deref(cx, v, hash);
    // (The element is made first, undef, so that what the allocation
    // below may collect is held by nothing that matters.)
    int64_t at = rt_elem_make(cx, array, index);
    rt_value c = made_container(cx, hash);
    rt_elem_put(cx, array, at, reference_to(c));
    return c;
}

// The same for a hash's element. The key, if it is no string, is made one
// as it is stored: an allocation, after which it is in the hash, and only
// then the container is made.
rt_value rt_helem_hop(rt_ctx *cx, rt_value h, rt_value key, int hash) {
    rt_value v = rt_helem(cx, h, key);
    if (v.tag != RT_TAG_UNDEF) return rt_deref(cx, v, hash);
    int64_t pair = rt_helem_make(cx, h, key);
    rt_value c = made_container(cx, hash);
    rt_helem_put(cx, h, pair, reference_to(c));
    return c;
}

static const rt_str STR_ARRAY = { 5, 5, "ARRAY", RT_STR_CONSTANT };
static const rt_str STR_HASH = { 4, 4, "HASH", RT_STR_CONSTANT };

rt_value rt_ref(rt_ctx *cx, rt_value v) {
    if (v.tag == RT_TAG_AREF) return rt_string(&STR_ARRAY);
    if (v.tag == RT_TAG_HREF) return rt_string(&STR_HASH);
    if (!a_scalar(v.tag)) rt_fault(cx, "not a value");
    return rt_string(&STR_FALSE);
}

// The containers to freeze are kept as container values, raw, in a list no
// program sees: it is in a slot, so they are alive while the loop runs.
void rt_frozen_add(rt_ctx *cx, rt_value frozen, rt_value c) {
    if (c.tag != RT_TAG_ARRAY && c.tag != RT_TAG_HASH) rt_internal(cx, "a frozen container is no container");
    append(cx, array_of(cx, frozen), c);
}

void rt_freeze_all(rt_ctx *cx, rt_value frozen) {
    rt_array *a = array_of(cx, frozen);
    for (uint64_t n = 0; n < a->count; n++) rt_freeze(cx, a->items[n]);
}

void rt_thaw_all(rt_ctx *cx, rt_value frozen) {
    rt_array *a = array_of(cx, frozen);
    for (uint64_t n = 0; n < a->count; n++) rt_thaw(cx, a->items[n]);
}
