# kind: fault
# model: t/models/ref.py
use v5.42;
say(1);
my @l = (undef, undef);
for my $x (@l) {
    $x->[0] = 1;
}
say(2);
