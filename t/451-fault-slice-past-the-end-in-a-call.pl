# kind: fault
# A slice past the end of its array, among a call's arguments: perl makes
# the elements, and the array is seven long afterwards (T161). A fault.
# Read as an element, or assigned to an array, it is two undefs and
# nothing is made.
use v5.42;
sub count($p = "-", $q = "-") { return defined($p) ? "defined" : "undef" }
my @c = (1, 2);
my @t = @c[5, 6];
say scalar(@t), " ", scalar(@c);
say count(@c[0, 1]);
say count(@c[5, 6]);
say "not reached";
