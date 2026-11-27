// Shared between the runtime and generated code. Every name is prefixed
// rt_/RT_: macOS's <stdlib.h> pulls in <sys/wait.h>, which has a P_PID,
// and its <sys/types.h> defines major() and minor() as macros.
#ifndef RT_H
#define RT_H
#include <stddef.h>
#include <stdint.h>

// On a local the generated C declares and a program may never read: a
// variable that is only ever set, the value of `$x++;`.
#define RT_UNUSED __attribute__((unused))

// A value is two words, a tag and a payload (D25), so that a 64-bit
// integer fits whole; both C compilers pass the pair in registers. The
// union gains a member per kind of value. No tag is 0: memory that was
// never made a value then faults at the first operator that checks it.
enum { RT_TAG_INT = 1, RT_TAG_NUM = 2, RT_TAG_STR = 3, RT_TAG_UNDEF = 4, RT_TAG_BOOL = 5, RT_TAG_ARRAY = 6, RT_TAG_ABSENT = 7, RT_TAG_HASH = 8 };

// An array (D80): a row of values that grows and shrinks in place, the
// collector's as a heap string is, with storage of its own. It is what an
// array variable's slot holds, and what a list is while a statement builds
// and uses it: a list is an array with no name, in a temporary. An array
// holds no array yet (step 13). `dead` says it was collected, and nothing
// may read it.
typedef struct rt_array {
    uint64_t count;
    uint64_t room;          // how many values `items` has space for
    struct rt_value_ *items;
    uint64_t dead;
    uint64_t frozen;        // how many `foreach` loops are over it (D80)
    // A hash is this block too (step 12, runtime/hash.c): `items` holds a
    // key and its value by turns, and `index` finds a key's pair.
    uint32_t *index;
    uint64_t slots;
    uint64_t gone;          // how many of its pairs are holes, deleted
} rt_array;

// A Str (D24): Unicode characters, held as UTF-8, and never changed once
// made. `len` is its bytes and `chars` its characters, which are the same
// number when every character is ASCII. The byte after the last is a NUL,
// which is not part of the string; a string may hold NULs of its own.
//
// `where` says whose its memory is (D26, D66). A constant is a literal of
// the program or the runtime's own, and is 0 so that a constant written
// as its three first members is one. A heap string was made as the
// program ran, and is the collector's. A scratch string is a number as a
// string, on the C stack for as long as one operation runs, and never
// what a runtime function returns. A dead one was a heap string, and was
// collected: nothing may read it.
enum { RT_STR_CONSTANT = 0, RT_STR_HEAP = 1, RT_STR_SCRATCH = 2, RT_STR_DEAD = 3 };

typedef struct rt_str {
    uint64_t len;
    uint64_t chars;
    const char *bytes;
    uint64_t where;
} rt_str;

typedef struct rt_value_ {
    uint64_t tag;
    union { int64_t i; double n; uint64_t bits; const rt_str *s; rt_array *a; } as;
} rt_value;

// What a sub that returns nothing gives a list: no value at all (D79).
// It is never an operand: a list leaves it out as it is built.
static inline rt_value rt_absent(void) {
    rt_value v;
    v.tag = RT_TAG_ABSENT;
    v.as.i = 0;
    return v;
}

static inline rt_value rt_int(int64_t n) {
    rt_value v;
    v.tag = RT_TAG_INT;
    v.as.i = n;
    return v;
}

// A Num (D23): a double, and always a finite one (D37); the operators see
// to that, and a literal that isn't was refused. The compiler hands a
// literal over as its bits.
static inline rt_value rt_num(double x) {
    rt_value v;
    v.tag = RT_TAG_NUM;
    v.as.n = x;
    return v;
}

static inline rt_value rt_num_bits(uint64_t bits) {
    rt_value v;
    v.tag = RT_TAG_NUM;
    v.as.bits = bits;
    return v;
}

// A string literal is a constant in the generated C, and this is its
// value.
static inline rt_value rt_string(const rt_str *s) {
    rt_value v;
    v.tag = RT_TAG_STR;
    v.as.s = s;
    return v;
}

// undef (D48): the one value that is no value. Its payload is nothing.
static inline rt_value rt_undef(void) {
    rt_value v;
    v.tag = RT_TAG_UNDEF;
    v.as.i = 0;
    return v;
}

// A boolean (D47): `true` or `false`, and what a comparison gives. The
// payload is 1 or 0.
static inline rt_value rt_bool(int truth) {
    rt_value v;
    v.tag = RT_TAG_BOOL;
    v.as.i = truth != 0;
    return v;
}

