# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my $r = [1, 2];
sub poke($s) {
    $s->[1] = 0;
    return;
}
for my $x ($r->[0]) {
    poke($r);
}
say(2);
