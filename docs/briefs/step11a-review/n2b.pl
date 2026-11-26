use v5.42;
# N2: T175 with an interpolated string: perl does not compile it.
my @a = (1, 2);
my @r = map { "$_", 1 } @a;
