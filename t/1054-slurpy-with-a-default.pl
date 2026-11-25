# kind: refused
# perl: A slurpy parameter may not have a default value (T182).
use v5.42;
sub f(@r = (1)) {
    return 1;
}
say f(1);
