use v5.42;
sub f { my $s = ""; for my $x (@_) { $s .= "<$x>"; last if $x eq "b" } $s } print f(qw(a b c)), "\n";
