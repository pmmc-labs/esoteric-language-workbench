# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my @a = (1, 2);
my $r = \@a;
for my $x (@a) {
    $r->[0] = 5;
    last;
}
say(2);
