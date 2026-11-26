use v5.42;
sub f {} my %h; f($h{a}); print exists $h{a} ? 1 : 0, "\n";
