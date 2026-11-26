use v5.42;
sub f { my @o; for my $x (@_) { next unless length $x > 1; push @o, uc $x } "@o" } print f(qw(ab c de)), "\n";
