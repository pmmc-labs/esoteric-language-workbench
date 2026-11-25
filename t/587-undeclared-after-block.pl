# kind: refused
# A my ends with its block. perl doesn't compile it.
use v5.42;
if (1) {
    my $x = 1;
}
say $x;
