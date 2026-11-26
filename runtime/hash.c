// Hashes (step 12; D27). rt.c includes this file: it is a part of the
// runtime, apart for its size.
//
// A hash is the block an array is, with another tag: its storage holds a
// key and its value by turns, in the order the keys were first stored
// (D27), so that the collector marks and frees a hash exactly as it does
// an array, and a hash where a list is wanted is its storage, copied.
// Over the storage is an index, by the key's bytes: `slots` numbers, each
// 0 for empty or one more than the number of a pair, probed in a line.
// A deleted pair is a hole, its key ABSENT, which the index still points
// at and every reader steps over; the holes are closed, and the index
// made again, when the index fills or more than half the pairs are holes.
// So the number of a pair holds until a key is added or deleted.
//
// A key is a Str. One made from a number or a boolean is allocated as the
// key is stored, and that is the only allocation here: the hash, and the
// list its values come from, are in slots as it happens.

static rt_array *hash_of(rt_ctx *cx, rt_value v) {
    if (v.tag != RT_TAG_HASH) rt_fault(cx, "not a hash");
    if (v.as.a->dead) rt_internal(cx, "a hash was used after it was collected");
    return v.as.a;
}

static rt_array *hash_changing(rt_ctx *cx, rt_value v) {
    rt_array *h = hash_of(cx, v);
    if (h->frozen != 0) rt_fault(cx, "a hash was changed while a foreach is over it");
    return h;
}

rt_value rt_hash_new(rt_ctx *cx) {
    rt_value v = rt_array_new(cx);
    v.tag = RT_TAG_HASH;
    return v;
}

// FNV-1a, over the key's bytes. No seed: the order of a hash is the order
// its keys were stored in, whatever this gives (D27).
static uint64_t hash_bytes(const rt_str *s) {
    uint64_t h = UINT64_C(14695981039346656037);
    for (uint64_t k = 0; k < s->len; k++) h = (h ^ (unsigned char)s->bytes[k]) * UINT64_C(1099511628211);
    return h;
}

static int same_key(const rt_str *a, const rt_str *b) {
    return a->len == b->len && (a->len == 0 || memcmp(a->bytes, b->bytes, a->len) == 0);
}

// The number of the pair with this key, or -1.
static int64_t hash_find(rt_ctx *cx, const rt_array *h, const rt_str *key) {
    if (h->slots == 0) return -1;
    for (uint64_t at = hash_bytes(key) & (h->slots - 1); ; at = (at + 1) & (h->slots - 1)) {
        uint32_t pair = h->index[at];
        if (pair == 0) return -1;
        const rt_value k = h->items[2 * (uint64_t)(pair - 1)];
        if (k.tag == RT_TAG_ABSENT) continue;
        if (k.tag != RT_TAG_STR) rt_internal(cx, "a hash's key is not a string");
        // (A key is read as every string is: one that was collected,
        // because its hash was in no slot, stops the program here.)
        alive(cx, k.as.s);
        if (same_key(k.as.s, key)) return (int64_t)(pair - 1);
    }
}

static void index_add(rt_array *h, uint64_t pair) {
    uint64_t at = hash_bytes(h->items[2 * pair].as.s) & (h->slots - 1);
    while (h->index[at] != 0) at = (at + 1) & (h->slots - 1);
    h->index[at] = (uint32_t)(pair + 1);
}

// The holes closed, and the index made again for the pairs there are and
// `more` to come: at most half full. Counted against the cap as the
// storage is, and starting no collection.
static void hash_index(rt_ctx *cx, rt_array *h, uint64_t more) {
    uint64_t pairs = 0;
    for (uint64_t k = 0; k < h->count; k += 2) {
        if (h->items[k].tag == RT_TAG_ABSENT) continue;
        h->items[2 * pairs] = h->items[k];
        h->items[2 * pairs + 1] = h->items[k + 1];
        pairs += 1;
    }
    h->count = 2 * pairs;
    h->gone = 0;
    uint64_t slots = 8;
    while (slots < 2 * (pairs + more)) slots *= 2;
    if (slots != h->slots) {
        uint64_t was = h->slots * sizeof(uint32_t), now = slots * sizeof(uint32_t);
        if (now > was && cx->cap != 0 && (now - was > cx->cap || cx->held > cx->cap - (now - was))) rt_fault(cx, "out of memory");
        uint32_t *index = realloc(h->index, now);
        if (index == NULL) rt_fault(cx, "out of memory");
        h->index = index;
        h->slots = slots;
        cx->held = cx->held - was + now;
        if (now > was) cx->since += now - was;
        ((rt_block *)h - 1)->size = ((rt_block *)h - 1)->size - was + now;
    }
    memset(h->index, 0, h->slots * sizeof(uint32_t));
    for (uint64_t pair = 0; pair < pairs; pair++) index_add(h, pair);
}

