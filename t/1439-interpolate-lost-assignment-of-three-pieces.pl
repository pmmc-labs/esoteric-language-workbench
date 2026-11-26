# kind: refused
# perl prints taza and then u (T212).
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
my $z = "z";
$t .= ($u = "$x$z$x");
say $t;
say $u;
