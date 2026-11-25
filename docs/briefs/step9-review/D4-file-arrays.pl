use v5.42;
# T156 for each shape of `my`.
fill();
my @a;
say scalar(@a);
fill();
my ($n, @b);
say scalar(@b);
fill();
my ($m, @c) = (5);
say scalar(@c);
fill();
my @d = ();
say scalar(@d);
fill();
my ($s, $t) = (1);
say defined($t) ? 1 : 0;
sub fill() { push @a, 1, 2; push @b, 1; push @c, 1; push @d, 1; $t = 5; }
