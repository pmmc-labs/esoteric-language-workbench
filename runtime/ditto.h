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
struct List { int64_t len; Value items[]; };
/* Keys and values in insertion order, searched linearly (D27). */
struct Map { int64_t len; Value *keys; Value *vals; };

extern const char *dt_path;

static inline Value dt_nil(void) { Value v; v.tag = T_NIL; v.i = 0; return v; }
static inline Value dt_bool(bool b) { Value v; v.tag = T_BOOL; v.i = 0; v.b = b; return v; }
static inline Value dt_int(int64_t i) { Value v; v.tag = T_INT; v.i = i; return v; }

/* Bump allocator over large malloc'ed chunks kept on a global list, never
   freed (D26). Memory is 16-byte aligned; dt_alloc(0) is a valid pointer. */
void *dt_alloc(size_t n);

/* Flushes standard output, prints `path:line:col: fault: message` on standard
   error and exits 1 (D28). */
_Noreturn void dt_fault(int line, int col, const char *fmt, ...);

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
/* The number of items a `for` over v walks, and item i (from 0). Anything but
   a string, list or map faults `cannot iterate over T`; those three arrive
   with steps 4 to 6, so for now every value faults. */
int64_t dt_iter_len(int line, int col, Value v);
Value dt_iter_item(Value v, int64_t i);

/* Builtins: every one takes its call's position and its arguments, and
   returns a Value. Named dt_b_NAME, which is what the code generator emits. */
Value dt_b_print(int line, int col, int argc, const Value *argv);

#endif
