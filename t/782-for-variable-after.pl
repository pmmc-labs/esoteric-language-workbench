# kind: refused
# A my in a for's first part ends with the loop. perl doesn't compile it.
use v5.42;
for (my $k = 0; $k < 3; $k++) {
    say $k;
}
say $k;
