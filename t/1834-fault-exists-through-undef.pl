# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r;
say(exists($r->{a}) ? 1 : 0);
say(2);
