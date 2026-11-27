# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $x = {};
say(defined($x->[0]) ? 1 : 0);
say(2);
