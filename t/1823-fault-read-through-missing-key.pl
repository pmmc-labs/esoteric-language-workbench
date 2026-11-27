# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $h = {};
my $x = $h->{a}{b};
say(2);
