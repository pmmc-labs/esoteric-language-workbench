# kind: refused
# perl reads the name $x_y, which is not declared (T205).
use v5.42;
my $x = 3;
say "$x_y";
