use v5.42;
our $g=1; my %h = (a => $g, b => $g++); print "$h{a}$h{b}\n";
