use v5.42;
our $g=1; print $g, local $g = 5; print "\n";
