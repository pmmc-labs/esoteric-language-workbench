use v5.42;
our $x=1; sub g { $x++ } print "$x", g(), "$x", "\n";
