# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1];
for my $x ($r->[3]) {
}
say(2);
