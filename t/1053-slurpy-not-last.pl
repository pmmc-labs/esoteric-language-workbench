# kind: refused
# perl: Slurpy parameter not last (T182).
use v5.42;
sub f(@r, $x) {
    return 1;
}
say f(1);
