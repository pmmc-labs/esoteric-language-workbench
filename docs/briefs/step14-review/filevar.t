### closure-before-my-init
my $c = get();
say defined $c->() ? "def" : "undef";
my $x = 5;
say $c->();
sub get() { return sub { $x } }
### closure-before-my-noinit
my $c = get();
$c->(3);
my $x;
say defined $x ? "def:$x" : "undef";
sub get() { return sub ($v) { $x = $v } }
### closure-before-my-array
my $c = get();
$c->();
my @a;
say scalar(@a);
sub get() { return sub { push @a, 1 } }
### closure-before-my-array-init
my $c = get();
$c->();
my @a = (7);
say scalar(@a), " ", $c->();
sub get() { return sub { push @a, 1; scalar(@a) } }
### identity-before-and-after
my $c1 = get();
my $x = 1;
my $c2 = get();
say $c1 == $c2 ? "same" : "diff";
$x = 9; say $c1->(), $c2->();
sub get() { return sub { $x } }
