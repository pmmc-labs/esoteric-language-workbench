# kind: refused
# perl runs it: 2.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @k = ("b");
say "$h{$k[0]}";
