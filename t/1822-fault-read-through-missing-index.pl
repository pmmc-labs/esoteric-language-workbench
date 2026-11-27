# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [];
say(defined($r->[0][1]) ? 1 : 0);
say(2);
