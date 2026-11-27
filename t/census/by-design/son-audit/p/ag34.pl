use v5.42;
my $r = []; sub f { $r->[0] = 5; "" } my @l = ($r->[0], f()); print $l[0] // "u", "\n";
