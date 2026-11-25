# kind: refused
# The outer loop's variable, changed in the inner loop.
use v5.42;
my @a = (1, 2);
for my $x (@a) {
    for my $y (1, 2) {
        $x += $y;
    }
}
say @a;
