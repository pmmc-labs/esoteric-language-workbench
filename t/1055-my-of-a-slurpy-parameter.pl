# kind: refused
# A my of a parameter's name, in the sub's own block (T141): perl warns.
use v5.42;
sub f(@v) {
    my @v = (1);
    return 1;
}
say f(1);
