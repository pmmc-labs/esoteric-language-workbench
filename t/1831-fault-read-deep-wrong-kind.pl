# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $x = {a => [1, {b => 2}]};
say($x->{a}[1][0]);
say(2);
