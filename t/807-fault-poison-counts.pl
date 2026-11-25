# kind: fault
# env: CURLY_GC_STRESS=1 CURLY_GC_POISON=1 CURLY_HEAP_CAP=2000000
# Under poison a collected string's memory is never handed out again, and
# it counts toward the cap (D65): three megabytes of garbage under a cap
# of two is out of memory, though nothing is alive. A cap on the living
# alone would never stop a program that runs away under poison.
use v5.42;
my $total = 0;
for (my $i = 0; $i < 3000; $i++) {
    say $i if $i % 500 == 0;
    $total += length(("x" x 1000) . $i);
}
say $total;
