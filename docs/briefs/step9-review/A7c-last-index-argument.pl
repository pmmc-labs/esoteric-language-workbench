use v5.42;
# `$#a` as an argument, or in a foreach's list, is read late; a count is not.
my @a = (1, 2, 3);
sub f($x, $y) { return $x }
sub grow() { push @a, 4; return 0 }
say f($#a, grow());
say f(scalar(@a), grow());
say $#a + grow();
my @b = ($#a, grow());
say $b[0];
