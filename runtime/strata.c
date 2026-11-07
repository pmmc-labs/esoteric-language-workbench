#include "strata.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The arena (D26): 1 MiB chunks chained from a global, never freed. The
   global keeps LeakSanitizer quiet. */
#define CHUNK (1u << 20)
typedef struct chunk { struct chunk *next; size_t used, size; } chunk;
static chunk *arena;

static void out_of_memory(void) {
  fflush(stdout);
  fputs("fault: out of memory\n", stderr);
  exit(1);
}

void *strata_alloc(size_t n) {
  n = (n + 15) & ~(size_t)15;
  size_t head = (sizeof(chunk) + 15) & ~(size_t)15;
  if (arena == NULL || arena->size - arena->used < n) {
    size_t size = n + head > CHUNK ? n + head : CHUNK;
    chunk *c = malloc(size);
    if (c == NULL) out_of_memory();
    c->size = size;
    c->used = head;
    c->next = arena;
    arena = c;
  }
  void *p = (char *)arena + arena->used;
  arena->used += n;
  return p;
}

strata_hist strata_push(strata_hist below, strata_atom a) {
  strata_layer *l = strata_alloc(sizeof *l);
  l->atom = a;
  l->below = below;
  l->depth = below ? below->depth + 1 : 1;
  return l;
}

strata_hist strata_num(int64_t n) {
  strata_atom a;
  a.is_str = 0;
  a.v.n = n;
  return strata_push(NULL, a);
}

void strata_fault(int line, int col, const char *msg) {
  fflush(stdout);
  fprintf(stderr, "fault at %d:%d: %s\n", line, col, msg);
  exit(1);
}

static int depth;

void strata_enter(int line, int col) {
  if (depth >= 10000) strata_fault(line, col, "recursion too deep");
  depth++;
}

void strata_leave(void) { depth--; }

strata_atom strata_top(strata_hist h, int line, int col) {
  if (h == NULL) strata_fault(line, col, "empty history");
  return h->atom;
}

static int64_t top_num(strata_hist h, int line, int col) {
  strata_atom a = strata_top(h, line, col);
  if (a.is_str) strata_fault(line, col, "expected a number, got a string");
  return a.v.n;
}

static strata_hist str_hist(const char *bytes, int64_t len) {
  strata_str *s = strata_alloc(sizeof *s + (size_t)len);
  s->len = len;
  if (len > 0) memcpy(s->bytes, bytes, (size_t)len);
  strata_atom a;
  a.is_str = 1;
  a.v.s = s;
  return strata_push(NULL, a);
}

strata_hist strata_lit(const char *bytes, int64_t len) {
  return str_hist(bytes, len);
}

static const strata_str *top_str(strata_hist h, int line, int col) {
  strata_atom a = strata_top(h, line, col);
  if (!a.is_str) strata_fault(line, col, "expected a string, got a number");
  return a.v.s;
}

strata_hist strata_len(strata_hist s, int line, int col) {
  return strata_num(top_str(s, line, col)->len);
}

/* The string first, then the index, then the range. */
strata_hist strata_char_at(strata_hist s, strata_hist i, int line, int col) {
  const strata_str *str = top_str(s, line, col);
  int64_t n = top_num(i, line, col);
  if (n < 0 || n >= str->len) {
    char msg[96];
    snprintf(msg, sizeof msg, "index out of range (index %lld, length %lld)",
             (long long)n, (long long)str->len);
    strata_fault(line, col, msg);
  }
  return str_hist(str->bytes + n, 1);
}

strata_hist strata_to_str(strata_hist n, int line, int col) {
  char buf[32];
  int len = snprintf(buf, sizeof buf, "%lld", (long long)top_num(n, line, col));
  return str_hist(buf, len);
}

/* Both tops, a's first. Same kinds are fine; different kinds are the
   fault `mismatched types` in operand order (D21). Returns 1 for strings. */
static int same_kind(strata_atom x, strata_atom y, int line, int col) {
  if (x.is_str != y.is_str)
    strata_fault(line, col, x.is_str ? "mismatched types: string and number"
                                     : "mismatched types: number and string");
  return x.is_str;
}

static void print_top(strata_hist h, int line, int col) {
  strata_atom a = strata_top(h, line, col);
  if (a.is_str) fwrite(a.v.s->bytes, 1, (size_t)a.v.s->len, stdout);
  else printf("%lld", (long long)a.v.n);
}

strata_hist strata_lay(strata_hist h, strata_hist e, int line, int col) {
  return strata_push(h, strata_top(e, line, col));
}

strata_hist strata_depth(strata_hist h, int line, int col) {
  (void)line; (void)col;
  return strata_num(h ? h->depth : 0);
}

