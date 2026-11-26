use v5.42;
our $g = 0; my $z = ($g = 5) + ($g = 7) + $g; print "$z $g\n";
