# kind: refused
# perl adds into the element that was shifted off, and two are left (T159, D76).
use v5.42;
my @a = (1, 2, 3);
$a[0] += shift(@a);
say scalar(@a);
