use v5.42;
my %h = (a=>1); my @k = keys %h; $h{b} = 2; my @v = values %h; print scalar(@k), scalar(@v), "\n";
