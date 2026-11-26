use v5.42;
my @a = (20, 30);
my @head = (10);
unshift @a, @head;
print scalar(@head), "\n";
print scalar(@a), "\n";
print $a[0], "\n";
