# kind: refused
# perl takes f + 1 for f(+1), and dies: Too many arguments for subroutine 'main::f'.
use v5.42;
sub f() { return 1; }
my $x = f + 1;
say $x;
