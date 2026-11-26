# kind: refused
# perl does not compile it: Missing right curly or square bracket.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say "$h{a";
