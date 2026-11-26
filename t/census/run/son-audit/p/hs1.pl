use v5.42;
my %h = (a => 1); print %h ? "t" : "f"; delete $h{a}; print %h ? "t" : "f", "\n";
