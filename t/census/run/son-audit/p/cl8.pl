use v5.42;
my @subs; for my $i (1..3) { push @subs, sub { $i * 10 } } print join(",", map { $_->() } @subs), "\n";
