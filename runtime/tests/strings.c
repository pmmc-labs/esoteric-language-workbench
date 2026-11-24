// What a compiled program can't see of a string: its bytes beside its
// characters, and the NUL after the last, which the runtime's own reading
// of a number from a string relies on.
#include <stdio.h>
#include "rt.h"

static void show(const char *what, rt_value v) {
    printf("%s: %d bytes, %d character%s\n", what, (int)v.as.s->len, (int)v.as.s->chars, v.as.s->chars == 1 ? "" : "s");
}

static const rt_str nul = { 3, 3, "a\000b" };
static const rt_str empty = { 0, 0, "" };

static void body(rt_ctx *cx) {
    rt_value e = rt_chr(cx, rt_int(233));
    rt_value smile = rt_chr(cx, rt_int(9786));
    rt_value grin = rt_chr(cx, rt_int(128512));
    show("chr 233", e);
    show("chr 9786", smile);
    show("chr 128512", grin);
    rt_value joined = rt_concat(cx, rt_concat(cx, rt_concat(cx, e, smile), grin), rt_int(7));
    show("joined", joined);
    show("repeated", rt_repeat(cx, joined, rt_int(3)));
    show("substr 1, 2", rt_substr3(cx, joined, rt_int(1), rt_int(2)));
    printf("index of the last: %d\n", (int)rt_index2(cx, joined, rt_int(7)).as.i);
    show("a NUL in the middle", rt_concat(cx, rt_string(&nul), rt_string(&empty)));
    rt_value twelve = rt_concat(cx, rt_int(12), rt_string(&empty));
    show("12 as a string", twelve);
    printf("a literal ends with a NUL that is not its own: %d\n", twelve.as.s->bytes[twelve.as.s->len]);
}

int main(void) {
    return rt_run(body, "strings.pl");
}
