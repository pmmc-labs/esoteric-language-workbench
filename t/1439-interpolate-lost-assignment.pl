# kind: refused
# perl prints taz and then u: $u is never assigned (T198).
use v5.42;
my $t = "t";
my $u = "u";
my $x = "a";
my $z = "z";
$t .= ($u = "$x$z");
say $t;
say $u;
