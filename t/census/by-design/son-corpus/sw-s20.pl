use v5.42;
sub f { my @o; for my $x (reverse @_) { next if $x eq "b"; push @o, $x } "@o" } print f(qw(a b c)), "\n";
