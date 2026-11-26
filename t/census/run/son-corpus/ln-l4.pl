use v5.42;
my $h = {a => 1, b => 2}; print join(",", @{$h}{qw(a b)}), "\n";
