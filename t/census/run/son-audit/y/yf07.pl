use v5.42;
sub f {} my $x; f($x->{a}); print ref($x), exists $x->{a} ? 1 : 0, "\n";
