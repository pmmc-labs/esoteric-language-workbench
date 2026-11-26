use v5.42;
my @a = (1, 2, 3); my @g = grep { $_ = 9 } @a[0, 1]; print "@a|@g\n";
