use v5.42;
my $h={a=>1}; my %c=%$h; delete $h->{a}; print join(",", %c), "\n";
