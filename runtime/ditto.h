/* The Ditto runtime: values, the allocator, printing, faults (D26, D28).
   Runtime functions that can fault take the position as two ints (line,
   column); the path is a global the generated main sets. */
#ifndef DITTO_H
#define DITTO_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum { T_NIL, T_BOOL, T_INT, T_STR, T_LIST, T_MAP } Tag;

struct Str;
struct List;
struct Map;

/* 16 bytes, passed by value. Heap objects behind the pointers are immutable
   once built (D7), so copying a Value never needs a deep copy. */
typedef struct Value {
  uint8_t tag;
  union {
    int64_t i;
    bool b;
    struct Str *s;
    struct List *l;
    struct Map *m;
  };
} Value;

struct Str { int64_t len; char bytes[]; };
/* `owner`, when not NULL, is the address of the one variable that holds the
   only reference to this list or map: an update through that variable may
   write in place (D48). Reading the variable in any way that could keep the
   value clears it (dt_share). `cap` is the room allocated, for appends. */
struct List { int64_t len; int64_t cap; void *owner; Value items[]; };
/* Keys and values in insertion order, searched linearly (D27). */
struct Map { int64_t len; int64_t cap; void *owner; Value *keys; Value *vals; };

extern const char *dt_path;

static inline Value dt_nil(void) { Value v; v.tag = T_NIL; v.i = 0; return v; }
static inline Value dt_bool(bool b) { Value v; v.tag = T_BOOL; v.i = 0; v.b = b; return v; }
static inline Value dt_int(int64_t i) { Value v; v.tag = T_INT; v.i = i; return v; }
static inline Value dt_str(struct Str *s) { Value v; v.tag = T_STR; v.i = 0; v.s = s; return v; }
static inline Value dt_list(struct List *l) { Value v; v.tag = T_LIST; v.i = 0; v.l = l; return v; }
static inline Value dt_map(struct Map *m) { Value v; v.tag = T_MAP; v.i = 0; v.m = m; return v; }

/* Bump allocator over large malloc'ed chunks kept on a global list, never
   freed (D26). Memory is 16-byte aligned; dt_alloc(0) is a valid pointer. */
void *dt_alloc(size_t n);

/* Flushes standard output, prints `path:line:col: fault: message` on standard
   error and exits 1 (D28). */
_Noreturn void dt_fault(int line, int col, const char *fmt, ...);

/* Strings are byte sequences with a length: a NUL is an ordinary byte, and
   every function here goes by `len`, never by a terminator (there is one
   past the end, for C's convenience, and nothing relies on it). */
/* A new string holding a copy of `len` bytes. */
Value dt_str_new(const char *bytes, int64_t len);
/* The string of `n` parts joined, each as `str` gives it (interpolation). */
Value dt_interp(int n, const Value *parts);

/* Lists are immutable once built (D7): an update is a new list that shares
   the old one's items, and nothing here ever writes a List after it is
   returned. */
/* A new list holding a copy of the n items (n may be 0; items may then be NULL). */
Value dt_list_new(int64_t n, const Value *items);
/* `c` with the item at key `i` replaced by `v`, as a new value: the set of an
   assignment's last step (LANGUAGE.md, Assignment). Faults, at the step's `[`,
   `cannot assign into T` unless c is a list or a map (checked first), then the
   key's type and, for a list, its range. A map key is replaced in place if
   present and added at the end if not. */
Value dt_set_index(int line, int col, Value c, Value i, Value v);
/* The same, through the variable at `slot` that holds c (D48). */
Value dt_set_index_own(int line, int col, Value c, Value i, Value v, void *slot);
Value dt_set_field_own(int line, int col, Value c, Value name, Value v, void *slot);
Value dt_add_own(int line, int col, Value a, Value b, void *slot);
/* A variable's value is being read in a way that could keep it (D48). */
static inline void dt_share(Value v) {
  if (v.tag == T_LIST) v.l->owner = NULL;
  else if (v.tag == T_MAP) v.m->owner = NULL;
}
/* The same for a `.name` step, at the `.`: a map is set like dt_set_index; a
   list faults `cannot use .name on list`, anything else `cannot assign into T`. */
Value dt_set_field(int line, int col, Value c, Value name, Value v);

/* Maps are immutable once built, like lists (D7): keys and values in insertion
   order, searched linearly (D27), and an update is a new map. */
