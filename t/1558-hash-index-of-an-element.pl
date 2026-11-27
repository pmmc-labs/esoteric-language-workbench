# kind: fault
# perl dies: Can't use string ("1") as an ARRAY ref. Refused until step 13a,
# and a fault since (D107).
use v5.42;
my %h = (a => 1, b => 2, c => 3, d => 4);
say $h{a}[0];
