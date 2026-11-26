use v5.42;
my $x=1; ($x ||= 7) += 1; print "$x\n";
