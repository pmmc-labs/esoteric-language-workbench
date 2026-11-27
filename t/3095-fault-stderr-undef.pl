# kind: fault
# An undef in say STDERR's list: perl warns.
use v5.42;
my $u;
say "out";
say STDERR "a", $u;
