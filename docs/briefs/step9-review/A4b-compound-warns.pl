use v5.42;
my @a = (0);
$a[0] ||= pop(@a);
say scalar(@a);
