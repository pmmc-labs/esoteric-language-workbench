use v5.42;
our $g = 1; sub b { $g = 5 } b(); { local $g = 2; print "$g\n"; } print "$g\n";
