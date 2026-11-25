# kind: refused
# perl folds 0 && $y to 0 and warns: Found = in conditional (T112).
# Found by the review.
use v5.42;
my $x = 1;
my $y = 3;
if ($x = 0 && $y) {
    say "a";
}
say $x;
