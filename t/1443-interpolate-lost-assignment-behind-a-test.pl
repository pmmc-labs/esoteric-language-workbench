# kind: refused
# perl prints taz and then u (T212).
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
my $z = "z";
$t .= ($u = (1 ? "$x$z" : 0));
say $t;
say $u;
