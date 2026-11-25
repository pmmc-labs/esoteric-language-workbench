use v5.42;
# perl warns of an offset past the end only when a length is given.
my @a = (1, 2, 3, 4, 5);
my @r = splice(@a, 6);
say scalar(@r), " ", scalar(@a);
@r = splice(@a, 2147483648);
say scalar(@r), " ", scalar(@a);
@r = splice(@a, 6, 0);
say scalar(@r), " ", scalar(@a);
splice(@a, 6, 0, 7);
say scalar(@a), " ", $a[5];
