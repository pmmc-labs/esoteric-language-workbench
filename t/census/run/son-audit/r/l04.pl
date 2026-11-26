use v5.42;
my @a=(1,2,3,4); my $f; for my $x (@a) { if ($x==3) { $f=$x; last } } print defined $f ? $f : "u", "\n";
