use v5.42;
my @a = (10, 20, 30);
my @r = splice @a, 1, 1, 40, 50;
print $r[0], "\n";
print scalar(@a), "\n";
print $a[2], "\n";
