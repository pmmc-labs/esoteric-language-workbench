use v5.42;
my @a = (3, 1, 2);
my @b = sort @a;
my $n = () = sort @a;
my @c = (() = sort @a);
print "@b $n ", scalar(@c), "\n";
