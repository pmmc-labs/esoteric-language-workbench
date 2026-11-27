# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = {a => 1};
my $s = $r;
my @l = map { $s->{b} = 2 } ($r->{a});
say(2);
