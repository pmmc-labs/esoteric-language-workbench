use v5.42;
# t1 is freed by the allocation inside the second `.`, after to_str has
# passed it, and its poison is copied into t2; only t2's length is asked
# for. With the temporaries left out of the mark this prints what perl
# prints, and no check in to_str ever sees a dead string.
my $p = "p";
my $q = "q";
say length(($p . $q) . $p);
