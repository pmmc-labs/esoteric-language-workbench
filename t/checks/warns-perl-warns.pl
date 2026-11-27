# check: fails: perl warned as it ran
# kind: warns
# perl warns of the undef, which the program does not: the check must see it.
use v5.42;
my $u;
my $x = "a" . $u;
warn "w\n";
