// The built runtime, with a fault that longjmps and output into a buffer,
// behind an interface ctypes can call. Nothing of the runtime's rules is
// changed: rt_patched.c is rt.c with rt_fault's body and emit's two writes
// replaced.
#include <setjmp.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
static jmp_buf m_jmp;
static const char *m_msg = "";
static char *m_buf = NULL;
static size_t m_len = 0, m_cap = 0;
__attribute__((noreturn)) static void m_fault(const char *what) { m_msg = what; longjmp(m_jmp, 1); }
static void m_write(const char *p, size_t n) {
    if (m_len + n + 1 > m_cap) { m_cap = (m_len + n + 1) * 2; m_buf = realloc(m_buf, m_cap); }
    memcpy(m_buf + m_len, p, n); m_len += n;
}
#include "rt_patched.c"
static rt_ctx m_cx = { "model", 0, 0, NULL };
typedef rt_value V;
const char *m_what(void) { return m_msg; }
void m_reset(void) { release(&m_cx); m_len = 0; }
const char *m_out(long *len) { *len = (long)m_len; return m_buf; }
void m_mkstr(const char *bytes, long len, V *out) {
    char *p; const rt_str *s = str_new(&m_cx, (uint64_t)len, (uint64_t)len, &p);
    memcpy(p, bytes, (size_t)len); *out = rt_string(s);
}
const char *m_strbytes(const V *v, long *len) { *len = (long)v->as.s->len; return v->as.s->bytes; }
enum { ADD=1, SUB, MUL, DIV, MOD, POW, NEG, CONCAT, REPEAT, LENGTH, UC, LC, ORD, CHR, SUBSTR2, SUBSTR3, INDEX2, INDEX3,
       NOT, XOR, DEFINED, NEQ, NNE, NLT, NGT, NLE, NGE, NCMP, SEQ, SNE, SLT, SGT, SLE, SGE, SCMP };
int m_op(int op, const V *a, const V *b, const V *c, V *out) {
    if (setjmp(m_jmp)) return 1;
    rt_ctx *cx = &m_cx;
    switch (op) {
    case ADD: *out = rt_add(cx, *a, *b); break;
    case SUB: *out = rt_sub(cx, *a, *b); break;
    case MUL: *out = rt_mul(cx, *a, *b); break;
    case DIV: *out = rt_div(cx, *a, *b); break;
    case MOD: *out = rt_mod(cx, *a, *b); break;
    case POW: *out = rt_pow(cx, *a, *b); break;
    case NEG: *out = rt_neg(cx, *a); break;
    case CONCAT: *out = rt_concat(cx, *a, *b); break;
    case REPEAT: *out = rt_repeat(cx, *a, *b); break;
    case LENGTH: *out = rt_length(cx, *a); break;
    case UC: *out = rt_uc(cx, *a); break;
    case LC: *out = rt_lc(cx, *a); break;
    case ORD: *out = rt_ord(cx, *a); break;
    case CHR: *out = rt_chr(cx, *a); break;
    case SUBSTR2: *out = rt_substr2(cx, *a, *b); break;
    case SUBSTR3: *out = rt_substr3(cx, *a, *b, *c); break;
    case INDEX2: *out = rt_index2(cx, *a, *b); break;
    case INDEX3: *out = rt_index3(cx, *a, *b, *c); break;
    case NOT: *out = rt_not(cx, *a); break;
    case XOR: *out = rt_xor(cx, *a, *b); break;
    case DEFINED: *out = rt_defined(cx, *a); break;
    case NEQ: *out = rt_num_eq(cx, *a, *b); break;
    case NNE: *out = rt_num_ne(cx, *a, *b); break;
    case NLT: *out = rt_num_lt(cx, *a, *b); break;
    case NGT: *out = rt_num_gt(cx, *a, *b); break;
    case NLE: *out = rt_num_le(cx, *a, *b); break;
    case NGE: *out = rt_num_ge(cx, *a, *b); break;
    case NCMP: *out = rt_num_cmp(cx, *a, *b); break;
    case SEQ: *out = rt_str_eq(cx, *a, *b); break;
    case SNE: *out = rt_str_ne(cx, *a, *b); break;
    case SLT: *out = rt_str_lt(cx, *a, *b); break;
    case SGT: *out = rt_str_gt(cx, *a, *b); break;
    case SLE: *out = rt_str_le(cx, *a, *b); break;
    case SGE: *out = rt_str_ge(cx, *a, *b); break;
    case SCMP: *out = rt_str_cmp(cx, *a, *b); break;
    default: m_msg = "model: no such op"; return 1;
    }
    return 0;
}
int m_truth(const V *a, int *out) { if (setjmp(m_jmp)) return 1; *out = rt_is_true(&m_cx, *a); return 0; }
int m_emit(const V *a, int newline) { if (setjmp(m_jmp)) return 1; if (newline) rt_say(&m_cx, *a); else rt_print(&m_cx, *a); return 0; }
// A string (or any value) where a number is wanted, by the runtime's own rule:
// is_int and i, or n; and the double either way.
int m_numeric(const V *a, int *is_int, long long *i, double *n, double *as_dbl) {
    if (setjmp(m_jmp)) return 1;
    number x = numeric(&m_cx, *a);
    *is_int = x.is_int; *i = x.i; *n = x.n; *as_dbl = as_double(x);
    return 0;
}
