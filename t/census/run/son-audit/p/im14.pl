use v5.42;
my $c = 0; my @a = map { $c++; $_ * 2 } 1..3; print "$c @a\n";
