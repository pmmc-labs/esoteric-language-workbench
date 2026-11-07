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
