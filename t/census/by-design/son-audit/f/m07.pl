use v5.42;
my %h=(a=>"x\n"); chomp(%h); print "$h{a}|\n";
