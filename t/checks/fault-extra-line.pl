# check: fails: printed something perl does not
# kind: fault
# The program printed a line perl doesn't before it stopped: a wrong
# answer, however loudly it ended (D12).
use v5.42;
say "one";
my $u;
say $u + 1;
