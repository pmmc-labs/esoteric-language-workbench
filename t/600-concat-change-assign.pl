# kind: refused
# perl's .= with a row of dots on its right is one operation too
# (T117, D57).
use v5.42;
my $x = 3;
$x .= "a" . $x++;
