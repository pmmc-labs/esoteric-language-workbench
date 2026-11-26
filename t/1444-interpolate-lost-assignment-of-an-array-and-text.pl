# kind: refused
# perl prints t1 2 3- and then u (T198).
use v5.42;
my @a = (1, 2, 3);
my $t = "t";
my $u = "u";
$t .= ($u = "@a-");
say $t;
say $u;
