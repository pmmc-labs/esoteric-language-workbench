use v5.42;
my %h; delete $h{a}{b}; print exists $h{a} ? 1 : 0, "\n";