strata_hist strata_at(strata_hist h, strata_hist k, int line, int col) {
  int64_t n = top_num(k, line, col);
  int64_t depth = h ? h->depth : 0;
  if (n < 0 || n > depth) {
    char msg[96];
    snprintf(msg, sizeof msg, "@ out of range (index %lld, depth %lld)",
             (long long)n, (long long)depth);
    strata_fault(line, col, msg);
  }
  for (int64_t i = 0; i < n; i++) h = h->below;
  return h;
}

void strata_print(strata_hist h, int line, int col) {
  print_top(h, line, col);
  putchar('\n');
}

void strata_write(strata_hist h, int line, int col) {
  print_top(h, line, col);
}

/* Each overflow test is computed in a statement of its own, from operands
   already known to be in range, so the check itself never overflows. */
static void check(int overflow, int line, int col) {
  if (overflow) strata_fault(line, col, "integer overflow");
}

strata_hist strata_add(strata_hist a, strata_hist b, int line, int col) {
  strata_atom ax = strata_top(a, line, col);
  strata_atom bx = strata_top(b, line, col);
  if (same_kind(ax, bx, line, col)) {
    int64_t la = ax.v.s->len, lb = bx.v.s->len;
    strata_str *s = strata_alloc(sizeof *s + (size_t)(la + lb));
    s->len = la + lb;
    memcpy(s->bytes, ax.v.s->bytes, (size_t)la);
    memcpy(s->bytes + la, bx.v.s->bytes, (size_t)lb);
    strata_atom r;
    r.is_str = 1;
    r.v.s = s;
    return strata_push(NULL, r);
  }
  int64_t x = ax.v.n;
  int64_t y = bx.v.n;
  int over = (y > 0 && x > INT64_MAX - y) || (y < 0 && x < INT64_MIN - y);
  check(over, line, col);
  return strata_num(x + y);
}

strata_hist strata_sub(strata_hist a, strata_hist b, int line, int col) {
  int64_t x = top_num(a, line, col);
  int64_t y = top_num(b, line, col);
  int over = (y < 0 && x > INT64_MAX + y) || (y > 0 && x < INT64_MIN + y);
  check(over, line, col);
  return strata_num(x - y);
}

strata_hist strata_mul(strata_hist a, strata_hist b, int line, int col) {
  int64_t x = top_num(a, line, col);
  int64_t y = top_num(b, line, col);
  int over = 0;
  if (x > 0) over = y > 0 ? x > INT64_MAX / y : y < INT64_MIN / x;
  else if (x < 0) over = y > 0 ? x < INT64_MIN / y : y < INT64_MAX / x;
  check(over, line, col);
  return strata_num(x * y);
}

strata_hist strata_div(strata_hist a, strata_hist b, int line, int col) {
  int64_t x = top_num(a, line, col);
  int64_t y = top_num(b, line, col);
  if (y == 0) strata_fault(line, col, "division by zero");
  int over = x == INT64_MIN && y == -1;
  check(over, line, col);
  return strata_num(x / y);
}

/* The minimum % -1 is 0 in C only on paper (the hardware traps), and D19
   makes it an overflow so that % agrees with /. */
strata_hist strata_mod(strata_hist a, strata_hist b, int line, int col) {
  int64_t x = top_num(a, line, col);
  int64_t y = top_num(b, line, col);
  if (y == 0) strata_fault(line, col, "division by zero");
  int over = x == INT64_MIN && y == -1;
  check(over, line, col);
  return strata_num(x % y);
}

strata_hist strata_neg(strata_hist a, int line, int col) {
  int64_t x = top_num(a, line, col);
  int over = x == INT64_MIN;
  check(over, line, col);
  return strata_num(-x);
}

/* -1, 0, 1: bytewise as unsigned bytes, a prefix first. */
static int cmp_str(const strata_str *x, const strata_str *y) {
  int64_t n = x->len < y->len ? x->len : y->len;
  int c = n > 0 ? memcmp(x->bytes, y->bytes, (size_t)n) : 0;
  if (c != 0) return c < 0 ? -1 : 1;
  return x->len < y->len ? -1 : x->len > y->len;
}

#define COMPARISON(name, op) \
  strata_hist name(strata_hist a, strata_hist b, int line, int col) { \
    strata_atom x = strata_top(a, line, col); \
    strata_atom y = strata_top(b, line, col); \
    if (same_kind(x, y, line, col)) return strata_num(cmp_str(x.v.s, y.v.s) op 0); \
    return strata_num(x.v.n op y.v.n); \
  }
COMPARISON(strata_eq, ==)
COMPARISON(strata_ne, !=)
COMPARISON(strata_lt, <)
COMPARISON(strata_le, <=)
COMPARISON(strata_gt, >)
COMPARISON(strata_ge, >=)

int strata_truth(strata_hist a, int line, int col) {
  return top_num(a, line, col) != 0;
}

strata_hist strata_not(strata_hist a, int line, int col) {
  return strata_num(!strata_truth(a, line, col));
}
