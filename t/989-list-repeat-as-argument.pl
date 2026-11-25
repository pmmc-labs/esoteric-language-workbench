# kind: refused
# perl hands g no argument, and prints g's default (T143).
use v5.42;
sub g($p = "d") { return $p; }
my $n = 0;
say g(("a") x $n);
