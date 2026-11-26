use v5.42;
my @a=(1,2,3); my $s=""; for my $i (reverse 0..$#a) { $s.=$a[$i]; pop @a } print "$s", scalar(@a), "\n";
