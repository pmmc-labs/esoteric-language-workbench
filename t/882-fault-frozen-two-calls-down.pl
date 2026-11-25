# kind: fault
# A loop in one sub, the change in a sub that a sub it calls calls; and
# before it, a return from inside two loops over the array, which gives
# it back twice. By hand.
use v5.42;
my @a = (1, 2, 3);
sub change($v) {
    $a[0] = $v;
    return $v;
}
sub middle($v) {
    return change($v) + 1;
}
sub pair() {
    for my $x (@a) {
        for my $y (@a) {
            return $x + $y if $y == 2;
        }
    }
    return 0;
}
sub over() {
    for my $x (@a) {
        say $x;
        middle($x * 10);
    }
    return 0;
}
say pair();
say middle(5);
say $a[0];
over();
say 2;
