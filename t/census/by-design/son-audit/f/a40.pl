use v5.42;
my $x=1; sub g { $x++ } print $x, g(), $x, "\n";
