# kind: refused
# perl reads $x::y, undef and a warning (T199).
use v5.42;
my $x = 3;
say "$x::y";
