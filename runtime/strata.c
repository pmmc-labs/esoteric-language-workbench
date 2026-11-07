#include "strata.h"
#include <stdio.h>
#include <stdlib.h>

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

strata_atom strata_top(strata_hist h, int line, int col) {
  if (h == NULL) strata_fault(line, col, "empty history");
  return h->atom;
}

static int64_t top_num(strata_hist h, int line, int col) {
  strata_atom a = strata_top(h, line, col);
  if (a.is_str) strata_fault(line, col, "expected a number, got a string");
  return a.v.n;
}

static void print_top(strata_hist h, int line, int col) {
  strata_atom a = strata_top(h, line, col);
  if (a.is_str) fwrite(a.v.s->bytes, 1, (size_t)a.v.s->len, stdout);
  else printf("%lld", (long long)a.v.n);
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
  int64_t x = top_num(a, line, col);
  int64_t y = top_num(b, line, col);
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

#define COMPARISON(name, op) \
  strata_hist name(strata_hist a, strata_hist b, int line, int col) { \
    int64_t x = top_num(a, line, col); \
    int64_t y = top_num(b, line, col); \
    return strata_num(x op y); \
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