// A frame (D66): every variable and temporary of one function, as slots
// the collector can see. A slot whose tag is 0 holds no value yet. The
// frames are a list from the context, the newest first; the generated C
// opens one as a function begins and closes it as it returns, and a
// runtime function that makes more than one value opens one too.
typedef struct rt_frame {
    struct rt_frame *prev;
    uint64_t count;
    rt_value *slots;
} rt_frame;

// The context (D28): everything the runtime knows that isn't a value,
// passed first to every runtime function and every compiled sub, so that
// nothing is global and a second context can one day run beside this one.
// A sort that is under way (sort.c).
typedef struct rt_sort rt_sort;

typedef struct rt_ctx {
    const char *file;       // the program's path, as the compiler was given it
    int64_t line;           // the line of the statement that is running
    int out_utf8;           // `use open ':std', ':encoding(UTF-8)';` was said (D39)
    rt_frame *frames;       // the roots: the newest frame, and through it the rest
    rt_value *shared;       // the file's variables, which a sub reaches through here
    uint64_t deep;          // what the open frames count for, against the limit on recursion
    struct rt_sort *sorts;  // the sorts that are under way, the newest first
    struct rt_block *heap;  // every string made and not yet collected
    struct rt_block *dead;  // under poison, the collected: kept, never handed out again
    uint64_t held;          // the bytes of both, headers and all: what the cap is on
    uint64_t since;         // bytes allocated since the last collection
    uint64_t threshold;     // and how many of them bring the next
    // Counted for the runtime's own tests, and used by nothing else.
    uint64_t allocations;   // strings made, ever
    uint64_t collections;   // collections run
    uint64_t objects;       // strings on the heap now
    // The knobs (D63), read from the environment as the program starts.
    // 0 is off.
    uint64_t stress;        // CURLY_GC_STRESS: a collection at every nth allocation
    uint64_t poison;        // CURLY_GC_POISON: a collected string's memory is kept
    uint64_t cap;           // CURLY_HEAP_CAP: `out of memory` when more would be held
} rt_ctx;

// Run a compiled program: make its context, call its body, return the
// status main should. The generated C's main is this and nothing else.
int rt_run(void (*body)(rt_ctx *cx), const char *file);

// Open a frame of `count` slots, all holding no value, and close it: the
// newest must be the one closed.
void rt_enter(rt_ctx *cx, rt_frame *frame, rt_value *slots, uint64_t count);
void rt_leave(rt_ctx *cx, rt_frame *frame);

// A collection, now (D26): every heap string that no slot of any frame
// holds is freed. The runtime runs one by itself inside an allocation,
// when the knobs or the bytes allocated say so; this is for its tests.
void rt_collect(rt_ctx *cx);

// `use open ':std', ':encoding(UTF-8)';` (D39): from here a character
// past ASCII may be printed.
void rt_use_open(rt_ctx *cx);

// `say`: the value as a string, and a newline; `print`: without one. The
// bytes are UTF-8. Faults: a character past ASCII without `use open`
// (perl would print another byte, or warn), and a noncharacter (D42).
void rt_say(rt_ctx *cx, rt_value v);
void rt_print(rt_ctx *cx, rt_value v);

