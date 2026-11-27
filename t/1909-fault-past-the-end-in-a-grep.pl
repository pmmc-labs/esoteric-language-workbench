# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
my @g = grep { 1 } ($r->[0], $r->[2]);
say(2);
