# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my @a = ([1, 2]);
for my $x ($a[0][0], $a[0][1]) {
    my $in = $a[0];
    $in->[1] = 3;
    last;
}
say(2);
