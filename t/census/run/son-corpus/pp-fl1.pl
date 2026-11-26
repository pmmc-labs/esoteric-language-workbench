use v5.42;
my %h = (a => 1, b => 2); my @k = (sort(keys %h), "z"); print scalar(@k), "\n";
