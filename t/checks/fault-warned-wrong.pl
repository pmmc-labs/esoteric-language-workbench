# check: fails: wrote to stderr what perl does not
# kind: fault
# The program wrote to stderr what perl does not.
use v5.42;
warn "w\n";
my $n = "abc" + 1;
