// The core: printing, faults, main. The runtime prints the program's
// value, then a newline, and exits 0; a fault goes to stderr and exits 1.
#include <stdio.h>
#include <stdlib.h>
#include "rt.h"

void rt_print(rt_value v) {
    if ((v & 1) == RT_INT_TAG) printf("%lld", (long long)(v >> RT_INT_SHIFT));
    else rt_fault("unknown value");
}

void rt_fault(const char *what) {
    fflush(stdout);
    fprintf(stderr, "fault: %s\n", what);
    exit(1);
}

int main(void) {
    rt_print(lang_main());
    putchar('\n');
    return 0;
}
