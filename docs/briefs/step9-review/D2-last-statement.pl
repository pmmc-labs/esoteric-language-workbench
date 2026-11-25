use v5.42;
# A list assignment that ends a sub is the sub's value: a count, or the targets.
my @g;
my ($p, $q);
sub f1() { @g = (7, 8, 9) }
sub f2() { my @l = (7, 8) }
sub f3() { ($p, $q) = (4, 5, 6) }
sub f4() { my ($l) = (7, 8) }
my $s = f1();
my @l = f1();
say $s, " ", scalar(@l);
$s = f2();
@l = f2();
say $s, " ", scalar(@l);
$s = f3();
@l = f3();
say $s, " ", scalar(@l);
$s = f4();
@l = f4();
say $s, " ", scalar(@l);
