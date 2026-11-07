#ifndef STRATA_H
#define STRATA_H
#include <stdint.h>
#include <stddef.h>

/* Immutable byte string, allocated from the arena. */
typedef struct { int64_t len; char bytes[]; } strata_str;

/* An atom: a number or a string (D10). */
typedef struct {
  int is_str;
  union { int64_t n; const strata_str *s; } v;
} strata_atom;

/* A history is a pointer to its top layer; NULL is empty (DESIGN.md,
   "Values and memory"). `below` is shared, never copied or changed. */
typedef struct strata_layer {
  strata_atom atom;
  const struct strata_layer *below;
  int64_t depth;
} strata_layer;
typedef const strata_layer *strata_hist;

void *strata_alloc(size_t n);
strata_hist strata_push(strata_hist below, strata_atom a);
strata_hist strata_num(int64_t n);               /* one-layer history */
strata_atom strata_top(strata_hist h, int line, int col);
void strata_print(strata_hist h, int line, int col);

/* D23: flush stdout, print "fault at L:C: msg" to stderr, exit 1. */
void strata_fault(int line, int col, const char *msg);

#endif
