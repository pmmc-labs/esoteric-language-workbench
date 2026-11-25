# kind: refused
# perl warns: Found = in conditional, should be == (T112, D53).
use v5.42;
if (my $x = 5) {
    say $x;
}
