use v5.42;
my %h=(a=>1); my @l=(%h); $h{a}=2; print join(",", @l), "\n";
