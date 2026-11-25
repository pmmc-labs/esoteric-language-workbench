# kind: refused
# perl prints 95 (T157, D76).
use v5.42;
my $x = 1;
sub bump() { $x = 9; return 5; }
say $x, bump();
