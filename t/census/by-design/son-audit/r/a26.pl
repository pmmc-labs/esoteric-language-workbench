use v5.42;
our $g=0; sub inc { $g++ } for my $i (1..3) { inc(); print $g; } print "\n";
