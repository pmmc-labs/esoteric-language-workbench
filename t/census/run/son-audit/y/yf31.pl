use v5.42;
my $r = {}; my @k = keys %{ $r->{h} }; print exists $r->{h} ? 1 : 0, "\n";
