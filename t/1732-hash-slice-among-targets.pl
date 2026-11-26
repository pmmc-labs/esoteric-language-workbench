# kind: refused
# perl takes it: 7 8 3. One target, here (D100).
use v5.42;
my @a = (1, 2, 3);
(@a[0, 1], my $z) = (7, 8, 9);
say "@a";