// Arithmetic (D23, D35). Each is done on whole numbers when both operands
// are integral (an Int, or a whole Num below 2^53) and on doubles
// otherwise, as perl does it; rt.c has the rule for each. The faults:
// `integer overflow`, `float overflow`, `not a number`, `division by
// zero`, `modulus by zero`, `modulus of a number outside the integers`;
// and where perl has two answers by what was done with a value before
// (D40, D45).
rt_value rt_add(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_sub(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_mul(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_div(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_mod(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_pow(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_neg(rt_ctx *cx, rt_value a);

// `++` and `--` (D52): what the variable holds afterwards, by what it
// held. And what `$x++` is worth: what `$x` held, or 0 for an undef.
rt_value rt_inc(rt_ctx *cx, rt_value a);
rt_value rt_dec(rt_ctx *cx, rt_value a);
rt_value rt_before_inc(rt_ctx *cx, rt_value a);

// `+=`, `-=` and `.=`: the operator, but an undef on the left is 0, or
// the empty string, as perl has it (D56). The other assigning operators
// are the operators themselves, and fault on one.
rt_value rt_add_to(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_sub_from(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_concat_to(rt_ctx *cx, rt_value a, rt_value b);

// Strings (D24, D40 to D44). An operand that is a number is made a
// string as `say` prints it, and one that is a string is made a number by
// D40's rule where a number is wanted; rt.c has both. `x` takes a count,
// `substr` and `index` positions, cut toward zero. A character is a
// Unicode scalar value, and positions count characters.
rt_value rt_concat(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_repeat(rt_ctx *cx, rt_value a, rt_value count);
rt_value rt_length(rt_ctx *cx, rt_value a);
rt_value rt_uc(rt_ctx *cx, rt_value a);
rt_value rt_lc(rt_ctx *cx, rt_value a);
rt_value rt_ord(rt_ctx *cx, rt_value a);
rt_value rt_chr(rt_ctx *cx, rt_value a);
rt_value rt_substr2(rt_ctx *cx, rt_value a, rt_value offset);
rt_value rt_substr3(rt_ctx *cx, rt_value a, rt_value offset, rt_value count);
rt_value rt_index2(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_index3(rt_ctx *cx, rt_value a, rt_value b, rt_value position);

// Truth, definedness and comparison (D49). Truth is perl's: false is
// undef, `false`, a number that is zero, the empty string and the string
// `0`. The three tests are what the generated C branches on, for `&&`,
// `||`, `//` and `? :`, whose right operands and branches are C that may
// not run; each gives 1 or 0.
int rt_is_true(rt_ctx *cx, rt_value v);
int rt_is_false(rt_ctx *cx, rt_value v);
int rt_is_undef(rt_ctx *cx, rt_value v);
rt_value rt_not(rt_ctx *cx, rt_value a);
rt_value rt_xor(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_defined(rt_ctx *cx, rt_value a);

// `== != < > <= >=` and `<=>`: both operands as numbers, compared as
// whole numbers when both are integral and as doubles otherwise.
rt_value rt_num_eq(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_num_ne(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_num_lt(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_num_gt(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_num_le(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_num_ge(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_num_cmp(rt_ctx *cx, rt_value a, rt_value b);

// `eq ne lt gt le ge` and `cmp`: both operands as strings, compared
// character by character.
rt_value rt_str_eq(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_str_ne(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_str_lt(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_str_gt(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_str_le(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_str_ge(rt_ctx *cx, rt_value a, rt_value b);
rt_value rt_str_cmp(rt_ctx *cx, rt_value a, rt_value b);

// The context of a call, perl's three (D18). A compiled sub is handed one
// and, for each parameter, where its argument is, or NULL.
enum { RT_VOID = 0, RT_SCALAR = 1, RT_LIST = 2 };

// The limit on recursion (D68), which is the implementation's and no part
// of the language: the frames that are open may count for this much, each
// counting 16 bytes a slot and RT_CALL_BYTES besides, which is more of the
// C stack than a call was measured to take under any compiler
// (docs/briefs/step8-stack.c). So the count runs out, and `recursion too
// deep` is the fault, while half of an 8 MB stack is left; and rt_run
// stops a program that was given a smaller stack before it starts.
#define RT_CALL_BYTES 1024
#define RT_DEPTH_LIMIT (UINT64_C(4) << 20)
#define RT_STACK_NEEDED (UINT64_C(8) << 20)

// The faults of a call: a wrong number of arguments, as `too few
// arguments for NAME: got 1, expected 2`; and `NAME WHAT`, for a sub whose
// value was used when it has none (D18), and for one that returned nothing
// where perl wants a list (D71).
#define RT_NO_VALUE "has no value: it does not end in a return or an expression"
#define RT_LISTED "returned a list where one value is wanted"
#define RT_NOTHING "returned nothing where a list is wanted"
void rt_fault_arguments(rt_ctx *cx, const char *name, int64_t got, int64_t least, int64_t most) __attribute__((noreturn));
void rt_fault_sub(rt_ctx *cx, const char *name, const char *what) __attribute__((noreturn));

// Arrays and lists (D76, D80). A list is built in a temporary: made empty,
// and added to, left to right, a value at a time (an absent one is left
// out), an array's values, a range's, a slice's, a list's N times. None
// of the adding can start a collection: only `rt_array_new` allocates
// from the heap, and what it makes is in a slot before anything else is.
rt_value rt_array_new(rt_ctx *cx);
// A hash (step 12; D27): its keys in the order they were first stored. A
// key is made a string as `.` makes one. An element is read, made and
// stored as an array's is, a made one by the number of its pair, which
// holds until a key is deleted or the hash assigned.
rt_value rt_hash_new(rt_ctx *cx);
rt_value rt_helem(rt_ctx *cx, rt_value hash, rt_value key);
rt_value rt_helem_store(rt_ctx *cx, rt_value hash, rt_value key, rt_value v);
int64_t rt_helem_make(rt_ctx *cx, rt_value hash, rt_value key);
rt_value rt_helem_get(rt_ctx *cx, rt_value hash, int64_t pair);
rt_value rt_helem_put(rt_ctx *cx, rt_value hash, int64_t pair, rt_value v);
rt_value rt_hash_exists(rt_ctx *cx, rt_value hash, rt_value key);
rt_value rt_hash_delete(rt_ctx *cx, rt_value hash, rt_value key);
rt_value rt_hash_count(rt_ctx *cx, rt_value hash);
void rt_list_add_pairs(rt_ctx *cx, rt_value list, rt_value hash);
void rt_list_add_keys(rt_ctx *cx, rt_value list, rt_value hash);
void rt_list_add_values(rt_ctx *cx, rt_value list, rt_value hash);
// `%h = LIST`, and a hash as the last target of a list assignment, from
// the list's value `n` on; an odd number of values is a fault.
void rt_hash_assign(rt_ctx *cx, rt_value hash, rt_value list);
void rt_hash_rest(rt_ctx *cx, rt_value hash, rt_value list, int64_t n);
void rt_list_add(rt_ctx *cx, rt_value list, rt_value v);
void rt_list_add_all(rt_ctx *cx, rt_value list, rt_value array);
void rt_list_add_range(rt_ctx *cx, rt_value list, rt_value from, rt_value to);
// The elements of `from` at each of `indexes`, undef for one past either
// end. `how` 1: `from` is a list, and one with no values gives nothing at
// all (T164). `how` 2: an index past either end is a fault, where perl
// would make the element (T161).
void rt_list_add_slice(rt_ctx *cx, rt_value list, rt_value from, rt_value indexes, int how);
void rt_list_add_repeat(rt_ctx *cx, rt_value list, rt_value values, rt_value count);
// A list assignment: the value for target `n`, undef past the last; and
// for an array, the last target, every value from `n` on.
rt_value rt_list_item(rt_ctx *cx, rt_value list, int64_t n);
void rt_array_rest(rt_ctx *cx, rt_value array, rt_value list, int64_t n);
// A `foreach` (D17, D80): how many values its list has; an element in its
// list, a fault past either end, where perl would make it (T161); and the
// freeze of an array its list names, a count, for a loop in a loop: while
// it is not 0, whatever stores to the array or changes its size faults.
int64_t rt_list_length(rt_ctx *cx, rt_value list);
rt_value rt_elem_strict(rt_ctx *cx, rt_value array, rt_value index);
void rt_freeze(rt_ctx *cx, rt_value array);
void rt_thaw(rt_ctx *cx, rt_value array);
// A `foreach` over one range: its ends, and whether it has any values. An
// end below -2^63 + 513 is a fault, as perl has it (T166).
int rt_range_ends(rt_ctx *cx, rt_value from, rt_value to, int64_t *lo, int64_t *hi);
// `@a = LIST`: the array's values are the list's, copied.
void rt_array_assign(rt_ctx *cx, rt_value array, rt_value list);
// How many, and the last index, -1 for none.
rt_value rt_count(rt_ctx *cx, rt_value array);
rt_value rt_last_index(rt_ctx *cx, rt_value array);
// The first value of a list, or undef: `(LIST)[N]` where one is wanted.
rt_value rt_first(rt_ctx *cx, rt_value list);
// An element, read: undef past either end, and nothing is made.
rt_value rt_elem(rt_ctx *cx, rt_value array, rt_value index);
// An element, stored: the array grows to hold it, and before the start it
// is a fault. Gives what was stored.
rt_value rt_elem_store(rt_ctx *cx, rt_value array, rt_value index, rt_value v);
// An element, made, for an operator that reads it and stores it: where it
// is, from the start. Then read and stored there.
int64_t rt_elem_make(rt_ctx *cx, rt_value array, rt_value index);
rt_value rt_elem_get(rt_ctx *cx, rt_value array, int64_t at);
rt_value rt_elem_put(rt_ctx *cx, rt_value array, int64_t at, rt_value v);
// `push` and `unshift` give the new count; `pop` and `shift` undef from
// an empty array.
rt_value rt_push(rt_ctx *cx, rt_value array, rt_value list);
rt_value rt_unshift(rt_ctx *cx, rt_value array, rt_value list);
rt_value rt_pop(rt_ctx *cx, rt_value array);
rt_value rt_shift(rt_ctx *cx, rt_value array);
// `splice`: `given` is how many of offset and length were written. What
// was removed is added to `removed`, and `put` goes where it was.
void rt_splice(rt_ctx *cx, rt_value removed, rt_value array, int given, rt_value offset, rt_value length, rt_value put);
// `say LIST` and `print LIST`: every value is looked at before any is
// written, so a fault leaves nothing of the list on stdout.
void rt_say_list(rt_ctx *cx, rt_value list);
void rt_print_list(rt_ctx *cx, rt_value list);
// The arguments of a call that were built as a list: where each of the
// first `most` is, into `where`, and how many there are in all.
// A call's arguments when they were built as one list: where its values
// are, one after another. A slurpy parameter: every argument from `from`
// on, copied into `array`, from `flat` if the arguments are a list and
// from where `argv` says each is otherwise.
rt_value *rt_list_items(rt_ctx *cx, rt_value list);
// The one value of a list of one, and no value for a list of none: what
// a sub that gives no list gives a call that wants one.
rt_value rt_only(rt_ctx *cx, rt_value list);
void rt_slurp(rt_ctx *cx, rt_value array, int64_t argc, rt_value **argv, rt_value *flat, int64_t from);
// Step 12b. A hash as a last parameter, filled from the arguments left;
// an odd number of them is a fault as the sub is entered.
void rt_slurp_hash(rt_ctx *cx, rt_value hash, int64_t argc, rt_value **argv, rt_value *flat, int64_t from);
void rt_fault_odd_arguments(rt_ctx *cx, const char *name) __attribute__((noreturn));
// An element and a slice of a hash in a list where perl would make a key
// that is not there; a slice read, stored to and deleted; and an array's
// slice stored to.
rt_value rt_helem_strict(rt_ctx *cx, rt_value hash, rt_value key);
void rt_list_add_hslice(rt_ctx *cx, rt_value list, rt_value hash, rt_value keys, int strict);
void rt_hslice_store(rt_ctx *cx, rt_value hash, rt_value keys, rt_value list);
void rt_hash_delete_slice(rt_ctx *cx, rt_value list, rt_value hash, rt_value keys);
void rt_slice_store(rt_ctx *cx, rt_value array, rt_value indexes, rt_value list);
// `sort` (step 10c; D82, D83; sort.c). The generated code drives a sort
// with a block: `rt_sort_begin`, then `rt_sort_next` for as long as it
// gives two values to compare, the block's value handed to
// `rt_sort_answer` each time, then `rt_sort_end`, which adds the values in
// order to `into`. `lone`: a list of one value is looked at once, as perl
// looks at it for the blocks it throws away (T190). `rt_sort_strings` is
// a sort with no block, and `rt_sort_in_place` the fault for an undef in
// an array that perl would sort in place (T187).
rt_sort *rt_sort_begin(rt_ctx *cx, rt_value list, int lone);
int rt_sort_next(rt_ctx *cx, rt_sort *s, rt_value *a, rt_value *b);
void rt_sort_answer(rt_ctx *cx, rt_sort *s, rt_value v);
void rt_sort_end(rt_ctx *cx, rt_sort *s, rt_value into);
void rt_sort_strings(rt_ctx *cx, rt_value list, rt_value into);
void rt_sort_in_place(rt_ctx *cx, rt_value list);
// `reverse`: the values of `values`, last first, added to `list`. `join`:
// the separator made a string, used or not (T190), then each value, as `.`
// makes one.
void rt_list_add_reversed(rt_ctx *cx, rt_value list, rt_value values);
rt_value rt_join(rt_ctx *cx, rt_value separator, rt_value list);
// runtime/format.c (step 16b): the list is the format and its values.
rt_value rt_sprintf(rt_ctx *cx, rt_value list);
void rt_printf(rt_ctx *cx, rt_value list);

// A fault (D13): stdout as far as it got, then
// `fault: WHAT at FILE line N.` on stderr, and exit 1. Never returns, and
// nothing can catch it.
void rt_fault(rt_ctx *cx, const char *what) __attribute__((noreturn));

// A bug in the compiler or the runtime, found as the program ran (D66):
// `internal: WHAT at FILE line N.` on stderr, after what the program
// printed, and exit status 2. Never the program's doing.
void rt_internal(rt_ctx *cx, const char *what) __attribute__((noreturn));
#endif
