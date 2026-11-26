# kind: refused
# perl prints 3.
use v5.42;
my @a = (1, 2, 3);
my $i = 1;
say "$a[$i + 1]";
