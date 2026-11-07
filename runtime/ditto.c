#include "ditto.h"

#include <inttypes.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

const char *dt_path = "?";

/* Allocator --------------------------------------------------------------- */

#define CHUNK_SIZE ((size_t)1 << 20)
#define ALIGN 16

typedef struct Chunk {
  struct Chunk *next; /* keeps every chunk reachable, so LeakSanitizer is quiet */
  size_t used, size;
  _Alignas(16) char data[];
} Chunk;

static Chunk *chunks = NULL; /* the newest chunk with room is first */

static Chunk *new_chunk(size_t size) {
  Chunk *c = malloc(sizeof(Chunk) + size);
  if (c == NULL) {
    fflush(stdout);
    fprintf(stderr, "%s: fault: out of memory\n", dt_path);
    exit(1);
  }
  c->used = 0;
  c->size = size;
  return c;
}

void *dt_alloc(size_t n) {
  n = (n + ALIGN - 1) & ~(size_t)(ALIGN - 1);
  if (n > CHUNK_SIZE / 4) {
    /* A big object gets its own chunk, linked behind the current one so the
       current one keeps serving small requests. */
    Chunk *c = new_chunk(n);
    c->used = n;
    if (chunks == NULL) { c->next = NULL; chunks = c; }
    else { c->next = chunks->next; chunks->next = c; }
    return c->data;
  }
  if (chunks == NULL || chunks->size - chunks->used < n) {
    Chunk *c = new_chunk(CHUNK_SIZE);
    c->next = chunks;
    chunks = c;
  }
  void *p = chunks->data + chunks->used;
  chunks->used += n;
  return p;
}

/* Faults ------------------------------------------------------------------ */

_Noreturn void dt_fault(int line, int col, const char *fmt, ...) {
  fflush(stdout);
  fprintf(stderr, "%s:%d:%d: fault: ", dt_path, line, col);
  va_list ap;
  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap);
  va_end(ap);
  fputc('\n', stderr);
  fflush(stderr);
  exit(1);
}

/* Operators --------------------------------------------------------------- */

static const char *type_name(Value v) {
  switch (v.tag) {
    case T_NIL: return "nil";
    case T_BOOL: return "bool";
    case T_INT: return "int";
    case T_STR: return "string";
    case T_LIST: return "list";
    case T_MAP: return "map";
  }
  return "?";
}

static _Noreturn void type_fault2(int line, int col, const char *op, Value a, Value b) {
  dt_fault(line, col, "cannot use %s on %s and %s", op, type_name(a), type_name(b));
}

/* The overflow checks are written out rather than using __builtin_*_overflow,
   which is a compiler extension. */
Value dt_add(int line, int col, Value a, Value b) {
  if (a.tag != T_INT || b.tag != T_INT) type_fault2(line, col, "+", a, b);
  if ((b.i > 0 && a.i > INT64_MAX - b.i) || (b.i < 0 && a.i < INT64_MIN - b.i))
    dt_fault(line, col, "integer overflow");
  return dt_int(a.i + b.i);
}

Value dt_sub(int line, int col, Value a, Value b) {
  if (a.tag != T_INT || b.tag != T_INT) type_fault2(line, col, "-", a, b);
  if ((b.i < 0 && a.i > INT64_MAX + b.i) || (b.i > 0 && a.i < INT64_MIN + b.i))
    dt_fault(line, col, "integer overflow");
  return dt_int(a.i - b.i);
}

Value dt_mul(int line, int col, Value a, Value b) {
  if (a.tag != T_INT || b.tag != T_INT) type_fault2(line, col, "*", a, b);
  int64_t x = a.i, y = b.i;
  bool over;
  if (x > 0) over = y > 0 ? x > INT64_MAX / y : y < INT64_MIN / x;
  else if (x < 0) over = y > 0 ? x < INT64_MIN / y : y < INT64_MAX / x;
  else over = false;
  if (over) dt_fault(line, col, "integer overflow");
  return dt_int(x * y);
}

/* Division truncates toward zero and % takes the dividend's sign, as C does;
   the two cases C leaves undefined are handled first (D14). */
Value dt_div(int line, int col, Value a, Value b) {
  if (a.tag != T_INT || b.tag != T_INT) type_fault2(line, col, "/", a, b);
  if (b.i == 0) dt_fault(line, col, "division by zero");
  if (a.i == INT64_MIN && b.i == -1) dt_fault(line, col, "integer overflow");
  return dt_int(a.i / b.i);
}

