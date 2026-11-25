# kind: refused
# What the first part declares is seen once the whole part has been
# read: perl doesn't compile this (T58).
use v5.42;
for (my $k = 0, my $m = $k + 9; $k < $m; $k++) {
    say $k;
}
