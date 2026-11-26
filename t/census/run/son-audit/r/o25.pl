use v5.42;
my $x=1; { my $x=2; { my $x=3 } print $x } print "$x\n";
