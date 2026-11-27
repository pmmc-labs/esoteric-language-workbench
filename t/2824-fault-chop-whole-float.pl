# kind: fault
# perl makes the string 1e+15, and chops it to 1e+1 (D36).
use v5.42;
my $x = 1e15;
chop($x);
say $x;
