use v5.42;
# One index each, and no warning: perl's test is on the characters between
# the brackets (letters, digits, blanks, $ # + - ' "), not on the tree.
my @a = (4, 5, 6);
my @b = (0);
my $j = 0;
sub f() { return 1 }
my @r = @a[0,];
@r = @a[(0)];
@r = @a[$j * 1];
@r = @a[$j ** 1];
@r = @a[$a[0] - 4];
@r = @a[f()];
@r = @a[@b];
@r = @a[0 .. 0];
@r = @a[0.5];
@r = @a[!$j];
@r = @a[
0
];
@r = (@a)[0];
say scalar(@r);
