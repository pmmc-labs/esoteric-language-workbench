use v5.42;
our $answer = 42;
print "found: [", exists $::{answer}, "]\n";
print "gone: [", exists $::{nosuch}, "]\n";
my %stash = %::;
print "stash: [", exists $stash{answer}, "]\n";
