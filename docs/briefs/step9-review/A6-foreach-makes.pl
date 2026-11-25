use v5.42;
# An element past the end in a foreach's list, or a slice in a call, is made.
my @a;
for my $x ($a[5]) { say scalar(@a); }
say scalar(@a);
my @b;
for my $x (@b[5, 6]) { }
say scalar(@b);
sub f($x = 0, $y = 0) { return 1 }
my @c;
f($c[5]);
say scalar(@c);
f(@c[5, 6]);
say scalar(@c);
my @d;
my $r = $d[5] // 0;
my @t = @d[5, 6];
say scalar(@d), " ", scalar(@t);
