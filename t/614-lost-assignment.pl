# kind: refused
# perl 5.42 prints ta1 and then u: it makes one operation of the .=, the
# = and the dot, and never assigns $u (T129). Found by the review.
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
my $z = "1";
$t .= ($u = $x . $z);
say $t;
say $u;
