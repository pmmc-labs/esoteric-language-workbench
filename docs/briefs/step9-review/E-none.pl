use v5.42;
# Q4(a): a sub that returns nothing, in each list position.
sub none() { return }
sub g() { return none() }
sub h() { none() }
sub k($c) { return $c ? none() : 5 }
my @a = (1, 2, 3);
my @c = g();
say scalar(@c);
@c = h();
say scalar(@c);
@c = k(1);
say scalar(@c);
@c = (1, none(), 2);
say scalar(@c);
@c = (none()) x 3;
say scalar(@c);
@c = (1, none())[1];
say scalar(@c);
@c = @a[none()];
say scalar(@c);
say "a", none(), "b";
say none();
for my $x (none()) { say "never"; }
say push(@c, none());
my ($p) = none();
say defined($p) ? 1 : 0;
@c = (none(), 7)[0];
say $c[0];
push @a, none(), 5;
say scalar(@a);
