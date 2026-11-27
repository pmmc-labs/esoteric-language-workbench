# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my @a = (undef, 1);
for my $x (@a) {
    $a[0][0] = 1;
    last;
}
say(2);
