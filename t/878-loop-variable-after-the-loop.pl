# kind: refused
# The variable is the loop's: perl does not compile this either.
use v5.42;
for my $x (1, 2) {
    say $x;
}
say $x;
