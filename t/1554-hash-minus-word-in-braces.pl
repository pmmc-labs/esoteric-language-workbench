# kind: refused
# the key -bar, to perl: 0.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say defined($h{-bar}) ? 1 : 0;
