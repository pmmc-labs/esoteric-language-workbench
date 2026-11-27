# kind: refused
# perl dies: Can't call method 'size' on unblessed reference.
use v5.42;
my $r = [1, 2];
say $r->size;
