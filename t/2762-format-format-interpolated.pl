# kind: refused
# perl reads the % in $p as a conversion: 5.
use v5.42;
my $p = "%d";
say sprintf("<$p>", 5);
