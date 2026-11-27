# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
my @s = sort { $r } (1, 2);
say(2);
