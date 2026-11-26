use v5.42;
my @a=("a b","c d"); for my $x (@a) { ($x)=split " ", $x } print "@a\n";
