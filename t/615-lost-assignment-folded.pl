# kind: refused
# perl folds the ? : away first, and then loses the assignment as in
# 614: it prints ta-|u (T129).
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
$t .= (1 ? ($u = $x . "-") : 0);
say $t . "|" . $u;
