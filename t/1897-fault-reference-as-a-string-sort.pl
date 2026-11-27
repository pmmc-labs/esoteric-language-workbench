# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
my @l = ($r, [2]);
my @s = sort @l;
say(2);
