use v5.42;
our $x = 5; { my $x = $x + 1; print $x } print "$x\n";
