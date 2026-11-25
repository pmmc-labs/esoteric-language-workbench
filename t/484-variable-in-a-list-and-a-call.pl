# kind: refused
# perl makes the list 9 5: the variable is read when the list is used (T157, D76).
use v5.42;
my $x = 1;
sub bump() { $x = 9; return 5; }
my @b = ($x, bump());
say $b[0];
