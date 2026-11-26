use v5.42;
sub f { return wantarray ? "l" : "s" } my $x = eval { f() }; my @y = eval { f() }; print "$x@y\n";
