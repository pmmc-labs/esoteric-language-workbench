# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
say("a" lt $r ? 1 : 0);
say(2);
