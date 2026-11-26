use v5.42;
my $x=0; ($x ||= 5) = 7; print "$x\n";
