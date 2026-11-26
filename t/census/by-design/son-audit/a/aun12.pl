use v5.42;
our $g = 1; sub r { $g } sub w { $g = 5 } my $a = r(); w(); my $b = r(); print "$a $b $g\n";
