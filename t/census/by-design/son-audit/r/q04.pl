use v5.42;
use feature "state"; for my $i (1..3) { state $t=0; $t+=$i; print $t } print "\n";
