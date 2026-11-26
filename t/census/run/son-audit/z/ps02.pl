use v5.42;
my @a=("a","b"); for my $x (@a) { $x=~tr/a-b/A-B/ } print "@a\n";
