# kind: dies
# The list joined with nothing between (T300).
use v5.42;
my @a = (1, 2);
die "a", @a, 1.5, true, "\x{41}";
