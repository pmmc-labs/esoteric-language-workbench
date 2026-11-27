# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
my %h;
say(defined($h{$r}) ? 1 : 0);
say(2);
