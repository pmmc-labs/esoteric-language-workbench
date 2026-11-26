use v5.42;
our @g = (1,2); my $c = [ @g ]; @g = (); print scalar(@$c), "\n";
