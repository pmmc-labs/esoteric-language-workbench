# check: fails: perl does not compile it in silence
# kind: fault
# perl warns as it compiles, so the language refuses the program (D15),
# and a program that is refused can't be a fault test.
use v5.42;
say "one";
my $x = 1;
my $x = 2;
my $u;
say $u + 1;
