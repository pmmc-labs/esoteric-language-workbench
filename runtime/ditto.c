#include "ditto.h"

#include <inttypes.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

static void fault_head(int line, int col) {
  fflush(stdout);
  fprintf(stderr, "%s:%d:%d: fault: ", dt_path, line, col);
}

_Noreturn void dt_fault(int line, int col, const char *fmt, ...) {
  fault_head(line, col);
  va_list ap;
  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap);
  va_end(ap);
  fputc('\n', stderr);
  fflush(stderr);
  exit(1);
}

/* A message that is bytes with a length, which may hold NULs (fail, and the
   string in `not a number`). */
static _Noreturn void fault_bytes(int line, int col, const char *msg, size_t n) {
  fault_head(line, col);
  fwrite(msg, 1, n, stderr);
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

/* Strings ------------------------------------------------------------------ */

Value dt_str_new(const char *bytes, int64_t len) {
  struct Str *s = dt_alloc(sizeof(struct Str) + (size_t)len + 1);
  s->len = len;
  if (len > 0) memcpy(s->bytes, bytes, (size_t)len);
  s->bytes[len] = '\0';
  return dt_str(s);
}

/* One-byte strings, built on first use: indexing and `for` make many. */
static Value byte_str(unsigned char c) {
  static struct Str *cache[256];
  if (cache[c] == NULL) cache[c] = dt_str_new((const char *)&c, 1).s;
  return dt_str(cache[c]);
}

static _Noreturn void type_fault2(int line, int col, const char *op, Value a, Value b) {
  dt_fault(line, col, "cannot use %s on %s and %s", op, type_name(a), type_name(b));
}

/* The overflow checks are written out rather than using __builtin_*_overflow,
   which is a compiler extension. */
Value dt_add(int line, int col, Value a, Value b) {
  if (a.tag == T_STR && b.tag == T_STR) {
    struct Str *s = dt_alloc(sizeof(struct Str) + (size_t)a.s->len + (size_t)b.s->len + 1);
    s->len = a.s->len + b.s->len;
    memcpy(s->bytes, a.s->bytes, (size_t)a.s->len);
    memcpy(s->bytes + a.s->len, b.s->bytes, (size_t)b.s->len);
    s->bytes[s->len] = '\0';
    return dt_str(s);
  }
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

/* Ordering is for ints and strings now (bytes, unsigned, a prefix first);
   lists join at step 5. */
static int compare_str(const struct Str *a, const struct Str *b) {
  int64_t n = a->len < b->len ? a->len : b->len;
  int c = n == 0 ? 0 : memcmp(a->bytes, b->bytes, (size_t)n);
  if (c != 0) return c < 0 ? -1 : 1;
  return a->len < b->len ? -1 : a->len > b->len ? 1 : 0;
}

static int compare(int line, int col, const char *op, Value a, Value b) {
  if (a.tag == T_STR && b.tag == T_STR) return compare_str(a.s, b.s);
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
    case T_STR: return a.s->len == b.s->len && (a.s->len == 0 || memcmp(a.s->bytes, b.s->bytes, (size_t)a.s->len) == 0);
    default: return false; /* lists and maps arrive with later steps */
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
  if (v.tag == T_STR) return v.s->len;
  dt_fault(line, col, "cannot iterate over %s", type_name(v));
}

Value dt_iter_item(Value v, int64_t i) {
  if (v.tag == T_STR) return byte_str((unsigned char)v.s->bytes[i]);
  dt_fault(0, 0, "internal error: iteration over a list or map arrives with steps 5 and 6");
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

/* A growable buffer of bytes (malloc'ed, freed by the caller): the printed
   form of a value is built here, so a NUL in a string can't cut it short. */
typedef struct { char *p; size_t len, cap; } Buf;

static void buf_put(Buf *b, const char *s, size_t n) {
  if (b->len + n > b->cap) {
    size_t cap = b->cap == 0 ? 64 : b->cap;
    while (cap < b->len + n) cap *= 2;
    char *p = realloc(b->p, cap);
    if (p == NULL) dt_fault(0, 0, "out of memory");
    b->p = p;
    b->cap = cap;
  }
  if (n > 0) memcpy(b->p + b->len, s, n);
  b->len += n;
}

static void buf_str(Buf *b, const char *s) { buf_put(b, s, strlen(s)); }

/* Appends the printed form of v (LANGUAGE.md, str). `quoted` is true inside a
   list or map, and in `not a number`, where strings get quotes with \\ \" \n
   \t \r escaped and every other byte as it is (D24); lists and maps arrive
   with steps 5 and 6. */
static void put_value(Buf *b, Value v, bool quoted) {
  switch (v.tag) {
    case T_NIL: buf_str(b, "nil"); break;
    case T_BOOL: buf_str(b, v.b ? "true" : "false"); break;
    case T_INT: {
      char tmp[32];
      snprintf(tmp, sizeof tmp, "%" PRId64, v.i);
      buf_str(b, tmp);
      break;
    }
    case T_STR:
      if (!quoted) { buf_put(b, v.s->bytes, (size_t)v.s->len); break; }
      buf_put(b, "\"", 1);
      for (int64_t k = 0; k < v.s->len; k++) {
        char c = v.s->bytes[k];
        switch (c) {
          case '\\': buf_str(b, "\\\\"); break;
          case '"': buf_str(b, "\\\""); break;
          case '\n': buf_str(b, "\\n"); break;
          case '\t': buf_str(b, "\\t"); break;
          case '\r': buf_str(b, "\\r"); break;
          default: buf_put(b, &c, 1);
        }
      }
      buf_put(b, "\"", 1);
      break;
    default: dt_fault(0, 0, "internal error: cannot print tag %d", v.tag);
  }
}

/* The printed form of v as a string (`str`; an interpolated part). */
static Value to_str(Value v) {
  if (v.tag == T_STR) return v;
  Buf b = {NULL, 0, 0};
  put_value(&b, v, false);
  Value s = dt_str_new(b.p, (int64_t)b.len);
  free(b.p);
  return s;
}

Value dt_interp(int n, const Value *parts) {
  Value *strs = dt_alloc(sizeof(Value) * (size_t)(n > 0 ? n : 1));
  size_t total = 0;
  for (int i = 0; i < n; i++) {
    strs[i] = to_str(parts[i]);
    total += (size_t)strs[i].s->len;
  }
  struct Str *s = dt_alloc(sizeof(struct Str) + total + 1);
  s->len = (int64_t)total;
  size_t at = 0;
  for (int i = 0; i < n; i++) {
    memcpy(s->bytes + at, strs[i].s->bytes, (size_t)strs[i].s->len);
    at += (size_t)strs[i].s->len;
  }
  s->bytes[total] = '\0';
  return dt_str(s);
}

Value dt_b_print(int line, int col, int argc, const Value *argv) {
  (void)line;
  (void)col;
  Buf b = {NULL, 0, 0};
  for (int i = 0; i < argc; i++) {
    if (i > 0) buf_put(&b, " ", 1);
    put_value(&b, argv[i], false);
  }
  buf_put(&b, "\n", 1);
  fwrite(b.p, 1, b.len, stdout);
  free(b.p);
  return dt_nil();
}

/* Builtins on strings ----------------------------------------------------- */

/* `name: expected WHAT, got T` at the builtin's name. */
static _Noreturn void expected_fault(int line, int col, const char *name, const char *what, Value got) {
  dt_fault(line, col, "%s: expected %s, got %s", name, what, type_name(got));
}

Value dt_b_str(int line, int col, int argc, const Value *argv) {
  (void)line; (void)col; (void)argc;
  return to_str(argv[0]);
}

Value dt_b_len(int line, int col, int argc, const Value *argv) {
  (void)argc;
  Value v = argv[0];
  switch (v.tag) {
    case T_STR: return dt_int(v.s->len);
    case T_LIST: return dt_int(v.l->len);
    case T_MAP: return dt_int(v.m->len);
    default: expected_fault(line, col, "len", "a string, list or map", v);
  }
}

/* An optional -, then one or more decimal digits, all in range. */
bool dt_try_int(int line, int col, Value s, Value *out) {
  if (s.tag != T_STR) expected_fault(line, col, "int", "a string", s);
  const char *p = s.s->bytes;
  int64_t n = s.s->len, k = 0;
  bool neg = n > 0 && p[0] == '-';
  if (neg) k = 1;
  if (k == n) return false;
  /* Accumulate the magnitude as an unsigned number, so that the smallest int
     (whose magnitude is one more than the largest) is in range. */
  uint64_t limit = neg ? (uint64_t)INT64_MAX + 1 : (uint64_t)INT64_MAX, acc = 0;
  for (; k < n; k++) {
    if (p[k] < '0' || p[k] > '9') return false;
    uint64_t d = (uint64_t)(p[k] - '0');
    if (acc > (limit - d) / 10) return false;
    acc = acc * 10 + d;
  }
  *out = dt_int(neg ? (int64_t)(0 - acc) : (int64_t)acc);
  return true;
}

Value dt_b_int(int line, int col, int argc, const Value *argv) {
  (void)argc;
  Value out;
  if (dt_try_int(line, col, argv[0], &out)) return out;
  Buf b = {NULL, 0, 0};
  buf_str(&b, "not a number: ");
  put_value(&b, argv[0], true);
  fault_bytes(line, col, b.p, b.len);
}

static Value map_ascii(Value s, int from, int to, int delta) {
  Value r = dt_str_new(s.s->bytes, s.s->len);
  for (int64_t k = 0; k < r.s->len; k++) {
    int c = (unsigned char)r.s->bytes[k];
    if (c >= from && c <= to) r.s->bytes[k] = (char)(c + delta);
  }
  return r;
}

Value dt_b_lower(int line, int col, int argc, const Value *argv) {
  (void)argc;
  if (argv[0].tag != T_STR) expected_fault(line, col, "lower", "a string", argv[0]);
  return map_ascii(argv[0], 'A', 'Z', 'a' - 'A');
}

Value dt_b_upper(int line, int col, int argc, const Value *argv) {
  (void)argc;
  if (argv[0].tag != T_STR) expected_fault(line, col, "upper", "a string", argv[0]);
  return map_ascii(argv[0], 'a', 'z', 'A' - 'a');
}

Value dt_b_slice(int line, int col, int argc, const Value *argv) {
  (void)argc;
  Value x = argv[0];
  if (x.tag != T_STR) expected_fault(line, col, "slice", "a list or string", x);
  if (argv[1].tag != T_INT) expected_fault(line, col, "slice", "an int", argv[1]);
  if (argv[2].tag != T_INT) expected_fault(line, col, "slice", "an int", argv[2]);
  int64_t from = argv[1].i, to = argv[2].i, len = x.s->len;
  if (from < 0 || from > to || to > len) {
    dt_fault(line, col, "slice %" PRId64 "..%" PRId64 " out of range (length %" PRId64 ")", from, to, len);
  }
  return dt_str_new(x.s->bytes + from, to - from);
}

Value dt_b_read(int line, int col, int argc, const Value *argv) {
  (void)line; (void)col; (void)argc; (void)argv;
  Buf b = {NULL, 0, 0};
  char chunk[4096];
  size_t n;
  while ((n = fread(chunk, 1, sizeof chunk, stdin)) > 0) buf_put(&b, chunk, n);
  Value s = dt_str_new(b.p, (int64_t)b.len);
  free(b.p);
  return s;
}

Value dt_b_fail(int line, int col, int argc, const Value *argv) {
  (void)argc;
  Value s = to_str(argv[0]);
  fault_bytes(line, col, s.s->bytes, (size_t)s.s->len);
}

/* Lookups and membership --------------------------------------------------- */

bool dt_try_index(int line, int col, Value c, Value i, Value *out) {
  if (c.tag == T_STR) {
    if (i.tag != T_INT) dt_fault(line, col, "string index must be an int, got %s", type_name(i));
    if (i.i < 0 || i.i >= c.s->len) return false;
    *out = byte_str((unsigned char)c.s->bytes[i.i]);
    return true;
  }
  dt_fault(line, col, "cannot index %s", type_name(c));
}

Value dt_index(int line, int col, Value c, Value i) {
  Value out;
  if (dt_try_index(line, col, c, i, &out)) return out;
  dt_fault(line, col, "index %" PRId64 " out of range (length %" PRId64 ")", i.i, c.s->len);
}

bool dt_in(int line, int col, Value x, Value c) {
  if (x.tag == T_STR && c.tag == T_STR) {
    int64_t n = x.s->len, m = c.s->len;
    for (int64_t k = 0; k + n <= m; k++) {
      if (n == 0 || memcmp(c.s->bytes + k, x.s->bytes, (size_t)n) == 0) return true;
    }
    return false;
  }
  type_fault2(line, col, "in", x, c);
}
