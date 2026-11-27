# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $x = [5];
$x->[0][1] = 1;
say(2);
