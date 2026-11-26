use v5.42;
sub inc { $_[0]++ } my @a=(1); inc($#a); print scalar(@a), "\n";
