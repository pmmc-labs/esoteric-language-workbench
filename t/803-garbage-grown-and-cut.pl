# env: CURLY_GC_STRESS=0 CURLY_GC_POISON=0 CURLY_HEAP_CAP=16777216
# A string grown a kilobyte at a time to 400 KB and cut back, fifteen
# times: every step makes a new string and leaves the old one, more than
# a gigabyte in all, and never more than two of them at once.
use v5.42;
my $s = "";
my $grown = 0;
for (my $round = 0; $round < 15; $round++) {
    while (length($s) < 400000) {
        $s .= "0123456789" x 100;
    }
    $grown += length $s;
    $s = substr($s, 0, 1000 + $round);
}
say $grown;
say length $s;
say substr($s, 990);
