# kind: refused
# perl takes it, and warns nothing here: 9.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
@h{"a"} = (9);
say $h{a};
