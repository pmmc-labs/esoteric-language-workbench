# kind: refused
# perl warns: "my" variable $k masks earlier declaration in same
# statement.
use v5.42;
for (my $k = 0, my $k = 3; $k < 5; $k++) {
    say $k;
}
