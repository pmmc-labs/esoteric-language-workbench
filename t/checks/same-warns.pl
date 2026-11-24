# check: fails: perl wrote to stderr
# perl prints the 1 the .expected has, and warns of an uninitialized value:
# where perl warns the language faults (D15), so this is no same test.
use v5.42;
my $u;
say $u + 1;
