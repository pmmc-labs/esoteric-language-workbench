use v5.42;
our $g=1; sub bump { $_[0] .= "!" } bump($g .= "a"); print "$g\n";
