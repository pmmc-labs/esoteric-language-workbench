use v5.42;
my %h = (a => 1); print exists $h{a} ? "y" : "n", exists $h{z} ? "y" : "n", "\n";
