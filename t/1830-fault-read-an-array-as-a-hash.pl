# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $x = [1];
say(defined($x->{a}) ? 1 : 0);
say(2);
