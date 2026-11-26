use v5.42;
our $g = 1; do { local $g = 2; 1 }; print "$g\n";
