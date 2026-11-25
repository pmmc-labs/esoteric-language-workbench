# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=16777216
# Small strings made of numbers, six million of them: a number where a
# string is wanted makes no string of its own (D66), and what the dots
# make is garbage each time round.
use v5.42;
my $s = "";
my $sum = 0;
for (my $i = 0; $i < 2000000; $i++) {
    $s = $i . ":" . $i * 1.5 . ":" . ($i % 7 == 0);
    $sum += length $s;
}
say $sum;
say $s;
