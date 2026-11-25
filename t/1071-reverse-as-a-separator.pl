# kind: refused
# join's separator is one value (T182), and a reverse there is perl's other
# reverse.
use v5.42;
my @a = (1, 2);
say join(reverse(@a), 1, 2);
