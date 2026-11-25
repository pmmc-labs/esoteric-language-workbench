# kind: refused
# substr is a list operator to perl, as say is: it takes $x for a file
# handle and doesn't compile, Missing comma after first argument to
# substr function (T125). Found by the review.
use v5.42;
my $x = 5;
say substr($x -1, 0);
