# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my @m = (undef);
$_->{n} = 1 for @m;
say(2);
