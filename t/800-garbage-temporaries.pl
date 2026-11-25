# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=16777216
# A gigabyte of strings, a kilobyte at a time, each a temporary of one
# expression, under a cap of 16 MB (D65): the program ends only if what it
# can no longer reach is freed. The knobs are off, so the ordinary policy
# is what frees it (D66).
use v5.42;
my $total = 0;
for (my $i = 0; $i < 1000000; $i++) {
    $total += length(("x" x 1000) . $i);
}
say $total;