// The pair with this key, made if it is not there, with an undef for its
// value: its number. The one place a key is added.
static int64_t hash_make(rt_ctx *cx, rt_value hash, rt_value key) {
    scratch number;
    rt_array *h = hash_of(cx, hash);
    int64_t found = hash_find(cx, h, to_str(cx, key, &number));
    if (found >= 0) return found;
    hash_changing(cx, hash);
    if (h->count / 2 >= ARRAY_MAX / 2) rt_fault(cx, "hash too large");
    // A key that is no Str is made one: the allocation, after which
    // nothing here is held but what is in a slot.
    rt_value k = key.tag == RT_TAG_STR ? key : rt_concat(cx, key, rt_string(&STR_FALSE));
    if (2 * (h->count / 2 + 1) > h->slots) hash_index(cx, h, 1);
    reserve(cx, h, h->count + 2);
    uint64_t pair = h->count / 2;
    h->items[h->count++] = k;
    h->items[h->count++] = rt_undef();
    index_add(h, pair);
    return (int64_t)pair;
}

rt_value rt_helem(rt_ctx *cx, rt_value hash, rt_value key) {
    scratch number;
    rt_array *h = hash_of(cx, hash);
    int64_t pair = hash_find(cx, h, to_str(cx, key, &number));
    return pair < 0 ? rt_undef() : h->items[2 * pair + 1];
}

int64_t rt_helem_make(rt_ctx *cx, rt_value hash, rt_value key) {
    hash_changing(cx, hash);
    return hash_make(cx, hash, key);
}

// The pair a key was made at: there still, or the generated code let a
// key be added or deleted between making it and using it (D76).
static rt_array *made(rt_ctx *cx, rt_value hash, int64_t pair) {
    rt_array *h = hash_of(cx, hash);
    if (pair < 0 || (uint64_t)pair >= h->count / 2 || h->items[2 * pair].tag != RT_TAG_STR) rt_internal(cx, "a key that was made is not there");
    return h;
}

rt_value rt_helem_get(rt_ctx *cx, rt_value hash, int64_t pair) {
    rt_array *h = made(cx, hash, pair);
    return h->items[2 * pair + 1];
}

rt_value rt_helem_put(rt_ctx *cx, rt_value hash, int64_t pair, rt_value v) {
    rt_array *h = made(cx, hash, pair);
    h->items[2 * pair + 1] = scalar(cx, v);
    return v;
}

rt_value rt_helem_store(rt_ctx *cx, rt_value hash, rt_value key, rt_value v) {
    return rt_helem_put(cx, hash, rt_helem_make(cx, hash, key), v);
}

rt_value rt_hash_exists(rt_ctx *cx, rt_value hash, rt_value key) {
    scratch number;
    rt_array *h = hash_of(cx, hash);
    return rt_bool(hash_find(cx, h, to_str(cx, key, &number)) >= 0);
}

// The value that was at the key, or undef; and the pair is a hole.
rt_value rt_hash_delete(rt_ctx *cx, rt_value hash, rt_value key) {
    scratch number;
    rt_array *h = hash_of(cx, hash);
    int64_t pair = hash_find(cx, h, to_str(cx, key, &number));
    if (pair < 0) return rt_undef();
    hash_changing(cx, hash);
    rt_value was = h->items[2 * pair + 1];
    h->items[2 * pair].tag = RT_TAG_ABSENT;
    h->items[2 * pair + 1] = rt_undef();
    h->gone += 1;
    if (h->gone > h->count / 4) hash_index(cx, h, 0);
    return was;
}

rt_value rt_hash_count(rt_ctx *cx, rt_value hash) {
    rt_array *h = hash_of(cx, hash);
    return rt_int((int64_t)(h->count / 2 - h->gone));
}

// What a hash is where a list is wanted: `step` 1 and `from` 0 for its
// keys and values by turns, 2 and 0 for its keys, 2 and 1 for its values.
static void add_from(rt_ctx *cx, rt_value list, rt_value hash, uint64_t from, uint64_t step) {
    rt_array *to = array_of(cx, list);
    rt_array *h = hash_of(cx, hash);
    reserve(cx, to, to->count + h->count);
    for (uint64_t k = 0; k < h->count; k += 2) {
        if (h->items[k].tag == RT_TAG_ABSENT) continue;
        if (step == 1 || from == 0) to->items[to->count++] = h->items[k];
        if (step == 1 || from == 1) to->items[to->count++] = h->items[k + 1];
    }
}

