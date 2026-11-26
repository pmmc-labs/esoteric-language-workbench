use v5.42;
my $x=1; sub id { $_[0] } for (id($x)) { $_++ } print "$x\n";
