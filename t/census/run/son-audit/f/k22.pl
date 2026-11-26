use v5.42;
my $x=1; sub { $x=shift }->(7); print "$x\n";
