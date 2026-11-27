# check: fails: perl warned as it ran
# kind: warns
# An undef in warn's list is a warning of perl's too.
use v5.42;
my $u;
warn $u;
