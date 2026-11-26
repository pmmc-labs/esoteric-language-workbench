use v5.42;
my @a = (10);
my @tail = (20, 30);
push @a, @tail;
print scalar(@tail), "\n";
print scalar(@a), "\n";
print $a[2], "\n";
