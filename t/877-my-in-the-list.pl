# kind: refused
# A list assignment is a statement (D78).
use v5.42;
for my $x (my @b = (1, 2)) {
    say $x;
}
