# env: CURLY_GC_STRESS=1 CURLY_GC_POISON=0 CURLY_HEAP_CAP=16777216
# What must not be freed: a string made once and held in a variable
# through a million collections (one at every allocation), read each time
# round and at the end; and one handed from an inner variable to an outer
# one as its block ends.
use v5.42;
my $kept = "kept: " . ("k" x 1000);
my $outer = "";
my $sum = 0;
for (my $i = 0; $i < 300000; $i++) {
    my $inner = $kept . $i;
    $sum += length $inner;
    $outer = substr($inner, 0, 10) . $i if $i % 1000 == 0;
    {
        my $deep = $outer . "!";
        $outer = $deep if $i == 299999;
    }
}
say $sum;
say length $kept;
say substr($kept, 0, 12);
say $outer;
