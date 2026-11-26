# kind: refused
# perl dies: Can't use string ("1") as a HASH ref.
use v5.42;
my $r = 1;
say %$r;
