use v5.42;
our $g = "a"; { local $g = "b"; { local $g = "c"; print $g } print $g } print "$g\n";
