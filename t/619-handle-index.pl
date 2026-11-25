# kind: refused
# perl doesn't compile it: Missing comma after first argument to index
# function (T125).
use v5.42;
my $x = "abc";
say index($x .5, "c");
