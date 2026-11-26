use v5.42;
my @s; for my $i (1..3) { push @s, sub { $i } } print join(",", map { $_->() } @s), "\n";
