# kind: fault
# An undef in a warn's list (15b): perl warns twice.
use v5.42;
my $u;
say "before";
warn $u;
say "after";
