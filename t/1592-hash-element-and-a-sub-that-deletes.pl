# kind: refused
# perl: 2.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
sub del() { delete $h{a}; return 1 }
say $h{a} + del();
