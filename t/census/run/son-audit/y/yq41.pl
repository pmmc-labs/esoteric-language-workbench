use v5.42;
my @a=(1); (my @c = @a) = (7,8); print "@a@c\n";
