# kind: refused
# perl prints taa and then u (T198).
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
my $z = "z";
$t .= ($u = "a$x");
say $t;
say $u;
