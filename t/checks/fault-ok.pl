# check: ok
# kind: fault
# What a fault test is: the program stopped where perl warned and went on,
# having printed only the start of what perl prints. The .stdout stands
# for what a compiled program printed, since nothing can fault yet.
use v5.42;
say "one";
say "two";
my $u;
say $u + 1;
say "four";
