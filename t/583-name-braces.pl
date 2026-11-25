# kind: refused
# perl takes ${x} for $x, and warns here: Ambiguous use of ${x}
# resolved to $x (D55).
use v5.42;
my $x = 1;
say ${x};
