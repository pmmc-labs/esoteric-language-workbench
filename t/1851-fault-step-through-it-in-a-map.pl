# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my @m = (undef);
my @n = map { $_->[0]++ } @m;
say(2);
