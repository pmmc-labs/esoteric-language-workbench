# check: fails: the .expected is not what the program printed
# kind: fault
# A fault test's .expected ends with the fault's line and exit: 1.
use v5.42;
say "one";
my $u;
say $u + 1;
