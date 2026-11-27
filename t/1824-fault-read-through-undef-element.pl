# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1, undef];
say($r->[1]{k});
say(2);
