# kind: refused
# perl pushes the element as grow left it (T157, D76).
use v5.42;
my @a = (1, 2, 3);
sub grow() { $a[0] = 7; return 1; }
push @a, $a[0], grow();
say $a[3];
