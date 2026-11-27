use v5.42;
my %h; my $r = \$h{a}; print exists $h{a} ? 1 : 0, "\n";
