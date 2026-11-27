# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = {a => 1};
for my $x ($r->{b}) {
}
say(2);
