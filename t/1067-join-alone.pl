# kind: refused
# perl: Useless use of join or string in void context.
use v5.42;
my @a = (1, 2);
join(",", @a);
