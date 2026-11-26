# kind: refused
# perl runs it: 1.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my $k = "a";
say "$h{$k . q()}";
