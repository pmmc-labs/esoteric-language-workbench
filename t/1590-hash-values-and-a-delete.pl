# kind: refused
# perl: 5.
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
my @l = (values(%h), delete($h{a}));
say scalar(@l);
