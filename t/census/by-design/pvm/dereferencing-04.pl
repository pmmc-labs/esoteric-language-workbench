use v5.42;
my @a = (10, 20, 30);
my $r = \@a;
my @c = @$r;
print scalar(@c), " ", $c[0], "\n";
