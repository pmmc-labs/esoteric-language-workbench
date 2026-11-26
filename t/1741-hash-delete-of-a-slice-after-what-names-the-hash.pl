# kind: refused
# perl: 1213.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @l = (@h{"a", "b"}, delete @h{"a", "c"});
say @l;
