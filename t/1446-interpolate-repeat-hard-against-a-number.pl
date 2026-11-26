# kind: refused
# perl prints a3a3; refused as of any string (T57).
use v5.42;
my $x = 3;
say "a$x" x2;