/* A new map of the n pairs (keys[k], vals[k]), copied; the keys must be ints
   or strings and distinct (the compiler checks a literal's keys). */
Value dt_map_new(int64_t n, const Value *keys, const Value *vals);

/* Lookups (LANGUAGE.md, Indexing). The `try` forms store the value and return
   true on a hit, return false on a miss (an index out of range, a missing map
   key) and fault, as usual, on anything else (a wrong type); step 7's `else`
   branches on that. `dt_index` is the lookup that faults on a miss too. They
   take the position of the `[`. `dt_try_field` and `dt_field` are `m.name`
   (name is a string), at the position of the `.`: they fault
   `cannot use .name on T` unless c is a map. */
bool dt_try_index(int line, int col, Value c, Value i, Value *out);
Value dt_index(int line, int col, Value c, Value i);
bool dt_try_field(int line, int col, Value c, Value name, Value *out);
Value dt_field(int line, int col, Value c, Value name);
/* The builtin `int` the same way: faults `int: expected a string, got T`,
   returns false when the string isn't a number. Position of the name. */
bool dt_try_int(int line, int col, Value s, Value *out);

/* `x in c` (LANGUAGE.md, Comparison): a key of a map (an x that cannot be a
   key is not in it), an element of a list, a substring. Faults
   `cannot use in on T and U`. */
bool dt_in(int line, int col, Value x, Value c);

/* Operators (LANGUAGE.md, Expressions). Each takes the position of its
   operator and faults there. */
Value dt_add(int line, int col, Value a, Value b);
Value dt_sub(int line, int col, Value a, Value b);
Value dt_mul(int line, int col, Value a, Value b);
Value dt_div(int line, int col, Value a, Value b);
Value dt_mod(int line, int col, Value a, Value b);
Value dt_lt(int line, int col, Value a, Value b);
Value dt_le(int line, int col, Value a, Value b);
Value dt_gt(int line, int col, Value a, Value b);
Value dt_ge(int line, int col, Value a, Value b);
Value dt_neg(int line, int col, Value a);
Value dt_not(int line, int col, Value a);
/* Structural equality; never faults, values of different types differ (D18). */
bool dt_equal(Value a, Value b);
/* Faults `cannot use OP on T` unless v is a bool (and, or). */
void dt_need_bool(int line, int col, const char *op, Value v);

/* Statements (LANGUAGE.md, Statements). Each takes the position of the first
   token of the expression it checks. */
/* Faults `condition must be a bool, got T` unless v is a bool (if, while). */
void dt_need_cond(int line, int col, Value v);
/* Faults `range bounds must be ints, got T` unless v is an int (for). */
void dt_need_range_bound(int line, int col, Value v);
/* The number of items a `for` over v walks, and item i (from 0): the bytes of
   a string, the items of a list, the keys of a map. Anything else faults
   `cannot iterate over T`. */
int64_t dt_iter_len(int line, int col, Value v);
Value dt_iter_item(Value v, int64_t i);

/* Function calls (D28): a call is bracketed by dt_enter and dt_leave. Entering
   the 1001st nested call faults `stack overflow (more than 1000 nested
   calls)` at the position of the call's name. Builtins don't count. */
void dt_enter(int line, int col);
void dt_leave(void);

/* Builtins: every one takes its call's position and its arguments, and
   returns a Value. Named dt_b_NAME, which is what the code generator emits. */
Value dt_b_print(int line, int col, int argc, const Value *argv);
Value dt_b_str(int line, int col, int argc, const Value *argv);
Value dt_b_len(int line, int col, int argc, const Value *argv);
Value dt_b_int(int line, int col, int argc, const Value *argv);
Value dt_b_lower(int line, int col, int argc, const Value *argv);
Value dt_b_upper(int line, int col, int argc, const Value *argv);
Value dt_b_slice(int line, int col, int argc, const Value *argv);
Value dt_b_read(int line, int col, int argc, const Value *argv);
Value dt_b_sort(int line, int col, int argc, const Value *argv);
Value dt_b_split(int line, int col, int argc, const Value *argv);
Value dt_b_join(int line, int col, int argc, const Value *argv);
Value dt_b_words(int line, int col, int argc, const Value *argv);
Value dt_b_keys(int line, int col, int argc, const Value *argv);
Value dt_b_remove(int line, int col, int argc, const Value *argv);
_Noreturn Value dt_b_fail(int line, int col, int argc, const Value *argv);

#endif
