# kind: refused
# perl dies: Can't use string ("1") as a HASH ref.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say $h{a}{b};
