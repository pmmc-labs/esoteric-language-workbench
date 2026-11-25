# kind: fault
# The line is the return's, in the sub, and not the call's. By hand.
use v5.42;
my @a = (1, 2);
sub f($c) {
    if ($c) {
        return @a;
    }
    return 0;
}
say 1;
say f(0) + 1;
say f(1) + 1;
say 2;
