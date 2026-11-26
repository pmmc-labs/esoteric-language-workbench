use v5.42;
my $x="ab"; for (1..2) { $x =~ tr/ab/bc/ } print "$x\n";
