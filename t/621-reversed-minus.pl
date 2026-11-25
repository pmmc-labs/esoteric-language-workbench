# kind: refused
# perl warns: Reversed -= operator (T127). Found by the review.
use v5.42;
my $y = 2;
my $x =- $y;
say $x;