Value dt_mod(int line, int col, Value a, Value b) {
  if (a.tag != T_INT || b.tag != T_INT) type_fault2(line, col, "%", a, b);
  if (b.i == 0) dt_fault(line, col, "division by zero");
  if (b.i == -1) return dt_int(0);
  return dt_int(a.i % b.i);
}

Value dt_neg(int line, int col, Value a) {
  if (a.tag != T_INT) dt_fault(line, col, "cannot use - on %s", type_name(a));
  if (a.i == INT64_MIN) dt_fault(line, col, "integer overflow");
  return dt_int(-a.i);
}

Value dt_not(int line, int col, Value a) {
  if (a.tag != T_BOOL) dt_fault(line, col, "cannot use not on %s", type_name(a));
  return dt_bool(!a.b);
}

void dt_need_bool(int line, int col, const char *op, Value v) {
  if (v.tag != T_BOOL) dt_fault(line, col, "cannot use %s on %s", op, type_name(v));
}

/* Ordering is for ints now; strings and lists join at steps 4 and 5. */
static int compare(int line, int col, const char *op, Value a, Value b) {
  if (a.tag != T_INT || b.tag != T_INT) type_fault2(line, col, op, a, b);
  return a.i < b.i ? -1 : a.i > b.i ? 1 : 0;
}

Value dt_lt(int line, int col, Value a, Value b) { return dt_bool(compare(line, col, "<", a, b) < 0); }
Value dt_le(int line, int col, Value a, Value b) { return dt_bool(compare(line, col, "<=", a, b) <= 0); }
Value dt_gt(int line, int col, Value a, Value b) { return dt_bool(compare(line, col, ">", a, b) > 0); }
Value dt_ge(int line, int col, Value a, Value b) { return dt_bool(compare(line, col, ">=", a, b) >= 0); }

bool dt_equal(Value a, Value b) {
  if (a.tag != b.tag) return false;
  switch (a.tag) {
    case T_NIL: return true;
    case T_BOOL: return a.b == b.b;
    case T_INT: return a.i == b.i;
    default: return false; /* strings, lists and maps arrive with later steps */
  }
}

/* Statements -------------------------------------------------------------- */

void dt_need_cond(int line, int col, Value v) {
  if (v.tag != T_BOOL) dt_fault(line, col, "condition must be a bool, got %s", type_name(v));
}

void dt_need_range_bound(int line, int col, Value v) {
  if (v.tag != T_INT) dt_fault(line, col, "range bounds must be ints, got %s", type_name(v));
}

int64_t dt_iter_len(int line, int col, Value v) {
  dt_fault(line, col, "cannot iterate over %s", type_name(v));
}

Value dt_iter_item(Value v, int64_t i) {
  (void)v;
  (void)i;
  dt_fault(0, 0, "internal error: iteration over a collection arrives with steps 4 to 6");
}

/* Calls ------------------------------------------------------------------- */

#define MAX_DEPTH 1000
static int depth = 0;

void dt_enter(int line, int col) {
  if (depth >= MAX_DEPTH) dt_fault(line, col, "stack overflow (more than %d nested calls)", MAX_DEPTH);
  depth++;
}

void dt_leave(void) { depth--; }

/* Printing ---------------------------------------------------------------- */

/* Writes the printed form of v (LANGUAGE.md, str). `quoted` is true inside a
   list or map, where strings get quotes (D24); lists and maps arrive with
   steps 5 and 6. */
static void write_value(Value v, bool quoted) {
  (void)quoted;
  switch (v.tag) {
    case T_NIL: fputs("nil", stdout); break;
    case T_BOOL: fputs(v.b ? "true" : "false", stdout); break;
    case T_INT: printf("%" PRId64, v.i); break;
    default: dt_fault(0, 0, "internal error: cannot print tag %d", v.tag);
  }
}

Value dt_b_print(int line, int col, int argc, const Value *argv) {
  (void)line;
  (void)col;
  for (int i = 0; i < argc; i++) {
    if (i > 0) fputc(' ', stdout);
    write_value(argv[i], false);
  }
  fputc('\n', stdout);
  return dt_nil();
}
