# kind: refused
# perl takes it for the key 1, which is not there, and warns.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say "$h{1}";
