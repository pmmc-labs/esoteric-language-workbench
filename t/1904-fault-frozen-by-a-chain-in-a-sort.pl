# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [2, 1];
my $s = $r;
my @l = sort { $s->[0] = 3; $a <=> $b } ($r->[0], $r->[1]);
say(2);
