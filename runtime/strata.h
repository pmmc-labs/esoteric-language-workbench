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
void strata_write(strata_hist h, int line, int col);

/* Operators take the top of each operand and give a one-layer history
   (D11). L, C is the operator's position, where a fault is reported (D23).
   Callers pass temporaries only, so argument order never matters (D25). */
strata_hist strata_add(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_sub(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_mul(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_div(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_mod(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_neg(strata_hist a, int line, int col);
strata_hist strata_eq(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_ne(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_lt(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_le(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_gt(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_ge(strata_hist a, strata_hist b, int line, int col);
strata_hist strata_not(strata_hist a, int line, int col);
/* The top as a condition: 0 or 1 (D20). Used by and/or, which the
   generated code short-circuits itself. */
int strata_truth(strata_hist a, int line, int col);

/* D23: flush stdout, print "fault at L:C: msg" to stderr, exit 1. */
void strata_fault(int line, int col, const char *msg);

#endif
