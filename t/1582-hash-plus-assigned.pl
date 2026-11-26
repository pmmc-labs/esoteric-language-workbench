# kind: refused
# perl does not compile it: Can't modify private hash in addition (+).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
%h += 1;
