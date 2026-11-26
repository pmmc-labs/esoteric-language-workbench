use v5.42;
my @a=(1,2); sub z { print $a[0] } for my $x (@a) { $x=5; z() } print "\n";
