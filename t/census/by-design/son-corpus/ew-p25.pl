use v5.42;
our $g = 1; { local $g = 2; print "$g " } print "$g\n";
