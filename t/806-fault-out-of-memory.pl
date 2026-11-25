# kind: fault
# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=65536
# A string that doubles, under a cap of 64 KB: at 32768 it and the one it
# was made from fit, and the next would be 65536 beside its 32768. What is
# held is what is alive: the smaller ones before are garbage, and a cap
# that counted them would stop sooner. perl goes on to a megabyte.
use v5.42;
my $s = "ab";
for (my $k = 0; $k < 19; $k++) {
    $s .= $s;
    say length $s;
}
