# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my ($r, $s);
($r || $s)->[0] = 5;
say(2);
