# kind: refused
# A grep's block is a test (D53): perl warns that == was meant.
use v5.42;
my @a = (1, 2);
my $x = 0;
my @r = grep { $x = 5 } @a;
