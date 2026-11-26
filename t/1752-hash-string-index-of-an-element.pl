# kind: refused
# perl dies: Can't use string ("1") as an ARRAY ref (T227).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say "$h{a}[0]";
