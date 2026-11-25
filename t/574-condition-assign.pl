# kind: refused
# perl warns: Found = in conditional, should be == (T112, D53).
use v5.42;
my $x = 0;
if ($x = 5) {
    say $x;
}
