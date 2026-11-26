use v5.42;
my @a=("ab","cd"); for my $x (@a) { $x =~ tr/a-d/A-D/ } print "@a\n";
