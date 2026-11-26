use v5.42;
use feature "try"; no warnings; my $x=0; try { die "a\n" } catch ($e) { $x=$e } print "$x";
