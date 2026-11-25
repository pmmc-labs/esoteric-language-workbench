# kind: refused
# perl takes the ! of a condition away and tests the other way, so it
# warns here too: Found = in conditional (T112, D53).
use v5.42;
my $x = 0;
if (!($x = 5)) {
    say $x;
}