void rt_list_add_pairs(rt_ctx *cx, rt_value list, rt_value hash) {
    add_from(cx, list, hash, 0, 1);
}

void rt_list_add_keys(rt_ctx *cx, rt_value list, rt_value hash) {
    add_from(cx, list, hash, 0, 2);
}

void rt_list_add_values(rt_ctx *cx, rt_value list, rt_value hash) {
    add_from(cx, list, hash, 1, 2);
}

// `%h = LIST`, from the list's value `n` on: keys and values by turns, a
// key given twice keeping its first place and its last value. An odd
// number of them is a fault: perl warns, and leaves the last key with no
// value (T219).
void rt_hash_rest(rt_ctx *cx, rt_value hash, rt_value list, int64_t n) {
    rt_array *h = hash_changing(cx, hash);
    rt_array *from = array_of(cx, list);
    uint64_t first = (uint64_t)n < from->count ? (uint64_t)n : from->count;
    if ((from->count - first) % 2 != 0) rt_fault(cx, "an odd number of values for a hash");
    h->count = 0;
    h->gone = 0;
    hash_index(cx, h, (from->count - first) / 2);
    for (uint64_t k = first; k < from->count; k += 2) {
        // (The list is another array's storage: `%h = (%h, ...)` was
        // copied into it before this began.)
        int64_t pair = hash_make(cx, hash, from->items[k]);
        h->items[2 * pair + 1] = scalar(cx, from->items[k + 1]);
    }
}

void rt_hash_assign(rt_ctx *cx, rt_value hash, rt_value list) {
    rt_hash_rest(cx, hash, list, 0);
}

// ---- step 12b: what stands on a hash

// An element in the list of a loop, a `map`, a `grep` or a `sort`: perl
// would make a key that is not there (T216).
rt_value rt_helem_strict(rt_ctx *cx, rt_value hash, rt_value key) {
    scratch number;
    rt_array *h = hash_of(cx, hash);
    int64_t pair = hash_find(cx, h, to_str(cx, key, &number));
    if (pair < 0) rt_fault(cx, "a key that is not there in a foreach, where perl would make it");
    return h->items[2 * pair + 1];
}

// `@h{KEYS}`: the value at each key, undef for one that is not there;
// and with `strict`, in such a list or among a call's arguments, the
// fault for one.
void rt_list_add_hslice(rt_ctx *cx, rt_value list, rt_value hash, rt_value keys, int strict) {
    rt_array *to = array_of(cx, list);
    rt_array *h = hash_of(cx, hash);
    rt_array *ks = array_of(cx, keys);
    for (uint64_t n = 0; n < ks->count; n++) {
        scratch number;
        int64_t pair = hash_find(cx, h, to_str(cx, ks->items[n], &number));
        if (pair < 0 && strict) rt_fault(cx, "a slice with a key that is not there, where perl would make it");
        append(cx, to, pair < 0 ? rt_undef() : h->items[2 * pair + 1]);
    }
}

// `@h{KEYS} = LIST`: a value for each key in turn, and an undef for each
// the list does not reach, which makes its key all the same (T228).
void rt_hslice_store(rt_ctx *cx, rt_value hash, rt_value keys, rt_value list) {
    rt_array *ks = array_of(cx, keys);
    rt_array *from = array_of(cx, list);
    for (uint64_t n = 0; n < ks->count; n++) {
        rt_helem_store(cx, hash, ks->items[n], n < from->count ? from->items[n] : rt_undef());
    }
}

// `delete @h{KEYS}`: what each key held, or undef, added to `list`.
void rt_hash_delete_slice(rt_ctx *cx, rt_value list, rt_value hash, rt_value keys) {
    rt_array *ks = array_of(cx, keys);
    for (uint64_t n = 0; n < ks->count; n++) {
        // (Nothing here allocates: a deleted value is in the list at once.)
        rt_value was = rt_hash_delete(cx, hash, ks->items[n]);
        append(cx, array_of(cx, list), was);
    }
}

// A last parameter that is a hash, filled at its turn from the arguments
// left, `from` on: keys and values by turns. (That there is an even
// number of them was asked as the sub was entered, T226.)
void rt_slurp_hash(rt_ctx *cx, rt_value hash, int64_t argc, rt_value **argv, rt_value *flat, int64_t from) {
    for (int64_t n = from; n + 1 < argc; n += 2) {
        int64_t pair = hash_make(cx, hash, flat != NULL ? flat[n] : *argv[n]);
        hash_of(cx, hash)->items[2 * pair + 1] = scalar(cx, flat != NULL ? flat[n + 1] : *argv[n + 1]);
    }
}
