use v5.42;
my @a = (1,2,3); my ($x, $y) = @a[0,1]; @a[0,1] = ($y, $x); print "@a\n";
