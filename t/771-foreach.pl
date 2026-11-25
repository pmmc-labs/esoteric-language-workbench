# kind: refused
# foreach is for, to perl, with three parts as with a list (T122).
use v5.42;
foreach (my $k = 0; $k < 3; $k++) {
    say $k;
}
