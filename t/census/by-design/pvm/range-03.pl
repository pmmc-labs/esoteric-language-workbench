use v5.42;
my @on = (0, 1, 0, 0, 0, 0);
my @off = (0, 0, 0, 0, 1, 0);
my @i = (0, 1, 2, 3, 4, 5);
my @o = grep { $on[$_] .. $off[$_] } @i;
print "@o\n";
