use v5.42;
# An offset or a length too large for a whole number wraps.
my @a = (1, 2, 3, 4, 5);
my @r = splice(@a, 0, 1e30);
say scalar(@r), " ", scalar(@a);
@a = (1, 2, 3, 4, 5);
@r = splice(@a, 1e30);
say scalar(@r), " ", scalar(@a);
@a = (1, 2, 3, 4, 5);
@r = splice(@a, 0, 9223372036854775807);
say scalar(@r), " ", scalar(@a);
@a = (1, 2, 3, 4, 5);
@r = splice(@a, 0, -1e30);
say scalar(@r), " ", scalar(@a);
