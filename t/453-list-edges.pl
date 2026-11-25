# Two edges the first breaking of step 9a's code did not see
# (docs/briefs/step9a-mutations.py): a splice's length that is past the
# end from where it starts, though not past the array's own length; and
# the left side of || && // in a list, when it is the one given.
use v5.42;
my @a = (0, 1, 2, 3, 4, 5);
my @gone = splice(@a, 4, 3);
say $gone[0], $gone[1], " ", scalar(@gone), " ", scalar(@a);
@a = (0, 1, 2, 3, 4, 5);
@gone = splice(@a, 2, 5, 9);
say scalar(@gone), " ", scalar(@a), " ", $a[2];
@a = (0, 1, 2, 3, 4, 5);
@gone = splice(@a, 5, 6);
say scalar(@gone), " ", scalar(@a);
my $t = 7;
my $f = 0;
my $u;
my @r = ($t || (1, 2));
say scalar(@r), " ", $r[0];
@r = ($f || (1, 2));
say scalar(@r), " ", $r[0];
@r = ($f && (1, 2));
say scalar(@r), " ", $r[0];
@r = ($t && (1, 2));
say scalar(@r), " ", $r[0];
@r = ($t // (1, 2));
say scalar(@r), " ", $r[0];
@r = ($u // (1, 2));
say scalar(@r), " ", $r[0];
@r = (8, $t + 1 || @a, 9);
say scalar(@r), " ", $r[1];
