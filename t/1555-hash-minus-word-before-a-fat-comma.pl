# kind: refused
# the key -bar, to perl: -bar,x.
use v5.42;
my %g = (-bar => 1, x => 2);
say join(",", sort keys %g);
