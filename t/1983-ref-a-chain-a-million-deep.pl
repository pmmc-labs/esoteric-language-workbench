# env: CURLY_GC_STRESS=200000
# A list linked a million deep, each array holding a reference to the one
# made before, and walked back to the end (step 13a): the collector, at
# every 200,000th allocation, walks it with a stack of its own, and a mark
# that used C's stack would need hundreds of megabytes of it.
use v5.42;
my $l;
for my $i (1 .. 1000000) {
    $l = [$l, $i];
}
say $l->[1];
my $n = 0;
while (defined($l)) {
    $l = $l->[0];
    $n++;
}
say $n;
