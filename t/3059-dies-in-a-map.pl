# kind: dies
# From the block of a map, the line of the block's statement.
use v5.42;
my @a = (1, 2, 3);
my @b = map {
    die "no $_" if $_ == 2;
    $_ * 2 } @a;
