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

void strata_print(strata_hist h, int line, int col) {
  strata_atom a = strata_top(h, line, col);
  if (a.is_str) {
    fwrite(a.v.s->bytes, 1, (size_t)a.v.s->len, stdout);
    putchar('\n');
  } else {
    printf("%lld\n", (long long)a.v.n);
  }
}
