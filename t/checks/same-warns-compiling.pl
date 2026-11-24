# check: fails: perl does not compile it in silence
# The warning comes from perl -c, before anything runs: a refusal (D15).
use v5.42;
my $x = 1;
my $x = 2;
say $x;
