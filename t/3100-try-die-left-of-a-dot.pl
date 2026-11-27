# kind: refused
# perl warns: Possible precedence issue with control flow operator (die).
use v5.42;
my $x = die("x") . "y";
