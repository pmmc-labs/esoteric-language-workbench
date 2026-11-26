# kind: refused
# perl warns: Scalar value @h{"a"} better written as $h{"a"}.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
delete @h{"a"};
