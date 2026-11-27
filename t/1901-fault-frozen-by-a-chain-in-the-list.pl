# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [7, 8];
for my $x ($r->[0], $r->[1]) {
    my $s = $r;
    $s->[0] = 9;
    last;
}
say(2);
